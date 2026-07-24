#!/usr/bin/env python3
"""Convert the reviewed source-access TSV into a compact catalog snapshot."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path
from typing import Any


PROVIDER_PREFIX = {
    "google_drive": "drive",
    "youtube": "youtube",
}


def optional_int(value: str) -> int | None:
    return int(value) if value else None


def import_audit(path: Path, snapshot_date: str) -> dict[str, Any]:
    assets: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            provider = row["provider"]
            prefix = PROVIDER_PREFIX[provider]
            key = f"{prefix}:{row['identifier']}"
            if key in assets:
                raise ValueError(f"duplicate audit key: {key}")
            record: dict[str, Any] = {
                "access_status": row["access_status"],
                "content_type": row["type"],
            }
            for field in ("verified_title", "author", "sha256"):
                if row[field]:
                    record[field] = row[field]
            content_bytes = optional_int(row["content_bytes"])
            if content_bytes is not None:
                record["content_bytes"] = content_bytes
            assets[key] = record

    access_counts = Counter(
        record["access_status"] for record in assets.values()
    )
    provider_counts = Counter(key.split(":", 1)[0] for key in assets)
    return {
        "schema_version": 1,
        "snapshot_date": snapshot_date,
        "method": (
            "Anonymous Drive download and YouTube playback checks; an anti-bot "
            "challenge is recorded as unresolved, never inferred as public."
        ),
        "summary": {
            "total_assets": len(assets),
            "drive_assets": provider_counts["drive"],
            "youtube_assets": provider_counts["youtube"],
            "access_statuses": dict(sorted(access_counts.items())),
        },
        "assets": dict(sorted(assets.items())),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("catalog/source_access_audit.json"),
    )
    parser.add_argument("--snapshot-date", default="2026-07-24")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit = import_audit(args.input, args.snapshot_date)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
