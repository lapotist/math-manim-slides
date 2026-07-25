"""Smoke tests for the neutral shared-package API."""

import unittest

from carlo_manim import CarloSlide
from carlo_manim.components import filled_shape as legacy_filled_shape
from math_manim import BG, MathSlide, label
from math_manim.components import filled_shape


class PublicApiTests(unittest.TestCase):
    def test_math_slide_preserves_the_stable_base_contract(self) -> None:
        self.assertTrue(issubclass(MathSlide, CarloSlide))
        self.assertEqual(MathSlide.lesson_id, "")

    def test_shared_exports_are_available_from_neutral_namespace(self) -> None:
        self.assertEqual(BG, "#101214")
        self.assertTrue(callable(label))
        self.assertIs(filled_shape, legacy_filled_shape)


if __name__ == "__main__":
    unittest.main()
