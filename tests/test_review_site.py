"""Focused checks for the local human slide-review backend."""

from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

from scripts import build_site, review_site


def write_file(root: Path, relative_path: str, content: bytes) -> Path:
    path = root / relative_path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
    return path


def file_record(root: Path, relative_path: str, **extra: object) -> dict[str, object]:
    path = root / relative_path
    return {
        "path": relative_path,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        **extra,
    }


class ReviewFixture:
    """Create one complete two-beat live-QA bundle without invoking ffmpeg."""

    lesson_id = "source.collection.q01"
    safe_id = "source_collection_q01"

    def __init__(self, root: Path) -> None:
        self.root = root
        self.qa_root = root / "build" / "qa"
        self.site_root = root / "review-site"
        self.review_root = root / "reviews"
        self.static_root = root / "static"
        for filename in ("index.html", "styles.css", "app.js"):
            write_file(root, f"static/{filename}", filename.encode("ascii"))

        self.lesson = {
            "id": self.lesson_id,
            "collection_id": "source.collection",
            "collection_title": "Fixture Collection",
            "title": "Fixture lesson",
            "scene_class": "FixtureSlide",
            "production_state": "draft_rendered",
            "estimated_minutes": 2,
            "metadata_path": "lessons/collection/q01/lesson.toml",
            "scene_file": "lessons/collection/q01/deck.py",
            "presenter_script": "lessons/collection/q01/presenter.zh-TW.md",
            "storyboard": "lessons/collection/q01/storyboard.md",
            "expected_answer": "42",
            "independent_check": "An exact independent check.",
            "tags": ["fixture"],
            "beats": [
                {"id": "setup", "loop": False},
                {"id": "explore", "loop": True},
            ],
        }
        write_file(root, self.lesson["metadata_path"], b"id = 'fixture'\n")
        write_file(root, self.lesson["scene_file"], b"class FixtureSlide: pass\n")
        write_file(
            root,
            self.lesson["presenter_script"],
            (
                "# Presenter\n\n"
                "## 01 setup\n\nSet up the concrete object. [NEXT]\n\n"
                "## 02 explore\n\nVary one quantity. [LOOP]\n"
            ).encode("utf-8"),
        )
        write_file(root, self.lesson["storyboard"], b"Prerequisite and misconception.\n")

        self.manifest_relative = "slides/FixtureSlide.json"
        write_file(root, self.manifest_relative, b'{"slides": 2}\n')
        self.frame_root = f"build/qa/frames/{self.safe_id}"
        self.contact_relative = f"{self.frame_root}/contact-sheet.png"
        self.transition_relative = f"{self.frame_root}/transition-sweep.jpg"
        write_file(root, self.contact_relative, b"contact sheet")
        write_file(root, self.transition_relative, b"transition sheet")

        segments = [
            self._write_segment(1, "setup", loop=False),
            self._write_segment(2, "explore", loop=True),
        ]
        input_roles = {
            "lesson_metadata": self.lesson["metadata_path"],
            "scene_file": self.lesson["scene_file"],
            "presenter_script": self.lesson["presenter_script"],
            "storyboard": self.lesson["storyboard"],
        }
        report = {
            "schema_version": review_site.QA_SCHEMA_VERSION,
            "generated_at": "2026-07-31T05:00:00+00:00",
            "id": self.lesson_id,
            "scene_class": self.lesson["scene_class"],
            "status": "ok",
            "errors": [],
            "inputs": [
                file_record(root, path, role=role)
                for role, path in input_roles.items()
            ],
            "manifest": file_record(root, self.manifest_relative),
            "contact_sheet": file_record(root, self.contact_relative),
            "transition_sweep": file_record(root, self.transition_relative),
            "segments": segments,
        }
        self.report_relative = f"build/qa/{self.safe_id}.json"
        self.report_path = write_file(
            root,
            self.report_relative,
            (json.dumps(report, indent=2) + "\n").encode("utf-8"),
        )

    def _write_segment(self, number: int, beat_id: str, *, loop: bool) -> dict:
        media_relative = f"slides/files/FixtureSlide/{beat_id}.mp4"
        preview_relative = f"{self.frame_root}/{number:02d}-{beat_id}.png"
        sweep_relatives = [
            f"{self.frame_root}/sweep/{number:02d}-{beat_id}-{sample:02d}.jpg"
            for sample in (1, 2)
        ]
        write_file(self.root, media_relative, f"{beat_id} media".encode("ascii"))
        write_file(self.root, preview_relative, f"{beat_id} preview".encode("ascii"))
        for sample, relative_path in enumerate(sweep_relatives, start=1):
            write_file(
                self.root,
                relative_path,
                f"{beat_id} sweep {sample}".encode("ascii"),
            )
        return {
            "number": number,
            "beat_id": beat_id,
            "file": media_relative,
            "sha256": file_record(self.root, media_relative)["sha256"],
            "duration": 2.0,
            "resolution": [1920, 1080],
            "first_frame": {"mean_luma": 20.0, "luma_stddev": 4.0},
            "last_frame": {"mean_luma": 21.0, "luma_stddev": 5.0},
            "preview": file_record(
                self.root, preview_relative, at_seconds=1.85
            ),
            "sweep_previews": [
                file_record(
                    self.root,
                    relative_path,
                    at_seconds=0.15 + (sample - 1) * 0.5,
                )
                for sample, relative_path in enumerate(sweep_relatives, start=1)
            ],
            "loop": loop,
            "loop_endpoint_mean_absolute_difference": 0.25 if loop else None,
        }

    def load(self) -> dict:
        return review_site.load_reviewable_lesson(
            self.lesson,
            {},
            repository_root=self.root,
            live_qa_root=self.qa_root,
        )

    def complete_payload(self, record: dict) -> dict:
        payload = review_site.blank_review(record)
        for segment in payload["segments"].values():
            segment["verdict"] = "pass"
            segment["criteria"] = {
                criterion: True for criterion in segment["criteria"]
            }
        payload["lesson_criteria"] = {
            criterion: True for criterion in payload["lesson_criteria"]
        }
        return payload


class ReviewSiteBackendChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.fixture = ReviewFixture(self.root)

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def test_fresh_hashed_evidence_builds_a_reviewable_site(self) -> None:
        with mock.patch.object(review_site, "STATIC_ROOT", self.fixture.static_root):
            catalog, asset_map = review_site.build_review_site(
                [self.fixture.lesson],
                site_root=self.fixture.site_root,
                repository_root=self.root,
                live_qa_root=self.fixture.qa_root,
            )

        self.assertEqual(catalog["summary"]["selected"], 1)
        self.assertEqual(catalog["summary"]["reviewable"], 1)
        self.assertEqual(catalog["summary"]["blocked"], 0)
        self.assertEqual(catalog["summary"]["segments"], 2)
        self.assertEqual(len(asset_map), 10)
        self.assertTrue((self.fixture.site_root / "catalog.json").is_file())
        self.assertTrue((self.fixture.site_root / "asset-map.json").is_file())
        record = catalog["lessons"][0]
        self.assertEqual(record["expected_answer"], "42")
        self.assertEqual(record["segments"][0]["script"]["title"], "setup")
        self.assertEqual(len(record["segments"][1]["sweeps"]), 2)
        self.assertRegex(record["artifact_digest"], r"^[0-9a-f]{64}$")
        self.assertRegex(record["review_binding_digest"], r"^[0-9a-f]{64}$")
        report = json.loads(self.fixture.report_path.read_text(encoding="utf-8"))
        self.assertEqual(
            record["review_binding_digest"],
            build_site.live_report_binding_digest(report),
        )

    def test_review_binding_ignores_report_timestamp_and_file_bytes(self) -> None:
        before = self.fixture.load()
        report = json.loads(self.fixture.report_path.read_text(encoding="utf-8"))
        report["generated_at"] = "2026-08-01T05:00:00+00:00"
        self.fixture.report_path.write_text(
            json.dumps(report, indent=2) + "\n", encoding="utf-8"
        )
        after = self.fixture.load()

        self.assertNotEqual(before["artifact_digest"], after["artifact_digest"])
        self.assertEqual(
            before["review_binding_digest"], after["review_binding_digest"]
        )

    def test_public_status_feed_contains_counts_but_not_private_notes(self) -> None:
        record = self.fixture.load()
        payload = self.fixture.complete_payload(record)
        payload["notes"] = "private lesson note"
        payload["segments"]["setup"]["notes"] = "private segment note"
        saved = review_site.normalize_review(payload, record)
        review_site.write_review_state(saved, self.fixture.review_root)
        destination = self.root / "qa" / "review-status.json"

        feed = review_site.write_public_status_feed(
            [record], self.fixture.review_root, (destination,)
        )
        serialized = destination.read_text(encoding="utf-8")

        self.assertEqual(feed["lessons"][0]["status"], "review_complete")
        self.assertEqual(feed["lessons"][0]["passed_segments"], 2)
        self.assertNotIn("private lesson note", serialized)
        self.assertNotIn("private segment note", serialized)
        self.assertNotIn("notes", feed["lessons"][0])

    def test_changed_hashed_artifact_is_rejected_and_blocked(self) -> None:
        record = self.fixture.load()
        media_path = self.root / "slides/files/FixtureSlide/setup.mp4"
        media_path.write_bytes(b"changed after QA")

        with self.assertRaisesRegex(review_site.ReviewSiteError, "file hash is stale"):
            self.fixture.load()

        with mock.patch.object(review_site, "STATIC_ROOT", self.fixture.static_root):
            catalog, _ = review_site.build_review_site(
                [self.fixture.lesson],
                site_root=self.fixture.site_root,
                repository_root=self.root,
                live_qa_root=self.fixture.qa_root,
            )
        self.assertEqual(catalog["summary"]["reviewable"], 0)
        self.assertEqual(catalog["summary"]["blocked"], 1)
        self.assertIn("file hash is stale", catalog["blocked"][0]["reason"])
        self.assertNotEqual(record["artifact_digest"], "")

    def test_checked_record_path_enforces_root_and_hash(self) -> None:
        media_relative = "slides/files/FixtureSlide/setup.mp4"
        valid_record = file_record(self.root, media_relative)
        resolved = review_site.checked_record_path(
            valid_record,
            allowed_root=self.root / "slides",
            label="fixture media",
            repository_root=self.root,
        )
        self.assertEqual(resolved, (self.root / media_relative).resolve())

        secret_relative = "private/secret.mp4"
        write_file(self.root, secret_relative, b"secret")
        traversal_record = file_record(self.root, secret_relative)
        traversal_record["path"] = "slides/../private/secret.mp4"
        with self.assertRaisesRegex(review_site.ReviewSiteError, "outside its allowed root"):
            review_site.checked_record_path(
                traversal_record,
                allowed_root=self.root / "slides",
                label="escaped media",
                repository_root=self.root,
            )

        stale_record = dict(valid_record)
        stale_record["sha256"] = "0" * 64
        with self.assertRaisesRegex(review_site.ReviewSiteError, "file hash is stale"):
            review_site.checked_record_path(
                stale_record,
                allowed_root=self.root / "slides",
                label="stale media",
                repository_root=self.root,
            )

    def test_ready_requires_every_segment_criterion_and_lesson_criterion(self) -> None:
        record = self.fixture.load()
        complete = self.fixture.complete_payload(record)
        normalized = review_site.normalize_review(complete, record)
        self.assertTrue(normalized["ready"])
        self.assertNotIn(
            review_site.LOOP_CRITERION,
            normalized["segments"]["setup"]["criteria"],
        )
        self.assertIn(
            review_site.LOOP_CRITERION,
            normalized["segments"]["explore"]["criteria"],
        )

        for beat_id, segment in complete["segments"].items():
            for criterion in segment["criteria"]:
                with self.subTest(beat_id=beat_id, criterion=criterion):
                    incomplete = deepcopy(complete)
                    incomplete["segments"][beat_id]["criteria"][criterion] = False
                    self.assertFalse(
                        review_site.normalize_review(incomplete, record)["ready"]
                    )

        for criterion in complete["lesson_criteria"]:
            with self.subTest(lesson_criterion=criterion):
                incomplete = deepcopy(complete)
                incomplete["lesson_criteria"][criterion] = False
                self.assertFalse(review_site.normalize_review(incomplete, record)["ready"])

        issue = deepcopy(complete)
        issue["segments"]["setup"]["verdict"] = "issue"
        self.assertFalse(review_site.normalize_review(issue, record)["ready"])

        missing = deepcopy(complete)
        missing["segments"]["explore"]["criteria"].pop(review_site.LOOP_CRITERION)
        with self.assertRaisesRegex(review_site.ReviewSiteError, "criteria differ"):
            review_site.normalize_review(missing, record)

    def test_stale_artifact_digest_rejects_save_and_resets_stored_review(self) -> None:
        record = self.fixture.load()
        payload = self.fixture.complete_payload(record)
        saved = review_site.normalize_review(payload, record)
        review_site.write_review_state(saved, self.fixture.review_root)

        changed_record = deepcopy(record)
        changed_record["artifact_digest"] = "f" * 64
        state = review_site.read_review_state(changed_record, self.fixture.review_root)
        self.assertTrue(state["stale"])
        self.assertFalse(state["review"]["ready"])
        self.assertEqual(
            state["review"]["artifact_digest"], changed_record["artifact_digest"]
        )
        self.assertEqual(state["previous_updated_at"], saved["updated_at"])
        self.assertEqual(
            review_site.summarize_review(changed_record, state)["status"], "stale"
        )

        with self.assertRaisesRegex(review_site.ReviewSiteError, "artifact is stale"):
            review_site.normalize_review(payload, changed_record)

    def test_byte_range_parser_handles_open_suffix_clamped_and_invalid_ranges(self) -> None:
        valid = {
            "bytes=0-9": (0, 9),
            "bytes=10-": (10, 99),
            "bytes=-10": (90, 99),
            "bytes=-200": (0, 99),
            "bytes=95-200": (95, 99),
            " bytes=0-0 ": (0, 0),
        }
        for value, expected in valid.items():
            with self.subTest(value=value):
                self.assertEqual(review_site.parse_byte_range(value, 100), expected)

        invalid = (
            "bytes=",
            "bytes=-0",
            "bytes=100-",
            "bytes=20-10",
            "bytes=0-1,4-5",
            "items=0-9",
            "bytes=one-two",
        )
        for value in invalid:
            with self.subTest(value=value):
                self.assertIsNone(review_site.parse_byte_range(value, 100))
        self.assertIsNone(review_site.parse_byte_range("bytes=-1", 0))

    def test_bound_asset_rejects_bytes_changed_after_site_build(self) -> None:
        path = self.root / "slides/files/FixtureSlide/setup.mp4"
        initial = path.stat()
        asset = review_site.BoundAsset(
            path=path,
            sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
            size=initial.st_size,
            mtime_ns=initial.st_mtime_ns,
        )
        self.assertTrue(asset.is_current())

        path.write_bytes(b"other media")
        path.touch()
        self.assertFalse(asset.is_current())

    def test_running_site_rejects_a_source_changed_after_build(self) -> None:
        record = self.fixture.load()
        review_site.require_current_record(record)

        scene_path = self.root / self.fixture.lesson["scene_file"]
        scene_path.write_bytes(b"class FixtureSlide: changed = True\n")
        with self.assertRaisesRegex(review_site.ReviewSiteError, "evidence is stale"):
            review_site.require_current_record(record)


if __name__ == "__main__":
    unittest.main()
