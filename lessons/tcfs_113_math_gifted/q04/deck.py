"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q4."""

from __future__ import annotations

import math

import numpy as np

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    REGION,
    CarloSlide,
    label,
)
from manim import (
    Arc,
    Arrow,
    Circumscribe,
    Create,
    Cross,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Square,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


def is_valid_parameter(n: int) -> bool:
    """Return whether n-1, n, n+1 form an allowed acute triangle."""
    a, b, c = n - 1, n, n + 1
    return a > 0 and a + b > c and a * a + b * b > c * c and a + b + c <= 113


VALID_N = tuple(n for n in range(1, 114) if is_valid_parameter(n))
EXPECTED_N = tuple(range(5, 38))

if VALID_N != EXPECTED_N:
    raise ValueError(f"unexpected valid parameters: {VALID_N}")
if len(VALID_N) != 33:
    raise ValueError("unexpected count of acute consecutive-side triangles")


class CarloTcfs113MathQ04(CarloSlide):
    """Discover the lower and upper integer boundaries before counting."""

    lesson_id = "carlo.tcfs_113_math_gifted.q04"

    @staticmethod
    def triangle_points(
        n: int,
        *,
        base_mid: tuple[float, float] = (-3.75, -1.12),
        scale: float = 0.70,
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Place a triangle with side lengths n-1, n, n+1 on a horizontal base."""
        short, middle, longest = n - 1, n, n + 1
        horizontal = (middle * middle + longest * longest - short * short) / (
            2 * longest
        )
        height = math.sqrt(max(middle * middle - horizontal * horizontal, 0.0))
        center = np.array([base_mid[0], base_mid[1], 0.0])
        left = center + LEFT * longest * scale / 2
        right = center + RIGHT * longest * scale / 2
        apex = left + np.array([horizontal * scale, height * scale, 0.0])
        return left, right, apex

    @classmethod
    def triangle_model(
        cls,
        n: int,
        *,
        base_mid: tuple[float, float] = (-3.75, -1.12),
        scale: float = 0.70,
        symbolic: bool = False,
        font_size: float = 34,
    ) -> VGroup:
        """Build one family member while preserving each side's color role."""
        left, right, apex = cls.triangle_points(n, base_mid=base_mid, scale=scale)
        fill = Polygon(
            left,
            right,
            apex,
            stroke_width=0,
            fill_color=REGION,
            fill_opacity=0.055,
        )
        middle_side = Line(left, apex, color=POINT, stroke_width=5)
        short_side = Line(apex, right, color=BLUE, stroke_width=5)
        longest_side = Line(right, left, color=REGION, stroke_width=5)

        short_tex = "n-1" if symbolic else str(n - 1)
        middle_tex = "n" if symbolic else str(n)
        longest_tex = "n+1" if symbolic else str(n + 1)
        middle_label = MathTex(middle_tex, font_size=font_size, color=POINT)
        middle_label.move_to((left + apex) / 2 + LEFT * 0.33 + UP * 0.04)
        short_label = MathTex(short_tex, font_size=font_size, color=BLUE)
        short_label.move_to((apex + right) / 2 + RIGHT * 0.34 + UP * 0.04)
        longest_label = MathTex(longest_tex, font_size=font_size, color=REGION)
        longest_label.move_to((left + right) / 2 + DOWN * 0.34)
        return VGroup(
            fill,
            middle_side,
            short_side,
            longest_side,
            middle_label,
            short_label,
            longest_label,
        )

    @classmethod
    def vertex_angle(
        cls,
        n: int,
        tex: str,
        color: str,
        *,
        base_mid: tuple[float, float] = (-3.75, -1.12),
        scale: float = 0.70,
    ) -> VGroup:
        """Mark the angle opposite the longest side with an exact interior arc."""
        left, right, apex = cls.triangle_points(n, base_mid=base_mid, scale=scale)
        first = (left - apex) / np.linalg.norm(left - apex)
        second = (right - apex) / np.linalg.norm(right - apex)
        start = math.atan2(first[1], first[0])
        end = math.atan2(second[1], second[0])
        sweep = (end - start) % (2 * math.pi)
        if sweep > math.pi:
            start, end = end, start
            sweep = (end - start) % (2 * math.pi)
        arc = Arc(radius=0.40, start_angle=start, angle=sweep, color=color, stroke_width=5)
        arc.shift(apex)
        bisector = first + second
        bisector /= np.linalg.norm(bisector)
        angle_label = MathTex(tex, font_size=27, color=color)
        angle_label.move_to(apex + bisector * 0.82)
        return VGroup(arc, angle_label)

    @staticmethod
    def colored_triplet(n: int, *, font_size: float = 52) -> MathTex:
        result = MathTex(
            "(",
            str(n - 1),
            ",",
            str(n),
            ",",
            str(n + 1),
            ")",
            font_size=font_size,
            color=INK,
        )
        result[1].set_color(BLUE)
        result[3].set_color(POINT)
        result[5].set_color(REGION)
        return result

    @staticmethod
    def symbolic_triplet(*, font_size: float = 48) -> MathTex:
        result = MathTex(
            "n-1",
            ",",
            "n",
            ",",
            "n+1",
            font_size=font_size,
            color=INK,
        )
        result[0].set_color(BLUE)
        result[2].set_color(POINT)
        result[4].set_color(REGION)
        return result

    @staticmethod
    def length_panel(n: int, x: float) -> VGroup:
        """Compare the joined short sides against the longest side."""
        unit = 0.49
        first = Rectangle(
            width=(n - 1) * unit,
            height=0.42,
            stroke_color=BLUE,
            stroke_width=2.4,
            fill_color=BLUE,
            fill_opacity=0.18,
        )
        second = Rectangle(
            width=n * unit,
            height=0.42,
            stroke_color=POINT,
            stroke_width=2.4,
            fill_color=POINT,
            fill_opacity=0.18,
        )
        joined = VGroup(first, second).arrange(RIGHT, buff=0)
        joined.move_to([x, 0.57, 0])
        first_number = MathTex(str(n - 1), font_size=26, color=BLUE).move_to(first)
        second_number = MathTex(str(n), font_size=26, color=POINT).move_to(second)
        longest = Rectangle(
            width=(n + 1) * unit,
            height=0.42,
            stroke_color=REGION,
            stroke_width=2.4,
            fill_color=REGION,
            fill_opacity=0.18,
        )
        longest.align_to(joined, LEFT).move_to([longest.get_center()[0], -0.33, 0])
        longest_number = MathTex(str(n + 1), font_size=26, color=REGION).move_to(longest)
        relation = MathTex("=" if n == 2 else ">", font_size=42, color=CORAL if n == 2 else REGION)
        relation.move_to([x, -1.03, 0])
        equation = MathTex(
            str(n - 1),
            "+",
            str(n),
            "=" if n == 2 else ">",
            str(n + 1),
            font_size=35,
            color=INK,
        )
        equation[0].set_color(BLUE)
        equation[2].set_color(POINT)
        equation[4].set_color(REGION)
        equation[3].set_color(CORAL if n == 2 else REGION)
        equation.move_to([x, -1.58, 0])
        title = MathTex(rf"n={n}", font_size=39, color=CORAL if n == 2 else POINT)
        title.move_to([x, 1.58, 0])
        return VGroup(
            title,
            joined,
            first_number,
            second_number,
            longest,
            longest_number,
            relation,
            equation,
        )

    @staticmethod
    def area_square(side: float, tex: str, color: str) -> VGroup:
        box = Square(
            side_length=side,
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.13,
        )
        area = MathTex(tex, font_size=31, color=color).move_to(box)
        return VGroup(box, area)

    @classmethod
    def square_comparison(cls, n: int | None, relation: str) -> VGroup:
        """Arrange the two shorter-side squares against the longest one."""
        display_n = 5 if n is None else n
        unit = 1.72 / (display_n + 1)
        if n is None:
            area_tex = (r"(n-1)^2", "n^2", r"(n+1)^2")
        else:
            area_tex = (str((n - 1) ** 2), str(n**2), str((n + 1) ** 2))
        short_square = cls.area_square((display_n - 1) * unit, area_tex[0], BLUE)
        middle_square = cls.area_square(display_n * unit, area_tex[1], POINT)
        long_square = cls.area_square((display_n + 1) * unit, area_tex[2], REGION)
        short_square.move_to([1.55, 1.25, 0])
        middle_square.move_to([1.55, -0.90, 0])
        long_square.move_to([5.06, 0.10, 0])
        plus = MathTex("+", font_size=47, color=INK).move_to([1.55, 0.22, 0])
        comparator = MathTex(
            relation,
            font_size=54,
            color=CORAL if relation == "=" else REGION if relation == ">" else MUTED,
        ).move_to([3.28, 0.10, 0])
        return VGroup(short_square, plus, middle_square, comparator, long_square)

    @staticmethod
    def range_row(
        y: float,
        text: str,
        color: str,
        start: int,
        end: int,
        *,
        arrow_right: bool = False,
    ) -> VGroup:
        """Draw one aligned integer range from the shared 2-to-38 ruler."""
        left_x, right_x = -4.20, 6.05

        def x_for(value: int) -> float:
            return left_x + (value - 2) * (right_x - left_x) / 36

        baseline = Line([left_x, y, 0], [right_x, y, 0], color=HAIRLINE, stroke_width=2)
        ticks = VGroup(
            *(
                Line(
                    [x_for(value), y - 0.08, 0],
                    [x_for(value), y + 0.08, 0],
                    color=MUTED,
                    stroke_width=1.2,
                ).set_opacity(0.46)
                for value in range(2, 39)
            )
        )
        row_label = label(text, 24, color, "BOLD").move_to([-6.15, y, 0])
        if arrow_right:
            highlight = Arrow(
                [x_for(start), y, 0],
                [right_x + 0.20, y, 0],
                buff=0,
                color=color,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.028,
            )
        else:
            highlight = Line(
                [x_for(start), y, 0],
                [x_for(end), y, 0],
                color=color,
                stroke_width=7,
            )
        endpoints = VGroup(Dot([x_for(start), y, 0], radius=0.075, color=color))
        if not arrow_right:
            endpoints.add(Dot([x_for(end), y, 0], radius=0.075, color=color))
        return VGroup(row_label, baseline, ticks, highlight, endpoints)

    def construct(self) -> None:
        heading = label("第 4 題｜連續邊長的銳角三角形", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 4 頁｜影片 W-NGUVPlcOc 02:52-04:27",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.05, -3.42, 0], [0.05, 3.15, 0], color=HAIRLINE, stroke_width=1.5)

        # Beat 01: meet one concrete member before naming any condition.
        self.begin_beat("meet_consecutive_family")
        beat_title = label("先看一個真的三角形", 33, INK, "BOLD")
        beat_title.move_to([3.78, 2.35, 0])
        triangle = self.triangle_model(5)
        triplet = self.colored_triplet(5).move_to([3.78, 1.12, 0])
        growth_note = label("每一邊都比前一邊多 1", 27, INK, "BOLD")
        growth_note.move_to([3.78, 0.22, 0])
        family = self.symbolic_triplet(font_size=46).move_to([3.78, -0.75, 0])
        opening_question = label("每一組連續正整數，都能圍起來嗎？", 24, CORAL, "BOLD")
        opening_question.move_to([3.78, -1.88, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(beat_title), run_time=0.45)
        self.play(
            LaggedStart(*(Create(side) for side in triangle[1:4]), lag_ratio=0.18),
            FadeIn(triangle[0]),
            run_time=1.35,
        )
        self.play(LaggedStart(*(FadeIn(item) for item in triangle[4:]), lag_ratio=0.18), run_time=0.8)
        self.play(TransformFromCopy(VGroup(*triangle[4:]), triplet), FadeIn(growth_note), run_time=0.8)

        self.next_beat("ask_family_question")
        self.play(FadeIn(family), FadeIn(opening_question), run_time=0.65)
        self.wait(0.35)

        # Beat 02: shrink deliberately until the triangle becomes a segment.
        self.next_beat("shrink_to_existence_edge")
        next_title = label("一路縮小，哪裡會攤平？", 33, INK, "BOLD")
        next_title.move_to(beat_title)
        n_label = MathTex("n=5", font_size=44, color=POINT).move_to([3.78, 0.03, 0])
        collapse_equation = MathTex("1", "+", "2", "=", "3", font_size=52, color=INK)
        collapse_equation[0].set_color(BLUE)
        collapse_equation[2].set_color(POINT)
        collapse_equation[3].set_color(CORAL)
        collapse_equation[4].set_color(REGION)
        collapse_equation.move_to([3.78, -1.10, 0])
        collapse_note = label("沒有面積，只剩一條線", 27, CORAL, "BOLD")
        collapse_note.move_to([3.78, -2.10, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(growth_note),
            FadeOut(family),
            FadeOut(opening_question),
            FadeIn(n_label),
            run_time=0.65,
        )
        beat_title = next_title
        for n in (4, 3):
            target_triangle = self.triangle_model(n)
            target_triplet = self.colored_triplet(n).move_to(triplet)
            target_n = MathTex(rf"n={n}", font_size=44, color=CORAL if n == 2 else POINT)
            target_n.move_to(n_label)
            self.play(
                Transform(triangle, target_triangle),
                Transform(triplet, target_triplet),
                Transform(n_label, target_n),
                run_time=0.85,
            )

        self.next_beat("collapse_to_degenerate_triangle")
        n = 2
        target_triangle = self.triangle_model(n)
        target_triplet = self.colored_triplet(n).move_to(triplet)
        target_n = MathTex(rf"n={n}", font_size=44, color=CORAL)
        target_n.move_to(n_label)
        self.play(
            Transform(triangle, target_triangle),
            Transform(triplet, target_triplet),
            Transform(n_label, target_n),
            run_time=0.85,
        )
        self.play(Write(collapse_equation), FadeIn(collapse_note), run_time=0.7)
        self.play(Circumscribe(triangle, color=CORAL), run_time=0.8)
        self.wait(0.35)

        # Beat 03: turn the visible collapse into the exact existence range.
        self.next_beat("earn_triangle_range")
        next_title = label("先找出『能成為三角形』的邊界", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        panel_two = self.length_panel(2, -4.82)
        panel_three = self.length_panel(3, -1.72)
        separator = Line([0.20, -2.45, 0], [0.20, 2.28, 0], color=HAIRLINE)
        general_inequality = MathTex(
            "(n-1)",
            "+",
            "n",
            ">",
            "n+1",
            font_size=43,
            color=INK,
        ).move_to([4.05, 1.08, 0])
        general_inequality[0].set_color(BLUE)
        general_inequality[2].set_color(POINT)
        general_inequality[3].set_color(REGION)
        general_inequality[4].set_color(REGION)
        simplify_existence = MathTex("n>2", font_size=49, color=INK).move_to([4.05, -0.03, 0])
        integer_existence = MathTex(r"n\in\mathbb Z_{>0}", r"\Longrightarrow", r"n\ge3", font_size=40, color=INK)
        integer_existence[0].set_color(MUTED)
        integer_existence[2].set_color(POINT)
        integer_existence.move_to([4.05, -1.17, 0])
        existence_note = label("從 n = 3 開始，才有真正的面積", 24, POINT, "BOLD")
        existence_note.move_to([4.05, -2.13, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(triangle),
            FadeOut(triplet),
            FadeOut(n_label),
            FadeOut(collapse_equation),
            FadeOut(collapse_note),
            FadeOut(divider),
            run_time=0.7,
        )
        beat_title = next_title
        self.play(FadeIn(panel_two), run_time=0.75)
        self.play(FadeIn(panel_three), Create(separator), run_time=0.75)

        self.next_beat("derive_triangle_existence")
        self.play(Write(general_inequality), run_time=0.8)
        self.play(Write(simplify_existence), run_time=0.45)
        self.play(Write(integer_existence), FadeIn(existence_note), run_time=0.75)
        self.wait(0.35)

        # Beat 04: copy the three side roles into a square-area comparison.
        self.next_beat("build_square_test")
        next_title = label("銳角與否，要比較三個正方形", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        symbolic_triangle = self.triangle_model(5, symbolic=True, font_size=31)
        symbolic_angle = self.vertex_angle(5, r"\theta", MUTED)
        largest_note = label("最長邊對著最大角", 25, REGION, "BOLD")
        largest_note.move_to([-3.75, -2.33, 0])
        square_test = self.square_comparison(None, "?")
        square_formula = MathTex(
            r"(n-1)^2",
            "+",
            "n^2",
            r"\ ?\ ",
            r"(n+1)^2",
            font_size=38,
            color=INK,
        ).move_to([3.46, -2.35, 0])
        square_formula[0].set_color(BLUE)
        square_formula[2].set_color(POINT)
        square_formula[3].set_color(MUTED)
        square_formula[4].set_color(REGION)
        square_prompt = label("先測試邊界，不急著背公式", 23, MUTED, "MEDIUM")
        square_prompt.move_to([3.46, 2.32, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(panel_two),
            FadeOut(panel_three),
            FadeOut(separator),
            FadeOut(general_inequality),
            FadeOut(simplify_existence),
            FadeOut(integer_existence),
            FadeOut(existence_note),
            FadeIn(divider),
            FadeIn(symbolic_triangle),
            run_time=0.9,
        )
        beat_title = next_title
        self.play(Create(symbolic_angle[0]), FadeIn(symbolic_angle[1]), FadeIn(largest_note), run_time=0.75)
        self.play(
            LaggedStart(
                GrowFromCenter(square_test[0]),
                FadeIn(square_test[1]),
                GrowFromCenter(square_test[2]),
                FadeIn(square_test[3]),
                GrowFromCenter(square_test[4]),
                lag_ratio=0.14,
            ),
            run_time=1.3,
        )
        self.play(Write(square_formula), FadeIn(square_prompt), run_time=0.7)

        # Beat 05: equality of areas makes n=4 the right-angle boundary.
        self.next_beat("test_right_boundary")
        next_title = label("n = 4｜剛好卡在直角邊界", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        triangle_four = self.triangle_model(4)
        angle_four = self.vertex_angle(4, r"90^\circ", CORAL)
        squares_four = self.square_comparison(4, "=")
        formula_four = MathTex("9", "+", "16", "=", "25", font_size=43, color=INK)
        formula_four[0].set_color(BLUE)
        formula_four[2].set_color(POINT)
        formula_four[3].set_color(CORAL)
        formula_four[4].set_color(REGION)
        formula_four.move_to(square_formula)
        boundary_note = label("直角，不列入銳角", 27, CORAL, "BOLD")
        boundary_note.move_to([3.46, 2.32, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            Transform(symbolic_triangle, triangle_four),
            Transform(symbolic_angle, angle_four),
            Transform(square_test, squares_four),
            Transform(square_formula, formula_four),
            ReplacementTransform(square_prompt, boundary_note),
            FadeOut(largest_note),
            run_time=1.15,
        )
        beat_title = next_title
        self.play(Indicate(square_formula, color=CORAL), run_time=0.8)
        self.play(Circumscribe(symbolic_angle, color=CORAL), run_time=0.8)
        self.wait(0.3)

        # Beat 06: one integer step turns the area equality into a strict win.
        self.next_beat("step_into_acute")
        next_title = label("只往前一步：n = 5", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        triangle_five = self.triangle_model(5)
        angle_five = self.vertex_angle(5, r"<90^\circ", REGION)
        squares_five = self.square_comparison(5, ">")
        formula_five = MathTex(
            "16",
            "+",
            "25",
            "=",
            "41",
            ">",
            "36",
            font_size=41,
            color=INK,
        )
        formula_five[0].set_color(BLUE)
        formula_five[2].set_color(POINT)
        formula_five[4].set_color(POINT)
        formula_five[5].set_color(REGION)
        formula_five[6].set_color(REGION)
        formula_five.move_to(square_formula)
        acute_note = label("最大角已經小於 90 度", 27, REGION, "BOLD")
        acute_note.move_to([3.46, 2.32, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            Transform(symbolic_triangle, triangle_five),
            Transform(symbolic_angle, angle_five),
            Transform(square_test, squares_five),
            Transform(square_formula, formula_five),
            ReplacementTransform(boundary_note, acute_note),
            run_time=1.15,
        )
        beat_title = next_title
        self.play(Indicate(VGroup(square_formula[0], square_formula[2], square_formula[4]), color=POINT), run_time=0.8)
        self.play(Indicate(VGroup(square_formula[5], square_formula[6]), color=REGION), run_time=0.8)
        self.wait(0.35)

        # Beat 07: generalize only after both sides of the boundary are visible.
        self.next_beat("generalize_acute_range")
        next_title = label("現在才把銳角條件寫成一般式", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        anchor_formula = MathTex("16", "+", "25", ">", "36", font_size=38, color=INK)
        anchor_formula[0].set_color(BLUE)
        anchor_formula[2].set_color(POINT)
        anchor_formula[3].set_color(REGION)
        anchor_formula[4].set_color(REGION)
        anchor_formula.move_to([-3.75, -2.35, 0])
        generic_acute = MathTex(
            r"(n-1)^2",
            "+",
            "n^2",
            ">",
            r"(n+1)^2",
            font_size=39,
            color=INK,
        ).move_to([3.55, 1.73, 0])
        generic_acute[0].set_color(BLUE)
        generic_acute[2].set_color(POINT)
        generic_acute[3].set_color(REGION)
        generic_acute[4].set_color(REGION)
        expanded_acute = MathTex("n^2", "-", "4n", ">", "0", font_size=43, color=INK)
        expanded_acute[3].set_color(REGION)
        expanded_acute.move_to([3.55, 0.73, 0])
        factored_acute = MathTex("n", "(", "n-4", ")", ">", "0", font_size=43, color=INK)
        factored_acute[2].set_color(POINT)
        factored_acute[4].set_color(REGION)
        factored_acute.move_to([3.55, -0.20, 0])
        negative_branch = MathTex("n<0", font_size=39, color=MUTED)
        positive_branch = MathTex("n>4", font_size=39, color=POINT)
        branch_or = label("或", 24, MUTED, "MEDIUM")
        branches = VGroup(negative_branch, branch_or, positive_branch).arrange(RIGHT, buff=0.55)
        branches.move_to([3.55, -1.15, 0])
        negative_cross = Cross(negative_branch, stroke_color=CORAL, stroke_width=5)
        final_acute = MathTex(r"n\in\mathbb Z_{>0}", r"\Longrightarrow", r"n\ge5", font_size=39, color=INK)
        final_acute[0].set_color(MUTED)
        final_acute[2].set_color(POINT)
        final_acute.move_to([3.55, -2.28, 0])
        acute_box = SurroundingRectangle(final_acute[2], color=POINT, buff=0.15, stroke_width=3)

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(square_test),
            FadeOut(square_formula),
            FadeOut(acute_note),
            Transform(symbolic_angle, self.vertex_angle(5, r"<90^\circ", REGION)),
            FadeIn(anchor_formula),
            run_time=0.8,
        )
        beat_title = next_title
        self.play(Write(generic_acute), run_time=0.8)
        self.play(Write(expanded_acute), run_time=0.65)
        self.play(Write(factored_acute), run_time=0.65)

        self.next_beat("apply_positive_integer_domain")
        self.play(FadeIn(branches), run_time=0.55)
        self.play(Create(negative_cross), Indicate(positive_branch, color=POINT), run_time=0.8)
        self.play(Write(final_acute), Create(acute_box), run_time=0.75)
        self.wait(0.35)

        # Beat 08: add the independent perimeter ceiling and test both sides.
        self.next_beat("add_perimeter_ceiling")
        next_title = label("最後才加入周長 113", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        perimeter_triangle = self.triangle_model(5, symbolic=True, font_size=30)
        acute_badge = VGroup(
            label("銳角已知", 21, MUTED, "MEDIUM"),
            MathTex(r"n\ge5", font_size=39, color=POINT),
        ).arrange(RIGHT, buff=0.28).move_to([-3.75, -2.35, 0])
        perimeter_sum = MathTex(
            "(n-1)",
            "+",
            "n",
            "+",
            "(n+1)",
            "=",
            "3n",
            font_size=40,
            color=INK,
        ).move_to([3.65, 2.00, 0])
        perimeter_sum[0].set_color(BLUE)
        perimeter_sum[2].set_color(POINT)
        perimeter_sum[4].set_color(REGION)
        perimeter_sum[6].set_color(POINT)
        perimeter_limit = MathTex("3n", r"\le", "113", font_size=43, color=INK)
        perimeter_limit[0].set_color(POINT)
        perimeter_limit[1].set_color(BLUE)
        perimeter_limit[2].set_color(BLUE)
        perimeter_limit.move_to([3.65, 1.10, 0])
        perimeter_axis = NumberLine(
            x_range=[108, 115, 1],
            length=6.10,
            include_numbers=True,
            font_size=24,
            color=MUTED,
            stroke_width=2.2,
            include_tip=False,
        ).move_to([3.65, -0.25, 0])
        cap_line = Line(
            perimeter_axis.n2p(113) + DOWN * 0.42,
            perimeter_axis.n2p(113) + UP * 0.55,
            color=CORAL,
            stroke_width=4,
        )
        cap_label = MathTex("113", font_size=28, color=CORAL)
        cap_label.next_to(cap_line, UP, buff=0.08)
        dot_111 = Dot(perimeter_axis.n2p(111), radius=0.10, color=POINT)
        dot_114 = Dot(perimeter_axis.n2p(114), radius=0.10, color=CORAL)
        test_37 = MathTex("n=37", r"\Longrightarrow", "3n=111", font_size=31, color=INK)
        test_37[0].set_color(POINT)
        test_37[2].set_color(POINT)
        test_37.move_to([2.00, -1.45, 0])
        test_38 = MathTex("n=38", r"\Longrightarrow", "3n=114", font_size=31, color=INK)
        test_38[0].set_color(CORAL)
        test_38[2].set_color(CORAL)
        test_38.move_to([5.30, -1.45, 0])
        final_perimeter = MathTex(r"n\le37", font_size=49, color=BLUE).move_to([3.65, -2.45, 0])
        perimeter_box = SurroundingRectangle(final_perimeter, color=BLUE, buff=0.16, stroke_width=3)

        self.play(
            ReplacementTransform(beat_title, next_title),
            Transform(symbolic_triangle, perimeter_triangle),
            FadeOut(symbolic_angle),
            FadeOut(anchor_formula),
            FadeOut(generic_acute),
            FadeOut(expanded_acute),
            FadeOut(factored_acute),
            FadeOut(branches),
            FadeOut(negative_cross),
            FadeOut(final_acute),
            FadeOut(acute_box),
            FadeIn(acute_badge),
            run_time=0.8,
        )
        beat_title = next_title
        self.play(Write(perimeter_sum), run_time=0.85)
        self.play(Write(perimeter_limit), run_time=0.6)

        self.next_beat("test_perimeter_boundary")
        self.play(Create(perimeter_axis), Create(cap_line), FadeIn(cap_label), run_time=0.9)
        self.play(FadeIn(dot_111), Write(test_37), run_time=0.65)
        self.play(FadeIn(dot_114), Write(test_38), run_time=0.65)
        self.play(Write(final_perimeter), Create(perimeter_box), run_time=0.75)
        self.wait(0.35)

        # Beat 09: align the two live ranges and make their intersection literal.
        self.next_beat("intersect_integer_ranges")
        next_title = label("兩個條件，要同時成立", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        existence_reminder = VGroup(
            label("可成三角形", 20, MUTED, "MEDIUM"),
            MathTex(r"n\ge3", font_size=30, color=MUTED),
            label("已被更嚴格的銳角條件包含", 20, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.30).move_to([0, 2.30, 0])
        acute_row = self.range_row(1.16, "銳角  n ≥ 5", POINT, 5, 38, arrow_right=True)
        perimeter_row = self.range_row(0.05, "周長  n ≤ 37", BLUE, 2, 37)
        intersection_row = self.range_row(-1.16, "同時成立", REGION, 5, 37)
        boundary_numbers = VGroup(
            MathTex("3", font_size=25, color=MUTED).move_to([-3.92, -1.68, 0]),
            MathTex("5", font_size=28, color=POINT).move_to([-3.35, -1.68, 0]),
            MathTex("37", font_size=28, color=BLUE).move_to([5.77, -1.68, 0]),
        )
        intersection_formula = MathTex(
            "5",
            r"\le n\le",
            "37",
            r",\quad n\in\mathbb Z",
            font_size=42,
            color=INK,
        ).move_to([0, -2.35, 0])
        intersection_formula[0].set_color(POINT)
        intersection_formula[2].set_color(BLUE)
        range_question = label("包含兩端：這一段有幾個整數？", 25, CORAL, "BOLD")
        range_question.move_to([0, -3.05, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(symbolic_triangle),
            FadeOut(acute_badge),
            FadeOut(perimeter_sum),
            FadeOut(perimeter_limit),
            FadeOut(perimeter_axis),
            FadeOut(cap_line),
            FadeOut(cap_label),
            FadeOut(dot_111),
            FadeOut(dot_114),
            FadeOut(test_37),
            FadeOut(test_38),
            FadeOut(final_perimeter),
            FadeOut(perimeter_box),
            FadeOut(divider),
            FadeIn(existence_reminder),
            run_time=0.85,
        )
        beat_title = next_title
        self.play(FadeIn(acute_row), run_time=0.75)
        self.play(FadeIn(perimeter_row), run_time=0.75)

        self.next_beat("form_range_intersection")
        self.play(TransformFromCopy(VGroup(acute_row[3], perimeter_row[3]), intersection_row), run_time=0.9)
        self.play(FadeIn(boundary_numbers), Write(intersection_formula), run_time=0.75)
        self.play(FadeIn(range_question), run_time=0.45)
        self.wait(0.45)

        # Beat 10: count inclusively only after the intersection is owned.
        self.next_beat("count_surviving_values")
        next_title = label("從第一個整數，數到最後一個", 32, INK, "BOLD")
        next_title.move_to([0, 3.12, 0])
        start_x = -4.20 + (5 - 2) * (6.05 + 4.20) / 36
        end_x = -4.20 + (37 - 2) * (6.05 + 4.20) / 36
        start_count = VGroup(
            MathTex("n=5", font_size=32, color=POINT),
            label("第 1 個", 23, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.14).move_to([start_x, 0.12, 0])
        end_count = VGroup(
            MathTex("n=37", font_size=32, color=BLUE),
            label("最後一個", 23, BLUE, "BOLD"),
        ).arrange(DOWN, buff=0.14).move_to([end_x, 0.12, 0])
        start_guide = Line([start_x, 0.73, 0], [start_x, 1.33, 0], color=POINT, stroke_width=2)
        end_guide = Line([end_x, 0.73, 0], [end_x, 1.33, 0], color=BLUE, stroke_width=2)
        inclusive_note = label("起點本身也要算，所以補回 1", 25, MUTED, "MEDIUM")
        inclusive_note.move_to([2.45, -0.82, 0])
        partial_count = MathTex("37", "-", "5", "+", "1", font_size=61, color=INK)
        partial_count[0].set_color(BLUE)
        partial_count[2].set_color(POINT)
        partial_count[4].set_color(POINT)
        partial_count.move_to([2.10, -1.72, 0])
        final_tail = MathTex("=", "33", font_size=61, color=INK)
        final_tail[1].set_color(POINT)
        final_tail.next_to(partial_count, RIGHT, buff=0.22)
        answer_box = SurroundingRectangle(final_tail[1], color=POINT, buff=0.16, stroke_width=3)
        mini_triangle = self.triangle_model(
            5,
            base_mid=(-4.65, -2.12),
            scale=0.36,
            font_size=23,
        )
        mini_caption = label("4、5、6 是第一個", 21, REGION, "BOLD")
        mini_caption.move_to([-4.65, -3.02, 0])
        final_note = label("從 n = 5 到 n = 37，共 33 個", 24, INK, "BOLD", t2c={"33": POINT})
        final_note.move_to([2.30, -2.78, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(existence_reminder),
            FadeOut(acute_row),
            FadeOut(perimeter_row),
            FadeOut(boundary_numbers),
            FadeOut(intersection_formula),
            FadeOut(range_question),
            intersection_row.animate.shift(UP * 2.38),
            run_time=0.9,
        )
        beat_title = next_title
        self.play(
            Create(start_guide),
            Create(end_guide),
            FadeIn(start_count),
            FadeIn(end_count),
            run_time=0.75,
        )
        self.play(FadeIn(mini_triangle), FadeIn(mini_caption), FadeIn(inclusive_note), run_time=0.8)
        self.play(Write(partial_count), run_time=0.8)
        self.wait(0.65)

        self.next_beat("reveal_surviving_count")
        self.play(Write(final_tail), Create(answer_box), run_time=0.7)
        self.play(FadeIn(final_note), Indicate(final_tail[1], color=POINT), run_time=0.8)
        self.wait(0.65)
