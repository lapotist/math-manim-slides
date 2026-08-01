"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q8."""

from __future__ import annotations

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
    Axes,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
    ReplacementTransform,
    Succession,
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


class Tcfs115Q08Slide(CarloSlide):
    """Count distinct horizontal-line intersections via two shifted rows."""

    lesson_id = "carlo.tcfs_115_math_gifted.q08"

    @staticmethod
    def boundary_case(tex: str, count: str, note: str, color: str) -> VGroup:
        """Make one compact, unframed boundary-case column."""
        condition = MathTex(tex, font_size=42, color=color)
        result = label(count, 43, color, "BOLD")
        explanation = label(note, 22, MUTED, "MEDIUM")
        return VGroup(condition, result, explanation).arrange(DOWN, buff=0.24)

    @staticmethod
    def row_dot(position: np.ndarray, color: str, *, radius: float = 0.065) -> Dot:
        return Dot(position, radius=radius, color=color).set_z_index(4)

    @staticmethod
    def dense_row(start_x: float, y: float, step: float, color: str) -> VGroup:
        """Represent all 51 row entries without drawing all 51 parabolas."""
        return VGroup(
            *(
                Dot([start_x + index * step, y, 0], radius=0.032, color=color)
                for index in range(51)
            )
        )

    @staticmethod
    def overlap_connectors(
        start_x: float,
        step: float,
        offset: int,
        top_y: float,
        bottom_y: float,
        *,
        stroke_width: float = 1.2,
    ) -> VGroup:
        """Connect entries that occupy the same coordinate for integer offset."""
        return VGroup(
            *(
                Line(
                    [start_x + (index + offset) * step, top_y, 0],
                    [start_x + (index + offset) * step, bottom_y, 0],
                    color=PURPLE,
                    stroke_width=stroke_width,
                ).set_opacity(0.52)
                for index in range(51 - offset)
            )
        )

    @staticmethod
    def span_marker(left_x: float, right_x: float, y: float, text: str) -> VGroup:
        """Label the inclusive overlap span without a decorative container."""
        span = Line([left_x, y, 0], [right_x, y, 0], color=PURPLE, stroke_width=3)
        ticks = VGroup(
            Line([left_x, y - 0.09, 0], [left_x, y + 0.09, 0], color=PURPLE),
            Line([right_x, y - 0.09, 0], [right_x, y + 0.09, 0], color=PURPLE),
        )
        caption = label(text, 26, PURPLE, "BOLD")
        caption.next_to(span, UP, buff=0.1)
        return VGroup(span, ticks, caption)

    def construct(self) -> None:
        heading = label("第 8 題｜拋物線的交點碰撞", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        axes = Axes(
            x_range=[-2, 10, 2],
            y_range=[0, 2.5, 0.5],
            x_length=12.6,
            y_length=4.45,
            tips=False,
            axis_config={"color": HAIRLINE, "stroke_width": 2},
        ).shift(DOWN * 0.72)
        curve_colors = ("#59616A", "#6F7780", "#858E97", "#9BA4AD", MUTED)
        centers = tuple(2 * index for index in range(5))
        curves = VGroup(
            *(
                axes.plot(
                    lambda x, center=center: (x - center) ** 2,
                    x_range=[center - 1.55, center + 1.55],
                    color=color,
                    stroke_width=3.2,
                    use_smoothing=False,
                )
                for center, color in zip(centers, curve_colors, strict=True)
            )
        )
        vertices = VGroup(
            *(Dot(axes.c2p(center, 0), radius=0.06, color=INK) for center in centers)
        )
        vertex_labels = VGroup(
            *(
                label(str(center), 19, INK, "MEDIUM").next_to(
                    axes.c2p(center, 0), DOWN, buff=0.14
                )
                for center in centers
            )
        )
        family_prompt = label(
            "同一條水平線切過去，每條會提供幾個點？",
            32,
            INK,
            "BOLD",
            t2c={"每條": POINT},
        ).move_to(UP * 3.05)

        # Beat 01 parabola_family: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), Create(axes), run_time=0.9)
        self.play(
            LaggedStart(
                *(
                    Create(curve, rate_func=rate_functions.ease_in_out_sine)
                    for curve in curves
                ),
                lag_ratio=0.16,
            ),
            run_time=2.1,
        )
        self.play(
            LaggedStart(
                *(
                    GrowFromCenter(dot)
                    for dot in vertices
                ),
                *(
                    FadeIn(text, shift=UP * 0.05)
                    for text in vertex_labels
                ),
                lag_ratio=0.07,
            ),
            FadeIn(family_prompt),
            run_time=1.1,
        )

        t_tracker = ValueTracker(0.48)
        horizontal_line = always_redraw(
            lambda: Line(
                axes.c2p(-1.45, t_tracker.get_value() ** 2),
                axes.c2p(9.45, t_tracker.get_value() ** 2),
                color=POINT,
                stroke_width=4,
            ).set_z_index(2)
        )
        left_dots = VGroup(
            *(
                always_redraw(
                    lambda center=center: self.row_dot(
                        axes.c2p(
                            center - t_tracker.get_value(),
                            t_tracker.get_value() ** 2,
                        ),
                        BLUE,
                        radius=0.075,
                    )
                )
                for center in centers
            )
        )
        right_dots = VGroup(
            *(
                always_redraw(
                    lambda center=center: self.row_dot(
                        axes.c2p(
                            center + t_tracker.get_value(),
                            t_tracker.get_value() ** 2,
                        ),
                        REGION,
                        radius=0.075,
                    )
                )
                for center in centers
            )
        )
        dynamic_dots = VGroup(left_dots, right_dots)
        two_each = label(
            "每條：左 1 點 ＋ 右 1 點",
            27,
            INK,
            "BOLD",
            t2c={"左 1 點": BLUE, "右 1 點": REGION},
        ).move_to(UP * 3.04)

        # Beat 02 sweep_horizontal_line: settled semantic step.
        self.next_slide(loop=True)
        self.remove(family_prompt)
        self.add(horizontal_line, dynamic_dots, two_each)
        self.wait(0.35)
        self.play(
            t_tracker.animate.set_value(0.76),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.3)
        self.play(
            t_tracker.animate.set_value(0.48),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.35)

        # Beat 03 count_nominal_hits: settled semantic step.
        self.next_slide()
        plot_static = VGroup(axes, curves, vertices, vertex_labels)
        self.play(
            FadeOut(plot_static),
            FadeOut(horizontal_line),
            FadeOut(dynamic_dots),
            FadeOut(two_each),
            run_time=0.8,
        )
        below_case = self.boundary_case(r"k<0", "0 點", "水平線在頂點下方", CORAL)
        tangent_case = self.boundary_case(r"k=0", "51 點", "只碰到 51 個頂點", MUTED)
        positive_case = self.boundary_case(
            r"k>0", "51 x 2 = 102", "每條都有左右標記", POINT
        )
        cases = VGroup(below_case, tangent_case, positive_case).arrange(
            RIGHT, buff=1.65, aligned_edge=UP
        ).move_to(UP * 1.05)
        separators = VGroup(
            Line([-2.45, -0.45, 0], [-2.45, 2.35, 0], color=HAIRLINE),
            Line([2.1, -0.45, 0], [2.1, 2.35, 0], color=HAIRLINE),
        )
        nominal = VGroup(
            label("102 個來源標記", 36, POINT, "BOLD"),
            label("但題目只有", 25, MUTED, "MEDIUM"),
            label("76 個相異位置", 39, PURPLE, "BOLD"),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.72)
        missing_prompt = label(
            "少掉的 26 個，去哪裡了？", 30, INK, "BOLD", t2c={"26": PURPLE}
        ).next_to(nominal, DOWN, buff=0.36)
        self.play(
            LaggedStart(*(FadeIn(case, shift=UP * 0.12) for case in cases), lag_ratio=0.2),
            FadeIn(separators),
            run_time=1.35,
        )
        self.play(FadeIn(nominal), FadeIn(missing_prompt), run_time=0.9)

        # Beat 04 observe_collision: settled semantic step.
        self.next_slide()
        self.play(FadeOut(cases), FadeOut(separators), FadeOut(nominal), FadeOut(missing_prompt))
        t_tracker.set_value(0.48)
        self.play(
            FadeIn(plot_static),
            FadeIn(horizontal_line),
            FadeIn(dynamic_dots),
            run_time=0.9,
        )
        collision_title = label(
            "把水平距離調成 1", 31, INK, "BOLD", t2c={"1": POINT}
        ).move_to(UP * 3.05)
        self.play(FadeIn(collision_title), run_time=0.45)
        # Beat 05 compare_collision_times: settled semantic step.
        self.next_slide()
        self.play(
            t_tracker.animate.set_value(1.0),
            run_time=1.7,
            rate_func=rate_functions.ease_in_out_sine,
        )
        collision_positions = (1, 3, 5, 7)
        collision_rings = VGroup(
            *(
                Circle(radius=0.17, color=PURPLE, stroke_width=4).move_to(
                    axes.c2p(position, 1)
                )
                for position in collision_positions
            )
        ).set_z_index(6)
        focus_collision = axes.c2p(3, 1)
        source_guides = VGroup(
            DashedLine(
                axes.c2p(2, 0), focus_collision, color=REGION, stroke_width=3
            ),
            DashedLine(axes.c2p(4, 0), focus_collision, color=BLUE, stroke_width=3),
        ).set_z_index(1)
        guide_labels = VGroup(
            label("右點", 21, REGION, "BOLD").move_to(axes.c2p(2.35, 0.55)),
            label("左點", 21, BLUE, "BOLD").move_to(axes.c2p(3.65, 0.55)),
        )
        collision_count = label(
            "10 個來源標記  →  6 個相異位置",
            31,
            INK,
            "BOLD",
            t2c={"10": POINT, "6": PURPLE},
        ).move_to(UP * 2.48)
        self.play(
            LaggedStart(*(Create(ring) for ring in collision_rings), lag_ratio=0.12),
            Create(source_guides),
            FadeIn(guide_labels),
            run_time=1.1,
        )
        # Beat 06 name_first_collision: settled semantic step.
        self.next_slide()
        self.play(
            Succession(FadeOut(collision_title), FadeIn(collision_count)),
            run_time=0.65,
        )
        self.play(Circumscribe(collision_rings[1], color=PURPLE), run_time=0.8)
        self.wait(0.3)

        # Beat 07 compress_to_number_line: settled semantic step.
        self.next_slide()
        horizontal_line.clear_updaters()
        for dot in (*left_dots, *right_dots):
            dot.clear_updaters()
        row_x = lambda value: -5.0 + (value + 1)  # noqa: E731
        top_y = 0.55
        bottom_y = -0.75
        top_baseline = Line([-5.35, top_y, 0], [5.35, top_y, 0], color=HAIRLINE)
        bottom_baseline = Line([-5.35, bottom_y, 0], [5.35, bottom_y, 0], color=HAIRLINE)
        row_labels = VGroup(
            label("左交點", 24, BLUE, "BOLD").move_to([-6.15, top_y, 0]),
            label("右交點", 24, REGION, "BOLD").move_to([-6.15, bottom_y, 0]),
        )
        coordinate_labels = VGroup(
            *(
                label(str(value), 18, MUTED, "MEDIUM").move_to(
                    [row_x(value), bottom_y - 0.42, 0]
                )
                for value in (-1, 1, 3, 5, 7, 9)
            )
        )
        align_guides = VGroup(
            *(
                DashedLine(
                    [row_x(value), top_y, 0],
                    [row_x(value), bottom_y, 0],
                    color=PURPLE,
                    stroke_width=2,
                )
                for value in (1, 3, 5, 7)
            )
        )
        compression_title = label(
            "曲線淡去，只留下橫坐標", 32, INK, "BOLD", t2c={"橫坐標": POINT}
        ).move_to(UP * 2.72)
        same_x_note = label(
            "上下同一格 ＝ 同一個相異交點",
            28,
            INK,
            "MEDIUM",
            t2c={"同一格": PURPLE},
        ).move_to(DOWN * 2.25)
        self.play(
            FadeOut(plot_static),
            FadeOut(horizontal_line),
            FadeOut(source_guides),
            FadeOut(guide_labels),
            FadeOut(collision_rings),
            FadeOut(collision_count),
            FadeIn(top_baseline),
            FadeIn(bottom_baseline),
            FadeIn(row_labels),
            FadeIn(compression_title),
            run_time=0.9,
        )
        left_targets = [
            self.row_dot(np.array([row_x(center - 1), top_y, 0]), BLUE)
            for center in centers
        ]
        right_targets = [
            self.row_dot(np.array([row_x(center + 1), bottom_y, 0]), REGION)
            for center in centers
        ]
        self.play(
            *(
                Transform(dot, target)
                for dot, target in zip(left_dots, left_targets, strict=True)
            ),
            *(
                Transform(dot, target)
                for dot, target in zip(right_dots, right_targets, strict=True)
            ),
            run_time=1.45,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            FadeIn(coordinate_labels),
            Create(align_guides),
            FadeIn(same_x_note),
            run_time=0.85,
        )
        small_rows = VGroup(
            top_baseline,
            bottom_baseline,
            row_labels,
            coordinate_labels,
            left_dots,
            right_dots,
        )

        # Beat 08 define_offset_t: settled semantic step.
        self.next_slide()
        self.play(FadeOut(align_guides), FadeOut(same_x_note), FadeOut(compression_title))
        definition_title = label(
            "把水平距離命名為 t", 31, INK, "BOLD", t2c={"t": POINT}
        ).move_to(UP * 3.0)
        curve_equation = MathTex(r"(x-2j)^2=k", font_size=39, color=INK)
        curve_equation.move_to(UP * 2.2)
        distance_equation = MathTex(
            r"x=2j\pm\sqrt{k}", r",\qquad t=\sqrt{k}\ge 0",
            font_size=39,
            color=INK,
        ).move_to(UP * 1.43)
        distance_equation[1].set_color(POINT)
        left_formula = MathTex(
            r"L_j=2j-t", r":\ -t,\ 2-t,\ldots,\ 100-t",
            font_size=34,
            color=INK,
        )
        left_formula[0].set_color(BLUE)
        left_formula.move_to(DOWN * 1.65)
        right_formula = MathTex(
            r"R_j=2j+t", r":\ t,\ 2+t,\ldots,\ 100+t",
            font_size=34,
            color=INK,
        )
        right_formula[0].set_color(REGION)
        right_formula.next_to(left_formula, DOWN, buff=0.34)
        index_note = MathTex(r"j=0,1,\ldots,50", font_size=29, color=MUTED)
        index_note.next_to(right_formula, RIGHT, buff=0.45)
        self.play(FadeIn(definition_title), FadeIn(curve_equation), run_time=0.75)
        self.play(FadeIn(distance_equation), run_time=0.9)
        self.play(
            FadeIn(left_formula),
            FadeIn(right_formula),
            FadeIn(index_note),
            run_time=1.15,
        )

        # Beat 09 pose_76_count: settled semantic step.
        self.next_slide()
        formula_group = VGroup(
            definition_title,
            curve_equation,
            distance_equation,
            left_formula,
            right_formula,
            index_note,
        )
        self.play(
            FadeOut(formula_group),
            small_rows.animate.set_opacity(0.2),
            run_time=0.65,
        )
        deficit = MathTex(
            "102", "-", "76", "=", "26",
            font_size=76,
            color=INK,
        ).move_to(UP * 0.75)
        deficit[0].set_color(POINT)
        deficit[2].set_color(PURPLE)
        deficit[4].set_color(PURPLE)
        deficit_note = label("要合併掉 26 個重複標記", 30, MUTED, "MEDIUM")
        deficit_note.next_to(deficit, DOWN, buff=0.35)
        overlap_question = label(
            "哪一個 t，會產生剛好的重疊？",
            34,
            INK,
            "BOLD",
            t2c={"t": POINT, "重疊": PURPLE},
        ).next_to(deficit_note, DOWN, buff=0.62)
        self.play(FadeIn(deficit), run_time=0.9)
        self.play(FadeIn(deficit_note), FadeIn(overlap_question), run_time=0.75)

        # Beat 10 derive_collision_condition: settled semantic step.
        self.next_slide()
        self.play(
            FadeOut(deficit),
            FadeOut(deficit_note),
            FadeOut(overlap_question),
            FadeOut(small_rows),
            run_time=0.65,
        )
        condition_title = label(
            "任取一個重合位置", 31, INK, "BOLD", t2c={"重合": PURPLE}
        ).move_to(UP * 3.0)
        left_token = VGroup(
            Rectangle(
                width=2.25,
                height=0.8,
                color=BLUE,
                fill_color=BLUE,
                fill_opacity=0.09,
                stroke_width=3,
            ),
            MathTex(r"2j-t", font_size=39, color=BLUE),
        ).move_to([-3.9, 1.65, 0])
        right_token = VGroup(
            Rectangle(
                width=2.25,
                height=0.8,
                color=REGION,
                fill_color=REGION,
                fill_opacity=0.09,
                stroke_width=3,
            ),
            MathTex(r"2i+t", font_size=39, color=REGION),
        ).move_to([3.9, 1.65, 0])
        collision_dot = Dot([0, 1.65, 0], radius=0.12, color=PURPLE)
        arrows = VGroup(
            Arrow(left_token.get_right(), collision_dot.get_left(), buff=0.12, color=BLUE),
            Arrow(
                right_token.get_left(), collision_dot.get_right(), buff=0.12, color=REGION
            ),
        )
        derivation = VGroup(
            MathTex(r"2j-t=2i+t", font_size=43, color=INK),
            MathTex(r"2(j-i)=2t", font_size=41, color=INK),
            MathTex(r"t=j-i\in\mathbb Z", font_size=45, color=POINT),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 0.2)
        noninteger_note = MathTex(
            r"t\notin\mathbb Z\quad\Longrightarrow\quad |L\cup R|=102",
            font_size=31,
            color=MUTED,
        ).move_to(DOWN * 1.85)
        integer_line = NumberLine(
            x_range=[0, 50, 5],
            length=9.6,
            include_ticks=True,
            include_tip=False,
            color=HAIRLINE,
            stroke_width=2.5,
        ).move_to(DOWN * 2.75)
        integer_labels = VGroup(
            *(
                MathTex(str(value), font_size=21, color=MUTED).next_to(
                    integer_line.n2p(value), DOWN, buff=0.1
                )
                for value in (0, 10, 20, 30, 40, 50)
            )
        )
        valid_range = MathTex(r"1\le t\le 50", font_size=34, color=POINT)
        valid_range.next_to(integer_line, UP, buff=0.14)
        self.play(
            FadeIn(condition_title),
            FadeIn(left_token),
            FadeIn(right_token),
            GrowFromCenter(collision_dot),
            Create(arrows),
            run_time=1.0,
        )
        self.play(FadeIn(derivation[0]), run_time=0.65)
        # Beat 11 solve_collision_congruence: settled semantic step.
        self.next_slide()
        self.play(FadeIn(derivation[1]), run_time=0.55)
        self.play(FadeIn(derivation[2]), run_time=0.7)
        # Beat 12 state_collision_period: settled semantic step.
        self.next_slide()
        self.play(FadeIn(noninteger_note), Create(integer_line), FadeIn(integer_labels))
        self.play(FadeIn(valid_range), run_time=0.55)

        # Beat 13 count_overlap: settled semantic step.
        self.next_slide()
        condition_group = VGroup(
            condition_title,
            left_token,
            right_token,
            collision_dot,
            arrows,
            derivation,
            noninteger_note,
            integer_line,
            integer_labels,
            valid_range,
        )
        self.play(FadeOut(condition_group), run_time=0.65)
        dense_start = -5.2
        dense_step = 0.14
        dense_top_y = 0.35
        dense_bottom_y = -0.62
        demonstration_t = 8
        dense_left = self.dense_row(dense_start, dense_top_y, dense_step, BLUE)
        dense_right = self.dense_row(dense_start, dense_bottom_y, dense_step, REGION)
        dense_labels = VGroup(
            MathTex(
                r"L:\ -t,\ 2-t,\ldots,100-t", font_size=32, color=BLUE
            ).move_to(UP * 2.25),
            MathTex(
                r"R:\ t,\ 2+t,\ldots,100+t", font_size=32, color=REGION
            ).move_to(UP * 1.65),
        )
        row_count_labels = VGroup(
            label("51 點", 22, BLUE, "BOLD").move_to([6.05, dense_top_y, 0]),
            label("51 點", 22, REGION, "BOLD").move_to([6.05, dense_bottom_y, 0]),
        )
        shift_arrow = Arrow(
            [dense_start, -1.35, 0],
            [dense_start + demonstration_t * dense_step, -1.35, 0],
            buff=0,
            color=POINT,
            stroke_width=4,
        )
        shift_label = label("向右 t 格", 23, POINT, "BOLD")
        shift_label.next_to(shift_arrow, DOWN, buff=0.12)
        self.play(FadeIn(dense_labels), FadeIn(dense_left), FadeIn(dense_right), run_time=0.9)
        self.play(
            dense_right.animate.shift(RIGHT * demonstration_t * dense_step),
            GrowFromCenter(shift_arrow),
            FadeIn(shift_label),
            run_time=1.35,
            rate_func=rate_functions.ease_in_out_sine,
        )
        demonstration_connectors = self.overlap_connectors(
            dense_start,
            dense_step,
            demonstration_t,
            dense_top_y,
            dense_bottom_y,
        )
        overlap_span = self.span_marker(
            dense_start + demonstration_t * dense_step,
            dense_start + 50 * dense_step,
            0.88,
            "51 − t 個共同位置",
        )
        union_formula = MathTex(
            r"|L\cup R|=51+51-(51-t)=51+t",
            font_size=42,
            color=INK,
        ).move_to(DOWN * 2.42)
        union_formula.set_color_by_tex("51-t", PURPLE)
        union_formula.set_color_by_tex("51+t", POINT)
        # Beat 14 count_shared_positions: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(
                *(Create(line) for line in demonstration_connectors), lag_ratio=0.012
            ),
            FadeIn(overlap_span),
            FadeIn(row_count_labels),
            run_time=1.0,
        )
        self.play(FadeIn(union_formula), run_time=1.05)

        # Beat 15 solve_offset: settled semantic step.
        self.next_slide()
        solved_t = 25
        solved_connectors = self.overlap_connectors(
            dense_start,
            dense_step,
            solved_t,
            dense_top_y,
            dense_bottom_y,
            stroke_width=1.4,
        )
        solved_span = self.span_marker(
            dense_start + solved_t * dense_step,
            dense_start + 50 * dense_step,
            0.88,
            "51 − 25 = 26 個共同位置",
        )
        solve_equation = MathTex(
            r"51+t=76", r"\quad\Longrightarrow\quad", r"t=25",
            font_size=50,
            color=INK,
        ).move_to(DOWN * 2.25)
        solve_equation[2].set_color(POINT)
        distance_note = label(
            "每個交點離自己的頂點：25",
            27,
            MUTED,
            "MEDIUM",
            t2c={"25": POINT},
        ).next_to(solve_equation, DOWN, buff=0.24)
        self.play(
            FadeOut(demonstration_connectors),
            FadeOut(shift_arrow),
            FadeOut(shift_label),
            Succession(FadeOut(overlap_span), FadeIn(solved_span)),
            dense_right.animate.shift(RIGHT * (solved_t - demonstration_t) * dense_step),
            Succession(FadeOut(union_formula), FadeIn(solve_equation)),
            run_time=1.6,
            rate_func=rate_functions.ease_in_out_sine,
        )
        overlap_span = solved_span
        self.play(
            LaggedStart(*(Create(line) for line in solved_connectors), lag_ratio=0.018),
            FadeIn(distance_note),
            run_time=0.9,
        )
        self.play(Circumscribe(solve_equation[2], color=POINT), run_time=0.75)
        self.wait(0.3)
        dense_scene = VGroup(
            dense_labels,
            dense_left,
            dense_right,
            row_count_labels,
            overlap_span,
            solved_connectors,
            solve_equation,
            distance_note,
        )

        # Beat 16 recover_k: settled semantic step.
        self.next_slide()
        self.play(FadeOut(dense_scene), run_time=0.65)
        height_axes = Axes(
            x_range=[-30, 30, 10],
            y_range=[0, 650, 100],
            x_length=5.4,
            y_length=4.5,
            tips=False,
            axis_config={"color": HAIRLINE, "stroke_width": 2},
        ).move_to([-3.75, -0.25, 0])
        height_curve = height_axes.plot(
            lambda x: x**2,
            x_range=[-25, 25],
            color=MUTED,
            stroke_width=3,
            use_smoothing=False,
        )
        height_line = Line(
            height_axes.c2p(-27, 625),
            height_axes.c2p(27, 625),
            color=POINT,
            stroke_width=4,
        )
        height_points = VGroup(
            Dot(height_axes.c2p(-25, 625), radius=0.07, color=BLUE),
            Dot(height_axes.c2p(25, 625), radius=0.07, color=REGION),
        )
        offset_labels = VGroup(
            MathTex("-25", font_size=25, color=BLUE).next_to(
                height_axes.c2p(-25, 0), DOWN, buff=0.1
            ),
            MathTex("25", font_size=25, color=REGION).next_to(
                height_axes.c2p(25, 0), DOWN, buff=0.1
            ),
        )
        curve_name = MathTex(r"y=x^2", font_size=28, color=MUTED)
        curve_name.move_to(height_axes.c2p(16, 360))
        height_name = MathTex(r"y=k", font_size=29, color=POINT)
        height_name.next_to(height_line, UP, buff=0.12)
        solved_height_name = MathTex(r"y=625", font_size=29, color=POINT)
        solved_height_name.next_to(height_line, UP, buff=0.12)
        recover_title = label(
            "距離 25，對應到多高？", 31, INK, "BOLD", t2c={"25": POINT}
        ).move_to(UP * 3.0)
        recovery = VGroup(
            MathTex(r"t=\sqrt{k}", font_size=46, color=POINT),
            MathTex(r"k=t^2", font_size=46, color=INK),
            MathTex(r"=25^2", font_size=46, color=INK),
            MathTex(r"=625", font_size=62, color=POINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([3.2, -0.05, 0])
        self.play(FadeIn(recover_title), Create(height_axes), Create(height_curve), run_time=1.0)
        self.play(Create(height_line), FadeIn(height_points), FadeIn(offset_labels), run_time=0.8)
        # Beat 17 substitute_overlap_count: settled semantic step.
        self.next_slide()
        self.play(FadeIn(curve_name), FadeIn(height_name), FadeIn(recovery[0]), run_time=0.65)
        self.play(FadeIn(recovery[1]), run_time=0.55)
        self.play(FadeIn(recovery[2]), run_time=0.55)
        # Beat 18 solve_for_k: settled semantic step.
        self.next_slide()
        self.play(FadeIn(recovery[3]), run_time=0.65)
        self.play(
            Succession(FadeOut(height_name), FadeIn(solved_height_name)),
            run_time=0.55,
        )
        height_scene = VGroup(
            recover_title,
            height_axes,
            height_curve,
            height_line,
            height_points,
            offset_labels,
            curve_name,
            solved_height_name,
            recovery,
        )

        # Beat 19 verify_full_count: settled semantic step.
        self.next_slide()
        self.play(FadeOut(height_scene), run_time=0.65)
        compact_start = -6.2
        compact_step = 0.073
        compact_shift = solved_t * compact_step
        compact_top_y = 1.15
        compact_bottom_y = 0.48
        exact_left = self.dense_row(compact_start, compact_top_y, compact_step, BLUE)
        exact_right = self.dense_row(
            compact_start + compact_shift, compact_bottom_y, compact_step, REGION
        )
        exact_connectors = self.overlap_connectors(
            compact_start,
            compact_step,
            solved_t,
            compact_top_y,
            compact_bottom_y,
            stroke_width=1.0,
        )
        exact_rows_text = VGroup(
            MathTex(r"L=-25,-23,\ldots,75", font_size=29, color=BLUE),
            MathTex(r"R=25,27,\ldots,125", font_size=29, color=REGION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.55, 2.1, 0])
        overlap_check = MathTex(
            r"L\cap R=25,27,\ldots,75", r"\quad |L\cap R|=26",
            font_size=30,
            color=INK,
        ).move_to([-3.35, -0.35, 0])
        overlap_check[1].set_color(PURPLE)
        exact_count = MathTex(
            r"51+51-26=76", font_size=43, color=POINT
        ).move_to([-3.55, -1.25, 0])
        edge_note = label(
            "k=0 → 51；t 非整數 → 102",
            21,
            MUTED,
            "MEDIUM",
        ).move_to([-3.55, -2.05, 0])
        count_verification = VGroup(
            exact_rows_text,
            exact_left,
            exact_right,
            exact_connectors,
            overlap_check,
            exact_count,
            edge_note,
        )
        count_verification.shift(RIGHT * 3.55)

        verify_axes = Axes(
            x_range=[-5, 55, 10],
            y_range=[0, 650, 100],
            x_length=5.15,
            y_length=3.65,
            tips=False,
            axis_config={"color": HAIRLINE, "stroke_width": 2},
        ).move_to([3.75, -0.2, 0])
        first_parabola = verify_axes.plot(
            lambda x: x**2,
            x_range=[0, 25],
            color=BLUE,
            stroke_width=3,
            use_smoothing=False,
        )
        second_parabola = verify_axes.plot(
            lambda x: (x - 50) ** 2,
            x_range=[25, 50],
            color=REGION,
            stroke_width=3,
            use_smoothing=False,
        )
        verify_line = Line(
            verify_axes.c2p(-2, 625),
            verify_axes.c2p(52, 625),
            color=POINT,
            stroke_width=3.5,
        )
        verify_collision = Dot(verify_axes.c2p(25, 625), radius=0.09, color=PURPLE)
        collision_coordinate = MathTex(r"(25,625)", font_size=27, color=PURPLE)
        collision_coordinate.next_to(verify_collision, UP, buff=0.1)
        parabola_names = VGroup(
            MathTex(r"y=x^2", font_size=24, color=BLUE).move_to(
                verify_axes.c2p(10, 280)
            ),
            MathTex(r"y=(x-50)^2", font_size=24, color=REGION).move_to(
                verify_axes.c2p(43, 300)
            ),
        )
        verification_title = label(
            "把 76 一點不漏地數回來", 31, INK, "BOLD", t2c={"76": POINT}
        ).move_to(UP * 3.0)
        self.play(
            FadeIn(verification_title),
            FadeIn(exact_rows_text),
            FadeIn(exact_left),
            FadeIn(exact_right),
            Create(exact_connectors),
            run_time=1.0,
        )
        self.play(FadeIn(overlap_check), FadeIn(exact_count), FadeIn(edge_note), run_time=0.95)
        # Beat 20 recheck_union_count: settled semantic step.
        self.next_slide()
        self.play(
            count_verification.animate.shift(LEFT * 3.55),
            Create(verify_axes),
            Create(first_parabola),
            Create(second_parabola),
            Create(verify_line),
            run_time=1.15,
        )
        self.play(
            GrowFromCenter(verify_collision),
            FadeIn(collision_coordinate),
            FadeIn(parabola_names),
            run_time=0.75,
        )
        self.play(Circumscribe(exact_count, color=POINT), run_time=0.75)
        self.wait(0.3)
        verification_scene = VGroup(
            verification_title,
            count_verification,
            verify_axes,
            first_parabola,
            second_parabola,
            verify_line,
            verify_collision,
            collision_coordinate,
            parabola_names,
        )

        # Beat 21 consolidate: settled semantic step.
        self.next_slide()
        self.play(FadeOut(verification_scene), run_time=0.65)
        final_title = label(
            "從曲線碰撞，到兩排聯集", 33, INK, "BOLD", t2c={"碰撞": PURPLE}
        ).move_to(UP * 3.0)

        mini_axes = Axes(
            x_range=[0, 2, 1],
            y_range=[0, 1.1, 0.5],
            x_length=3.05,
            y_length=2.25,
            tips=False,
            axis_config={"color": HAIRLINE, "stroke_width": 1.8},
        ).move_to([-5.2, 0.55, 0])
        mini_curves = VGroup(
            mini_axes.plot(
                lambda x: x**2,
                x_range=[0, 1],
                color=BLUE,
                stroke_width=3,
                use_smoothing=False,
            ),
            mini_axes.plot(
                lambda x: (x - 2) ** 2,
                x_range=[1, 2],
                color=REGION,
                stroke_width=3,
                use_smoothing=False,
            ),
        )
        mini_line = Line(
            mini_axes.c2p(0, 1), mini_axes.c2p(2, 1), color=POINT, stroke_width=3
        )
        mini_collision = Dot(mini_axes.c2p(1, 1), radius=0.095, color=PURPLE)
        mini_caption = label("左右標記碰在一起", 23, MUTED, "MEDIUM")
        mini_caption.next_to(mini_axes, DOWN, buff=0.18)
        collision_icon = VGroup(
            mini_axes, mini_curves, mini_line, mini_collision, mini_caption
        )

        union_top = VGroup(
            *(Dot([-1.95 + index * 0.32, 0.94, 0], radius=0.045, color=BLUE) for index in range(9))
        )
        union_bottom = VGroup(
            *(Dot([-0.99 + index * 0.32, 0.2, 0], radius=0.045, color=REGION) for index in range(9))
        )
        union_links = VGroup(
            *(
                Line(
                    [-0.99 + index * 0.32, 0.94, 0],
                    [-0.99 + index * 0.32, 0.2, 0],
                    color=PURPLE,
                    stroke_width=1.5,
                )
                for index in range(6)
            )
        )
        union_caption = label("只扣掉共同位置", 23, MUTED, "MEDIUM")
        union_caption.move_to([-0.65, -0.82, 0])
        union_icon = VGroup(union_top, union_bottom, union_links, union_caption)

        final_chain = VGroup(
            MathTex(r"|L\cup R|=51+t", font_size=37, color=INK),
            MathTex(r"51+t=76", font_size=40, color=INK),
            MathTex(r"t=25", font_size=43, color=POINT),
            MathTex(r"k=t^2=625", font_size=49, color=POINT),
        ).arrange(DOWN, buff=0.27).move_to([4.65, 0.25, 0])
        final_box = SurroundingRectangle(
            final_chain[-1], color=POINT, buff=0.22, stroke_width=3
        )
        flow_arrows = VGroup(
            Arrow([-3.25, 0.5, 0], [-2.25, 0.5, 0], buff=0.1, color=MUTED),
            Arrow([1.82, 0.5, 0], [2.38, 0.5, 0], buff=0.06, color=MUTED),
        )
        final_answer = label("答案：625", 32, POINT, "BOLD")
        final_answer.move_to([4.65, -2.25, 0])
        self.play(FadeIn(final_title), FadeIn(collision_icon), run_time=0.8)
        self.play(Create(flow_arrows[0]), FadeIn(union_icon), run_time=0.75)
        # Beat 22 reveal_k_value: settled semantic step.
        self.next_slide()
        self.play(Create(flow_arrows[1]), run_time=0.45)
        self.play(
            LaggedStart(*(FadeIn(line) for line in final_chain), lag_ratio=0.2),
            run_time=1.35,
        )
        self.play(Create(final_box), FadeIn(final_answer), run_time=0.7)
        self.wait(0.5)
