"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q6."""

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
    CarloSlide,
    label,
)
from manim import (
    Arrow,
    Circumscribe,
    Create,
    Cross,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Polygon,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    TransformFromCopy,
    TransformMatchingTex,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, ORIGIN, RIGHT, UP


class Tcfs115Q06Slide(CarloSlide):
    """Complete a hidden product, then exhaustively filter its factor triples."""

    lesson_id = "carlo.tcfs_115_math_gifted.q06"

    @staticmethod
    def term_tile(tex: str, color: str, *, width: float = 1.55) -> VGroup:
        body = Rectangle(
            width=width,
            height=0.72,
            color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.08,
        )
        term = MathTex(tex, font_size=35, color=color)
        return VGroup(body, term)

    @staticmethod
    def choice_switch(symbol: str, color: str) -> VGroup:
        symbol_box = Rectangle(
            width=1.0,
            height=0.62,
            color=color,
            stroke_width=2.2,
            fill_color=color,
            fill_opacity=0.1,
        )
        symbol_tex = MathTex(symbol, font_size=34, color=color).move_to(symbol_box)
        one_box = Rectangle(
            width=1.0,
            height=0.62,
            color=PURPLE,
            stroke_width=2.2,
            fill_color=PURPLE,
            fill_opacity=0.1,
        )
        one_tex = MathTex("1", font_size=34, color=PURPLE).move_to(one_box)
        pair = VGroup(VGroup(symbol_box, symbol_tex), VGroup(one_box, one_tex))
        pair.arrange(RIGHT, buff=0.14)
        brace_text = label("二選一", 18, MUTED, "MEDIUM")
        brace_text.next_to(pair, DOWN, buff=0.11)
        return VGroup(pair, brace_text)

    @staticmethod
    def factor_candidate(value: int, quotient: str, *, valid: bool) -> VGroup:
        color = POINT if valid else CORAL
        body = Rectangle(
            width=1.72,
            height=1.18,
            color=color,
            stroke_width=2.6,
            fill_color=color,
            fill_opacity=0.08,
        )
        number = MathTex(str(value), font_size=39, color=color)
        number.move_to(body.get_center() + UP * 0.2)
        detail = MathTex(quotient, font_size=23, color=MUTED)
        detail.move_to(body.get_center() + DOWN * 0.34)
        return VGroup(body, number, detail)

    @staticmethod
    def threshold_card(z: int) -> VGroup:
        body = Rectangle(
            width=2.28,
            height=0.88,
            color=HAIRLINE,
            stroke_width=2,
            fill_color=HAIRLINE,
            fill_opacity=0.08,
        )
        z_tex = MathTex(rf"z={z}", font_size=27, color=POINT)
        rule = MathTex(rf"x-y<{z - 1}", font_size=27, color=INK)
        content = VGroup(z_tex, rule).arrange(DOWN, buff=0.08).move_to(body)
        return VGroup(body, content)

    @staticmethod
    def factor_table_row(
        z: int,
        product: int,
        x: int,
        y: int,
        gap: int,
        row_y: float,
    ) -> VGroup:
        cells = VGroup(
            MathTex(str(z), font_size=29, color=POINT).move_to([-4.7, row_y, 0]),
            MathTex(str(product), font_size=29, color=INK).move_to([-2.5, row_y, 0]),
            MathTex(
                rf"({x},{y})", font_size=29, color=INK
            ).move_to([0.15, row_y, 0]),
            MathTex(str(gap), font_size=32, color=PURPLE).move_to([3.35, row_y, 0]),
        )
        line = Line(
            [-5.75, row_y - 0.38, 0],
            [4.45, row_y - 0.38, 0],
            color=HAIRLINE,
            stroke_width=1.4,
        )
        return VGroup(cells, line)

    @staticmethod
    def comparison_row(
        z: int,
        gap: int,
        threshold: int,
        row_y: float,
        *,
        valid: bool,
        note: str = "",
    ) -> VGroup:
        result_color = REGION if valid else CORAL
        z_tex = MathTex(rf"z={z}", font_size=31, color=POINT).move_to(
            [-4.75, row_y, 0]
        )
        comparison = MathTex(
            rf"{gap}<{threshold}", font_size=34, color=result_color
        ).move_to([-1.95, row_y, 0])
        verdict = label(
            "通過" if valid else "淘汰",
            27,
            result_color,
            "BOLD",
        ).move_to([0.75, row_y, 0])
        note_label = label(note, 21, CORAL, "MEDIUM").move_to([3.38, row_y, 0])
        line = Line(
            [-5.75, row_y - 0.37, 0],
            [5.65, row_y - 0.37, 0],
            color=HAIRLINE,
            stroke_width=1.4,
        )
        row = VGroup(z_tex, comparison, verdict, note_label, line)
        if not valid:
            row.set_opacity(0.38)
            comparison.set_opacity(1)
            verdict.set_opacity(1)
            note_label.set_opacity(1)
        return row

    @staticmethod
    def tuple_tokens(values: tuple[int, int, int]) -> VGroup:
        colors = (BLUE, REGION, POINT)
        tokens = VGroup()
        for value, color in zip(values, colors, strict=True):
            body = Rectangle(
                width=1.04,
                height=0.76,
                color=color,
                stroke_width=2.4,
                fill_color=color,
                fill_opacity=0.09,
            )
            number = MathTex(str(value), font_size=34, color=color).move_to(body)
            tokens.add(VGroup(body, number))
        tokens.arrange(RIGHT, buff=0.16)
        left_paren = MathTex("(", font_size=49, color=MUTED)
        right_paren = MathTex(")", font_size=49, color=MUTED)
        left_paren.next_to(tokens, LEFT, buff=0.08)
        right_paren.next_to(tokens, RIGHT, buff=0.08)
        commas = VGroup(
            MathTex(",", font_size=36, color=MUTED).move_to(
                (tokens[0].get_right() + tokens[1].get_left()) / 2 + DOWN * 0.1
            ),
            MathTex(",", font_size=36, color=MUTED).move_to(
                (tokens[1].get_right() + tokens[2].get_left()) / 2 + DOWN * 0.1
            ),
        )
        return VGroup(left_paren, tokens, commas, right_paren)

    @staticmethod
    def exact_triangle(a: int, b: int, c: int, *, width: float = 3.35) -> VGroup:
        """Draw a triangle with side lengths a (base), b (left), and c (right)."""
        scale = width / a
        apex_x = (b * b + a * a - c * c) / (2 * a)
        apex_y = math.sqrt(max(b * b - apex_x * apex_x, 0))
        left_point = np.array([-width / 2, -0.55, 0])
        right_point = np.array([width / 2, -0.55, 0])
        apex = left_point + np.array([apex_x * scale, apex_y * scale, 0])
        base = Line(left_point, right_point, color=BLUE, stroke_width=4)
        left_side = Line(left_point, apex, color=REGION, stroke_width=4)
        right_side = Line(apex, right_point, color=POINT, stroke_width=4)
        a_label = MathTex(str(a), font_size=26, color=BLUE).next_to(
            base, DOWN, buff=0.1
        )
        b_label = MathTex(str(b), font_size=26, color=REGION).next_to(
            left_side.get_center(), LEFT, buff=0.12
        )
        c_label = MathTex(str(c), font_size=26, color=POINT).next_to(
            right_side.get_center(), RIGHT, buff=0.12
        )
        return VGroup(base, left_side, right_side, a_label, b_label, c_label)

    @staticmethod
    def status_line(caption: str, tex: str, color: str) -> VGroup:
        dot = Dot(radius=0.065, color=color)
        caption_label = label(caption, 20, MUTED, "MEDIUM")
        equation = MathTex(tex, font_size=27, color=color)
        row = VGroup(dot, caption_label, equation).arrange(RIGHT, buff=0.13)
        return row

    def construct(self) -> None:
        heading = label("第 6 題｜補齊乘積，再篩選三角形", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        term_specs = (
            (r"abc", INK, 1.72),
            (r"ab", BLUE, 1.55),
            (r"bc", REGION, 1.55),
            (r"ca", POINT, 1.55),
            (r"a", BLUE, 1.4),
            (r"b", REGION, 1.4),
            (r"c", POINT, 1.4),
        )
        terms = VGroup(
            *(self.term_tile(tex, color, width=width) for tex, color, width in term_specs)
        )
        terms[0].move_to([0, 1.75, 0])
        VGroup(*terms[1:4]).arrange(RIGHT, buff=0.34).move_to([0, 0.42, 0])
        VGroup(*terms[4:7]).arrange(RIGHT, buff=0.34).move_to([-0.93, -0.92, 0])
        missing_slot = DashedVMobject(
            Rectangle(width=1.4, height=0.72, color=PURPLE, stroke_width=2.2),
            num_dashes=14,
        ).move_to([2.79, -0.92, 0])
        missing_question = MathTex("?", font_size=35, color=PURPLE).move_to(missing_slot)
        level_labels = VGroup(
            label("三個字母", 19, MUTED, "MEDIUM").move_to([-4.25, 1.75, 0]),
            label("兩個字母", 19, MUTED, "MEDIUM").move_to([-4.25, 0.42, 0]),
            label("一個字母", 19, MUTED, "MEDIUM").move_to([-4.25, -0.92, 0]),
        )
        prompt = label(
            "這七項，像是哪個乘積展開後留下來的？",
            34,
            INK,
            "BOLD",
            t2c={"七項": POINT, "乘積": PURPLE},
        ).move_to([0, 3.0, 0])

        # Beat 01 original_seven_terms: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(prompt), run_time=0.8)
        self.play(
            LaggedStart(*(FadeIn(term, shift=UP * 0.12) for term in terms), lag_ratio=0.11),
            FadeIn(level_labels),
            run_time=1.7,
        )
        self.play(Create(missing_slot), FadeIn(missing_question), run_time=0.7)
        self.wait(0.3)

        # Beat 02 missing_one: settled semantic step.
        self.next_slide()
        switches = VGroup(
            self.choice_switch("a", BLUE),
            self.choice_switch("b", REGION),
            self.choice_switch("c", POINT),
        ).arrange(RIGHT, buff=0.76).move_to([0, 2.22, 0])
        multiplication_marks = VGroup(
            MathTex(r"\times", font_size=31, color=MUTED).move_to(
                (switches[0].get_right() + switches[1].get_left()) / 2
            ),
            MathTex(r"\times", font_size=31, color=MUTED).move_to(
                (switches[1].get_right() + switches[2].get_left()) / 2
            ),
        )
        result_specs = (
            (r"abc", INK),
            (r"ab", BLUE),
            (r"bc", REGION),
            (r"ca", POINT),
            (r"a", BLUE),
            (r"b", REGION),
            (r"c", POINT),
        )
        result_tiles = VGroup(
            *(self.term_tile(tex, color, width=1.18) for tex, color in result_specs)
        )
        result_tiles.arrange_in_grid(rows=2, cols=4, buff=(0.22, 0.2)).move_to(
            [-0.72, 0.38, 0]
        )
        empty_result = DashedVMobject(
            Rectangle(width=1.18, height=0.72, color=PURPLE, stroke_width=2.2),
            num_dashes=13,
        ).move_to(result_tiles[6].get_center() + RIGHT * 1.4)
        empty_mark = MathTex("?", font_size=33, color=PURPLE).move_to(empty_result)
        all_one_choice = MathTex(r"1\times1\times1", font_size=31, color=PURPLE)
        all_one_choice.next_to(empty_result, RIGHT, buff=0.42)
        all_one_arrow = Arrow(
            all_one_choice.get_left(),
            empty_result.get_right(),
            buff=0.12,
            color=PURPLE,
            stroke_width=3.5,
        )
        missing_one = self.term_tile("1", PURPLE, width=1.18).move_to(empty_result)
        full_sum = MathTex(
            r"abc+ab+bc+ca+a+b+c",
            r"+1",
            "=",
            "479",
            r"+1",
            font_size=34,
            color=INK,
        ).move_to([0, -2.18, 0])
        full_sum[1].set_color(PURPLE)
        full_sum[4].set_color(PURPLE)
        both_sides = label("兩邊同時補 1", 21, PURPLE, "BOLD")
        both_sides.next_to(full_sum, DOWN, buff=0.14)
        self.play(
            FadeOut(prompt),
            FadeOut(level_labels),
            FadeOut(missing_question),
            FadeIn(switches, shift=DOWN * 0.12),
            FadeIn(multiplication_marks),
            run_time=0.85,
        )
        self.play(
            *(
                ReplacementTransform(term, target)
                for term, target in zip(terms, result_tiles, strict=True)
            ),
            ReplacementTransform(missing_slot, empty_result),
            FadeIn(empty_mark),
            run_time=1.25,
        )
        self.wait(0.25)
        self.play(FadeIn(all_one_choice), GrowArrow(all_one_arrow), run_time=0.65)
        # Beat 03 identify_missing_side: settled semantic step.
        self.next_slide()
        self.play(
            FadeOut(empty_mark),
            ReplacementTransform(empty_result, missing_one[0]),
            FadeIn(missing_one[1]),
            run_time=0.6,
        )
        self.play(Write(full_sum), FadeIn(both_sides), run_time=0.95)
        self.wait(0.3)

        # Beat 04 complete_product: settled semantic step.
        self.next_slide()
        completed_product = MathTex(
            r"(a+1)",
            r"(b+1)",
            r"(c+1)",
            "=",
            "480",
            font_size=52,
            color=INK,
        )
        completed_product[0].set_color(BLUE)
        completed_product[1].set_color(REGION)
        completed_product[2].set_color(POINT)
        completed_product.move_to([0, 0.3, 0])
        binary_note = label(
            "八種選擇完整了，收回三個括號",
            29,
            INK,
            "BOLD",
            t2c={"八種選擇": PURPLE, "三個括號": POINT},
        ).move_to([0, 2.22, 0])
        right_change = MathTex(r"479+1", r"=480", font_size=35, color=MUTED)
        right_change[1].set_color(POINT)
        right_change.next_to(completed_product, DOWN, buff=0.48)
        choice_scene = VGroup(
            switches,
            multiplication_marks,
            result_tiles,
            missing_one,
            all_one_choice,
            all_one_arrow,
            both_sides,
        )
        self.play(FadeOut(choice_scene), FadeIn(binary_note), run_time=0.7)
        self.play(TransformMatchingTex(full_sum, completed_product), run_time=1.4)
        self.play(FadeIn(right_change, shift=UP * 0.1), run_time=0.6)
        self.wait(0.3)

        # Beat 05 shift_sides: settled semantic step.
        self.next_slide()
        shift_line = NumberLine(
            x_range=[0, 8, 1],
            length=7.0,
            include_ticks=True,
            tick_size=0.07,
            color=HAIRLINE,
            stroke_width=2.4,
        ).move_to([-3.7, -0.35, 0])
        old_values = (6, 4, 2)
        old_names = ("a", "b", "c")
        new_names = ("x", "y", "z")
        role_colors = (BLUE, REGION, POINT)
        old_dots = VGroup()
        new_dots = VGroup()
        shift_arrows = VGroup()
        for value, old_name, new_name, color in zip(
            old_values, old_names, new_names, role_colors, strict=True
        ):
            old_dot = Dot(shift_line.n2p(value), radius=0.09, color=color)
            old_label = MathTex(old_name, font_size=30, color=color).next_to(
                old_dot, DOWN, buff=0.18
            )
            new_dot = Dot(shift_line.n2p(value + 1), radius=0.09, color=color)
            new_label = MathTex(new_name, font_size=30, color=color).next_to(
                new_dot, UP, buff=0.18
            )
            arrow = Arrow(
                shift_line.n2p(value) + UP * 0.34,
                shift_line.n2p(value + 1) + UP * 0.34,
                buff=0.03,
                color=PURPLE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.25,
            )
            plus_one = MathTex("+1", font_size=22, color=PURPLE).next_to(
                arrow, UP, buff=0.05
            )
            old_dots.add(VGroup(old_dot, old_label))
            new_dots.add(VGroup(new_dot, new_label))
            shift_arrows.add(VGroup(arrow, plus_one))
        definitions = VGroup(
            MathTex(r"x=a+1", font_size=36, color=BLUE),
            MathTex(r"y=b+1", font_size=36, color=REGION),
            MathTex(r"z=c+1", font_size=36, color=POINT),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.42, 1.2, 0])
        new_order = MathTex(r"x>y>z\ge2", font_size=43, color=INK).move_to(
            [3.42, -0.35, 0]
        )
        new_product = MathTex(r"xyz=480", font_size=49, color=POINT).move_to(
            [3.42, -1.25, 0]
        )
        back_translation = MathTex(
            r"a=x-1,\quad b=y-1,\quad c=z-1", font_size=27, color=MUTED
        ).move_to([0, -2.73, 0])
        shift_prompt = label(
            "三條邊一起向右平移 1",
            32,
            INK,
            "BOLD",
            t2c={"平移 1": PURPLE},
        ).move_to([0, 3.0, 0])
        self.play(
            FadeOut(binary_note),
            FadeOut(right_change),
            completed_product.animate.scale(0.58).move_to([4.25, 2.55, 0]).set_opacity(0.45),
            FadeIn(shift_prompt),
            Create(shift_line),
            FadeIn(old_dots),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*(GrowArrow(item[0]) for item in shift_arrows), lag_ratio=0.18),
            FadeIn(VGroup(*(item[1] for item in shift_arrows))),
            LaggedStart(*(FadeIn(dot) for dot in new_dots), lag_ratio=0.18),
            run_time=1.2,
        )
        self.play(
            LaggedStart(*(FadeIn(row, shift=LEFT * 0.12) for row in definitions), lag_ratio=0.15),
            FadeIn(new_order),
            TransformFromCopy(completed_product, new_product),
            FadeIn(back_translation),
            run_time=1.1,
        )

        # Beat 06 bound_z: settled semantic step.
        self.next_slide()
        shift_scene = VGroup(
            shift_line,
            old_dots,
            new_dots,
            shift_arrows,
            definitions,
            new_order,
            new_product,
            back_translation,
            shift_prompt,
            completed_product,
        )
        bars = VGroup()
        bar_specs = (("z", 1.45, POINT), ("y", 2.25, REGION), ("x", 3.05, BLUE))
        for symbol, height, color in bar_specs:
            body = Rectangle(
                width=1.45,
                height=height,
                color=color,
                stroke_width=3,
                fill_color=color,
                fill_opacity=0.12,
            )
            body.align_to(DOWN * 1.42, DOWN)
            symbol_tex = MathTex(symbol, font_size=39, color=color).move_to(body)
            bars.add(VGroup(body, symbol_tex))
        bars.arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to([-3.45, -0.1, 0])
        z_level = DashedVMobject(
            Line([-5.55, -0.41, 0], [-1.35, -0.41, 0], color=POINT, stroke_width=2),
            num_dashes=18,
        )
        z_level_label = MathTex("z", font_size=27, color=POINT).next_to(
            z_level, LEFT, buff=0.1
        )
        comparisons = VGroup(
            MathTex(r"x>z", font_size=34, color=BLUE),
            MathTex(r"y>z", font_size=34, color=REGION),
            MathTex(r"z=z", font_size=34, color=POINT),
        ).arrange(RIGHT, buff=0.58).move_to([-3.45, -2.18, 0])
        bound_steps = VGroup(
            MathTex(r"xyz>z^3", font_size=43, color=INK),
            MathTex(r"z^3<480", font_size=43, color=INK),
            MathTex(r"z<\sqrt[3]{480}<8", font_size=43, color=POINT),
        ).arrange(DOWN, buff=0.45).move_to([3.25, 0.32, 0])
        bound_number_line = NumberLine(
            x_range=[1, 8, 1],
            length=5.2,
            color=HAIRLINE,
            stroke_width=2.2,
        ).move_to([3.25, -2.05, 0])
        bound_number_labels = VGroup(
            *(
                label(str(n), 18, MUTED, "MEDIUM").next_to(
                    bound_number_line.n2p(n), DOWN, buff=0.13
                )
                for n in range(1, 8)
            )
        )
        integer_dots = VGroup(
            *(Dot(bound_number_line.n2p(n), radius=0.07, color=POINT) for n in range(2, 8))
        )
        bound_title = label(
            "先抓住最小因數 z",
            33,
            INK,
            "BOLD",
            t2c={"z": POINT},
        ).move_to([0, 3.0, 0])
        self.play(FadeOut(shift_scene), FadeIn(bound_title), run_time=0.75)
        self.play(
            LaggedStart(*(FadeIn(bar, shift=UP * 0.15) for bar in bars), lag_ratio=0.18),
            run_time=1.0,
        )
        self.play(Create(z_level), FadeIn(z_level_label), FadeIn(comparisons), run_time=0.75)
        # Beat 07 list_bounded_candidates: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(*(Write(step) for step in bound_steps), lag_ratio=0.35),
            run_time=1.55,
        )
        self.play(
            Create(bound_number_line),
            FadeIn(bound_number_labels),
            FadeIn(integer_dots),
            run_time=0.75,
        )

        # Beat 08 candidate_divisors: settled semantic step.
        self.next_slide()
        bound_scene = VGroup(
            bars,
            z_level,
            z_level_label,
            comparisons,
            bound_steps,
            bound_number_line,
            bound_number_labels,
            integer_dots,
            bound_title,
        )
        divisor_title = label(
            "範圍還不夠：z 必須整除 480",
            33,
            INK,
            "BOLD",
            t2c={"整除 480": POINT},
        ).move_to([0, 3.0, 0])
        divides_formula = MathTex(r"z\mid480", font_size=47, color=POINT).move_to(
            [0, 2.12, 0]
        )
        candidate_data = (
            (2, r"480/2=240", True),
            (3, r"480/3=160", True),
            (4, r"480/4=120", True),
            (5, r"480/5=96", True),
            (6, r"480/6=80", True),
            (7, r"480=7\cdot68+4", False),
        )
        candidate_cards = VGroup(
            *(
                self.factor_candidate(value, quotient, valid=valid)
                for value, quotient, valid in candidate_data
            )
        ).arrange(RIGHT, buff=0.18).move_to([0, 0.42, 0])
        seven_cross = Cross(candidate_cards[-1][0], stroke_color=CORAL, stroke_width=5)
        exact_candidates = MathTex(
            r"z\in\{2,3,4,5,6\}", font_size=49, color=POINT
        ).move_to([0, -1.65, 0])
        clarification = label(
            "7 雖小於 8，卻不是 480 的因數",
            24,
            MUTED,
            "MEDIUM",
            t2c={"不是 480 的因數": CORAL},
        ).move_to([0, -2.34, 0])
        self.play(FadeOut(bound_scene), FadeIn(divisor_title), FadeIn(divides_formula), run_time=0.8)
        self.play(
            LaggedStart(*(FadeIn(card, shift=UP * 0.12) for card in candidate_cards), lag_ratio=0.13),
            run_time=1.3,
        )
        self.play(Create(seven_cross), candidate_cards[-1].animate.set_opacity(0.34), run_time=0.65)
        self.play(FadeIn(exact_candidates), FadeIn(clarification), run_time=0.7)

        # Beat 09 pose_triangle_filter: settled semantic step.
        self.next_slide()
        divisor_scene = VGroup(
            divisor_title,
            divides_formula,
            candidate_cards,
            seven_cross,
            exact_candidates,
            clarification,
        )
        triangle_title = label(
            "乘積正確，三條邊就一定合得起來嗎？",
            34,
            INK,
            "BOLD",
            t2c={"合得起來": POINT},
        ).move_to([0, 3.0, 0])
        divider = Line([0, 2.25, 0], [0, -2.45, 0], color=HAIRLINE, stroke_width=2)
        flat_left = np.array([-6.1, -0.2, 0])
        flat_joint = np.array([-3.95, -0.2, 0])
        flat_right = np.array([-1.05, -0.2, 0])
        flat_base = Line(flat_left, flat_right, color=BLUE, stroke_width=7).shift(DOWN * 0.18)
        flat_b = Line(flat_left, flat_joint, color=REGION, stroke_width=4)
        flat_c = Line(flat_joint, flat_right, color=POINT, stroke_width=4)
        flat_labels = VGroup(
            MathTex("a", font_size=31, color=BLUE).next_to(flat_base, DOWN, buff=0.18),
            MathTex("b", font_size=31, color=REGION).next_to(flat_b, UP, buff=0.13),
            MathTex("c", font_size=31, color=POINT).next_to(flat_c, UP, buff=0.13),
        )
        flat_caption = VGroup(
            MathTex(r"b+c=a", font_size=35, color=CORAL),
            label("只能攤平", 24, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.18).move_to([-3.58, -1.5, 0])
        valid_left = np.array([1.05, -0.75, 0])
        valid_right = np.array([6.1, -0.75, 0])
        valid_apex = np.array([4.0, 1.15, 0])
        valid_base = Line(valid_left, valid_right, color=BLUE, stroke_width=4)
        valid_b = Line(valid_left, valid_apex, color=REGION, stroke_width=4)
        valid_c = Line(valid_apex, valid_right, color=POINT, stroke_width=4)
        valid_labels = VGroup(
            MathTex("a", font_size=31, color=BLUE).next_to(valid_base, DOWN, buff=0.16),
            MathTex("b", font_size=31, color=REGION).next_to(valid_b.get_center(), LEFT, buff=0.14),
            MathTex("c", font_size=31, color=POINT).next_to(valid_c.get_center(), RIGHT, buff=0.14),
        )
        valid_caption = VGroup(
            MathTex(r"b+c>a", font_size=39, color=REGION),
            label("才能合攏", 24, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.18).move_to([3.58, -1.72, 0])
        triangle_question = label(
            "決定能否合攏的嚴格條件是？",
            27,
            MUTED,
            "MEDIUM",
        ).move_to([0, 2.3, 0])
        self.play(FadeOut(divisor_scene), FadeIn(triangle_title), FadeIn(triangle_question), run_time=0.75)
        self.play(Create(divider), Create(flat_base), Create(flat_b), Create(flat_c), FadeIn(flat_labels), run_time=0.9)
        self.play(FadeIn(flat_caption), run_time=0.55)
        self.wait(0.35)
        # Beat 10 state_triangle_filter: settled semantic step.
        self.next_slide()
        self.play(Create(valid_base), Create(valid_b), Create(valid_c), FadeIn(valid_labels), run_time=0.9)
        self.play(FadeIn(valid_caption), run_time=0.55)

        # Beat 11 translate_triangle: settled semantic step.
        self.next_slide()
        triangle_scene = VGroup(
            triangle_title,
            triangle_question,
            divider,
            flat_base,
            flat_b,
            flat_c,
            flat_labels,
            flat_caption,
            valid_base,
            valid_b,
            valid_c,
            valid_labels,
            valid_caption,
        )
        retained_triangle = VGroup(valid_base, valid_b, valid_c, valid_labels).copy()
        retained_triangle.scale(0.72).move_to([-4.55, 0.55, 0]).set_opacity(0.62)
        triangle_rule = MathTex(r"b+c>a", font_size=43, color=REGION).move_to(
            [-4.55, -1.25, 0]
        )
        substitution = MathTex(
            r"(y-1)+(z-1)>x-1", font_size=43, color=INK
        ).move_to([2.25, 1.18, 0])
        gap_rule = MathTex(r"x-y<z-1", font_size=50, color=POINT).move_to(
            [2.25, 0.12, 0]
        )
        gap_meaning = label(
            "x、y 不能相差太遠",
            26,
            MUTED,
            "MEDIUM",
            t2c={"不能相差太遠": PURPLE},
        ).move_to([2.25, -0.68, 0])
        threshold_cards = VGroup(*(self.threshold_card(z) for z in range(2, 7)))
        threshold_cards.arrange(RIGHT, buff=0.16).move_to([0, -2.25, 0])
        translate_title = label(
            "把三角形條件搬到 x、y、z",
            33,
            INK,
            "BOLD",
            t2c={"x、y、z": POINT},
        ).move_to([0, 3.0, 0])
        self.play(FadeOut(triangle_scene), FadeIn(translate_title), FadeIn(retained_triangle), run_time=0.75)
        self.play(TransformFromCopy(retained_triangle, triangle_rule), run_time=0.65)
        self.play(Write(substitution), run_time=0.8)
        # Beat 12 factor_triangle_condition: settled semantic step.
        self.next_slide()
        self.play(TransformMatchingTex(substitution.copy(), gap_rule), run_time=0.85)
        self.play(FadeIn(gap_meaning), run_time=0.45)
        self.play(
            LaggedStart(*(FadeIn(card, shift=UP * 0.1) for card in threshold_cards), lag_ratio=0.12),
            run_time=1.0,
        )

        # Beat 13 nearest_factor_pairs: settled semantic step.
        self.next_slide()
        translate_scene = VGroup(
            translate_title,
            retained_triangle,
            triangle_rule,
            substitution,
            gap_rule,
            gap_meaning,
            threshold_cards,
        )
        method_title = label(
            "固定 z：找最接近平方根的因數對",
            33,
            INK,
            "BOLD",
            t2c={"最接近": PURPLE},
        ).move_to([0, 3.0, 0])
        fixed_product = MathTex(r"xy=480/z", font_size=39, color=POINT).move_to(
            [3.9, 2.2, 0]
        )
        square_like = Rectangle(
            width=2.28,
            height=1.9,
            color=REGION,
            stroke_width=3,
            fill_color=REGION,
            fill_opacity=0.1,
        ).move_to([-3.85, 1.16, 0])
        square_sides = VGroup(
            MathTex("12", font_size=24, color=REGION).next_to(square_like, UP, buff=0.08),
            MathTex("10", font_size=24, color=REGION).next_to(square_like, LEFT, buff=0.08),
            MathTex(r"x-y=2", font_size=25, color=PURPLE).move_to(square_like),
        )
        thin_like = Rectangle(
            width=3.8,
            height=1.14,
            color=MUTED,
            stroke_width=2.5,
            fill_color=MUTED,
            fill_opacity=0.06,
        ).move_to([0.22, 1.16, 0])
        thin_sides = VGroup(
            MathTex("20", font_size=24, color=MUTED).next_to(thin_like, UP, buff=0.08),
            MathTex("6", font_size=24, color=MUTED).next_to(thin_like, LEFT, buff=0.08),
            MathTex(r"x-y=14", font_size=25, color=MUTED).move_to(thin_like),
        )
        same_area = MathTex(r"12\cdot10=20\cdot6=120", font_size=28, color=INK)
        same_area.move_to([3.9, 1.42, 0])
        rectangle_conclusion = label(
            "同面積越接近正方形，邊長差越小",
            22,
            MUTED,
            "MEDIUM",
            t2c={"邊長差越小": PURPLE},
        ).move_to([0, -0.28, 0])
        table_headers = VGroup(
            label("z", 22, POINT, "BOLD").move_to([-4.7, 1.5, 0]),
            label("xy=480/z", 22, MUTED, "BOLD").move_to([-2.5, 1.5, 0]),
            label("最近因數對", 22, MUTED, "BOLD").move_to([0.15, 1.5, 0]),
            label("最小差距", 22, PURPLE, "BOLD").move_to([3.35, 1.5, 0]),
        )
        header_line = Line([-5.75, 1.16, 0], [4.45, 1.16, 0], color=MUTED, stroke_width=2)
        table_data = (
            (2, 240, 16, 15, 1),
            (3, 160, 16, 10, 6),
            (4, 120, 12, 10, 2),
            (5, 96, 12, 8, 4),
            (6, 80, 10, 8, 2),
        )
        table_rows = VGroup(
            *(
                self.factor_table_row(*row, row_y=0.72 - index * 0.65)
                for index, row in enumerate(table_data)
            )
        )
        gap_highlight = Rectangle(
            width=1.55,
            height=3.72,
            color=PURPLE,
            stroke_width=2.2,
            fill_color=PURPLE,
            fill_opacity=0.05,
        ).move_to([3.35, -0.12, 0])
        completeness_note = label(
            "最近的一對若仍失敗，其他更不平均的因數對也一定失敗",
            21,
            MUTED,
            "MEDIUM",
            t2c={"也一定失敗": CORAL},
        ).move_to([0, -2.78, 0])
        self.play(FadeOut(translate_scene), FadeIn(method_title), FadeIn(fixed_product), run_time=0.75)
        self.play(Create(square_like), FadeIn(square_sides), run_time=0.65)
        self.play(Create(thin_like), FadeIn(thin_sides), FadeIn(same_area), run_time=0.7)
        # Beat 14 test_near_factor_pairs: settled semantic step.
        self.next_slide()
        self.play(FadeIn(rectangle_conclusion), Indicate(square_like, color=PURPLE), run_time=0.65)
        rectangle_demo = VGroup(
            fixed_product,
            square_like,
            square_sides,
            thin_like,
            thin_sides,
            same_area,
            rectangle_conclusion,
        )
        self.play(FadeOut(rectangle_demo), run_time=0.55)
        self.play(FadeIn(gap_highlight), FadeIn(table_headers), Create(header_line), run_time=0.65)
        # Beat 15 test_far_factor_pairs: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(*(FadeIn(row, shift=RIGHT * 0.12) for row in table_rows), lag_ratio=0.16),
            run_time=1.55,
        )
        self.play(FadeIn(completeness_note), run_time=0.55)

        # Beat 16 select_valid_rows: settled semantic step.
        self.next_slide()
        factor_table_scene = VGroup(
            method_title,
            gap_highlight,
            table_headers,
            header_line,
            table_rows,
            completeness_note,
        )
        filter_title = label(
            "逐列套入嚴格門檻 x-y<z-1",
            33,
            INK,
            "BOLD",
            t2c={"嚴格門檻": CORAL},
        ).move_to([0, 3.0, 0])
        comparison_headers = VGroup(
            label("候選", 21, MUTED, "BOLD").move_to([-4.75, 2.15, 0]),
            label("最小差距 < 門檻", 21, MUTED, "BOLD").move_to([-1.95, 2.15, 0]),
            label("結果", 21, MUTED, "BOLD").move_to([0.75, 2.15, 0]),
            label("邊界意義", 21, MUTED, "BOLD").move_to([3.38, 2.15, 0]),
        )
        comparison_line = Line([-5.75, 1.82, 0], [5.65, 1.82, 0], color=MUTED, stroke_width=2)
        comparisons_data = (
            (2, 1, 1, False, "等號，不成立"),
            (3, 6, 2, False, "差距太大"),
            (4, 2, 3, True, ""),
            (5, 4, 4, False, "等號＝攤平"),
            (6, 2, 5, True, ""),
        )
        comparison_rows = VGroup(
            *(
                self.comparison_row(
                    z,
                    gap,
                    threshold,
                    row_y=1.36 - index * 0.62,
                    valid=valid,
                    note=note,
                )
                for index, (z, gap, threshold, valid, note) in enumerate(comparisons_data)
            )
        )
        survivor_one = MathTex(
            r"(x,y,z)=(12,10,4)", font_size=34, color=REGION
        )
        survivor_two = MathTex(
            r"(x,y,z)=(10,8,6)", font_size=34, color=REGION
        )
        survivors = VGroup(survivor_one, survivor_two).arrange(RIGHT, buff=0.9)
        survivors.move_to([0, -2.35, 0])
        survivor_boxes = VGroup(
            SurroundingRectangle(survivor_one, color=REGION, buff=0.14, stroke_width=2.5),
            SurroundingRectangle(survivor_two, color=REGION, buff=0.14, stroke_width=2.5),
        )
        self.play(FadeOut(factor_table_scene), FadeIn(filter_title), run_time=0.65)
        self.play(FadeIn(comparison_headers), Create(comparison_line), run_time=0.55)
        # Beat 17 test_candidate_rows: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(
                *(FadeIn(row, shift=RIGHT * 0.1) for row in comparison_rows[:3]),
                lag_ratio=0.18,
            ),
            run_time=0.9,
        )

        # Beat 18 retain_valid_rows: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(
                *(FadeIn(row, shift=RIGHT * 0.1) for row in comparison_rows[3:]),
                lag_ratio=0.22,
            ),
            run_time=0.7,
        )
        self.play(FadeIn(survivors), Create(survivor_boxes), run_time=0.7)
        self.play(
            Circumscribe(comparison_rows[2], color=REGION, time_width=0.55),
            Circumscribe(comparison_rows[4], color=REGION, time_width=0.55),
            run_time=0.9,
        )
        self.wait(0.3)

        # Beat 19 restore_sides: settled semantic step.
        self.next_slide()
        filter_scene = VGroup(
            filter_title,
            comparison_headers,
            comparison_line,
            comparison_rows,
            survivors,
            survivor_boxes,
        )
        restore_title = label(
            "每個新變數都向左平移 1",
            33,
            INK,
            "BOLD",
            t2c={"平移 1": PURPLE},
        ).move_to([0, 3.0, 0])
        shifted_tuples = VGroup(
            self.tuple_tokens((12, 10, 4)),
            self.tuple_tokens((10, 8, 6)),
        )
        shifted_tuples[0].move_to([-3.6, 1.15, 0])
        shifted_tuples[1].move_to([3.6, 1.15, 0])
        minus_arrows = VGroup()
        for x_position in (-3.6, 3.6):
            arrow = Arrow(
                [x_position, 0.65, 0],
                [x_position, -0.25, 0],
                buff=0.04,
                color=PURPLE,
                stroke_width=3.5,
            )
            note = label("每個數 −1", 21, PURPLE, "BOLD").next_to(
                arrow, RIGHT, buff=0.13
            )
            minus_arrows.add(VGroup(arrow, note))
        restored_tuples = VGroup(
            self.tuple_tokens((11, 9, 3)),
            self.tuple_tokens((9, 7, 5)),
        )
        restored_tuples[0].move_to([-3.6, -0.92, 0])
        restored_tuples[1].move_to([3.6, -0.92, 0])
        variable_labels = VGroup(
            MathTex(r"(x,y,z)", font_size=28, color=MUTED).move_to([-3.6, 2.0, 0]),
            MathTex(r"(x,y,z)", font_size=28, color=MUTED).move_to([3.6, 2.0, 0]),
            MathTex(r"(a,b,c)", font_size=31, color=INK).move_to([-3.6, -1.72, 0]),
            MathTex(r"(a,b,c)", font_size=31, color=INK).move_to([3.6, -1.72, 0]),
        )
        restore_equations = VGroup(
            MathTex(r"(12,10,4)\mapsto(11,9,3)", font_size=29, color=INK),
            MathTex(r"(10,8,6)\mapsto(9,7,5)", font_size=29, color=INK),
        ).arrange(RIGHT, buff=1.0).move_to([0, -2.45, 0])
        self.play(FadeOut(filter_scene), FadeIn(restore_title), run_time=0.65)
        self.play(
            TransformFromCopy(survivor_one, shifted_tuples[0]),
            TransformFromCopy(survivor_two, shifted_tuples[1]),
            FadeIn(VGroup(variable_labels[0], variable_labels[1])),
            run_time=0.85,
        )
        self.play(
            GrowArrow(minus_arrows[0][0]),
            GrowArrow(minus_arrows[1][0]),
            FadeIn(VGroup(minus_arrows[0][1], minus_arrows[1][1])),
            run_time=0.65,
        )
        # Beat 20 reconstruct_side_triples: settled semantic step.
        self.next_slide()
        self.play(
            TransformFromCopy(shifted_tuples[0], restored_tuples[0]),
            TransformFromCopy(shifted_tuples[1], restored_tuples[1]),
            FadeIn(VGroup(variable_labels[2], variable_labels[3])),
            run_time=0.95,
        )
        self.play(FadeIn(restore_equations), run_time=0.6)

        # Beat 21 verify_triangles: settled semantic step.
        self.next_slide()
        restore_scene = VGroup(
            restore_title,
            shifted_tuples,
            minus_arrows,
            restored_tuples,
            variable_labels,
            restore_equations,
        )
        verify_title = label(
            "兩組都要把三個條件驗回去",
            33,
            INK,
            "BOLD",
            t2c={"三個條件": POINT},
        ).move_to([0, 3.0, 0])
        verify_divider = Line([0, 2.4, 0], [0, -2.6, 0], color=HAIRLINE, stroke_width=2)
        first_name = MathTex(r"(a,b,c)=(11,9,3)", font_size=34, color=INK).move_to(
            [-3.85, 2.12, 0]
        )
        second_name = MathTex(r"(a,b,c)=(9,7,5)", font_size=34, color=INK).move_to(
            [3.85, 2.12, 0]
        )
        first_triangle = self.exact_triangle(11, 9, 3).scale(0.92).move_to(
            [-3.85, 0.64, 0]
        )
        second_triangle = self.exact_triangle(9, 7, 5).scale(0.92).move_to(
            [3.85, 0.64, 0]
        )
        first_checks = VGroup(
            self.status_line("次序", r"11>9>3\ge1", REGION),
            self.status_line("三角形", r"9+3>11", REGION),
            self.status_line("乘積", r"12\cdot10\cdot4=480", REGION),
            self.status_line("原式", r"480-1=479", POINT),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-3.85, -1.65, 0])
        second_checks = VGroup(
            self.status_line("次序", r"9>7>5\ge1", REGION),
            self.status_line("三角形", r"7+5>9", REGION),
            self.status_line("乘積", r"10\cdot8\cdot6=480", REGION),
            self.status_line("原式", r"480-1=479", POINT),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.85, -1.65, 0])
        self.play(FadeOut(restore_scene), FadeIn(verify_title), Create(verify_divider), run_time=0.7)
        self.play(FadeIn(first_name), Create(first_triangle), run_time=0.9)
        self.play(
            LaggedStart(*(FadeIn(row, shift=RIGHT * 0.08) for row in first_checks), lag_ratio=0.17),
            run_time=1.15,
        )
        # Beat 22 check_triangle_witnesses: settled semantic step.
        self.next_slide()
        self.play(FadeIn(second_name), Create(second_triangle), run_time=0.9)
        self.play(
            LaggedStart(*(FadeIn(row, shift=RIGHT * 0.08) for row in second_checks), lag_ratio=0.17),
            run_time=1.15,
        )
        self.play(
            Circumscribe(first_name, color=REGION, time_width=0.55),
            Circumscribe(second_name, color=REGION, time_width=0.55),
            run_time=0.9,
        )
        self.wait(0.3)

        # Beat 23 consolidate: settled semantic step.
        self.next_slide()
        verification_scene = VGroup(
            verify_title,
            verify_divider,
            first_name,
            second_name,
            first_triangle,
            second_triangle,
            first_checks,
            second_checks,
        )
        final_title = label(
            "補一個 1，完成整個篩選",
            34,
            INK,
            "BOLD",
            t2c={"補一個 1": PURPLE, "篩選": POINT},
        ).move_to([0, 3.0, 0])
        first_recap_body = Rectangle(
            width=2.25,
            height=0.72,
            color=PURPLE,
            stroke_width=2.4,
            fill_color=PURPLE,
            fill_opacity=0.08,
        )
        first_recap_text = label("七項 ＋ 1", 27, PURPLE, "BOLD")
        first_recap = VGroup(first_recap_body, first_recap_text)
        recap_steps = VGroup(
            first_recap,
            self.term_tile(r"xyz=480", INK, width=2.25),
            self.term_tile(r"z\in\{2,3,4,5,6\}", POINT, width=3.0),
            self.term_tile(r"x-y<z-1", REGION, width=2.45),
        ).arrange(RIGHT, buff=0.52).move_to([0, 1.38, 0])
        recap_arrows = VGroup(
            *(
                Arrow(
                    recap_steps[index].get_right(),
                    recap_steps[index + 1].get_left(),
                    buff=0.1,
                    color=MUTED,
                    stroke_width=3,
                )
                for index in range(3)
            )
        )
        factor_links = VGroup(
            MathTex(r"(12,10,4)", font_size=31, color=MUTED),
            MathTex(r"(10,8,6)", font_size=31, color=MUTED),
        ).arrange(RIGHT, buff=2.1).move_to([0, 0.15, 0])
        final_answers = VGroup(
            MathTex(r"(a,b,c)=(11,9,3)", font_size=43, color=REGION),
            MathTex(r"(a,b,c)=(9,7,5)", font_size=43, color=REGION),
        ).arrange(RIGHT, buff=1.0).move_to([0, -1.03, 0])
        answer_arrows = VGroup(
            Arrow(factor_links[0].get_bottom(), final_answers[0].get_top(), buff=0.11, color=PURPLE),
            Arrow(factor_links[1].get_bottom(), final_answers[1].get_top(), buff=0.11, color=PURPLE),
        )
        final_answer_label = label("答案只有這兩組", 29, POINT, "BOLD").move_to(
            [0, -2.0, 0]
        )
        source_detail = label(
            "第壹部分第 6 題・PDF 第 3 頁",
            17,
            MUTED,
            "MEDIUM",
        ).to_corner(DOWN + LEFT, buff=0.24)
        self.play(FadeOut(verification_scene), FadeIn(final_title), FadeIn(source_detail), run_time=0.7)
        self.play(
            LaggedStart(*(FadeIn(step, shift=UP * 0.1) for step in recap_steps), lag_ratio=0.15),
            LaggedStart(*(GrowArrow(arrow) for arrow in recap_arrows), lag_ratio=0.18),
            run_time=1.35,
        )
        self.play(FadeIn(factor_links), run_time=0.55)
        # Beat 24 reveal_triangle_count: settled semantic step.
        self.next_slide()
        self.play(
            GrowArrow(answer_arrows[0]),
            GrowArrow(answer_arrows[1]),
            TransformFromCopy(factor_links[0], final_answers[0]),
            TransformFromCopy(factor_links[1], final_answers[1]),
            run_time=0.9,
        )
        self.play(FadeIn(final_answer_label), run_time=0.55)
        self.wait(0.4)
