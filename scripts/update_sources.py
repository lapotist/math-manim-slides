#!/usr/bin/env python3
"""Regenerate the exact per-lesson provenance index in SOURCES.md."""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- lesson-source-index:start -->"
END = "<!-- lesson-source-index:end -->"
LESSON_PATTERN = "lessons/*/*/lesson.toml"
COLLECTION_PATTERN = "lessons/*/collection.toml"
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def escape_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def linked_reference(label: str, url: str | None) -> str:
    if not url:
        return label
    return f"[{label}]({url})"


def source_references(
    lesson: dict[str, Any],
    collection: dict[str, Any],
) -> str:
    references: list[str] = []
    source_url = lesson.get("source_url")
    if source_url:
        page_label = (
            "creator context"
            if collection.get("source_origin") == "user_supplied"
            else "canonical page"
        )
        references.append(linked_reference(page_label, source_url))

    source_asset_id = lesson.get("source_asset_id")
    source_asset_url = lesson.get("source_asset_url")
    if source_asset_id:
        reference = linked_reference("source asset", source_asset_url)
        references.append(f"{reference} `{source_asset_id}`")
    elif lesson.get("source_asset"):
        references.append(f"source asset `{lesson['source_asset']}`")

    solution_asset_id = lesson.get("solution_asset_id")
    solution_url = lesson.get("solution_url")
    if solution_asset_id:
        reference = linked_reference("solution", solution_url)
        references.append(f"{reference} `{solution_asset_id}`")
    elif solution_url:
        references.append(linked_reference("solution", solution_url))

    if not references:
        raise ValueError(f"{lesson.get('id')}: no source or solution reference")
    return " / ".join(references)


def render_lesson_index(root: Path = ROOT) -> tuple[str, int]:
    collections = {
        collection["id"]: collection
        for path in sorted(root.glob(COLLECTION_PATTERN))
        for collection in (load_toml(path),)
    }
    rows = [
        START,
        "| Lesson | Pages and exact locator | Source references | Source SHA-256 | Credit | Rights |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    count = 0
    for path in sorted(root.glob(LESSON_PATTERN)):
        lesson = load_toml(path)
        lesson_id = lesson.get("id")
        collection_id = lesson.get("collection_id")
        collection = collections.get(collection_id)
        if collection is None:
            raise ValueError(
                f"{lesson_id}: unknown collection for generated source index"
            )

        required = (
            "source_pages",
            "source_locator",
            "source_asset_sha256",
            "source_credit",
            "rights_review",
        )
        missing = [field for field in required if not lesson.get(field)]
        if missing:
            raise ValueError(
                f"{lesson_id}: source index fields missing: {', '.join(missing)}"
            )
        checksum = lesson["source_asset_sha256"]
        if not isinstance(checksum, str) or SHA256_RE.fullmatch(checksum) is None:
            raise ValueError(f"{lesson_id}: invalid source SHA-256")

        pages = ", ".join(str(page) for page in lesson["source_pages"])
        locator = f"pages {pages}; {lesson['source_locator']}"
        references = source_references(lesson, collection)
        rows.append(
            "| "
            f"`{escape_cell(lesson_id)}` | {escape_cell(locator)} | "
            f"{references} | `{checksum}` | "
            f"{escape_cell(lesson['source_credit'])} | "
            f"`{escape_cell(lesson['rights_review'])}` |"
        )
        count += 1
    rows.append(END)
    return "\n".join(rows), count


def update_document(document: str, generated_block: str) -> str:
    pattern = re.compile(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        re.DOTALL,
    )
    if not pattern.search(document):
        raise ValueError("SOURCES.md lesson index markers are missing")
    return pattern.sub(generated_block, document)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if SOURCES.md does not match lesson metadata",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    sources_path = ROOT / "SOURCES.md"
    current = sources_path.read_text(encoding="utf-8")
    try:
        generated, count = render_lesson_index()
        expected = update_document(current, generated)
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    if args.check:
        if current != expected:
            print(
                "ERROR: SOURCES.md lesson index is stale; run "
                "`pixi run update-sources`.",
                file=sys.stderr,
            )
            return 1
        print(f"Source index current: {count} lessons.")
        return 0

    sources_path.write_text(expected, encoding="utf-8")
    print(f"Updated SOURCES.md for {count} lessons.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
