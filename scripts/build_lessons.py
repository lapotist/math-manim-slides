#!/usr/bin/env python3
"""Run Manim Slides actions for cataloged lessons."""

from __future__ import annotations

import argparse
import html
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
PROJECT_TITLE = "Carlo Math Manim Slides"
PROJECT_URL = "https://github.com/lapotist/carlo-math-manim-slides"
CC_BY_URL = "https://creativecommons.org/licenses/by/4.0/"
REVEAL_VERSION = "6.0.1"
ATTRIBUTION_MARKER = 'id="carlo-project-attribution"'
THIRD_PARTY_NOTICE_MARKER = "BEGIN CARLO THIRD-PARTY LICENSE NOTICES"
REVEAL_CLOSING_MARKER = "\n</div>\n</div>\n\n\n"
PLUGIN_MARKER = "<!-- To include plugins"
THIRD_PARTY_LICENSES = (
    ("Manim Slides 5.6.0", ROOT / "LICENSES" / "Manim-Slides-5.6.0.txt"),
    ("Reveal.js 6.0.1", ROOT / "LICENSES" / "Reveal.js-6.0.1.txt"),
)


def load_lessons() -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for path in sorted(ROOT.glob(LESSON_PATTERN)):
        with path.open("rb") as handle:
            lesson = tomllib.load(handle)
        collection_path = path.parents[1] / "collection.toml"
        with collection_path.open("rb") as handle:
            collection = tomllib.load(handle)
        lesson["metadata_path"] = str(path.relative_to(ROOT))
        lesson["collection_source_origin"] = collection["source_origin"]
        lesson["collection_source_context_url_role"] = collection.get(
            "source_context_url_role", "題目與解題資料頁"
        )
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


def media_path(lesson_id: str) -> Path:
    safe_id = lesson_id.replace(".", "_")
    return ROOT / "build" / "media" / safe_id


def add_export_attribution(destination: Path, lesson: dict[str, Any]) -> None:
    document = destination.read_text(encoding="utf-8")
    if ATTRIBUTION_MARKER in document or THIRD_PARTY_NOTICE_MARKER in document:
        raise ValueError(f"{lesson['id']}: export already contains attribution")
    plugin_index = document.rfind(PLUGIN_MARKER)
    closing_index = document.rfind(REVEAL_CLOSING_MARKER, 0, plugin_index)
    if plugin_index < 0 or closing_index < 0:
        raise ValueError(
            f"{lesson['id']}: unsupported Manim Slides HTML structure"
        )

    title = html.escape(str(lesson["title"]), quote=True)
    source_credit = html.escape(str(lesson["source_credit"]), quote=True)
    source_asset = html.escape(str(lesson["source_asset"]), quote=True)
    source_locator = html.escape(str(lesson["source_locator"]), quote=True)
    source_url = html.escape(str(lesson["source_url"]), quote=True)
    source_origin = lesson.get("collection_source_origin", "")
    source_context_role = html.escape(
        str(lesson.get("collection_source_context_url_role", "題目與解題資料頁")),
        quote=True,
    )

    source_asset_url = lesson.get("source_asset_url")
    if source_asset_url:
        escaped_asset_url = html.escape(str(source_asset_url), quote=True)
        asset_markup = (
            f'<a href="{escaped_asset_url}" rel="dcterms:source" '
            f'style="color:#f2c14e;">{source_asset}</a>'
        )
    elif source_origin == "user_supplied":
        asset_markup = f"{source_asset}（使用者提供；未嵌入本檔）"
    else:
        asset_markup = source_asset

    solution_url = lesson.get("solution_url")
    if solution_url:
        escaped_solution_url = html.escape(str(solution_url), quote=True)
        solution_markup = (
            '<br/>解題參考：'
            f'<a href="{escaped_solution_url}" rel="dcterms:source" '
            f'style="color:#f2c14e;">{source_credit}</a>'
        )
    else:
        solution_markup = f"<br/>來源署名紀錄：{source_credit}"

    third_party_parts: list[str] = []
    for component, license_path in THIRD_PARTY_LICENSES:
        license_text = license_path.read_text(encoding="utf-8").rstrip()
        if "--" in license_text:
            raise ValueError(f"unsafe HTML comment text in {license_path}")
        third_party_parts.append(f"{component}\n{license_text}")
    third_party_notices = (
        f"\n<!-- {THIRD_PARTY_NOTICE_MARKER}\n"
        + "\n\n".join(third_party_parts)
        + "\nEND CARLO THIRD-PARTY LICENSE NOTICES -->\n"
    )
    attribution_slide = f"""
<section id="carlo-project-attribution" data-generated-legal-appendix="true" data-background-color="#101214" typeof="CreativeWork">
  <div style="box-sizing:border-box;color:#f4f1e8;font-family:sans-serif;margin:0 auto;max-width:1040px;padding:54px 68px;text-align:left;">
    <h2 style="color:#f4f1e8;font-size:39px;letter-spacing:0;margin:0 0 20px;">授權與來源</h2>
    <p style="font-size:22px;line-height:1.45;margin:0 0 14px;"><strong><a href="{PROJECT_URL}" property="url" style="color:#f4f1e8;">{PROJECT_TITLE}</a></strong><br/><span property="name">{title}</span><br/><span property="creator">Carlo Math Manim Slides contributors</span></p>
    <p style="font-size:19px;line-height:1.45;margin:0 0 14px;">本檔為專案原始匯出；未標記後續修改。專案原創教學內容採 <a href="{CC_BY_URL}" property="license" rel="license" style="color:#59c3c3;">CC BY 4.0</a>。</p>
    <p style="font-size:18px;line-height:1.45;margin:0 0 14px;"><strong>來源紀錄</strong><br/>素材：{asset_markup}<br/>定位：{source_locator}{solution_markup}<br/><a href="{source_url}" style="color:#f2c14e;">資料頁</a>（{source_context_role}；非來源檔授權連結）</p>
    <p style="color:#b9bec4;font-size:15px;line-height:1.4;margin:0;">來源素材與匯出檔內的第三方軟體保留各自的權利與授權；完整的 Reveal.js 與 Manim Slides MIT 通知已內嵌於本 HTML 原始碼。來源署名不代表來源作者是本專案內容的授權人。</p>
  </div>
</section>"""
    document = (
        document[:closing_index]
        + attribution_slide
        + document[closing_index:plugin_index]
        + third_party_notices
        + document[plugin_index:]
    )
    destination.write_text(document, encoding="utf-8")


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
            "--media_dir",
            str(media_path(lesson["id"])),
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
            "-c",
            f"reveal_version={REVEAL_VERSION}",
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
    output = completed.stdout
    returncode = completed.returncode
    if returncode == 0 and action == "export":
        try:
            add_export_attribution(output_path(lesson["id"]), lesson)
        except (OSError, ValueError) as error:
            output += f"\nExport attribution failed: {error}\n"
            returncode = 1
    log_path.write_text(output, encoding="utf-8")
    result["returncode"] = returncode
    result["status"] = "ok" if returncode == 0 else "failed"
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
        if action == "export" and lesson.get("release_rights_state") != "cleared":
            errors.append(
                f"{lesson['id']}: standalone export requires rights clearance"
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
