"""Manim Slides lesson for ROC 114 TCFS mathematics gifted fill-in Q2."""

from __future__ import annotations

import math

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    PURPLE,
    REGION,
    WHITE,
    CarloSlide,
    label,
)
from manim import (
    Arrow,
    Axes,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
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
    ReplacementTransform,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class CarloTcfs114MathQ02(CarloSlide):
    """Discover the exact parameter set, repair its endpoint, and minimize."""

    lesson_id = "carlo.tcfs_114_math_gifted.q02"

    @staticmethod
    def value(a: float, x: float) -> float:
        return x * x + a * x + a + 3

    @staticmethod
    def discriminant(a: float) -> float:
        return a * a - 4 * (a + 3)

    @classmethod
    def visible_parabola(
        cls,
        axes: Axes,
        a: float,
        *,
        color: str = POINT,
        stroke_width: float = 5,
    ):
        """Plot the visible portion below a stable top boundary."""
        top = 11.4
        center = -a / 2
        vertex = -cls.discriminant(a) / 4
        reach = math.sqrt(max(top - vertex, 0.05))
        lower = max(-6.0, center - reach)
        upper = min(6.0, center + reach)
        return axes.plot(
            lambda x: cls.value(a, x),
            x_range=[lower, upper, 0.06],
            color=color,
            stroke_width=stroke_width,
            use_smoothing=True,
        )

    @classmethod
    def negative_arc(cls, axes: Axes, a: float) -> VGroup:
        delta = cls.discriminant(a)
        if delta <= 0:
            return VGroup()
        root = math.sqrt(delta)
        left_root = max(-6.0, (-a - root) / 2)
        right_root = min(6.0, (-a + root) / 2)
        if left_root >= right_root:
            return VGroup()
        return VGroup(
            axes.plot(
                lambda x: cls.value(a, x),
                x_range=[left_root, right_root, 0.035],
                color=CORAL,
                stroke_width=9,
                use_smoothing=True,
            )
        )

    @classmethod
    def root_dots(cls, axes: Axes, a: float) -> VGroup:
        delta = cls.discriminant(a)
        if delta <= 0:
            return VGroup()
        root = math.sqrt(delta)
        roots = ((-a - root) / 2, (-a + root) / 2)
        return VGroup(
            *(
                Dot(axes.c2p(x, 0), radius=0.07, color=REGION).set_z_index(8)
                for x in roots
                if -6 <= x <= 6
            )
        )

    @staticmethod
    def quadrant(
        axes: Axes,
        x0: float,
        x1: float,
        y0: float,
        y1: float,
        color: str,
    ) -> Polygon:
        return Polygon(
            axes.c2p(x0, y0),
            axes.c2p(x1, y0),
            axes.c2p(x1, y1),
            axes.c2p(x0, y1),
            stroke_color=HAIRLINE,
            stroke_width=1.2,
            fill_color=color,
            fill_opacity=0.025,
        ).set_z_index(-5)

    @staticmethod
    def open_dot(point, color: str) -> Circle:
        return Circle(radius=0.105, color=color, stroke_width=3).move_to(point)

    def construct(self) -> None:
        heading = label("第 2 題｜三個象限留下哪些 a？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label(
            "解題來源：正哥愛數學｜114 中一中資優班填充第 2 題",
            17,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.24)

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-6, 12, 3],
            x_length=8.35,
            y_length=5.65,
            axis_config={"color": MUTED, "stroke_width": 2.2, "include_tip": True},
            tips=True,
        ).move_to([-3.3, -0.45, 0])
        x_label = MathTex("x", font_size=25, color=MUTED)
        x_label.next_to(axes.x_axis.get_end(), DOWN, buff=0.08)
        y_label = MathTex("y", font_size=25, color=MUTED)
        y_label.next_to(axes.y_axis.get_end(), LEFT, buff=0.08)

        quadrant_colors = (BLUE, PURPLE, CORAL, REGION)
        quadrants = VGroup(
            self.quadrant(axes, 0, 6, 0, 12, quadrant_colors[0]),
            self.quadrant(axes, -6, 0, 0, 12, quadrant_colors[1]),
            self.quadrant(axes, -6, 0, -6, 0, quadrant_colors[2]),
            self.quadrant(axes, 0, 6, -6, 0, quadrant_colors[3]),
        )
        quadrant_labels = VGroup(
            *(
                label(roman, 22, color, "BOLD")
                .move_to(axes.c2p(x, y))
                .set_opacity(0.34)
                for roman, x, y, color in (
                    ("I", 5.3, 10.45, BLUE),
                    ("II", -5.25, 10.45, PURPLE),
                    ("III", -5.1, -4.75, CORAL),
                    ("IV", 5.15, -4.75, REGION),
                )
            )
        )

        a_tracker = ValueTracker(0)
        curve = always_redraw(
            lambda: self.visible_parabola(axes, a_tracker.get_value())
        )
        negative_curve = always_redraw(
            lambda: self.negative_arc(axes, a_tracker.get_value())
        )
        roots = always_redraw(lambda: self.root_dots(axes, a_tracker.get_value()))
        y_intercept = always_redraw(
            lambda: Dot(
                axes.c2p(0, a_tracker.get_value() + 3),
                radius=0.085,
                color=BLUE,
            ).set_z_index(9)
        )

        family = MathTex(
            r"f_a(x)=x^2+ax+(a+3)",
            font_size=39,
            color=INK,
        ).move_to([3.45, 2.25, 0])
        a_display = MathTex("a=0", font_size=49, color=POINT)
        a_display.move_to([3.45, 0.95, 0])
        state_note = label("兩端向上：I、II 一定出現", 28, INK, "BOLD")
        state_note.move_to([3.45, -0.15, 0])
        opening_hint = label("下方的紅弧會怎麼變？", 24, MUTED, "MEDIUM")
        opening_hint.move_to([3.45, -1.05, 0])

        notes = {
            0: label("沒有紅弧｜只經過 I、II", 27, INK, "BOLD"),
            -4: label("紅弧跨過 y 軸｜四個象限", 26, CORAL, "BOLD"),
            -2.5: label("紅弧只在右側｜恰三象限", 26, REGION, "BOLD"),
            7: label("紅弧只在左側｜恰三象限", 26, REGION, "BOLD"),
        }
        for note in notes.values():
            note.move_to(state_note)
        badges = {
            0: MathTex("a=0", font_size=49, color=POINT).move_to(a_display),
            -4: MathTex("a=-4", font_size=49, color=POINT).move_to(a_display),
            -2.5: MathTex(r"a=-\frac52", font_size=49, color=POINT).move_to(a_display),
            -2: MathTex("a=-2", font_size=49, color=POINT).move_to(a_display),
            -3: MathTex("a=-3", font_size=49, color=POINT).move_to(a_display),
            7: MathTex("a=7", font_size=49, color=POINT).move_to(a_display),
        }

        def quadrant_animations(
            active: set[int],
            *,
            idle: float = 0.025,
            idle_label: float = 0.3,
        ):
            animations = []
            for index, (region, roman, color) in enumerate(
                zip(quadrants, quadrant_labels, quadrant_colors, strict=True)
            ):
                animations.append(
                    region.animate.set_fill(
                        color, opacity=0.13 if index in active else idle
                    )
                )
                animations.append(
                    roman.animate.set_opacity(1 if index in active else idle_label)
                )
            return animations

        # Beat 01 meet_family: establish the family and the unavoidable top quadrants.
        self.begin_beat("meet_family")
        self.play(FadeIn(heading), FadeIn(source), FadeIn(quadrants), run_time=0.65)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(quadrant_labels))
        self.play(Create(curve), FadeIn(y_intercept), run_time=1.0)
        self.add(negative_curve, roots)
        self.play(Write(family), FadeIn(a_display), FadeIn(state_note), run_time=0.85)
        self.play(*quadrant_animations({0, 1}), FadeIn(opening_hint), run_time=0.65)

        # Beat 02 explore_parameter: compare four states and return exactly to a=0.
        self.next_beat("explore_parameter", loop=True)
        self.wait(0.4)
        for value, active in (
            (-4, {0, 1, 2, 3}),
            (-2.5, {0, 1, 3}),
            (7, {0, 1, 2}),
        ):
            self.play(
                a_tracker.animate.set_value(value),
                Transform(a_display, badges[value]),
                Transform(state_note, notes[value]),
                *quadrant_animations(active),
                run_time=1.35,
                rate_func=rate_functions.ease_in_out_sine,
            )
            self.wait(1.35)
        self.play(
            a_tracker.animate.set_value(0),
            Transform(a_display, badges[0]),
            Transform(
                state_note,
                label("兩端向上：I、II 一定出現", 28, INK, "BOLD").move_to(
                    state_note
                ),
            ),
            *quadrant_animations({0, 1}),
            run_time=1.35,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.4)

        # Beat 03 pose_three_quadrants: isolate what the lower arc must accomplish.
        self.next_beat("pose_three_quadrants")
        question = label("恰三象限，真正要守住什麼？", 28, INK, "BOLD")
        question.move_to([3.45, 0.15, 0])
        need_below = label("1｜要有一段在 x 軸下方", 25, CORAL, "BOLD")
        need_below.move_to([3.45, -0.68, 0])
        stay_one_side = label("2｜但不能跨到 y 軸兩側", 25, BLUE, "BOLD")
        stay_one_side.move_to([3.45, -1.5, 0])
        focus_arc = self.negative_arc(axes, -2.5).set_stroke(CORAL, width=13)

        self.play(
            a_tracker.animate.set_value(-2.5),
            Transform(
                a_display,
                badges[-2.5].copy().move_to([3.45, 1.15, 0]),
            ),
            *quadrant_animations({0, 1, 3}),
            FadeOut(state_note),
            FadeOut(opening_hint),
            run_time=1.2,
        )
        self.play(Create(focus_arc), FadeIn(question), run_time=0.8)
        self.play(FadeOut(focus_arc), FadeIn(need_below), FadeIn(stay_one_side))

        # Beat 04 require_negative_arc: distinguish two crossings from tangency.
        self.next_beat("require_negative_arc")
        root_prompt = label("下方弧段被兩個相異根包住", 27, CORAL, "BOLD")
        root_prompt.move_to([3.45, 0.25, 0])
        tangent_note = label("Δ = 0：只相切，沒有下方弧段", 24, MUTED, "MEDIUM")
        tangent_note.move_to([3.45, -0.65, 0])
        delta_condition = MathTex(r"\Delta>0", font_size=52, color=REGION)
        delta_condition.move_to([3.45, -1.48, 0])
        tangent_dot = Dot(axes.c2p(1, 0), radius=0.095, color=CORAL).set_z_index(9)
        sample_delta = self.discriminant(-2.5)
        sample_roots = (
            (2.5 - math.sqrt(sample_delta)) / 2,
            (2.5 + math.sqrt(sample_delta)) / 2,
        )
        root_rings = VGroup(
            *(
                Circle(radius=0.16, color=REGION, stroke_width=3).move_to(
                    axes.c2p(root, 0)
                )
                for root in sample_roots
            )
        )

        self.play(
            FadeOut(question),
            FadeOut(need_below),
            FadeOut(stay_one_side),
            FadeIn(root_prompt),
            run_time=0.65,
        )
        self.play(Create(root_rings), run_time=0.7)
        self.play(
            a_tracker.animate.set_value(-2),
            Transform(a_display, badges[-2]),
            *quadrant_animations({0, 1}),
            FadeOut(root_rings),
            FadeOut(root_prompt),
            run_time=1.1,
        )
        self.play(GrowFromCenter(tangent_dot), FadeIn(tangent_note), run_time=0.6)
        self.play(
            a_tracker.animate.set_value(-2.5),
            Transform(
                a_display,
                badges[-2.5].copy().move_to([3.45, 1.15, 0]),
            ),
            *quadrant_animations({0, 1, 3}),
            FadeOut(tangent_dot),
            FadeOut(tangent_note),
            FadeIn(root_prompt),
            run_time=1.1,
        )
        self.play(Write(delta_condition), run_time=0.65)

        # Beat 05 guard_y_axis: lower f(0), expose both lower quadrants, and return.
        self.next_beat("guard_y_axis")
        condition_one = VGroup(
            label("條件一", 21, MUTED, "MEDIUM"),
            MathTex(r"\Delta>0", font_size=34, color=REGION),
        ).arrange(RIGHT, buff=0.16).move_to([3.45, 1.72, 0])
        warning = label("截點在下方：原點左右都出現負值", 25, CORAL, "BOLD")
        warning.move_to([3.45, 0.23, 0])
        warning_equation = MathTex(r"f(0)=a+3=-1<0", font_size=38, color=CORAL)
        warning_equation.move_to([3.45, -0.68, 0])
        guard = MathTex(r"f(0)=a+3\ge0", font_size=43, color=BLUE)
        guard.move_to([3.45, -0.42, 0])
        guard_note = label("等號先保留，下一步真的測", 23, MUTED, "MEDIUM")
        guard_note.move_to([3.45, -1.35, 0])
        near_points = VGroup(
            Dot(axes.c2p(-0.12, self.value(-4, -0.12)), radius=0.07, color=CORAL),
            Dot(axes.c2p(0.12, self.value(-4, 0.12)), radius=0.07, color=CORAL),
        ).set_z_index(10)

        self.play(
            FadeOut(family),
            FadeOut(root_prompt),
            Transform(delta_condition, condition_one),
            a_display.animate.move_to([3.45, 0.88, 0]),
            run_time=0.65,
        )
        self.play(
            a_tracker.animate.set_value(-4),
            Transform(a_display, badges[-4]),
            *quadrant_animations({0, 1, 2, 3}),
            FadeIn(warning),
            FadeIn(warning_equation),
            run_time=1.2,
        )
        self.play(Indicate(y_intercept, color=BLUE), FadeIn(near_points), run_time=0.7)
        self.play(
            a_tracker.animate.set_value(-2.5),
            Transform(a_display, badges[-2.5]),
            *quadrant_animations({0, 1, 3}),
            FadeOut(warning),
            FadeOut(near_points),
            ReplacementTransform(warning_equation, guard),
            run_time=1.2,
        )
        self.play(FadeIn(guard_note), Indicate(y_intercept, color=BLUE), run_time=0.7)

        # Beat 06 explain_root_sides: turn the red-arc observation into a proof.
        self.next_beat("explain_root_sides")
        vieta = MathTex(r"r_1<r_2,\qquad r_1r_2=a+3", font_size=39, color=INK)
        vieta.move_to([3.75, 2.2, 0])
        interval_note = label("f(x)<0 只在兩根之間", 23, MUTED, "MEDIUM")
        interval_note.move_to([3.75, 1.58, 0])

        def sign_row(
            y: float,
            product: str,
            root_positions: tuple[float, float],
            outcome: str,
            outcome_color: str,
        ) -> VGroup:
            baseline = Line([2.45, y, 0], [5.45, y, 0], color=HAIRLINE, stroke_width=2)
            zero_tick = Line([3.9, y - 0.12, 0], [3.9, y + 0.12, 0], color=MUTED)
            zero = MathTex("0", font_size=20, color=MUTED).next_to(
                zero_tick, DOWN, buff=0.08
            )
            left_root, right_root = root_positions
            red_interval = Line(
                [left_root, y, 0], [right_root, y, 0], color=CORAL, stroke_width=8
            )
            dots = VGroup(
                Dot([left_root, y, 0], radius=0.065, color=REGION),
                Dot([right_root, y, 0], radius=0.065, color=REGION),
            )
            product_label = MathTex(product, font_size=31, color=INK)
            product_label.move_to([1.35, y, 0])
            result = label(outcome, 21, outcome_color, "BOLD")
            result.move_to([6.45, y, 0])
            return VGroup(
                product_label,
                baseline,
                zero_tick,
                zero,
                red_interval,
                dots,
                result,
            )

        sign_rows = VGroup(
            sign_row(0.75, r"r_1r_2<0", (3.05, 4.75), "跨過 0｜四象限", CORAL),
            sign_row(-0.35, r"r_1r_2>0", (4.35, 5.15), "同在一側", REGION),
            sign_row(-1.45, r"r_1r_2=0", (3.9, 5.05), "從 0 向一側", BLUE),
        ).shift(RIGHT * 0.35)
        sufficiency = VGroup(
            label("已有 Δ > 0 時，恰三象限", 23, INK, "BOLD"),
            MathTex(r"\Longleftrightarrow\ a+3\ge0", font_size=38, color=REGION),
        ).arrange(RIGHT, buff=0.18).move_to([4.15, -2.38, 0])

        self.play(
            FadeOut(a_display),
            FadeOut(delta_condition),
            FadeOut(guard),
            FadeOut(guard_note),
            FadeIn(vieta),
            FadeIn(interval_note),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*(FadeIn(row) for row in sign_rows), lag_ratio=0.28),
            run_time=1.5,
        )
        self.play(FadeIn(sufficiency), run_time=0.7)

        # Beat 07 test_endpoint: substitute a=-3 and repair the omitted boundary.
        self.next_beat("test_endpoint")
        endpoint_formula = VGroup(
            MathTex("a=-3", font_size=45, color=POINT),
            MathTex(r"f(x)=x^2-3x=x(x-3)", font_size=39, color=INK),
            MathTex(r"r_1=0,\qquad r_2=3", font_size=38, color=REGION),
            MathTex(r"0<x<3\ \Longrightarrow\ f(x)<0", font_size=36, color=CORAL),
        ).arrange(DOWN, buff=0.35).move_to([3.65, 0.55, 0])
        endpoint_verdict = label("I、II、IV｜a = -3 仍可行", 27, REGION, "BOLD")
        endpoint_verdict.move_to([3.65, -1.75, 0])
        correction_note = label(
            "來源略去此端點｜本題最小值不受影響", 22, MUTED, "MEDIUM"
        )
        correction_note.move_to([3.65, -2.5, 0])
        endpoint_root_rings = VGroup(
            *(
                Circle(radius=0.16, color=REGION, stroke_width=3).move_to(
                    axes.c2p(root, 0)
                )
                for root in (0, 3)
            )
        )

        self.play(
            FadeOut(vieta),
            FadeOut(interval_note),
            FadeOut(sign_rows),
            FadeOut(sufficiency),
            a_tracker.animate.set_value(-3),
            *quadrant_animations({0, 1, 3}),
            run_time=1.2,
        )
        self.play(LaggedStart(*(Write(line) for line in endpoint_formula), lag_ratio=0.22))
        self.play(FadeIn(endpoint_verdict), Create(endpoint_root_rings), run_time=0.8)
        self.play(FadeIn(correction_note), run_time=0.55)

        # Beat 08 solve_discriminant: stop the geometry and solve Delta>0 exactly.
        self.next_beat("solve_discriminant")
        for dynamic in (curve, negative_curve, roots, y_intercept):
            dynamic.clear_updaters()
        graph_group = VGroup(
            axes,
            x_label,
            y_label,
            quadrants,
            quadrant_labels,
            curve,
            negative_curve,
            roots,
            y_intercept,
            a_display,
            endpoint_root_rings,
        )
        endpoint_group = VGroup(endpoint_formula, endpoint_verdict, correction_note)
        algebra_title = label("第一條件｜兩個相異根", 30, INK, "BOLD")
        algebra_title.move_to(UP * 2.92)
        delta_1 = MathTex(r"\Delta=a^2-4(a+3)>0", font_size=45, color=INK)
        delta_1.move_to(UP * 1.55)
        delta_2 = MathTex(r"a^2-4a-12>0", font_size=45, color=INK)
        delta_2.move_to(UP * 0.45)
        delta_3 = MathTex(r"(a-6)(a+2)>0", font_size=47, color=REGION)
        delta_3.move_to(DOWN * 0.65)
        delta_solution = VGroup(
            MathTex(r"a<-2", font_size=48, color=POINT),
            label("或", 29, MUTED, "BOLD"),
            MathTex(r"a>6", font_size=48, color=POINT),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 1.92)

        self.play(FadeOut(graph_group), FadeOut(endpoint_group), FadeIn(algebra_title))
        self.play(Write(delta_1), run_time=0.8)
        self.play(TransformFromCopy(delta_1, delta_2), run_time=0.75)
        self.play(TransformFromCopy(delta_2, delta_3), run_time=0.75)
        self.play(Write(delta_solution), run_time=0.75)

        # Beat 09 intersect_ranges: intersect both continuous parameter filters.
        self.next_beat("intersect_ranges")
        algebra_group = VGroup(algebra_title, delta_1, delta_2, delta_3, delta_solution)
        lines = VGroup(
            *(
                NumberLine(
                    x_range=[-4, 8, 1],
                    length=10.7,
                    include_ticks=True,
                    tick_size=0.07,
                    color=HAIRLINE,
                    stroke_width=2.2,
                ).move_to([0.55, y, 0])
                for y in (1.45, 0.0, -1.45)
            )
        )
        line_labels = VGroup(
            MathTex(r"\Delta>0", font_size=34, color=CORAL).move_to([-6.1, 1.45, 0]),
            MathTex(r"a\ge-3", font_size=34, color=BLUE).move_to([-6.1, 0.0, 0]),
            label("交集", 24, REGION, "BOLD").move_to([-6.1, -1.45, 0]),
        )

        top_line, middle_line, bottom_line = lines
        delta_rays = VGroup(
            Arrow(
                top_line.n2p(-2),
                top_line.n2p(-4),
                buff=0,
                color=CORAL,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            ),
            Arrow(
                top_line.n2p(6),
                top_line.n2p(8),
                buff=0,
                color=CORAL,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            ),
            self.open_dot(top_line.n2p(-2), CORAL),
            self.open_dot(top_line.n2p(6), CORAL),
        )
        guard_ray = VGroup(
            Arrow(
                middle_line.n2p(-3),
                middle_line.n2p(8),
                buff=0,
                color=BLUE,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.035,
            ),
            Dot(middle_line.n2p(-3), radius=0.095, color=BLUE),
        )
        intersection = VGroup(
            Line(
                bottom_line.n2p(-3),
                bottom_line.n2p(-2),
                color=REGION,
                stroke_width=8,
            ),
            Dot(bottom_line.n2p(-3), radius=0.095, color=REGION),
            self.open_dot(bottom_line.n2p(-2), REGION),
            Arrow(
                bottom_line.n2p(6),
                bottom_line.n2p(8),
                buff=0,
                color=REGION,
                stroke_width=7,
                max_tip_length_to_length_ratio=0.12,
            ),
            self.open_dot(bottom_line.n2p(6), REGION),
        )
        endpoint_labels = VGroup(
            *(
                MathTex(str(value), font_size=25, color=INK).next_to(
                    bottom_line.n2p(value), DOWN, buff=0.17
                )
                for value in (-3, -2, 6)
            )
        )
        endpoint_checked = label("-3 已驗證", 21, BLUE, "BOLD")
        endpoint_checked.next_to(bottom_line.n2p(-3), UP, buff=0.2)
        domain_result = MathTex(
            r"a\in[-3,-2)\cup(6,\infty)",
            font_size=48,
            color=REGION,
        ).move_to(DOWN * 2.62)

        self.play(FadeOut(algebra_group), FadeIn(lines), FadeIn(line_labels), run_time=0.7)
        self.play(Create(delta_rays), run_time=0.9)
        self.play(Create(guard_ray), run_time=0.8)
        self.play(
            Create(intersection),
            FadeIn(endpoint_labels),
            FadeIn(endpoint_checked),
            run_time=0.9,
        )
        self.play(Write(domain_result), run_time=0.7)

        # Beat 10 introduce_target: show the objective only after the domain is known.
        self.next_beat("introduce_target")
        range_visuals = VGroup(
            lines,
            line_labels,
            delta_rays,
            guard_ray,
            intersection,
            endpoint_labels,
            endpoint_checked,
        )
        domain_chip = domain_result.copy().scale(0.72).move_to(UP * 2.62)
        objective_title = label("現在才看：題目要最小化什麼？", 30, INK, "BOLD")
        objective_title.move_to(UP * 1.55)
        objective = MathTex(
            r"E(a)=",
            r"(a-2025)^2",
            r"+8(a-2025)",
            r"+6",
            font_size=47,
            color=INK,
        ).move_to(DOWN * 0.05)
        objective[1].set_color(BLUE)
        objective[2].set_color(BLUE)
        repeat_note = label("同一塊 a - 2025 出現兩次", 25, BLUE, "BOLD")
        repeat_note.move_to(DOWN * 1.05)
        minimum_question = label("最低點藏在哪裡？", 27, MUTED, "MEDIUM")
        minimum_question.move_to(DOWN * 1.95)

        self.play(
            FadeOut(range_visuals),
            ReplacementTransform(domain_result, domain_chip),
            FadeIn(objective_title),
            run_time=0.75,
        )
        self.play(Write(objective), run_time=0.9)
        self.play(FadeIn(repeat_note), FadeIn(minimum_question), run_time=0.65)

        # Beat 11 complete_square: preserve the repeated block and expose the vertex.
        self.next_beat("complete_square")
        t_definition = MathTex(r"t=a-2025", font_size=38, color=BLUE)
        t_definition.move_to(UP * 1.15)
        square_0 = MathTex(r"E=t^2+8t+6", font_size=43, color=INK)
        square_0.move_to(UP * 0.25)
        square_1 = MathTex(r"=(t+4)^2-16+6", font_size=43, color=INK)
        square_1.move_to(DOWN * 0.7)
        half_note = MathTex(r"8\div2=4", font_size=30, color=POINT)
        half_note.move_to([4.65, -0.7, 0])
        square_2 = MathTex(r"=(t+4)^2-10", font_size=45, color=INK)
        square_2.move_to(DOWN * 1.62)
        square_3 = MathTex(r"E(a)=(a-2021)^2-10", font_size=48, color=REGION)
        square_3.move_to(DOWN * 2.62)

        self.play(
            FadeOut(objective_title),
            FadeOut(repeat_note),
            FadeOut(minimum_question),
            objective.animate.scale(0.75).move_to(UP * 2.03),
            FadeIn(t_definition),
            run_time=0.7,
        )
        self.play(TransformFromCopy(objective, square_0), run_time=0.75)
        self.play(TransformFromCopy(square_0, square_1), FadeIn(half_note), run_time=0.8)
        self.play(TransformFromCopy(square_1, square_2), run_time=0.75)
        self.play(TransformFromCopy(square_2, square_3), run_time=0.85)

        # Beat 12 locate_vertex: plot in u=a-2021 and verify the equality point.
        self.next_beat("locate_vertex")
        algebra_min_group = VGroup(
            domain_chip,
            objective,
            t_definition,
            square_0,
            square_1,
            half_note,
            square_2,
            square_3,
        )
        opt_axes = Axes(
            x_range=[-4.5, 4.5, 1],
            y_range=[-12, 8, 5],
            x_length=7.7,
            y_length=5.3,
            axis_config={"color": MUTED, "stroke_width": 2.1, "include_tip": True},
            tips=True,
        ).move_to([-3.3, -0.45, 0])
        opt_curve = opt_axes.plot(
            lambda u: u * u - 10,
            x_range=[-4.2, 4.2, 0.05],
            color=POINT,
            stroke_width=5,
        )
        opt_x = MathTex("u", font_size=25, color=MUTED)
        opt_x.next_to(opt_axes.x_axis.get_end(), DOWN, buff=0.08)
        opt_y = MathTex("E", font_size=25, color=MUTED)
        opt_y.next_to(opt_axes.y_axis.get_end(), LEFT, buff=0.08)
        vertex = Dot(opt_axes.c2p(0, -10), radius=0.105, color=CORAL).set_z_index(8)
        vertex_guide = DashedLine(
            opt_axes.c2p(0, 0),
            opt_axes.c2p(0, -10),
            color=BLUE,
            dash_length=0.12,
        )
        vertex_label = MathTex(r"(0,-10)", font_size=30, color=CORAL)
        vertex_label.next_to(vertex, RIGHT, buff=0.15)
        u_definition = MathTex(r"u=a-2021", font_size=41, color=BLUE)
        u_definition.move_to([3.5, 2.2, 0])
        u_formula = MathTex(r"E=u^2-10", font_size=45, color=INK)
        u_formula.move_to([3.5, 1.2, 0])
        equality = MathTex(r"u=0\ \Longleftrightarrow\ a=2021", font_size=40, color=POINT)
        equality.move_to([3.5, 0.05, 0])
        admissible = MathTex(r"2021>6", font_size=46, color=REGION)
        admissible.move_to([3.5, -1.05, 0])
        admissible_note = label("落在允許的右側區間", 23, REGION, "BOLD")
        admissible_note.move_to([3.5, -1.65, 0])
        minimum = MathTex(r"\min E=-10", font_size=56, color=CORAL)
        minimum.move_to([3.5, -2.55, 0])

        self.play(FadeOut(algebra_min_group), Create(opt_axes), FadeIn(opt_x), FadeIn(opt_y))
        self.play(Create(opt_curve), Write(u_definition), Write(u_formula), run_time=1.0)
        self.play(
            Create(vertex_guide),
            GrowFromCenter(vertex),
            FadeIn(vertex_label),
            run_time=0.75,
        )
        self.play(Write(equality), run_time=0.7)
        self.play(Write(admissible), FadeIn(admissible_note), run_time=0.7)
        self.play(Write(minimum), Circumscribe(vertex, color=CORAL), run_time=0.8)

        # Beat 13 consolidate: retain the correction and the attained minimum together.
        self.next_beat("consolidate")
        optimization_group = VGroup(
            opt_axes,
            opt_curve,
            opt_x,
            opt_y,
            vertex,
            vertex_guide,
            vertex_label,
            u_definition,
            u_formula,
            equality,
            admissible,
            admissible_note,
            minimum,
        )
        divider = Line([0, 2.7, 0], [0, -2.45, 0], color=HAIRLINE, stroke_width=2)
        left_title = label("恰三象限", 29, INK, "BOLD").move_to([-3.65, 2.45, 0])
        left_conditions = VGroup(
            MathTex(r"\Delta>0", font_size=42, color=CORAL),
            MathTex(r"f(0)=a+3\ge0", font_size=42, color=BLUE),
            MathTex(r"a\in[-3,-2)\cup(6,\infty)", font_size=40, color=REGION),
        ).arrange(DOWN, buff=0.43).move_to([-3.65, 0.45, 0])
        left_note = label("a = -3 已由根 0、3 驗證", 22, MUTED, "MEDIUM")
        left_note.move_to([-3.65, -1.65, 0])
        right_title = label("完成平方", 29, INK, "BOLD").move_to([3.65, 2.45, 0])
        right_steps = VGroup(
            MathTex(r"E(a)=(a-2021)^2-10", font_size=40, color=REGION),
            MathTex(r"a=2021>6", font_size=43, color=POINT),
        ).arrange(DOWN, buff=0.55).move_to([3.65, 0.68, 0])
        final_answer = MathTex(r"\min E(a)=-10", font_size=57, color=CORAL)
        final_answer.move_to([3.65, -1.2, 0])
        final_box = SurroundingRectangle(
            final_answer,
            color=POINT,
            buff=0.25,
            corner_radius=0.08,
            stroke_width=3,
        )
        correction_recap = label(
            "補回端點，條件更完整｜最小值仍與來源答案一致",
            23,
            MUTED,
            "MEDIUM",
        ).move_to([0, -3.0, 0])

        self.play(FadeOut(optimization_group), Create(divider), run_time=0.7)
        self.play(
            FadeIn(left_title),
            FadeIn(right_title),
            LaggedStart(*(Write(item) for item in left_conditions), lag_ratio=0.22),
            run_time=1.15,
        )
        self.play(FadeIn(left_note), LaggedStart(*(Write(item) for item in right_steps)))
        self.play(Write(final_answer), Create(final_box), run_time=0.85)
        self.play(FadeIn(correction_recap), run_time=0.55)
        self.wait(0.3)
