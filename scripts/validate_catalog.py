#!/usr/bin/env python3
"""Validate collection metadata, lesson beats, scripts, and slide manifests."""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any

from update_sources import render_lesson_index, update_document


ROOT = Path(__file__).resolve().parents[1]
COLLECTION_PATTERN = "lessons/*/collection.toml"
LESSON_PATTERN = "lessons/*/*/lesson.toml"
SCRIPT_BEAT_RE = re.compile(
    r"^##\s+\d{2}\s+([a-z0-9_]+)(?:\||\N{FULLWIDTH VERTICAL LINE})",
    re.MULTILINE,
)
SOURCE_BEAT_RE = re.compile(r"# Beat \d{2} ([a-z0-9_]+):")
BEAT_CALL_RE = re.compile(
    r"\bself\.(?:begin_beat|next_beat)\(\s*['\"]([a-z0-9_]+)['\"]"
)
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
VERIFIED_STATES = {"visual_verified", "published"}
ANSWER_REQUIRED_STATES = {
    "storyboarded",
    "math_verified",
    "draft_rendered",
    "visual_verified",
    "published",
}
VALID_CONTENT_TYPES = {"problem_solution"}
VALID_RIGHTS_REVIEW_STATES = {"pending_cc0_scope"}
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def expected_math_review_state(production_state: str | None) -> str | None:
    if production_state in VERIFIED_STATES:
        return "independently_verified"
    if production_state in {"discovered", "blocked"}:
        return "not_reviewed"
    if production_state in VALID_PRODUCTION_STATES:
        return "pending"
    return None


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def check(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def non_ascii_mathtex_lines(source: str) -> list[int]:
    """Return calls where a literal MathTex argument contains CJK or Unicode."""
    tree = ast.parse(source)
    lines: list[int] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        function_name = None
        if isinstance(node.func, ast.Name):
            function_name = node.func.id
        elif isinstance(node.func, ast.Attribute):
            function_name = node.func.attr
        if function_name != "MathTex":
            continue
        if any(
            isinstance(argument, ast.Constant)
            and isinstance(argument.value, str)
            and not argument.value.isascii()
            for argument in node.args
        ):
            lines.append(node.lineno)
    return lines


def load_source_asset_index() -> dict[str, dict[str, Any]]:
    path = ROOT / "catalog" / "source_assets.json"
    if not path.is_file():
        return {}
    registry = load_json(path)
    entries = registry.get("drive_assets", []) + registry.get("youtube_assets", [])
    return {entry["id"]: entry for entry in entries}


def load_site_page_index() -> dict[str, dict[str, Any]]:
    path = ROOT / "catalog" / "site_pages.json"
    if not path.is_file():
        return {}
    inventory = load_json(path)
    return {page["url"]: page for page in inventory.get("pages", [])}


def validate_collections(
    source_assets: dict[str, dict[str, Any]],
    site_pages: dict[str, dict[str, Any]],
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
        source_page_url = data.get("source_page_url")
        collection_checksum = data.get("source_asset_sha256")
        check(
            isinstance(collection_checksum, str)
            and SHA256_RE.fullmatch(collection_checksum) is not None,
            f"{collection_id}: missing or invalid source asset checksum",
            errors,
        )
        if data.get("source_origin") == "frozen_site_inventory":
            page_record = site_pages.get(source_page_url)
            check(
                page_record is not None,
                f"{collection_id}: source page is absent from site inventory",
                errors,
            )
            check(
                bool(data.get("source_page_sha256")),
                f"{collection_id}: missing frozen source page checksum",
                errors,
            )
            if page_record and data.get("source_page_sha256"):
                check(
                    data["source_page_sha256"] == page_record.get("page_sha256"),
                    f"{collection_id}: source page checksum differs from inventory",
                    errors,
                )
            source_asset_id = data.get("source_asset_id")
            source_record = source_assets.get(source_asset_id)
            check(
                source_record is not None,
                f"{collection_id}: source asset is absent from source registry",
                errors,
            )
            if source_record:
                check(
                    data.get("source_asset_sha256") == source_record.get("sha256"),
                    f"{collection_id}: source checksum differs from source registry",
                    errors,
                )
                check(
                    source_page_url in source_record.get("source_pages", []),
                    f"{collection_id}: source asset is not linked from source page",
                    errors,
                )
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
            production_state = problem.get("production_state")
            check(
                problem.get("content_type") in VALID_CONTENT_TYPES,
                f"{problem_id}: missing or invalid content_type",
                errors,
            )
            duplicate_of = problem.get("duplicate_of")
            check(
                isinstance(duplicate_of, str),
                f"{problem_id}: duplicate_of must be a string",
                errors,
            )
            check(
                problem.get("rights_review") in VALID_RIGHTS_REVIEW_STATES,
                f"{problem_id}: missing or invalid rights_review",
                errors,
            )
            expected_review = expected_math_review_state(production_state)
            check(
                problem.get("math_review_state") == expected_review,
                f"{problem_id}: math_review_state does not match production state",
                errors,
            )
            if problem.get("eligible") is False and production_state != "blocked":
                check(
                    bool(problem.get("eligibility_reason")),
                    f"{problem_id}: ineligible review item lacks eligibility_reason",
                    errors,
                )
            if production_state in ANSWER_REQUIRED_STATES:
                check(
                    bool(problem.get("answer")),
                    f"{problem_id}: missing answer",
                    errors,
                )
            if production_state == "blocked":
                check(
                    bool(problem.get("blocker_reason")),
                    f"{problem_id}: blocked without blocker_reason",
                    errors,
                )
            solution_asset_id = problem.get("solution_asset")
            if (
                data.get("source_origin") == "frozen_site_inventory"
                and solution_asset_id
            ):
                solution_record = source_assets.get(solution_asset_id)
                check(
                    solution_record is not None,
                    f"{problem_id}: solution asset is absent from source registry",
                    errors,
                )
                if solution_record:
                    check(
                        solution_record.get("watch_url")
                        == problem.get("solution_url"),
                        f"{problem_id}: solution URL differs from source registry",
                        errors,
                    )
                    check(
                        solution_record.get("access_status") == "public_stream",
                        f"{problem_id}: mapped solution is not confirmed public",
                        errors,
                    )
                    check(
                        source_page_url in solution_record.get("source_pages", []),
                        f"{problem_id}: solution is not linked from source page",
                        errors,
                    )
    for problem_id, problem in problems_by_id.items():
        duplicate_of = problem.get("duplicate_of")
        if duplicate_of:
            check(
                duplicate_of != problem_id,
                f"{problem_id}: duplicate_of points to itself",
                errors,
            )
            check(
                duplicate_of in problems_by_id,
                f"{problem_id}: duplicate_of target is unknown",
                errors,
            )
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


def validate_qa_evidence(
    metadata: dict[str, Any],
    beats: list[dict[str, Any]],
    errors: list[str],
) -> None:
    if metadata["production_state"] not in VERIFIED_STATES:
        return
    lesson_id = metadata["id"]
    evidence_path = ROOT / "qa" / f"{lesson_id.replace('.', '_')}.json"
    if not evidence_path.is_file():
        errors.append(f"{lesson_id}: verified lesson has no committed QA evidence")
        return
    evidence = load_json(evidence_path)
    check(evidence.get("schema_version") == 1, f"{lesson_id}: bad QA schema", errors)
    check(evidence.get("lesson_id") == lesson_id, f"{lesson_id}: QA ID differs", errors)
    check(
        evidence.get("scene_class") == metadata["scene_class"],
        f"{lesson_id}: QA scene class differs",
        errors,
    )
    check(evidence.get("status") == "ok", f"{lesson_id}: QA status is not ok", errors)
    review = evidence.get("review", {})
    check(
        review.get("mechanical") == "passed",
        f"{lesson_id}: mechanical QA is not attested",
        errors,
    )
    check(
        review.get("visual") == "human_reviewed",
        f"{lesson_id}: human visual QA is not attested",
        errors,
    )
    render = evidence.get("render", {})
    expected_beats = [
        {"id": beat["id"], "loop": bool(beat.get("loop"))}
        for beat in beats
    ]
    check(
        render.get("segment_count") == len(beats),
        f"{lesson_id}: QA segment count differs",
        errors,
    )
    check(
        render.get("resolution") == [1920, 1080],
        f"{lesson_id}: QA resolution differs",
        errors,
    )
    check(
        render.get("beats") == expected_beats,
        f"{lesson_id}: QA beat contract differs",
        errors,
    )
    source_hashes = evidence.get("source_hashes", {})
    for field in ("scene_file", "presenter_script", "storyboard"):
        record = source_hashes.get(field, {})
        relative_path = metadata[field]
        path = ROOT / relative_path
        check(
            record.get("path") == relative_path,
            f"{lesson_id}: QA {field} path differs",
            errors,
        )
        if path.is_file():
            check(
                record.get("sha256") == sha256(path),
                f"{lesson_id}: QA evidence is stale for {field}",
                errors,
            )


def validate_lessons(
    collections: dict[str, Any],
    problems_by_id: dict[str, dict[str, Any]],
    source_assets: dict[str, dict[str, Any]],
    errors: list[str],
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
            bool(data.get("source_locator")),
            f"{lesson_id}: missing exact source locator",
            errors,
        )
        lesson_checksum = data.get("source_asset_sha256")
        check(
            isinstance(lesson_checksum, str)
            and SHA256_RE.fullmatch(lesson_checksum) is not None,
            f"{lesson_id}: missing or invalid source asset checksum",
            errors,
        )
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

        problem = problems_by_id.get(lesson_id, {})
        collection = collections.get(data.get("collection_id"), {})
        check(
            bool(collection),
            f"{lesson_id}: lesson collection is unknown",
            errors,
        )
        if collection:
            check(
                lesson_checksum == collection.get("source_asset_sha256"),
                f"{lesson_id}: lesson/collection source checksums differ",
                errors,
            )
        if problem:
            check(
                data.get("rights_review") == problem.get("rights_review"),
                f"{lesson_id}: lesson/problem rights reviews differ",
                errors,
            )
        expected_solution_id = problem.get("solution_asset")
        if expected_solution_id:
            solution_id = data.get("solution_asset_id")
            check(
                solution_id == expected_solution_id,
                f"{lesson_id}: lesson/collection solution asset IDs differ",
                errors,
            )
            check(
                data.get("solution_url") == problem.get("solution_url"),
                f"{lesson_id}: lesson/collection solution URLs differ",
                errors,
            )
            solution_record = source_assets.get(expected_solution_id)
            check(
                solution_record is not None,
                f"{lesson_id}: solution asset is absent from source registry",
                errors,
            )
            if solution_record:
                check(
                    solution_record.get("watch_url") == data.get("solution_url"),
                    f"{lesson_id}: solution URL differs from source registry",
                    errors,
                )
                check(
                    solution_record.get("access_status") == "public_stream",
                    f"{lesson_id}: solution asset is not confirmed public",
                    errors,
                )
                check(
                    data.get("source_url") in solution_record.get("source_pages", []),
                    f"{lesson_id}: solution asset is not linked from source page",
                    errors,
                )

            source_asset_id = data.get("source_asset_id")
            source_record = source_assets.get(source_asset_id)
            check(
                source_record is not None,
                f"{lesson_id}: source asset is absent from source registry",
                errors,
            )
            if source_record:
                check(
                    data.get("source_asset_sha256") == source_record.get("sha256"),
                    f"{lesson_id}: source checksum differs from source registry",
                    errors,
                )
                check(
                    data.get("source_url") in source_record.get("source_pages", []),
                    f"{lesson_id}: source PDF is not linked from source page",
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
            try:
                compile(source, str(scene_path), "exec")
            except SyntaxError as error:
                errors.append(f"{lesson_id}: scene syntax error: {error}")
            else:
                for line_number in non_ascii_mathtex_lines(source):
                    errors.append(
                        f"{lesson_id}: MathTex contains non-ASCII text at "
                        f"{scene_path}:{line_number}; use label/Text for CJK"
                    )
            beat_call_ids = BEAT_CALL_RE.findall(source)
            source_ids = beat_call_ids or SOURCE_BEAT_RE.findall(source)
            check(
                source_ids == metadata_ids,
                f"{lesson_id}: source/metadata beat IDs differ",
                errors,
            )
            if beat_call_ids:
                check(
                    len(beat_call_ids) == len(metadata_ids),
                    f"{lesson_id}: beat API count does not match metadata",
                    errors,
                )
            else:
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

        validate_qa_evidence(data, beats, errors)
        validate_manifest(data, beats, errors)
    check(count > 0, "no lesson metadata found", errors)
    return count


def validate_generated_source_index(errors: list[str]) -> None:
    sources_path = ROOT / "SOURCES.md"
    check(sources_path.is_file(), "missing SOURCES.md", errors)
    if not sources_path.is_file():
        return
    current = sources_path.read_text(encoding="utf-8")
    try:
        generated, _ = render_lesson_index(ROOT)
        expected = update_document(current, generated)
    except ValueError as error:
        errors.append(f"source index cannot be generated: {error}")
        return
    check(
        current == expected,
        "SOURCES.md lesson index is stale; run pixi run update-sources",
        errors,
    )


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
    registry_eligibility_counts = Counter(
        entry.get("asset_eligibility") for entry in registry_entries
    )
    check(
        dict(sorted(registry_eligibility_counts.items()))
        == assets["summary"].get("asset_eligibility"),
        "source registry eligibility summary differs from asset records",
        errors,
    )
    check(
        registry_eligibility_counts
        == Counter(
            {
                "review_pending": audit["access"]["confirmed_public"],
                "blocked_access": audit["access"]["confirmed_restricted"],
                "blocked_access_verification": audit["access"][
                    "unresolved_bot_challenge"
                ],
            }
        ),
        "source eligibility counts do not match audited access groups",
        errors,
    )
    check(
        all(entry.get("blocker_reasons") for entry in registry_entries),
        "source registry contains an asset without blocker/review reasons",
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
    source_assets = load_source_asset_index()
    site_pages = load_site_page_index()
    collections, problems_by_id = validate_collections(
        source_assets, site_pages, errors
    )
    lesson_count = validate_lessons(
        collections, problems_by_id, source_assets, errors
    )
    validate_generated_source_index(errors)
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
