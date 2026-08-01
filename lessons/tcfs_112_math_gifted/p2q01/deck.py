"""Manim Slides lesson for ROC 112 TCFS gifted mathematics proof Q1."""

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
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    RightAngle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ExactPoint = tuple[Fraction, Fraction]


def exact_vector(start: ExactPoint, end: ExactPoint) -> ExactPoint:
    return (end[0] - start[0], end[1] - start[1])


def exact_add(first: ExactPoint, second: ExactPoint) -> ExactPoint:
    return (first[0] + second[0], first[1] + second[1])


def exact_scale(factor: Fraction, vector: ExactPoint) -> ExactPoint:
    return (factor * vector[0], factor * vector[1])


def exact_cross(first: ExactPoint, second: ExactPoint) -> Fraction:
    return first[0] * second[1] - first[1] * second[0]


def twice_area(first: ExactPoint, second: ExactPoint, third: ExactPoint) -> Fraction:
    return abs(
        exact_cross(
            exact_vector(first, second),
            exact_vector(first, third),
        )
    )


def exact_midpoint(first: ExactPoint, second: ExactPoint) -> ExactPoint:
    return ((first[0] + second[0]) / 2, (first[1] + second[1]) / 2)


# Exact checks are independent of the scene coordinates used below.
HERON_S = Fraction(3 + 4 + 5, 2)
if HERON_S * (HERON_S - 3) * (HERON_S - 4) * (HERON_S - 5) != 36:
    raise ValueError("the 3-4-5 Heron radicand must give area 6")
if Fraction(3 * 4, 2) != 6:
    raise ValueError("the 3-4-5 right-triangle area must be 6")

EXACT_A: ExactPoint = (Fraction(0), Fraction(4))
EXACT_B: ExactPoint = (Fraction(-4), Fraction(-2))
EXACT_C: ExactPoint = (Fraction(3), Fraction(-1))
EXACT_G: ExactPoint = (
    (EXACT_A[0] + EXACT_B[0] + EXACT_C[0]) / 3,
    (EXACT_A[1] + EXACT_B[1] + EXACT_C[1]) / 3,
)
EXACT_MA = exact_midpoint(EXACT_B, EXACT_C)
EXACT_MB = exact_midpoint(EXACT_C, EXACT_A)
EXACT_MC = exact_midpoint(EXACT_A, EXACT_B)
ORIGINAL_TWICE_AREA = twice_area(EXACT_A, EXACT_B, EXACT_C)

for wedge in (
    (EXACT_A, EXACT_MC, EXACT_G),
    (EXACT_A, EXACT_G, EXACT_MB),
    (EXACT_B, EXACT_MA, EXACT_G),
    (EXACT_B, EXACT_G, EXACT_MC),
    (EXACT_C, EXACT_MB, EXACT_G),
    (EXACT_C, EXACT_G, EXACT_MA),
):
    if twice_area(*wedge) * 6 != ORIGINAL_TWICE_AREA:
        raise ValueError("the three medians must form six equal-area wedges")

GA = exact_vector(EXACT_G, EXACT_A)
GB = exact_vector(EXACT_G, EXACT_B)
GC = exact_vector(EXACT_G, EXACT_C)
if exact_add(exact_add(GA, GB), GC) != (0, 0):
    raise ValueError("centroid vectors must close head-to-tail")
VECTOR_TRIANGLE_TWICE_AREA = abs(exact_cross(GA, GB))
if 3 * VECTOR_TRIANGLE_TWICE_AREA != ORIGINAL_TWICE_AREA:
    raise ValueError("the centroid-vector triangle must have one-third the area")

MEDIAN_FACTOR = Fraction(3, 2)
MEDIAN_TRIANGLE_TWICE_AREA = abs(
    exact_cross(exact_scale(MEDIAN_FACTOR, GA), exact_scale(MEDIAN_FACTOR, GB))
)
if MEDIAN_TRIANGLE_TWICE_AREA * 4 != ORIGINAL_TWICE_AREA * 3:
    raise ValueError("the median-side triangle must have area factor 3/4")
if Fraction(16) * Fraction(3, 4) != 12 or Fraction(12) * Fraction(3, 4) != 9:
    raise ValueError("two median iterations must carry 16 to 12 to 9")

scaled_a = exact_scale(Fraction(2), EXACT_A)
scaled_b = exact_scale(Fraction(2), EXACT_B)
scaled_c = exact_scale(Fraction(2), EXACT_C)
if twice_area(scaled_a, scaled_b, scaled_c) != 4 * ORIGINAL_TWICE_AREA:
    raise ValueError("doubling all side vectors must quadruple area")

EXACT_K = Fraction(45)
EXACT_H = Fraction(30)
ALTITUDE_SCALE = EXACT_H / EXACT_K
if ALTITUDE_SCALE != Fraction(2, 3):
    raise ValueError("the second-altitude side scale must be 2/3")
for test_side in (Fraction(7, 2), Fraction(9), Fraction(13, 3)):
    first_altitude = 2 * EXACT_K / test_side
    second_altitude = 2 * EXACT_H / first_altitude
    if EXACT_K != test_side * first_altitude / 2:
        raise ValueError("the original paired base-height identity failed")
    if EXACT_H != first_altitude * second_altitude / 2:
        raise ValueError("the height-triangle paired identity failed")
    if second_altitude != ALTITUDE_SCALE * test_side:
        raise ValueError("each second altitude must scale its original side by H/K")
if EXACT_K * ALTITUDE_SCALE * ALTITUDE_SCALE != 20:
    raise ValueError("the second altitude triangle must have area 20")


