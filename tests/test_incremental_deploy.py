"""Checks for guarded incremental GitHub Pages deployment."""

from __future__ import annotations

import io
import json
import shutil
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import build_site, incremental_deploy


BASE_REVISION = "a" * 40
HEAD_REVISION = "b" * 40
SEGMENTS = (
    ("setup", b"reviewed setup video"),
    ("explore", b"reviewed loop video"),
)


def lesson_metadata(
    lesson_id: str = "source.collection.q01",
    state: str = "draft_rendered",
) -> dict:
    return {
        "id": lesson_id,
        "metadata_path": "lessons/collection/q01/lesson.toml",
        "production_state": state,
    }


class IncrementalPlanChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.lessons = {"source.collection.q01": lesson_metadata()}

    def test_site_shell_change_renders_no_lessons(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["scripts/public_site_assets/styles.css"], self.lessons
        )
        self.assertEqual((mode, ids), ("site", []))

    def test_one_lesson_change_selects_only_that_lesson(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["lessons/collection/q01/deck.py"], self.lessons
        )
        self.assertEqual((mode, ids), ("lessons", ["source.collection.q01"]))

    def test_collection_metadata_is_site_only(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["lessons/collection/collection.toml"], self.lessons
        )
        self.assertEqual((mode, ids), ("site", []))

    def test_provenance_change_is_site_only(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["docs/provenance/CARLO_PERMISSION.md"], self.lessons
        )
        self.assertEqual((mode, ids), ("site", []))

    def test_shared_render_input_selects_every_deployable_lesson(self) -> None:
        lessons = {
            **self.lessons,
            "source.collection.q02": {
                **lesson_metadata("source.collection.q02"),
                "metadata_path": "lessons/collection/q02/lesson.toml",
            },
        }
        mode, ids, _ = incremental_deploy.classify_paths(
            ["src/math_manim/layout.py"], lessons
        )
        self.assertEqual(mode, "full")
        self.assertEqual(ids, ["source.collection.q01", "source.collection.q02"])

    @mock.patch.object(incremental_deploy, "is_render_contract_bootstrap")
    @mock.patch.object(incremental_deploy, "changed_paths")
    @mock.patch.object(incremental_deploy, "is_ancestor", return_value=True)
    @mock.patch.object(incremental_deploy, "load_lesson_metadata")
    def test_matching_first_render_contract_is_a_site_migration(
        self,
        load: mock.Mock,
        _ancestor: mock.Mock,
        changed: mock.Mock,
        bootstrap: mock.Mock,
    ) -> None:
        load.return_value = self.lessons
        changed.return_value = ["scripts/render-contract.json"]
        bootstrap.return_value = True
        plan = incremental_deploy.make_plan(
            base_revision=BASE_REVISION,
            base_run_id="123",
            head_revision=HEAD_REVISION,
        )
        self.assertEqual(plan["mode"], "site")
        self.assertEqual(plan["changed_lesson_ids"], [])
        self.assertIn("site:render-contract-bootstrap", plan["reasons"])

    def test_later_render_contract_change_rebuilds_every_lesson(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["scripts/render-contract.json"], self.lessons
        )
        self.assertEqual((mode, ids), ("full", ["source.collection.q01"]))

    def test_non_public_change_is_a_true_noop(self) -> None:
        mode, ids, _ = incremental_deploy.classify_paths(
            ["docs/PUBLISHING.md", "tests/test_math.py"], self.lessons
        )
        self.assertEqual((mode, ids), ("noop", []))

    def test_unknown_path_fails_closed(self) -> None:
        with self.assertRaisesRegex(ValueError, "unclassified"):
            incremental_deploy.classify_paths(["mystery/input.dat"], self.lessons)

    @mock.patch.object(incremental_deploy, "load_lesson_metadata")
    def test_missing_baseline_requires_explicit_full_rebuild(
        self, load: mock.Mock
    ) -> None:
        load.return_value = self.lessons
        with self.assertRaisesRegex(ValueError, "explicitly request"):
            incremental_deploy.make_plan(
                base_revision="",
                base_run_id="",
                head_revision=HEAD_REVISION,
            )
        plan = incremental_deploy.make_plan(
            base_revision="",
            base_run_id="",
            head_revision=HEAD_REVISION,
            force_full_rebuild=True,
        )
        self.assertEqual(plan["mode"], "full")
        self.assertEqual(plan["changed_lesson_ids"], ["source.collection.q01"])


