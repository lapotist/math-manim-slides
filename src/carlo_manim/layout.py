"""Stable anchors for the collection's common two-column compositions."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TwoColumnLayout:
    """Named anchors that avoid scattered coordinate literals."""

    diagram_center: np.ndarray
    explanation_center: np.ndarray
    heading_anchor: np.ndarray
    formula_anchor: np.ndarray


STANDARD_TWO_COLUMN = TwoColumnLayout(
    diagram_center=np.array([-3.75, -0.25, 0.0]),
    explanation_center=np.array([3.3, -0.25, 0.0]),
    heading_anchor=np.array([3.3, 3.7, 0.0]),
    formula_anchor=np.array([3.3, 0.6, 0.0]),
)
