"""Checks for the deployable public mathematics lesson library."""

from __future__ import annotations

import base64
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from PIL import Image

from scripts import build_site


SEGMENTS = (("setup", b"reviewed setup video"), ("explore", b"reviewed loop video"))


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sample_lesson(lesson_id: str = "source.collection.q01") -> dict:
    return {
        "id": lesson_id,
        "collection_id": "source.collection",
        "collection_title": "Collection <One>",
        "title": "A < B & C",
        "scene_class": "ExampleSlide",
        "locale": "zh-TW",
        "production_state": "visual_verified",
        "release_rights_state": "cleared",
        "question": 1,
        "estimated_minutes": 6,
        "metadata_path": "lessons/collection/q01/lesson.toml",
        "scene_file": "lessons/collection/q01/deck.py",
        "presenter_script": "lessons/collection/q01/presenter.zh-TW.md",
        "storyboard": "lessons/collection/q01/storyboard.md",
        "source_credit": "Solution source",
        "source_url": "https://example.test/source?a=1&b=2",
        "source_asset": "sample-problems.pdf",
        "source_asset_url": "https://example.test/problems.pdf",
        "source_pages": [1],
        "source_locator": "Question 1, page 1",
        "solution_url": "https://example.test/solution",
        "problem_display": {
            "kind": "project_restatement",
            "locale": "zh-TW",
            "text": "設 a、b 為正整數且 a+b=12，求 ab 的最大值。",
        },
        "tags": ["geometry", "finite search"],
        "beats": [
            {"id": "setup", "loop": False},
            {"id": "explore", "loop": True},
        ],
    }


