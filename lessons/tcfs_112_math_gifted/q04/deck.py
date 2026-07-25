"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q4."""

from __future__ import annotations

from fractions import Fraction

import numpy as np

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    PURPLE,
    REGION,
    CarloSlide,
    label,
)
from manim import (
    Arc,
    Brace,
    Circumscribe,
    Create,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ExactPoint = tuple[Fraction, Fraction]


def exact_cross(first: ExactPoint, second: ExactPoint) -> Fraction:
    """Return the exact two-dimensional cross product."""
    return first[0] * second[1] - first[1] * second[0]


def exact_subtract(first: ExactPoint, second: ExactPoint) -> ExactPoint:
    """Subtract exact affine points or vectors."""
    return first[0] - second[0], first[1] - second[1]


def exact_add(first: ExactPoint, second: ExactPoint) -> ExactPoint:
    """Add exact affine points or vectors."""
    return first[0] + second[0], first[1] + second[1]


def exact_scale(value: Fraction, point: ExactPoint) -> ExactPoint:
    """Scale an exact vector."""
    return value * point[0], value * point[1]


def exact_line_parameters(
    first_start: ExactPoint,
    first_end: ExactPoint,
    second_start: ExactPoint,
    second_end: ExactPoint,
) -> tuple[Fraction, Fraction]:
    """Solve two nonparallel exact parametric lines."""
    first_direction = exact_subtract(first_end, first_start)
    second_direction = exact_subtract(second_end, second_start)
    separation = exact_subtract(second_start, first_start)
    denominator = exact_cross(first_direction, second_direction)
    if denominator == 0:
        raise ValueError("exact line intersection is undefined for parallel lines")
    first_parameter = exact_cross(separation, second_direction) / denominator
    second_parameter = exact_cross(separation, first_direction) / denominator
    return first_parameter, second_parameter


def exact_point_on_line(
    start: ExactPoint,
    end: ExactPoint,
    parameter: Fraction,
) -> ExactPoint:
    """Evaluate an exact parametric line."""
    return exact_add(start, exact_scale(parameter, exact_subtract(end, start)))


def exact_configuration(shear: int) -> dict[str, ExactPoint | Fraction]:
    """Build a normalized nondegenerate member of the trapezoid family."""
    a = (Fraction(0), Fraction(0))
    b = (Fraction(3), Fraction(0))
    d = (Fraction(shear), Fraction(1))
    c = (Fraction(shear + 1), Fraction(1))
    e = exact_scale(Fraction(1, 2), exact_add(a, c))
    f_on_ad, f_on_be = exact_line_parameters(a, d, b, e)
    f = exact_point_on_line(a, d, f_on_ad)
    g_on_be, g_on_dc = exact_line_parameters(b, e, d, c)
    g = exact_point_on_line(b, e, g_on_be)
    return {
        "A": a,
        "B": b,
        "C": c,
        "D": d,
        "E": e,
        "F": f,
        "G": g,
        "f_on_ad": f_on_ad,
        "f_on_be": f_on_be,
        "g_on_be": g_on_be,
        "g_on_dc": g_on_dc,
    }


for _shear in (-4, 0, 7):
    _configuration = exact_configuration(_shear)
    if _configuration["f_on_ad"] != Fraction(3, 5):
        raise ValueError("F must divide AD at the exact parameter 3/5")
    if _configuration["f_on_be"] != Fraction(6, 5):
        raise ValueError("F must lie beyond E on the ray from B through E")
    if _configuration["g_on_be"] != Fraction(2):
        raise ValueError("G must be the second affine image of E from B")
    if _configuration["g_on_dc"] != Fraction(-2):
        raise ValueError("G must be two top-base units beyond D")
    if not Fraction(0) < _configuration["f_on_ad"] < Fraction(1):
        raise ValueError("F must lie strictly inside side AD")
    _a = _configuration["A"]
    _c = _configuration["C"]
    _e = _configuration["E"]
    if exact_scale(Fraction(2), _e) != exact_add(_a, _c):
        raise ValueError("E must remain the exact midpoint of AC")

BASE_RATIO = Fraction(3)
TOP_REMAINDER_RATIO = BASE_RATIO - Fraction(1)
SIDE_PART_RATIO = TOP_REMAINDER_RATIO / BASE_RATIO
FINAL_RATIO = Fraction(1) / (Fraction(1) + SIDE_PART_RATIO)

if TOP_REMAINDER_RATIO != 2:
    raise ValueError("the top extension must have two unit parts")
if SIDE_PART_RATIO != Fraction(2, 3):
    raise ValueError("similarity must transfer the ratio DF:AF = 2:3")
if FINAL_RATIO != Fraction(3, 5):
    raise ValueError("the independently reconstructed final ratio is not 3/5")


class CarloTcfs112MathQ04(CarloSlide):
    """Discover an affine side ratio through two visible triangle comparisons."""

    lesson_id = "carlo.tcfs_112_math_gifted.q04"

    @staticmethod
    def title_change(old, new) -> Succession:
        """Replace CJK titles without morphing their glyphs."""
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def line_intersection(
        first_start: np.ndarray,
        first_end: np.ndarray,
        second_start: np.ndarray,
        second_end: np.ndarray,
    ) -> np.ndarray:
        """Intersect two display lines without using the proven ratio."""
        first_direction = first_end - first_start
        second_direction = second_end - second_start
        denominator = (
            first_direction[0] * second_direction[1]
            - first_direction[1] * second_direction[0]
        )
        if abs(denominator) < 1e-9:
            raise ValueError("display lines unexpectedly became parallel")
        separation = second_start - first_start
        numerator = (
            separation[0] * second_direction[1]
            - separation[1] * second_direction[0]
        )
        parameter = numerator / denominator
        return first_start + float(parameter) * first_direction

    @classmethod
    def display_points(cls, d_x: float, height: float) -> dict[str, np.ndarray]:
        """Return one exact-givens display configuration."""
        a = np.array([-5.45, -1.78, 0.0])
        b = np.array([0.35, -1.78, 0.0])
        unit = (b[0] - a[0]) / 3
        d = np.array([d_x, -1.78 + height, 0.0])
        c = d + np.array([unit, 0.0, 0.0])
        e = (a + c) / 2
        f = cls.line_intersection(a, d, b, e)
        g = cls.line_intersection(b, e, d, c)
        return {"A": a, "B": b, "C": c, "D": d, "E": e, "F": f, "G": g}

    @staticmethod
    def midpoint_tick(start: np.ndarray, end: np.ndarray) -> Line:
        """Place one compact equal-length tick at a segment midpoint."""
        direction = end - start
        direction /= np.linalg.norm(direction)
        normal = np.array([-direction[1], direction[0], 0.0])
        midpoint = (start + end) / 2
        return Line(
            midpoint - normal * 0.105,
            midpoint + normal * 0.105,
            color=REGION,
            stroke_width=3.4,
        ).set_z_index(8)

    @staticmethod
    def parallel_chevron(start: np.ndarray, end: np.ndarray) -> VGroup:
        """Mark two segments with the same one-chevron parallel symbol."""
        direction = end - start
        direction /= np.linalg.norm(direction)
        normal = np.array([-direction[1], direction[0], 0.0])
        center = (start + end) / 2
        tip = center + direction * 0.13
        back = center - direction * 0.13
        return VGroup(
            Line(back + normal * 0.10, tip, color=MUTED, stroke_width=3.0),
            Line(back - normal * 0.10, tip, color=MUTED, stroke_width=3.0),
        ).set_z_index(8)

    @staticmethod
    def minor_arc(
        vertex: np.ndarray,
        first: np.ndarray,
        second: np.ndarray,
        color: str,
        *,
        radius: float = 0.31,
    ) -> Arc:
        """Draw the smaller angle between two visible rays."""
        first_angle = float(np.arctan2(first[1] - vertex[1], first[0] - vertex[0]))
        second_angle = float(np.arctan2(second[1] - vertex[1], second[0] - vertex[0]))
        sweep = (second_angle - first_angle) % (2 * np.pi)
        if sweep > np.pi:
            first_angle, second_angle = second_angle, first_angle
            sweep = (second_angle - first_angle) % (2 * np.pi)
        return Arc(
            radius=radius,
            start_angle=first_angle,
            angle=sweep,
            arc_center=vertex,
            color=color,
            stroke_width=5,
        ).set_z_index(10)

    @classmethod
    def diagram(cls, d_x: float, height: float) -> VGroup:
        """Build one trapezoid while preserving all object roles and order."""
        points = cls.display_points(d_x, height)
        a, b, c, d, e, f = (points[name] for name in "ABCDEF")
        fill = Polygon(
            a,
            b,
            c,
            d,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.045,
        ).set_z_index(-3)
        outline = VGroup(
            Line(a, b, color=REGION, stroke_width=5.0),
            Line(b, c, color=INK, stroke_width=3.2),
            Line(c, d, color=BLUE, stroke_width=5.0),
            Line(d, a, color=INK, stroke_width=3.2),
        )
        constructions = VGroup(
            Line(a, c, color=MUTED, stroke_width=2.8),
            Line(b, f, color=PURPLE, stroke_width=4.0),
        )
        dots = VGroup(
            Dot(a, radius=0.072, color=INK),
            Dot(b, radius=0.072, color=INK),
            Dot(c, radius=0.072, color=INK),
            Dot(d, radius=0.072, color=INK),
            Dot(e, radius=0.082, color=REGION),
            Dot(f, radius=0.095, color=POINT),
        ).set_z_index(12)
        names = VGroup(
            MathTex("A", font_size=27, color=INK).next_to(dots[0], DOWN + LEFT, buff=0.09),
            MathTex("B", font_size=27, color=INK).next_to(dots[1], DOWN + RIGHT, buff=0.09),
            MathTex("C", font_size=27, color=INK).next_to(dots[2], UP + RIGHT, buff=0.09),
            MathTex("D", font_size=27, color=INK).next_to(dots[3], UP + LEFT, buff=0.09),
            MathTex("E", font_size=27, color=REGION).next_to(dots[4], DOWN + RIGHT, buff=0.08),
            MathTex("F", font_size=27, color=POINT).next_to(dots[5], UP + LEFT, buff=0.08),
        ).set_z_index(13)
        markings = VGroup(
            cls.midpoint_tick(a, e),
            cls.midpoint_tick(e, c),
            cls.parallel_chevron(a, b),
            cls.parallel_chevron(d, c),
        )
        measures = VGroup(
            MathTex("3u", font_size=30, color=REGION).next_to(outline[0], DOWN, buff=0.22),
            MathTex("u", font_size=30, color=BLUE).next_to(outline[2], UP, buff=0.27),
        )
        return VGroup(fill, outline, constructions, dots, names, markings, measures)

    @staticmethod
    def base_strip() -> VGroup:
        """Show the given three-to-one base relation as concrete unit bars."""
        long_units = VGroup(
            *[
                Rectangle(
                    width=0.90,
                    height=0.34,
                    color=REGION,
                    stroke_width=2.2,
                    fill_color=REGION,
                    fill_opacity=0.16,
                )
                for _ in range(3)
            ]
        ).arrange(RIGHT, buff=0.035)
        short_unit = Rectangle(
            width=0.90,
            height=0.34,
            color=BLUE,
            stroke_width=2.2,
            fill_color=BLUE,
            fill_opacity=0.16,
        )
        long_name = MathTex("AB", font_size=28, color=REGION).next_to(long_units, LEFT, buff=0.23)
        short_name = MathTex("CD", font_size=28, color=BLUE).next_to(short_unit, LEFT, buff=0.23)
        long_row = VGroup(long_name, long_units)
        short_row = VGroup(short_name, short_unit)
        rows = VGroup(long_row, short_row).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        return rows

    @staticmethod
    def model_focus(model: VGroup, line_opacity: float, fill_opacity: float):
        """Dim or restore a diagram without turning its subtle fill opaque."""
        return (
            model[0].animate.set_fill(opacity=fill_opacity),
            *(part.animate.set_opacity(line_opacity) for part in model[1:]),
        )

    @staticmethod
    def five_part_bar() -> tuple[VGroup, VGroup, VGroup, VGroup]:
        """Return a two-plus-three partition without evaluating its fraction."""
        units = VGroup(
            *[
                Rectangle(
                    width=0.82,
                    height=0.58,
                    color=CORAL if index < 2 else POINT,
                    stroke_width=2.6,
                    fill_color=CORAL if index < 2 else POINT,
                    fill_opacity=0.16,
                )
                for index in range(5)
            ]
        ).arrange(RIGHT, buff=0.035)
        first_two = VGroup(*units[:2])
        last_three = VGroup(*units[2:])
        first_brace = Brace(first_two, UP, color=CORAL, buff=0.10)
        last_brace = Brace(last_three, UP, color=POINT, buff=0.10)
        first_label = MathTex("DF=2k", font_size=31, color=CORAL).next_to(first_brace, UP, buff=0.10)
        last_label = MathTex("AF=3k", font_size=31, color=POINT).next_to(last_brace, UP, buff=0.10)
        whole_brace = Brace(units, DOWN, color=INK, buff=0.11)
        whole_label = MathTex("AD", font_size=31, color=INK).next_to(whole_brace, DOWN, buff=0.10)
        endpoint_labels = VGroup(
            MathTex("D", font_size=25, color=CORAL).next_to(units, LEFT, buff=0.14),
            MathTex("F", font_size=25, color=POINT).move_to(
                (units[1].get_right() + units[2].get_left()) / 2 + DOWN * 0.53
            ),
            MathTex("A", font_size=25, color=POINT).next_to(units, RIGHT, buff=0.14),
        )
        upper = VGroup(first_brace, last_brace, first_label, last_label)
        lower = VGroup(whole_brace, whole_label, endpoint_labels)
        return units, upper, lower, VGroup(first_label, last_label)

    def construct(self) -> None:
        final_points = self.display_points(-3.62, 3.48)
        a, b, c, d, e, f, g = (final_points[name] for name in "ABCDEFG")

        heading = label("第 4 題｜梯形裡不變的分點", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 4 頁｜影片 K9kwq9apPR0",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        self.add(heading, source)

        # Beat 01: establish only the given trapezoid and its two constructions.
        self.begin_beat("build_given_trapezoid")
        beat_title = label("先把題目的每一個點放回圖上", 35, INK, "BOLD")
        beat_title.move_to([0, 3.28, 0])
        model = self.diagram(-4.15, 3.05)
        given_title = label("固定條件", 28, MUTED, "BOLD")
        parallel = MathTex(r"AB\parallel CD", font_size=39, color=INK)
        base_ratio = MathTex(r"AB=3CD", font_size=39, color=INK)
        base_ratio.set_color_by_tex("AB", REGION)
        base_ratio.set_color_by_tex("CD", BLUE)
        midpoint = MathTex(r"AE=EC", font_size=39, color=REGION)
        strip = self.base_strip()
        given_panel = VGroup(given_title, parallel, base_ratio, strip, midpoint)
        given_panel.arrange(DOWN, buff=0.30).move_to([4.15, -0.02, 0])

        self.play(FadeIn(beat_title), FadeIn(model[0]), Create(model[1]), run_time=1.0)
        self.play(
            LaggedStart(Create(model[2][0]), Create(model[2][1]), lag_ratio=0.25),
            FadeIn(model[3]), FadeIn(model[4]),
            run_time=1.0,
        )
        self.play(Create(model[5]), FadeIn(model[6]), run_time=0.7)
        self.play(FadeIn(given_title), Write(parallel), Write(base_ratio), run_time=0.75)
        self.play(FadeIn(strip), Write(midpoint), run_time=0.7)
        self.wait(0.30)

        # Beat 02: vary only the trapezoid while F remains the actual intersection.
        self.next_beat("vary_shape_watch_f")
        next_title = label("梯形換個樣子，交點 F 會怎麼移動？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        observation = label("每一次都重新取 AC 中點，再畫直線 BE", 26, MUTED, "MEDIUM")
        observation.move_to([4.10, -2.72, 0])
        self.play(self.title_change(beat_title, next_title), FadeIn(observation), run_time=0.6)
        beat_title = next_title
        for d_x, height in ((-3.05, 3.75), (-4.72, 3.26), (-3.62, 3.48)):
            self.play(Transform(model, self.diagram(d_x, height)), run_time=1.05)
            self.play(Indicate(model[3][5], color=POINT), run_time=0.38)
        self.wait(0.30)

        # Beat 03: ask for the split before introducing any auxiliary point.
        self.next_beat("pause_on_unknown_split")
        next_title = label("F 把整條 AD 分成哪個比例？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        ad_focus = Line(a, d, color=POINT, stroke_width=8.0).set_opacity(0.75)
        f_focus = Dot(f, radius=0.13, color=POINT).set_z_index(15)
        ratio_question = MathTex(r"\frac{AF}{AD}=?", font_size=58, color=POINT)
        ratio_question.move_to([4.15, 0.20, 0])
        prompt = label("先猜一猜；圖形的傾斜會影響答案嗎？", 27, MUTED, "MEDIUM")
        prompt.next_to(ratio_question, DOWN, buff=0.45)
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(given_panel), FadeOut(observation),
            Create(ad_focus), FadeIn(f_focus),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(Write(ratio_question), FadeIn(prompt), run_time=0.65)
        self.wait(0.45)

        # Beat 04: extend the two already-visible lines until they meet at G.
        self.next_beat("extend_lines_to_g")
        next_title = label("把兩條延長線接起來，製造一個新交點", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        top_extension = Line(g, d, color=BLUE, stroke_width=4.0)
        be_extension = Line(g, f, color=PURPLE, stroke_width=4.0)
        dot_g = Dot(g, radius=0.09, color=PURPLE).set_z_index(12)
        name_g = MathTex("G", font_size=28, color=PURPLE).next_to(dot_g, UP, buff=0.10)
        construction_note = VGroup(
            MathTex("G,D,C", font_size=38, color=BLUE),
            MathTex("G,F,E,B", font_size=38, color=PURPLE),
        ).arrange(DOWN, buff=0.35).move_to([4.15, 0.05, 0])
        collinear_note = label("兩排點各自在同一直線上", 25, MUTED, "MEDIUM")
        collinear_note.next_to(construction_note, DOWN, buff=0.42)
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(ratio_question), FadeOut(prompt), FadeOut(ad_focus), FadeOut(f_focus),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(Create(top_extension), Create(be_extension), run_time=0.9)
        self.play(FadeIn(dot_g), FadeIn(name_g), Write(construction_note), FadeIn(collinear_note), run_time=0.7)
        self.wait(0.30)

        # Beat 05: earn GC = AB from midpoint, vertical angles, and parallel bases.
        self.next_beat("earn_equal_long_segment")
        next_title = label("先比對 E 兩側的三角形", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        triangle_gec = Polygon(
            g, e, c, color=BLUE, stroke_width=4.5, fill_color=BLUE, fill_opacity=0.10
        ).set_z_index(5)
        triangle_bea = Polygon(
            b, e, a, color=REGION, stroke_width=4.5, fill_color=REGION, fill_opacity=0.10
        ).set_z_index(5)
        vertical_gec = self.minor_arc(e, g, c, POINT, radius=0.25)
        vertical_bea = self.minor_arc(e, b, a, POINT, radius=0.34)
        parallel_gce = self.minor_arc(c, g, e, BLUE, radius=0.28)
        parallel_bae = self.minor_arc(a, b, e, BLUE, radius=0.38)
        equal_ae = Line(a, e, color=REGION, stroke_width=6.0).set_z_index(7)
        equal_ec = Line(e, c, color=REGION, stroke_width=6.0).set_z_index(7)
        first_angle = MathTex(r"\angle GEC=\angle BEA", font_size=34, color=POINT)
        second_angle = MathTex(r"\angle GCE=\angle BAE", font_size=34, color=BLUE)
        equal_half = MathTex(r"EC=EA", font_size=34, color=REGION)
        congruent = MathTex(r"\triangle GEC\cong\triangle BEA", font_size=40, color=INK)
        equal_long = MathTex(r"GC=BA", font_size=44, color=REGION)
        first_panel = VGroup(first_angle, second_angle, equal_half, congruent, equal_long)
        first_panel.arrange(DOWN, buff=0.30).move_to([4.18, -0.02, 0])
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(construction_note), FadeOut(collinear_note),
            *self.model_focus(model, 0.20, 0.012),
            top_extension.animate.set_opacity(0.25),
            be_extension.animate.set_opacity(0.25),
            FadeIn(triangle_gec), FadeIn(triangle_bea),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(Create(vertical_gec), Create(vertical_bea), Write(first_angle), run_time=0.70)
        self.play(Create(parallel_gce), Create(parallel_bae), Write(second_angle), run_time=0.70)
        self.play(Create(equal_ae), Create(equal_ec), Write(equal_half), run_time=0.65)
        self.play(Write(congruent), run_time=0.65)
        self.play(Write(equal_long), run_time=0.65)
        self.wait(0.30)

        # Beat 06: turn the given three units into the visible two-plus-one split.
        self.next_beat("split_three_units")
        next_title = label("三份長度，扣掉一份，延長段剩兩份", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        gd_segment = Line(g, d, color=CORAL, stroke_width=7.0).set_z_index(8)
        dc_segment = Line(d, c, color=BLUE, stroke_width=7.0).set_z_index(8)
        whole_gc = DoubleArrow(
            g + UP * 0.52,
            c + UP * 0.52,
            buff=0,
            color=REGION,
            stroke_width=2.5,
            tip_length=0.14,
        )
        whole_gc_label = MathTex("3u", font_size=31, color=REGION).next_to(whole_gc, UP, buff=0.08)
        gd_label = MathTex("2u", font_size=29, color=CORAL).move_to((g + d) / 2 + DOWN * 0.30)
        dc_label = MathTex("u", font_size=29, color=BLUE).move_to((d + c) / 2 + DOWN * 0.30)
        gc_equals = MathTex(r"GC=AB=3u", font_size=39, color=REGION)
        cd_unit = MathTex(r"CD=u", font_size=39, color=BLUE)
        subtract = MathTex(r"GD=GC-CD=2u", font_size=39, color=CORAL)
        base_split = MathTex(r"GD:AB=2:3", font_size=43, color=INK)
        length_panel = VGroup(gc_equals, cd_unit, subtract, base_split)
        length_panel.arrange(DOWN, buff=0.37).move_to([4.20, -0.02, 0])
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(triangle_gec), FadeOut(triangle_bea),
            FadeOut(vertical_gec), FadeOut(vertical_bea),
            FadeOut(parallel_gce), FadeOut(parallel_bae),
            FadeOut(equal_ae), FadeOut(equal_ec), FadeOut(first_panel),
            *self.model_focus(model, 1.0, 0.045),
            top_extension.animate.set_opacity(1.0),
            be_extension.animate.set_opacity(1.0),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(Create(whole_gc), FadeIn(whole_gc_label), Write(gc_equals), run_time=0.70)
        self.play(Create(dc_segment), FadeIn(dc_label), Write(cd_unit), run_time=0.60)
        self.play(Create(gd_segment), FadeIn(gd_label), Write(subtract), run_time=0.65)
        self.play(Write(base_split), run_time=0.60)
        self.wait(0.30)

        # Beat 07: use the same two intersecting lines to earn a second similarity.
        self.next_beat("earn_second_similarity")
        next_title = label("再看 F 周圍，第二組三角形有同樣的角", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        triangle_gdf = Polygon(
            g, d, f, color=CORAL, stroke_width=4.5, fill_color=CORAL, fill_opacity=0.11
        ).set_z_index(5)
        triangle_baf = Polygon(
            b, a, f, color=POINT, stroke_width=4.5, fill_color=POINT, fill_opacity=0.09
        ).set_z_index(5)
        vertical_gfd = self.minor_arc(f, g, d, PURPLE, radius=0.29)
        vertical_bfa = self.minor_arc(f, b, a, PURPLE, radius=0.38)
        parallel_gdf = self.minor_arc(d, g, f, BLUE, radius=0.30)
        parallel_baf = self.minor_arc(a, b, f, BLUE, radius=0.40)
        f_angles = MathTex(r"\angle GFD=\angle BFA", font_size=34, color=PURPLE)
        base_angles = MathTex(r"\angle GDF=\angle BAF", font_size=34, color=BLUE)
        similar = MathTex(r"\triangle GDF\sim\triangle BAF", font_size=41, color=INK)
        correspondence = MathTex(
            r"\frac{GD}{AB}=\frac{DF}{AF}", font_size=44, color=INK
        )
        second_panel = VGroup(f_angles, base_angles, similar, correspondence)
        second_panel.arrange(DOWN, buff=0.38).move_to([4.20, -0.10, 0])
        ratio_memory = base_split.copy().scale(0.82).move_to([4.20, 2.55, 0])
        self.play(
            FadeOut(gc_equals), FadeOut(cd_unit), FadeOut(subtract),
            FadeOut(whole_gc), FadeOut(whole_gc_label), FadeOut(gd_label), FadeOut(dc_label),
            run_time=0.42,
        )
        self.play(
            self.title_change(beat_title, next_title),
            Transform(base_split, ratio_memory),
            *self.model_focus(model, 0.18, 0.010),
            top_extension.animate.set_opacity(0.20), be_extension.animate.set_opacity(0.20),
            gd_segment.animate.set_opacity(0.25), dc_segment.animate.set_opacity(0.25),
            FadeIn(triangle_gdf), FadeIn(triangle_baf),
            run_time=0.80,
        )
        beat_title = next_title
        self.play(Create(vertical_gfd), Create(vertical_bfa), Write(f_angles), run_time=0.70)
        self.play(Create(parallel_gdf), Create(parallel_baf), Write(base_angles), run_time=0.70)
        self.play(Write(similar), run_time=0.65)
        self.play(Write(correspondence), run_time=0.65)
        self.wait(0.30)

        # Beat 08: transfer the visible base ratio onto side AD.
        self.next_beat("transfer_two_to_three")
        next_title = label("相似把上方的 2 比 3 搬到側邊", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        df_segment = Line(d, f, color=CORAL, stroke_width=8.0).set_z_index(9)
        af_segment = Line(f, a, color=POINT, stroke_width=8.0).set_z_index(9)
        df_label = MathTex("2k", font_size=31, color=CORAL).next_to(df_segment, LEFT, buff=0.18)
        af_label = MathTex("3k", font_size=31, color=POINT).next_to(af_segment, LEFT, buff=0.18)
        known_ratio = MathTex(r"GD:AB=2:3", font_size=42, color=INK)
        transfer_arrow = MathTex(r"\Downarrow", font_size=38, color=MUTED)
        side_ratio = MathTex(r"DF:AF=2:3", font_size=46, color=INK)
        side_lengths = MathTex(r"DF=2k,\quad AF=3k", font_size=40, color=INK)
        side_lengths.set_color_by_tex("DF", CORAL)
        side_lengths.set_color_by_tex("AF", POINT)
        transfer_panel = VGroup(known_ratio, transfer_arrow, side_ratio, side_lengths)
        transfer_panel.arrange(DOWN, buff=0.30).move_to([4.18, -0.05, 0])
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(triangle_gdf), FadeOut(triangle_baf),
            FadeOut(vertical_gfd), FadeOut(vertical_bfa),
            FadeOut(parallel_gdf), FadeOut(parallel_baf),
            FadeOut(second_panel), FadeOut(base_split),
            FadeOut(gd_segment), FadeOut(dc_segment),
            *self.model_focus(model, 0.42, 0.020),
            top_extension.animate.set_opacity(0.25), be_extension.animate.set_opacity(0.25),
            Create(df_segment), Create(af_segment),
            run_time=0.80,
        )
        beat_title = next_title
        self.play(Write(known_ratio), run_time=0.50)
        self.play(Write(transfer_arrow), Write(side_ratio), run_time=0.65)
        self.play(FadeIn(df_label), FadeIn(af_label), Write(side_lengths), run_time=0.65)
        self.wait(0.30)

        # Beat 09: hold on a two-plus-three bar with no evaluated answer visible.
        self.next_beat("hold_before_fraction")
        next_title = label("分子是三份；分母要數整條 AD", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        units, upper_braces, lower_brace, brace_labels = self.five_part_bar()
        partition = VGroup(units, upper_braces, lower_brace).move_to([3.95, 0.40, 0])
        final_question = MathTex(r"\frac{AF}{AD}=?", font_size=58, color=POINT)
        final_question.move_to([3.95, -2.10, 0])
        pause_note = label("先在心裡完成最後一步", 26, MUTED, "MEDIUM")
        pause_note.next_to(final_question, DOWN, buff=0.28)
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(transfer_panel), FadeOut(df_label), FadeOut(af_label),
            *self.model_focus(model, 0.18, 0.010),
            FadeOut(top_extension), FadeOut(be_extension), FadeOut(dot_g), FadeOut(name_g),
            run_time=0.70,
        )
        beat_title = next_title
        self.play(
            LaggedStart(*[FadeIn(unit) for unit in units], lag_ratio=0.12),
            run_time=0.85,
        )
        self.play(Create(upper_braces[0]), Create(upper_braces[1]), FadeIn(brace_labels), run_time=0.65)
        self.play(Create(lower_brace[0]), FadeIn(VGroup(*lower_brace[1:])), run_time=0.65)
        self.play(Write(final_question), FadeIn(pause_note), run_time=0.55)
        self.wait(0.55)

        # Beat 10: count the whole only after the reflected partition has settled.
        self.next_beat("reveal_three_fifths")
        next_title = label("把五份數完，比例才真正落定", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        whole_length = MathTex(r"AD=2k+3k=5k", font_size=39, color=INK)
        whole_length.move_to([3.95, -1.22, 0])
        fraction_build = MathTex(
            r"\frac{AF}{AD}=\frac{3k}{2k+3k}", font_size=48, color=INK
        )
        final_equals = MathTex(r"=\frac{3}{5}", font_size=58, color=POINT)
        final_row = VGroup(fraction_build, final_equals).arrange(RIGHT, buff=0.35)
        final_row.move_to([3.95, -2.25, 0])
        answer_frame = SurroundingRectangle(
            final_equals, color=POINT, buff=0.18, stroke_width=3.0
        )
        conclusion = label("梯形改變形狀，這個分點比例仍然不變", 25, REGION, "BOLD")
        conclusion.move_to([-2.65, -3.15, 0])
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(final_question), FadeOut(pause_note),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(FadeIn(whole_length), run_time=0.65)
        self.play(Write(fraction_build), run_time=0.80)
        self.play(Write(final_equals), Create(answer_frame), run_time=0.70)
        self.play(
            *self.model_focus(model, 0.60, 0.028),
            Indicate(af_segment, color=POINT),
            FadeIn(conclusion),
            run_time=0.75,
        )
        self.play(Circumscribe(model[3][5], color=POINT), run_time=0.70)
        self.wait(0.40)