class CarloTcfs112MathP2Q01(CarloSlide):
    """Connect four area questions through visible length-scale changes."""

    lesson_id = "carlo.tcfs_112_math_gifted.p2q01"

    @staticmethod
    def stage_title(text: str, size: int = 30):
        result = label(text, size, INK, "BOLD")
        result.move_to([0, 3.58, 0])
        return result

    @staticmethod
    def replace_title(scene: "CarloTcfs112MathP2Q01", old, text: str, size: int = 30):
        new = scene.stage_title(text, size)
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.56)
        return new

    @staticmethod
    def edge_label(
        expression: str,
        start: np.ndarray,
        end: np.ndarray,
        offset: np.ndarray,
        color: str,
        size: int = 28,
    ) -> MathTex:
        result = MathTex(expression, font_size=size, color=color)
        result.move_to((start + end) / 2 + offset)
        return result

    @staticmethod
    def triangle_icon(center: np.ndarray, color: str = REGION, scale: float = 1.0):
        points = [
            center + np.array([-0.72, -0.45, 0]) * scale,
            center + np.array([0.72, -0.45, 0]) * scale,
            center + np.array([-0.18, 0.62, 0]) * scale,
        ]
        return Polygon(
            *points,
            color=color,
            stroke_width=2.7,
            fill_color=color,
            fill_opacity=0.10,
        )

    @staticmethod
    def answer_frame(answer, color: str = POINT):
        return SurroundingRectangle(
            answer,
            color=color,
            stroke_width=2.7,
            buff=0.20,
            corner_radius=0.06,
        )

    @staticmethod
    def result_card(heading: str, expression: str, center: np.ndarray, color: str):
        frame = RoundedRectangle(
            width=3.02,
            height=1.82,
            corner_radius=0.08,
            color=HAIRLINE,
            stroke_width=1.6,
            fill_color="#171B1F",
            fill_opacity=0.94,
        ).move_to(center)
        title = label(heading, 23, color, "BOLD").move_to(center + UP * 0.45)
        formula = MathTex(expression, font_size=42, color=INK).move_to(center + DOWN * 0.30)
        return VGroup(frame, title, formula)

    def construct(self) -> None:
        # Beat 01 introduce_area_notation: attach the notation to one concrete region.
        self.begin_beat("introduce_area_notation")
        title = self.stage_title("先讓面積符號回到一個具體三角形")
        p0 = np.array([-5.15, -1.65, 0.0])
        p1 = np.array([-1.15, -1.65, 0.0])
        p2 = np.array([-5.15, 1.35, 0.0])
        fill_345 = Polygon(
            p0,
            p1,
            p2,
            stroke_width=0,
            fill_color=REGION,
            fill_opacity=0.11,
        )
        side_4 = Line(p0, p1, color=POINT, stroke_width=5.0)
        side_3 = Line(p0, p2, color=BLUE, stroke_width=5.0)
        side_5 = Line(p2, p1, color=PURPLE, stroke_width=5.0)
        label_4 = self.edge_label("4", p0, p1, DOWN * 0.27, POINT, 34)
        label_3 = self.edge_label("3", p0, p2, LEFT * 0.28, BLUE, 34)
        label_5 = self.edge_label("5", p2, p1, RIGHT * 0.23 + UP * 0.05, PURPLE, 34)
        tri_345 = VGroup(fill_345, side_4, side_3, side_5, label_4, label_3, label_5)
        notation_title = MathTex(r"T(a,b,c)", font_size=52, color=INK)
        notation_title.move_to([3.25, 1.45, 0])
        notation_text = label("三邊長決定一個三角形", 24, MUTED, "MEDIUM")
        notation_text.move_to([3.25, 0.70, 0])
        area_symbol = MathTex(r"\Delta(a,b,c)", font_size=52, color=REGION)
        area_symbol.move_to([3.25, -0.25, 0])
        area_text = label("記這一塊區域的面積", 24, MUTED, "MEDIUM")
        area_text.move_to([3.25, -0.95, 0])
        question_1 = MathTex(r"\Delta(3,4,5)=?", font_size=49, color=CORAL)
        question_1.move_to([3.25, -2.05, 0])
        notation_group = VGroup(notation_title, notation_text, area_symbol, area_text)
        self.play(FadeIn(title), run_time=0.42)
        self.play(
            FadeIn(fill_345),
            LaggedStart(Create(side_4), Create(side_3), Create(side_5), lag_ratio=0.18),
            run_time=1.05,
        )
        self.play(FadeIn(label_4), FadeIn(label_3), FadeIn(label_5), run_time=0.48)
        self.play(
            LaggedStart(
                FadeIn(notation_title),
                FadeIn(notation_text),
                FadeIn(area_symbol),
                FadeIn(area_text),
                lag_ratio=0.18,
            ),
            run_time=1.25,
        )

        # Beat 02 meet_area_notation: continue at a settled semantic boundary.
        self.next_beat("meet_area_notation")
        self.play(FadeIn(question_1), run_time=0.64)
        self.wait(0.72)

        # Beat 03 derive_three_four_five_area: recognize the right angle, then reveal the first answer.
        self.next_beat("derive_three_four_five_area")
        title = self.replace_title(self, title, "三邊先辨認直角，再量底和高")
        self.play(FadeOut(notation_group), question_1.animate.move_to([3.25, 1.85, 0]), run_time=0.52)
        right_345 = RightAngle(
            Line(p0, p1),
            Line(p0, p2),
            length=0.26,
            color=REGION,
            stroke_width=3.8,
        )
        pythagoras = MathTex(r"3^2+4^2=5^2", font_size=45, color=INK)
        pythagoras.move_to([3.25, 0.80, 0])
        area_setup = MathTex(r"\frac12\cdot4\cdot3", font_size=55, color=INK)
        area_setup.set_color_by_tex("4", POINT)
        area_setup.set_color_by_tex("3", BLUE)
        area_setup.move_to([3.25, -0.35, 0])
        answer_1 = MathTex(r"\Delta(3,4,5)=6", font_size=57, color=CORAL)
        answer_1.move_to([3.25, -1.55, 0])
        answer_1_frame = self.answer_frame(answer_1)
        self.play(FadeIn(pythagoras), Create(right_345), run_time=0.78)
        self.play(Indicate(side_4, color=POINT), Indicate(side_3, color=BLUE), run_time=0.62)
        self.play(FadeIn(area_setup), run_time=0.76)
        self.wait(0.48)

        # Beat 04 earn_three_four_five: continue at a settled semantic boundary.
        self.next_beat("earn_three_four_five")
        self.play(Succession(FadeOut(question_1), FadeIn(answer_1)), run_time=0.66)
        self.play(Create(answer_1_frame), run_time=0.46)
        self.wait(0.72)

        # Beat 05 build_doubled_triangle: double a generic triangle without revealing the area factor.
        self.next_beat("build_doubled_triangle")
        title = self.replace_title(self, title, "三邊都乘 2，底和高各怎麼變？")
        self.play(
            FadeOut(tri_345),
            FadeOut(right_345),
            FadeOut(pythagoras),
            FadeOut(area_setup),
            FadeOut(answer_1),
            FadeOut(answer_1_frame),
            run_time=0.58,
        )
        sb = np.array([-5.50, -1.15, 0.0])
        sc = np.array([-3.00, -1.15, 0.0])
        sa = np.array([-4.90, 0.65, 0.0])
        lb = np.array([0.55, -2.05, 0.0])
        lc = np.array([5.55, -2.05, 0.0])
        la = np.array([1.75, 1.55, 0.0])
        small_tri = Polygon(sb, sc, sa, color=BLUE, stroke_width=3.0, fill_color=BLUE, fill_opacity=0.08)
        large_tri = Polygon(lb, lc, la, color=PURPLE, stroke_width=3.0, fill_color=PURPLE, fill_opacity=0.08)
        small_foot = np.array([sa[0], sb[1], 0.0])
        large_foot = np.array([la[0], lb[1], 0.0])
        small_height = DashedLine(sa, small_foot, color=REGION, stroke_width=3.0)
        large_height = DashedLine(la, large_foot, color=REGION, stroke_width=3.0)
        small_labels = VGroup(
            self.edge_label("b", sb, sc, DOWN * 0.25, POINT),
            self.edge_label("a", sc, sa, RIGHT * 0.22, BLUE),
            self.edge_label("c", sa, sb, LEFT * 0.20, PURPLE),
            MathTex("h", font_size=28, color=REGION).move_to(small_foot + LEFT * 0.22 + UP * 0.55),
        )
        large_labels = VGroup(
            self.edge_label("2b", lb, lc, DOWN * 0.25, POINT),
            self.edge_label("2a", lc, la, RIGHT * 0.22, BLUE),
            self.edge_label("2c", la, lb, LEFT * 0.20, PURPLE),
            MathTex("2h", font_size=28, color=REGION).move_to(large_foot + LEFT * 0.30 + UP * 0.75),
        )
        scale_arrow = MathTex(r"\times2", font_size=46, color=POINT).move_to([-1.25, 0.10, 0])
        k_question = MathTex(r"\Delta(2a,2b,2c)=k\Delta(a,b,c),\quad k=?", font_size=42, color=CORAL)
        k_question.move_to([0, -2.78, 0])
        scale_stage = VGroup(small_tri, large_tri, small_height, large_height, small_labels, large_labels, scale_arrow)
        self.play(FadeIn(small_tri), Create(small_height), FadeIn(small_labels), run_time=0.72)
        self.play(TransformFromCopy(small_tri, large_tri), FadeIn(scale_arrow), run_time=0.95)
        self.play(Create(large_height), FadeIn(large_labels), run_time=0.68)

        # Beat 06 double_one_triangle: continue at a settled semantic boundary.
        self.next_beat("double_one_triangle")
        self.play(Indicate(small_labels[0], color=POINT), Indicate(large_labels[0], color=POINT), run_time=0.56)
        self.play(Indicate(small_height, color=REGION), Indicate(large_height, color=REGION), run_time=0.56)
        self.play(FadeIn(k_question), run_time=0.68)
        self.wait(0.72)

        # Beat 07 earn_scale_factor: earn the factor from the two independent dimensions.
        self.next_beat("earn_scale_factor")
        title = self.replace_title(self, title, "底收到一個 2，高又收到一個 2")
        self.play(scale_stage.animate.set_opacity(0.20), FadeOut(k_question), run_time=0.52)
        doubled_area = MathTex(
            r"\frac12(2b)(2h)=4\left(\frac12bh\right)",
            font_size=54,
            color=INK,
        )
        doubled_area.set_color_by_tex("2b", POINT)
        doubled_area.set_color_by_tex("2h", REGION)
        doubled_area.move_to([0, 0.75, 0])
        two_factors = MathTex(r"2\times2=4", font_size=61, color=REGION)
        two_factors.move_to([0, -0.48, 0])
        answer_2 = MathTex(r"k=4", font_size=68, color=CORAL).move_to([0, -1.75, 0])
        answer_2_frame = self.answer_frame(answer_2)
        self.play(FadeIn(doubled_area), run_time=0.86)
        self.play(FadeIn(two_factors), run_time=0.62)
        self.wait(0.45)
        self.play(FadeIn(answer_2), Create(answer_2_frame), run_time=0.72)
        self.wait(0.70)

        # Beat 08 introduce_medians: construct all three medians on one asymmetric triangle.
        self.next_beat("introduce_medians")
        title = self.replace_title(self, title, "三條中線，要變成下一個三角形的邊")
        self.play(
            FadeOut(scale_stage),
            FadeOut(doubled_area),
            FadeOut(two_factors),
            FadeOut(answer_2),
            FadeOut(answer_2_frame),
            run_time=0.55,
        )
        a = np.array([-3.50, 2.15, 0.0])
        b = np.array([-5.50, -1.80, 0.0])
        c = np.array([-0.70, -1.20, 0.0])
        ma = (b + c) / 2
        mb = (c + a) / 2
        mc = (a + b) / 2
        g = (a + b + c) / 3
        main_triangle = Polygon(a, b, c, color=INK, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.025)
        vertices = VGroup(
            MathTex("A", font_size=28, color=INK).next_to(a, UP, buff=0.10),
            MathTex("B", font_size=28, color=INK).next_to(b, LEFT + DOWN, buff=0.08),
            MathTex("C", font_size=28, color=INK).next_to(c, RIGHT + DOWN, buff=0.08),
        )
        midpoint_dots = VGroup(
            Dot(ma, radius=0.055, color=MUTED),
            Dot(mb, radius=0.055, color=MUTED),
            Dot(mc, radius=0.055, color=MUTED),
        )
        median_a = Line(a, ma, color=BLUE, stroke_width=4.0)
        median_b = Line(b, mb, color=POINT, stroke_width=4.0)
        median_c = Line(c, mc, color=PURPLE, stroke_width=4.0)
        medians = VGroup(median_a, median_b, median_c)
        median_definition = VGroup(
            MathTex(r"l_a=|AM_a|", font_size=39, color=BLUE),
            MathTex(r"l_b=|BM_b|", font_size=39, color=POINT),
            MathTex(r"l_c=|CM_c|", font_size=39, color=PURPLE),
        ).arrange(DOWN, buff=0.45)
        median_definition.move_to([3.35, 0.20, 0])
        definition_note = label("頂點連到對邊中點", 24, MUTED, "MEDIUM")
        definition_note.move_to([3.35, 2.10, 0])
        median_stage = VGroup(main_triangle, vertices, midpoint_dots, medians)
        self.play(Create(main_triangle), FadeIn(vertices), run_time=0.68)
        self.play(FadeIn(midpoint_dots), FadeIn(definition_note), run_time=0.48)
        self.play(
            LaggedStart(
                Create(median_a),
                FadeIn(median_definition[0]),
                Create(median_b),
                FadeIn(median_definition[1]),
                Create(median_c),
                FadeIn(median_definition[2]),
                lag_ratio=0.16,
            ),
            run_time=1.48,
        )
        self.wait(0.62)

        # Beat 09 derive_one_third_centroid_area: prove one pair first, then cycle the argument around the triangle.
        self.next_beat("derive_one_third_centroid_area")
        title = self.replace_title(self, title, "先證明一組，再循環得到六塊相等")
        self.play(FadeOut(median_definition), FadeOut(definition_note), run_time=0.44)
        g_dot = Dot(g, radius=0.075, color=POINT, z_index=6)
        g_name = MathTex("G", font_size=29, color=POINT).move_to(g + np.array([0.20, -0.20, 0]))
        mc_name = MathTex("M_c", font_size=25, color=MUTED).next_to(mc, LEFT, buff=0.10)
        ab_vector = b - a
        foot_c = a + np.dot(c - a, ab_vector) / np.dot(ab_vector, ab_vector) * ab_vector
        foot_g = a + np.dot(g - a, ab_vector) / np.dot(ab_vector, ab_vector) * ab_vector
        height_c_to_ab = DashedLine(c, foot_c, color=MUTED, stroke_width=2.6)
        height_g_to_ab = DashedLine(g, foot_g, color=REGION, stroke_width=3.4)
        centroid_guides = VGroup(mc_name, height_c_to_ab, height_g_to_ab)
        wedge_vertices = (
            (a, mc, g),
            (a, g, mb),
            (b, ma, g),
            (b, g, mc),
            (c, mb, g),
            (c, g, ma),
        )
        wedge_colors = (BLUE, REGION, POINT, PURPLE, BLUE, REGION)
        wedges = VGroup(
            *(
                Polygon(
                    *points,
                    color=color,
                    stroke_width=1.2,
                    fill_color=color,
                    fill_opacity=0.20,
                )
                for points, color in zip(wedge_vertices, wedge_colors, strict=True)
            )
        )
        wedge_labels = VGroup(
            *(
                MathTex(r"\frac K6", font_size=20, color=INK).move_to(
                    (points[0] + points[1] + points[2]) / 3
                )
                for points in wedge_vertices
            )
        )
        wedge_summary = VGroup(
            MathTex(r"K=\Delta(A,B,C)", font_size=36, color=INK),
            MathTex(r"CG:GM_c=2:1", font_size=36, color=POINT),
            MathTex(r"\frac{d(G,AB)}{d(C,AB)}=\frac13", font_size=37, color=REGION),
            MathTex(r"\Delta(A,G,B)=\frac K3", font_size=40, color=POINT),
            MathTex(r"\frac K3\div2=\frac K6", font_size=40, color=REGION),
            MathTex(r"6\times\frac K6=K", font_size=40, color=REGION),
        ).arrange(DOWN, buff=0.25)
        wedge_summary.move_to([3.35, 0.02, 0])
        self.play(FadeIn(g_dot), FadeIn(g_name), FadeIn(mc_name), FadeIn(wedge_summary[0]), run_time=0.55)
        self.play(
            Create(height_c_to_ab),
            Create(height_g_to_ab),
            FadeIn(wedge_summary[1]),
            FadeIn(wedge_summary[2]),
            run_time=0.88,
        )
        agb_region = Polygon(a, g, b, color=POINT, stroke_width=3.0, fill_color=POINT, fill_opacity=0.10)
        self.play(FadeIn(agb_region), FadeIn(wedge_summary[3]), run_time=0.66)

        # Beat 10 split_six_equal_wedges: continue at a settled semantic boundary.
        self.next_beat("split_six_equal_wedges")
        self.play(
            FadeIn(wedges[0]),
            FadeIn(wedges[3]),
            FadeIn(wedge_labels[0]),
            FadeIn(wedge_labels[3]),
            FadeIn(wedge_summary[4]),
            run_time=0.82,
        )
        remaining_wedges = (wedges[1], wedges[2], wedges[4], wedges[5])
        remaining_labels = (wedge_labels[1], wedge_labels[2], wedge_labels[4], wedge_labels[5])
        self.play(
            LaggedStart(*(FadeIn(wedge) for wedge in remaining_wedges), lag_ratio=0.12),
            LaggedStart(*(FadeIn(item) for item in remaining_labels), lag_ratio=0.10),
            FadeIn(wedge_summary[5]),
            run_time=1.00,
        )
        self.wait(0.62)

        # Beat 11 start_centroid_vector_chain: translate the three centroid vectors head-to-tail.
        self.next_beat("start_centroid_vector_chain")
        title = self.replace_title(self, title, "從重心出發的三支箭頭，平移後剛好閉合")
        self.play(
            FadeOut(wedge_summary),
            FadeOut(wedge_labels),
            FadeOut(centroid_guides),
            wedges.animate.set_opacity(0.10),
            medians.animate.set_opacity(0.22),
            run_time=0.50,
        )
        source_ga = Arrow(g, a, buff=0, color=BLUE, stroke_width=5.0, tip_length=0.18)
        source_gb = Arrow(g, b, buff=0, color=POINT, stroke_width=5.0, tip_length=0.18)
        source_gc = Arrow(g, c, buff=0, color=PURPLE, stroke_width=5.0, tip_length=0.18)
        source_vectors = VGroup(source_ga, source_gb, source_gc)
        q0 = np.array([3.10, -1.25, 0.0])
        q1 = q0 + (a - g)
        q2 = q1 + (b - g)
        q3 = q2 + (c - g)
        target_ga = Arrow(q0, q1, buff=0, color=BLUE, stroke_width=5.0, tip_length=0.18)
        target_gb = Arrow(q1, q2, buff=0, color=POINT, stroke_width=5.0, tip_length=0.18)
        target_gc = Arrow(q2, q3, buff=0, color=PURPLE, stroke_width=5.0, tip_length=0.18)
        target_vectors = VGroup(target_ga, target_gb, target_gc)
        closure_formula = MathTex(r"\overrightarrow{GA}+\overrightarrow{GB}+\overrightarrow{GC}=0", font_size=40, color=INK)
        closure_formula.move_to([3.18, 2.55, 0])
        vector_area = VGroup(
            label("閉合面積", 22, MUTED, "MEDIUM"),
            MathTex(r"=\frac K3", font_size=39, color=REGION),
        ).arrange(RIGHT, buff=0.16)
        vector_area.move_to([3.10, -2.45, 0])
        vector_triangle = Polygon(q0, q1, q2, color=REGION, stroke_width=2.0, fill_color=REGION, fill_opacity=0.10)
        ga_vector = a - g
        source_height_foot = g + np.dot(b - g, ga_vector) / np.dot(ga_vector, ga_vector) * ga_vector
        target_height_foot = q0 + np.dot(q2 - q0, ga_vector) / np.dot(ga_vector, ga_vector) * ga_vector
        source_perpendicular = DashedLine(b, source_height_foot, color=REGION, stroke_width=2.8)
        target_perpendicular = DashedLine(q2, target_height_foot, color=REGION, stroke_width=2.8)
        if not np.isclose(source_perpendicular.get_length(), target_perpendicular.get_length()):
            raise ValueError("translation must preserve the perpendicular component of GB")
        source_height_label = MathTex(r"h_\perp", font_size=25, color=REGION).next_to(
            source_perpendicular, DOWN, buff=0.08
        )
        target_height_label = MathTex(r"h_\perp", font_size=25, color=REGION).next_to(
            target_perpendicular, RIGHT, buff=0.08
        )
        vector_area_guides = VGroup(
            source_perpendicular,
            target_perpendicular,
            source_height_label,
            target_height_label,
        )
        self.play(LaggedStart(*(GrowArrow(item) for item in source_vectors), lag_ratio=0.16), run_time=0.86)
        self.play(FadeIn(closure_formula), run_time=0.58)
        self.play(TransformFromCopy(source_ga, target_ga), run_time=0.72)

        # Beat 12 translate_centroid_vectors: continue at a settled semantic boundary.
        self.next_beat("translate_centroid_vectors")
        self.play(TransformFromCopy(source_gb, target_gb), run_time=0.72)
        self.play(TransformFromCopy(source_gc, target_gc), run_time=0.72)
        self.play(
            FadeIn(vector_triangle),
            Create(source_perpendicular),
            Create(target_perpendicular),
            FadeIn(source_height_label),
            FadeIn(target_height_label),
            FadeIn(vector_area),
            run_time=0.76,
        )
        self.wait(0.65)

        # Beat 13 scale_centroid_triangle_to_medians: enlarge the vector triangle to the three full medians.
        self.next_beat("scale_centroid_triangle_to_medians")
        title = self.replace_title(self, title, "中線是重心箭頭的 3/2 倍")
        centroid_ratio = VGroup(
            MathTex(r"l_a=\frac32GA", font_size=37, color=BLUE),
            MathTex(r"l_b=\frac32GB", font_size=37, color=POINT),
            MathTex(r"l_c=\frac32GC", font_size=37, color=PURPLE),
        ).arrange(DOWN, buff=0.24)
        centroid_ratio.move_to([-3.65, 0.82, 0])
        ratio_note = label("重心分中線為 2:1", 24, MUTED, "MEDIUM")
        ratio_note.move_to([-3.65, 2.20, 0])
        self.play(
            FadeOut(wedges),
            FadeOut(source_vectors),
            FadeOut(median_stage),
            FadeOut(agb_region),
            FadeOut(vector_area_guides),
            FadeOut(g_dot),
            FadeOut(g_name),
            FadeOut(closure_formula),
            FadeOut(vector_area),
            run_time=0.55,
        )
        self.play(
            FadeIn(ratio_note),
            LaggedStart(*(FadeIn(item) for item in centroid_ratio), lag_ratio=0.16),
            run_time=0.78,
        )
        median_triangle = vector_triangle.copy().scale(1.5).set_color(REGION)
        median_triangle.set_fill(REGION, opacity=0.16)
        median_edge_labels = VGroup(
            self.edge_label("l_a", median_triangle.get_vertices()[0], median_triangle.get_vertices()[1], RIGHT * 0.18, BLUE),
            self.edge_label("l_b", median_triangle.get_vertices()[1], median_triangle.get_vertices()[2], DOWN * 0.20, POINT),
            self.edge_label("l_c", median_triangle.get_vertices()[2], median_triangle.get_vertices()[0], LEFT * 0.18, PURPLE),
        )
        self.play(
            FadeOut(target_vectors),
            ReplacementTransform(vector_triangle, median_triangle),
            run_time=0.92,
        )
        self.play(FadeIn(median_edge_labels), run_time=0.45)

        # Beat 14 earn_median_area_factor: continue at a settled semantic boundary.
        self.next_beat("earn_median_area_factor")
        median_area_formula = MathTex(
            r"\frac K3\left(\frac32\right)^2=\frac34K",
            font_size=51,
            color=INK,
        )
        median_area_formula.set_color_by_tex(r"\frac34K", REGION)
        median_area_formula.move_to([-3.25, -1.35, 0])
        median_rule = MathTex(r"K\longmapsto\frac34K", font_size=54, color=CORAL)
        median_rule.move_to([-3.25, -2.35, 0])
        self.play(FadeIn(median_area_formula), run_time=0.82)
        self.play(FadeIn(median_rule), Indicate(median_triangle, color=REGION), run_time=0.72)
        self.wait(0.68)

        # Beat 15 set_up_first_median_step: apply the median factor once to area 16.
        self.next_beat("set_up_first_median_step")
        title = self.replace_title(self, title, "先做第一次：16 的四分之三")
        self.play(
            FadeOut(ratio_note),
            FadeOut(centroid_ratio),
            FadeOut(median_triangle),
            FadeOut(median_edge_labels),
            FadeOut(median_area_formula),
            FadeOut(median_rule),
            run_time=0.52,
        )
        flow_y = 0.25
        icon_0 = self.triangle_icon(np.array([-4.25, flow_y, 0]), BLUE, 1.12)
        icon_1 = self.triangle_icon(np.array([0.00, flow_y, 0]), REGION, 1.12)
        label_0 = MathTex(r"T(a,b,c)", font_size=34, color=BLUE).move_to([-4.25, -1.02, 0])
        label_1 = MathTex(r"T(l_a,l_b,l_c)", font_size=34, color=REGION).move_to([0.00, -1.02, 0])
        area_0 = MathTex("16", font_size=58, color=INK).move_to([-4.25, 0.28, 0])
        area_1_question = MathTex("?", font_size=58, color=CORAL).move_to([0.00, 0.28, 0])
        arrow_1 = Arrow([-3.00, flow_y, 0], [-1.25, flow_y, 0], buff=0.12, color=POINT, stroke_width=4.0)
        factor_1 = MathTex(r"\times\frac34", font_size=39, color=POINT).move_to([-2.12, 0.78, 0])
        first_calculation = MathTex(r"16\times\frac34=12", font_size=51, color=INK).move_to([-2.12, -2.15, 0])
        flow_stage = VGroup(icon_0, icon_1, label_0, label_1, area_0, arrow_1, factor_1)
        self.play(FadeIn(icon_0), FadeIn(label_0), FadeIn(area_0), run_time=0.58)
        self.play(GrowArrow(arrow_1), FadeIn(factor_1), run_time=0.58)
        self.play(FadeIn(icon_1), FadeIn(label_1), FadeIn(area_1_question), run_time=0.58)

        # Beat 16 apply_first_median_step: continue at a settled semantic boundary.
        self.next_beat("apply_first_median_step")
        self.play(FadeIn(first_calculation), run_time=0.74)
        area_1 = MathTex("12", font_size=58, color=REGION).move_to(area_1_question)
        self.play(
            Succession(FadeOut(area_1_question), FadeIn(area_1)),
            run_time=0.52,
        )
        self.play(Indicate(area_1, color=REGION), run_time=0.50)
        self.wait(0.62)

        # Beat 17 hold_second_median_step: hold the second application behind a question, then reveal 9.
        self.next_beat("hold_second_median_step")
        title = self.replace_title(self, title, "同一個四分之三，再用一次")
        self.play(
            flow_stage.animate.shift(LEFT * 0.30),
            area_1.animate.shift(LEFT * 0.30),
            first_calculation.animate.set_opacity(0.35),
            run_time=0.45,
        )
        icon_2 = self.triangle_icon(np.array([4.05, flow_y, 0]), PURPLE, 1.12)
        label_2 = MathTex(r"T(l'_a,l'_b,l'_c)", font_size=32, color=PURPLE).move_to([4.05, -1.02, 0])
        arrow_2 = Arrow([1.10, flow_y, 0], [2.80, flow_y, 0], buff=0.12, color=POINT, stroke_width=4.0)
        factor_2 = MathTex(r"\times\frac34", font_size=39, color=POINT).move_to([1.95, 0.78, 0])
        area_2_question = MathTex("?", font_size=61, color=CORAL).move_to([4.05, 0.28, 0])
        second_calculation = MathTex(r"12\times\frac34", font_size=50, color=INK).move_to([2.05, -2.15, 0])
        self.play(GrowArrow(arrow_2), FadeIn(factor_2), run_time=0.58)
        self.play(FadeIn(icon_2), FadeIn(label_2), FadeIn(area_2_question), run_time=0.58)
        self.play(FadeIn(second_calculation), run_time=0.62)
        self.wait(1.05)

        # Beat 18 reveal_second_median_step: continue at a settled semantic boundary.
        self.next_beat("reveal_second_median_step")
        area_2 = MathTex("9", font_size=64, color=CORAL).move_to(area_2_question)
        answer_3 = MathTex(r"12\times\frac34=9", font_size=54, color=CORAL).move_to([2.05, -2.15, 0])
        self.play(
            Succession(FadeOut(area_2_question), FadeIn(area_2)),
            Succession(FadeOut(second_calculation), FadeIn(answer_3)),
            run_time=0.76,
        )
        answer_3_frame = self.answer_frame(answer_3)
        self.play(Create(answer_3_frame), Indicate(icon_2, color=PURPLE), run_time=0.56)
        self.wait(0.68)

        # Beat 19 construct_side_altitude_pair: introduce one side-altitude pair in the original triangle.
        self.next_beat("construct_side_altitude_pair")
        title = self.replace_title(self, title, "先配對一條邊 a，與它對應的高 h_a")
        self.play(
            FadeOut(flow_stage),
            FadeOut(area_1),
            FadeOut(first_calculation),
            FadeOut(icon_2),
            FadeOut(label_2),
            FadeOut(arrow_2),
            FadeOut(factor_2),
            FadeOut(area_2),
            FadeOut(answer_3),
            FadeOut(answer_3_frame),
            run_time=0.58,
        )
        oa = np.array([-2.90, 2.05, 0.0])
        ob = np.array([-5.45, -1.65, 0.0])
        oc = np.array([-0.65, -1.65, 0.0])
        ofoot = np.array([oa[0], ob[1], 0.0])
        original_alt_triangle = Polygon(oa, ob, oc, color=INK, stroke_width=3.2, fill_color=BLUE, fill_opacity=0.035)
        base_a = Line(ob, oc, color=POINT, stroke_width=5.0)
        altitude_a = DashedLine(oa, ofoot, color=REGION, stroke_width=4.0)
        base_a_name = self.edge_label("a", ob, oc, DOWN * 0.28, POINT, 34)
        altitude_a_name = MathTex(r"h_a", font_size=34, color=REGION).move_to(ofoot + LEFT * 0.28 + UP * 0.78)
        side_b_name = self.edge_label("b", oc, oa, RIGHT * 0.24, BLUE, 30)
        side_c_name = self.edge_label("c", oa, ob, LEFT * 0.23, PURPLE, 30)
        right_mark_a = RightAngle(Line(ofoot, oc), Line(ofoot, oa), length=0.24, color=REGION, stroke_width=3.2)
        original_labels = VGroup(base_a_name, altitude_a_name, side_b_name, side_c_name)
        k_formula = MathTex(r"K=\frac12a h_a", font_size=58, color=INK).move_to([3.20, 0.55, 0])
        k_formula.set_color_by_tex("a", POINT)
        k_formula.set_color_by_tex("h_a", REGION)
        cyclic_formula = MathTex(r"a h_a=b h_b=c h_c=2K", font_size=39, color=MUTED).move_to([3.20, -0.70, 0])
        altitude_stage = VGroup(original_alt_triangle, base_a, altitude_a, original_labels, right_mark_a)
        self.play(Create(original_alt_triangle), run_time=0.55)
        self.play(Create(base_a), FadeIn(base_a_name), run_time=0.48)
        self.play(Create(altitude_a), FadeIn(altitude_a_name), Create(right_mark_a), run_time=0.65)

        # Beat 20 introduce_altitude_triangle: continue at a settled semantic boundary.
        self.next_beat("introduce_altitude_triangle")
        self.play(FadeIn(side_b_name), FadeIn(side_c_name), run_time=0.36)
        self.play(FadeIn(k_formula), run_time=0.72)
        self.play(FadeIn(cyclic_formula), run_time=0.62)
        self.wait(0.65)

        # Beat 21 construct_second_altitude: place the altitude-side triangle beside the original one.
        self.next_beat("construct_second_altitude")
        title = self.replace_title(self, title, "同一條 h_a，現在成為右邊三角形的底")
        self.play(FadeOut(k_formula), FadeOut(cyclic_formula), altitude_stage.animate.set_opacity(0.44), run_time=0.48)
        ha_b = np.array([1.30, -1.60, 0.0])
        ha_c = np.array([5.00, -1.60, 0.0])
        ha_a = np.array([2.35, 1.65, 0.0])
        ha_foot = np.array([ha_a[0], ha_b[1], 0.0])
        if not np.isclose(np.linalg.norm(ha_c - ha_b), np.linalg.norm(oa - ofoot)):
            raise ValueError("the displayed h_a base must equal the copied original altitude")
        height_triangle_fill = Polygon(ha_a, ha_b, ha_c, stroke_width=0, fill_color=REGION, fill_opacity=0.08)
        edge_ha = Line(ha_b, ha_c, color=REGION, stroke_width=5.0)
        edge_hb = Line(ha_c, ha_a, color=BLUE, stroke_width=5.0)
        edge_hc = Line(ha_a, ha_b, color=PURPLE, stroke_width=5.0)
        height_triangle = VGroup(height_triangle_fill, edge_ha, edge_hb, edge_hc)
        height_labels = VGroup(
            self.edge_label("h_a", ha_b, ha_c, DOWN * 0.26, REGION, 31),
            self.edge_label("h_b", ha_c, ha_a, RIGHT * 0.24, BLUE, 31),
            self.edge_label("h_c", ha_a, ha_b, LEFT * 0.22, PURPLE, 31),
        )
        second_height = DashedLine(ha_a, ha_foot, color=POINT, stroke_width=3.6)
        second_height_name = MathTex(r"h'_a", font_size=32, color=POINT).move_to(ha_foot + RIGHT * 0.32 + UP * 0.72)
        second_right = RightAngle(Line(ha_foot, ha_c), Line(ha_foot, ha_a), length=0.22, color=POINT, stroke_width=3.0)
        k_badge = MathTex(r"K=45", font_size=44, color=INK).move_to([-3.05, -2.50, 0])
        h_badge = MathTex(r"H=\Delta(h_a,h_b,h_c)=30", font_size=40, color=REGION).move_to([3.10, -2.50, 0])
        self.play(
            FadeIn(height_triangle_fill),
            Create(edge_hb),
            Create(edge_hc),
            FadeIn(height_labels[1]),
            FadeIn(height_labels[2]),
            run_time=0.68,
        )
        self.play(TransformFromCopy(altitude_a, edge_ha), FadeIn(height_labels[0]), run_time=0.72)
        self.play(Create(second_height), FadeIn(second_height_name), Create(second_right), run_time=0.62)

        # Beat 22 compare_two_area_units: continue at a settled semantic boundary.
        self.next_beat("compare_two_area_units")
        self.play(FadeIn(k_badge), FadeIn(h_badge), run_time=0.62)
        altitude_question = MathTex(r"\Delta(h'_a,h'_b,h'_c)=?", font_size=43, color=CORAL).move_to([3.15, 2.35, 0])
        self.play(FadeIn(altitude_question), run_time=0.58)
        self.wait(0.70)

        # Beat 23 derive_one_second_altitude: divide the paired base-height formulas.
        self.next_beat("derive_one_second_altitude")
        title = self.replace_title(self, title, "兩個面積式相除，共用的 h_a 消去")
        height_stage = VGroup(height_triangle, height_labels, second_height, second_height_name, second_right)
        self.play(
            FadeOut(altitude_question),
            FadeOut(k_badge),
            FadeOut(h_badge),
            FadeOut(altitude_stage),
            FadeOut(height_stage),
            run_time=0.48,
        )
        paired_formulas = VGroup(
            MathTex(r"K=\frac12a h_a=45", font_size=44, color=INK),
            MathTex(r"H=\frac12h_a h'_a=30", font_size=44, color=INK),
        ).arrange(DOWN, buff=0.52)
        paired_formulas.move_to([-3.35, 0.35, 0])
        paired_formulas[0].set_color_by_tex("h_a", REGION)
        paired_formulas[1].set_color_by_tex("h_a", REGION)
        ratio_a = MathTex(r"\frac{h'_a}{a}=\frac HK=\frac{30}{45}=\frac23", font_size=47, color=INK)
        ratio_a.set_color_by_tex(r"\frac23", REGION)
        ratio_a.move_to([2.55, 1.32, 0])
        cyclic_altitudes = VGroup(
            MathTex(r"h'_a=\frac23a", font_size=42, color=POINT),
            MathTex(r"h'_b=\frac23b", font_size=42, color=BLUE),
            MathTex(r"h'_c=\frac23c", font_size=42, color=PURPLE),
        ).arrange(DOWN, buff=0.38)
        cyclic_altitudes.move_to([2.55, -0.78, 0])
        self.play(FadeIn(paired_formulas[0]), FadeIn(paired_formulas[1]), run_time=0.90)
        self.play(Indicate(paired_formulas[0], color=REGION), Indicate(paired_formulas[1], color=REGION), run_time=0.58)
        self.play(FadeIn(ratio_a), run_time=0.82)

        # Beat 24 derive_second_altitudes: continue at a settled semantic boundary.
        self.next_beat("derive_second_altitudes")
        self.play(LaggedStart(*(FadeIn(item) for item in cyclic_altitudes), lag_ratio=0.18), run_time=0.95)
        self.wait(0.70)

        # Beat 25 build_second_altitude_similarity: show the 2/3 similarity and hold the area behind a question.
        self.next_beat("build_second_altitude_similarity")
        title = self.replace_title(self, title, "三邊同時縮成 2/3，面積比要平方")
        self.play(
            FadeOut(paired_formulas),
            FadeOut(ratio_a),
            FadeOut(cyclic_altitudes),
            run_time=0.52,
        )
        sim_left_center = np.array([-3.45, 0.25, 0])
        sim_right_center = np.array([3.35, 0.25, 0])
        sim_left = self.triangle_icon(sim_left_center, BLUE, 2.15)
        sim_right = self.triangle_icon(sim_right_center, PURPLE, 1.43)
        sim_left_labels = VGroup(
            MathTex("a", font_size=32, color=POINT).move_to(sim_left_center + DOWN * 1.20),
            MathTex("b", font_size=32, color=BLUE).move_to(sim_left_center + RIGHT * 1.45 + UP * 0.05),
            MathTex("c", font_size=32, color=PURPLE).move_to(sim_left_center + LEFT * 1.25 + UP * 0.10),
        )
        sim_right_labels = VGroup(
            MathTex(r"h'_a=\frac23a", font_size=29, color=POINT).move_to(sim_right_center + DOWN * 0.93),
            MathTex(r"h'_b", font_size=28, color=BLUE).move_to(sim_right_center + RIGHT * 1.08),
            MathTex(r"h'_c", font_size=28, color=PURPLE).move_to(sim_right_center + LEFT * 0.94),
        )
        similarity_arrow = MathTex(r"\times\frac23", font_size=52, color=REGION).move_to([0, 0.35, 0])
        original_area_label = MathTex("45", font_size=48, color=INK).move_to(sim_left_center)
        new_area_question = MathTex("?", font_size=52, color=CORAL).move_to(sim_right_center)
        preanswer_4 = MathTex(
            r"\Delta(h'_a,h'_b,h'_c)=45\left(\frac23\right)^2=?",
            font_size=48,
            color=INK,
        )
        preanswer_4.set_color_by_tex("?", CORAL)
        preanswer_4.move_to([0, -2.38, 0])
        similarity_stage = VGroup(sim_left, sim_right, sim_left_labels, sim_right_labels, similarity_arrow, original_area_label)
        self.play(FadeIn(sim_left), FadeIn(sim_left_labels), FadeIn(original_area_label), run_time=0.58)
        self.play(TransformFromCopy(sim_left, sim_right), FadeIn(similarity_arrow), run_time=0.86)
        self.play(FadeIn(sim_right_labels), FadeIn(new_area_question), run_time=0.52)

        # Beat 26 hold_altitude_area_preanswer: continue at a settled semantic boundary.
        self.next_beat("hold_altitude_area_preanswer")
        self.play(FadeIn(preanswer_4), run_time=0.78)
        self.wait(0.92)

        # Beat 27 reveal_altitude_area: reveal the fourth answer only after the squared factor settles.
        self.next_beat("reveal_altitude_area")
        title = self.replace_title(self, title, "九分之四乘回 45，最後才算出新面積")
        self.play(Indicate(preanswer_4, color=REGION), run_time=0.58)
        self.wait(0.78)
        answer_4_number = MathTex("20", font_size=58, color=CORAL).move_to(new_area_question)
        answer_4 = MathTex(
            r"\Delta(h'_a,h'_b,h'_c)=20",
            font_size=58,
            color=CORAL,
        ).move_to([0, -2.38, 0])
        self.play(FadeOut(new_area_question), FadeOut(preanswer_4), run_time=0.42)
        self.play(FadeIn(answer_4_number), FadeIn(answer_4), run_time=0.68)
        answer_4_frame = self.answer_frame(answer_4)
        self.play(Create(answer_4_frame), Indicate(sim_right, color=PURPLE), run_time=0.60)
        self.wait(0.72)

        # Beat 28 collect_four_area_results: consolidate only after all four answers have been earned.
        self.next_beat("collect_four_area_results")
        title = self.replace_title(self, title, "四小題，其實都在追同一個面積倍率")
        self.play(
            FadeOut(similarity_stage),
            FadeOut(answer_4_number),
            FadeOut(answer_4),
            FadeOut(answer_4_frame),
            run_time=0.54,
        )
        card_centers = [
            np.array([-4.85, 0.55, 0]),
            np.array([-1.62, 0.55, 0]),
            np.array([1.62, 0.55, 0]),
            np.array([4.85, 0.55, 0]),
        ]
        cards = VGroup(
            self.result_card("第一小題", r"\Delta(3,4,5)=6", card_centers[0], BLUE),
            self.result_card("第二小題", r"k=4", card_centers[1], POINT),
            self.result_card("第三小題", r"16\to12\to9", card_centers[2], REGION),
            self.result_card("第四小題", r"45\to20", card_centers[3], CORAL),
        )
        final_tuple = MathTex(r"(6,4,9,20)", font_size=68, color=CORAL).move_to([0, -1.35, 0])
        final_frame = self.answer_frame(final_tuple, REGION)
        principle = label("先找長度比，再平方成面積比", 27, INK, "BOLD")
        principle.move_to([0, -2.45, 0])
        footer = label("解題來源：正哥愛數學｜原創重繪與獨立核對", 20, MUTED, "MEDIUM")
        footer.move_to([0, -3.38, 0])
        self.play(LaggedStart(*(FadeIn(card) for card in cards), lag_ratio=0.16), run_time=1.08)
        self.play(FadeIn(final_tuple), Create(final_frame), run_time=0.76)

        # Beat 29 consolidate_four_results: continue at a settled semantic boundary.
        self.next_beat("consolidate_four_results")
        self.play(FadeIn(principle), run_time=0.50)
        self.play(FadeIn(footer), run_time=0.42)
        self.wait(0.92)
