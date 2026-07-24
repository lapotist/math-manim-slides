"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q7."""

from __future__ import annotations

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
    Axes,
    Circle,
    Circumscribe,
    Create,
    Cross,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Succession,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


def quadratic(x: float) -> float:
    """Evaluate the quadratic from the problem."""
    return x * x - 6 * x + 12


def interval_extrema(a: float, b: float) -> tuple[float, float]:
    """Return the exact extrema candidates on one closed interval."""
    values = [quadratic(a), quadratic(b)]
    if a <= 3 <= b:
        values.append(quadratic(3))
    return min(values), max(values)


FIXED_POINTS = tuple(x for x in range(-20, 21) if quadratic(x) == x)

if FIXED_POINTS != (3, 4):
    raise ValueError(f"unexpected integral fixed points: {FIXED_POINTS}")
if interval_extrema(3, 4) != (3, 4):
    raise ValueError("[3,4] is not preserved by the quadratic")
if not (interval_extrema(0.9, 2.3)[0] > 3 > 0.9):
    raise ValueError("left-branch rejection check failed")
if interval_extrema(1.5, 4.7)[0] != 3:
    raise ValueError("straddling-interval minimum check failed")


class CarloTcfs113MathQ07(CarloSlide):
    """Discover the only interval preserved by the quadratic."""

    lesson_id = "carlo.tcfs_113_math_gifted.q07"

    @staticmethod
    def coordinate_system() -> tuple[Axes, VGroup]:
        """Build one stable coordinate system for all ten beats."""
        axes = Axes(
            x_range=[0, 6, 1],
            y_range=[0, 9, 1],
            x_length=7.50,
            y_length=5.90,
            axis_config={
                "color": MUTED,
                "stroke_width": 2.1,
                "include_tip": True,
                "include_ticks": True,
            },
            tips=True,
        ).move_to([-3.30, -0.30, 0])
        axis_labels = VGroup(
            MathTex("x", font_size=25, color=MUTED).next_to(
                axes.x_axis.get_end(), DOWN, buff=0.08
            ),
            MathTex("y", font_size=25, color=MUTED).next_to(
                axes.y_axis.get_end(), LEFT, buff=0.08
            ),
        )
        return axes, axis_labels

    @staticmethod
    def interval_model(
        axes: Axes,
        a: float,
        b: float,
        *,
        left_tex: str = "a",
        right_tex: str = "b",
    ) -> VGroup:
        """Draw the same domain interval and its two endpoint images."""
        domain_y = 0.34
        curve_segment = axes.plot(
            quadratic,
            x_range=[a, b],
            color=PURPLE,
            stroke_width=7,
        ).set_z_index(3)
        domain = Line(
            axes.c2p(a, domain_y),
            axes.c2p(b, domain_y),
            color=INK,
            stroke_width=7,
        ).set_z_index(4)
        left_domain = Dot(axes.c2p(a, domain_y), radius=0.085, color=POINT).set_z_index(6)
        right_domain = Dot(axes.c2p(b, domain_y), radius=0.085, color=CORAL).set_z_index(6)
        left_label = MathTex(left_tex, font_size=31, color=POINT).next_to(
            left_domain, DOWN, buff=0.12
        )
        right_label = MathTex(right_tex, font_size=31, color=CORAL).next_to(
            right_domain, DOWN, buff=0.12
        )
        left_guide = DashedLine(
            axes.c2p(a, domain_y),
            axes.c2p(a, quadratic(a)),
            color=POINT,
            dash_length=0.10,
            stroke_width=2.2,
        ).set_opacity(0.72)
        right_guide = DashedLine(
            axes.c2p(b, domain_y),
            axes.c2p(b, quadratic(b)),
            color=CORAL,
            dash_length=0.10,
            stroke_width=2.2,
        ).set_opacity(0.72)
        left_image = Dot(
            axes.c2p(a, quadratic(a)), radius=0.09, color=POINT
        ).set_z_index(7)
        right_image = Dot(
            axes.c2p(b, quadratic(b)), radius=0.09, color=CORAL
        ).set_z_index(7)
        return VGroup(
            curve_segment,
            domain,
            left_domain,
            right_domain,
            left_label,
            right_label,
            left_guide,
            right_guide,
            left_image,
            right_image,
        )

    @staticmethod
    def rejected_case(tex: str) -> VGroup:
        """Show one positional case with an explicit rejection mark."""
        formula = MathTex(tex, font_size=34, color=MUTED)
        cross = Cross(formula, stroke_color=CORAL, stroke_width=4.5)
        return VGroup(formula, cross)

    @staticmethod
    def number_chip(value: int, color: str) -> VGroup:
        """Create a movable fixed-point candidate."""
        ring = Circle(
            radius=0.42,
            stroke_color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.08,
        )
        number = MathTex(str(value), font_size=43, color=color).move_to(ring)
        return VGroup(ring, number)

    def construct(self) -> None:
        heading = label("第 7 題｜被二次函數保留下來的區間", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 7 頁｜影片 xRrA7_xEStU 00:00-03:31",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.82, -3.52, 0], [0.82, 3.42, 0], color=HAIRLINE, stroke_width=1.5)

        axes, axis_labels = self.coordinate_system()
        parabola = axes.plot(
            quadratic,
            x_range=[0.55, 5.45],
            color=BLUE,
            stroke_width=5,
        )
        curve_formula = MathTex(r"y=(x-3)^2+3", font_size=36, color=BLUE)
        curve_formula.move_to([-3.35, 3.15, 0])
        floor = DashedLine(
            axes.c2p(0.25, 3),
            axes.c2p(5.75, 3),
            color=REGION,
            dash_length=0.11,
            stroke_width=2.2,
        ).set_opacity(0.65)
        vertex = Dot(axes.c2p(3, 3), radius=0.10, color=REGION).set_z_index(8)
        vertex_label = MathTex("(3,3)", font_size=27, color=REGION)
        vertex_label.next_to(vertex, DOWN + RIGHT, buff=0.12)

        # Beat 01: reveal the global floor before moving an interval.
        self.begin_beat("reveal_vertex_form")
        stage_title = label("先看拋物線的最低點", 33, INK, "BOLD")
        stage_title.move_to([4.30, 3.02, 0])
        square_nonnegative = MathTex(r"(x-3)^2\ge0", font_size=43, color=REGION)
        global_floor = MathTex(r"f(x)\ge3", font_size=49, color=REGION)
        interval_condition = MathTex("0<a<b", font_size=42, color=INK)
        interval_note = label("放上一個正數區間", 26, INK, "BOLD")
        minimum_row = VGroup(
            label("題目指定最低值", 24, MUTED, "MEDIUM"),
            MathTex("a", font_size=39, color=POINT),
        ).arrange(RIGHT, buff=0.25)
        maximum_row = VGroup(
            label("題目指定最大值", 24, MUTED, "MEDIUM"),
            MathTex("b", font_size=39, color=CORAL),
        ).arrange(RIGHT, buff=0.25)
        opening_question = label("區間可以放在哪裡？", 27, CORAL, "BOLD")
        opening_side = VGroup(
            square_nonnegative,
            global_floor,
            interval_note,
            interval_condition,
            minimum_row,
            maximum_row,
            opening_question,
        ).arrange(DOWN, buff=0.28)
        opening_side.move_to([4.30, -0.25, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Create(axes), FadeIn(axis_labels), run_time=0.85)
        self.play(Create(parabola), FadeIn(curve_formula), run_time=1.25)
        self.play(Create(floor), GrowFromCenter(vertex), FadeIn(vertex_label), run_time=0.75)
        self.play(Write(square_nonnegative), run_time=0.55)
        self.play(TransformFromCopy(square_nonnegative, global_floor), run_time=0.65)
        self.play(
            LaggedStart(
                FadeIn(interval_note),
                FadeIn(interval_condition),
                FadeIn(minimum_row),
                FadeIn(maximum_row),
                FadeIn(opening_question),
                lag_ratio=0.12,
            ),
            run_time=1.0,
        )
        self.wait(0.35)

        # Beat 02: test an interval wholly left of the vertex.
        self.next_beat("test_left_interval")
        next_title = label("情況一｜整段都在 3 左邊", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        left_interval = self.interval_model(axes, 0.90, 2.30)
        left_condition = MathTex("0<a<b<3", font_size=44, color=INK)
        left_motion = label("從左往右，曲線一路下降", 25, MUTED, "MEDIUM")
        left_minimum = MathTex(r"\min f=f(b)>3>a", font_size=42, color=INK)
        left_minimum[0].set_color(CORAL)
        left_failure = MathTex(r"\min f\ne a", font_size=48, color=CORAL)
        left_panel = VGroup(
            left_condition,
            left_motion,
            left_minimum,
            left_failure,
        ).arrange(DOWN, buff=0.50)
        left_panel.move_to([4.30, -0.10, 0])

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(opening_side),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(
            Create(left_interval[0]),
            Create(left_interval[1]),
            FadeIn(VGroup(*left_interval[2:])),
            run_time=1.0,
        )
        self.play(FadeIn(left_condition), FadeIn(left_motion), run_time=0.6)
        self.play(Write(left_minimum), run_time=0.75)
        self.play(FadeIn(left_failure), Circumscribe(left_failure, color=CORAL), run_time=0.75)
        self.wait(0.35)

        # Beat 03: move the same interval so it contains the vertex.
        self.next_beat("test_straddling_interval")
        next_title = label("情況二｜區間碰到最低點", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        straddling_interval = self.interval_model(axes, 1.50, 4.70)
        straddle_condition = MathTex(r"0<a<3\le b", font_size=44, color=INK)
        straddle_motion = label("最低點落進區間裡", 25, MUTED, "MEDIUM")
        straddle_minimum = MathTex(r"\min f=f(3)=3>a", font_size=42, color=INK)
        straddle_minimum[0].set_color(REGION)
        straddle_failure = MathTex(r"\min f\ne a", font_size=48, color=CORAL)
        straddle_panel = VGroup(
            straddle_condition,
            straddle_motion,
            straddle_minimum,
            straddle_failure,
        ).arrange(DOWN, buff=0.50)
        straddle_panel.move_to([4.30, -0.10, 0])

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            Transform(left_interval, straddling_interval),
            Succession(FadeOut(left_condition), FadeIn(straddle_condition)),
            FadeOut(VGroup(left_motion, left_minimum, left_failure)),
            run_time=1.0,
        )
        stage_title = next_title
        self.play(Indicate(vertex, color=REGION, scale_factor=1.7), FadeIn(straddle_motion), run_time=0.75)
        self.play(Write(straddle_minimum), run_time=0.75)
        self.play(
            FadeIn(straddle_failure),
            Circumscribe(straddle_failure, color=CORAL),
            run_time=0.75,
        )
        self.wait(0.35)

        # Beat 04: reject every a<3 position and keep the increasing branch.
        self.next_beat("settle_right_branch")
        next_title = label("只剩情況三｜整段在右半邊", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        right_interval = self.interval_model(axes, 3.35, 4.70)
        rejected_left = self.rejected_case("0<a<b<3")
        rejected_straddle = self.rejected_case(r"0<a<3\le b")
        survivor = MathTex(r"3\le a<b", font_size=43, color=REGION)
        necessary = MathTex(r"a\ge3", font_size=54, color=REGION)
        case_panel = VGroup(
            rejected_left,
            rejected_straddle,
            survivor,
            necessary,
        ).arrange(DOWN, buff=0.42)
        case_panel.move_to([4.30, -0.12, 0])

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            Transform(left_interval, right_interval),
            FadeOut(straddle_panel),
            run_time=1.0,
        )
        stage_title = next_title
        self.play(
            LaggedStart(
                FadeIn(rejected_left),
                FadeIn(rejected_straddle),
                FadeIn(survivor),
                lag_ratio=0.16,
            ),
            run_time=0.9,
        )
        self.play(TransformFromCopy(survivor, necessary), run_time=0.65)
        self.play(Circumscribe(necessary, color=REGION), run_time=0.75)
        self.wait(0.35)

        # Beat 05: connect each endpoint to the corresponding extremum.
        self.next_beat("connect_endpoint_extrema")
        next_title = label("右半邊從左到右一路上升", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        fa_label = MathTex("f(a)", font_size=31, color=POINT)
        fa_label.next_to(left_interval[8], LEFT + UP, buff=0.12)
        fb_label = MathTex("f(b)", font_size=31, color=CORAL)
        fb_label.next_to(left_interval[9], RIGHT + UP, buff=0.12)
        rise_arrow = Arrow(
            [2.25, 1.45, 0],
            [6.30, 1.45, 0],
            color=PURPLE,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.07,
        )
        rise_note = label("高度持續增加", 24, PURPLE, "BOLD")
        rise_note.next_to(rise_arrow, UP, buff=0.12)
        actual_min = VGroup(
            MathTex("f(a)", font_size=46, color=POINT),
            label("實際最低值", 25, INK, "BOLD"),
        ).arrange(DOWN, buff=0.18)
        actual_max = VGroup(
            MathTex("f(b)", font_size=46, color=CORAL),
            label("實際最大值", 25, INK, "BOLD"),
        ).arrange(DOWN, buff=0.18)
        endpoint_roles = VGroup(actual_min, actual_max).arrange(RIGHT, buff=1.20)
        endpoint_roles.move_to([4.30, -0.35, 0])
        role_panel = VGroup(rise_arrow, rise_note, endpoint_roles)

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(case_panel),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(FadeIn(fa_label), FadeIn(fb_label), run_time=0.55)
        self.play(Create(rise_arrow), FadeIn(rise_note), run_time=0.7)
        self.play(
            TransformFromCopy(fa_label, actual_min[0]),
            TransformFromCopy(fb_label, actual_max[0]),
            FadeIn(actual_min[1]),
            FadeIn(actual_max[1]),
            run_time=0.85,
        )
        self.wait(0.35)

        # Beat 06: match actual extrema with the names required by the problem.
        self.next_beat("earn_fixed_endpoint_equations")
        next_title = label("同一個極值，必須對上同一個數", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        given_caption = label("題目指定的名字", 24, MUTED, "MEDIUM")
        given_a = MathTex("a", font_size=46, color=POINT)
        given_b = MathTex("b", font_size=46, color=CORAL)
        given_min = VGroup(label("最低值", 24, INK, "BOLD"), given_a).arrange(RIGHT, buff=0.25)
        given_max = VGroup(label("最大值", 24, INK, "BOLD"), given_b).arrange(RIGHT, buff=0.25)
        given_caption.move_to([4.30, 1.20, 0])
        given_min.move_to([3.10, 0.42, 0])
        given_max.move_to([5.50, 0.42, 0])
        given_names = VGroup(given_caption, given_min, given_max)
        min_equation = MathTex("f(a)", "=", "a", font_size=49, color=INK)
        min_equation[0].set_color(POINT)
        min_equation[2].set_color(POINT)
        max_equation = MathTex("f(b)", "=", "b", font_size=49, color=INK)
        max_equation[0].set_color(CORAL)
        max_equation[2].set_color(CORAL)
        min_equation.move_to([3.10, -1.12, 0])
        max_equation.move_to([5.50, -1.12, 0])
        fixed_equations = VGroup(min_equation, max_equation)

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(role_panel),
            FadeIn(given_names),
            run_time=0.75,
        )
        stage_title = next_title
        self.play(
            TransformFromCopy(fa_label, min_equation[0]),
            TransformFromCopy(given_a, min_equation[2]),
            FadeIn(min_equation[1]),
            run_time=0.75,
        )
        self.play(
            TransformFromCopy(fb_label, max_equation[0]),
            TransformFromCopy(given_b, max_equation[2]),
            FadeIn(max_equation[1]),
            run_time=0.75,
        )
        self.play(Circumscribe(fixed_equations, color=REGION), run_time=0.8)
        self.wait(0.35)

        # Beat 07: translate fixed-point equations into graph intersections.
        self.next_beat("locate_fixed_points")
        next_title = label("輸入與輸出相同，圖上在哪裡？", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        identity_line = axes.plot(
            lambda x: x,
            x_range=[0.35, 5.60],
            color=PURPLE,
            stroke_width=4,
        )
        identity_label = MathTex("y=x", font_size=30, color=PURPLE)
        identity_label.move_to(axes.c2p(5.22, 5.65))
        intersection_rings = VGroup(
            Circle(radius=0.13, color=POINT, stroke_width=4).move_to(axes.c2p(3, 3)),
            Circle(radius=0.13, color=CORAL, stroke_width=4).move_to(axes.c2p(4, 4)),
        ).set_z_index(10)
        question_marks = VGroup(
            MathTex("?", font_size=30, color=POINT).next_to(
                axes.c2p(3, 3), LEFT + UP, buff=0.12
            ),
            MathTex("?", font_size=30, color=CORAL).next_to(
                axes.c2p(4, 4), RIGHT + UP, buff=0.12
            ),
        )
        fixed_prompt = MathTex("f(x)=x", font_size=53, color=INK)
        fixed_prompt.move_to([4.30, 0.55, 0])
        prompt_note = label("兩條曲線同高的地方", 26, PURPLE, "BOLD")
        prompt_note.move_to([4.30, -0.48, 0])
        prompt_question = label("兩個橫座標各是多少？", 25, CORAL, "BOLD")
        prompt_question.move_to([4.30, -1.48, 0])
        fixed_panel = VGroup(fixed_prompt, prompt_note, prompt_question)

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(given_names),
            FadeOut(fixed_equations),
            left_interval.animate.set_opacity(0.20),
            FadeOut(fa_label),
            FadeOut(fb_label),
            FadeOut(vertex_label),
            run_time=0.75,
        )
        stage_title = next_title
        self.play(Write(fixed_prompt), FadeIn(prompt_note), run_time=0.65)
        self.play(Create(identity_line), FadeIn(identity_label), run_time=0.9)
        self.play(
            LaggedStart(*(GrowFromCenter(ring) for ring in intersection_rings), lag_ratio=0.24),
            FadeIn(question_marks),
            FadeIn(prompt_question),
            run_time=0.8,
        )
        self.wait(0.35)

        # Beat 08: solve the intersection equation only after the graph motivates it.
        self.next_beat("solve_fixed_points")
        next_title = label("把兩個交點算準", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        equation_zero = MathTex("f(x)=x", font_size=38, color=INK)
        equation_one = MathTex(r"x^2-6x+12=x", font_size=38, color=INK)
        equation_two = MathTex(r"x^2-7x+12=0", font_size=38, color=INK)
        equation_three = MathTex(r"(x-3)(x-4)=0", font_size=38, color=INK)
        equation_four = MathTex(r"x\in\{3,4\}", font_size=43, color=REGION)
        derivation = VGroup(
            equation_zero,
            equation_one,
            equation_two,
            equation_three,
            equation_four,
        ).arrange(DOWN, buff=0.30)
        derivation.move_to([4.30, -0.18, 0])
        root_labels = VGroup(
            MathTex("(3,3)", font_size=28, color=POINT).next_to(
                axes.c2p(3, 3), LEFT + UP, buff=0.12
            ),
            MathTex("(4,4)", font_size=28, color=CORAL).next_to(
                axes.c2p(4, 4), RIGHT + UP, buff=0.12
            ),
        )

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(fixed_panel),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Write(equation_zero), run_time=0.45)
        self.play(Write(equation_one), run_time=0.65)
        self.play(Write(equation_two), run_time=0.65)
        self.play(Write(equation_three), run_time=0.65)
        self.play(Write(equation_four), run_time=0.55)
        self.play(
            Succession(FadeOut(question_marks[0]), FadeIn(root_labels[0])),
            Succession(FadeOut(question_marks[1]), FadeIn(root_labels[1])),
            run_time=0.7,
        )
        self.wait(0.35)

        # Beat 09: use a<b to assign the two candidates in one order.
        self.next_beat("assign_ordered_endpoints")
        next_title = label("兩個候選值，次序只有一種", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        order_condition = MathTex("a<b", font_size=49, color=INK)
        order_condition.move_to([4.30, 1.70, 0])
        three_chip = self.number_chip(3, POINT).move_to([3.15, 0.55, 0])
        four_chip = self.number_chip(4, CORAL).move_to([5.45, 0.55, 0])
        numeric_order = MathTex("3<4", font_size=38, color=MUTED)
        numeric_order.move_to([4.30, 0.55, 0])
        assign_a = MathTex("a=3", font_size=46, color=POINT).move_to([3.15, -0.90, 0])
        assign_b = MathTex("b=4", font_size=46, color=CORAL).move_to([5.45, -0.90, 0])
        arrow_a = Arrow(
            three_chip.get_bottom(),
            assign_a.get_top(),
            color=POINT,
            buff=0.12,
            stroke_width=3.5,
        )
        arrow_b = Arrow(
            four_chip.get_bottom(),
            assign_b.get_top(),
            color=CORAL,
            buff=0.12,
            stroke_width=3.5,
        )
        ordered_pair = MathTex(r"(a,b)=(3,4)", font_size=50, color=REGION)
        ordered_pair.move_to([4.30, -2.15, 0])
        assignment_panel = VGroup(
            order_condition,
            three_chip,
            four_chip,
            numeric_order,
            assign_a,
            assign_b,
            arrow_a,
            arrow_b,
            ordered_pair,
        )

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(derivation),
            FadeIn(order_condition),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(
            GrowFromCenter(three_chip),
            GrowFromCenter(four_chip),
            FadeIn(numeric_order),
            run_time=0.7,
        )
        self.play(
            Create(arrow_a),
            Create(arrow_b),
            TransformFromCopy(three_chip[1], assign_a),
            TransformFromCopy(four_chip[1], assign_b),
            run_time=0.85,
        )
        self.play(Write(ordered_pair), run_time=0.65)
        self.play(Circumscribe(ordered_pair, color=REGION), run_time=0.8)
        self.wait(0.35)

        # Beat 10: verify the entire range, not only the two endpoints.
        self.next_beat("verify_preserved_interval")
        next_title = label("最後檢查整段區間", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        exact_interval = self.interval_model(
            axes,
            3,
            4,
            left_tex="3",
            right_tex="4",
        )
        f3_label = MathTex("f(3)=3", font_size=29, color=POINT)
        f3_label.next_to(axes.c2p(3, 3), LEFT + UP, buff=0.13)
        f4_label = MathTex("f(4)=4", font_size=29, color=CORAL)
        f4_label.next_to(axes.c2p(4, 4), RIGHT + UP, buff=0.13)
        check_zero = MathTex(r"3\le x\le4", font_size=40, color=INK)
        check_one = MathTex(r"0\le x-3\le1", font_size=38, color=INK)
        check_two = MathTex(r"0\le(x-3)^2\le1", font_size=38, color=INK)
        check_three = MathTex(r"3\le f(x)\le4", font_size=43, color=REGION)
        check_lines = VGroup(check_zero, check_one, check_two, check_three).arrange(
            DOWN, buff=0.34
        )
        check_lines.move_to([4.30, 0.42, 0])
        min_check = VGroup(
            label("最低值", 23, MUTED, "MEDIUM"),
            MathTex("3=a", font_size=35, color=POINT),
        ).arrange(RIGHT, buff=0.20)
        max_check = VGroup(
            label("最大值", 23, MUTED, "MEDIUM"),
            MathTex("4=b", font_size=35, color=CORAL),
        ).arrange(RIGHT, buff=0.20)
        extrema_check = VGroup(min_check, max_check).arrange(RIGHT, buff=0.70)
        extrema_check.move_to([4.30, -1.78, 0])
        final_answer = MathTex(r"(a,b)=(3,4)", font_size=49, color=REGION)
        final_answer.move_to([4.30, -2.68, 0])

        self.play(
            Succession(FadeOut(stage_title), FadeIn(next_title)),
            FadeOut(assignment_panel),
            FadeOut(identity_line),
            FadeOut(identity_label),
            FadeOut(intersection_rings),
            FadeOut(root_labels),
            FadeOut(left_interval),
            run_time=1.0,
        )
        self.play(FadeIn(exact_interval), run_time=0.65)
        self.play(FadeIn(f3_label), FadeIn(f4_label), run_time=0.55)
        self.play(Write(check_zero), run_time=0.45)
        self.play(Write(check_one), run_time=0.55)
        self.play(Write(check_two), run_time=0.60)
        self.play(Write(check_three), run_time=0.55)
        self.play(FadeIn(extrema_check), run_time=0.55)
        self.play(Write(final_answer), run_time=0.7)
        self.play(Circumscribe(final_answer, color=REGION), run_time=0.8)
        self.wait(0.45)
