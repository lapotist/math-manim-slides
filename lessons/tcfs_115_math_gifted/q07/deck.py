"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q7."""

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
    Circumscribe,
    Create,
    Cross,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Square,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    TransformMatchingTex,
    VGroup,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, ORIGIN, RIGHT, UP


class Tcfs115Q07Slide(CarloSlide):
    """Discover conjugate invariants before isolating the requested cross term."""

    lesson_id = "carlo.tcfs_115_math_gifted.q07"

    @staticmethod
    def pair_state(
        *,
        a_tex: str,
        cap_a_tex: str,
        width_value: int,
        height_value: int,
        area_tex: str,
    ) -> VGroup:
        """Build one exact state of the area-four exploration rectangle."""
        scale = 0.86
        body = Rectangle(
            width=width_value * scale,
            height=height_value * scale,
            color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.14,
        )
        state = MathTex(
            rf"a={a_tex},\quad A={cap_a_tex}",
            font_size=36,
            color=INK,
        )
        state.next_to(body, UP, buff=0.25)
        width_label = MathTex(
            rf"A+a={width_value}",
            font_size=31,
            color=BLUE,
        )
        width_label.next_to(body, DOWN, buff=0.18)
        height_label = MathTex(
            rf"A-a={height_value}",
            font_size=31,
            color=BLUE,
        )
        height_label.next_to(body, RIGHT, buff=0.2)
        area = MathTex(area_tex, font_size=34, color=POINT)
        area.move_to(body)
        return VGroup(body, state, width_label, height_label, area)

    @staticmethod
    def positivity_guard(symbol: str, variable: str, color: str) -> VGroup:
        """Show the variable strictly between the two radical bounds."""
        axis = Line(LEFT * 1.55, RIGHT * 1.55, color=HAIRLINE, stroke_width=3)
        left_tick = Line(UP * 0.1, DOWN * 0.1, color=MUTED, stroke_width=2)
        left_tick.move_to(axis.get_left())
        right_tick = left_tick.copy().move_to(axis.get_right())
        variable_dot = Dot(axis.point_from_proportion(0.61), radius=0.07, color=color)
        left_label = MathTex(rf"-{symbol}", font_size=25, color=MUTED)
        left_label.next_to(left_tick, DOWN, buff=0.12)
        right_label = MathTex(symbol, font_size=25, color=MUTED)
        right_label.next_to(right_tick, DOWN, buff=0.12)
        variable_label = MathTex(variable, font_size=27, color=color)
        variable_label.next_to(variable_dot, UP, buff=0.12)
        bound = MathTex(
            rf"{symbol}^2={variable}^2+{4 if symbol == 'A' else 9}",
            rf"\Rightarrow {symbol}>|{variable}|",
            font_size=29,
            color=INK,
        )
        bound[1].set_color(color)
        bound.next_to(axis, UP, buff=0.48)
        positive = MathTex(
            rf"{symbol}+{variable}>0,\quad {symbol}-{variable}>0",
            font_size=27,
            color=color,
        )
        positive.next_to(axis, DOWN, buff=0.55)
        return VGroup(
            axis,
            left_tick,
            right_tick,
            variable_dot,
            left_label,
            right_label,
            variable_label,
            bound,
            positive,
        )

    @staticmethod
    def grouped_row(lhs_tex: str, sign_tex: str, y: float) -> VGroup:
        """Lay out the two product expansions on identical semantic columns."""
        lhs = MathTex(lhs_tex, font_size=45, color=POINT).move_to([-4.55, y, 0])
        equals = MathTex("=", font_size=43, color=INK).move_to([-3.5, y, 0])
        common = MathTex(r"AB+ab", font_size=42, color=MUTED).move_to([-1.25, y, 0])
        sign = MathTex(sign_tex, font_size=44, color=INK).move_to([1.08, y, 0])
        target = MathTex("T", font_size=48, color=PURPLE).move_to([2.18, y, 0])
        common_box = SurroundingRectangle(
            common,
            color=MUTED,
            buff=0.17,
            stroke_width=2.5,
        )
        target_box = SurroundingRectangle(
            target,
            color=PURPLE,
            buff=0.19,
            stroke_width=3,
        )
        return VGroup(lhs, equals, common, sign, target, common_box, target_box)

    @staticmethod
    def value_badge(tex: str, caption: str, color: str, *, width: float = 1.75) -> VGroup:
        """Create a compact cause-and-effect token for the final recap."""
        body = Rectangle(
            width=width,
            height=1.25,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.1,
        )
        value = MathTex(tex, font_size=37, color=color)
        value.scale_to_fit_height(min(value.height, 0.53))
        value.move_to(body.get_center() + UP * 0.2)
        note = label(caption, 18, MUTED, "MEDIUM")
        note.move_to(body.get_center() + DOWN * 0.43)
        return VGroup(body, value, note)

    def construct(self) -> None:
        heading = label("第 7 題｜根式夥伴的隱藏乘積", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        opening_prompt = label(
            "不知道 a、b，目標為什麼仍可能固定？",
            34,
            INK,
            "BOLD",
            t2c={"目標": PURPLE, "固定": POINT},
        ).move_to(UP * 2.55)
        given = MathTex(
            r"\left(\sqrt{a^2+4}+a\right)",
            r"\left(\sqrt{b^2+9}+b\right)",
            "=",
            "7",
            font_size=49,
            color=INK,
        ).move_to(UP * 0.75)
        given[0].set_color(BLUE)
        given[1].set_color(REGION)
        given[3].set_color(POINT)
        first_factor_box = SurroundingRectangle(
            given[0], color=BLUE, buff=0.15, stroke_width=3
        )
        second_factor_box = SurroundingRectangle(
            given[1], color=REGION, buff=0.15, stroke_width=3
        )
        target_caption = label("題目要找的交叉項", 25, MUTED, "MEDIUM")
        target_caption.move_to(DOWN * 0.55)
        original_target = MathTex(
            r"a\sqrt{b^2+9}",
            "+",
            r"b\sqrt{a^2+4}",
            "=",
            "?",
            font_size=47,
            color=INK,
        ).move_to(DOWN * 1.45)
        original_target[0:3].set_color(PURPLE)
        original_target[4].set_color(POINT)

        # Beat 01 given_product: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(opening_prompt), run_time=0.8)
        self.play(Write(given), run_time=1.25)
        self.play(Create(first_factor_box), Create(second_factor_box), run_time=0.65)
        # Beat 02 expand_given_product: settled semantic step.
        self.next_slide()
        self.play(FadeIn(target_caption), Write(original_target), run_time=1.0)
        self.play(Circumscribe(original_target[0:3], color=PURPLE), run_time=0.8)

        # Beat 03 isolate_radical_pairs: settled semantic step.
        self.next_slide()

        definitions = VGroup(
            MathTex(r"A=\sqrt{a^2+4}", font_size=38, color=BLUE),
            MathTex(r"B=\sqrt{b^2+9}", font_size=38, color=REGION),
        ).arrange(RIGHT, buff=1.15)
        definitions.move_to(UP * 2.22)
        short_given = MathTex(
            r"(A+a)",
            r"(B+b)",
            "=",
            "7",
            font_size=51,
            color=INK,
        ).move_to(UP * 1.08)
        short_given[0].set_color(BLUE)
        short_given[1].set_color(REGION)
        short_given[3].set_color(POINT)
        guard_a = self.positivity_guard("A", "a", BLUE).scale(0.86)
        guard_b = self.positivity_guard("B", "b", REGION).scale(0.86)
        guard_a.move_to([-3.45, -0.85, 0])
        guard_b.move_to([3.45, -0.85, 0])
        positivity_note = label(
            "四個夥伴因子都為正｜矩形與除法都合法",
            25,
            MUTED,
            "MEDIUM",
            t2c={"都為正": POINT},
        ).move_to(DOWN * 3.15)

        opening_group = VGroup(
            opening_prompt,
            given,
            first_factor_box,
            second_factor_box,
            target_caption,
            original_target,
        )
        self.play(FadeOut(opening_group), FadeIn(definitions), Write(short_given), run_time=1.0)
        self.play(
            LaggedStart(Create(guard_a), Create(guard_b), lag_ratio=0.18),
            run_time=1.45,
        )
        self.play(FadeIn(positivity_note), run_time=0.55)

        loop_prompt = label(
            "先只看 A+a 與 A-a：兩邊一起變時，什麼不變？",
            32,
            INK,
            "BOLD",
            t2c={"A+a": BLUE, "A-a": BLUE, "不變": POINT},
        ).move_to(UP * 3.0)
        first_pair = self.pair_state(
            a_tex=r"-\frac32",
            cap_a_tex=r"\frac52",
            width_value=1,
            height_value=4,
            area_tex=r"1\times4",
        )
        first_pair.shift(DOWN * 0.22 - first_pair[0].get_center())
        setup_group = VGroup(definitions, short_given, guard_a, guard_b, positivity_note)
        self.play(FadeOut(setup_group), FadeIn(loop_prompt), FadeIn(first_pair), run_time=0.95)
        self.wait(0.3)

        # Beat 04 vary_first_pair: settled semantic step.
        self.next_slide(loop=True)

        square_state = self.pair_state(
            a_tex="0",
            cap_a_tex="2",
            width_value=2,
            height_value=2,
            area_tex=r"2\times2=4",
        )
        square_state.shift(DOWN * 0.22 - square_state[0].get_center())
        wide_state = self.pair_state(
            a_tex=r"\frac32",
            cap_a_tex=r"\frac52",
            width_value=4,
            height_value=1,
            area_tex=r"4\times1=4",
        )
        wide_state.shift(DOWN * 0.22 - wide_state[0].get_center())
        return_state = self.pair_state(
            a_tex=r"-\frac32",
            cap_a_tex=r"\frac52",
            width_value=1,
            height_value=4,
            area_tex=r"1\times4",
        )
        return_state.shift(DOWN * 0.22 - return_state[0].get_center())

        self.play(
            Transform(first_pair, square_state),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.45)
        self.play(
            Transform(first_pair, wide_state),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.45)
        self.play(
            Transform(first_pair, return_state),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_sine,
        )

        # Beat 05 discover_first_invariant: settled semantic step.
        self.next_slide()

        proof_title = label("為什麼面積總是 4？", 33, INK, "BOLD")
        proof_title.move_to(UP * 3.0)
        a_square = Square(
            side_length=2.35,
            color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.14,
        ).move_to([-4.15, -0.05, 0])
        area_four = label("面積 4", 34, POINT, "BOLD").move_to(a_square)
        proof_lines = VGroup(
            MathTex(r"(A+a)(A-a)", font_size=44, color=BLUE),
            MathTex(r"=A^2-a^2", font_size=44, color=INK),
            MathTex(r"=(a^2+4)-a^2", font_size=44, color=INK),
            MathTex(r"=4", font_size=58, color=POINT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        proof_lines.move_to([2.35, -0.05, 0])
        a_equation = MathTex(
            r"(A+a)(A-a)",
            "=",
            "4",
            font_size=36,
            color=INK,
        )
        a_equation[0].set_color(BLUE)
        a_equation[2].set_color(POINT)
        a_equation.next_to(a_square, DOWN, buff=0.32)

        self.play(ReplacementTransform(loop_prompt, proof_title), run_time=0.55)
        self.play(
            ReplacementTransform(first_pair[0], a_square),
            FadeOut(VGroup(*first_pair[1:])),
            run_time=1.0,
        )
        self.play(FadeIn(area_four), Write(proof_lines[0]), run_time=0.7)
        # Beat 06 compare_first_pair: settled semantic step.
        self.next_slide()
        self.play(Write(proof_lines[1]), run_time=0.65)
        self.play(Write(proof_lines[2]), run_time=0.75)
        # Beat 07 state_first_invariant: settled semantic step.
        self.next_slide()
        self.play(Write(proof_lines[3]), Circumscribe(area_four, color=POINT), run_time=0.75)
        self.play(TransformFromCopy(proof_lines[0], a_equation[0]), FadeIn(a_equation[1:]), run_time=0.7)

        # Beat 08 mirror_second_pair: settled semantic step.
        self.next_slide()

        mirror_title = label("同一個結構，第二組留下 9", 33, INK, "BOLD")
        mirror_title.move_to(UP * 3.0)
        b_square = Square(
            side_length=2.85,
            color=REGION,
            stroke_width=4,
            fill_color=REGION,
            fill_opacity=0.13,
        ).move_to([3.65, -0.02, 0])
        area_nine = label("面積 9", 34, POINT, "BOLD").move_to(b_square)
        b_derivation = MathTex(
            r"(B+b)(B-b)",
            "=",
            r"B^2-b^2",
            "=",
            r"(b^2+9)-b^2",
            "=",
            "9",
            font_size=37,
            color=INK,
        ).move_to(UP * 2.12)
        b_derivation[0].set_color(REGION)
        b_derivation[6].set_color(POINT)
        b_equation = MathTex(
            r"(B+b)(B-b)",
            "=",
            "9",
            font_size=36,
            color=INK,
        )
        b_equation[0].set_color(REGION)
        b_equation[2].set_color(POINT)
        b_equation.next_to(b_square, DOWN, buff=0.32)

        self.play(
            ReplacementTransform(proof_title, mirror_title),
            FadeOut(proof_lines),
            run_time=0.65,
        )
        self.play(TransformFromCopy(a_square, b_square), run_time=0.85)
        self.play(
            LaggedStart(*(Write(part) for part in b_derivation), lag_ratio=0.12),
            run_time=1.5,
        )
        # Beat 09 state_second_invariant: settled semantic step.
        self.next_slide()
        self.play(FadeIn(area_nine), Circumscribe(b_derivation[6], color=POINT), run_time=0.7)
        self.play(TransformFromCopy(b_derivation[0], b_equation[0]), FadeIn(b_equation[1:]), run_time=0.65)

        # Beat 10 combine_invariants: settled semantic step.
        self.next_slide()

        combine_title = label("兩個固定乘積合起來", 33, INK, "BOLD")
        combine_title.move_to(UP * 3.02)
        area_product = MathTex(
            "4",
            r"\times",
            "9",
            "=",
            "36",
            font_size=54,
            color=INK,
        ).move_to(UP * 1.95)
        area_product[0].set_color(BLUE)
        area_product[2].set_color(REGION)
        area_product[4].set_color(POINT)
        combined = MathTex(
            r"(A+a)",
            r"(B+b)",
            r"(A-a)",
            r"(B-b)",
            "=",
            "36",
            font_size=43,
            color=INK,
        ).move_to(DOWN * 0.1)
        combined[0].set_color(BLUE)
        combined[1].set_color(REGION)
        combined[2].set_color(BLUE).set_opacity(0.62)
        combined[3].set_color(REGION).set_opacity(0.62)
        combined[5].set_color(POINT)
        plus_box = SurroundingRectangle(
            VGroup(combined[0], combined[1]),
            color=POINT,
            buff=0.16,
            stroke_width=3,
        )
        minus_box = SurroundingRectangle(
            VGroup(combined[2], combined[3]),
            color=MUTED,
            buff=0.16,
            stroke_width=2.5,
        )
        known_value = MathTex(r"=7", font_size=35, color=POINT)
        known_value.next_to(plus_box, DOWN, buff=0.2)
        shadow_question = MathTex(r"=?", font_size=35, color=MUTED)
        shadow_question.next_to(minus_box, DOWN, buff=0.2)
        total_note = label("總乘積固定", 24, MUTED, "MEDIUM")
        total_note.next_to(combined[5], DOWN, buff=0.7)

        invariant_context = VGroup(
            a_square,
            area_four,
            a_equation,
            b_square,
            area_nine,
            b_equation,
            b_derivation,
        )
        self.play(
            ReplacementTransform(mirror_title, combine_title),
            FadeOut(b_derivation),
            run_time=0.55,
        )
        self.play(
            TransformFromCopy(a_equation[2], area_product[0]),
            FadeIn(area_product[1]),
            TransformFromCopy(b_equation[2], area_product[2]),
            FadeIn(area_product[3]),
            run_time=0.8,
        )
        self.play(Write(area_product[4]), run_time=0.5)
        # Beat 11 collect_invariant_sum: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(*(Write(part) for part in combined), lag_ratio=0.1),
            FadeOut(VGroup(*invariant_context[:6])),
            run_time=1.45,
        )
        self.play(
            Create(plus_box),
            Create(minus_box),
            FadeIn(known_value),
            FadeIn(shadow_question),
            FadeIn(total_note),
            run_time=0.8,
        )

        # Beat 12 pose_target: settled semantic step.
        self.next_slide()

        target_title = label("目標藏在乘法表的交叉位置", 33, INK, "BOLD")
        target_title.move_to(UP * 3.05)
        combined_context = VGroup(
            combined,
            plus_box,
            minus_box,
            known_value,
            shadow_question,
            total_note,
        )
        target_t = MathTex(
            "T",
            "=",
            "aB",
            "+",
            "bA",
            font_size=49,
            color=PURPLE,
        ).move_to(UP * 1.05)
        cells = VGroup(
            *(
                Rectangle(width=1.8, height=0.9, stroke_width=2.5)
                for _ in range(4)
            )
        ).arrange_in_grid(rows=2, cols=2, buff=0)
        cells.move_to(DOWN * 0.85)
        cells[0].set_stroke(MUTED).set_fill(MUTED, opacity=0.05)
        cells[3].set_stroke(MUTED).set_fill(MUTED, opacity=0.05)
        cells[1].set_stroke(PURPLE, width=3.5).set_fill(PURPLE, opacity=0.12)
        cells[2].set_stroke(PURPLE, width=3.5).set_fill(PURPLE, opacity=0.12)
        column_headers = VGroup(
            MathTex("B", font_size=31, color=REGION),
            MathTex("b", font_size=31, color=REGION),
        )
        for header, cell in zip(column_headers, cells[:2], strict=True):
            header.next_to(cell, UP, buff=0.16)
        row_headers = VGroup(
            MathTex("A", font_size=31, color=BLUE),
            MathTex("a", font_size=31, color=BLUE),
        )
        row_headers[0].next_to(cells[0], LEFT, buff=0.2)
        row_headers[1].next_to(cells[2], LEFT, buff=0.2)
        cell_contents = VGroup(
            MathTex("?", font_size=34, color=MUTED).move_to(cells[0]),
            MathTex("bA", font_size=34, color=PURPLE).move_to(cells[1]),
            MathTex("aB", font_size=34, color=PURPLE).move_to(cells[2]),
            MathTex("?", font_size=34, color=MUTED).move_to(cells[3]),
        )
        pose_prompt = label(
            "另外兩格會混入什麼？哪一組乘積能把它們消掉？",
            27,
            MUTED,
            "MEDIUM",
            t2c={"哪一組乘積": POINT},
        ).move_to(DOWN * 2.62)
        grid = VGroup(cells, column_headers, row_headers, cell_contents)

        self.play(
            ReplacementTransform(combine_title, target_title),
            FadeOut(area_product),
            combined_context.animate.scale(0.72).move_to([0, 2.12, 0]),
            run_time=0.8,
        )
        self.play(Write(target_t), run_time=0.7)
        self.play(Create(cells), FadeIn(column_headers), FadeIn(row_headers), run_time=0.85)
        self.play(
            LaggedStart(*(FadeIn(item) for item in cell_contents), lag_ratio=0.15),
            FadeIn(pose_prompt),
            run_time=0.95,
        )

        # Beat 13 build_shadow_product: settled semantic step.
        self.next_slide()

        shadow_title = label("從總乘積 36 除去已知的 7", 33, INK, "BOLD")
        shadow_title.move_to(UP * 3.05)
        division = MathTex(
            "36",
            r"\div",
            "7",
            "=",
            r"\frac{36}{7}",
            font_size=48,
            color=INK,
        ).move_to(UP * 0.9)
        division[0].set_color(POINT)
        division[2].set_color(POINT)
        division[4].set_color(POINT)
        shadow_equation = MathTex(
            r"(A-a)",
            r"(B-b)",
            "=",
            r"\frac{36}{7}",
            font_size=49,
            color=INK,
        ).move_to(DOWN * 0.75)
        shadow_equation[0].set_color(BLUE).set_opacity(0.78)
        shadow_equation[1].set_color(REGION).set_opacity(0.78)
        shadow_equation[3].set_color(POINT)
        shadow_box = SurroundingRectangle(
            shadow_equation,
            color=POINT,
            buff=0.22,
            stroke_width=3,
        )
        shadow_note = label(
            "影子乘積",
            25,
            MUTED,
            "MEDIUM",
        ).next_to(shadow_box, DOWN, buff=0.2)

        self.play(
            ReplacementTransform(target_title, shadow_title),
            FadeOut(VGroup(target_t, grid, pose_prompt)),
            run_time=0.65,
        )
        self.play(
            TransformFromCopy(combined[5], division[0]),
            FadeIn(division[1]),
            TransformFromCopy(known_value, division[2]),
            FadeIn(division[3]),
            run_time=0.85,
        )
        self.play(Write(division[4]), run_time=0.55)
        # Beat 14 name_shadow_product: settled semantic step.
        self.next_slide()
        self.play(
            TransformFromCopy(VGroup(combined[2], combined[3]), shadow_equation[0:2]),
            FadeIn(shadow_equation[2]),
            TransformFromCopy(division[4], shadow_equation[3]),
            run_time=1.0,
        )
        self.play(Create(shadow_box), FadeIn(shadow_note), run_time=0.6)
        self.play(combined_context.animate.set_opacity(0.28), run_time=0.45)

        # Beat 15 expand_known_product: settled semantic step.
        self.next_slide()

        known_title = label("先展開已知的加號乘積", 33, INK, "BOLD")
        known_title.move_to(UP * 3.05)
        known_factor = MathTex(
            r"(A+a)(B+b)=7",
            font_size=43,
            color=INK,
        ).move_to(UP * 2.05)
        known_factor.set_color_by_tex("A+a", BLUE)
        known_factor.set_color_by_tex("B+b", REGION)
        known_expanded = MathTex(
            "7",
            "=",
            "AB",
            "+",
            "Ab",
            "+",
            "aB",
            "+",
            "ab",
            font_size=43,
            color=INK,
        ).move_to(UP * 0.7)
        known_expanded[0].set_color(POINT)
        known_expanded[2].set_color(MUTED)
        known_expanded[4].set_color(PURPLE)
        known_expanded[6].set_color(PURPLE)
        known_expanded[8].set_color(MUTED)
        known_row = self.grouped_row("7", "+", 0.55)
        common_caption = label("共通項", 21, MUTED, "MEDIUM")
        common_caption.next_to(known_row[5], UP, buff=0.12)
        target_caption_grouped = label("目標 T", 21, PURPLE, "MEDIUM")
        target_caption_grouped.next_to(known_row[6], UP, buff=0.12)

        shadow_bundle = VGroup(shadow_equation, shadow_box, shadow_note)
        self.play(
            ReplacementTransform(shadow_title, known_title),
            FadeOut(VGroup(division, combined_context)),
            shadow_bundle.animate.scale(0.76).move_to([0, -1.35, 0]),
            run_time=0.8,
        )
        self.play(FadeIn(known_factor), run_time=0.5)
        self.play(
            LaggedStart(*(Write(part) for part in known_expanded), lag_ratio=0.09),
            run_time=1.4,
        )
        # Beat 16 collect_known_terms: settled semantic step.
        self.next_slide()
        self.play(
            Indicate(VGroup(known_expanded[2], known_expanded[8]), color=MUTED),
            Indicate(VGroup(known_expanded[4], known_expanded[6]), color=PURPLE),
            run_time=0.8,
        )
        self.play(
            TransformFromCopy(known_expanded[0], known_row[0]),
            FadeIn(known_row[1]),
            TransformFromCopy(VGroup(known_expanded[2], known_expanded[8]), known_row[2]),
            FadeIn(known_row[3]),
            TransformFromCopy(VGroup(known_expanded[4], known_expanded[6]), known_row[4]),
            FadeIn(known_row[5:]),
            FadeIn(common_caption),
            FadeIn(target_caption_grouped),
            run_time=1.1,
        )
        self.play(FadeOut(VGroup(known_factor, known_expanded)), run_time=0.45)
        self.wait(0.3)

        # Beat 17 expand_shadow_product: settled semantic step.
        self.next_slide()

        shadow_expand_title = label("同一位置展開影子乘積", 33, INK, "BOLD")
        shadow_expand_title.move_to(UP * 3.05)
        shadow_factor = MathTex(
            r"(A-a)(B-b)=\frac{36}{7}",
            font_size=41,
            color=INK,
        ).move_to(DOWN * 0.25)
        shadow_factor.set_color_by_tex("A-a", BLUE)
        shadow_factor.set_color_by_tex("B-b", REGION)
        shadow_expanded = MathTex(
            r"\frac{36}{7}",
            "=",
            "AB",
            "-",
            "Ab",
            "-",
            "aB",
            "+",
            "ab",
            font_size=41,
            color=INK,
        ).move_to(DOWN * 1.3)
        shadow_expanded[0].set_color(POINT)
        shadow_expanded[2].set_color(MUTED)
        shadow_expanded[4].set_color(PURPLE)
        shadow_expanded[6].set_color(PURPLE)
        shadow_expanded[8].set_color(MUTED)
        shadow_row = self.grouped_row(r"\frac{36}{7}", "-", -1.08)
        row_captions = VGroup(common_caption, target_caption_grouped)

        self.play(
            ReplacementTransform(known_title, shadow_expand_title),
            FadeOut(shadow_bundle),
            known_row.animate.shift(UP * 0.66),
            row_captions.animate.shift(UP * 0.66),
            run_time=0.7,
        )
        self.play(FadeIn(shadow_factor), run_time=0.5)
        self.play(
            LaggedStart(*(Write(part) for part in shadow_expanded), lag_ratio=0.09),
            run_time=1.4,
        )
        # Beat 18 collect_shadow_terms: settled semantic step.
        self.next_slide()
        self.play(
            TransformFromCopy(shadow_expanded[0], shadow_row[0]),
            FadeIn(shadow_row[1]),
            TransformFromCopy(VGroup(shadow_expanded[2], shadow_expanded[8]), shadow_row[2]),
            FadeIn(shadow_row[3]),
            TransformFromCopy(VGroup(shadow_expanded[4], shadow_expanded[6]), shadow_row[4]),
            FadeIn(shadow_row[5:]),
            run_time=1.05,
        )
        self.play(FadeOut(VGroup(shadow_factor, shadow_expanded)), run_time=0.4)
        self.wait(0.3)

        # Beat 19 subtract_to_isolate: settled semantic step.
        self.next_slide()

        subtract_title = label("上式減下式：共通項消失", 33, INK, "BOLD")
        subtract_title.move_to(UP * 3.05)
        subtract_sign = MathTex("-", font_size=48, color=CORAL)
        subtract_sign.move_to([-5.65, -1.08, 0])
        subtract_line = Line(
            np.array([-5.25, -1.78, 0]),
            np.array([3.0, -1.78, 0]),
            color=MUTED,
            stroke_width=2.5,
        )
        known_common_cross = Cross(known_row[2], stroke_color=CORAL, stroke_width=5)
        shadow_common_cross = Cross(shadow_row[2], stroke_color=CORAL, stroke_width=5)
        isolation = MathTex(
            "7",
            "-",
            r"\frac{36}{7}",
            "=",
            "2T",
            font_size=51,
            color=INK,
        ).move_to(DOWN * 2.35)
        isolation[0].set_color(POINT)
        isolation[2].set_color(POINT)
        isolation[4].set_color(PURPLE)
        no_variables = label(
            "不用解 a、b｜乘積的差只留下目標",
            25,
            MUTED,
            "MEDIUM",
            t2c={"只留下目標": PURPLE},
        ).next_to(isolation, DOWN, buff=0.25)

        self.play(
            ReplacementTransform(shadow_expand_title, subtract_title),
            FadeOut(row_captions),
            FadeIn(subtract_sign),
            Create(subtract_line),
            run_time=0.65,
        )
        self.play(
            Circumscribe(known_row[2], color=MUTED),
            Circumscribe(shadow_row[2], color=MUTED),
            run_time=0.7,
        )
        self.play(Create(known_common_cross), Create(shadow_common_cross), run_time=0.65)
        # Beat 20 isolate_requested_product: settled semantic step.
        self.next_slide()
        self.play(
            TransformFromCopy(known_row[0], isolation[0]),
            FadeIn(isolation[1]),
            TransformFromCopy(shadow_row[0], isolation[2]),
            FadeIn(isolation[3]),
            TransformFromCopy(VGroup(known_row[4], shadow_row[4]), isolation[4]),
            run_time=1.0,
        )
        self.play(
            known_row.animate.set_opacity(0.38),
            shadow_row.animate.set_opacity(0.38),
            FadeIn(no_variables),
            run_time=0.55,
        )

        # Beat 21 final_value: settled semantic step.
        self.next_slide()

        final_title = label("最後只剩一小步", 33, INK, "BOLD")
        final_title.move_to(UP * 3.05)
        step_one = MathTex(
            r"2T=7-\frac{36}{7}",
            font_size=48,
            color=INK,
        ).move_to(UP * 1.65)
        step_one.set_color_by_tex("T", PURPLE)
        step_two = MathTex(
            r"2T=\frac{49}{7}-\frac{36}{7}",
            font_size=48,
            color=INK,
        ).move_to(UP * 1.65)
        step_two.set_color_by_tex("T", PURPLE)
        step_three = MathTex(
            r"2T=\frac{13}{7}",
            font_size=51,
            color=INK,
        ).move_to(UP * 1.65)
        step_three.set_color_by_tex("T", PURPLE)
        target_value = MathTex(
            r"T=\frac{13}{14}",
            font_size=58,
            color=PURPLE,
        ).move_to(UP * 0.35)
        full_target = MathTex(
            r"a\sqrt{b^2+9}+b\sqrt{a^2+4}",
            "=",
            r"\frac{13}{14}",
            font_size=47,
            color=INK,
        ).move_to(DOWN * 1.35)
        full_target[0].set_color(PURPLE)
        full_target[2].set_color(POINT)
        answer_box = SurroundingRectangle(
            full_target[2], color=POINT, buff=0.18, stroke_width=3
        )

        subtraction_context = VGroup(
            known_row,
            shadow_row,
            subtract_sign,
            subtract_line,
            known_common_cross,
            shadow_common_cross,
            no_variables,
        )
        self.play(
            ReplacementTransform(subtract_title, final_title),
            FadeOut(subtraction_context),
            ReplacementTransform(isolation, step_one),
            run_time=0.85,
        )
        self.play(TransformMatchingTex(step_one, step_two), run_time=0.9)
        self.play(TransformMatchingTex(step_two, step_three), run_time=0.8)
        # Beat 22 reveal_product_value: settled semantic step.
        self.next_slide()
        self.play(TransformFromCopy(step_three, target_value), run_time=0.75)
        self.play(TransformFromCopy(target_value, full_target), run_time=1.0)
        self.play(Create(answer_box), Circumscribe(full_target[0], color=PURPLE), run_time=0.75)

        # Beat 23 consolidate: settled semantic step.
        self.next_slide()

        recap_title = label("不是求變數，而是找不變量", 34, INK, "BOLD")
        recap_title.move_to(UP * 3.05)
        four_badge = self.value_badge("4", "第一對", BLUE, width=1.55)
        nine_badge = self.value_badge("9", "第二對", REGION, width=1.55)
        pair_badges = VGroup(four_badge, nine_badge).arrange(DOWN, buff=0.2)
        pair_badges.move_to([-6.05, 0.25, 0])
        total_badge = self.value_badge("36", "總乘積", POINT)
        total_badge.move_to([-3.45, 0.25, 0])
        known_badge = self.value_badge("7", "已知加號組", POINT)
        known_badge.scale(0.88).move_to([-3.45, -1.35, 0])
        shadow_badge = self.value_badge(r"\frac{36}{7}", "減號影子", MUTED, width=2.0)
        shadow_badge.move_to([-0.35, 0.25, 0])
        difference_badge = self.value_badge(
            r"7-\frac{36}{7}",
            "留下 2T",
            PURPLE,
            width=2.65,
        )
        difference_badge.move_to([2.75, 0.25, 0])
        answer_badge = self.value_badge(
            r"\frac{13}{14}",
            "目標 T",
            POINT,
            width=2.0,
        )
        answer_badge.move_to([5.75, 0.25, 0])
        arrow_one = Arrow(
            pair_badges.get_right(),
            total_badge.get_left(),
            buff=0.18,
            color=MUTED,
            stroke_width=3,
        )
        arrow_two = Arrow(
            total_badge.get_right(),
            shadow_badge.get_left(),
            buff=0.18,
            color=MUTED,
            stroke_width=3,
        )
        divide_label = label("除以 7", 20, MUTED, "MEDIUM")
        divide_label.next_to(arrow_two, UP, buff=0.1)
        known_link = Arrow(
            known_badge.get_right(),
            shadow_badge.get_bottom() + DOWN * 0.02,
            buff=0.15,
            color=POINT,
            stroke_width=2.5,
        )
        arrow_three = Arrow(
            shadow_badge.get_right(),
            difference_badge.get_left(),
            buff=0.18,
            color=MUTED,
            stroke_width=3,
        )
        arrow_four = Arrow(
            difference_badge.get_right(),
            answer_badge.get_left(),
            buff=0.18,
            color=MUTED,
            stroke_width=3,
        )
        recap_target = full_target.copy().scale(0.88).move_to(DOWN * 2.65)
        recap_box = SurroundingRectangle(
            recap_target,
            color=POINT,
            buff=0.2,
            stroke_width=2.5,
        )

        self.play(
            ReplacementTransform(final_title, recap_title),
            FadeOut(VGroup(step_three, target_value, answer_box)),
            ReplacementTransform(full_target, recap_target),
            run_time=0.85,
        )
        self.play(
            LaggedStart(
                FadeIn(pair_badges),
                GrowArrow(arrow_one),
                FadeIn(total_badge),
                FadeIn(known_badge),
                GrowArrow(known_link),
                GrowArrow(arrow_two),
                FadeIn(divide_label),
                FadeIn(shadow_badge),
                GrowArrow(arrow_three),
                FadeIn(difference_badge),
                GrowArrow(arrow_four),
                FadeIn(answer_badge),
                lag_ratio=0.1,
            ),
            run_time=2.3,
        )
        self.play(Create(recap_box), Circumscribe(answer_badge, color=POINT), run_time=0.75)
        self.wait(0.35)