def write_export(
    export_root: Path,
    lesson_id: str,
    segments: tuple[tuple[str, bytes], ...] = SEGMENTS,
) -> Path:
    path = export_root / build_site.deck_relative_path(lesson_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    slides = "".join(
        '<section data-background-video="data:video/mp4;base64,'
        + base64.b64encode(video).decode("ascii")
        + '"></section>'
        for _, video in segments
    )
    path.write_text(
        "<html><body>"
        + slides
        + f"<{build_site.ATTRIBUTION_MARKER}>"
        + f"<!-- {build_site.THIRD_PARTY_NOTICE_MARKER} -->"
        + "</body></html>",
        encoding="utf-8",
    )
    return path


def write_repository_file(root: Path, relative_path: str, data: bytes) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return path


def file_record(root: Path, relative_path: str) -> dict[str, str]:
    return {
        "path": relative_path,
        "sha256": build_site.sha256(root / relative_path),
    }


def write_qa(repository_root: Path, lesson: dict) -> Path:
    lesson_id = lesson["id"]
    for field in ("metadata_path", "scene_file", "presenter_script", "storyboard"):
        write_repository_file(
            repository_root, lesson[field], f"{field}\n".encode("utf-8")
        )
    for filename in ("pixi.toml", "pixi.lock"):
        write_repository_file(repository_root, filename, f"{filename}\n".encode())
    for filename in build_site.LEGAL_FILES:
        write_repository_file(repository_root, filename, f"{filename}\n".encode())
    manifest_path = f"slides/{lesson['scene_class']}.json"
    write_repository_file(repository_root, manifest_path, b'{"slides": 2}\n')
    segment_records = []
    for beat_id, video in SEGMENTS:
        relative_path = f"slides/files/{beat_id}.mp4"
        write_repository_file(repository_root, relative_path, video)
        segment_records.append(
            {"beat_id": beat_id, "path": relative_path, "sha256": digest(video)}
        )

    qa_root = repository_root / "qa"
    qa_root.mkdir(exist_ok=True)
    path = qa_root / f"{build_site.safe_id(lesson_id)}.json"
    evidence = {
        "schema_version": 2,
        "lesson_id": lesson_id,
        "scene_class": "ExampleSlide",
        "verified_at": "2026-07-29",
        "status": "ok",
        "review": {
            "mechanical": "passed",
            "visual": "human_reviewed",
            "mathematics": "Independent exact check.",
        },
        "render": {
            "segment_count": 2,
            "resolution": [1920, 1080],
            "beats": [
                {"id": "setup", "loop": False},
                {"id": "explore", "loop": True},
            ],
            "manifest": file_record(repository_root, manifest_path),
            "segments": segment_records,
        },
        "source_hashes": {
            "lesson_metadata": file_record(repository_root, lesson["metadata_path"]),
            "scene_file": file_record(repository_root, lesson["scene_file"]),
            "presenter_script": file_record(
                repository_root, lesson["presenter_script"]
            ),
            "storyboard": file_record(repository_root, lesson["storyboard"]),
        },
        "toolchain_hashes": {
            filename: build_site.sha256(repository_root / filename)
            for filename in ("pixi.toml", "pixi.lock")
        },
    }
    path.write_text(json.dumps(evidence), encoding="utf-8")
    return path


def write_draft_qa(repository_root: Path, lesson: dict) -> Path:
    input_records = []
    roles = {
        "metadata_path": "lesson_metadata",
        "scene_file": "scene_file",
        "presenter_script": "presenter_script",
        "storyboard": "storyboard",
    }
    for field, role in roles.items():
        content = (
            "## 01 setup｜建立條件\n## 02 explore｜比較結果\n"
            if field == "presenter_script"
            else f"{field}\n"
        )
        write_repository_file(repository_root, lesson[field], content.encode("utf-8"))
        input_records.append(
            {**file_record(repository_root, lesson[field]), "role": role}
        )
    for filename in ("pixi.toml", "pixi.lock"):
        write_repository_file(repository_root, filename, f"{filename}\n".encode())
        input_records.append(
            {**file_record(repository_root, filename), "role": "toolchain"}
        )
    for filename in build_site.LEGAL_FILES:
        write_repository_file(repository_root, filename, f"{filename}\n".encode())
    manifest_path = f"slides/{lesson['scene_class']}.json"
    write_repository_file(repository_root, manifest_path, b'{"slides": 2}\n')
    segments = []
    for number, ((beat_id, video), beat) in enumerate(
        zip(SEGMENTS, lesson["beats"], strict=True),
        start=1,
    ):
        relative_path = f"slides/files/{beat_id}.mp4"
        write_repository_file(repository_root, relative_path, video)
        frame_root = f"build/qa/frames/{build_site.safe_id(lesson['id'])}"
        preview_path = f"{frame_root}/{number:02d}-{beat_id}.png"
        sweep_path = f"{frame_root}/sweep/{number:02d}-{beat_id}-01.jpg"
        write_repository_file(repository_root, preview_path, b"preview")
        write_repository_file(repository_root, sweep_path, b"sweep")
        segments.append(
            {
                "number": number,
                "beat_id": beat_id,
                "file": relative_path,
                "sha256": digest(video),
                "duration": float(number + 1),
                "resolution": [1920, 1080],
                "loop": bool(beat["loop"]),
                "preview": file_record(repository_root, preview_path),
                "sweep_previews": [file_record(repository_root, sweep_path)],
            }
        )
    frame_root = f"build/qa/frames/{build_site.safe_id(lesson['id'])}"
    contact_path = f"{frame_root}/contact-sheet.png"
    transition_path = f"{frame_root}/transition-sweep.jpg"
    write_repository_file(repository_root, contact_path, b"contact")
    write_repository_file(repository_root, transition_path, b"transition")
    qa_root = repository_root / "build" / "qa"
    qa_root.mkdir(parents=True, exist_ok=True)
    path = qa_root / f"{build_site.safe_id(lesson['id'])}.json"
    path.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "generated_at": "2026-07-30T00:00:00+00:00",
                "id": lesson["id"],
                "scene_class": lesson["scene_class"],
                "status": "ok",
                "errors": [],
                "inputs": input_records,
                "manifest": file_record(repository_root, manifest_path),
                "contact_sheet": file_record(repository_root, contact_path),
                "transition_sweep": file_record(
                    repository_root, transition_path
                ),
                "segments": segments,
            }
        ),
        encoding="utf-8",
    )
    return path


