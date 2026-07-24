"""Small focus helpers that preserve object identity."""

from __future__ import annotations

from manim import AnimationGroup, Mobject


def dim_context(*mobjects: Mobject, opacity: float = 0.25) -> AnimationGroup:
    """Dim inactive context without removing and rebuilding it."""
    return AnimationGroup(
        *(mobject.animate.set_opacity(opacity) for mobject in mobjects),
        lag_ratio=0.0,
    )


def restore_context(*mobjects: Mobject) -> AnimationGroup:
    """Restore context previously dimmed with ``dim_context``."""
    return AnimationGroup(
        *(mobject.animate.set_opacity(1.0) for mobject in mobjects),
        lag_ratio=0.0,
    )
