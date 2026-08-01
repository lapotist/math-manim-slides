"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q12."""

from __future__ import annotations

from fractions import Fraction

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
    Axes,
    Circumscribe,
    Create,
    DashedLine,
    DecimalNumber,
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
    Square,
    Succession,
    SurroundingRectangle,
    VGroup,
    ValueTracker,
    always_redraw,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


A_COORD = (Fraction(1), Fraction(-3))
B_COORD = (Fraction(7), Fraction(-3))
C_COORD = (Fraction(-2), Fraction(9))
G_COORD = (Fraction(2), Fraction(1))


def b_from_a(a_value: Fraction) -> Fraction:
    """Return the coefficient b forced by the centroid condition."""
    return Fraction(9) - 2 * a_value


def objective(a_value: Fraction) -> Fraction:
    """Return 2a^2+b^2 on the centroid line."""
    b_value = b_from_a(a_value)
    return 2 * a_value**2 + b_value**2


if (
    (A_COORD[0] + B_COORD[0] + C_COORD[0]) / 3,
    (A_COORD[1] + B_COORD[1] + C_COORD[1]) / 3,
) != G_COORD:
    raise ValueError("centroid computation is incorrect")
if 2 * G_COORD[0] + G_COORD[1] != 5:
    raise ValueError("unexpected centroid coordinates")
COEFFICIENT_STATES = (
    (Fraction(1), Fraction(7)),
    (Fraction(3, 2), Fraction(6)),
    (Fraction(2), Fraction(5)),
)
if any(b_value != b_from_a(a_value) for a_value, b_value in COEFFICIENT_STATES):
    raise ValueError("representative coefficient state misses the centroid")
if [objective(a_value) for a_value, _ in COEFFICIENT_STATES] != [
    Fraction(51),
    Fraction(81, 2),
    Fraction(33),
]:
    raise ValueError("unexpected representative objective values")
for numerator in range(8, 17):
    a_value = Fraction(numerator, 8)
    completed_square = 6 * (a_value - 3) ** 2 + 27
    if objective(a_value) != completed_square:
        raise ValueError("completed-square identity failed")
DECREASE_GRID = tuple(Fraction(numerator, 8) for numerator in range(8, 17))
if any(
    objective(right) >= objective(left)
    for left, right in zip(DECREASE_GRID, DECREASE_GRID[1:])
):
    raise ValueError("objective is not strictly decreasing on the check grid")
if (objective(Fraction(1)), objective(Fraction(2))) != (Fraction(51), Fraction(33)):
    raise ValueError("endpoint extrema are incorrect")


