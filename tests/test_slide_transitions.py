"""Checks for stable text entrances and non-overprinting transitions."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "slide_transitions.py"
    spec = importlib.util.spec_from_file_location("slide_transitions", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import slide_transitions.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SlideTransitionChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_write_is_rejected(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n    def construct(self):\n        self.play(Write(text))\n"
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("glyph strokes", issues[0][1])

    def test_concurrent_cross_fade_is_rejected(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        old.move_to(anchor)\n"
            "        new.move_to(anchor)\n"
            "        self.play(FadeOut(old), FadeIn(new))\n"
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("same anchor", issues[0][1])

    def test_succession_cross_fade_is_allowed(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        self.play(Succession(FadeOut(old), FadeIn(new)))\n"
        )
        self.assertEqual(issues, [])

    def test_independent_fade_calls_are_allowed(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        self.play(FadeOut(old))\n"
            "        self.play(FadeIn(new))\n"
        )
        self.assertEqual(issues, [])

    def test_concurrent_fades_at_different_anchors_are_allowed(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        old.move_to(left_anchor)\n"
            "        new.move_to(right_anchor)\n"
            "        self.play(FadeOut(old), FadeIn(new))\n"
        )
        self.assertEqual(issues, [])

    def test_math_text_transform_is_rejected(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        old = MathTex('1')\n"
            "        new = MathTex('2')\n"
            "        self.play(Transform(old, new))\n"
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("glyph content", issues[0][1])

    def test_same_math_text_transform_is_allowed(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        old = MathTex('1')\n"
            "        new = old.copy().scale(0.8)\n"
            "        self.play(Transform(old, new))\n"
        )
        self.assertEqual(issues, [])

    def test_text_inside_helper_group_is_rejected(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def card(self):\n"
            "        caption = label('one')\n"
            "        return VGroup(Square(), caption)\n"
            "    def construct(self):\n"
            "        old = self.card()\n"
            "        new = self.card()\n"
            "        self.play(ReplacementTransform(old, new))\n"
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("text-bearing", issues[0][1])

    def test_transform_matching_tex_is_always_rejected(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        self.play(TransformMatchingTex(old, new))\n"
        )
        self.assertEqual(len(issues), 1)
        self.assertIn("reshapes glyphs", issues[0][1])

    def test_geometry_transform_is_allowed(self) -> None:
        issues = self.module.transition_issues(
            "class Example:\n"
            "    def construct(self):\n"
            "        old = Square()\n"
            "        new = Circle()\n"
            "        self.play(Transform(old, new))\n"
        )
        self.assertEqual(issues, [])


if __name__ == "__main__":
    unittest.main()
