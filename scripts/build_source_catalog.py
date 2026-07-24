#!/usr/bin/env python3
"""Flatten the site-page inventory into a source-asset registry."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any


PUBLIC_ACCESS = {"public", "public_stream"}
UNRESOLVED_ACCESS = {"verification_inconclusive_bot_challenge"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def asset_kind(title: str | None) -> str:
    normalized = (title or "").lower().removesuffix(" 的副本")
    if normalized.endswith(".pdf"):
        return "pdf"
    if normalized.endswith(".pptx"):
        return "pptx"
    return "unknown"


def build_registry(
    site_inventory: dict[str, Any],
    access_audit: dict[str, Any] | None = None,
) -> dict[str, Any]:
    drive: dict[str, dict[str, Any]] = {}
    video_pages: defaultdict[str, set[str]] = defaultdict(set)

    for page in site_inventory["pages"]:
        page_url = page["url"]
        for source in page["drive_files"]:
            file_id = source["id"]
            entry = drive.setdefault(
                file_id,
                {
                    "id": f"drive:{file_id}",
                    "provider_id": file_id,
                    "kind": asset_kind(source.get("title")),
                    "titles": set(),
                    "source_pages": set(),
                    "preview_url": source["preview_url"],
                    "download_url": source["download_url"],
                    "content_review": "pending",
                    "rights_review": "pending_cc0_scope",
                    "production_state": "discovered",
                },
            )
            if source.get("title"):
                entry["titles"].add(source["title"])
            entry["source_pages"].add(page_url)

        for video_id in page["youtube_ids"]:
            video_pages[video_id].add(page_url)

    drive_entries = []
    for entry in drive.values():
        entry["titles"] = sorted(entry["titles"])
        entry["source_pages"] = sorted(entry["source_pages"])
        drive_entries.append(entry)
    drive_entries.sort(key=lambda entry: entry["id"])

    video_entries = [
        {
            "id": f"youtube:{video_id}",
            "provider_id": video_id,
            "kind": "youtube_video",
            "source_pages": sorted(pages),
            "watch_url": f"https://www.youtube.com/watch?v={video_id}",
            "content_review": "pending",
            "rights_review": "pending_cc0_scope",
            "production_state": "discovered",
        }
        for video_id, pages in sorted(video_pages.items())
    ]

    registry = {
        "schema_version": 1,
        "generated_from": "catalog/site_pages.json",
        "site_inventory_sha256": site_inventory["root_sha256"],
        "summary": {
            "drive_assets": len(drive_entries),
            "pdf_assets": sum(entry["kind"] == "pdf" for entry in drive_entries),
            "pptx_assets": sum(entry["kind"] == "pptx" for entry in drive_entries),
            "unknown_drive_assets": sum(
                entry["kind"] == "unknown" for entry in drive_entries
            ),
            "youtube_assets": len(video_entries),
            "total_assets": len(drive_entries) + len(video_entries),
            "content_review_pending": len(drive_entries) + len(video_entries),
            "rights_review_pending": len(drive_entries) + len(video_entries),
        },
        "drive_assets": drive_entries,
        "youtube_assets": video_entries,
    }
    if access_audit is not None:
        audit_assets = access_audit["assets"]
        registry_assets = {
            entry["id"]: entry for entry in drive_entries + video_entries
        }
        missing = sorted(registry_assets.keys() - audit_assets.keys())
        extra = sorted(audit_assets.keys() - registry_assets.keys())
        if missing or extra:
            raise ValueError(
                "access audit does not match source registry: "
                f"{len(missing)} missing and {len(extra)} extra keys"
            )
        for key, entry in registry_assets.items():
            entry.update(audit_assets[key])
            access_status = entry["access_status"]
            if access_status in PUBLIC_ACCESS:
                entry["asset_eligibility"] = "review_pending"
                entry["blocker_reasons"] = [
                    "problem_solution_decomposition_pending",
                    "rights_scope_pending",
                ]
            elif access_status in UNRESOLVED_ACCESS:
                entry["asset_eligibility"] = "blocked_access_verification"
                entry["blocker_reasons"] = [
                    "anonymous_playback_verification_inconclusive",
                ]
            else:
                entry["asset_eligibility"] = "blocked_access"
                entry["blocker_reasons"] = ["source_not_anonymously_accessible"]
        registry["access_audit"] = {
            "path": "catalog/source_access_audit.json",
            "snapshot_date": access_audit["snapshot_date"],
            "summary": access_audit["summary"],
        }
        registry["summary"]["access_statuses"] = access_audit["summary"][
            "access_statuses"
        ]
        eligibility_counts: dict[str, int] = {}
        for entry in registry_assets.values():
            status = entry["asset_eligibility"]
            eligibility_counts[status] = eligibility_counts.get(status, 0) + 1
        registry["summary"]["asset_eligibility"] = dict(
            sorted(eligibility_counts.items())
        )
    return registry


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="catalog/site_pages.json")
    parser.add_argument("--output", default="catalog/source_assets.json")
    parser.add_argument(
        "--access-audit",
        default="catalog/source_access_audit.json",
        help="Optional per-asset access snapshot; omitted when the file is absent.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    audit_path = Path(args.access_audit)
    access_audit = load_json(audit_path) if audit_path.is_file() else None
    registry = build_registry(load_json(Path(args.input)), access_audit)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(registry, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(registry["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
