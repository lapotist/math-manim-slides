"""Checks for batch selection in the slide QA runner."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "qa_slides.py"
    spec = importlib.util.spec_from_file_location("qa_slides", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import qa_slides.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SlideQaSelectionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()
        cls.lessons = {
            "example.q01": {"id": "example.q01", "production_state": "draft_rendered"},
            "example.q02": {"id": "example.q02", "production_state": "published"},
        }

    def test_status_selects_a_deterministic_batch(self) -> None:
        selected = self.module.select_lessons(
            self.lessons,
            [],
            "published,draft_rendered",
        )
        self.assertEqual([lesson["id"] for lesson in selected], ["example.q01", "example.q02"])

    def test_empty_invocation_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "provide lesson IDs"):
            self.module.select_lessons(self.lessons, [], None)

    def test_unknown_lesson_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown lesson"):
            self.module.select_lessons(self.lessons, ["missing.q99"], None)

    def test_sweep_samples_segment_at_fixed_cadence(self) -> None:
        self.assertEqual(
            self.module.sweep_sample_times(1.8, cadence=0.5),
            [0.15, 0.65, 1.15, 1.65],
        )

    def test_short_segment_has_one_sweep_sample(self) -> None:
        self.assertEqual(self.module.sweep_sample_times(0.2), [0.1])

    def test_sweep_rejects_nonpositive_values(self) -> None:
        with self.assertRaisesRegex(ValueError, "duration"):
            self.module.sweep_sample_times(0)
        with self.assertRaisesRegex(ValueError, "cadence"):
            self.module.sweep_sample_times(1, cadence=0)

    def test_missing_commands_reports_every_qa_dependency(self) -> None:
        available = {"ffmpeg", "ffprobe"}
        with patch.object(
            self.module.shutil,
            "which",
            side_effect=lambda command: command if command in available else None,
        ):
            self.assertEqual(self.module.missing_commands(), ["montage"])

    def test_deployment_installs_contact_sheet_dependency(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "deploy-slides.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("ImageMagick", workflow)

    def test_deployment_configures_pages_before_rendering(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "deploy-slides.yml").read_text(
            encoding="utf-8"
        )
        self.assertLess(
            workflow.index("Configure GitHub Pages"),
            workflow.index("Render public lessons"),
        )


if __name__ == "__main__":
    unittest.main()
