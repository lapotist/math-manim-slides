#!/usr/bin/env python3
"""Run mechanical media checks against rendered Manim Slides segments."""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_lessons() -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for path in sorted(ROOT.glob("lessons/*/*/lesson.toml")):
        with path.open("rb") as handle:
            lesson = tomllib.load(handle)
        lessons[lesson["id"]] = lesson
    return lessons


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


def write_preview(path: Path, at_seconds: float, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
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
    safe_id = lesson["id"].replace(".", "_")
    preview_dir = ROOT / "build" / "qa" / "frames" / safe_id
    preview_paths: list[Path] = []
    for index, (slide, beat) in enumerate(
        zip(slides, lesson["beats"], strict=True),
        start=1,
    ):
        media_path = ROOT / slide["file"]
        if not media_path.is_file():
            errors.append(f"beat {index:02}: missing {slide['file']}")
            continue
        media = probe(media_path)
        sample_at = min(0.15, media["duration"] / 2)
        first = gray_frame(media_path, sample_at)
        last_at = max(media["duration"] - 0.15, sample_at)
        last = gray_frame(media_path, last_at)
        preview_path = preview_dir / f"{index:02d}-{beat['id']}.png"
        write_preview(media_path, last_at, preview_path)
        preview_paths.append(preview_path)
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
                "duration": media["duration"],
                "resolution": [media["width"], media["height"]],
                "first_frame": first_stats,
                "last_frame": last_stats,
                "preview": str(preview_path.relative_to(ROOT)),
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
    return {
        "id": lesson["id"],
        "scene_class": scene_class,
        "status": "ok" if not errors else "failed",
        "errors": errors,
        "contact_sheet": str(contact_sheet.relative_to(ROOT)),
        "segments": segments,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="+")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lessons = load_lessons()
    unknown = sorted(set(args.ids) - lessons.keys())
    if unknown:
        print("ERROR: unknown lesson IDs: " + ", ".join(unknown), file=sys.stderr)
        return 2

    report_dir = ROOT / "build" / "qa"
    report_dir.mkdir(parents=True, exist_ok=True)
    failed = False
    for lesson_id in args.ids:
        try:
            result = qa_lesson(lessons[lesson_id])
        except (ValueError, subprocess.CalledProcessError) as error:
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
