"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q3."""

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
    PURPLE,
    REGION,
    WHITE,
    CarloSlide,
    label,
)
from manim import (
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
    NumberLine,
    Polygon,
    Rectangle,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class CarloTcfs115MathQ03(CarloSlide):
    """Discover the quadrant conditions, then filter integer-root candidates."""

    lesson_id = "carlo.tcfs_115_math_gifted.q03"

    @staticmethod
    def radicand(k: int | float) -> int | float:
        return k * k - k - 1

    @classmethod
    def visible_parabola(
        cls,
        axes: Axes,
        k: float,
        *,
        color: str = POINT,
        stroke_width: float = 5,
    ):
        """Plot only the part below the graph's fixed top boundary."""
        top = 7.6
        reach = math.sqrt(max(top + cls.radicand(k), 0.05))
        lower = max(-6.0, -k - reach)
        upper = min(6.0, -k + reach)
        return axes.plot(
            lambda x: x * x + 2 * k * x + k + 1,
            x_range=[lower, upper, 0.07],
            color=color,
            stroke_width=stroke_width,
            use_smoothing=True,
        )

    @classmethod
    def negative_arc(cls, axes: Axes, k: float) -> VGroup:
        radicand = cls.radicand(k)
        if radicand <= 0:
            return VGroup()
        root = math.sqrt(radicand)
        left_root = max(-6.0, -k - root)
        right_root = min(6.0, -k + root)
        return VGroup(
            axes.plot(
                lambda x: x * x + 2 * k * x + k + 1,
                x_range=[left_root, right_root, 0.04],
                color=CORAL,
                stroke_width=8,
                use_smoothing=True,
            )
        )

    @classmethod
    def root_dots(cls, axes: Axes, k: float) -> VGroup:
        radicand = cls.radicand(k)
        if radicand <= 0:
            return VGroup()
        root = math.sqrt(radicand)
        roots = (-k - root, -k + root)
        return VGroup(
            *(
                Dot(axes.c2p(value, 0), radius=0.065, color=REGION).set_z_index(7)
                for value in roots
                if -6 <= value <= 6
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
            fill_opacity=0.03,
        ).set_z_index(-5)

    @staticmethod
    def table_cell(tex: str, *, width: float = 1.04) -> VGroup:
        box = Rectangle(
            width=width,
            height=0.72,
            stroke_color=HAIRLINE,
            stroke_width=1.6,
            fill_color=HAIRLINE,
            fill_opacity=0.08,
        )
        value = MathTex(tex, font_size=29, color=INK)
        return VGroup(box, value)

    def construct(self) -> None:
        heading = label("第 3 題｜參數如何改變拋物線？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        axes = Axes(
            x_range=[-6, 6, 1],
            y_range=[-6, 8, 2],
            x_length=8.4,
            y_length=5.55,
            axis_config={"color": MUTED, "stroke_width": 2.2, "include_tip": True},
            tips=True,
        ).move_to([-3.25, -0.45, 0])
        x_label = MathTex("x", font_size=26, color=MUTED)
        x_label.next_to(axes.x_axis.get_end(), DOWN, buff=0.08)
        y_label = MathTex("y", font_size=26, color=MUTED)
        y_label.next_to(axes.y_axis.get_end(), LEFT, buff=0.08)

        quadrant_colors = (BLUE, PURPLE, CORAL, REGION)
        quadrants = VGroup(
            self.quadrant(axes, 0, 6, 0, 8, quadrant_colors[0]),
            self.quadrant(axes, -6, 0, 0, 8, quadrant_colors[1]),
            self.quadrant(axes, -6, 0, -6, 0, quadrant_colors[2]),
            self.quadrant(axes, 0, 6, -6, 0, quadrant_colors[3]),
        )
        quadrant_labels = VGroup(
            *(
                label(roman, 22, color, "BOLD")
                .move_to(axes.c2p(x, y))
                .set_opacity(0.38)
                for roman, x, y, color in (
                    ("I", 5.35, 6.9, BLUE),
                    ("II", -5.3, 6.9, PURPLE),
                    ("III", -5.15, -5.15, CORAL),
                    ("IV", 5.2, -5.15, REGION),
                )
            )
        )

        k_tracker = ValueTracker(0)
        curve = always_redraw(
            lambda: self.visible_parabola(axes, k_tracker.get_value())
        )
        negative_curve = always_redraw(
            lambda: self.negative_arc(axes, k_tracker.get_value())
        )
        roots = always_redraw(lambda: self.root_dots(axes, k_tracker.get_value()))
        y_intercept = always_redraw(
            lambda: Dot(
                axes.c2p(0, k_tracker.get_value() + 1),
                radius=0.085,
                color=BLUE,
            ).set_z_index(8)
        )

        family = MathTex(
            r"f_k(x)=x^2+2kx+(k+1)",
            font_size=40,
            color=INK,
        ).move_to([3.35, 2.28, 0])
        k_range = MathTex(
            r"k\in\mathbb Z,\qquad |k|\le5",
            font_size=34,
            color=MUTED,
        ).move_to([3.35, 1.5, 0])
        k_display = MathTex("k=0", font_size=50, color=POINT)
        k_display.move_to([3.35, 0.45, 0])
        state_note = label("先看曲線怎麼變", 29, INK, "BOLD")
        state_note.move_to([3.35, -0.55, 0])
        opening_hint = label("四個象限先保持安靜", 24, MUTED, "MEDIUM")
        opening_hint.move_to([3.35, -1.32, 0])

        # Beat 01 meet_family: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(quadrants), run_time=0.7)
        self.play(Create(axes), FadeIn(x_label), FadeIn(y_label), FadeIn(quadrant_labels))
        self.play(Create(curve), FadeIn(y_intercept), run_time=1.1)
        self.play(
            Write(family),
            FadeIn(k_range),
            FadeIn(k_display),
            FadeIn(state_note),
            FadeIn(opening_hint),
            run_time=0.9,
        )

        notes = {
            0: label("只經過 I、II", 29, INK, "BOLD"),
            -2: label("紅弧跨過 y 軸｜四個象限", 27, CORAL, "BOLD"),
            -1: label("紅弧只在右側｜恰三象限", 27, REGION, "BOLD"),
            3: label("紅弧只在左側｜恰三象限", 27, REGION, "BOLD"),
        }
        for note in notes.values():
            note.move_to(state_note)
        k_badges = {
            value: MathTex(f"k={value}", font_size=50, color=POINT).move_to(k_display)
            for value in notes
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
                opacity = 0.13 if index in active else idle
                label_opacity = 1 if index in active else idle_label
                animations.append(region.animate.set_fill(color, opacity=opacity))
                animations.append(roman.animate.set_opacity(label_opacity))
            return animations

        # Beat 02 compare_quadrants: settled semantic step.
        self.next_slide(loop=True)

        self.wait(0.35)
        next_state_note = notes[0].copy()
        self.play(
            *quadrant_animations({0, 1}),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            FadeOut(opening_hint),
            run_time=0.55,
        )
        state_note = next_state_note
        self.wait(1.5)
        next_k_display = k_badges[3].copy()
        next_state_note = notes[3].copy()
        self.play(
            k_tracker.animate.set_value(3),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            *quadrant_animations({0, 1, 2}),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        k_display = next_k_display
        state_note = next_state_note
        self.wait(1.5)
        next_k_display = k_badges[0].copy()
        next_state_note = notes[0].copy()
        self.play(
            k_tracker.animate.set_value(0),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            *quadrant_animations({0, 1}),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        k_display = next_k_display
        state_note = next_state_note
        self.wait(1.5)
        next_state_note = label("先看曲線怎麼變", 29, INK, "BOLD").move_to(state_note)
        self.play(
            *quadrant_animations(set(), idle=0.03, idle_label=0.38),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            FadeIn(opening_hint),
            run_time=0.55,
        )
        state_note = next_state_note
        self.wait(0.35)

        # Beat 03 compare_negative_quadrants: settled semantic step.
        self.next_slide(loop=True)
        next_k_display = k_badges[-2].copy()
        next_state_note = notes[-2].copy()
        self.play(
            k_tracker.animate.set_value(-2),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            *quadrant_animations({0, 1, 2, 3}),
            FadeOut(opening_hint),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        k_display = next_k_display
        state_note = next_state_note
        self.wait(1.5)
        next_k_display = k_badges[-1].copy()
        next_state_note = notes[-1].copy()
        self.play(
            k_tracker.animate.set_value(-1),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            *quadrant_animations({0, 1, 3}),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        k_display = next_k_display
        state_note = next_state_note
        self.wait(1.5)
        next_k_display = k_badges[0].copy()
        next_state_note = notes[0].copy()
        self.play(
            k_tracker.animate.set_value(0),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            *quadrant_animations({0, 1}),
            run_time=1.4,
            rate_func=rate_functions.ease_in_out_sine,
        )
        k_display = next_k_display
        state_note = next_state_note
        self.wait(1.5)
        next_state_note = label("先看曲線怎麼變", 29, INK, "BOLD").move_to(state_note)
        self.play(
            *quadrant_animations(set(), idle=0.03, idle_label=0.38),
            Succession(FadeOut(state_note), FadeIn(next_state_note)),
            FadeIn(opening_hint),
            run_time=0.55,
        )
        state_note = next_state_note
        self.wait(0.35)

        # Beat 04 need_two_roots: settled semantic step.
        self.next_slide()

        three_quadrant_note = label("三象限例：紅弧真的進到 x 軸下方", 27, INK, "BOLD")
        three_quadrant_note.move_to([3.35, 1.42, 0])
        below_note = label("下方弧段需要兩個相異交點", 27, CORAL, "BOLD")
        below_note.move_to([3.35, -0.38, 0])
        delta_first = MathTex(
            r"\Delta=(2k)^2-4(k+1)",
            font_size=37,
            color=INK,
        ).move_to([3.35, -1.0, 0])
        delta_result = MathTex(
            r"\Delta=4(k^2-k-1)>0",
            font_size=39,
            color=REGION,
        ).move_to([3.35, -1.62, 0])
        tangent_note = label("Δ = 0 只相切，沒有下方弧段", 23, MUTED, "MEDIUM")
        tangent_note.move_to([3.35, -2.32, 0])
        focus_arc = self.negative_arc(axes, -1)
        focus_arc.set_stroke(CORAL, width=12)

        next_k_display = k_badges[-1].copy()
        self.play(
            FadeOut(opening_hint),
            FadeOut(k_range),
            family.animate.scale(0.82).move_to([3.35, 2.36, 0]),
            k_tracker.animate.set_value(-1),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            Succession(FadeOut(state_note), FadeIn(three_quadrant_note)),
            *quadrant_animations({0, 1, 3}),
            run_time=1.25,
        )
        k_display = next_k_display
        state_note = three_quadrant_note
        self.play(Create(focus_arc), FadeIn(below_note), run_time=0.9)
        self.play(FadeOut(focus_arc), Write(delta_first), run_time=0.75)
        self.play(TransformFromCopy(delta_first, delta_result), FadeIn(tangent_note), run_time=0.8)

        # Beat 05 guard_y_axis: settled semantic step.
        self.next_slide()

        warning = label("f(0) < 0：左右下方一起出現", 28, CORAL, "BOLD")
        warning.move_to([3.35, -0.35, 0])
        warning_equation = MathTex(
            r"f(0)=k+1<0",
            font_size=39,
            color=CORAL,
        ).move_to([3.35, -1.18, 0])
        guard = MathTex(
            r"f(0)=k+1\ge0",
            font_size=41,
            color=BLUE,
        ).move_to([3.35, -0.42, 0])
        guard_result = MathTex(r"k\ge-1", font_size=48, color=REGION)
        guard_result.move_to([3.35, -1.32, 0])
        condition_one = VGroup(
            label("條件一：", 22, MUTED, "MEDIUM"),
            MathTex(r"\Delta>0", font_size=34, color=MUTED),
        ).arrange(RIGHT, buff=0.16).move_to([3.35, 1.95, 0])

        self.play(
            FadeOut(family),
            FadeOut(state_note),
            FadeOut(below_note),
            FadeOut(delta_first),
            delta_result.animate.scale(0.8).move_to([3.35, 1.28, 0]),
            FadeOut(tangent_note),
            FadeIn(condition_one),
            run_time=0.7,
        )
        next_k_display = k_badges[-2].copy()
        self.play(
            k_tracker.animate.set_value(-2),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            *quadrant_animations({0, 1, 2, 3}),
            FadeIn(warning),
            FadeIn(warning_equation),
            run_time=1.3,
        )
        k_display = next_k_display
        self.play(Indicate(y_intercept, color=BLUE), run_time=0.8)
        # Beat 06 derive_y_axis_guard: settled semantic step.
        self.next_slide()
        next_k_display = k_badges[-1].copy()
        self.play(
            k_tracker.animate.set_value(-1),
            Succession(FadeOut(k_display), FadeIn(next_k_display)),
            *quadrant_animations({0, 1, 3}),
            Succession(
                FadeOut(VGroup(warning, warning_equation)),
                FadeIn(guard),
            ),
            run_time=1.25,
        )
        k_display = next_k_display
        self.play(Write(guard_result), Indicate(y_intercept, color=BLUE), run_time=0.8)

        # Beat 07 count_m: settled semantic step.
        self.next_slide()

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
            k_display,
            delta_result,
            condition_one,
            guard,
            guard_result,
        )
        number_line = NumberLine(
            x_range=[-5, 5, 1],
            length=11.8,
            include_ticks=True,
            tick_size=0.08,
            color=MUTED,
            stroke_width=3,
        ).move_to(DOWN * 0.52)
        integer_labels = VGroup(
            *(
                label(str(k), 24, INK, "BOLD").next_to(
                    number_line.n2p(k), DOWN, buff=0.18
                )
                for k in range(-5, 6)
            )
        )
        integer_dots = VGroup(
            *(Dot(number_line.n2p(k), radius=0.09, color=WHITE) for k in range(-5, 6))
        )
        first_filter = MathTex(
            r"k^2-k-1>0\quad\Longrightarrow\quad k\le-1\quad\lor\quad k\ge2",
            font_size=38,
            color=INK,
        ).move_to(UP * 2.38)
        second_filter = MathTex(
            r"k\ge-1",
            font_size=41,
            color=BLUE,
        ).move_to(UP * 1.47)
        final_values = MathTex(
            r"k\in\{-1,2,3,4,5\}",
            font_size=44,
            color=REGION,
        ).move_to(DOWN * 1.68)
        count_labels = VGroup(
            *(
                MathTex(str(index), font_size=25, color=POINT).next_to(
                    number_line.n2p(k), UP, buff=0.22
                )
                for index, k in enumerate((-1, 2, 3, 4, 5), start=1)
            )
        )
        m_result = MathTex("m=5", font_size=54, color=POINT)
        m_result.move_to(DOWN * 2.73)

        for dynamic_mobject in (curve, negative_curve, roots, y_intercept):
            dynamic_mobject.clear_updaters()
        self.play(FadeOut(graph_group), Create(number_line), FadeIn(integer_labels))
        self.play(FadeIn(integer_dots), Write(first_filter), run_time=0.9)
        self.play(
            *(
                dot.animate.set_color(BLUE).set_opacity(1)
                if self.radicand(k) > 0
                else dot.animate.set_opacity(0.15)
                for k, dot in zip(range(-5, 6), integer_dots, strict=True)
            ),
            run_time=0.9,
        )
        # Beat 08 intersect_parameter_conditions: settled semantic step.
        self.next_slide()
        self.play(Write(second_filter), run_time=0.55)
        self.play(
            *(
                dot.animate.set_color(REGION).set_opacity(1)
                if k in {-1, 2, 3, 4, 5}
                else dot.animate.set_opacity(0.12)
                for k, dot in zip(range(-5, 6), integer_dots, strict=True)
            ),
            run_time=0.9,
        )
        # Beat 09 count_valid_parameters: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(*(FadeIn(number) for number in count_labels), lag_ratio=0.16),
            Write(final_values),
            run_time=1.0,
        )
        self.play(Write(m_result), run_time=0.6)

        # Beat 10 ask_integer_root: settled semantic step.
        self.next_slide()

        count_group = VGroup(
            number_line,
            integer_labels,
            integer_dots,
            first_filter,
            second_filter,
            final_values,
            count_labels,
            m_result,
        )
        second_question = label("第二問｜什麼時候會有正整數根？", 31, INK, "BOLD")
        second_question.move_to(UP * 2.82)
        equation = MathTex(
            r"x^2+2kx+(k+1)=0",
            font_size=43,
            color=INK,
        ).move_to(UP * 1.72)
        formula_first = MathTex(
            r"x=\frac{-2k\pm\sqrt{4k^2-4(k+1)}}{2}",
            font_size=42,
            color=INK,
        ).move_to(UP * 0.55)
        formula_result = MathTex(
            r"x=-k\pm\sqrt{k^2-k-1}",
            font_size=48,
            color=REGION,
        ).move_to(DOWN * 0.72)
        square_condition = MathTex(
            r"\sqrt{k^2-k-1}=s,\qquad s\in\mathbb Z_{\ge0}",
            font_size=40,
            color=POINT,
        ).move_to(DOWN * 1.9)
        symbol_note = label("s：根號的整數值　｜　n：合格 k 的個數", 24, MUTED, "MEDIUM")
        symbol_note.move_to(DOWN * 2.75)

        self.play(FadeOut(count_group), FadeIn(second_question), run_time=0.65)
        self.play(Write(equation), run_time=0.7)
        self.play(TransformFromCopy(equation, formula_first), run_time=0.9)
        # Beat 11 derive_root_formula: settled semantic step.
        self.next_slide()
        self.play(TransformFromCopy(formula_first, formula_result), run_time=0.9)
        self.play(Write(square_condition), FadeIn(symbol_note), run_time=0.8)

        # Beat 12 perfect_square_filter: settled semantic step.
        self.next_slide()

        derivation_group = VGroup(
            second_question,
            equation,
            formula_first,
            formula_result,
            square_condition,
            symbol_note,
        )
        table_title = label("十一個 k，先用完全平方篩選", 31, INK, "BOLD")
        table_title.move_to(UP * 2.95)
        values = [int(self.radicand(k)) for k in range(-5, 6)]
        columns = VGroup()
        for k, value in zip(range(-5, 6), values, strict=True):
            column = VGroup(
                self.table_cell(str(k)),
                self.table_cell(str(value)),
            ).arrange(DOWN, buff=0.04)
            columns.add(column)
        columns.arrange(RIGHT, buff=0.04)
        columns.move_to([0.45, 0.15, 0])
        row_k = MathTex("k", font_size=32, color=POINT)
        row_k.next_to(columns[0][0], LEFT, buff=0.32)
        row_q = MathTex(r"k^2-k-1", font_size=27, color=MUTED)
        row_q.next_to(columns[0][1], LEFT, buff=0.24)
        negative_note = label("負數先淘汰", 25, CORAL, "BOLD")
        negative_note.move_to(DOWN * 1.65)
        square_note = label("其餘只有 1 是完全平方", 27, REGION, "BOLD")
        square_note.move_to(DOWN * 2.3)
        survivor_boxes = VGroup(
            *(
                SurroundingRectangle(
                    columns[index], color=REGION, buff=0.08, stroke_width=3
                )
                for index in (4, 7)
            )
        )
        candidate_labels = VGroup(
            *(
                label("候選", 21, REGION, "BOLD").next_to(
                    columns[index], UP, buff=0.14
                )
                for index in (4, 7)
            )
        )
        candidate_result = MathTex(
            r"k\in\{-1,2\}",
            font_size=43,
            color=POINT,
        ).move_to(DOWN * 3.02)

        self.play(FadeOut(derivation_group), FadeIn(table_title), run_time=0.65)
        self.play(
            LaggedStart(*(FadeIn(column) for column in columns), lag_ratio=0.06),
            FadeIn(row_k),
            FadeIn(row_q),
            run_time=1.15,
        )
        self.play(
            columns[5].animate.set_opacity(0.18),
            columns[6].animate.set_opacity(0.18),
            FadeIn(negative_note),
            run_time=0.65,
        )
        nonsquare_indices = (0, 1, 2, 3, 8, 9, 10)
        # Beat 13 bound_square_candidates: settled semantic step.
        self.next_slide()
        self.play(
            *(columns[index].animate.set_opacity(0.18) for index in nonsquare_indices),
            Succession(FadeOut(negative_note), FadeIn(square_note)),
            run_time=0.95,
        )
        self.play(
            Create(survivor_boxes),
            FadeIn(candidate_labels),
            Write(candidate_result),
            run_time=0.8,
        )

        # Beat 14 test_candidates: settled semantic step.
        self.next_slide()

        table_group = VGroup(
            table_title,
            columns,
            row_k,
            row_q,
            square_note,
            survivor_boxes,
            candidate_labels,
            candidate_result,
        )
        test_title = label("候選還要檢查：根是不是正的？", 31, INK, "BOLD")
        test_title.move_to(UP * 3.0)
        divider = Line(UP * 2.25, DOWN * 2.25, color=HAIRLINE, stroke_width=2)
        left_axes = Axes(
            x_range=[-0.5, 2.8, 1],
            y_range=[-1.5, 4, 1],
            x_length=5.1,
            y_length=3.2,
            axis_config={"color": MUTED, "stroke_width": 1.8, "include_tip": False},
            tips=False,
        ).move_to([-3.7, -0.48, 0])
        right_axes = Axes(
            x_range=[-4, 0.5, 1],
            y_range=[-1.5, 5, 1],
            x_length=5.1,
            y_length=3.2,
            axis_config={"color": MUTED, "stroke_width": 1.8, "include_tip": False},
            tips=False,
        ).move_to([3.65, -0.48, 0])
        left_curve = left_axes.plot(
            lambda x: x * x - 2 * x,
            x_range=[-0.45, 2.75, 0.05],
            color=POINT,
            stroke_width=5,
        )
        right_curve = right_axes.plot(
            lambda x: x * x + 4 * x + 3,
            x_range=[-3.9, 0.35, 0.05],
            color=POINT,
            stroke_width=5,
        )
        left_formula = MathTex(
            r"k=-1:\quad x(x-2)=0",
            font_size=37,
            color=INK,
        ).move_to([-3.7, 1.95, 0])
        right_formula = MathTex(
            r"k=2:\quad (x+1)(x+3)=0",
            font_size=37,
            color=INK,
        ).move_to([3.65, 1.95, 0])
        left_roots = VGroup(
            Dot(left_axes.c2p(0, 0), radius=0.08, color=MUTED),
            Dot(left_axes.c2p(2, 0), radius=0.105, color=REGION),
        )
        right_roots = VGroup(
            Dot(right_axes.c2p(-3, 0), radius=0.09, color=CORAL),
            Dot(right_axes.c2p(-1, 0), radius=0.09, color=CORAL),
        )
        left_result = VGroup(
            MathTex(r"x=0,\ \boxed{2}", font_size=38, color=REGION),
            label("可行", 23, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.2).move_to([-3.7, -2.47, 0])
        right_result = VGroup(
            MathTex(r"x=-3,-1<0", font_size=35, color=CORAL),
            label("不合", 23, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.2).move_to([3.65, -2.47, 0])
        n_result = MathTex("n=1", font_size=51, color=POINT)
        n_result.move_to([0, -3.12, 0])

        self.play(FadeOut(table_group), FadeIn(test_title), Create(divider), run_time=0.7)
        self.play(Create(left_axes), Create(right_axes), FadeIn(left_formula), FadeIn(right_formula))
        self.play(Create(left_curve), Create(right_curve), run_time=1.0)
        # Beat 15 verify_integer_roots: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(*(GrowFromCenter(dot) for dot in left_roots), lag_ratio=0.2),
            LaggedStart(*(GrowFromCenter(dot) for dot in right_roots), lag_ratio=0.2),
            run_time=0.75,
        )
        self.play(Write(left_result), Write(right_result), run_time=0.8)
        self.play(Write(n_result), run_time=0.55)

        # Beat 16 final_pair: settled semantic step.
        self.next_slide()

        candidate_test_group = VGroup(
            test_title,
            divider,
            left_axes,
            right_axes,
            left_curve,
            right_curve,
            left_formula,
            right_formula,
            left_roots,
            right_roots,
            left_result,
            right_result,
            n_result,
        )
        final_title = label("兩條篩選路線，收回同一個答案", 31, INK, "BOLD")
        final_title.move_to(UP * 3.0)
        left_caption = label("下方弧段不跨 y 軸", 26, CORAL, "BOLD")
        left_caption.move_to([-3.7, 2.12, 0])
        left_values = MathTex(
            r"k=-1,2,3,4,5",
            font_size=38,
            color=REGION,
        ).move_to([-3.7, 1.18, 0])
        left_count = MathTex("m=5", font_size=50, color=POINT)
        left_count.move_to([-3.7, 0.12, 0])
        right_caption = label("完全平方，再檢查正負", 26, REGION, "BOLD")
        right_caption.move_to([3.7, 2.12, 0])
        right_candidates = VGroup(
            VGroup(
                MathTex(r"k=-1:\ 2", font_size=36, color=REGION),
                label("可行", 22, REGION, "BOLD"),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                MathTex(r"k=2:\ -3,-1", font_size=36, color=CORAL),
                label("不合", 22, CORAL, "BOLD"),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.34).move_to([3.7, 0.85, 0])
        right_count = MathTex("n=1", font_size=50, color=POINT)
        right_count.move_to([3.7, -0.38, 0])
        arrows = VGroup(
            Line([-3.7, -0.52, 0], [-1.25, -1.45, 0], color=MUTED, stroke_width=3),
            Line([3.7, -0.92, 0], [1.25, -1.45, 0], color=MUTED, stroke_width=3),
        )
        final_pair = MathTex(
            r"(m,n)=(5,1)",
            font_size=62,
            color=INK,
        ).move_to([0, -2.22, 0])
        final_pair[0].set_color(POINT)
        final_box = SurroundingRectangle(
            final_pair,
            color=REGION,
            buff=0.28,
            stroke_width=3,
        )

        self.play(FadeOut(candidate_test_group), FadeIn(final_title), run_time=0.7)
        self.play(FadeIn(left_caption), Write(left_values), FadeIn(right_caption))
        self.play(Write(left_count), FadeIn(right_candidates), Write(right_count), run_time=0.85)
        # Beat 17 reveal_ordered_pair: settled semantic step.
        self.next_slide()
        self.play(Create(arrows), run_time=0.55)
        self.play(Write(final_pair), Create(final_box), run_time=0.9)