class CarloTcfs113MathQ12(CarloSlide):
    """Discover the allowed coefficient segment before optimizing its objective."""

    lesson_id = "carlo.tcfs_113_math_gifted.q12"

    @staticmethod
    def transition_title(scene: "CarloTcfs113MathQ12", old, new) -> None:
        """Swap CJK titles without morphing glyph outlines."""
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.55)

    @staticmethod
    def triangle_axes() -> tuple[Axes, VGroup]:
        """Build the stable coordinate plane used at the start and finish."""
        axes = Axes(
            x_range=[-3, 8, 1],
            y_range=[-4, 10, 2],
            x_length=5.65,
            y_length=6.55,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": True,
                "include_ticks": True,
            },
            tips=True,
        ).move_to([-3.67, -0.20, 0])
        axis_labels = VGroup(
            MathTex("x", font_size=23, color=MUTED).next_to(
                axes.x_axis.get_end(), DOWN, buff=0.06
            ),
            MathTex("y", font_size=23, color=MUTED).next_to(
                axes.y_axis.get_end(), LEFT, buff=0.06
            ),
        )
        return axes, axis_labels

    @staticmethod
    def colored_objective(font_size: float = 42) -> MathTex:
        """Create the objective with stable coefficient colors."""
        expression = MathTex(
            "2a^2",
            "+",
            "b^2",
            font_size=font_size,
            color=INK,
        )
        expression[0].set_color(BLUE)
        expression[2].set_color(PURPLE)
        return expression

    def construct(self) -> None:
        heading = label("第 12 題｜重心固定的直線與二次式", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 12 頁｜影片 FxSdkChC9Z8 03:00-04:11",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.72, -3.52, 0], [0.72, 3.42, 0], color=HAIRLINE, stroke_width=1.5)

        axes, axis_labels = self.triangle_axes()
        a_point = axes.c2p(1, -3)
        b_point = axes.c2p(7, -3)
        c_point = axes.c2p(-2, 9)
        g_point = axes.c2p(2, 1)
        triangle = Polygon(
            a_point,
            b_point,
            c_point,
            color=INK,
            stroke_width=3.5,
            fill_color=INK,
            fill_opacity=0.035,
        ).set_z_index(2)
        vertex_dots = VGroup(
            Dot(a_point, radius=0.075, color=INK),
            Dot(b_point, radius=0.075, color=INK),
            Dot(c_point, radius=0.075, color=INK),
        ).set_z_index(7)
        vertex_names = VGroup(
            MathTex("A", font_size=28, color=INK).next_to(a_point, DOWN + LEFT, buff=0.10),
            MathTex("B", font_size=28, color=INK).next_to(b_point, DOWN + RIGHT, buff=0.10),
            MathTex("C", font_size=28, color=INK).next_to(c_point, UP + LEFT, buff=0.10),
        ).set_z_index(8)
        coordinate_labels = VGroup(
            MathTex("(1,-3)", font_size=24, color=MUTED).next_to(a_point, UP + LEFT, buff=0.12),
            MathTex("(7,-3)", font_size=24, color=MUTED).next_to(b_point, UP + RIGHT, buff=0.12),
            MathTex("(-2,9)", font_size=24, color=MUTED).next_to(c_point, RIGHT, buff=0.12),
        ).set_z_index(8)

        # Beat 01 meet_triangle: establish the fixed triangle before naming its centroid.
        self.begin_beat("meet_triangle")
        stage_title = label("先找到三角形裡不會動的點", 33, INK, "BOLD")
        stage_title.move_to([4.30, 3.04, 0])
        triangle_data = VGroup(
            MathTex("A=(1,-3)", font_size=38, color=INK),
            MathTex("B=(7,-3)", font_size=38, color=INK),
            MathTex("C=(-2,9)", font_size=38, color=INK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        opening_question = label("三條中線會在哪裡相遇？", 30, POINT, "BOLD")
        opening_panel = VGroup(
            label("三個頂點都固定", 25, MUTED, "MEDIUM"),
            triangle_data,
            opening_question,
        ).arrange(DOWN, buff=0.52)
        opening_panel.move_to([4.30, -0.12, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Create(axes), FadeIn(axis_labels), run_time=0.9)
        self.play(Create(triangle), FadeIn(vertex_dots), FadeIn(vertex_names), run_time=0.8)
        self.play(FadeIn(coordinate_labels), run_time=0.55)
        self.play(LaggedStart(*(FadeIn(item) for item in opening_panel), lag_ratio=0.15), run_time=0.9)
        self.wait(0.35)

        # Beat 02 locate_centroid: construct all medians and then compute their meeting point.
        self.next_beat("locate_centroid")
        next_title = label("三條中線交在同一點 G", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        midpoint_bc = axes.c2p(Fraction(5, 2), 3)
        midpoint_ca = axes.c2p(Fraction(-1, 2), 3)
        midpoint_ab = axes.c2p(4, -3)
        midpoint_dots = VGroup(
            Dot(midpoint_bc, radius=0.055, color=MUTED),
            Dot(midpoint_ca, radius=0.055, color=MUTED),
            Dot(midpoint_ab, radius=0.055, color=MUTED),
        ).set_z_index(7)
        medians = VGroup(
            DashedLine(a_point, midpoint_bc, color=BLUE, dash_length=0.11, stroke_width=2.5),
            DashedLine(b_point, midpoint_ca, color=BLUE, dash_length=0.11, stroke_width=2.5),
            DashedLine(c_point, midpoint_ab, color=BLUE, dash_length=0.11, stroke_width=2.5),
        ).set_z_index(3)
        g_dot = Dot(g_point, radius=0.105, color=REGION).set_z_index(10)
        g_label = MathTex("G", font_size=31, color=REGION).next_to(
            g_dot, UP + RIGHT, buff=0.11
        ).set_z_index(11)
        centroid_x = MathTex(
            r"x_G={1+7-2\over3}=2",
            font_size=39,
            color=INK,
        )
        centroid_y = MathTex(
            r"y_G={-3-3+9\over3}=1",
            font_size=39,
            color=INK,
        )
        centroid_result = MathTex("G=(2,1)", font_size=51, color=REGION)
        centroid_panel = VGroup(centroid_x, centroid_y, centroid_result).arrange(
            DOWN, aligned_edge=LEFT, buff=0.48
        )
        centroid_panel.move_to([4.30, -0.10, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(opening_panel), FadeIn(midpoint_dots), run_time=0.55)
        self.play(LaggedStart(*(Create(line) for line in medians), lag_ratio=0.18), run_time=1.25)
        self.play(GrowFromCenter(g_dot), FadeIn(g_label), run_time=0.6)

        self.next_beat("compute_centroid_coordinates")
        self.play(FadeIn(centroid_x), run_time=0.8)
        self.play(FadeIn(centroid_y), run_time=0.8)
        self.play(FadeIn(centroid_result), run_time=0.65)
        self.play(Circumscribe(g_dot, color=REGION), run_time=0.7)
        self.wait(0.35)

        # Beat 03 pivot_line_family: pivot one line through G without revealing its constraint.
        self.next_beat("pivot_line_family")
        next_title = label("方向一直變，通過的點不變", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        a_tracker = ValueTracker(1.0)
        moving_line = always_redraw(
            lambda: axes.plot(
                lambda x: (9 - a_tracker.get_value() * x)
                / (9 - 2 * a_tracker.get_value()),
                x_range=[-3, 8],
                color=POINT,
                stroke_width=5,
            ).set_z_index(5)
        )
        a_readout = always_redraw(
            lambda: VGroup(
                MathTex("a=", font_size=35, color=BLUE),
                DecimalNumber(
                    a_tracker.get_value(),
                    num_decimal_places=2,
                    font_size=35,
                    color=BLUE,
                ),
            ).arrange(RIGHT, buff=0.12).move_to([4.30, 0.15, 0])
        )
        b_readout = always_redraw(
            lambda: VGroup(
                MathTex("b=", font_size=35, color=PURPLE),
                DecimalNumber(
                    9 - 2 * a_tracker.get_value(),
                    num_decimal_places=2,
                    font_size=35,
                    color=PURPLE,
                ),
            ).arrange(RIGHT, buff=0.12).move_to([4.30, -0.45, 0])
        )
        moving_equation = MathTex("ax+by=9", font_size=49, color=INK)
        moving_equation.move_to([4.30, 1.72, 0])
        fixed_point_note = VGroup(
            label("每一個方向", 25, MUTED, "MEDIUM"),
            label("都穿過同一個 G", 29, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.24)
        fixed_point_note.move_to([4.30, -1.60, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(VGroup(midpoint_dots, medians, centroid_panel, coordinate_labels)),
            FadeIn(moving_equation),
            FadeIn(a_readout),
            FadeIn(b_readout),
            Create(moving_line),
            run_time=0.85,
        )
        self.play(a_tracker.animate.set_value(1.5), run_time=1.25, rate_func=rate_functions.ease_in_out_sine)
        self.play(a_tracker.animate.set_value(2.0), run_time=1.25, rate_func=rate_functions.ease_in_out_sine)
        self.play(a_tracker.animate.set_value(1.5), run_time=1.05, rate_func=rate_functions.ease_in_out_sine)

        self.next_beat("mark_fixed_centroid")
        self.play(FadeIn(fixed_point_note), Indicate(g_dot, color=REGION), run_time=0.75)
        self.wait(0.4)

        # Beat 04 earn_coefficient_constraint: substitute the fixed point into the moving line.
        self.next_beat("earn_coefficient_constraint")
        next_title = label("把固定交點代入直線", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        substitution = MathTex(
            "a(2)",
            "+",
            "b(1)",
            "=9",
            font_size=43,
            color=INK,
        )
        substitution[0].set_color(BLUE)
        substitution[2].set_color(PURPLE)
        coefficient_constraint = MathTex("2a+b=9", font_size=52, color=INK)
        coefficient_constraint[0][1].set_color(BLUE)
        coefficient_constraint[0][3].set_color(PURPLE)
        solved_b = MathTex("b", "=", "9-2a", font_size=52, color=INK)
        solved_b[0].set_color(PURPLE)
        solved_b[2].set_color(BLUE)
        constraint_note = label("選定 a，b 就跟著決定", 27, MUTED, "MEDIUM")
        constraint_panel = VGroup(
            MathTex("G=(2,1)", font_size=39, color=REGION),
            substitution,
            coefficient_constraint,
            solved_b,
            constraint_note,
        ).arrange(DOWN, buff=0.38)
        constraint_panel.move_to([4.30, -0.50, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(VGroup(a_readout, b_readout, fixed_point_note)), run_time=0.45)
        self.play(FadeIn(constraint_panel[0]), run_time=0.4)
        self.play(FadeIn(substitution), run_time=0.65)

        self.next_beat("solve_coefficient_constraint")
        self.play(FadeOut(moving_equation), FadeIn(coefficient_constraint), run_time=0.7)
        self.play(FadeIn(solved_b), run_time=0.65)
        self.play(FadeIn(constraint_note), run_time=0.45)
        self.wait(0.35)

        # Beat 05 carve_allowed_segment: intersect both inequalities on the coefficient line.
        self.next_beat("carve_allowed_segment")
        next_title = label("兩個限制，只留下一小段", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        coefficient_axes = Axes(
            x_range=[0, 3, 0.5],
            y_range=[4, 8, 1],
            x_length=5.95,
            y_length=5.65,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": True,
                "include_ticks": True,
            },
            tips=True,
        ).move_to([-3.45, -0.22, 0])
        coefficient_labels = VGroup(
            MathTex("a", font_size=27, color=BLUE).next_to(
                coefficient_axes.x_axis.get_end(), DOWN, buff=0.08
            ),
            MathTex("b", font_size=27, color=PURPLE).next_to(
                coefficient_axes.y_axis.get_end(), LEFT, buff=0.08
            ),
        )
        coefficient_line = coefficient_axes.plot(
            lambda x: 9 - 2 * x,
            x_range=[0.52, 2.48],
            color=BLUE,
            stroke_width=3.2,
        )
        boundary_a = DashedLine(
            coefficient_axes.c2p(1, 4.05),
            coefficient_axes.c2p(1, 7.85),
            color=CORAL,
            dash_length=0.10,
            stroke_width=2.5,
        )
        boundary_b = DashedLine(
            coefficient_axes.c2p(0.05, 5),
            coefficient_axes.c2p(2.95, 5),
            color=CORAL,
            dash_length=0.10,
            stroke_width=2.5,
        )
        valid_segment = Line(
            coefficient_axes.c2p(1, 7),
            coefficient_axes.c2p(2, 5),
            color=REGION,
            stroke_width=9,
        ).set_z_index(5)
        endpoint_dots = VGroup(
            Dot(coefficient_axes.c2p(1, 7), radius=0.105, color=POINT),
            Dot(coefficient_axes.c2p(2, 5), radius=0.105, color=POINT),
        ).set_z_index(7)
        endpoint_labels = VGroup(
            MathTex("(1,7)", font_size=27, color=POINT).next_to(
                coefficient_axes.c2p(1, 7), UP + RIGHT, buff=0.12
            ),
            MathTex("(2,5)", font_size=27, color=POINT).next_to(
                coefficient_axes.c2p(2, 5), DOWN + LEFT, buff=0.12
            ),
        ).set_z_index(8)
        a_bound = MathTex(r"a\ge1", font_size=42, color=BLUE)
        b_bound = MathTex(r"b\ge5", font_size=42, color=PURPLE)
        derived_bound = MathTex(
            r"9-2a\ge5",
            r"\Longrightarrow",
            r"a\le2",
            font_size=37,
            color=INK,
        )
        derived_bound[0].set_color(PURPLE)
        derived_bound[2].set_color(BLUE)
        allowed_interval = MathTex(r"1\le a\le2", font_size=54, color=REGION)
        allowed_panel = VGroup(
            MathTex("b=9-2a", font_size=41, color=INK),
            a_bound,
            b_bound,
            derived_bound,
            allowed_interval,
        ).arrange(DOWN, buff=0.38)
        allowed_panel.move_to([4.30, -0.14, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    axes,
                    axis_labels,
                    triangle,
                    vertex_dots,
                    vertex_names,
                    g_dot,
                    g_label,
                    moving_line,
                    moving_equation,
                    constraint_panel,
                )
            ),
            Create(coefficient_axes),
            FadeIn(coefficient_labels),
            run_time=0.9,
        )
        self.play(Create(coefficient_line), FadeIn(allowed_panel[0]), run_time=0.75)
        self.play(Create(boundary_a), FadeIn(a_bound), run_time=0.65)
        self.play(Create(boundary_b), FadeIn(b_bound), run_time=0.65)

        self.next_beat("form_allowed_interval")
        self.play(FadeIn(derived_bound), run_time=0.8)
        self.play(Create(valid_segment), FadeIn(endpoint_dots), FadeIn(endpoint_labels), run_time=0.85)
        self.play(FadeIn(allowed_interval), Circumscribe(valid_segment, color=REGION), run_time=0.8)
        self.wait(0.35)

        # Beat 06 watch_weighted_squares: compare two growing a-squares with one shrinking b-square.
        self.next_beat("watch_weighted_squares")
        next_title = label("先看三塊面積怎麼變", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        square_a_tracker = ValueTracker(1.0)
        large_square = always_redraw(
            lambda: VGroup(
                Square(
                    side_length=0.45 * (9 - 2 * square_a_tracker.get_value()),
                    color=PURPLE,
                    stroke_width=4,
                    fill_color=PURPLE,
                    fill_opacity=0.16,
                ),
                MathTex("b^2", font_size=37, color=PURPLE),
            ).move_to([-4.25, -0.20, 0])
        )
        first_small_square = always_redraw(
            lambda: VGroup(
                Square(
                    side_length=0.52 * square_a_tracker.get_value(),
                    color=BLUE,
                    stroke_width=4,
                    fill_color=BLUE,
                    fill_opacity=0.18,
                ),
                MathTex("a^2", font_size=28, color=BLUE),
            ).move_to([-1.85, 0.85, 0])
        )
        second_small_square = always_redraw(
            lambda: VGroup(
                Square(
                    side_length=0.52 * square_a_tracker.get_value(),
                    color=BLUE,
                    stroke_width=4,
                    fill_color=BLUE,
                    fill_opacity=0.18,
                ),
                MathTex("a^2", font_size=28, color=BLUE),
            ).move_to([-0.70, 0.85, 0])
        )
        square_number_line = NumberLine(
            x_range=[1, 2, 0.5],
            length=4.65,
            color=MUTED,
            stroke_width=2.4,
            include_numbers=True,
            font_size=24,
        ).move_to([-2.60, -2.95, 0])
        number_dot = always_redraw(
            lambda: Dot(
                square_number_line.n2p(square_a_tracker.get_value()),
                radius=0.095,
                color=POINT,
            ).set_z_index(8)
        )
        square_a_value = always_redraw(
            lambda: VGroup(
                MathTex("a=", font_size=36, color=BLUE),
                DecimalNumber(
                    square_a_tracker.get_value(),
                    num_decimal_places=2,
                    font_size=36,
                    color=BLUE,
                ),
            ).arrange(RIGHT, buff=0.12).move_to([4.25, -0.70, 0])
        )
        square_b_value = always_redraw(
            lambda: VGroup(
                MathTex("b=", font_size=36, color=PURPLE),
                DecimalNumber(
                    9 - 2 * square_a_tracker.get_value(),
                    num_decimal_places=2,
                    font_size=36,
                    color=PURPLE,
                ),
            ).arrange(RIGHT, buff=0.12).move_to([4.25, -1.30, 0])
        )
        square_relation = MathTex("b=9-2a", font_size=39, color=INK)
        square_relation.move_to([4.25, 0.05, 0])
        square_objective = self.colored_objective(50)
        square_objective.move_to([4.25, 1.18, 0])
        square_question = label("總面積往哪一邊變？", 28, POINT, "BOLD")
        square_question.move_to([4.25, -2.30, 0])
        square_scale_note = label("同一個長度比例", 24, MUTED, "MEDIUM")
        square_scale_note.move_to([4.25, 2.15, 0])
        square_panel = VGroup(
            square_scale_note,
            square_objective,
            square_relation,
            square_a_value,
            square_b_value,
            square_question,
        )
        square_scene = VGroup(
            large_square,
            first_small_square,
            second_small_square,
            square_number_line,
            number_dot,
        )

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    coefficient_axes,
                    coefficient_labels,
                    coefficient_line,
                    boundary_a,
                    boundary_b,
                    valid_segment,
                    endpoint_dots,
                    endpoint_labels,
                    allowed_panel,
                )
            ),
            FadeIn(square_number_line),
            run_time=0.8,
        )
        self.play(GrowFromCenter(large_square), GrowFromCenter(first_small_square), GrowFromCenter(second_small_square), run_time=0.9)
        self.play(FadeIn(number_dot), LaggedStart(*(FadeIn(item) for item in square_panel), lag_ratio=0.12), run_time=0.8)

        self.next_beat("explore_weighted_squares")
        self.play(square_a_tracker.animate.set_value(1.5), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.play(square_a_tracker.animate.set_value(2.0), run_time=1.3, rate_func=rate_functions.ease_in_out_sine)
        self.play(square_a_tracker.animate.set_value(1.5), run_time=1.15, rate_func=rate_functions.ease_in_out_sine)
        self.wait(0.4)

        # Beat 07 compress_objective: stop the geometry and build one-variable algebra from it.
        self.next_beat("compress_objective")
        next_title = label("圖形停下來，再逐行壓成代數", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        formula_one = MathTex("f(a)", "=", "2a^2", "+", "b^2", font_size=40, color=INK)
        formula_one[2].set_color(BLUE)
        formula_one[4].set_color(PURPLE)
        formula_two = MathTex("=", "2a^2", "+", "(9-2a)^2", font_size=40, color=INK)
        formula_two[1].set_color(BLUE)
        formula_two[3].set_color(PURPLE)
        formula_three = MathTex("=6a^2-36a+81", font_size=40, color=INK)
        formula_four = MathTex("=6(a-3)^2+27", font_size=48, color=REGION)
        formula_stack = VGroup(formula_one, formula_two, formula_three, formula_four).arrange(
            DOWN, aligned_edge=LEFT, buff=0.42
        )
        formula_stack.move_to([4.25, -0.14, 0])
        algebra_note = label("現在只剩一個變數 a", 25, MUTED, "MEDIUM")
        algebra_note.next_to(formula_stack, DOWN, buff=0.46)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(VGroup(square_panel, number_dot)), run_time=0.45)
        self.play(FadeIn(formula_one), run_time=0.75)
        self.play(FadeIn(formula_two), run_time=0.8)

        self.next_beat("finish_objective_compression")
        self.play(FadeIn(formula_three), run_time=0.75)
        self.play(FadeIn(formula_four), run_time=0.85)
        self.play(FadeIn(algebra_note), Circumscribe(formula_four, color=REGION), run_time=0.8)
        self.wait(0.35)

        # Beat 08 prove_decreasing: show the vertex outside the interval and track the falling point.
        self.next_beat("prove_decreasing")
        next_title = label("允許區間在頂點的左邊", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        graph_axes = Axes(
            x_range=[0.5, 3.5, 0.5],
            y_range=[25, 55, 5],
            x_length=6.15,
            y_length=5.65,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": True,
                "include_ticks": True,
            },
            tips=True,
        ).move_to([-3.45, -0.22, 0])
        graph_labels = VGroup(
            MathTex("a", font_size=26, color=BLUE).next_to(
                graph_axes.x_axis.get_end(), DOWN, buff=0.08
            ),
            MathTex("f(a)", font_size=26, color=POINT).next_to(
                graph_axes.y_axis.get_end(), LEFT, buff=0.08
            ),
        )
        parabola = graph_axes.plot(
            lambda x: 6 * (x - 3) ** 2 + 27,
            x_range=[0.88, 3.38],
            color=MUTED,
            stroke_width=3.2,
        )
        allowed_curve = graph_axes.plot(
            lambda x: 6 * (x - 3) ** 2 + 27,
            x_range=[1, 2],
            color=REGION,
            stroke_width=8,
        ).set_z_index(5)
        vertex_dot = Dot(graph_axes.c2p(3, 27), radius=0.105, color=CORAL).set_z_index(7)
        vertex_graph_label = MathTex("(3,27)", font_size=26, color=CORAL).next_to(
            vertex_dot, UP + RIGHT, buff=0.16
        )
        graph_a_tracker = ValueTracker(1.0)
        graph_dot = always_redraw(
            lambda: Dot(
                graph_axes.c2p(
                    graph_a_tracker.get_value(),
                    6 * (graph_a_tracker.get_value() - 3) ** 2 + 27,
                ),
                radius=0.105,
                color=POINT,
            ).set_z_index(9)
        )
        distance_bar = always_redraw(
            lambda: Line(
                graph_axes.c2p(graph_a_tracker.get_value(), 27.8),
                graph_axes.c2p(3, 27.8),
                color=BLUE,
                stroke_width=6,
            ).set_z_index(6)
        )
        distance_label = always_redraw(
            lambda: MathTex("3-a", font_size=26, color=BLUE).next_to(
                distance_bar, UP, buff=0.10
            )
        )
        graph_formula = MathTex("f(a)=6(a-3)^2+27", font_size=42, color=REGION)
        interval_formula = MathTex(r"1\le a\le2<3", font_size=42, color=INK)
        distance_note = VGroup(
            label("a 往右走", 26, BLUE, "BOLD"),
            label("到 3 的距離變短", 27, INK, "BOLD"),
            label("所以 f(a) 嚴格下降", 29, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.32)
        graph_panel = VGroup(graph_formula, interval_formula, distance_note).arrange(DOWN, buff=0.52)
        graph_panel.move_to([4.28, -0.10, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    square_scene,
                    formula_stack,
                    algebra_note,
                )
            ),
            Create(graph_axes),
            FadeIn(graph_labels),
            run_time=0.85,
        )
        self.play(Create(parabola), FadeIn(vertex_dot), FadeIn(vertex_graph_label), run_time=0.8)
        self.play(Create(allowed_curve), FadeIn(graph_dot), FadeIn(distance_bar), FadeIn(distance_label), run_time=0.75)
        self.play(LaggedStart(*(FadeIn(item) for item in graph_panel), lag_ratio=0.14), run_time=0.9)

        self.next_beat("trace_decreasing_interval")
        self.play(graph_a_tracker.animate.set_value(1.5), run_time=1.25, rate_func=rate_functions.ease_in_out_sine)
        self.play(graph_a_tracker.animate.set_value(2.0), run_time=1.25, rate_func=rate_functions.ease_in_out_sine)
        self.play(Indicate(allowed_curve, color=REGION), run_time=0.65)
        self.wait(0.4)

        # Beat 09 evaluate_endpoints: calculate only the two endpoint values.
        self.next_beat("evaluate_endpoints")
        next_title = label("嚴格下降，所以只算兩個端點", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        middle_rule = Line([0, -2.75, 0], [0, 2.35, 0], color=HAIRLINE, stroke_width=1.5)
        left_state = MathTex("(a,b)=(1,7)", font_size=41, color=INK)
        left_state[0][1].set_color(BLUE)
        left_state[0][3].set_color(PURPLE)
        left_calculation = MathTex(
            "2(1)^2",
            "+",
            "7^2",
            "=",
            "51",
            font_size=46,
            color=INK,
        )
        left_calculation[0].set_color(BLUE)
        left_calculation[2].set_color(PURPLE)
        left_calculation[4].set_color(POINT)
        left_caption = label("左端", 27, MUTED, "BOLD")
        left_endpoint_panel = VGroup(left_caption, left_state, left_calculation).arrange(DOWN, buff=0.55)
        left_endpoint_panel.move_to([-3.75, -0.20, 0])
        right_state = MathTex("(a,b)=(2,5)", font_size=41, color=INK)
        right_state[0][1].set_color(BLUE)
        right_state[0][3].set_color(PURPLE)
        right_calculation = MathTex(
            "2(2)^2",
            "+",
            "5^2",
            "=",
            "33",
            font_size=46,
            color=INK,
        )
        right_calculation[0].set_color(BLUE)
        right_calculation[2].set_color(PURPLE)
        right_calculation[4].set_color(POINT)
        right_caption = label("右端", 27, MUTED, "BOLD")
        right_endpoint_panel = VGroup(right_caption, right_state, right_calculation).arrange(DOWN, buff=0.55)
        right_endpoint_panel.move_to([3.75, -0.20, 0])
        endpoint_reason = VGroup(
            MathTex("f(a)", font_size=35, color=REGION),
            label("在", 27, INK, "MEDIUM"),
            MathTex("[1,2]", font_size=35, color=BLUE),
            label("嚴格下降", 27, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.18)
        endpoint_reason.move_to([0, 2.65, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    divider,
                    graph_axes,
                    graph_labels,
                    parabola,
                    allowed_curve,
                    vertex_dot,
                    vertex_graph_label,
                    graph_dot,
                    distance_bar,
                    distance_label,
                    graph_panel,
                )
            ),
            FadeIn(middle_rule),
            FadeIn(endpoint_reason),
            run_time=0.8,
        )
        self.play(FadeIn(left_caption), FadeIn(left_state), run_time=0.6)
        self.play(FadeIn(left_calculation), run_time=0.75)

        self.next_beat("evaluate_right_endpoint")
        self.play(FadeIn(right_caption), FadeIn(right_state), run_time=0.6)
        self.play(FadeIn(right_calculation), run_time=0.75)
        self.wait(0.4)

        # Beat 10 hold_ordered_pair: assign maximum and minimum but withhold the ordered pair.
        self.next_beat("hold_ordered_pair")
        next_title = label("最大值在左端，最小值在右端", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        max_value = MathTex("M=51", font_size=54, color=POINT)
        min_value = MathTex("m=33", font_size=54, color=REGION)
        ordered_pair_question = MathTex(
            "(M,m)", "=", r"(\,?\,,\,?\,)", font_size=62, color=INK
        )
        order_note = label("第一格放最大值，第二格放最小值", 29, MUTED, "MEDIUM")
        preanswer_panel = VGroup(max_value, min_value, ordered_pair_question, order_note).arrange(
            DOWN, buff=0.52
        )
        preanswer_panel.move_to([0, -0.25, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(VGroup(middle_rule, endpoint_reason, left_endpoint_panel, right_endpoint_panel)), run_time=0.65)
        self.play(FadeIn(max_value), run_time=0.55)
        self.play(FadeIn(min_value), run_time=0.55)
        self.play(FadeIn(ordered_pair_question), FadeIn(order_note), run_time=0.7)
        self.wait(0.55)

        # Beat 11 reveal_ordered_pair: reveal the ordered answer and reconnect both boundary lines.
        self.next_beat("reveal_ordered_pair")
        next_title = label("把端點依順序放回答案", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        final_answer = MathTex(
            "(M,m)", "=", "(", "51", ",", "33", ")", font_size=62, color=INK
        )
        final_answer[3].set_color(POINT)
        final_answer[5].set_color(REGION)
        final_box = SurroundingRectangle(final_answer, color=REGION, buff=0.30, stroke_width=4)
        final_group = VGroup(final_answer, final_box).move_to([4.15, -0.12, 0])
        final_max_line = axes.plot(
            lambda x: (9 - x) / 7,
            x_range=[-3, 8],
            color=POINT,
            stroke_width=4.5,
        ).set_z_index(5)
        final_min_line = axes.plot(
            lambda x: (9 - 2 * x) / 5,
            x_range=[-3, 8],
            color=REGION,
            stroke_width=4.5,
        ).set_z_index(5)
        final_line_labels = VGroup(
            MathTex("(a,b)=(1,7)", font_size=25, color=POINT).move_to([-2.05, 2.55, 0]),
            MathTex("(a,b)=(2,5)", font_size=25, color=REGION).move_to([-1.65, -2.72, 0]),
        )
        final_note = VGroup(
            label("兩個允許端點", 25, MUTED, "MEDIUM"),
            label("對應最大值與最小值", 27, INK, "BOLD"),
        ).arrange(DOWN, buff=0.25)
        final_note.next_to(final_group, DOWN, buff=0.58)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(VGroup(max_value, min_value, order_note)),
            FadeIn(divider),
            FadeIn(axes),
            FadeIn(axis_labels),
            FadeIn(triangle),
            FadeIn(vertex_dots),
            FadeIn(vertex_names),
            FadeIn(g_dot),
            FadeIn(g_label),
            run_time=0.85,
        )
        self.play(Create(final_max_line), Create(final_min_line), FadeIn(final_line_labels), run_time=0.85)
        self.play(
            Succession(FadeOut(ordered_pair_question), FadeIn(final_answer)),
            run_time=0.7,
        )
        self.play(Create(final_box), FadeIn(final_note), Indicate(g_dot, color=REGION), run_time=0.7)
        self.wait(0.55)
