#!/usr/bin/env python3
"""Build and serve the loopback-only human slide verification workspace."""

from __future__ import annotations

import argparse
import hashlib
import json
import mimetypes
import os
import re
import shutil
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, BinaryIO
from urllib.parse import unquote, urlparse

try:
    from scripts.build_lessons import load_lessons, select_lessons
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from build_lessons import load_lessons, select_lessons  # type: ignore[no-redef]


ROOT = Path(__file__).resolve().parents[1]
STATIC_ROOT = ROOT / "scripts" / "review_site_assets"
SITE_ROOT = ROOT / "build" / "review-site"
REVIEW_ROOT = ROOT / "build" / "reviews"
PUBLIC_STATUS_PATH = ROOT / "qa" / "review-status.json"
BUILT_PUBLIC_STATUS_PATH = ROOT / "build" / "site" / "review-status.json"
LIVE_QA_ROOT = ROOT / "build" / "qa"
QA_FRAME_ROOT = LIVE_QA_ROOT / "frames"
SLIDES_ROOT = ROOT / "slides"
QA_SCHEMA_VERSION = 2
REVIEW_SCHEMA_VERSION = 1
DEFAULT_PORT = 8765
RENDERED_STATES = {"draft_rendered", "visual_verified", "published"}
LESSON_ID_RE = re.compile(
    r"[a-z0-9][a-z0-9_-]*(?:\.[a-z0-9][a-z0-9_-]*)*"
)
SCRIPT_HEADING_RE = re.compile(
    r"^##\s+\d+\s+([a-z0-9_-]+)(?:\s*｜(.*))?$", re.MULTILINE
)
VERDICTS = {"pending", "pass", "issue"}
SEGMENT_CRITERIA = ("legibility", "layout", "motion", "settled")
LOOP_CRITERION = "loop"
LESSON_CRITERIA = (
    "contact_sheet",
    "transition_sweep",
    "narration",
    "mathematics",
    "answer",
)
ISSUE_TAGS = {
    "glyph",
    "overlap",
    "clipping",
    "timing",
    "motion",
    "loop",
    "mathematics",
    "script",
}


class ReviewSiteError(ValueError):
    """Raised when review evidence is absent, stale, or unsafe."""


@dataclass(frozen=True)
class BoundAsset:
    """A live file whose bytes must remain identical to the built catalog."""

    path: Path
    sha256: str
    size: int
    mtime_ns: int

    def is_current(self) -> bool:
        try:
            stat = self.path.stat()
        except OSError:
            return False
        if stat.st_size == self.size and stat.st_mtime_ns == self.mtime_ns:
            return True
        return stat.st_size == self.size and sha256(self.path) == self.sha256


def utc_now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


