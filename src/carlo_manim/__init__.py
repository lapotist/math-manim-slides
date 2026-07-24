"""Shared visual language and infrastructure for Carlo Math lessons."""

from .tex import TECTONIC_TEX_TEMPLATE
from .base import CarloSlide
from .theme import (
    BG,
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    PURPLE,
    REGION,
    REGION_DARK,
    WHITE,
    label,
)

__all__ = [
    "BG",
    "BLUE",
    "CORAL",
    "CarloSlide",
    "HAIRLINE",
    "INK",
    "MUTED",
    "POINT",
    "PURPLE",
    "REGION",
    "REGION_DARK",
    "TECTONIC_TEX_TEMPLATE",
    "WHITE",
    "label",
]
