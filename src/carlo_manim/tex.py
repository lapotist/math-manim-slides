"""Pinned MathTex configuration backed by the project Tectonic wrapper."""

from __future__ import annotations

from manim import MathTex, Tex, TexTemplate


TECTONIC_TEX_TEMPLATE = TexTemplate(
    tex_compiler="xelatex",
    output_format=".xdv",
    description="Tectonic XDV through tools/bin/xelatex",
)
TECTONIC_TEX_TEMPLATE.add_to_preamble(r"% carlo-tectonic-toolchain-v2")

MathTex.set_default(tex_template=TECTONIC_TEX_TEMPLATE)
Tex.set_default(tex_template=TECTONIC_TEX_TEMPLATE)
