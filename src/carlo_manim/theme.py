"""Collection-wide frame, typography, and semantic colors."""

from __future__ import annotations

from collections.abc import Mapping

from manim import Text, config


FONT = "Noto Sans CJK TC"
BG = "#101214"
INK = "#F4F1EA"
MUTED = "#AAB2BB"
HAIRLINE = "#343A40"
POINT = "#F4D35E"
REGION = "#4EC5B1"
REGION_DARK = "#197A70"
CORAL = "#FF786A"
BLUE = "#70B7FF"
PURPLE = "#B79CED"
WHITE = "#FFFFFF"


def configure_frame() -> None:
    """Apply the fixed presentation frame before Manim creates a scene."""
    config.pixel_width = 1920
    config.pixel_height = 1080
    config.frame_width = 16
    config.frame_height = 9
    config.frame_rate = 30


def label(
    text: str,
    size: float,
    color: str = INK,
    weight: str = "NORMAL",
    *,
    t2c: Mapping[str, str] | None = None,
) -> Text:
    """Create project-standard Traditional Chinese text."""
    return Text(
        text,
        font=FONT,
        font_size=size,
        color=color,
        weight=weight,
        t2c=dict(t2c or {}),
    )


configure_frame()
