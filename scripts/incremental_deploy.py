#!/usr/bin/env python3
"""Plan and assemble an integrity-checked incremental Pages deployment."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PLAN_SCHEMA_VERSION = 1
DEPLOYABLE_STATES = {"draft_rendered", "visual_verified", "published"}
LESSON_ID_RE = re.compile(
    r"[a-z0-9][a-z0-9_-]*(?:\.[a-z0-9][a-z0-9_-]*)*"
)
SHA256_RE = re.compile(r"[0-9a-f]{64}")
GLOBAL_ARTIFACT_PATHS = {
    "pixi.toml",
    "pixi.lock",
    "pyproject.toml",
    "scripts/activate.sh",
    "scripts/build_lessons.py",
    "scripts/prepare_tex.py",
    "scripts/qa_slides.py",
    "scripts/render-contract.json",
}
GLOBAL_ARTIFACT_PREFIXES = ("src/", "tools/bin/", "LICENSES/")
SITE_PATHS = {
    "LICENSE",
    "LICENSE-CONTENT",
    "NOTICE.md",
    "SOURCES.md",
    "scripts/build_site.py",
    "scripts/incremental_deploy.py",
    "scripts/site-requirements.txt",
}
SITE_PREFIXES = (
    "catalog/",
    "docs/provenance/",
    "qa/",
    "scripts/public_site_assets/",
)
NO_PUBLIC_PATHS = {
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "scripts/freeze_qa.py",
    "scripts/import_site_taxonomy.py",
    "scripts/inventory_site.py",
    "scripts/publish_review_status.py",
    "scripts/review_site.py",
    "scripts/slide_density.py",
    "scripts/slide_transitions.py",
    "scripts/update_readme.py",
    "scripts/update_sources.py",
    "scripts/validate_catalog.py",
}
NO_PUBLIC_PREFIXES = (".github/", "docs/", "tests/", "scripts/review_site_assets/")
RENDER_CONTRACT_KEYS = ("container", "pixi", "cjk_font", "dvisvgm", "amsfonts")


def load_build_site() -> Any:
    try:
        return importlib.import_module("scripts.build_site")
    except ModuleNotFoundError:
        return importlib.import_module("build_site")


def load_render_contract(repository_root: Path = ROOT) -> dict[str, Any]:
    contract_path = repository_root / "scripts" / "render-contract.json"
    try:
        contract = json.loads(contract_path.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid render contract: {error}") from error
    if contract.get("schema_version") != 1 or contract.get("quality") != "h":
        raise ValueError("render contract schema or quality is invalid")
    for key in RENDER_CONTRACT_KEYS:
        value = contract.get(key)
        if not isinstance(value, str) or not value:
            raise ValueError(f"render contract key is invalid: {key}")
    return contract


def workflow_contains_render_pins(contract: dict[str, Any], workflow: str) -> bool:
    return all(str(contract[key]) in workflow for key in RENDER_CONTRACT_KEYS)


def validate_render_workflow_contract(repository_root: Path = ROOT) -> None:
    contract = load_render_contract(repository_root)
    workflow_path = repository_root / ".github" / "workflows" / "deploy-slides.yml"
    execute_path = repository_root / "scripts" / "incremental_deploy.py"
    try:
        workflow = workflow_path.read_text(encoding="utf-8")
        execute_source = execute_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ValueError(f"invalid render workflow: {error}") from error
    if not workflow_contains_render_pins(contract, workflow):
        for key in RENDER_CONTRACT_KEYS:
            if str(contract[key]) not in workflow:
                raise ValueError(
                    f"workflow does not implement render contract key: {key}"
                )
    if 'RENDER_CONTRACT["quality"]' not in execute_source:
        raise ValueError("render action does not use the contracted quality")


def is_render_contract_bootstrap(
    base_revision: str, repository_root: Path = ROOT
) -> bool:
    """Permit the first contract file only when the baseline used identical pins."""
    existing = subprocess.run(
        [
            "git",
            "cat-file",
            "-e",
            f"{base_revision}:scripts/render-contract.json",
        ],
        cwd=repository_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if existing.returncode == 0:
        return False
    try:
        baseline_workflow = git_output(
            ["show", f"{base_revision}:.github/workflows/deploy-slides.yml"],
            repository_root,
        )
    except subprocess.CalledProcessError:
        return False
    contract = load_render_contract(repository_root)
    return workflow_contains_render_pins(contract, baseline_workflow) and (
        f"--quality {contract['quality']}" in baseline_workflow
    )


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_id(lesson_id: str) -> str:
    if LESSON_ID_RE.fullmatch(lesson_id) is None:
        raise ValueError(f"unsafe lesson ID: {lesson_id!r}")
    return lesson_id.replace(".", "_")


def load_lesson_metadata(repository_root: Path = ROOT) -> dict[str, dict[str, Any]]:
    lessons: dict[str, dict[str, Any]] = {}
    for path in sorted(repository_root.glob("lessons/*/*/lesson.toml")):
        with path.open("rb") as handle:
            lesson = tomllib.load(handle)
        lesson_id = lesson.get("id")
        if not isinstance(lesson_id, str) or LESSON_ID_RE.fullmatch(lesson_id) is None:
            raise ValueError(f"invalid lesson ID in {path}")
        if lesson_id in lessons:
            raise ValueError(f"duplicate lesson ID: {lesson_id}")
        lesson["metadata_path"] = path.relative_to(repository_root).as_posix()
        lessons[lesson_id] = lesson
    return lessons


def deployable_ids(lessons: dict[str, dict[str, Any]]) -> list[str]:
    return sorted(
        lesson_id
        for lesson_id, lesson in lessons.items()
        if lesson.get("production_state") in DEPLOYABLE_STATES
    )


def git_output(arguments: list[str], repository_root: Path = ROOT) -> str:
    completed = subprocess.run(
        ["git", *arguments],
        cwd=repository_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return completed.stdout


def is_ancestor(base_revision: str, head_revision: str, repository_root: Path) -> bool:
    if not base_revision:
        return False
    completed = subprocess.run(
        ["git", "merge-base", "--is-ancestor", base_revision, head_revision],
        cwd=repository_root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.returncode == 0


def changed_paths(
    base_revision: str, head_revision: str, repository_root: Path = ROOT
) -> list[str]:
    output = subprocess.run(
        [
            "git",
            "diff",
            "--name-only",
            "-z",
            base_revision,
            head_revision,
            "--",
        ],
        cwd=repository_root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    ).stdout
    return sorted(
        value.decode("utf-8")
        for value in output.split(b"\0")
        if value
    )


def classify_paths(
    paths: list[str], lessons: dict[str, dict[str, Any]]
) -> tuple[str, list[str], list[str]]:
    current_ids = set(deployable_ids(lessons))
    lesson_roots = {
        str(PurePosixPath(str(lesson["metadata_path"])).parent): lesson_id
        for lesson_id, lesson in lessons.items()
    }
    collection_ids: dict[str, set[str]] = {}
    qa_ids = {f"qa/{safe_id(lesson_id)}.json": lesson_id for lesson_id in lessons}
    for lesson_id, lesson in lessons.items():
        collection = str(PurePosixPath(str(lesson["metadata_path"])).parents[1])
        collection_ids.setdefault(collection, set()).add(lesson_id)

    changed_ids: set[str] = set()
    reasons: set[str] = set()
    site_changed = False
    render_all = False
    for path in paths:
        if path in GLOBAL_ARTIFACT_PATHS or path.startswith(
            GLOBAL_ARTIFACT_PREFIXES
        ):
            render_all = True
            site_changed = True
            reasons.add(f"shared-artifact:{path}")
            continue
        matched_lesson = next(
            (
                lesson_id
                for root, lesson_id in lesson_roots.items()
                if path == root or path.startswith(f"{root}/")
            ),
            None,
        )
        if matched_lesson is not None:
            site_changed = True
            if matched_lesson in current_ids:
                changed_ids.add(matched_lesson)
            reasons.add(f"lesson:{matched_lesson}")
            continue
        matched_collection = next(
            (
                root
                for root in collection_ids
                if path == f"{root}/collection.toml"
            ),
            None,
        )
        if matched_collection is not None:
            site_changed = True
            reasons.add(f"collection:{matched_collection}")
            continue
        if path in qa_ids:
            site_changed = True
            if qa_ids[path] in current_ids:
                changed_ids.add(qa_ids[path])
            reasons.add(f"attestation:{qa_ids[path]}")
            continue
        if path == "qa/review-status.json":
            site_changed = True
            reasons.add("review-status")
            continue
        if path.startswith("lessons/"):
            site_changed = True
            reasons.add(f"lesson-inventory:{path}")
            continue
        if path in SITE_PATHS or path.startswith(SITE_PREFIXES):
            site_changed = True
            reasons.add(f"site:{path}")
            continue
        if path in NO_PUBLIC_PATHS or path.startswith(NO_PUBLIC_PREFIXES):
            continue
        raise ValueError(f"unclassified deployment input: {path}")

    if render_all:
        return "full", sorted(current_ids), sorted(reasons)
    if changed_ids:
        return "lessons", sorted(changed_ids), sorted(reasons)
    if site_changed:
        return "site", [], sorted(reasons)
    return "noop", [], ["no-public-output-change"]


def make_plan(
    *,
    base_revision: str,
    base_run_id: str,
    head_revision: str,
    force_full_rebuild: bool = False,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    lessons = load_lesson_metadata(repository_root)
    selected_ids = deployable_ids(lessons)
    if force_full_rebuild:
        mode = "full"
        selected = selected_ids
        paths: list[str] = []
        reasons = ["explicit-full-rebuild"]
    elif not base_revision or not base_run_id:
        raise ValueError(
            "no successful Pages baseline; explicitly request a full rebuild"
        )
    elif not is_ancestor(base_revision, head_revision, repository_root):
        raise ValueError(
            "Pages baseline is not an ancestor; explicitly request a full rebuild"
        )
    else:
        paths = changed_paths(base_revision, head_revision, repository_root)
        classification_paths = paths
        contract_bootstrap = (
            "scripts/render-contract.json" in paths
            and is_render_contract_bootstrap(base_revision, repository_root)
        )
        if contract_bootstrap:
            classification_paths = [
                path for path in paths if path != "scripts/render-contract.json"
            ]
        mode, selected, reasons = classify_paths(classification_paths, lessons)
        if contract_bootstrap:
            if mode == "noop":
                mode = "site"
            reasons = sorted([*reasons, "site:render-contract-bootstrap"])
    return {
        "schema_version": PLAN_SCHEMA_VERSION,
        "base_run_id": str(base_run_id),
        "base_revision": base_revision,
        "head_revision": head_revision,
        "mode": mode,
        "changed_lesson_ids": selected,
        "selected_lesson_count": len(selected_ids),
        "changed_paths": paths,
        "reasons": reasons,
    }


def write_plan(
    plan: dict[str, Any], output: Path, github_output: Path | None = None
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(plan, indent=2) + "\n", encoding="ascii")
    ids_path = output.with_name("changed-lessons.txt")
    ids_path.write_text(
        "".join(f"{lesson_id}\n" for lesson_id in plan["changed_lesson_ids"]),
        encoding="ascii",
    )
    if github_output is not None:
        with github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"mode={plan['mode']}\n")
            handle.write(f"changed_count={len(plan['changed_lesson_ids'])}\n")
            handle.write(f"base_run_id={plan['base_run_id']}\n")
            handle.write(f"base_revision={plan['base_revision']}\n")


def read_plan(path: Path) -> dict[str, Any]:
    try:
        plan = json.loads(path.read_text(encoding="ascii"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid deployment plan: {error}") from error
    if plan.get("schema_version") != PLAN_SCHEMA_VERSION:
        raise ValueError("unsupported deployment plan schema")
    mode = plan.get("mode")
    ids = plan.get("changed_lesson_ids")
    if mode not in {"noop", "site", "lessons", "full"}:
        raise ValueError("deployment plan mode is invalid")
    if not isinstance(ids, list) or any(
        not isinstance(value, str) or LESSON_ID_RE.fullmatch(value) is None
        for value in ids
    ):
        raise ValueError("deployment plan lesson IDs are invalid")
    if ids != sorted(set(ids)):
        raise ValueError("deployment plan lesson IDs are not unique and sorted")
    return plan


def execute_lesson_action(action: str, plan_path: Path, jobs: int) -> int:
    plan = read_plan(plan_path)
    ids = plan["changed_lesson_ids"]
    if not ids:
        raise ValueError("deployment plan has no changed lessons")
    if action in {"render", "export"}:
        command = [
            sys.executable,
            str(ROOT / "scripts" / "build_lessons.py"),
            action,
            *ids,
            "--jobs",
            str(jobs),
        ]
        if action == "render":
            build_site = load_build_site()
            command.extend(["--quality", build_site.RENDER_CONTRACT["quality"]])
    elif action == "qa":
        command = [sys.executable, str(ROOT / "scripts" / "qa_slides.py"), *ids]
    else:
        raise ValueError(f"unsupported lesson action: {action}")
    return subprocess.run(command, cwd=ROOT, check=False).returncode


def extract_pages_artifact(archive: Path, site_root: Path) -> None:
    if not archive.is_file():
        raise ValueError(f"Pages archive is missing: {archive}")
    site_root = site_root.resolve()
    if site_root == Path(site_root.anchor):
        raise ValueError("refusing to replace a filesystem root")
    if site_root.exists():
        shutil.rmtree(site_root)
    site_root.mkdir(parents=True)
    with tarfile.open(archive, "r:*") as handle:
        for member in handle.getmembers():
            relative = PurePosixPath(member.name)
            if relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"unsafe Pages archive path: {member.name}")
            if member.issym() or member.islnk() or not (
                member.isfile() or member.isdir()
            ):
                raise ValueError(f"unsupported Pages archive entry: {member.name}")
        handle.extractall(site_root, filter="data")


def checked_site_file(site_root: Path, relative_path: object, label: str) -> Path:
    if not isinstance(relative_path, str) or not relative_path:
        raise ValueError(f"{label}: path is missing")
    relative = PurePosixPath(relative_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise ValueError(f"{label}: unsafe path {relative_path!r}")
    root = site_root.resolve()
    candidate = (root / Path(*relative.parts)).resolve()
    if not candidate.is_relative_to(root) or not candidate.is_file():
        raise ValueError(f"{label}: file is missing: {relative_path}")
    return candidate


def require_hash(value: object, label: str) -> str:
    if not isinstance(value, str) or SHA256_RE.fullmatch(value) is None:
        raise ValueError(f"{label}: SHA-256 is invalid")
    return value


def copy_bound_file(
    source_root: Path,
    destination_root: Path,
    relative_path: object,
    expected_hash: object,
    label: str,
) -> Path:
    source = checked_site_file(source_root, relative_path, label)
    expected = require_hash(expected_hash, label)
    if sha256(source) != expected:
        raise ValueError(f"{label}: SHA-256 differs")
    relative = PurePosixPath(str(relative_path))
    destination = destination_root.joinpath(*relative.parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def expected_qa_inputs(
    lesson: dict[str, Any], repository_root: Path
) -> dict[str, str]:
    paths = [
        str(lesson["metadata_path"]),
        str(lesson["scene_file"]),
        str(lesson["presenter_script"]),
        str(lesson["storyboard"]),
        "pixi.toml",
        "pixi.lock",
    ]
    source_root = repository_root / "src"
    if source_root.is_dir():
        paths.extend(
            path.relative_to(repository_root).as_posix()
            for path in sorted(source_root.rglob("*.py"))
        )
    return {
        path: sha256(repository_root / path)
        for path in paths
        if (repository_root / path).is_file()
    }


def validate_reused_qa(
    lesson: dict[str, Any], record: dict[str, Any], qa_path: Path, repository_root: Path
) -> None:
    build_site = load_build_site()

    try:
        evidence = json.loads(qa_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{lesson['id']}: invalid reused QA: {error}") from error
    if evidence.get("status") != "ok":
        raise ValueError(f"{lesson['id']}: reused QA is not successful")
    expected_inputs = expected_qa_inputs(lesson, repository_root)
    if lesson.get("production_state") == "draft_rendered":
        if evidence.get("id") != lesson["id"]:
            raise ValueError(f"{lesson['id']}: reused draft QA names another lesson")
        inputs = evidence.get("inputs")
        if not isinstance(inputs, list):
            raise ValueError(f"{lesson['id']}: reused draft QA inputs are missing")
        recorded = {
            item.get("path"): item.get("sha256")
            for item in inputs
            if isinstance(item, dict)
        }
        if any(recorded.get(path) != digest for path, digest in expected_inputs.items()):
            raise ValueError(f"{lesson['id']}: reused draft QA inputs are stale")
        binding = build_site.live_report_binding_digest(evidence)
        raw_segments = evidence.get("segments", [])
        qa_hashes = [item.get("sha256") for item in raw_segments]
    else:
        if evidence.get("lesson_id") != lesson["id"]:
            raise ValueError(f"{lesson['id']}: reused QA names another lesson")
        recorded: dict[str, str] = {}
        for item in evidence.get("source_hashes", {}).values():
            if isinstance(item, dict) and isinstance(item.get("path"), str):
                recorded[item["path"]] = item.get("sha256")
        for path, digest in evidence.get("toolchain_hashes", {}).items():
            recorded[path] = digest
        required = {
            path: digest
            for path, digest in expected_inputs.items()
            if not path.startswith("src/")
        }
        if any(recorded.get(path) != digest for path, digest in required.items()):
            raise ValueError(f"{lesson['id']}: reused QA inputs are stale")
        binding = build_site.committed_binding_digest(evidence)
        raw_segments = evidence.get("render", {}).get("segments", [])
        qa_hashes = [item.get("sha256") for item in raw_segments]
    if binding != record.get("review_binding_digest"):
        raise ValueError(f"{lesson['id']}: reused QA binding differs")
    if qa_hashes != [item.get("sha256") for item in record.get("segments", [])]:
        raise ValueError(f"{lesson['id']}: reused QA segment hashes differ")


def copy_record_assets(
    record: dict[str, Any], source_root: Path, destination_root: Path
) -> None:
    lesson_id = str(record.get("id"))
    copy_bound_file(
        source_root,
        destination_root,
        record.get("qa_path"),
        record.get("qa_sha256"),
        f"{lesson_id}: QA",
    )
    for segment in record.get("segments", []):
        if not isinstance(segment, dict):
            raise ValueError(f"{lesson_id}: segment record is invalid")
        copy_bound_file(
            source_root,
            destination_root,
            segment.get("path"),
            segment.get("sha256"),
            f"{lesson_id}: segment {segment.get('beat_id')}",
        )
    thumbnail_path = record.get("thumbnail_path")
    if thumbnail_path:
        thumbnail = checked_site_file(
            source_root, thumbnail_path, f"{lesson_id}: thumbnail"
        )
        expected = record.get("thumbnail_sha256")
        if expected is not None and sha256(thumbnail) != require_hash(
            expected, f"{lesson_id}: thumbnail"
        ):
            raise ValueError(f"{lesson_id}: thumbnail SHA-256 differs")
        destination = destination_root.joinpath(*PurePosixPath(thumbnail_path).parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(thumbnail, destination)


def reused_record(
    lesson: dict[str, Any],
    previous: dict[str, Any],
    *,
    base_site: Path,
    revision: str,
    repository_url: str,
    source_asset_urls: dict[str, str],
    repository_root: Path,
) -> dict[str, Any]:
    build_site = load_build_site()

    lesson_id = lesson["id"]
    build_site.validate_lesson(lesson)
    if previous.get("id") != lesson_id:
        raise ValueError(f"{lesson_id}: reused record ID differs")
    if previous.get("production_state") != lesson.get("production_state"):
        raise ValueError(f"{lesson_id}: reused production state differs")
    current_fingerprint = build_site.lesson_artifact_fingerprint(
        lesson, repository_root
    )
    previous_fingerprint = previous.get("artifact_fingerprint")
    if previous_fingerprint is not None and previous_fingerprint != current_fingerprint:
        raise ValueError(f"{lesson_id}: reused artifact fingerprint differs")
    beats = lesson.get("beats", [])
    segments = previous.get("segments")
    if not isinstance(segments, list) or len(segments) != len(beats):
        raise ValueError(f"{lesson_id}: reused segment count differs")
    titles = build_site.parse_presenter_titles(lesson, repository_root)
    rebuilt_segments = []
    for index, (beat, segment) in enumerate(zip(beats, segments, strict=True), start=1):
        beat_id = beat.get("id")
        expected_path = (
            Path("assets")
            / "segments"
            / safe_id(lesson_id)
            / f"{index:02d}-{beat_id}.mp4"
        ).as_posix()
        if (
            not isinstance(segment, dict)
            or segment.get("number") != index
            or segment.get("beat_id") != beat_id
            or bool(segment.get("loop")) != bool(beat.get("loop"))
            or segment.get("path") != expected_path
        ):
            raise ValueError(f"{lesson_id}: reused segment contract differs")
        rebuilt_segments.append(
            {
                **segment,
                "title": titles.get(str(beat_id), str(beat_id).replace("_", " ")),
            }
        )
    qa_path = checked_site_file(
        base_site, previous.get("qa_path"), f"{lesson_id}: QA"
    )
    if sha256(qa_path) != require_hash(previous.get("qa_sha256"), f"{lesson_id}: QA"):
        raise ValueError(f"{lesson_id}: reused QA SHA-256 differs")
    validate_reused_qa(lesson, previous, qa_path, repository_root)
    thumbnail_path = previous.get("thumbnail_path")
    thumbnail_hash = None
    if thumbnail_path:
        thumbnail = checked_site_file(
            base_site, thumbnail_path, f"{lesson_id}: thumbnail"
        )
        thumbnail_hash = sha256(thumbnail)
        recorded_thumbnail_hash = previous.get("thumbnail_sha256")
        if recorded_thumbnail_hash is not None and recorded_thumbnail_hash != thumbnail_hash:
            raise ValueError(f"{lesson_id}: reused thumbnail SHA-256 differs")
    return {
        **build_site.lesson_record_metadata(
            lesson,
            revision,
            repository_url,
            source_asset_urls,
            repository_root,
        ),
        "segment_count": len(rebuilt_segments),
        "verified_at": previous.get("verified_at"),
        "review_state": previous.get("review_state"),
        "review_binding_digest": previous.get("review_binding_digest"),
        "export_sha256": require_hash(
            previous.get("export_sha256"), f"{lesson_id}: export"
        ),
        "qa_path": previous.get("qa_path"),
        "qa_sha256": previous.get("qa_sha256"),
        "thumbnail_path": thumbnail_path,
        "thumbnail_sha256": thumbnail_hash,
        "segments": rebuilt_segments,
    }


def assemble_incremental_site(
    *,
    plan_path: Path,
    base_site: Path,
    site_root: Path,
    revision: str,
    repository_root: Path = ROOT,
    repository_url: str | None = None,
) -> tuple[int, int]:
    build_site = load_build_site()

    plan = read_plan(plan_path)
    if plan["mode"] not in {"site", "lessons"}:
        raise ValueError("incremental assembly requires site or lessons mode")
    if plan.get("head_revision") != revision:
        raise ValueError("deployment plan revision differs")
    manifest_path = base_site / "site-manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid baseline site manifest: {error}") from error
    if manifest.get("schema_version") != build_site.SITE_SCHEMA_VERSION:
        raise ValueError("baseline site schema differs")
    if manifest.get("source_revision") != plan.get("base_revision"):
        raise ValueError("baseline site revision differs from the plan")
    summary = manifest.get("summary")
    if not isinstance(summary, dict) or summary.get("missing") != 0:
        raise ValueError("baseline site is incomplete")
    raw_records = manifest.get("lessons")
    if not isinstance(raw_records, list):
        raise ValueError("baseline site lesson records are missing")
    raw_ids = [item.get("id") for item in raw_records if isinstance(item, dict)]
    if (
        len(raw_ids) != len(raw_records)
        or len(raw_ids) != len(set(raw_ids))
        or summary.get("deployed") != len(raw_records)
    ):
        raise ValueError("baseline site lesson inventory is invalid")
    previous_records = {
        item.get("id"): item for item in raw_records if isinstance(item, dict)
    }

    lessons = build_site.load_lessons()
    selected = build_site.select_lessons(
        lessons, [], "draft_rendered,visual_verified,published"
    )
    selected_by_id = {lesson["id"]: lesson for lesson in selected}
    changed_ids = plan["changed_lesson_ids"]
    if any(lesson_id not in selected_by_id for lesson_id in changed_ids):
        raise ValueError("deployment plan names a non-deployable lesson")
    repository_url = repository_url or build_site.repository_url_from_environment()

    partial_root: Path | None = None
    fresh_records: dict[str, dict[str, Any]] = {}
    if changed_ids:
        partial_root = site_root.parent / "incremental-changed-site"
        records, missing = build_site.assemble_site(
            [selected_by_id[lesson_id] for lesson_id in changed_ids],
            site_root=partial_root,
            repository_root=repository_root,
            revision=revision,
            repository_url=repository_url,
        )
        if missing:
            raise ValueError("changed lesson build unexpectedly has missing exports")
        fresh_records = {record["id"]: record for record in records}

    build_site.reset_site_root(site_root)
    build_site.copy_static_assets(site_root)
    build_site.copy_legal_files(
        site_root,
        repository_root,
        revision=revision,
        repository_url=repository_url,
    )
    (site_root / "qa").mkdir()
    source_asset_urls = build_site.load_source_asset_urls(repository_root)
    final_records: list[dict[str, Any]] = []
    reused_count = 0
    for lesson in selected:
        lesson_id = lesson["id"]
        if lesson_id in fresh_records:
            record = fresh_records[lesson_id]
            assert partial_root is not None
            copy_record_assets(record, partial_root, site_root)
        else:
            previous = previous_records.get(lesson_id)
            if not isinstance(previous, dict):
                raise ValueError(f"{lesson_id}: no reusable baseline artifact")
            record = reused_record(
                lesson,
                previous,
                base_site=base_site,
                revision=revision,
                repository_url=repository_url,
                source_asset_urls=source_asset_urls,
                repository_root=repository_root,
            )
            copy_record_assets(record, base_site, site_root)
            reused_count += 1
        final_records.append(record)
    build_site.write_site_outputs(
        site_root,
        final_records,
        selected_count=len(selected),
        missing=[],
        repository_root=repository_root,
        revision=revision,
        repository_url=repository_url,
        max_site_bytes=build_site.DEFAULT_MAX_SITE_BYTES,
    )
    return reused_count, len(fresh_records)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan")
    plan_parser.add_argument("--base-revision", default="")
    plan_parser.add_argument("--base-run-id", default="")
    plan_parser.add_argument("--head-revision", default="HEAD")
    plan_parser.add_argument(
        "--full-rebuild", choices=("true", "false"), default="false"
    )
    plan_parser.add_argument("--output", type=Path, required=True)
    plan_parser.add_argument("--github-output", type=Path)

    extract_parser = subparsers.add_parser("extract")
    extract_parser.add_argument("--archive", type=Path, required=True)
    extract_parser.add_argument("--site-root", type=Path, required=True)

    execute_parser = subparsers.add_parser("execute")
    execute_parser.add_argument("action", choices=["render", "qa", "export"])
    execute_parser.add_argument("--plan", type=Path, required=True)
    execute_parser.add_argument("--jobs", type=int, default=2)

    assemble_parser = subparsers.add_parser("assemble")
    assemble_parser.add_argument("--plan", type=Path, required=True)
    assemble_parser.add_argument("--base-site", type=Path, required=True)
    assemble_parser.add_argument("--site-root", type=Path, required=True)
    assemble_parser.add_argument(
        "--revision", default=os.environ.get("GITHUB_SHA", "HEAD")
    )
    assemble_parser.add_argument("--repository-url")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.command == "plan":
            validate_render_workflow_contract(ROOT)
            head = git_output(
                ["rev-parse", "--verify", args.head_revision], ROOT
            ).strip()
            plan = make_plan(
                base_revision=args.base_revision,
                base_run_id=args.base_run_id,
                head_revision=head,
                force_full_rebuild=args.full_rebuild == "true",
                repository_root=ROOT,
            )
            write_plan(plan, args.output, args.github_output)
            print(
                f"Deployment plan: {plan['mode']} "
                f"({len(plan['changed_lesson_ids'])} changed lessons)"
            )
            return 0
        if args.command == "extract":
            extract_pages_artifact(args.archive, args.site_root)
            print(f"Extracted baseline site: {args.site_root}")
            return 0
        if args.command == "execute":
            if args.jobs < 1:
                raise ValueError("--jobs must be positive")
            return execute_lesson_action(args.action, args.plan, args.jobs)
        if args.command == "assemble":
            reused, fresh = assemble_incremental_site(
                plan_path=args.plan,
                base_site=args.base_site,
                site_root=args.site_root,
                revision=args.revision,
                repository_url=args.repository_url,
            )
            print(f"Incremental site ready: {reused} reused, {fresh} rebuilt")
            return 0
    except (OSError, ValueError, subprocess.CalledProcessError, tarfile.TarError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
