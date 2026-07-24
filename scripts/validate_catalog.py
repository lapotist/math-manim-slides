#!/usr/bin/env python3
"""Validate collection metadata, lesson beats, scripts, and slide manifests."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_PATTERN = "lessons/*/collection.toml"
LESSON_PATTERN = "lessons/*/*/lesson.toml"
SCRIPT_BEAT_RE = re.compile(
    r"^##\s+\d{2}\s+([a-z0-9_]+)(?:\||\N{FULLWIDTH VERTICAL LINE})",
    re.MULTILINE,
)
SOURCE_BEAT_RE = re.compile(r"# Beat \d{2} ([a-z0-9_]+):")
NEXT_SLIDE_RE = re.compile(r"\bself\.next_slide\(")
NEXT_CUE_RE = re.compile(r"\[NEXT\]")
LOOP_CUE_RE = re.compile(r"\[LOOP[^\]]*\]")
VALID_PRODUCTION_STATES = {
    "discovered",
    "blocked",
    "planned",
    "storyboarded",
    "math_verified",
    "draft_rendered",
    "visual_verified",
    "published",
}
RENDERED_STATES = {"draft_rendered", "visual_verified", "published"}


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def validate_collections(
    errors: list[str],
) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    collections: dict[str, Any] = {}
    problems_by_id: dict[str, dict[str, Any]] = {}
    for path in sorted(ROOT.glob(COLLECTION_PATTERN)):
        data = load_toml(path)
        collection_id = data.get("id")
        check(bool(collection_id), f"{path}: missing id", errors)
        if not collection_id:
            continue
        check(
            collection_id not in collections,
            f"duplicate collection id: {collection_id}",
            errors,
        )
        collections[collection_id] = data
        problems = data.get("problems", [])
        check(
            len(problems) == data.get("expected_problem_count"),
            f"{path}: expected_problem_count does not match problems",
            errors,
        )
        for problem in problems:
            problem_id = problem.get("id")
            check(bool(problem_id), f"{path}: problem missing id", errors)
            check(
                problem_id not in problems_by_id,
                f"duplicate problem id: {problem_id}",
                errors,
            )
            if problem_id:
                problems_by_id[problem_id] = problem
            check(
                problem.get("production_state") in VALID_PRODUCTION_STATES,
                f"{problem_id}: invalid production_state",
                errors,
            )
            check(bool(problem.get("answer")), f"{problem_id}: missing answer", errors)
    check(bool(collections), "no collection metadata found", errors)
    return collections, problems_by_id


def validate_manifest(
    metadata: dict[str, Any],
    beats: list[dict[str, Any]],
    errors: list[str],
) -> None:
    scene_class = metadata["scene_class"]
    manifest_path = ROOT / "slides" / f"{scene_class}.json"
    if not manifest_path.exists():
        check(
            metadata["production_state"] not in {"visual_verified", "published"},
            f"{metadata['id']}: verified lesson has no Slides manifest",
            errors,
        )
        return
    manifest = load_json(manifest_path)
    slides = manifest.get("slides", [])
    check(
        len(slides) == len(beats),
        f"{metadata['id']}: manifest/metadata beat count differs",
        errors,
    )
    if len(slides) == len(beats):
        manifest_loops = [bool(slide.get("loop")) for slide in slides]
        metadata_loops = [bool(beat.get("loop")) for beat in beats]
        check(
            manifest_loops == metadata_loops,
            f"{metadata['id']}: manifest/metadata loop flags differ",
            errors,
        )
    check(
        manifest.get("resolution") == [1920, 1080],
        f"{metadata['id']}: manifest is not 1920x1080",
        errors,
    )


def validate_lessons(
    problems_by_id: dict[str, dict[str, Any]], errors: list[str]
) -> int:
    lesson_ids: set[str] = set()
    scene_classes: set[str] = set()
    count = 0
    for path in sorted(ROOT.glob(LESSON_PATTERN)):
        count += 1
        data = load_toml(path)
        lesson_id = data.get("id")
        check(
            lesson_id in problems_by_id,
            f"{path}: unknown problem id {lesson_id}",
            errors,
        )
        check(lesson_id not in lesson_ids, f"duplicate lesson id: {lesson_id}", errors)
        if lesson_id:
            lesson_ids.add(lesson_id)

        scene_class = data.get("scene_class")
        check(bool(scene_class), f"{lesson_id}: missing scene_class", errors)
        check(
            scene_class not in scene_classes,
            f"duplicate scene class: {scene_class}",
            errors,
        )
        if scene_class:
            scene_classes.add(scene_class)

        production_state = data.get("production_state")
        check(
            production_state in VALID_PRODUCTION_STATES,
            f"{lesson_id}: invalid production_state",
            errors,
        )
        if lesson_id in problems_by_id:
            check(
                production_state
                == problems_by_id[lesson_id].get("production_state"),
                f"{lesson_id}: collection/lesson production states differ",
                errors,
            )
        check(bool(data.get("expected_answer")), f"{lesson_id}: missing answer", errors)
        check(
            bool(data.get("independent_check")),
            f"{lesson_id}: missing independent_check",
            errors,
        )
        check(bool(data.get("source_url")), f"{lesson_id}: missing source URL", errors)
        check(
            bool(data.get("source_credit")),
            f"{lesson_id}: missing source credit",
            errors,
        )
        check(
            bool(data.get("rights_review")),
            f"{lesson_id}: missing rights review",
            errors,
        )

        scene_path = ROOT / data.get("scene_file", "")
        script_path = ROOT / data.get("presenter_script", "")
        storyboard_path = ROOT / data.get("storyboard", "")
        if production_state in RENDERED_STATES:
            check(scene_path.is_file(), f"{lesson_id}: missing scene file", errors)
        check(script_path.is_file(), f"{lesson_id}: missing presenter script", errors)
        check(storyboard_path.is_file(), f"{lesson_id}: missing storyboard", errors)
        beats = data.get("beats", [])
        metadata_ids = [beat.get("id") for beat in beats]
        check(
            len(metadata_ids) == len(set(metadata_ids)),
            f"{lesson_id}: duplicate beat IDs",
            errors,
        )

        if scene_path.is_file():
            source = scene_path.read_text(encoding="utf-8")
            source_ids = SOURCE_BEAT_RE.findall(source)
            check(
                source_ids == metadata_ids,
                f"{lesson_id}: source/metadata beat IDs differ",
                errors,
            )
            check(
                len(NEXT_SLIDE_RE.findall(source)) + 1 == len(metadata_ids),
                f"{lesson_id}: next_slide count does not match beats",
                errors,
            )

        if script_path.is_file():
            script = script_path.read_text(encoding="utf-8")
            script_ids = SCRIPT_BEAT_RE.findall(script)
            check(
                script_ids == metadata_ids,
                f"{lesson_id}: presenter/metadata beat IDs differ",
                errors,
            )
            check(
                data["source_credit"] in script,
                f"{lesson_id}: presenter script lacks source credit",
                errors,
            )
            check(
                len(NEXT_CUE_RE.findall(script)) == max(len(beats) - 1, 0),
                f"{lesson_id}: presenter NEXT cue count does not match beats",
                errors,
            )
            check(
                len(LOOP_CUE_RE.findall(script))
                == sum(bool(beat.get("loop")) for beat in beats),
                f"{lesson_id}: presenter LOOP cues do not match beat flags",
                errors,
            )

        validate_manifest(data, beats, errors)
    check(count > 0, "no lesson metadata found", errors)
    return count


def validate_source_registry(errors: list[str]) -> None:
    site_path = ROOT / "catalog" / "site_pages.json"
    asset_path = ROOT / "catalog" / "source_assets.json"
    audit_path = ROOT / "catalog" / "audit_summary.json"
    access_path = ROOT / "catalog" / "source_access_audit.json"
    taxonomy_path = ROOT / "catalog" / "site_taxonomy.json"
    check(site_path.is_file(), "missing site_pages.json", errors)
    check(asset_path.is_file(), "missing source_assets.json", errors)
    check(audit_path.is_file(), "missing audit_summary.json", errors)
    check(access_path.is_file(), "missing source_access_audit.json", errors)
    check(taxonomy_path.is_file(), "missing site_taxonomy.json", errors)
    if (
        not site_path.is_file()
        or not asset_path.is_file()
        or not audit_path.is_file()
        or not access_path.is_file()
        or not taxonomy_path.is_file()
    ):
        return
    site = load_json(site_path)
    assets = load_json(asset_path)
    audit = load_json(audit_path)
    access = load_json(access_path)
    taxonomy = load_json(taxonomy_path)
    check(site["summary"]["failed_pages"] == 0, "site inventory has failures", errors)
    check(
        site["summary"]["unique_drive_files"] == assets["summary"]["drive_assets"],
        "site/asset Drive counts differ",
        errors,
    )
    check(
        audit["scope"]["pages"] == site["summary"]["discovered_pages"],
        "audit/site page counts differ",
        errors,
    )
    check(
        audit["unique_assets"]["total"] == assets["summary"]["total_assets"],
        "audit/source total asset counts differ",
        errors,
    )
    check(
        sum(audit["page_taxonomy"].values()) == audit["scope"]["pages"],
        "audit page taxonomy does not partition all pages",
        errors,
    )
    check(
        audit["access"]["confirmed_public"]
        + audit["access"]["confirmed_restricted"]
        + audit["access"]["unresolved_bot_challenge"]
        == audit["unique_assets"]["total"],
        "audit access statuses do not partition all assets",
        errors,
    )
    registry_entries = assets["drive_assets"] + assets["youtube_assets"]
    registry_ids = {entry["id"] for entry in registry_entries}
    access_ids = set(access["assets"])
    check(
        registry_ids == access_ids,
        "source registry/access-audit provider IDs differ",
        errors,
    )
    registry_access_counts = Counter(
        entry.get("access_status") for entry in registry_entries
    )
    check(
        dict(sorted(registry_access_counts.items()))
        == access["summary"]["access_statuses"],
        "source registry/access-audit status counts differ",
        errors,
    )
    check(
        access["summary"]["total_assets"]
        == audit["unique_assets"]["total"],
        "access-audit/aggregate-audit total counts differ",
        errors,
    )
    site_urls = {page["url"].rstrip("/") for page in site["pages"]}
    taxonomy_urls = {page["url"].rstrip("/") for page in taxonomy["pages"]}
    check(
        site_urls == taxonomy_urls,
        "site inventory/taxonomy page URLs differ",
        errors,
    )
    check(
        taxonomy["summary"]["content_statuses"]
        == {
            "artifacts": audit["page_status"]["with_embedded_assets"],
            "empty_or_shell": audit["page_status"]["empty_or_shell"],
            "text_or_links": audit["page_status"]["text_or_links_only"],
        },
        "taxonomy/aggregate-audit page statuses differ",
        errors,
    )
    check(
        site["summary"]["unique_youtube_videos"]
        == assets["summary"]["youtube_assets"],
        "site/asset YouTube counts differ",
        errors,
    )


def main() -> int:
    errors: list[str] = []
    _, problems_by_id = validate_collections(errors)
    lesson_count = validate_lessons(problems_by_id, errors)
    validate_source_registry(errors)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Catalog validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1
    print(
        f"Catalog valid: {len(problems_by_id)} problems, {lesson_count} lesson, "
        "site and source registries consistent."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
