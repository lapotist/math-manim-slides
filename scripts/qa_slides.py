#!/usr/bin/env python3
"""Run mechanical media checks against rendered Manim Slides segments."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import sys
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SWEEP_CADENCE_SECONDS = 0.5
QA_SCHEMA_VERSION = 2
RENDER_BOUND_ROLES = {"scene_file", "shared_python"}
REQUIRED_COMMANDS = ("ffmpeg", "ffprobe", "montage")


def load_lessons() -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for path in sorted(ROOT.glob("lessons/*/*/lesson.toml")):
        with path.open("rb") as handle:
            lesson = tomllib.load(handle)
        lesson["metadata_path"] = str(path.relative_to(ROOT))
        lessons[lesson["id"]] = lesson
    return lessons


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_record(path: Path, *, role: str | None = None) -> dict[str, str]:
    record = {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256(path),
    }
    if role is not None:
        record["role"] = role
    return record


def review_input_paths(lesson: dict[str, Any]) -> list[tuple[str, Path]]:
    paths = [
        ("lesson_metadata", ROOT / lesson["metadata_path"]),
        ("scene_file", ROOT / lesson["scene_file"]),
        ("presenter_script", ROOT / lesson["presenter_script"]),
        ("storyboard", ROOT / lesson["storyboard"]),
        ("toolchain", ROOT / "pixi.toml"),
        ("toolchain", ROOT / "pixi.lock"),
    ]
    paths.extend(("shared_python", path) for path in sorted((ROOT / "src").rglob("*.py")))
    missing = [str(path.relative_to(ROOT)) for _, path in paths if not path.is_file()]
    if missing:
        raise ValueError("missing review input(s): " + ", ".join(missing))
    return paths


def select_lessons(
    lessons: dict[str, dict[str, Any]],
    requested: list[str],
    status: str | None,
) -> list[dict[str, Any]]:
    if requested:
        missing = sorted(set(requested) - lessons.keys())
        if missing:
            raise ValueError("unknown lesson ID(s): " + ", ".join(missing))
        selected = [lessons[lesson_id] for lesson_id in requested]
    else:
        selected = list(lessons.values())
    if status:
        statuses = {value.strip() for value in status.split(",") if value.strip()}
        if not statuses:
            raise ValueError("status filter is empty")
        selected = [
            lesson for lesson in selected if lesson.get("production_state") in statuses
        ]
    if not requested and not status:
        raise ValueError("provide lesson IDs or --status")
    if not selected:
        raise ValueError("no lessons matched the QA selection")
    return sorted(selected, key=lambda lesson: lesson["id"])


def missing_commands() -> list[str]:
    return [command for command in REQUIRED_COMMANDS if shutil.which(command) is None]


def probe(path: Path) -> dict[str, Any]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-select_streams",
        "v:0",
        "-show_entries",
        "stream=width,height:format=duration",
        "-of",
        "json",
        str(path),
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    data = json.loads(completed.stdout)
    stream = data["streams"][0]
    return {
        "width": int(stream["width"]),
        "height": int(stream["height"]),
        "duration": float(data["format"]["duration"]),
    }


def gray_frame(path: Path, at_seconds: float) -> bytes:
    command = [
        "ffmpeg",
        "-v",
        "error",
        "-ss",
        f"{at_seconds:.6f}",
        "-i",
        str(path),
        "-frames:v",
        "1",
        "-f",
        "rawvideo",
        "-pix_fmt",
        "gray",
        "pipe:1",
    ]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout


def write_preview(
    path: Path,
    at_seconds: float,
    output: Path,
    *,
    scale_width: int | None = None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    filters = [] if scale_width is None else ["-vf", f"scale={scale_width}:-2"]
    quality = ["-q:v", "3"] if output.suffix.lower() in {".jpg", ".jpeg"} else []
    subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-ss",
            f"{at_seconds:.6f}",
            "-i",
            str(path),
            "-frames:v",
            "1",
            *filters,
            *quality,
            "-y",
            str(output),
        ],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def frame_stats(frame: bytes) -> dict[str, float]:
    if not frame:
        raise ValueError("ffmpeg returned an empty frame")
    count = len(frame)
    mean = sum(frame) / count
    square_mean = sum(value * value for value in frame) / count
    variance = max(square_mean - mean * mean, 0.0)
    return {"mean_luma": mean, "luma_stddev": math.sqrt(variance)}


def mean_absolute_difference(first: bytes, last: bytes) -> float:
    if len(first) != len(last):
        raise ValueError("loop endpoint frames have different sizes")
    return sum(abs(a - b) for a, b in zip(first, last, strict=True)) / len(first)


def sweep_sample_times(
    duration: float,
    *,
    cadence: float = SWEEP_CADENCE_SECONDS,
    inset: float = 0.15,
) -> list[float]:
    """Return fixed-cadence samples, including readable segment endpoints."""
    if duration <= 0:
        raise ValueError("segment duration must be positive")
    if cadence <= 0:
        raise ValueError("sweep cadence must be positive")
    first = min(inset, duration / 2)
    last = max(duration - inset, first)
    times = [first]
    next_time = first + cadence
    while next_time < last - 1e-6:
        times.append(next_time)
        next_time += cadence
    if last - times[-1] > 1e-6:
        times.append(last)
    return [round(sample, 6) for sample in times]


def qa_lesson(lesson: dict[str, Any]) -> dict[str, Any]:
    scene_class = lesson["scene_class"]
    manifest_path = ROOT / "slides" / f"{scene_class}.json"
    if not manifest_path.is_file():
        raise ValueError(f"{lesson['id']}: no Slides manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    slides = manifest["slides"]
    if len(slides) != len(lesson["beats"]):
        raise ValueError(f"{lesson['id']}: manifest/beat count differs")

    segments: list[dict[str, Any]] = []
    errors: list[str] = []
    input_paths = review_input_paths(lesson)
    inputs_newer_than_render = [
        str(path.relative_to(ROOT))
        for role, path in input_paths
        if role in RENDER_BOUND_ROLES
        and path.stat().st_mtime_ns > manifest_path.stat().st_mtime_ns
    ]
    if inputs_newer_than_render:
        errors.append(
            "render predates review input(s): "
            + ", ".join(inputs_newer_than_render)
        )
    safe_id = lesson["id"].replace(".", "_")
    preview_dir = ROOT / "build" / "qa" / "frames" / safe_id
    if preview_dir.exists():
        shutil.rmtree(preview_dir)
    preview_paths: list[Path] = []
    sweep_paths: list[Path] = []
    slides_root = (ROOT / "slides").resolve()
    for index, (slide, beat) in enumerate(
        zip(slides, lesson["beats"], strict=True),
        start=1,
    ):
        media_path = ROOT / slide["file"]
        if not media_path.is_file():
            errors.append(f"beat {index:02}: missing {slide['file']}")
            continue
        if not media_path.resolve().is_relative_to(slides_root):
            errors.append(f"beat {index:02}: media is outside slides/")
            continue
        media = probe(media_path)
        sample_at = min(0.15, media["duration"] / 2)
        first = gray_frame(media_path, sample_at)
        last_at = max(media["duration"] - 0.15, sample_at)
        last = gray_frame(media_path, last_at)
        preview_path = preview_dir / f"{index:02d}-{beat['id']}.png"
        write_preview(media_path, last_at, preview_path)
        preview_paths.append(preview_path)
        transition_previews: list[dict[str, Any]] = []
        for sample_number, transition_at in enumerate(
            sweep_sample_times(media["duration"]),
            start=1,
        ):
            transition_frame = gray_frame(media_path, transition_at)
            transition_stats = frame_stats(transition_frame)
            if transition_stats["luma_stddev"] < 0.5:
                errors.append(
                    f"beat {index:02}: sweep frame at {transition_at:.2f}s appears blank"
                )
            transition_path = (
                preview_dir
                / "sweep"
                / f"{index:02d}-{beat['id']}-{sample_number:02d}.jpg"
            )
            write_preview(
                media_path,
                transition_at,
                transition_path,
                scale_width=960,
            )
            sweep_paths.append(transition_path)
            transition_previews.append(
                {
                    **file_record(transition_path),
                    "at_seconds": transition_at,
                }
            )
        first_stats = frame_stats(first)
        last_stats = frame_stats(last)
        if (media["width"], media["height"]) != (1920, 1080):
            errors.append(f"beat {index:02}: media is not 1920x1080")
        if first_stats["luma_stddev"] < 0.5:
            errors.append(f"beat {index:02}: sampled first frame appears blank")
        if last_stats["luma_stddev"] < 0.5:
            errors.append(f"beat {index:02}: sampled last frame appears blank")

        loop_difference = None
        if beat.get("loop"):
            loop_first = first
            loop_last = last
            loop_difference = mean_absolute_difference(loop_first, loop_last)
            if loop_difference > 8.0:
                errors.append(
                    f"beat {index:02}: loop endpoint difference "
                    f"{loop_difference:.2f} exceeds 8.00"
                )
        segments.append(
            {
                "number": index,
                "beat_id": beat["id"],
                "file": slide["file"],
                "sha256": sha256(media_path),
                "duration": media["duration"],
                "resolution": [media["width"], media["height"]],
                "first_frame": first_stats,
                "last_frame": last_stats,
                "preview": {
                    **file_record(preview_path),
                    "at_seconds": last_at,
                },
                "sweep_previews": transition_previews,
                "loop": bool(beat.get("loop")),
                "loop_endpoint_mean_absolute_difference": loop_difference,
            }
        )

    contact_sheet = preview_dir / "contact-sheet.png"
    if preview_paths:
        subprocess.run(
            [
                "montage",
                *(str(path) for path in preview_paths),
                "-thumbnail",
                "480x270",
                "-tile",
                "4x",
                "-geometry",
                "+8+8",
                "-background",
                "#111111",
                str(contact_sheet),
            ],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    sweep_contact_sheet = preview_dir / "transition-sweep.jpg"
    if sweep_paths:
        subprocess.run(
            [
                "montage",
                *(str(path) for path in sweep_paths),
                "-thumbnail",
                "320x180",
                "-tile",
                "5x",
                "-geometry",
                "+6+6",
                "-background",
                "#111111",
                str(sweep_contact_sheet),
            ],
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    return {
        "schema_version": QA_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "id": lesson["id"],
        "scene_class": scene_class,
        "status": "ok" if not errors else "failed",
        "errors": errors,
        "inputs": [file_record(path, role=role) for role, path in input_paths],
        "manifest": file_record(manifest_path),
        "contact_sheet": file_record(contact_sheet),
        "transition_sweep": file_record(sweep_contact_sheet),
        "segments": segments,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument(
        "--status",
        help="Select one production state or a comma-separated set of states.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lessons = load_lessons()
    try:
        selected = select_lessons(lessons, args.ids, args.status)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    missing = missing_commands()
    if missing:
        print(
            "ERROR: slide QA requires these commands: " + ", ".join(missing),
            file=sys.stderr,
        )
        return 2

    report_dir = ROOT / "build" / "qa"
    report_dir.mkdir(parents=True, exist_ok=True)
    failed = False
    for lesson in selected:
        lesson_id = lesson["id"]
        try:
            result = qa_lesson(lesson)
        except (OSError, ValueError, subprocess.CalledProcessError) as error:
            result = {
                "id": lesson_id,
                "status": "failed",
                "errors": [str(error)],
                "segments": [],
            }
        report_path = report_dir / f"{lesson_id.replace('.', '_')}.json"
        report_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(f"{result['status']}: {lesson_id}: {report_path.relative_to(ROOT)}")
        for error in result["errors"]:
            print(f"  {error}", file=sys.stderr)
        failed |= result["status"] != "ok"
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
