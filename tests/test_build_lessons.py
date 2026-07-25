"""Checks for batch lesson selection and standalone export attribution."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_build_lessons_module():
    path = ROOT / "scripts" / "build_lessons.py"
    spec = importlib.util.spec_from_file_location("build_lessons", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import build_lessons.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExportAttributionChecks(unittest.TestCase):
    def test_standalone_export_gets_license_and_source_slide(self) -> None:
        module = load_build_lessons_module()
        source = (
            "<html><head><title>Manim Slides</title></head><body>\n"
            '<div class="reveal">\n<div class="slides">\n'
            "<section></section>\n</div>\n</div>\n\n\n"
            "<!-- To include plugins --></body></html>\n"
        )
        lesson = {
            "id": "carlo.example.q01",
            "title": "A < B",
            "source_credit": "解題來源：正哥愛數學",
            "source_url": "https://example.test/source?a=1&b=2",
            "source_asset": "supplied-answer.pdf",
            "source_locator": "Question 1, PDF page 2",
            "collection_source_origin": "user_supplied",
            "collection_source_context_url_role": "creator context; PDF absent",
        }
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "lesson.html"
            destination.write_text(source, encoding="utf-8")
            module.add_export_attribution(destination, lesson)
            result = destination.read_text(encoding="utf-8")

        self.assertIn('id="carlo-project-attribution"', result)
        self.assertIn('rel="license"', result)
        self.assertIn("CC BY 4.0", result)
        self.assertIn("Carlo Math Manim Slides contributors", result)
        self.assertIn("A &lt; B", result)
        self.assertIn("a=1&amp;b=2", result)
        self.assertIn("解題來源：正哥愛數學", result)
        self.assertIn("supplied-answer.pdf（使用者提供；未嵌入本檔）", result)
        self.assertIn("Question 1, PDF page 2", result)
        self.assertIn('data-generated-legal-appendix="true"', result)
        self.assertNotIn('data-visibility="uncounted"', result)
        self.assertNotIn('rel="dcterms:source"', result)
        self.assertEqual(result.count("<section"), source.count("<section") + 1)
        self.assertIn("BEGIN CARLO THIRD-PARTY LICENSE NOTICES", result)
        self.assertIn("Copyright (c) 2022-2024 Jérome Eertmans", result)
        self.assertIn("Copyright (C) 2011-2026 Hakim El Hattab", result)

    def test_linked_source_and_solution_are_machine_labeled(self) -> None:
        module = load_build_lessons_module()
        source = (
            "<html><body>\n<div class=\"reveal\">\n<div class=\"slides\">\n"
            "<section></section>\n</div>\n</div>\n\n\n"
            "<!-- To include plugins --></body></html>\n"
        )
        lesson = {
            "id": "carlo.example.q02",
            "title": "Linked source",
            "source_credit": "Solution author",
            "source_url": "https://example.test/collection",
            "source_asset": "answer.pdf",
            "source_asset_url": "https://example.test/answer.pdf?a=1&b=2",
            "source_locator": "Question 2, page 3; video 00:10-00:20",
            "solution_url": "https://example.test/solution?v=2&part=1",
            "collection_source_origin": "frozen_site_inventory",
            "collection_source_context_url_role": "collection page",
        }
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "lesson.html"
            destination.write_text(source, encoding="utf-8")
            module.add_export_attribution(destination, lesson)
            result = destination.read_text(encoding="utf-8")

        self.assertEqual(result.count('rel="dcterms:source"'), 2)
        self.assertIn("answer.pdf?a=1&amp;b=2", result)
        self.assertIn("solution?v=2&amp;part=1", result)
        self.assertIn("Question 2, page 3; video 00:10-00:20", result)
        self.assertNotIn(
            'href="https://example.test/collection" rel="dcterms:source"', result
        )

    def test_export_command_pins_bundled_reveal_version(self) -> None:
        module = load_build_lessons_module()
        command = module.action_command(
            "export",
            {
                "id": "carlo.example.q01",
                "scene_file": "lessons/example/deck.py",
                "scene_class": "ExampleSlide",
            },
            "l",
        )

        self.assertIn("reveal_version=6.0.1", command)

    def test_unknown_export_structure_fails_closed(self) -> None:
        module = load_build_lessons_module()
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory) / "lesson.html"
            destination.write_text("<html></html>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported"):
                module.add_export_attribution(
                    destination,
                    {
                        "id": "carlo.example.q01",
                        "title": "Example",
                        "source_credit": "Source",
                        "source_url": "https://example.test",
                    },
                )


if __name__ == "__main__":
    unittest.main()
