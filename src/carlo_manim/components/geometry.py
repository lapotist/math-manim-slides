"""Geometry primitives shared by multiple problem-specific arguments."""

from __future__ import annotations

import numpy as np
from manim import VMobject


def filled_shape(
    points: list[np.ndarray],
    color: str,
    opacity: float,
    *,
    z_index: int = -4,
) -> VMobject:
    """Create a filled region from an explicit sampled closed boundary."""
    if len(points) < 3:
        raise ValueError("a filled shape needs at least three points")
    shape = VMobject()
    shape.set_points_as_corners([*points, points[0]])
    shape.set_fill(color, opacity=opacity)
    shape.set_stroke(width=0)
    shape.set_z_index(z_index)
    return shape
