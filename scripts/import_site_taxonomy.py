#!/usr/bin/env python3
"""Convert the reviewed page-taxonomy TSV into a stable catalog snapshot."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


INTEGER_FIELDS = {
    "artifact_count",
    "drive_count",
    "youtube_count",
    "direct_file_count",
    "external_embed_count",
    "content_chars",
    "public_artifact_count",
    "private_artifact_count",
}
KEPT_FIELDS = (
    "page_id",
    "url",
    "title",
    "section",
    "subsection",
    "leaf",
    "year_roc",
    "audience",
    "exam",
    "topic",
    "content_status",
    *sorted(INTEGER_FIELDS),
)


def import_taxonomy(path: Path, snapshot_date: str) -> dict[str, Any]:
    raw = path.read_bytes()
    pages: list[dict[str, Any]] = []
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            page: dict[str, Any] = {}
            for field in KEPT_FIELDS:
                value: Any = row[field]
                if field in INTEGER_FIELDS:
                    value = int(value)
                elif value == "":
                    value = None
                page[field] = value
            pages.append(page)

    urls = [page["url"] for page in pages]
    if len(urls) != len(set(urls)):
        raise ValueError("page taxonomy contains duplicate URLs")
    content_statuses = Counter(page["content_status"] for page in pages)
    sections = Counter(page["section"] for page in pages)
    return {
        "schema_version": 1,
        "snapshot_date": snapshot_date,
        "input_sha256": hashlib.sha256(raw).hexdigest(),
        "summary": {
            "pages": len(pages),
            "content_statuses": dict(sorted(content_statuses.items())),
            "sections": dict(sorted(sections.items())),
        },
        "pages": pages,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("catalog/site_taxonomy.json"),
    )
    parser.add_argument("--snapshot-date", default="2026-07-24")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    taxonomy = import_taxonomy(args.input, args.snapshot_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(taxonomy, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(taxonomy["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
