"""Checks for the generated public README catalog views."""

from __future__ import annotations

import importlib.util
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_update_readme_module():
    path = ROOT / "scripts" / "update_readme.py"
    spec = importlib.util.spec_from_file_location("update_readme", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import update_readme.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReadmeCatalogChecks(unittest.TestCase):
    def test_only_access_blockers_are_excluded(self) -> None:
        module = load_update_readme_module()

        self.assertFalse(
            module.include_in_public_lesson_table(
                {"production_state": "blocked", "blocker_category": "access"}
            )
        )
        self.assertTrue(
            module.include_in_public_lesson_table(
                {"production_state": "blocked", "blocker_category": "rights"}
            )
        )
        self.assertTrue(
            module.include_in_public_lesson_table(
                {"production_state": "visual_verified"}
            )
        )

    def test_public_lesson_table_excludes_blocked_access_records(self) -> None:
        module = load_update_readme_module()
        table = module.render_lesson_table()

        for path in sorted(ROOT.glob("lessons/*/collection.toml")):
            with path.open("rb") as handle:
                collection = tomllib.load(handle)
            collection_label = collection["slug"].replace("_", " ").upper()
            for problem in collection["problems"]:
                if problem.get("blocker_category") == "access":
                    row_prefix = f"| {collection_label} · {problem['label']} |"
                    self.assertNotIn(row_prefix, table)
        self.assertNotIn("solution access blocked", table)
        self.assertIn("`discovered`", table)
        self.assertIn("`draft_rendered`", table)

    def test_generated_sections_match_readme(self) -> None:
        module = load_update_readme_module()
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertIn(module.render_summary(), readme)
        self.assertIn(module.render_lesson_table(), readme)


if __name__ == "__main__":
    unittest.main()