def safe_id(lesson_id: str) -> str:
    if not isinstance(lesson_id, str) or LESSON_ID_RE.fullmatch(lesson_id) is None:
        raise ReviewSiteError(f"unsafe lesson ID: {lesson_id!r}")
    return lesson_id.replace(".", "_")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def digest_json(value: object) -> str:
    encoded = json.dumps(
        value, ensure_ascii=True, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def checked_record_path(
    record: object,
    *,
    allowed_root: Path,
    label: str,
    repository_root: Path = ROOT,
) -> Path:
    if not isinstance(record, dict):
        raise ReviewSiteError(f"{label}: file record is missing")
    relative_path = record.get("path")
    expected_hash = record.get("sha256")
    if not isinstance(relative_path, str) or not relative_path:
        raise ReviewSiteError(f"{label}: path is missing")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ReviewSiteError(f"{label}: SHA-256 is missing")
    root = repository_root.resolve()
    allowed = allowed_root.resolve()
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_relative_to(allowed):
        raise ReviewSiteError(f"{label}: path is outside its allowed root")
    if not candidate.is_file():
        raise ReviewSiteError(f"{label}: file is unavailable: {relative_path}")
    if sha256(candidate) != expected_hash:
        raise ReviewSiteError(f"{label}: file hash is stale: {relative_path}")
    return candidate


def parse_presenter_sections(path: Path) -> dict[str, dict[str, str]]:
    text = path.read_text(encoding="utf-8")
    matches = list(SCRIPT_HEADING_RE.finditer(text))
    sections: dict[str, dict[str, str]] = {}
    for index, match in enumerate(matches):
        body_start = match.end()
        body_end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = {
            "title": (match.group(2) or match.group(1)).strip(),
            "body": text[body_start:body_end].strip(),
        }
    return sections


def register_asset(
    path: Path,
    asset_map: dict[str, BoundAsset],
    *,
    repository_root: Path = ROOT,
) -> str:
    relative = str(path.resolve().relative_to(repository_root.resolve()))
    content_hash = sha256(path)
    token_base = hashlib.sha256(
        f"{relative}\0{content_hash}".encode("utf-8")
    ).hexdigest()[:24]
    token = token_base + path.suffix.lower()
    existing = asset_map.get(token)
    if existing is not None and existing.path.resolve() != path.resolve():
        raise ReviewSiteError(f"asset token collision for {relative}")
    stat = path.stat()
    asset_map[token] = BoundAsset(
        path=path,
        sha256=content_hash,
        size=stat.st_size,
        mtime_ns=stat.st_mtime_ns,
    )
    return f"/asset/{token}"


def require_report_inputs(
    lesson: dict[str, Any],
    report: dict[str, Any],
    *,
    repository_root: Path,
) -> list[dict[str, str]]:
    raw_inputs = report.get("inputs")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        raise ReviewSiteError(f"{lesson['id']}: QA input binding is missing")
    records: list[dict[str, str]] = []
    paths_by_role: dict[str, set[str]] = {}
    for index, record in enumerate(raw_inputs, start=1):
        path = checked_record_path(
            record,
            allowed_root=repository_root,
            label=f"{lesson['id']}: QA input {index}",
            repository_root=repository_root,
        )
        role = record.get("role")
        if not isinstance(role, str) or not role:
            raise ReviewSiteError(f"{lesson['id']}: QA input {index} has no role")
        relative = str(path.relative_to(repository_root))
        paths_by_role.setdefault(role, set()).add(relative)
        records.append(
            {"role": role, "path": relative, "sha256": str(record["sha256"])}
        )

    expected_roles = {
        "lesson_metadata": str(lesson["metadata_path"]),
        "scene_file": str(lesson["scene_file"]),
        "presenter_script": str(lesson["presenter_script"]),
        "storyboard": str(lesson["storyboard"]),
    }
    for role, expected_path in expected_roles.items():
        if paths_by_role.get(role) != {expected_path}:
            raise ReviewSiteError(
                f"{lesson['id']}: QA {role} binding differs from metadata"
            )
    return records


def load_reviewable_lesson(
    lesson: dict[str, Any],
    asset_map: dict[str, BoundAsset],
    *,
    repository_root: Path = ROOT,
    live_qa_root: Path = LIVE_QA_ROOT,
) -> dict[str, Any]:
    lesson_id = lesson["id"]
    report_path = live_qa_root / f"{safe_id(lesson_id)}.json"
    if not report_path.is_file():
        raise ReviewSiteError(f"{lesson_id}: fresh QA report is missing")
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ReviewSiteError(f"{lesson_id}: invalid QA report: {error}") from error
    if report.get("schema_version") != QA_SCHEMA_VERSION:
        raise ReviewSiteError(f"{lesson_id}: refresh QA for the local verifier")
    if report.get("id") != lesson_id:
        raise ReviewSiteError(f"{lesson_id}: QA report names another lesson")
    if report.get("scene_class") != lesson.get("scene_class"):
        raise ReviewSiteError(f"{lesson_id}: QA scene class differs")
    if report.get("status") != "ok" or report.get("errors"):
        raise ReviewSiteError(f"{lesson_id}: mechanical QA is not clean")
    if not isinstance(report.get("generated_at"), str):
        raise ReviewSiteError(f"{lesson_id}: QA generation time is missing")

    input_records = require_report_inputs(
        lesson, report, repository_root=repository_root
    )
    bindings: dict[Path, BoundAsset] = {}

    def remember(path: Path, expected_hash: str) -> None:
        stat = path.stat()
        bindings[path] = BoundAsset(
            path=path,
            sha256=expected_hash,
            size=stat.st_size,
            mtime_ns=stat.st_mtime_ns,
        )

    remember(report_path, sha256(report_path))
    for input_record in input_records:
        remember(
            repository_root / input_record["path"],
            input_record["sha256"],
        )
    manifest_path = checked_record_path(
        report.get("manifest"),
        allowed_root=repository_root / "slides",
        label=f"{lesson_id}: Slides manifest",
        repository_root=repository_root,
    )
    expected_manifest = repository_root / "slides" / f"{lesson['scene_class']}.json"
    if manifest_path != expected_manifest.resolve():
        raise ReviewSiteError(f"{lesson_id}: QA manifest path differs")
    remember(manifest_path, report["manifest"]["sha256"])

    contact_path = checked_record_path(
        report.get("contact_sheet"),
        allowed_root=repository_root / "build" / "qa" / "frames" / safe_id(lesson_id),
        label=f"{lesson_id}: contact sheet",
        repository_root=repository_root,
    )
    sweep_sheet_path = checked_record_path(
        report.get("transition_sweep"),
        allowed_root=repository_root / "build" / "qa" / "frames" / safe_id(lesson_id),
        label=f"{lesson_id}: transition sweep",
        repository_root=repository_root,
    )
    remember(contact_path, report["contact_sheet"]["sha256"])
    remember(sweep_sheet_path, report["transition_sweep"]["sha256"])

    beats = lesson.get("beats", [])
    raw_segments = report.get("segments")
    if (
        not isinstance(raw_segments, list)
        or len(raw_segments) != len(beats)
        or not all(isinstance(segment, dict) for segment in raw_segments)
    ):
        raise ReviewSiteError(f"{lesson_id}: QA segment count differs")
    if [segment.get("beat_id") for segment in raw_segments] != [
        beat["id"] for beat in beats
    ]:
        raise ReviewSiteError(f"{lesson_id}: QA beat IDs differ")
    if [bool(segment.get("loop")) for segment in raw_segments] != [
        bool(beat.get("loop")) for beat in beats
    ]:
        raise ReviewSiteError(f"{lesson_id}: QA loop flags differ")

    script_path = repository_root / lesson["presenter_script"]
    script_sections = parse_presenter_sections(script_path)
    missing_script_beats = [
        beat["id"] for beat in beats if beat["id"] not in script_sections
    ]
    if missing_script_beats:
        raise ReviewSiteError(
            f"{lesson_id}: presenter script is missing beat(s): "
            + ", ".join(missing_script_beats)
        )

    frame_root = repository_root / "build" / "qa" / "frames" / safe_id(lesson_id)
    segments: list[dict[str, Any]] = []
    binding_segments: list[dict[str, Any]] = []
    for segment, beat in zip(raw_segments, beats, strict=True):
        if segment.get("resolution") != [1920, 1080]:
            raise ReviewSiteError(
                f"{lesson_id}: {segment.get('beat_id')} is not 1920x1080"
            )
        media_record = {
            "path": segment.get("file"),
            "sha256": segment.get("sha256"),
        }
        media_path = checked_record_path(
            media_record,
            allowed_root=repository_root / "slides",
            label=f"{lesson_id}: {segment['beat_id']} media",
            repository_root=repository_root,
        )
        remember(media_path, segment["sha256"])
        preview_record = segment.get("preview")
        preview_path = checked_record_path(
            preview_record,
            allowed_root=frame_root,
            label=f"{lesson_id}: {segment['beat_id']} settled frame",
            repository_root=repository_root,
        )
        remember(preview_path, preview_record["sha256"])
        raw_sweeps = segment.get("sweep_previews")
        if not isinstance(raw_sweeps, list) or len(raw_sweeps) < 1:
            raise ReviewSiteError(
                f"{lesson_id}: {segment['beat_id']} has no transition sweep"
            )
        sweeps: list[dict[str, Any]] = []
        for sweep_index, sweep_record in enumerate(raw_sweeps, start=1):
            sweep_path = checked_record_path(
                sweep_record,
                allowed_root=frame_root,
                label=(
                    f"{lesson_id}: {segment['beat_id']} sweep {sweep_index}"
                ),
                repository_root=repository_root,
            )
            remember(sweep_path, sweep_record["sha256"])
            at_seconds = sweep_record.get("at_seconds")
            if not isinstance(at_seconds, (int, float)) or at_seconds < 0:
                raise ReviewSiteError(
                    f"{lesson_id}: {segment['beat_id']} sweep time is invalid"
                )
            sweeps.append(
                {
                    "at_seconds": float(at_seconds),
                    "url": register_asset(
                        sweep_path, asset_map, repository_root=repository_root
                    ),
                }
            )
        preview_at = preview_record.get("at_seconds")
        if not isinstance(preview_at, (int, float)) or preview_at < 0:
            raise ReviewSiteError(
                f"{lesson_id}: {segment['beat_id']} preview time is invalid"
            )
        segments.append(
            {
                "number": int(segment["number"]),
                "beat_id": str(segment["beat_id"]),
                "loop": bool(segment.get("loop")),
                "duration": float(segment["duration"]),
                "resolution": segment["resolution"],
                "loop_endpoint_difference": segment.get(
                    "loop_endpoint_mean_absolute_difference"
                ),
                "video_url": register_asset(
                    media_path, asset_map, repository_root=repository_root
                ),
                "preview_url": register_asset(
                    preview_path, asset_map, repository_root=repository_root
                ),
                "preview_at_seconds": float(preview_at),
                "sweeps": sweeps,
                "first_frame": segment.get("first_frame", {}),
                "last_frame": segment.get("last_frame", {}),
                "script": script_sections[beat["id"]],
            }
        )
        binding_segments.append(
            {
                "beat_id": segment["beat_id"],
                "media_sha256": segment["sha256"],
                "preview_sha256": preview_record["sha256"],
                "sweep_sha256": [item["sha256"] for item in raw_sweeps],
            }
        )

    binding_payload = {
        "inputs": sorted(
            input_records, key=lambda item: (item["role"], item["path"])
        ),
        "manifest_sha256": report["manifest"]["sha256"],
        "segments": binding_segments,
        "contact_sheet_sha256": report["contact_sheet"]["sha256"],
        "transition_sweep_sha256": report["transition_sweep"]["sha256"],
    }
    review_binding_digest = digest_json(binding_payload)
    report_digest = sha256(report_path)
    artifact_digest = digest_json(
        {"report_sha256": report_digest, **binding_payload}
    )
    return {
        "id": lesson_id,
        "safe_id": safe_id(lesson_id),
        "title": lesson["title"],
        "collection_id": lesson["collection_id"],
        "collection_title": lesson.get("collection_title", lesson["collection_id"]),
        "production_state": lesson["production_state"],
        "estimated_minutes": lesson.get("estimated_minutes"),
        "expected_answer": lesson.get("expected_answer", ""),
        "independent_check": lesson.get("independent_check", ""),
        "tags": lesson.get("tags", []),
        "qa_generated_at": report["generated_at"],
        "qa_report_sha256": report_digest,
        "artifact_digest": artifact_digest,
        "review_binding_digest": review_binding_digest,
        "contact_sheet_url": register_asset(
            contact_path, asset_map, repository_root=repository_root
        ),
        "transition_sweep_url": register_asset(
            sweep_sheet_path, asset_map, repository_root=repository_root
        ),
        "segments": segments,
        "_bindings": tuple(
            bindings[path] for path in sorted(bindings, key=lambda item: str(item))
        ),
    }


def reset_site_root(site_root: Path) -> None:
    if site_root.exists():
        shutil.rmtree(site_root)
    site_root.mkdir(parents=True)


def build_review_site(
    lessons: list[dict[str, Any]],
    *,
    site_root: Path = SITE_ROOT,
    repository_root: Path = ROOT,
    live_qa_root: Path = LIVE_QA_ROOT,
) -> tuple[dict[str, Any], dict[str, BoundAsset]]:
    reset_site_root(site_root)
    asset_map: dict[str, BoundAsset] = {}
    records: list[dict[str, Any]] = []
    blocked: list[dict[str, str]] = []
    for lesson in lessons:
        try:
            records.append(
                load_reviewable_lesson(
                    lesson,
                    asset_map,
                    repository_root=repository_root,
                    live_qa_root=live_qa_root,
                )
            )
        except ReviewSiteError as error:
            blocked.append(
                {
                    "id": str(lesson["id"]),
                    "title": str(lesson["title"]),
                    "collection_title": str(
                        lesson.get("collection_title", lesson["collection_id"])
                    ),
                    "reason": str(error),
                }
            )
    records.sort(key=lambda item: (item["collection_title"], item["id"]))
    blocked.sort(key=lambda item: (item["collection_title"], item["id"]))
    if not records and not blocked:
        raise ReviewSiteError("no lessons were selected")
    catalog = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "local_only": True,
        "summary": {
            "selected": len(lessons),
            "reviewable": len(records),
            "blocked": len(blocked),
            "segments": sum(len(record["segments"]) for record in records),
        },
        "lessons": records,
        "blocked": blocked,
    }
    for filename in ("index.html", "styles.css", "app.js"):
        source = STATIC_ROOT / filename
        if not source.is_file():
            raise ReviewSiteError(f"review-site asset is missing: {source}")
        shutil.copy2(source, site_root / filename)
    public_catalog = {
        **catalog,
        "lessons": [
            {key: value for key, value in record.items() if key != "_bindings"}
            for record in records
        ],
    }
    (site_root / "catalog.json").write_text(
        json.dumps(public_catalog, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (site_root / "asset-map.json").write_text(
        json.dumps(
            {
                token: {
                    "path": str(asset.path.relative_to(repository_root)),
                    "sha256": asset.sha256,
                }
                for token, asset in sorted(asset_map.items())
            },
            ensure_ascii=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return catalog, asset_map


def required_segment_criteria(segment: dict[str, Any]) -> tuple[str, ...]:
    if segment.get("loop"):
        return (*SEGMENT_CRITERIA, LOOP_CRITERION)
    return SEGMENT_CRITERIA


def blank_review(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "lesson_id": record["id"],
        "artifact_digest": record["artifact_digest"],
        "updated_at": None,
        "ready": False,
        "segments": {
            segment["beat_id"]: {
                "verdict": "pending",
                "criteria": {
                    criterion: False
                    for criterion in required_segment_criteria(segment)
                },
                "issue_tags": [],
                "notes": "",
            }
            for segment in record["segments"]
        },
        "lesson_criteria": {criterion: False for criterion in LESSON_CRITERIA},
        "notes": "",
    }


def clean_text(value: object, *, limit: int, label: str) -> str:
    if not isinstance(value, str):
        raise ReviewSiteError(f"{label} must be text")
    value = value.strip()
    if len(value) > limit:
        raise ReviewSiteError(f"{label} exceeds {limit} characters")
    return value


def normalize_review(payload: object, record: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ReviewSiteError("review payload must be an object")
    if payload.get("artifact_digest") != record["artifact_digest"]:
        raise ReviewSiteError("review artifact is stale; reload before saving")
    raw_segments = payload.get("segments")
    if not isinstance(raw_segments, dict):
        raise ReviewSiteError("segment reviews are missing")
    expected_ids = [segment["beat_id"] for segment in record["segments"]]
    if set(raw_segments) != set(expected_ids):
        raise ReviewSiteError("segment review IDs differ")

    cleaned_segments: dict[str, Any] = {}
    all_segments_pass = True
    for segment in record["segments"]:
        beat_id = segment["beat_id"]
        raw = raw_segments[beat_id]
        if not isinstance(raw, dict):
            raise ReviewSiteError(f"{beat_id}: review must be an object")
        verdict = raw.get("verdict")
        if verdict not in VERDICTS:
            raise ReviewSiteError(f"{beat_id}: invalid verdict")
        criteria = raw.get("criteria")
        required = required_segment_criteria(segment)
        if not isinstance(criteria, dict) or set(criteria) != set(required):
            raise ReviewSiteError(f"{beat_id}: review criteria differ")
        cleaned_criteria = {}
        for criterion in required:
            if not isinstance(criteria[criterion], bool):
                raise ReviewSiteError(f"{beat_id}: criterion must be Boolean")
            cleaned_criteria[criterion] = criteria[criterion]
        tags = raw.get("issue_tags", [])
        if (
            not isinstance(tags, list)
            or not all(isinstance(tag, str) and tag in ISSUE_TAGS for tag in tags)
        ):
            raise ReviewSiteError(f"{beat_id}: issue tags are invalid")
        cleaned_segments[beat_id] = {
            "verdict": verdict,
            "criteria": cleaned_criteria,
            "issue_tags": sorted(set(tags)),
            "notes": clean_text(
                raw.get("notes", ""), limit=4000, label=f"{beat_id} notes"
            ),
        }
        all_segments_pass &= verdict == "pass" and all(cleaned_criteria.values())

    raw_lesson_criteria = payload.get("lesson_criteria")
    if (
        not isinstance(raw_lesson_criteria, dict)
        or set(raw_lesson_criteria) != set(LESSON_CRITERIA)
    ):
        raise ReviewSiteError("lesson review criteria differ")
    lesson_criteria: dict[str, bool] = {}
    for criterion in LESSON_CRITERIA:
        value = raw_lesson_criteria[criterion]
        if not isinstance(value, bool):
            raise ReviewSiteError("lesson criterion must be Boolean")
        lesson_criteria[criterion] = value
    ready = all_segments_pass and all(lesson_criteria.values())
    return {
        "schema_version": REVIEW_SCHEMA_VERSION,
        "lesson_id": record["id"],
        "artifact_digest": record["artifact_digest"],
        "qa_report_sha256": record["qa_report_sha256"],
        "updated_at": utc_now(),
        "ready": ready,
        "segments": cleaned_segments,
        "lesson_criteria": lesson_criteria,
        "notes": clean_text(payload.get("notes", ""), limit=8000, label="lesson notes"),
    }


def review_path(lesson_id: str, review_root: Path = REVIEW_ROOT) -> Path:
    return review_root / f"{safe_id(lesson_id)}.json"


def read_review_state(
    record: dict[str, Any], review_root: Path = REVIEW_ROOT
) -> dict[str, Any]:
    path = review_path(record["id"], review_root)
    blank = blank_review(record)
    if not path.is_file():
        return {"review": blank, "stale": False, "previous_updated_at": None}
    try:
        stored = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"review": blank, "stale": True, "previous_updated_at": None}
    if (
        stored.get("schema_version") != REVIEW_SCHEMA_VERSION
        or stored.get("lesson_id") != record["id"]
        or stored.get("artifact_digest") != record["artifact_digest"]
    ):
        return {
            "review": blank,
            "stale": True,
            "previous_updated_at": stored.get("updated_at"),
        }
    return {"review": stored, "stale": False, "previous_updated_at": None}


def write_review_state(
    review: dict[str, Any], review_root: Path = REVIEW_ROOT
) -> Path:
    review_root.mkdir(parents=True, exist_ok=True)
    destination = review_path(review["lesson_id"], review_root)
    temporary = destination.with_suffix(".json.tmp")
    temporary.write_text(
        json.dumps(review, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, destination)
    return destination


def summarize_review(record: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    review = state["review"]
    segments = list(review["segments"].values())
    passed = sum(segment["verdict"] == "pass" for segment in segments)
    issues = sum(segment["verdict"] == "issue" for segment in segments)
    if state["stale"]:
        status = "stale"
    elif review.get("ready"):
        status = "ready"
    elif issues:
        status = "issue"
    elif passed:
        status = "in_progress"
    else:
        status = "not_started"
    return {
        "lesson_id": record["id"],
        "status": status,
        "passed_segments": passed,
        "issue_segments": issues,
        "segment_count": len(segments),
        "updated_at": review.get("updated_at"),
        "ready": bool(review.get("ready")),
    }


def write_public_status_feed(
    records: list[dict[str, Any]],
    review_root: Path = REVIEW_ROOT,
    destinations: tuple[Path, ...] | None = None,
) -> dict[str, Any]:
    """Publish sanitized progress only; private review notes never leave build/."""
    destinations = destinations or (PUBLIC_STATUS_PATH, BUILT_PUBLIC_STATUS_PATH)
    status_names = {
        "not_started": "not_started",
        "in_progress": "in_progress",
        "issue": "changes_needed",
        "ready": "review_complete",
        "stale": "stale",
    }
    entries = []
    for record in sorted(records, key=lambda item: item["id"]):
        summary = summarize_review(record, read_review_state(record, review_root))
        entries.append(
            {
                "lesson_id": record["id"],
                "review_binding_digest": record["review_binding_digest"],
                "status": status_names[summary["status"]],
                "passed_segments": summary["passed_segments"],
                "issue_segments": summary["issue_segments"],
                "segment_count": summary["segment_count"],
                "updated_at": summary["updated_at"],
            }
        )
    feed = {
        "schema_version": 1,
        "generated_at": utc_now(),
        "lessons": entries,
    }
    payload = json.dumps(feed, ensure_ascii=False, indent=2) + "\n"
    for destination in destinations:
        if destination == BUILT_PUBLIC_STATUS_PATH and not destination.parent.is_dir():
            continue
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(destination.suffix + ".tmp")
        temporary.write_text(payload, encoding="utf-8")
        os.replace(temporary, destination)
    return feed


def require_current_record(record: dict[str, Any]) -> None:
    bindings = record.get("_bindings")
    if not isinstance(bindings, tuple) or not bindings:
        raise ReviewSiteError("review evidence binding is missing")
    if not all(
        isinstance(binding, BoundAsset) and binding.is_current()
        for binding in bindings
    ):
        raise ReviewSiteError(
            "review evidence is stale; restart the local verifier"
        )


def parse_byte_range(value: str, size: int) -> tuple[int, int] | None:
    match = re.fullmatch(r"bytes=(\d*)-(\d*)", value.strip())
    if match is None:
        return None
    start_text, end_text = match.groups()
    if not start_text and not end_text:
        return None
    if start_text:
        start = int(start_text)
        end = int(end_text) if end_text else size - 1
    else:
        suffix = int(end_text)
        if suffix < 1:
            return None
        start = max(size - suffix, 0)
        end = size - 1
    if start >= size or end < start:
        return None
    return start, min(end, size - 1)


def copy_bytes(source: BinaryIO, destination: BinaryIO, count: int) -> None:
    remaining = count
    while remaining:
        chunk = source.read(min(1024 * 1024, remaining))
        if not chunk:
            break
        destination.write(chunk)
        remaining -= len(chunk)


class ReviewHTTPServer(ThreadingHTTPServer):
    catalog: dict[str, Any]
    asset_map: dict[str, BoundAsset]
    records: dict[str, dict[str, Any]]
    site_root: Path
    review_root: Path


class ReviewRequestHandler(BaseHTTPRequestHandler):
    server: ReviewHTTPServer

    def log_message(self, format: str, *args: object) -> None:
        sys.stderr.write("review-site: " + (format % args) + "\n")

    def send_json(self, value: object, status: int = HTTPStatus.OK) -> None:
        payload = (json.dumps(value, ensure_ascii=False) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(payload)

    def send_static(self, filename: str) -> None:
        path = (self.server.site_root / filename).resolve()
        if not path.is_relative_to(self.server.site_root.resolve()) or not path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        content = path.read_bytes()
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if path.suffix in {".html", ".css", ".js", ".json"}:
            content_type += "; charset=utf-8"
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(content)

    def send_asset(self, token: str) -> None:
        asset = self.server.asset_map.get(token)
        if asset is None or not asset.path.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        if not asset.is_current():
            self.send_error(
                HTTPStatus.CONFLICT,
                "review evidence changed; rebuild the local verifier",
            )
            return
        path = asset.path
        size = path.stat().st_size
        selected_range = None
        range_header = self.headers.get("Range")
        if range_header:
            selected_range = parse_byte_range(range_header, size)
            if selected_range is None:
                self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                self.send_header("Content-Range", f"bytes */{size}")
                self.end_headers()
                return
        content_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if selected_range is None:
            start, end = 0, size - 1
            status = HTTPStatus.OK
        else:
            start, end = selected_range
            status = HTTPStatus.PARTIAL_CONTENT
        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(length))
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "private, max-age=3600")
        if selected_range is not None:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self.end_headers()
        with path.open("rb") as handle:
            handle.seek(start)
            copy_bytes(handle, self.wfile, length)

    def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API.
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in {"/", "/index.html"}:
            self.send_static("index.html")
            return
        if path in {"/styles.css", "/app.js", "/catalog.json"}:
            self.send_static(path.removeprefix("/"))
            return
        if path.startswith("/asset/"):
            self.send_asset(path.removeprefix("/asset/"))
            return
        if path == "/api/reviews":
            summaries = []
            for record in self.server.records.values():
                state = read_review_state(record, self.server.review_root)
                try:
                    require_current_record(record)
                except ReviewSiteError:
                    state["stale"] = True
                summaries.append(summarize_review(record, state))
            self.send_json({"reviews": summaries})
            return
        if path.startswith("/api/reviews/"):
            lesson_id = path.removeprefix("/api/reviews/")
            record = self.server.records.get(lesson_id)
            if record is None:
                self.send_error(HTTPStatus.NOT_FOUND)
                return
            try:
                require_current_record(record)
            except ReviewSiteError as error:
                self.send_json({"error": str(error)}, HTTPStatus.CONFLICT)
                return
            self.send_json(read_review_state(record, self.server.review_root))
            return
        self.send_error(HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API.
        path = unquote(urlparse(self.path).path)
        if not path.startswith("/api/reviews/"):
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        lesson_id = path.removeprefix("/api/reviews/")
        record = self.server.records.get(lesson_id)
        if record is None:
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            require_current_record(record)
        except ReviewSiteError as error:
            self.send_json({"error": str(error)}, HTTPStatus.CONFLICT)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.send_error(HTTPStatus.BAD_REQUEST)
            return
        if content_length < 1 or content_length > 1024 * 1024:
            self.send_error(HTTPStatus.REQUEST_ENTITY_TOO_LARGE)
            return
        try:
            payload = json.loads(self.rfile.read(content_length).decode("utf-8"))
            review = normalize_review(payload, record)
            write_review_state(review, self.server.review_root)
            write_public_status_feed(
                list(self.server.records.values()), self.server.review_root
            )
        except (
            UnicodeDecodeError,
            json.JSONDecodeError,
            OSError,
            ReviewSiteError,
        ) as error:
            status = (
                HTTPStatus.CONFLICT
                if "stale" in str(error).lower()
                else HTTPStatus.BAD_REQUEST
            )
            self.send_json({"error": str(error)}, status)
            return
        self.send_json(
            {
                "review": review,
                "summary": summarize_review(
                    record,
                    {"review": review, "stale": False, "previous_updated_at": None},
                ),
            }
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument(
        "--status",
        default="draft_rendered,visual_verified,published",
        help="Select one production state or a comma-separated set of states.",
    )
    parser.add_argument(
        "--build-only",
        action="store_true",
        help="Generate build/review-site without starting the local server.",
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.port < 1 or args.port > 65535:
        print("ERROR: port must be between 1 and 65535", file=sys.stderr)
        return 2
    try:
        lessons = load_lessons()
        selected = select_lessons(lessons, args.ids, args.status)
        selected = [
            lesson
            for lesson in selected
            if lesson.get("production_state") in RENDERED_STATES
        ]
        if not selected:
            raise ReviewSiteError("no rendered lessons matched the selection")
        catalog, asset_map = build_review_site(selected)
    except (OSError, ReviewSiteError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    reviewable = catalog["summary"]["reviewable"]
    blocked = catalog["summary"]["blocked"]
    if args.build_only:
        print(
            f"Review site ready: {SITE_ROOT.relative_to(ROOT)} "
            f"({reviewable} reviewable, {blocked} blocked)"
        )
        return 0
    if reviewable < 1:
        print("ERROR: no lesson has fresh reviewable QA", file=sys.stderr)
        return 2

    server = ReviewHTTPServer(("127.0.0.1", args.port), ReviewRequestHandler)
    server.catalog = catalog
    server.asset_map = asset_map
    server.records = {record["id"]: record for record in catalog["lessons"]}
    server.site_root = SITE_ROOT
    server.review_root = REVIEW_ROOT
    try:
        write_public_status_feed(list(server.records.values()), server.review_root)
    except OSError as error:
        print(f"ERROR: could not publish review status: {error}", file=sys.stderr)
        server.server_close()
        return 2
    url = f"http://127.0.0.1:{args.port}/"
    print(
        f"Review site: {url} ({reviewable} reviewable, {blocked} blocked)",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
