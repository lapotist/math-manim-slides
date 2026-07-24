"""Base class for cataloged Manim Slides lessons."""

from __future__ import annotations

from manim import ManimColor
from manim_slides import Slide

from .theme import BG


class CarloSlide(Slide):
    """Set the stable frame and retain beat IDs during construction."""

    lesson_id = ""

    def setup(self) -> None:
        super().setup()
        self.camera.background_color = ManimColor(BG)
        self.constructed_beat_ids: list[str] = []

    def begin_beat(self, beat_id: str) -> None:
        """Record the first implicit presentation segment."""
        if self.constructed_beat_ids:
            raise ValueError("begin_beat can only record the first beat")
        self.constructed_beat_ids.append(beat_id)

    def next_beat(self, beat_id: str, *, loop: bool = False) -> None:
        """Start the next named segment using Manim Slides semantics."""
        if beat_id in self.constructed_beat_ids:
            raise ValueError(f"duplicate beat id: {beat_id}")
        self.next_slide(loop=loop)
        self.constructed_beat_ids.append(beat_id)
