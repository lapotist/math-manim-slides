#!/usr/bin/env python3
"""Assemble rights-cleared lesson media into the public mathematics library."""

from __future__ import annotations

import argparse
import base64
import binascii
import hashlib
import html
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import unicodedata
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit, urlunsplit

from markdown_it import MarkdownIt
from markdown_it.token import Token

try:
    from scripts.build_lessons import (
        ATTRIBUTION_MARKER,
        PROJECT_TITLE,
        PROJECT_URL,
        THIRD_PARTY_NOTICE_MARKER,
        load_lessons,
        select_lessons,
    )
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from build_lessons import (  # type: ignore[no-redef]
        ATTRIBUTION_MARKER,
        PROJECT_TITLE,
        PROJECT_URL,
        THIRD_PARTY_NOTICE_MARKER,
        load_lessons,
        select_lessons,
    )


ROOT = Path(__file__).resolve().parents[1]
SITE_ROOT = ROOT / "build" / "site"
STATIC_ROOT = ROOT / "scripts" / "public_site_assets"
QA_ROOT = ROOT / "qa"
DRAFT_QA_ROOT = ROOT / "build" / "qa"
DEPLOYABLE_STATES = {"draft_rendered", "visual_verified", "published"}
LEGAL_FILES = ("LICENSE", "LICENSE-CONTENT", "NOTICE.md", "SOURCES.md")
LEGAL_MARKDOWN_PAGES = {
    "SOURCES.md": {
        "output": "SOURCES.html",
        "label": "來源",
        "title": "來源與出處",
        "wide": True,
    },
    "NOTICE.md": {
        "output": "NOTICE.html",
        "label": "權利範圍",
        "title": "權利範圍",
        "wide": False,
    },
}
SITE_SCHEMA_VERSION = 2
REVIEW_STATUS_SCHEMA_VERSION = 1
DEFAULT_MAX_SITE_BYTES = 950 * 1024 * 1024
LESSON_ARTIFACT_SCHEMA_VERSION = 1
RENDER_CONTRACT_PATH = ROOT / "scripts" / "render-contract.json"
RENDER_CONTRACT = json.loads(RENDER_CONTRACT_PATH.read_text(encoding="ascii"))
LESSON_ID_RE = re.compile(
    r"[a-z0-9][a-z0-9_-]*(?:\.[a-z0-9][a-z0-9_-]*)*"
)
BEAT_ID_RE = re.compile(r"[a-z0-9][a-z0-9_-]*")
SCRIPT_HEADING_RE = re.compile(
    r"^##\s+\d+\s+([a-z0-9_-]+)(?:\s*｜(.*))?$", re.MULTILINE
)


class EmbeddedVideoParser(HTMLParser):
    """Collect self-contained Reveal background videos in document order."""

    PREFIX = "data:video/mp4;base64,"

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.encoded_videos: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag != "section":
            return
        for name, value in attrs:
            if name == "data-background-video" and value:
                if not value.startswith(self.PREFIX):
                    raise ValueError("standalone export contains an external video")
                self.encoded_videos.append(value[len(self.PREFIX) :])


def lesson_id_parts(lesson_id: str) -> tuple[str, ...]:
    if not isinstance(lesson_id, str) or LESSON_ID_RE.fullmatch(lesson_id) is None:
        raise ValueError(f"unsafe lesson ID: {lesson_id!r}")
    return tuple(lesson_id.split("."))


def repository_url_from_environment() -> str:
    server = os.environ.get("GITHUB_SERVER_URL")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if server and repository:
        return f"{server.rstrip('/')}/{repository.strip('/')}"
    return PROJECT_URL


def safe_id(lesson_id: str) -> str:
    return "_".join(lesson_id_parts(lesson_id))


def deck_relative_path(lesson_id: str) -> Path:
    return Path(*lesson_id_parts(lesson_id)).with_suffix(".html")


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


