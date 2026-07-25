"""Checks for catalog schema and generated provenance metadata."""

from __future__ import annotations

import importlib.util
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUPPLIED_PDF_SHA256 = (
    "983f12dbd22aaa7d19c914c4e88c42973faa6d09e32ae036edf15961bbeadcc2"
)


def load_toml(path: Path) -> dict:
    with path.open("rb") as handle:
        return tomllib.load(handle)


def load_update_sources_module():
    path = ROOT / "scripts" / "update_sources.py"
    spec = importlib.util.spec_from_file_location("update_sources", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import update_sources.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogMetadataChecks(unittest.TestCase):
    def test_problem_review_fields_cover_every_catalog_record(self) -> None:
        problems = []
        for path in sorted(ROOT.glob("lessons/*/collection.toml")):
            problems.extend(load_toml(path)["problems"])

        self.assertEqual(len(problems), 76)
        expected_review = {
            "blocked": "not_reviewed",
            "discovered": "not_reviewed",
            "planned": "pending",
            "storyboarded": "pending",
            "math_verified": "pending",
            "draft_rendered": "pending",
            "visual_verified": "independently_verified",
            "published": "independently_verified",
        }
        ids = {problem["id"] for problem in problems}
        for problem in problems:
            self.assertEqual(problem["content_type"], "problem_solution")
            self.assertIsInstance(problem["duplicate_of"], str)
            self.assertEqual(problem["rights_review"], "pending_cc0_scope")
            self.assertEqual(
                problem["math_review_state"],
                expected_review[problem["production_state"]],
            )
            if problem["duplicate_of"]:
                self.assertIn(problem["duplicate_of"], ids)
                self.assertNotEqual(problem["duplicate_of"], problem["id"])

    def test_supplied_pdf_checksum_and_q04_locator_are_pinned(self) -> None:
        collection_path = ROOT / "lessons/tcfs_115_math_gifted/collection.toml"
        collection = load_toml(collection_path)
        self.assertEqual(collection["source_asset_sha256"], SUPPLIED_PDF_SHA256)

        lesson_paths = sorted(
            (ROOT / "lessons/tcfs_115_math_gifted").glob("*/lesson.toml")
        )
        self.assertEqual(len(lesson_paths), 14)
        for path in lesson_paths:
            lesson = load_toml(path)
            self.assertEqual(lesson["source_asset_sha256"], SUPPLIED_PDF_SHA256)
        q04 = load_toml(
            ROOT / "lessons/tcfs_115_math_gifted/q04/lesson.toml"
        )
        self.assertEqual(q04["source_locator"], "Part 1, Question 4, PDF page 2")

    def test_generated_source_index_matches_every_lesson(self) -> None:
        module = load_update_sources_module()
        generated, count = module.render_lesson_index(ROOT)
        current = (ROOT / "SOURCES.md").read_text(encoding="utf-8")
        self.assertEqual(module.update_document(current, generated), current)
        lesson_count = len(list(ROOT.glob("lessons/*/*/lesson.toml")))
        self.assertEqual(count, lesson_count)


if __name__ == "__main__":
    unittest.main()
