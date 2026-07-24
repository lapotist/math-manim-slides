#!/usr/bin/env python3
"""Run Manim Slides actions for cataloged lessons."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tomllib
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LESSON_PATTERN = "lessons/*/*/lesson.toml"
RENDERED_STATES = {"draft_rendered", "visual_verified", "published"}


def load_lessons() -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for path in sorted(ROOT.glob(LESSON_PATTERN)):
        with path.open("rb") as handle:
            lesson = tomllib.load(handle)
        lesson["metadata_path"] = str(path.relative_to(ROOT))
        lesson_id = lesson["id"]
        if lesson_id in lessons:
            raise ValueError(f"duplicate lesson id: {lesson_id}")
        lessons[lesson_id] = lesson
    return lessons


def select_lessons(
    lessons: dict[str, dict[str, Any]],
    requested: list[str],
    status: str | None,
) -> list[dict[str, Any]]:
    if requested:
        missing = sorted(set(requested) - lessons.keys())
        if missing:
            raise ValueError("unknown lesson id(s): " + ", ".join(missing))
        selected = [lessons[lesson_id] for lesson_id in requested]
    else:
        selected = list(lessons.values())
    if status:
        selected = [item for item in selected if item["production_state"] == status]
    return sorted(selected, key=lambda item: item["id"])


def output_path(lesson_id: str) -> Path:
    parts = lesson_id.split(".")
    return ROOT / "dist" / Path(*parts).with_suffix(".html")


def action_command(
    action: str,
    lesson: dict[str, Any],
    quality: str,
) -> list[str]:
    scene_file = lesson["scene_file"]
    scene_class = lesson["scene_class"]
    if action == "render":
        return [
            "manim-slides",
            "render",
            "--quality",
            quality,
            scene_file,
            scene_class,
        ]
    if action == "present":
        return ["manim-slides", "present", scene_class]
    if action == "export":
        destination = output_path(lesson["id"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        return [
            "manim-slides",
            "convert",
            "--to",
            "html",
            "--one-file",
            "--offline",
            scene_class,
            str(destination),
        ]
    raise ValueError(f"unsupported action: {action}")


def run_lesson(
    action: str,
    lesson: dict[str, Any],
    quality: str,
    dry_run: bool,
) -> dict[str, Any]:
    command = action_command(action, lesson, quality)
    result = {
        "id": lesson["id"],
        "action": action,
        "command": command,
        "status": "dry_run" if dry_run else "pending",
        "returncode": None,
        "log": None,
    }
    if dry_run:
        return result

    log_dir = ROOT / "build" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    safe_id = lesson["id"].replace(".", "_")
    log_path = log_dir / f"{safe_id}-{action}.log"
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log_path.write_text(completed.stdout, encoding="utf-8")
    result["returncode"] = completed.returncode
    result["status"] = "ok" if completed.returncode == 0 else "failed"
    result["log"] = str(log_path.relative_to(ROOT))
    return result


def validate_action_inputs(action: str, lessons: list[dict[str, Any]]) -> None:
    errors: list[str] = []
    for lesson in lessons:
        scene_path = ROOT / lesson["scene_file"]
        if not scene_path.is_file():
            errors.append(
                f"{lesson['id']}: no scene file; current state is "
                f"{lesson['production_state']}"
            )
            continue
        if action in {"present", "export"}:
            manifest_path = ROOT / "slides" / f"{lesson['scene_class']}.json"
            if not manifest_path.is_file():
                errors.append(
                    f"{lesson['id']}: no Slides manifest; render the lesson first"
                )
        if action in {"present", "export"} and lesson["production_state"] not in RENDERED_STATES:
            errors.append(
                f"{lesson['id']}: state {lesson['production_state']} is not rendered"
            )
    if errors:
        raise ValueError("\n".join(errors))


def write_report(action: str, results: list[dict[str, Any]]) -> Path:
    report_dir = ROOT / "build" / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / f"{action}.json"
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "action": action,
        "summary": {
            "total": len(results),
            "ok": sum(item["status"] == "ok" for item in results),
            "failed": sum(item["status"] == "failed" for item in results),
            "dry_run": sum(item["status"] == "dry_run" for item in results),
        },
        "results": sorted(results, key=lambda item: item["id"]),
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report_path


def list_lessons(lessons: dict[str, dict[str, Any]]) -> int:
    for lesson in lessons.values():
        print(
            f"{lesson['id']}\t{lesson['production_state']}\t"
            f"{lesson['scene_class']}\t{lesson['title']}"
        )
    return 0


def execute(args: argparse.Namespace) -> int:
    lessons = load_lessons()
    if args.action == "list":
        return list_lessons(lessons)
    selected = select_lessons(lessons, args.ids, args.status)
    if not selected:
        print("No lessons matched the selection.", file=sys.stderr)
        return 1
    if args.action == "present" and len(selected) != 1:
        print("Present requires exactly one lesson ID.", file=sys.stderr)
        return 1
    validate_action_inputs(args.action, selected)

    results: list[dict[str, Any]] = []
    if args.action == "present" or args.jobs == 1:
        for lesson in selected:
            results.append(
                run_lesson(args.action, lesson, args.quality, args.dry_run),
            )
    else:
        with ThreadPoolExecutor(max_workers=args.jobs) as executor:
            futures = {
                executor.submit(
                    run_lesson,
                    args.action,
                    lesson,
                    args.quality,
                    args.dry_run,
                ): lesson["id"]
                for lesson in selected
            }
            for future in as_completed(futures):
                results.append(future.result())

    report_path = write_report(args.action, results)
    for result in sorted(results, key=lambda item: item["id"]):
        command = " ".join(result["command"])
        print(f"{result['status']}: {result['id']}: {command}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    return 1 if any(item["status"] == "failed" for item in results) else 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["list", "render", "present", "export"])
    parser.add_argument("ids", nargs="*")
    parser.add_argument("--status")
    parser.add_argument("--quality", choices=["l", "m", "h", "p", "k"], default="l")
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.jobs < 1:
        parser.error("--jobs must be positive")
    return args


def main() -> int:
    try:
        return execute(parse_args())
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