def lesson_artifact_fingerprint(
    lesson: dict[str, Any], repository_root: Path = ROOT
) -> str:
    """Bind a published lesson artifact to every render and export input."""
    metadata_path = repository_file(
        repository_root,
        lesson.get("metadata_path"),
        f"{lesson['id']}: lesson metadata",
    )
    problem_root = metadata_path.parent
    candidates = [
        repository_root / "pixi.toml",
        repository_root / "pixi.lock",
        repository_root / "pyproject.toml",
        repository_root / "scripts" / "build_lessons.py",
        repository_root / "scripts" / "qa_slides.py",
        repository_root / "scripts" / "prepare_tex.py",
        repository_root / "scripts" / "activate.sh",
        repository_root / "scripts" / "render-contract.json",
        repository_root / "tools" / "bin" / "xelatex",
        repository_root / "tools" / "bin" / "dvisvgm",
        repository_root / "LICENSES" / "Manim-Slides-5.6.0.txt",
        repository_root / "LICENSES" / "Reveal.js-6.0.1.txt",
    ]
    candidates.extend(
        path
        for path in sorted(problem_root.rglob("*"))
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    source_root = repository_root / "src"
    if source_root.is_dir():
        candidates.extend(sorted(source_root.rglob("*.py")))
    records = []
    seen: set[Path] = set()
    for candidate in candidates:
        if not candidate.is_file():
            continue
        resolved = candidate.resolve()
        if resolved in seen:
            continue
        if not resolved.is_relative_to(repository_root.resolve()):
            raise ValueError(f"artifact input leaves repository: {candidate}")
        seen.add(resolved)
        records.append(
            {
                "path": resolved.relative_to(repository_root.resolve()).as_posix(),
                "sha256": sha256(resolved),
            }
        )
    records.sort(key=lambda record: record["path"])
    return digest_json(
        {
            "schema_version": LESSON_ARTIFACT_SCHEMA_VERSION,
            "render_contract": RENDER_CONTRACT,
            "inputs": records,
        }
    )


def live_report_binding_digest(report: dict[str, Any]) -> str:
    """Return the stable join key shared with local human-review receipts."""
    raw_inputs = report.get("inputs")
    raw_segments = report.get("segments")
    manifest = report.get("manifest")
    contact_sheet = report.get("contact_sheet")
    transition_sweep = report.get("transition_sweep")
    if (
        not isinstance(raw_inputs, list)
        or not isinstance(raw_segments, list)
        or not isinstance(manifest, dict)
        or not isinstance(contact_sheet, dict)
        or not isinstance(transition_sweep, dict)
    ):
        raise ValueError("mechanical QA binding evidence is incomplete")
    inputs: list[dict[str, str]] = []
    for record in raw_inputs:
        if not isinstance(record, dict):
            raise ValueError("mechanical QA input binding is invalid")
        role = record.get("role")
        path = record.get("path")
        content_hash = record.get("sha256")
        if not all(isinstance(value, str) and value for value in (role, path, content_hash)):
            raise ValueError("mechanical QA input binding is invalid")
        inputs.append({"role": role, "path": path, "sha256": content_hash})
    inputs.sort(key=lambda item: (item["role"], item["path"]))

    segments: list[dict[str, Any]] = []
    for segment in raw_segments:
        if not isinstance(segment, dict):
            raise ValueError("mechanical QA segment binding is invalid")
        preview = segment.get("preview")
        sweeps = segment.get("sweep_previews")
        if not isinstance(preview, dict) or not isinstance(sweeps, list):
            raise ValueError("mechanical QA preview binding is incomplete")
        sweep_hashes = []
        for sweep in sweeps:
            if not isinstance(sweep, dict) or not isinstance(sweep.get("sha256"), str):
                raise ValueError("mechanical QA sweep binding is invalid")
            sweep_hashes.append(sweep["sha256"])
        segments.append(
            {
                "beat_id": segment.get("beat_id"),
                "media_sha256": segment.get("sha256"),
                "preview_sha256": preview.get("sha256"),
                "sweep_sha256": sweep_hashes,
            }
        )
    return digest_json(
        {
            "inputs": inputs,
            "manifest_sha256": manifest.get("sha256"),
            "segments": segments,
            "contact_sheet_sha256": contact_sheet.get("sha256"),
            "transition_sweep_sha256": transition_sweep.get("sha256"),
        }
    )


def committed_binding_digest(evidence: dict[str, Any]) -> str:
    """Bind a committed attestation without its timestamp or report bytes."""
    source_hashes = evidence.get("source_hashes", {})
    toolchain_hashes = evidence.get("toolchain_hashes", {})
    render = evidence.get("render", {})
    return digest_json(
        {
            "source_hashes": source_hashes,
            "toolchain_hashes": toolchain_hashes,
            "manifest": render.get("manifest"),
            "segments": render.get("segments"),
            "beats": render.get("beats"),
        }
    )


def repository_file(repository_root: Path, relative_path: object, label: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise ValueError(f"{label}: path is missing")
    root = repository_root.resolve()
    candidate = (root / relative_path).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ValueError(f"{label}: file is unavailable: {relative_path}")
    return candidate


def verify_recorded_file(
    repository_root: Path,
    record: object,
    expected_path: str,
    label: str,
) -> Path:
    if not isinstance(record, dict) or record.get("path") != expected_path:
        raise ValueError(f"{label}: recorded path differs")
    path = repository_file(repository_root, expected_path, label)
    if record.get("sha256") != sha256(path):
        raise ValueError(f"{label}: recorded hash is stale")
    return path


def verify_qa_binding(
    lesson: dict[str, Any], evidence: dict[str, Any], repository_root: Path
) -> None:
    lesson_id = lesson["id"]
    source_hashes = evidence.get("source_hashes")
    if not isinstance(source_hashes, dict):
        raise ValueError(f"{lesson_id}: QA source hashes are missing")
    source_fields = {
        "lesson_metadata": "metadata_path",
        "scene_file": "scene_file",
        "presenter_script": "presenter_script",
        "storyboard": "storyboard",
    }
    for record_name, lesson_field in source_fields.items():
        expected_path = lesson.get(lesson_field)
        if not isinstance(expected_path, str):
            raise ValueError(f"{lesson_id}: lesson {lesson_field} path is missing")
        verify_recorded_file(
            repository_root,
            source_hashes.get(record_name),
            expected_path,
            f"{lesson_id}: QA {record_name}",
        )

    toolchain_hashes = evidence.get("toolchain_hashes")
    if not isinstance(toolchain_hashes, dict):
        raise ValueError(f"{lesson_id}: QA toolchain hashes are missing")
    for relative_path in ("pixi.toml", "pixi.lock"):
        path = repository_file(
            repository_root, relative_path, f"{lesson_id}: QA {relative_path}"
        )
        if toolchain_hashes.get(relative_path) != sha256(path):
            raise ValueError(f"{lesson_id}: QA {relative_path} hash is stale")

    render = evidence["render"]
    manifest_path = f"slides/{lesson['scene_class']}.json"
    verify_recorded_file(
        repository_root,
        render.get("manifest"),
        manifest_path,
        f"{lesson_id}: QA Slides manifest",
    )
    slides_root = (repository_root / "slides").resolve()
    for segment in render["segments"]:
        segment_path = repository_file(
            repository_root,
            segment.get("path"),
            f"{lesson_id}: QA segment {segment.get('beat_id')}",
        )
        if not segment_path.is_relative_to(slides_root):
            raise ValueError(f"{lesson_id}: QA segment path is outside slides/")
        if segment.get("sha256") != sha256(segment_path):
            raise ValueError(
                f"{lesson_id}: QA segment {segment.get('beat_id')} hash is stale"
            )


def read_qa(
    lesson: dict[str, Any], qa_root: Path, repository_root: Path = ROOT
) -> tuple[dict[str, Any], Path]:
    qa_path = qa_root / f"{safe_id(lesson['id'])}.json"
    if not qa_path.is_file():
        raise ValueError(f"{lesson['id']}: missing committed QA attestation")
    try:
        evidence = json.loads(qa_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(f"{lesson['id']}: invalid QA attestation: {error}") from error

    if evidence.get("schema_version") != 2:
        raise ValueError(f"{lesson['id']}: unsupported QA attestation schema")
    if evidence.get("lesson_id") != lesson["id"]:
        raise ValueError(f"{lesson['id']}: QA attestation names another lesson")
    if evidence.get("scene_class") != lesson.get("scene_class"):
        raise ValueError(f"{lesson['id']}: QA scene class differs")
    if evidence.get("status") != "ok":
        raise ValueError(f"{lesson['id']}: QA attestation is not successful")
    review = evidence.get("review", {})
    if not isinstance(review, dict):
        raise ValueError(f"{lesson['id']}: QA review evidence is invalid")
    if review.get("mechanical") != "passed":
        raise ValueError(f"{lesson['id']}: mechanical QA is not passed")
    if review.get("visual") != "human_reviewed":
        raise ValueError(f"{lesson['id']}: visual QA is not human reviewed")
    if not review.get("mathematics"):
        raise ValueError(f"{lesson['id']}: mathematical QA evidence is missing")
    render = evidence.get("render", {})
    if not isinstance(render, dict):
        raise ValueError(f"{lesson['id']}: QA render evidence is invalid")
    beats = lesson.get("beats", [])
    expected_beats = [
        {"id": beat["id"], "loop": bool(beat.get("loop"))} for beat in beats
    ]
    if render.get("segment_count") != len(expected_beats):
        raise ValueError(f"{lesson['id']}: QA segment count differs")
    if render.get("resolution") != [1920, 1080]:
        raise ValueError(f"{lesson['id']}: QA render is not 1920x1080")
    if render.get("beats") != expected_beats:
        raise ValueError(f"{lesson['id']}: QA beat contract differs")
    segments = render.get("segments", [])
    if (
        not isinstance(segments, list)
        or len(segments) != len(expected_beats)
        or not all(isinstance(segment, dict) for segment in segments)
    ):
        raise ValueError(f"{lesson['id']}: QA segment evidence is incomplete")
    if [segment.get("beat_id") for segment in segments] != [
        beat["id"] for beat in expected_beats
    ]:
        raise ValueError(f"{lesson['id']}: QA segment IDs differ")
    verify_qa_binding(lesson, evidence, repository_root)
    return evidence, qa_path


def read_draft_qa(
    lesson: dict[str, Any], qa_root: Path, repository_root: Path = ROOT
) -> tuple[dict[str, Any], Path]:
    """Read source-bound mechanical QA without claiming a human review."""
    lesson_id = lesson["id"]
    qa_path = qa_root / f"{safe_id(lesson_id)}.json"
    if not qa_path.is_file():
        raise ValueError(f"{lesson_id}: missing fresh mechanical QA report")
    try:
        report = json.loads(qa_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(f"{lesson_id}: invalid mechanical QA report: {error}") from error
    if report.get("schema_version") != 2:
        raise ValueError(f"{lesson_id}: refresh mechanical QA for publication")
    if report.get("id") != lesson_id:
        raise ValueError(f"{lesson_id}: mechanical QA report names another lesson")
    if report.get("scene_class") != lesson.get("scene_class"):
        raise ValueError(f"{lesson_id}: mechanical QA scene class differs")
    if report.get("status") != "ok" or report.get("errors"):
        raise ValueError(f"{lesson_id}: mechanical QA report is not successful")
    if not isinstance(report.get("generated_at"), str):
        raise ValueError(f"{lesson_id}: mechanical QA generation time is missing")

    raw_inputs = report.get("inputs")
    if not isinstance(raw_inputs, list) or not raw_inputs:
        raise ValueError(f"{lesson_id}: mechanical QA input binding is missing")
    inputs_by_role: dict[str, list[dict[str, str]]] = {}
    for index, record in enumerate(raw_inputs, start=1):
        if not isinstance(record, dict):
            raise ValueError(f"{lesson_id}: QA input {index} is invalid")
        role = record.get("role")
        relative_path = record.get("path")
        if not isinstance(role, str) or not role:
            raise ValueError(f"{lesson_id}: QA input {index} role is missing")
        path = repository_file(
            repository_root,
            relative_path,
            f"{lesson_id}: QA input {index}",
        )
        if record.get("sha256") != sha256(path):
            raise ValueError(f"{lesson_id}: QA input {index} hash is stale")
        inputs_by_role.setdefault(role, []).append(
            {
                "path": str(relative_path),
                "sha256": str(record["sha256"]),
            }
        )
    expected_inputs = {
        "lesson_metadata": str(lesson["metadata_path"]),
        "scene_file": str(lesson["scene_file"]),
        "presenter_script": str(lesson["presenter_script"]),
        "storyboard": str(lesson["storyboard"]),
    }
    for role, expected_path in expected_inputs.items():
        records = inputs_by_role.get(role, [])
        if len(records) != 1 or records[0]["path"] != expected_path:
            raise ValueError(f"{lesson_id}: QA {role} binding differs")
    toolchain_hashes: dict[str, str] = {}
    for record in inputs_by_role.get("toolchain", []):
        toolchain_hashes[record["path"]] = record["sha256"]
    for relative_path in ("pixi.toml", "pixi.lock"):
        if toolchain_hashes.get(relative_path) != sha256(
            repository_root / relative_path
        ):
            raise ValueError(f"{lesson_id}: QA {relative_path} hash is stale")

    beats = lesson.get("beats", [])
    expected_beats = [
        {"id": beat["id"], "loop": bool(beat.get("loop"))} for beat in beats
    ]
    raw_segments = report.get("segments")
    if (
        not isinstance(raw_segments, list)
        or len(raw_segments) != len(expected_beats)
        or not all(isinstance(segment, dict) for segment in raw_segments)
    ):
        raise ValueError(f"{lesson_id}: mechanical QA segment count differs")
    if [segment.get("beat_id") for segment in raw_segments] != [
        beat["id"] for beat in expected_beats
    ]:
        raise ValueError(f"{lesson_id}: mechanical QA beat IDs differ")
    if [bool(segment.get("loop")) for segment in raw_segments] != [
        beat["loop"] for beat in expected_beats
    ]:
        raise ValueError(f"{lesson_id}: mechanical QA loop flags differ")

    slides_root = (repository_root / "slides").resolve()
    frame_root = (
        repository_root / "build" / "qa" / "frames" / safe_id(lesson_id)
    ).resolve()

    def verify_frame_record(record: object, label: str) -> None:
        if not isinstance(record, dict):
            raise ValueError(f"{label}: frame record is missing")
        path = repository_file(repository_root, record.get("path"), label)
        if not path.is_relative_to(frame_root):
            raise ValueError(f"{label}: frame is outside the lesson QA directory")
        if record.get("sha256") != sha256(path):
            raise ValueError(f"{label}: frame hash is stale")

    verify_frame_record(
        report.get("contact_sheet"), f"{lesson_id}: QA contact sheet"
    )
    verify_frame_record(
        report.get("transition_sweep"), f"{lesson_id}: QA transition sweep"
    )
    segments: list[dict[str, Any]] = []
    for segment in raw_segments:
        if segment.get("resolution") != [1920, 1080]:
            raise ValueError(f"{lesson_id}: draft segment is not 1920x1080")
        segment_path = repository_file(
            repository_root,
            segment.get("file"),
            f"{lesson_id}: mechanical QA segment {segment.get('beat_id')}",
        )
        if not segment_path.is_relative_to(slides_root):
            raise ValueError(f"{lesson_id}: draft segment path is outside slides/")
        if segment.get("sha256") != sha256(segment_path):
            raise ValueError(
                f"{lesson_id}: draft segment {segment.get('beat_id')} hash is stale"
            )
        duration = segment.get("duration")
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(
                f"{lesson_id}: draft segment {segment.get('beat_id')} duration is invalid"
            )
        verify_frame_record(
            segment.get("preview"),
            f"{lesson_id}: QA segment {segment.get('beat_id')} preview",
        )
        sweeps = segment.get("sweep_previews")
        if not isinstance(sweeps, list) or not sweeps:
            raise ValueError(
                f"{lesson_id}: QA segment {segment.get('beat_id')} sweep is missing"
            )
        for index, sweep in enumerate(sweeps, start=1):
            verify_frame_record(
                sweep,
                f"{lesson_id}: QA segment {segment.get('beat_id')} sweep {index}",
            )
        segments.append(
            {
                "beat_id": str(segment["beat_id"]),
                "path": str(segment["file"]),
                "sha256": str(segment["sha256"]),
                "duration": float(duration),
            }
        )

    manifest_path = f"slides/{lesson['scene_class']}.json"
    manifest = verify_recorded_file(
        repository_root,
        report.get("manifest"),
        manifest_path,
        f"{lesson_id}: draft Slides manifest",
    )
    evidence = {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "scene_class": lesson["scene_class"],
        "status": "ok",
        "verified_at": None,
        "review": {
            "mechanical": "passed",
            "visual": "pending_human_review",
            "mathematics": "pending renewed review after slide-boundary changes",
        },
        "render": {
            "segment_count": len(segments),
            "resolution": [1920, 1080],
            "beats": expected_beats,
            "manifest": {
                "path": manifest_path,
                "sha256": sha256(manifest),
            },
            "segments": segments,
        },
        "source_hashes": {
            role: records[0]
            for role, records in inputs_by_role.items()
            if role in expected_inputs and len(records) == 1
        },
        "toolchain_hashes": toolchain_hashes,
        "review_binding_digest": live_report_binding_digest(report),
    }
    return evidence, qa_path


def read_review_evidence(
    lesson: dict[str, Any],
    committed_qa_root: Path,
    draft_qa_root: Path,
    repository_root: Path = ROOT,
) -> tuple[dict[str, Any], Path]:
    if lesson.get("production_state") == "draft_rendered":
        return read_draft_qa(lesson, draft_qa_root, repository_root)
    return read_qa(lesson, committed_qa_root, repository_root)


def verify_export(
    lesson: dict[str, Any], export_path: Path, evidence: dict[str, Any]
) -> None:
    document = export_path.read_text(encoding="utf-8")
    if ATTRIBUTION_MARKER not in document:
        raise ValueError(f"{lesson['id']}: export lacks the legal appendix")
    if THIRD_PARTY_NOTICE_MARKER not in document:
        raise ValueError(f"{lesson['id']}: export lacks third-party notices")
    parser = EmbeddedVideoParser()
    actual_hashes: list[str] = []
    try:
        parser.feed(document)
        parser.close()
        for encoded_video in parser.encoded_videos:
            video = base64.b64decode(encoded_video, validate=True)
            actual_hashes.append(hashlib.sha256(video).hexdigest())
    except (binascii.Error, ValueError) as error:
        raise ValueError(f"{lesson['id']}: export contains invalid video data") from error
    expected_hashes = [
        segment["sha256"] for segment in evidence["render"]["segments"]
    ]
    if actual_hashes != expected_hashes:
        raise ValueError(
            f"{lesson['id']}: exported videos differ from the reviewed render"
        )


def validate_lesson(lesson: dict[str, Any]) -> None:
    lesson_id = lesson["id"]
    if lesson.get("production_state") not in DEPLOYABLE_STATES:
        raise ValueError(
            f"{lesson_id}: state {lesson.get('production_state')} is not deployable"
        )
    if lesson.get("release_rights_state") != "cleared":
        raise ValueError(f"{lesson_id}: deployment requires cleared release rights")


def make_thumbnail(segment_path: Path, destination: Path) -> None:
    from PIL import Image, UnidentifiedImageError

    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-sseof",
        "-0.08",
        "-i",
        str(segment_path),
        "-frames:v",
        "1",
        "-vf",
        "scale=480:-2",
        "-y",
        str(destination),
    ]
    completed = subprocess.run(command, cwd=ROOT, check=False)
    if completed.returncode != 0 or not destination.is_file():
        raise ValueError(f"could not create thumbnail from {segment_path}")
    try:
        with Image.open(destination) as thumbnail:
            thumbnail.load()
            if thumbnail.width != 480 or thumbnail.height < 2:
                raise ValueError(
                    f"thumbnail has unexpected dimensions: {thumbnail.size}"
                )
    except (OSError, UnidentifiedImageError) as error:
        raise ValueError(f"thumbnail is not a readable image: {destination}") from error


def thumbnail_source(
    evidence: dict[str, Any], repository_root: Path = ROOT
) -> Path:
    segments = evidence.get("render", {}).get("segments", [])
    if not segments:
        raise ValueError("QA attestation has no rendered segments")
    relative_path = Path(segments[0].get("path", ""))
    candidate = (repository_root / relative_path).resolve()
    slides_root = (repository_root / "slides").resolve()
    if not candidate.is_relative_to(slides_root) or not candidate.is_file():
        raise ValueError(f"QA thumbnail source is unavailable: {relative_path}")
    return candidate


def parse_presenter_titles(
    lesson: dict[str, Any], repository_root: Path = ROOT
) -> dict[str, str]:
    path = repository_file(
        repository_root,
        lesson.get("presenter_script"),
        f"{lesson['id']}: presenter script",
    )
    text = path.read_text(encoding="utf-8")
    return {
        match.group(1): (match.group(2) or match.group(1)).strip()
        for match in SCRIPT_HEADING_RE.finditer(text)
    }


def load_source_asset_urls(repository_root: Path = ROOT) -> dict[str, str]:
    path = repository_root / "catalog" / "source_assets.json"
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as error:
        raise ValueError(f"invalid source asset catalog: {error}") from error
    urls: dict[str, str] = {}
    for group in ("drive_assets", "youtube_assets"):
        records = data.get(group, [])
        if not isinstance(records, list):
            continue
        for record in records:
            if not isinstance(record, dict):
                continue
            asset_id = record.get("id")
            preview_url = record.get("preview_url")
            if (
                isinstance(asset_id, str)
                and isinstance(preview_url, str)
                and record.get("access_status") == "public"
            ):
                urls[asset_id] = preview_url
    return urls


def external_http_url(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    value = value.strip()
    if value.startswith("https://") or value.startswith("http://"):
        return value
    return None


def original_source_url(
    lesson: dict[str, Any], source_asset_urls: dict[str, str]
) -> str | None:
    if lesson.get("collection_source_origin") == "user_supplied":
        return None
    direct = external_http_url(lesson.get("source_asset_url"))
    if direct:
        return direct
    asset_id = lesson.get("source_asset_id")
    if isinstance(asset_id, str):
        return external_http_url(source_asset_urls.get(asset_id))
    return None


def problem_display(lesson: dict[str, Any]) -> dict[str, str]:
    display = lesson.get("problem_display")
    if not isinstance(display, dict):
        raise ValueError(f"{lesson['id']}: problem_display metadata is missing")
    kind = display.get("kind")
    locale = display.get("locale")
    text = display.get("text")
    if kind != "project_restatement":
        raise ValueError(f"{lesson['id']}: problem_display must be a project restatement")
    if locale != "zh-TW":
        raise ValueError(f"{lesson['id']}: problem_display locale must be zh-TW")
    if not isinstance(text, str) or not text.strip():
        raise ValueError(f"{lesson['id']}: problem_display text is missing")
    return {"kind": kind, "locale": locale, "text": text.strip()}


def problem_label(lesson: dict[str, Any]) -> str:
    question = lesson.get("question")
    part = lesson.get("part")
    if isinstance(question, int) and isinstance(part, int):
        return f"第 {part} 部分 · 第 {question} 題"
    if isinstance(question, int):
        return f"第 {question} 題"
    return str(lesson["title"])


def copy_segment_assets(
    lesson: dict[str, Any],
    evidence: dict[str, Any],
    site_root: Path,
    repository_root: Path,
) -> list[dict[str, Any]]:
    beats = lesson.get("beats", [])
    raw_segments = evidence.get("render", {}).get("segments", [])
    if len(raw_segments) != len(beats):
        raise ValueError(f"{lesson['id']}: segment packaging count differs")
    titles = parse_presenter_titles(lesson, repository_root)
    packaged: list[dict[str, Any]] = []
    for index, (beat, segment) in enumerate(
        zip(beats, raw_segments, strict=True), start=1
    ):
        beat_id = beat.get("id")
        if not isinstance(beat_id, str) or BEAT_ID_RE.fullmatch(beat_id) is None:
            raise ValueError(f"{lesson['id']}: unsafe beat ID {beat_id!r}")
        if segment.get("beat_id") != beat_id:
            raise ValueError(f"{lesson['id']}: segment order differs from metadata")
        source = repository_file(
            repository_root,
            segment.get("path"),
            f"{lesson['id']}: segment {beat_id}",
        )
        if segment.get("sha256") != sha256(source):
            raise ValueError(f"{lesson['id']}: segment {beat_id} hash is stale")
        relative = (
            Path("assets")
            / "segments"
            / safe_id(lesson["id"])
            / f"{index:02d}-{beat_id}.mp4"
        )
        destination = site_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        duration = segment.get("duration")
        packaged.append(
            {
                "number": index,
                "beat_id": beat_id,
                "title": titles.get(beat_id, beat_id.replace("_", " ")),
                "loop": bool(beat.get("loop")),
                "duration": (
                    round(float(duration), 3)
                    if isinstance(duration, (int, float)) and duration > 0
                    else None
                ),
                "path": relative.as_posix(),
                "sha256": str(segment["sha256"]),
            }
        )
    return packaged


def lesson_record_metadata(
    lesson: dict[str, Any],
    revision: str,
    repository_url: str,
    source_asset_urls: dict[str, str],
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    beats = lesson.get("beats", [])
    metadata_path = str(lesson["metadata_path"])
    source_asset_url = original_source_url(lesson, source_asset_urls)
    return {
        "id": lesson["id"],
        "title": lesson["title"],
        "problem_label": problem_label(lesson),
        "part": int(lesson.get("part") or 1),
        "question": int(lesson.get("question") or 0),
        "collection_id": lesson["collection_id"],
        "collection_title": lesson.get(
            "collection_display_title",
            lesson.get("collection_title", lesson["collection_id"]),
        ),
        "locale": lesson.get("locale", "zh-TW"),
        "production_state": lesson["production_state"],
        "release_rights_state": lesson["release_rights_state"],
        "estimated_minutes": lesson.get("estimated_minutes"),
        "beat_count": len(beats),
        "loop_count": sum(bool(beat.get("loop")) for beat in beats),
        "tags": lesson.get("tags", []),
        "problem_display": problem_display(lesson),
        "source_asset": lesson.get("source_asset", ""),
        "source_pages": lesson.get("source_pages", []),
        "source_locator": lesson.get("source_locator", ""),
        "source_credit": lesson.get("source_credit", ""),
        "source_url": external_http_url(lesson.get("source_url")),
        "original_source_url": source_asset_url,
        "solution_url": external_http_url(lesson.get("solution_url")),
        "source_availability": (
            "external_link"
            if source_asset_url
            else "locator_only"
        ),
        "artifact_fingerprint": lesson_artifact_fingerprint(
            lesson, repository_root
        ),
        "source_revision": revision,
        "metadata_url": f"{repository_url}/blob/{revision}/{metadata_path}",
    }


def make_record(
    lesson: dict[str, Any],
    evidence: dict[str, Any],
    qa_path: Path,
    export_path: Path,
    revision: str,
    repository_url: str,
    thumbnail_path: str | None,
    thumbnail_sha256: str | None,
    segments: list[dict[str, Any]],
    source_asset_urls: dict[str, str],
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    render = evidence.get("render", {})
    review_state = evidence.get("review", {}).get("visual")
    binding_digest = evidence.get("review_binding_digest")
    if not isinstance(binding_digest, str):
        binding_digest = committed_binding_digest(evidence)
    return {
        **lesson_record_metadata(
            lesson,
            revision,
            repository_url,
            source_asset_urls,
            repository_root,
        ),
        "segment_count": render.get("segment_count"),
        "verified_at": evidence.get("verified_at"),
        "review_state": review_state,
        "review_binding_digest": binding_digest,
        "export_sha256": sha256(export_path),
        "qa_path": f"qa/{qa_path.name}",
        "qa_sha256": sha256(qa_path),
        "thumbnail_path": thumbnail_path,
        "thumbnail_sha256": thumbnail_sha256,
        "segments": segments,
    }


def reset_site_root(site_root: Path) -> None:
    if site_root.exists():
        shutil.rmtree(site_root)
    site_root.mkdir(parents=True)


def document_slug(text: str, fallback: str, used: set[str]) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    base = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-") or fallback
    candidate = base
    suffix = 2
    while candidate in used:
        candidate = f"{base}-{suffix}"
        suffix += 1
    used.add(candidate)
    return candidate


def inline_token_text(token: Token) -> str:
    if token.children is None:
        return token.content
    return "".join(
        child.content
        for child in token.children
        if child.type in {"text", "code_inline"}
    )


def annotate_document_tokens(tokens: list[Token]) -> None:
    used_heading_ids: set[str] = set()
    heading_count = 0
    table_count = 0
    table_headers: list[str] = []
    in_table_head = False
    in_table_body = False
    column_index = 0
    row_open: Token | None = None

    for index, token in enumerate(tokens):
        next_token = tokens[index + 1] if index + 1 < len(tokens) else None
        if token.type == "heading_open" and next_token is not None:
            heading_count += 1
            token.attrSet(
                "id",
                document_slug(
                    inline_token_text(next_token),
                    f"section-{heading_count}",
                    used_heading_ids,
                ),
            )
        elif token.type == "table_open":
            table_count += 1
            token.meta["document_table_number"] = table_count
            table_headers = []
        elif token.type == "thead_open":
            in_table_head = True
        elif token.type == "thead_close":
            in_table_head = False
        elif token.type == "tbody_open":
            in_table_body = True
        elif token.type == "tbody_close":
            in_table_body = False
        elif token.type == "tr_open":
            column_index = 0
            row_open = token if in_table_body else None
        elif token.type == "tr_close":
            row_open = None
        elif token.type == "th_open" and in_table_head:
            label = inline_token_text(next_token) if next_token is not None else ""
            table_headers.append(label.strip())
            token.attrSet("scope", "col")
        elif token.type == "td_open" and in_table_body:
            label = (
                table_headers[column_index]
                if column_index < len(table_headers)
                else f"Column {column_index + 1}"
            )
            token.attrSet("data-label", label)
            if "SHA-256" in label:
                token.attrJoin("class", "document-hash-cell")
            if column_index == 0 and next_token is not None and row_open is not None:
                identifier = inline_token_text(next_token).strip()
                if LESSON_ID_RE.fullmatch(identifier) is not None:
                    row_open.attrSet("id", f"source-{identifier}")
            column_index += 1


def repository_blob_url(
    repository_url: str,
    revision: str,
    relative_path: str,
    query: str = "",
    fragment: str = "",
) -> str:
    path = (
        f"{urlsplit(repository_url.rstrip('/')).path.rstrip('/')}"
        f"/blob/{quote(revision, safe='')}/{quote(relative_path, safe='/')}"
    )
    repository = urlsplit(repository_url)
    return urlunsplit((repository.scheme, repository.netloc, path, query, fragment))


def document_link_target(
    href: str,
    *,
    repository_url: str,
    revision: str,
) -> tuple[str, bool]:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return href, parsed.scheme in {"http", "https"}
    if not parsed.path or parsed.path.startswith("/"):
        return href, False
    if "\\" in parsed.path:
        raise ValueError(f"unsafe Markdown link path: {href}")
    target = posixpath.normpath(parsed.path)
    if target == ".." or target.startswith("../"):
        raise ValueError(f"Markdown link leaves repository root: {href}")
    if target in LEGAL_MARKDOWN_PAGES:
        output = str(LEGAL_MARKDOWN_PAGES[target]["output"])
        return urlunsplit(("", "", output, parsed.query, parsed.fragment)), False
    if target in LEGAL_FILES:
        return urlunsplit(("", "", target, parsed.query, parsed.fragment)), False
    return (
        repository_blob_url(
            repository_url,
            revision,
            target,
            parsed.query,
            parsed.fragment,
        ),
        True,
    )


def rewrite_document_links(
    tokens: list[Token],
    *,
    repository_url: str,
    revision: str,
) -> None:
    for token in tokens:
        for child in token.children or []:
            if child.type != "link_open":
                continue
            href = child.attrGet("href")
            if href is None:
                continue
            target, external = document_link_target(
                href,
                repository_url=repository_url,
                revision=revision,
            )
            child.attrSet("href", target)
            if external:
                child.attrSet("target", "_blank")
                child.attrSet("rel", "noopener noreferrer")


def render_safe_markdown_html(
    _renderer: object,
    tokens: list[Token],
    index: int,
    _options: dict[str, Any],
    _env: dict[str, Any],
) -> str:
    content = tokens[index].content
    stripped = content.strip()
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return ""
    if tokens[index].type == "html_inline" and re.fullmatch(
        r"<br\s*/?>", stripped, re.IGNORECASE
    ):
        return "<br>"
    return html.escape(content)


def render_document_table_open(
    _renderer: object,
    tokens: list[Token],
    index: int,
    _options: dict[str, Any],
    _env: dict[str, Any],
) -> str:
    number = int(tokens[index].meta.get("document_table_number", 1))
    return (
        '<div class="document-table" role="region" '
        f'aria-label="資料表 {number}" tabindex="0">\n'
        '<table class="document-data-table">\n'
    )


def render_document_table_close(
    _renderer: object,
    _tokens: list[Token],
    _index: int,
    _options: dict[str, Any],
    _env: dict[str, Any],
) -> str:
    return "</table>\n</div>\n"


def render_document_cell_open(
    renderer: Any,
    tokens: list[Token],
    index: int,
    options: dict[str, Any],
    env: dict[str, Any],
) -> str:
    return (
        renderer.renderToken(tokens, index, options, env)
        + '<span class="document-cell-value">'
    )


def render_document_cell_close(
    renderer: Any,
    tokens: list[Token],
    index: int,
    options: dict[str, Any],
    env: dict[str, Any],
) -> str:
    return "</span>" + renderer.renderToken(tokens, index, options, env)


def render_legal_document(
    source_name: str,
    markdown_source: str,
    *,
    repository_url: str,
    revision: str,
) -> str:
    page = LEGAL_MARKDOWN_PAGES.get(source_name)
    if page is None:
        raise ValueError(f"unsupported legal Markdown page: {source_name}")
    markdown = MarkdownIt("commonmark", {"html": True}).enable("table")
    markdown.add_render_rule("html_inline", render_safe_markdown_html)
    markdown.add_render_rule("html_block", render_safe_markdown_html)
    markdown.add_render_rule("table_open", render_document_table_open)
    markdown.add_render_rule("table_close", render_document_table_close)
    markdown.add_render_rule("td_open", render_document_cell_open)
    markdown.add_render_rule("td_close", render_document_cell_close)
    tokens = markdown.parse(markdown_source)
    annotate_document_tokens(tokens)
    rewrite_document_links(
        tokens,
        repository_url=repository_url,
        revision=revision,
    )
    body = markdown.renderer.render(tokens, markdown.options, {})
    nav_links = []
    for name, candidate in LEGAL_MARKDOWN_PAGES.items():
        current = ' aria-current="page"' if name == source_name else ""
        nav_links.append(
            f'<a href="{candidate["output"]}"{current}>{candidate["label"]}</a>'
        )
    main_class = "document-main document-main-wide" if page["wide"] else "document-main"
    title = html.escape(str(page["title"]))
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <meta name="description" content="{title}：Math Manim Slides 專案文件">
  <title>{title}｜數學動畫題庫</title>
  <link rel="stylesheet" href="../styles.css">
</head>
<body class="document-page">
  <header class="topbar document-topbar">
    <a class="brand" href="../">數學動畫題庫</a>
    <nav class="top-links" aria-label="專案文件">
      <a href="../site-manifest.json">資料清單</a>
      {''.join(nav_links)}
    </nav>
  </header>
  <main class="{main_class}">
    <article class="document-body">
{body}
    </article>
    <footer class="document-footer">
      <a href="{html.escape(source_name, quote=True)}">檢視原始 Markdown</a>
    </footer>
  </main>
</body>
</html>
"""


def copy_legal_files(
    site_root: Path,
    repository_root: Path = ROOT,
    *,
    revision: str = "main",
    repository_url: str = PROJECT_URL,
) -> None:
    legal_root = site_root / "legal"
    legal_root.mkdir()
    markdown_sources: dict[str, str] = {}
    for filename in LEGAL_FILES:
        source = repository_root / filename
        if not source.is_file():
            raise ValueError(f"missing required legal file: {filename}")
        shutil.copy2(source, legal_root / filename)
        if filename in LEGAL_MARKDOWN_PAGES:
            markdown_sources[filename] = source.read_text(encoding="utf-8")
    for filename, markdown_source in markdown_sources.items():
        output = str(LEGAL_MARKDOWN_PAGES[filename]["output"])
        (legal_root / output).write_text(
            render_legal_document(
                filename,
                markdown_source,
                repository_url=repository_url,
                revision=revision,
            ),
            encoding="utf-8",
        )


def copy_static_assets(site_root: Path) -> None:
    for filename in ("index.html", "styles.css", "app.js"):
        source = STATIC_ROOT / filename
        if not source.is_file():
            raise ValueError(f"missing public-site asset: {source}")
        shutil.copy2(source, site_root / filename)


def review_status_feed_url(repository_url: str) -> str:
    match = re.fullmatch(r"https://github\.com/([^/]+)/([^/]+?)(?:\.git)?/?", repository_url)
    if match is None:
        return "review-status.json"
    owner, repository = match.groups()
    return (
        f"https://raw.githubusercontent.com/{owner}/{repository}/main/"
        "qa/review-status.json"
    )


def initial_review_status(
    records: list[dict[str, Any]], status_path: Path
) -> dict[str, Any]:
    entries: dict[str, dict[str, Any]] = {}
    if status_path.is_file():
        try:
            candidate = json.loads(status_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as error:
            raise ValueError(f"invalid review status feed: {error}") from error
        if candidate.get("schema_version") != REVIEW_STATUS_SCHEMA_VERSION:
            raise ValueError("unsupported review status feed schema")
        raw_entries = candidate.get("lessons", [])
        if not isinstance(raw_entries, list):
            raise ValueError("review status feed lessons must be a list")
        entries = {
            str(entry.get("lesson_id")): entry
            for entry in raw_entries
            if isinstance(entry, dict)
        }
    generated = []
    for record in records:
        entry = entries.get(record["id"])
        if (
            not isinstance(entry, dict)
            or entry.get("review_binding_digest")
            != record["review_binding_digest"]
        ):
            entry = {
                "lesson_id": record["id"],
                "review_binding_digest": record["review_binding_digest"],
                "status": "not_started",
                "passed_segments": 0,
                "issue_segments": 0,
                "segment_count": record["segment_count"],
                "updated_at": None,
            }
        allowed_statuses = {
            "not_started",
            "in_progress",
            "changes_needed",
            "review_complete",
            "stale",
        }
        status = entry.get("status")
        if record.get("review_state") == "human_reviewed":
            status = "verified"
        elif status not in allowed_statuses:
            status = "not_started"
        generated.append(
            {
                "lesson_id": record["id"],
                "review_binding_digest": record["review_binding_digest"],
                "status": status,
                "passed_segments": int(entry.get("passed_segments") or 0),
                "issue_segments": int(entry.get("issue_segments") or 0),
                "segment_count": record["segment_count"],
                "updated_at": entry.get("updated_at"),
            }
        )
    return {
        "schema_version": REVIEW_STATUS_SCHEMA_VERSION,
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "lessons": generated,
    }


def directory_size(directory: Path, exclude: Path | None = None) -> int:
    return sum(
        path.stat().st_size
        for path in directory.rglob("*")
        if path.is_file() and path != exclude
    )


def write_site_outputs(
    site_root: Path,
    records: list[dict[str, Any]],
    *,
    selected_count: int,
    missing: list[str],
    repository_root: Path,
    revision: str,
    repository_url: str,
    max_site_bytes: int | None,
) -> None:
    if not records:
        raise ValueError("site has no deployable lesson exports")
    records.sort(
        key=lambda record: (
            record["collection_id"],
            record["part"],
            record["question"],
            record["id"],
        )
    )
    generated_at = datetime.now(UTC).replace(microsecond=0).isoformat()
    status_url = review_status_feed_url(repository_url)
    manifest = {
        "schema_version": SITE_SCHEMA_VERSION,
        "project": PROJECT_TITLE,
        "project_url": repository_url,
        "generated_at": generated_at,
        "source_revision": revision,
        "review_status_url": status_url,
        "summary": {
            "selected": selected_count,
            "deployed": len(records),
            "missing": len(missing),
            "site_bytes": 0,
        },
        "missing_lesson_ids": sorted(missing),
        "lessons": records,
    }
    library_data = {
        "schema_version": SITE_SCHEMA_VERSION,
        "review_status_url": status_url,
        "lessons": records,
    }
    (site_root / "library-data.js").write_text(
        "window.__MATH_LESSON_LIBRARY__ = "
        + json.dumps(library_data, ensure_ascii=False, separators=(",", ":"))
        + ";\n",
        encoding="utf-8",
    )
    status_feed = initial_review_status(
        records, repository_root / "qa" / "review-status.json"
    )
    (site_root / "review-status.json").write_text(
        json.dumps(status_feed, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (site_root / ".nojekyll").write_text("", encoding="ascii")
    manifest_path = site_root / "site-manifest.json"
    other_bytes = directory_size(site_root, exclude=manifest_path)
    manifest_bytes = b""
    for _ in range(8):
        manifest_bytes = (
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        site_bytes = other_bytes + len(manifest_bytes)
        if manifest["summary"]["site_bytes"] == site_bytes:
            break
        manifest["summary"]["site_bytes"] = site_bytes
    manifest_path.write_bytes(manifest_bytes)
    site_bytes = directory_size(site_root)
    if max_site_bytes is not None and site_bytes > max_site_bytes:
        raise ValueError(
            "site is "
            f"{site_bytes / (1024 * 1024):.1f} MiB; configured limit is "
            f"{max_site_bytes / (1024 * 1024):.1f} MiB"
        )


def assemble_site(
    lessons: list[dict[str, Any]],
    *,
    site_root: Path = SITE_ROOT,
    export_root: Path = ROOT / "dist",
    qa_root: Path = QA_ROOT,
    draft_qa_root: Path = DRAFT_QA_ROOT,
    repository_root: Path = ROOT,
    revision: str = "main",
    repository_url: str | None = None,
    allow_missing: bool = False,
    generate_thumbnails: bool = True,
    max_site_bytes: int | None = DEFAULT_MAX_SITE_BYTES,
) -> tuple[list[dict[str, Any]], list[str]]:
    if max_site_bytes is not None and max_site_bytes < 1:
        raise ValueError("site byte budget must be positive")
    repository_url = repository_url or repository_url_from_environment()
    reset_site_root(site_root)
    copy_static_assets(site_root)
    copy_legal_files(
        site_root,
        repository_root,
        revision=revision,
        repository_url=repository_url,
    )
    (site_root / "qa").mkdir()
    source_asset_urls = load_source_asset_urls(repository_root)

    records: list[dict[str, Any]] = []
    missing: list[str] = []
    errors: list[str] = []
    for lesson in lessons:
        try:
            validate_lesson(lesson)
            export_path = export_root / deck_relative_path(lesson["id"])
            if not export_path.is_file():
                if allow_missing:
                    missing.append(lesson["id"])
                    continue
                raise ValueError(f"{lesson['id']}: standalone export is missing")
            evidence, qa_path = read_review_evidence(
                lesson,
                qa_root,
                draft_qa_root,
                repository_root,
            )
            verify_export(lesson, export_path, evidence)

            deployed_qa = site_root / "qa" / qa_path.name
            shutil.copy2(qa_path, deployed_qa)

            segment_records = copy_segment_assets(
                lesson, evidence, site_root, repository_root
            )

            thumbnail_relative: str | None = None
            thumbnail_hash: str | None = None
            if generate_thumbnails:
                thumbnail_relative = (
                    Path("assets") / "thumbnails" / f"{safe_id(lesson['id'])}.webp"
                ).as_posix()
                make_thumbnail(
                    thumbnail_source(evidence, repository_root),
                    site_root / thumbnail_relative,
                )
                thumbnail_hash = sha256(site_root / thumbnail_relative)
            records.append(
                make_record(
                    lesson,
                    evidence,
                    deployed_qa,
                    export_path,
                    revision,
                    repository_url,
                    thumbnail_relative,
                    thumbnail_hash,
                    segment_records,
                    source_asset_urls,
                    repository_root,
                )
            )
        except (OSError, ValueError) as error:
            errors.append(str(error))

    if errors:
        raise ValueError("\n".join(errors))
    write_site_outputs(
        site_root,
        records,
        selected_count=len(lessons),
        missing=missing,
        repository_root=repository_root,
        revision=revision,
        repository_url=repository_url,
        max_site_bytes=max_site_bytes,
    )
    return records, missing


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument(
        "--status",
        default="draft_rendered,visual_verified,published",
        help="Select one production state or a comma-separated set of states.",
    )
    parser.add_argument(
        "--allow-missing",
        action="store_true",
        help="Build a partial local preview from exports that already exist.",
    )
    parser.add_argument(
        "--no-thumbnails",
        action="store_true",
        help="Skip extracting settled preview frames from rendered segments.",
    )
    parser.add_argument(
        "--revision",
        default=os.environ.get("GITHUB_SHA", "main"),
        help="Repository revision used by metadata links.",
    )
    parser.add_argument(
        "--repository-url",
        help=(
            "Repository base URL for source links; defaults to the current "
            "GitHub Actions repository or the canonical project."
        ),
    )
    parser.add_argument(
        "--max-site-mib",
        type=int,
        default=DEFAULT_MAX_SITE_BYTES // (1024 * 1024),
        help="Fail when the assembled site exceeds this many MiB (default: 950).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        lessons = load_lessons()
        selected = select_lessons(lessons, args.ids, args.status)
        if not selected:
            raise ValueError("no lessons matched the site selection")
        records, missing = assemble_site(
            selected,
            revision=args.revision,
            repository_url=args.repository_url,
            allow_missing=args.allow_missing,
            generate_thumbnails=not args.no_thumbnails,
            max_site_bytes=args.max_site_mib * 1024 * 1024,
        )
    except ValueError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(
        f"Site ready: {SITE_ROOT.relative_to(ROOT)} "
        f"({len(records)} deployed, {len(missing)} missing, "
        f"{directory_size(SITE_ROOT) / (1024 * 1024):.1f} MiB)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