class SiteBuilderChecks(unittest.TestCase):
    def test_public_player_exposes_chapters_and_keyboard_navigation(self) -> None:
        html_source = (
            build_site.STATIC_ROOT / "index.html"
        ).read_text(encoding="utf-8")
        script = (build_site.STATIC_ROOT / "app.js").read_text(encoding="utf-8")

        self.assertIn('id="problem-list"', html_source)
        self.assertIn('id="lesson-video"', html_source)
        self.assertIn('id="problem-text"', html_source)
        self.assertIn('event.key === "ArrowRight"', script)
        self.assertIn('addEventListener("ended"', script)
        self.assertIn("selectSegment", script)
        self.assertNotIn(".play()", script)
        self.assertIn("elements.video.loop = false", script)
        self.assertIn(
            'elements.video.addEventListener("ended", () => {\n'
            "    elements.video.pause();\n"
            "  });",
            script,
        )
        self.assertIn('window.addEventListener("focus"', script)
        self.assertIn("isLoopbackPreview() ? 2000 : 30000", script)
        self.assertIn(
            "generatedAt > existing.generatedAt",
            script,
        )
        self.assertIn(
            'if (!isLoopbackPreview() && state.manifest.review_status_url)',
            script,
        )

    def test_default_selection_keeps_published_lessons(self) -> None:
        with mock.patch("sys.argv", ["build_site.py"]):
            args = build_site.parse_args()

        self.assertEqual(args.status, "draft_rendered,visual_verified,published")

    def test_repository_url_follows_the_actions_repository(self) -> None:
        with mock.patch.dict(
            "os.environ",
            {
                "GITHUB_SERVER_URL": "https://github.example",
                "GITHUB_REPOSITORY": "team/slides-fork",
            },
        ):
            url = build_site.repository_url_from_environment()

        self.assertEqual(url, "https://github.example/team/slides-fork")

    def test_lesson_id_cannot_escape_the_site_root(self) -> None:
        with self.assertRaisesRegex(ValueError, "unsafe lesson ID"):
            build_site.deck_relative_path("../outside")

    @mock.patch("scripts.build_site.subprocess.run")
    def test_thumbnail_accepts_a_small_valid_webp(self, run: mock.Mock) -> None:
        def write_thumbnail(command: list[str], **_: object) -> SimpleNamespace:
            destination = Path(command[-1])
            Image.new("RGB", (480, 270), "#101214").save(destination, "WEBP")
            return SimpleNamespace(returncode=0)

        run.side_effect = write_thumbnail
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "thumbnail.webp"
            build_site.make_thumbnail(Path("segment.mp4"), destination)
            size = destination.stat().st_size

        self.assertLess(size, 1024)

    def test_site_contains_only_validated_exports_and_qa(self) -> None:
        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            export_root = root / "dist"
            qa_root = root / "qa"
            site_root = root / "site"
            write_export(export_root, lesson["id"])
            write_qa(root, lesson)

            records, missing = build_site.assemble_site(
                [lesson],
                site_root=site_root,
                export_root=export_root,
                qa_root=qa_root,
                repository_root=root,
                revision="abc123",
                repository_url="https://github.example/acme/slides",
                generate_thumbnails=False,
            )

            index = (site_root / "index.html").read_text(encoding="utf-8")
            manifest = json.loads(
                (site_root / "site-manifest.json").read_text(encoding="utf-8")
            )
            deployed_deck = site_root / build_site.deck_relative_path(lesson["id"])
            segment_path = (
                site_root
                / "assets"
                / "segments"
                / build_site.safe_id(lesson["id"])
                / "01-setup.mp4"
            )
            deck_was_deployed = deployed_deck.is_file()
            deployed_segment = segment_path.read_bytes()
            status_feed = json.loads(
                (site_root / "review-status.json").read_text(encoding="utf-8")
            )
            site_bytes = sum(
                path.stat().st_size for path in site_root.rglob("*") if path.is_file()
            )

        self.assertEqual(missing, [])
        self.assertEqual(len(records), 1)
        self.assertFalse(deck_was_deployed)
        self.assertEqual(deployed_segment, SEGMENTS[0][1])
        self.assertIn("數學動畫題庫", index)
        self.assertIn("lesson-video", index)
        self.assertNotIn("https://cdn.", index)
        self.assertEqual(manifest["summary"]["selected"], 1)
        self.assertEqual(manifest["summary"]["deployed"], 1)
        self.assertEqual(manifest["summary"]["missing"], 0)
        self.assertEqual(manifest["summary"]["site_bytes"], site_bytes)
        self.assertEqual(manifest["lessons"][0]["loop_count"], 1)
        self.assertEqual(manifest["lessons"][0]["segments"][0]["beat_id"], "setup")
        self.assertEqual(
            manifest["lessons"][0]["problem_display"]["kind"],
            "project_restatement",
        )
        self.assertEqual(
            manifest["lessons"][0]["original_source_url"],
            "https://example.test/problems.pdf",
        )
        self.assertEqual(status_feed["lessons"][0]["status"], "verified")
        self.assertEqual(manifest["lessons"][0]["source_revision"], "abc123")
        self.assertEqual(
            manifest["lessons"][0]["metadata_url"],
            "https://github.example/acme/slides/blob/abc123/"
            "lessons/collection/q01/lesson.toml",
        )

    def test_site_rejects_uncleared_lesson(self) -> None:
        lesson = sample_lesson()
        lesson["release_rights_state"] = "pending"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", lesson["id"])
            write_qa(root, lesson)
            with self.assertRaisesRegex(ValueError, "cleared release rights"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                )

    def test_site_rejects_lesson_without_a_reviewed_problem_restatement(self) -> None:
        lesson = sample_lesson()
        lesson.pop("problem_display")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", lesson["id"])
            write_qa(root, lesson)
            with self.assertRaisesRegex(ValueError, "problem_display metadata"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                )

    def test_site_labels_fresh_draft_as_pending_human_review(self) -> None:
        lesson = sample_lesson()
        lesson["production_state"] = "draft_rendered"
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", lesson["id"])
            write_draft_qa(root, lesson)

            records, missing = build_site.assemble_site(
                [lesson],
                site_root=root / "site",
                export_root=root / "dist",
                qa_root=root / "qa",
                draft_qa_root=root / "build" / "qa",
                repository_root=root,
                generate_thumbnails=False,
            )
            index = (root / "site" / "index.html").read_text(encoding="utf-8")
            status_feed = json.loads(
                (root / "site" / "review-status.json").read_text(encoding="utf-8")
            )

        self.assertEqual(missing, [])
        self.assertEqual(records[0]["review_state"], "pending_human_review")
        self.assertIn("數學動畫題庫", index)
        self.assertEqual(status_feed["lessons"][0]["status"], "not_started")

    def test_site_rejects_export_without_notices(self) -> None:
        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            export_path = root / "dist" / build_site.deck_relative_path(lesson["id"])
            export_path.parent.mkdir(parents=True)
            export_path.write_text(
                f"<html><{build_site.ATTRIBUTION_MARKER}></html>",
                encoding="utf-8",
            )
            write_qa(root, lesson)
            with self.assertRaisesRegex(ValueError, "third-party notices"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                )

    def test_site_rejects_stale_source_bound_qa(self) -> None:
        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", lesson["id"])
            write_qa(root, lesson)
            (root / lesson["scene_file"]).write_text("changed\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "recorded hash is stale"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                )

    def test_site_rejects_export_from_another_render(self) -> None:
        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            changed_segments = (SEGMENTS[0], ("explore", b"different video"))
            write_export(root / "dist", lesson["id"], changed_segments)
            write_qa(root, lesson)

            with self.assertRaisesRegex(ValueError, "reviewed render"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                )

    def test_site_enforces_the_pages_size_budget(self) -> None:
        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", lesson["id"])
            write_qa(root, lesson)

            with self.assertRaisesRegex(ValueError, "configured limit"):
                build_site.assemble_site(
                    [lesson],
                    site_root=root / "site",
                    export_root=root / "dist",
                    qa_root=root / "qa",
                    repository_root=root,
                    generate_thumbnails=False,
                    max_site_bytes=10,
                )

    def test_partial_preview_reports_missing_exports(self) -> None:
        available = sample_lesson()
        missing_lesson = sample_lesson("source.collection.q02")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            write_export(root / "dist", available["id"])
            write_qa(root, available)

            records, missing = build_site.assemble_site(
                [available, missing_lesson],
                site_root=root / "site",
                export_root=root / "dist",
                qa_root=root / "qa",
                repository_root=root,
                allow_missing=True,
                generate_thumbnails=False,
            )

            manifest = json.loads(
                (root / "site" / "site-manifest.json").read_text(encoding="utf-8")
            )

        self.assertEqual(len(records), 1)
        self.assertEqual(missing, [missing_lesson["id"]])
        self.assertEqual(manifest["summary"]["missing"], 1)


if __name__ == "__main__":
    unittest.main()
