"""Checks for the shared slide-density policy."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module():
    path = ROOT / "scripts" / "slide_density.py"
    spec = importlib.util.spec_from_file_location("slide_density", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import slide_density.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SlideDensityChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.module = load_module()

    def test_named_beat_api_counts_play_calls(self) -> None:
        source = """
class Example:
    def construct(self):
        self.begin_beat("one")
        self.play(A())
        self.play(B())
        self.next_beat("two")
        self.play(C())
"""
        self.assertEqual(self.module.segment_play_counts(source), [2, 1])

    def test_raw_next_slide_api_counts_implicit_first_segment(self) -> None:
        source = """
class Example:
    def construct(self):
        self.play(A())
        self.next_slide()
        self.play(B())
        self.play(C())
"""
        self.assertEqual(self.module.segment_play_counts(source), [1, 2])

    def test_play_before_named_first_beat_is_rejected(self) -> None:
        source = """
class Example:
    def construct(self):
        self.play(A())
        self.begin_beat("late")
"""
        with self.assertRaisesRegex(ValueError, "before begin_beat"):
            self.module.segment_play_counts(source)

    def test_constant_loops_count_each_animation_phase(self) -> None:
        source = """
class Example:
    def construct(self):
        self.begin_beat("one")
        for value in range(2, 5):
            self.play(Move(value))
        self.next_beat("two")
        for value in (10, 20):
            self.play(Move(value))
"""
        self.assertEqual(self.module.segment_play_counts(source), [3, 2])

    def test_unknown_animation_loop_length_is_rejected(self) -> None:
        source = """
class Example:
    def construct(self):
        self.begin_beat("one")
        for value in dynamic_values:
            self.play(Move(value))
"""
        with self.assertRaisesRegex(ValueError, "cannot determine animation-loop length"):
            self.module.segment_play_counts(source)


if __name__ == "__main__":
    unittest.main()