class IncrementalArtifactChecks(unittest.TestCase):
    def test_archive_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "artifact.tar"
            with tarfile.open(archive, "w") as handle:
                info = tarfile.TarInfo("../outside.txt")
                payload = b"outside"
                info.size = len(payload)
                handle.addfile(info, io.BytesIO(payload))
            with self.assertRaisesRegex(ValueError, "unsafe Pages archive path"):
                incremental_deploy.extract_pages_artifact(
                    archive, root / "site"
                )
            self.assertFalse((root / "outside.txt").exists())

    def test_site_only_build_reuses_bound_media_without_render_outputs(self) -> None:
        from tests.test_build_site import sample_lesson, write_export, write_qa

        lesson = sample_lesson()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_site = root / "base-site"
            output_site = root / "output-site"
            write_export(root / "dist", lesson["id"])
            write_qa(root, lesson)
            records, missing = build_site.assemble_site(
                [lesson],
                site_root=base_site,
                export_root=root / "dist",
                qa_root=root / "qa",
                repository_root=root,
                revision=BASE_REVISION,
                repository_url="https://github.example/acme/slides",
                generate_thumbnails=False,
            )
            self.assertEqual(missing, [])
            self.assertEqual(len(records), 1)
            for generated in (root / "dist", root / "slides", root / "qa"):
                shutil.rmtree(generated)
            plan_path = root / "plan.json"
            incremental_deploy.write_plan(
                {
                    "schema_version": incremental_deploy.PLAN_SCHEMA_VERSION,
                    "base_run_id": "123",
                    "base_revision": BASE_REVISION,
                    "head_revision": HEAD_REVISION,
                    "mode": "site",
                    "changed_lesson_ids": [],
                    "selected_lesson_count": 1,
                    "changed_paths": ["scripts/public_site_assets/styles.css"],
                    "reasons": ["site:scripts/public_site_assets/styles.css"],
                },
                plan_path,
            )
            with mock.patch.object(
                build_site, "load_lessons", return_value={lesson["id"]: lesson}
            ):
                reused, fresh = incremental_deploy.assemble_incremental_site(
                    plan_path=plan_path,
                    base_site=base_site,
                    site_root=output_site,
                    revision=HEAD_REVISION,
                    repository_root=root,
                    repository_url="https://github.example/acme/slides",
                )
            manifest = json.loads(
                (output_site / "site-manifest.json").read_text(encoding="utf-8")
            )
            segment = manifest["lessons"][0]["segments"][0]
            reused_segment = (output_site / segment["path"]).read_bytes()

        self.assertEqual((reused, fresh), (1, 0))
        self.assertEqual(manifest["source_revision"], HEAD_REVISION)
        self.assertEqual(manifest["summary"]["deployed"], 1)
        self.assertRegex(
            manifest["lessons"][0]["artifact_fingerprint"], r"^[0-9a-f]{64}$"
        )
        self.assertEqual(reused_segment, SEGMENTS[0][1])

    def test_duplicate_baseline_lesson_ids_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base_site = root / "base-site"
            base_site.mkdir()
            record = {"id": "source.collection.q01"}
            (base_site / "site-manifest.json").write_text(
                json.dumps(
                    {
                        "schema_version": build_site.SITE_SCHEMA_VERSION,
                        "source_revision": BASE_REVISION,
                        "summary": {"missing": 0, "deployed": 2},
                        "lessons": [record, record],
                    }
                ),
                encoding="utf-8",
            )
            plan_path = root / "plan.json"
            incremental_deploy.write_plan(
                {
                    "schema_version": incremental_deploy.PLAN_SCHEMA_VERSION,
                    "base_run_id": "123",
                    "base_revision": BASE_REVISION,
                    "head_revision": HEAD_REVISION,
                    "mode": "site",
                    "changed_lesson_ids": [],
                    "selected_lesson_count": 1,
                    "changed_paths": [],
                    "reasons": [],
                },
                plan_path,
            )
            with self.assertRaisesRegex(ValueError, "inventory is invalid"):
                incremental_deploy.assemble_incremental_site(
                    plan_path=plan_path,
                    base_site=base_site,
                    site_root=root / "output",
                    revision=HEAD_REVISION,
                    repository_root=root,
                )


class IncrementalWorkflowChecks(unittest.TestCase):
    def test_site_only_job_cannot_install_or_render_manim(self) -> None:
        workflow = (
            Path(__file__).resolve().parents[1]
            / ".github"
            / "workflows"
            / "deploy-slides.yml"
        ).read_text(encoding="utf-8")
        site_job = workflow[workflow.index("  site:") : workflow.index("  render:")]
        self.assertIn("mode == 'site'", site_job)
        self.assertIn("incremental_deploy.py assemble", site_job)
        self.assertNotIn("ImageMagick", site_job)
        self.assertNotIn("setup-pixi", site_job)
        self.assertNotIn("pixi run", site_job)
        self.assertNotIn("prepare-tex", site_job)
        self.assertNotIn("execute render", site_job)
        self.assertIn("scripts/site-requirements.txt", site_job)
        self.assertIn("tests.test_build_site.SiteBuilderChecks", site_job)
        self.assertNotIn("\n  cleanup:", workflow)
        self.assertIn("listArtifactsForRepo", workflow)
        self.assertIn("cancel-in-progress: true", workflow)
        self.assertEqual(workflow.count("retention-days: 90"), 2)
        self.assertIn("No public site or lesson output changed", workflow)

    def test_render_fingerprint_contract_matches_workflow_pins(self) -> None:
        root = Path(__file__).resolve().parents[1]
        incremental_deploy.validate_render_workflow_contract(root)
        workflow = (root / ".github" / "workflows" / "deploy-slides.yml").read_text(
            encoding="utf-8"
        )
        for key in ("container", "pixi", "cjk_font", "dvisvgm", "amsfonts"):
            self.assertIn(build_site.RENDER_CONTRACT[key], workflow)
        script = (root / "scripts" / "incremental_deploy.py").read_text(
            encoding="utf-8"
        )
        self.assertIn('RENDER_CONTRACT["quality"]', script)


if __name__ == "__main__":
    unittest.main()
