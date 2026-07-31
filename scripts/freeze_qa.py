#!/usr/bin/env python3
"""Freeze a compact, source-bound QA attestation from ignored render output."""

from __future__ import annotations

import argparse
import hashlib
import json
import tomllib
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

try:
    from scripts.review_site import (
        REVIEW_ROOT,
        ReviewSiteError,
        load_reviewable_lesson,
        read_review_state,
    )
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from review_site import (  # type: ignore[no-redef]
        REVIEW_ROOT,
        ReviewSiteError,
        load_reviewable_lesson,
        read_review_state,
    )


ROOT = Path(__file__).resolve().parents[1]
LESSON_PATTERN = "lessons/*/*/lesson.toml"
VERIFIED_STATES = {"visual_verified", "published"}


def load_lessons() -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for metadata_path in sorted(ROOT.glob(LESSON_PATTERN)):
        with metadata_path.open("rb") as handle:
            lesson = tomllib.load(handle)
        lesson["metadata_path"] = metadata_path
        lesson_id = lesson["id"]
        if lesson_id in lessons:
            raise ValueError(f"duplicate lesson id: {lesson_id}")
        lessons[lesson_id] = lesson
    return lessons


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def safe_id(lesson_id: str) -> str:
    return lesson_id.replace(".", "_")


def require_ready_review(lesson: dict[str, Any]) -> None:
    review_lesson = {
        **lesson,
        "metadata_path": str(lesson["metadata_path"].relative_to(ROOT)),
    }
    try:
        record = load_reviewable_lesson(review_lesson, {})
        state = read_review_state(record, REVIEW_ROOT)
    except ReviewSiteError as error:
        raise ValueError(
            f"{lesson['id']}: local review evidence is invalid: {error}"
        ) from error
    if state.get("stale") or not state.get("review", {}).get("ready"):
        raise ValueError(
            f"{lesson['id']}: complete the current local review before freezing QA"
        )


def freeze_lesson(lesson: dict[str, Any], human_reviewed: bool) -> Path:
    lesson_id = lesson["id"]
    if lesson["production_state"] not in VERIFIED_STATES:
        raise ValueError(
            f"{lesson_id}: state {lesson['production_state']} is not verified"
        )
    if not human_reviewed:
        raise ValueError(
            "refusing to attest visual QA without --human-reviewed"
        )
    require_ready_review(lesson)

    report_path = ROOT / "build" / "qa" / f"{safe_id(lesson_id)}.json"
    if not report_path.is_file():
        raise ValueError(f"{lesson_id}: missing live QA report {report_path}")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("status") != "ok" or report.get("errors"):
        raise ValueError(f"{lesson_id}: live QA report is not clean")
    if report.get("id") != lesson_id:
        raise ValueError(f"{lesson_id}: live QA report ID differs")
    if report.get("scene_class") != lesson["scene_class"]:
        raise ValueError(f"{lesson_id}: live QA scene class differs")

    beats = lesson.get("beats", [])
    expected_ids = [beat["id"] for beat in beats]
    expected_loops = [bool(beat.get("loop")) for beat in beats]
    segments = report.get("segments", [])
    actual_ids = [segment.get("beat_id") for segment in segments]
    actual_loops = [bool(segment.get("loop")) for segment in segments]
    if actual_ids != expected_ids:
        raise ValueError(f"{lesson_id}: live QA beat IDs differ from metadata")
    if actual_loops != expected_loops:
        raise ValueError(f"{lesson_id}: live QA loop flags differ from metadata")
    if any(segment.get("resolution") != [1920, 1080] for segment in segments):
        raise ValueError(f"{lesson_id}: live QA contains a non-1920x1080 segment")

    source_fields = ("scene_file", "presenter_script", "storyboard")
    source_hashes: dict[str, dict[str, str]] = {}
    source_hashes["lesson_metadata"] = {
        "path": str(lesson["metadata_path"].relative_to(ROOT)),
        "sha256": sha256(lesson["metadata_path"]),
    }
    for field in source_fields:
        relative_path = lesson[field]
        path = ROOT / relative_path
        if not path.is_file():
            raise ValueError(f"{lesson_id}: missing {field}: {relative_path}")
        source_hashes[field] = {
            "path": relative_path,
            "sha256": sha256(path),
        }

    loop_endpoints = [
        {
            "beat_id": segment["beat_id"],
            "mean_absolute_difference": segment[
                "loop_endpoint_mean_absolute_difference"
            ],
        }
        for segment in segments
        if segment.get("loop")
    ]
    manifest_path = ROOT / "slides" / f"{lesson['scene_class']}.json"
    if not manifest_path.is_file():
        raise ValueError(f"{lesson_id}: missing Slides manifest {manifest_path}")
    rendered_segments = []
    for segment in segments:
        relative_path = segment["file"]
        path = ROOT / relative_path
        if not path.is_file():
            raise ValueError(f"{lesson_id}: missing rendered segment {path}")
        rendered_segments.append(
            {
                "beat_id": segment["beat_id"],
                "path": relative_path,
                "sha256": sha256(path),
                "duration": float(segment["duration"]),
            }
        )

    evidence = {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "scene_class": lesson["scene_class"],
        "verified_at": datetime.now(UTC).date().isoformat(),
        "status": "ok",
        "review": {
            "mechanical": "passed",
            "visual": "human_reviewed",
            "mathematics": lesson["independent_check"],
        },
        "render": {
            "segment_count": len(segments),
            "resolution": [1920, 1080],
            "manifest": {
                "path": str(manifest_path.relative_to(ROOT)),
                "sha256": sha256(manifest_path),
            },
            "segments": rendered_segments,
            "beats": [
                {"id": beat_id, "loop": loop}
                for beat_id, loop in zip(expected_ids, expected_loops, strict=True)
            ],
            "loop_endpoints": loop_endpoints,
        },
        "source_hashes": source_hashes,
        "toolchain_hashes": {
            relative_path: sha256(ROOT / relative_path)
            for relative_path in ("pixi.toml", "pixi.lock")
        },
    }
    output_dir = ROOT / "qa"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{safe_id(lesson_id)}.json"
    output_path.write_text(
        json.dumps(evidence, ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument(
        "--human-reviewed",
        action="store_true",
        help="attest that all settled and relevant transition frames were reviewed",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    lessons = load_lessons()
    selected_ids = args.ids or [
        lesson_id
        for lesson_id, lesson in lessons.items()
        if lesson["production_state"] in VERIFIED_STATES
    ]
    missing = sorted(set(selected_ids) - lessons.keys())
    if missing:
        raise SystemExit("unknown lesson id(s): " + ", ".join(missing))
    try:
        for lesson_id in sorted(selected_ids):
            output_path = freeze_lesson(lessons[lesson_id], args.human_reviewed)
            print(f"frozen: {lesson_id}: {output_path.relative_to(ROOT)}")
    except ValueError as error:
        raise SystemExit(f"ERROR: {error}") from error
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
