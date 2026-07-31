"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q5."""

from __future__ import annotations

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
    Arrow,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class Tcfs115Q05Slide(CarloSlide):
    """Turn a ratio-scale conjecture into an integer-bound proof."""

    lesson_id = "carlo.tcfs_115_math_gifted.q05"

    @staticmethod
    def ratio_fraction(index: str, addition: str, *, size: int = 42) -> MathTex:
        addition_tex = f"+{addition}"
        return MathTex(
            rf"\frac{{a_{{{index}}}}}{{a_{{{index}}}{addition_tex}}}",
            font_size=size,
            color=INK,
            substrings_to_isolate=[addition_tex],
            tex_to_color_map={addition_tex: POINT},
        )

    @staticmethod
    def scale_bar(
        factor: int,
        blue_text: str,
        yellow_text: str,
        *,
        center: tuple[float, float, float] = (0.0, -0.15, 0.0),
    ) -> VGroup:
        blue_width = 2.05 * factor
        yellow_width = 0.80 * factor
        total_width = blue_width + yellow_width
        blue = Rectangle(
            width=blue_width,
            height=0.88,
            color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.30,
        )
        yellow = Rectangle(
            width=yellow_width,
            height=0.88,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.32,
        )
        blue.move_to(LEFT * yellow_width / 2)
        yellow.move_to(RIGHT * blue_width / 2)
        blue_label = label(blue_text, 28, BLUE, "BOLD").move_to(blue)
        yellow_label = label(yellow_text, 28, POINT, "BOLD").move_to(yellow)
        factor_label = label(f"{factor} 倍", 25, MUTED, "BOLD")
        factor_label.next_to(VGroup(blue, yellow), DOWN, buff=0.20)
        result = VGroup(blue, yellow, blue_label, yellow_label, factor_label)
        result.move_to(center)
        # Stabilize target dimensions when text changes during Transform.
        result[0].set_width(blue_width)
        result[1].set_width(yellow_width)
        assert abs(total_width - result[0].width - result[1].width) < 1e-6
        return result

    @staticmethod
    def term_chip(tex: str, color: str) -> VGroup:
        box = Rectangle(
            width=2.05,
            height=0.88,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.10,
        )
        term = MathTex(tex, font_size=37, color=color)
        return VGroup(box, term)

    @staticmethod
    def pair_column(first: int) -> VGroup:
        last = 21 - first
        top = label(str(first), 23, BLUE, "BOLD")
        plus = label("+", 20, MUTED, "BOLD")
        bottom = label(str(last), 23, REGION, "BOLD")
        bar = Line(LEFT * 0.31, RIGHT * 0.31, color=HAIRLINE, stroke_width=2)
        result = label("21", 24, POINT, "BOLD")
        return VGroup(top, plus, bottom, bar, result).arrange(DOWN, buff=0.08)

    def construct(self) -> None:
        heading = label("第 5 題｜相同比例裡藏著怎樣的放大？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學｜第壹部分第 5 題", 16, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)
        self.add(heading, source)

        # Beat 01: read the equal-ratio chain before exposing the sum bound.
        self.begin_beat("equal_ratio_chain")
        ratio_items = VGroup(
            self.ratio_fraction("1", "2"),
            label("=", 32, MUTED, "BOLD"),
            self.ratio_fraction("2", "4"),
            label("=", 32, MUTED, "BOLD"),
            self.ratio_fraction("3", "6"),
            label("=", 32, MUTED, "BOLD"),
            label("⋯", 38, MUTED, "BOLD"),
            label("=", 32, MUTED, "BOLD"),
            self.ratio_fraction("19", "38"),
            label("=", 32, MUTED, "BOLD"),
            self.ratio_fraction("20", "40"),
        ).arrange(RIGHT, buff=0.22)
        ratio_items.scale_to_fit_width(13.6).move_to(UP * 0.65)
        prompt = label("這一串式子，真正固定的是什麼？", 35, INK, "BOLD")
        prompt.move_to(UP * 2.45)
        equal_focus = VGroup(*(ratio_items[index] for index in (1, 3, 5, 7, 9)))
        invariant = label("每一個分式的值都相同", 31, POINT, "BOLD")
        invariant.move_to(DOWN * 1.20)

        self.play(FadeIn(prompt), run_time=0.6)
        self.play(
            LaggedStart(*(FadeIn(item) for item in ratio_items), lag_ratio=0.08),
            run_time=1.4,
        )
        self.play(
            LaggedStart(
                *(Indicate(ratio_items[index], color=POINT) for index in (0, 2, 4, 8, 10)),
                lag_ratio=0.12,
            ),
            run_time=1.5,
        )
        self.play(Indicate(equal_focus, color=POINT), FadeIn(invariant), run_time=0.9)
        self.wait(0.30)

        # Beat 02: turn the first fraction into a two-part visual ratio.
        self.next_beat("focus_first_ratio")
        first_ratio = self.ratio_fraction("1", "2", size=55).move_to(UP * 1.85)
        bar_model = self.scale_bar(1, "a₁", "2")
        model_title = label("藍色部分，占整體多少？", 32, INK, "BOLD")
        model_title.move_to(UP * 3.05)
        model_note = label("示意模型｜其他項的符號尚未證明", 24, CORAL, "MEDIUM")
        model_note.move_to(DOWN * 1.55)
        ratio_brace = Line(
            bar_model[0].get_corner(DOWN + LEFT) + DOWN * 0.10,
            bar_model[1].get_corner(DOWN + RIGHT) + DOWN * 0.10,
            color=MUTED,
            stroke_width=3,
        )

        self.play(
            FadeOut(prompt),
            FadeOut(invariant),
            FadeOut(ratio_items),
            FadeIn(model_title),
            TransformFromCopy(ratio_items[0], first_ratio),
            run_time=0.9,
        )
        self.play(FadeIn(bar_model), Create(ratio_brace), FadeIn(model_note), run_time=0.9)
        self.play(Indicate(bar_model[0], color=BLUE), Indicate(bar_model[1], color=POINT))
        self.wait(0.30)

        # Beat 03: the loop starts and ends on exactly the one-times model.
        self.next_beat("scale_model", loop=True)
        model_two = self.scale_bar(2, "?", "4")
        model_three = self.scale_bar(3, "?", "6")
        model_one_again = self.scale_bar(1, "a₁", "2")
        self.wait(0.40)
        self.play(
            Transform(bar_model, model_two),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.15,
        )
        self.play(
            Transform(bar_model, model_three),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.15,
        )
        self.play(
            Transform(bar_model, model_one_again),
            rate_func=rate_functions.ease_in_out_sine,
            run_time=1.15,
        )
        self.wait(0.40)

        # Beat 04: place the first and nth ratios together, leaving a real gap.
        self.next_beat("pose_nth_term")
        first_bar = self.scale_bar(1, "a₁", "2", center=(0.0, 0.75, 0.0))
        nth_bar = self.scale_bar(2, "?", "2n", center=(0.0, -0.85, 0.0))
        first_tag = MathTex(r"\frac{a_1}{a_1+2}", font_size=40, color=INK)
        first_tag.next_to(first_bar, LEFT, buff=0.65)
        nth_tag = MathTex(r"\frac{a_n}{a_n+2n}", font_size=40, color=INK)
        nth_tag.next_to(nth_bar, LEFT, buff=0.65)
        same_ratio = label("相同", 26, POINT, "BOLD").move_to([-3.65, -0.05, 0])
        question = MathTex(
            r"a_n",
            r"\ ?=\ ",
            r"n a_1",
            font_size=50,
            color=INK,
        ).move_to([4.40, -0.15, 0])
        question[0].set_color(BLUE)
        question[2].set_color(POINT)
        pose_title = label("黃色乘 n，藍色要變成多少？", 32, INK, "BOLD")
        pose_title.move_to(model_title)
        pending = label("從圖猜想，還沒有證明", 24, CORAL, "BOLD")
        pending.move_to([4.35, -1.40, 0])

        self.play(
            ReplacementTransform(model_title, pose_title),
            FadeOut(first_ratio),
            FadeOut(ratio_brace),
            Transform(bar_model, first_bar),
            FadeOut(model_note),
            run_time=0.8,
        )
        self.play(
            FadeIn(nth_bar, shift=DOWN * 0.15),
            FadeIn(first_tag),
            FadeIn(nth_tag),
            FadeIn(same_ratio),
            run_time=0.9,
        )
        self.play(Write(question[0:2]), run_time=0.55)
        self.wait(0.35)
        self.play(Write(question[2]), FadeIn(pending), run_time=0.65)
        self.wait(0.30)

        # Beat 05: prove the scale relation without assuming signs.
        self.next_beat("derive_nth_term")
        given = MathTex(
            r"\frac{a_1}{a_1+2}",
            "=",
            r"\frac{a_n}{a_n+2n}",
            font_size=42,
            color=INK,
        ).move_to(UP * 2.45)
        cross = MathTex(
            r"a_1(a_n+2n)",
            "=",
            r"a_n(a_1+2)",
            font_size=43,
            color=INK,
        ).move_to(UP * 1.10)
        expanded = MathTex(
            r"a_1a_n",
            "+",
            r"2na_1",
            "=",
            r"a_1a_n",
            "+",
            r"2a_n",
            font_size=42,
            color=INK,
        ).move_to(DOWN * 0.10)
        expanded[0].set_color(MUTED)
        expanded[4].set_color(MUTED)
        cancel_left = Line(
            expanded[0].get_corner(DOWN + LEFT),
            expanded[0].get_corner(UP + RIGHT),
            color=CORAL,
            stroke_width=3,
        )
        cancel_right = Line(
            expanded[4].get_corner(DOWN + LEFT),
            expanded[4].get_corner(UP + RIGHT),
            color=CORAL,
            stroke_width=3,
        )
        reduced = MathTex(r"2na_1=2a_n", font_size=44, color=INK)
        reduced.move_to(DOWN * 1.25)
        nth_result = MathTex(r"a_n=na_1", font_size=52, color=POINT)
        nth_result.move_to(DOWN * 2.35)
        rigorous_note = label("不需要預先假設 aₙ 的正負", 23, MUTED, "MEDIUM")
        rigorous_note.move_to([4.95, -2.35, 0])

        self.play(
            FadeOut(pose_title),
            FadeOut(bar_model),
            FadeOut(nth_bar),
            FadeOut(first_tag),
            FadeOut(nth_tag),
            FadeOut(same_ratio),
            FadeOut(question),
            FadeOut(pending),
            FadeIn(given),
            run_time=0.85,
        )
        self.play(TransformFromCopy(given, cross), run_time=0.9)
        self.play(Write(expanded), run_time=0.9)
        self.play(Create(cancel_left), Create(cancel_right), run_time=0.6)

        # Beat 06: finish the cancellation only after the shared term is visible.
        self.next_beat("solve_scale_relation")
        self.play(TransformFromCopy(expanded, reduced), run_time=0.75)
        self.play(TransformFromCopy(reduced, nth_result), FadeIn(rigorous_note), run_time=0.8)
        self.wait(0.30)

        # Beat 06: collapse twenty variables to one free parameter.
        self.next_beat("build_sequence")
        sequence_title = label("二十個未知數，其實只有一個自由量", 32, INK, "BOLD")
        sequence_title.move_to(UP * 3.0)
        chips = VGroup(
            self.term_chip(r"a_1", BLUE),
            self.term_chip(r"2a_1", BLUE),
            self.term_chip(r"3a_1", BLUE),
            self.term_chip(r"\cdots", MUTED),
            self.term_chip(r"20a_1", BLUE),
        ).arrange(RIGHT, buff=0.28).move_to(DOWN * 0.10)
        sequence_formula = MathTex(
            r"a_1,\ 2a_1,\ 3a_1,\ \ldots,\ 20a_1",
            font_size=46,
            color=INK,
        ).move_to(UP * 1.45)
        one_control = label("每一項都由同一個 a₁ 控制", 28, POINT, "BOLD")
        one_control.move_to(DOWN * 1.45)
        algebra_context = VGroup(
            given,
            cross,
            expanded,
            cancel_left,
            cancel_right,
            reduced,
            rigorous_note,
        )

        self.play(FadeOut(algebra_context), FadeIn(sequence_title), run_time=0.7)
        self.play(TransformFromCopy(nth_result, sequence_formula), run_time=0.8)
        self.play(
            LaggedStart(*(FadeIn(chip, shift=UP * 0.12) for chip in chips), lag_ratio=0.15),
            run_time=1.2,
        )
        self.play(FadeIn(one_control), run_time=0.5)
        self.wait(0.30)

        # Beat 07: introduce the strict sum bound only after the sequence is known.
        self.next_beat("pose_sum_limit")
        given_sum = MathTex(
            r"a_1+a_2+\cdots+a_{20}<2026",
            font_size=47,
            color=INK,
        ).move_to(UP * 1.35)
        coefficient_bound = MathTex(
            r"a_1(1+2+3+\cdots+20)<2026",
            font_size=47,
            color=INK,
        ).move_to(DOWN * 0.15)
        coefficient_bound.set_color_by_tex("<", CORAL)
        sum_prompt = label("現在只差：1+2+⋯+20 是多少？", 31, INK, "BOLD")
        sum_prompt.move_to(DOWN * 1.55)

        self.play(
            FadeOut(sequence_title),
            FadeOut(sequence_formula),
            FadeOut(one_control),
            FadeIn(given_sum),
            run_time=0.7,
        )
        self.play(TransformFromCopy(chips, coefficient_bound), run_time=0.9)
        self.play(FadeOut(chips), FadeIn(sum_prompt), run_time=0.55)
        self.wait(0.30)

        # Beat 08: derive the triangular number by ten visible endpoint pairs.
        self.next_beat("pair_coefficients")
        pair_title = label("首尾配對：每一欄都是 21", 32, INK, "BOLD")
        pair_title.move_to(UP * 3.05)
        pairs = VGroup(*(self.pair_column(first) for first in range(1, 11)))
        pairs.arrange(RIGHT, buff=0.38).scale_to_fit_width(12.8).move_to(DOWN * 0.25)
        ten_pairs = label("剛好 10 對", 29, POINT, "BOLD")
        ten_pairs.move_to(DOWN * 2.55)

        self.play(
            FadeOut(given_sum),
            FadeOut(coefficient_bound),
            FadeOut(sum_prompt),
            FadeOut(nth_result),
            FadeIn(pair_title),
            run_time=0.65,
        )
        self.play(
            LaggedStart(*(FadeIn(pair, shift=UP * 0.14) for pair in pairs), lag_ratio=0.10),
            run_time=1.7,
        )
        self.play(
            LaggedStart(*(Indicate(pair[-1], color=POINT) for pair in pairs), lag_ratio=0.08),
            FadeIn(ten_pairs),
            run_time=1.25,
        )
        self.wait(0.30)

        # Beat 09: move the visible ten 21s into the inequality.
        self.next_beat("sum_coefficients")
        ten_twenty_one = MathTex(r"10\times21=210", font_size=52, color=INK)
        ten_twenty_one.move_to(UP * 1.35)
        final_bound = MathTex(r"210a_1<2026", font_size=54, color=INK)
        final_bound.set_color_by_tex("210", POINT)
        final_bound.set_color_by_tex("<", CORAL)
        final_bound.move_to(DOWN * 0.35)
        mini_twenty_ones = VGroup(
            *(label("21", 20, POINT, "BOLD") for _ in range(10))
        ).arrange(RIGHT, buff=0.20).move_to(DOWN * 1.65)

        self.play(FadeOut(pair_title), FadeOut(ten_pairs), run_time=0.45)
        self.play(
            LaggedStart(
                *(
                    TransformFromCopy(pair[-1], mini_twenty_ones[index])
                    for index, pair in enumerate(pairs)
                ),
                lag_ratio=0.07,
            ),
            run_time=1.25,
        )
        self.play(TransformFromCopy(mini_twenty_ones, ten_twenty_one), run_time=0.8)
        self.play(TransformFromCopy(ten_twenty_one, final_bound), FadeOut(pairs), run_time=0.8)
        self.wait(0.30)

        # Beat 10: preserve the strict inequality on a number line.
        self.next_beat("bound_a1")
        divided_bound = MathTex(
            r"a_1<\frac{2026}{210}\approx9.648",
            font_size=47,
            color=INK,
        ).move_to(UP * 1.75)
        divided_bound.set_color_by_tex("<", CORAL)
        number_line = NumberLine(
            x_range=[8, 11, 0.5],
            length=10.5,
            include_numbers=True,
            font_size=26,
            color=MUTED,
        ).move_to(DOWN * 0.40)
        cutoff = number_line.n2p(2026 / 210)
        cutoff_dot = Dot(cutoff, radius=0.10, color=CORAL)
        cutoff_label = MathTex(r"\frac{2026}{210}", font_size=31, color=CORAL)
        cutoff_label.next_to(cutoff_dot, UP, buff=0.18)
        nine_dot = Dot(number_line.n2p(9), radius=0.11, color=POINT)
        nine_prompt = label("最大的正整數候選：9", 30, POINT, "BOLD")
        nine_prompt.move_to(DOWN * 1.70)

        self.play(
            FadeOut(ten_twenty_one),
            FadeOut(mini_twenty_ones),
            ReplacementTransform(final_bound, divided_bound),
            Create(number_line),
            run_time=1.0,
        )
        self.play(FadeIn(cutoff_dot), FadeIn(cutoff_label), run_time=0.55)
        self.play(FadeIn(nine_dot), FadeIn(nine_prompt), Indicate(nine_dot, color=POINT))
        self.wait(0.30)

        # Beat 11: test both sides of the integer boundary.
        self.next_beat("test_neighboring_integers")
        test_nine = MathTex(
            r"210\times9=1890<2026",
            font_size=46,
            color=INK,
        ).move_to(UP * 1.05)
        test_nine.set_color_by_tex("9", POINT)
        test_nine.set_color_by_tex("<", REGION)
        pass_label = label("可行", 30, REGION, "BOLD").next_to(test_nine, RIGHT, buff=0.45)
        test_ten = MathTex(
            r"210\times10=2100>2026",
            font_size=46,
            color=INK,
        ).move_to(DOWN * 0.55)
        test_ten.set_color_by_tex("10", CORAL)
        test_ten.set_color_by_tex(">", CORAL)
        fail_label = label("越界", 30, CORAL, "BOLD").next_to(test_ten, RIGHT, buff=0.45)
        ten_strike = Line(
            test_ten.get_corner(DOWN + LEFT),
            test_ten.get_corner(UP + RIGHT),
            color=CORAL,
            stroke_width=4,
        )
        boundary_title = label("9 可以做到；下一個整數 10 已經超過", 32, INK, "BOLD")
        boundary_title.move_to(UP * 2.75)

        self.play(
            FadeOut(divided_bound),
            FadeOut(number_line),
            FadeOut(cutoff_dot),
            FadeOut(cutoff_label),
            FadeOut(nine_dot),
            FadeOut(nine_prompt),
            FadeIn(boundary_title),
            run_time=0.75,
        )
        self.play(Write(test_nine), FadeIn(pass_label), run_time=0.75)
        self.play(Write(test_ten), FadeIn(fail_label), Create(ten_strike), run_time=0.85)
        self.wait(0.30)

        # Beat 12: reconnect every conclusion to its reason before the answer.
        self.next_beat("consolidate")
        path_one = VGroup(
            label("相同比例", 28, INK, "BOLD"),
            label("⇒", 31, MUTED, "BOLD"),
            MathTex(r"a_n=na_1", font_size=39, color=BLUE),
        ).arrange(RIGHT, buff=0.22)
        path_two = MathTex(r"1+2+\cdots+20=210", font_size=39, color=INK)
        path_three = MathTex(r"210a_1<2026", font_size=43, color=INK)
        path_two.set_color_by_tex("210", POINT)
        path_three.set_color_by_tex("<", CORAL)
        reasoning_path = VGroup(path_one, path_two, path_three).arrange(DOWN, buff=0.40)
        reasoning_path.move_to([-2.65, 0.15, 0])
        arrows = VGroup(
            Arrow(path_one.get_bottom(), path_two.get_top(), buff=0.10, color=MUTED),
            Arrow(path_two.get_bottom(), path_three.get_top(), buff=0.10, color=MUTED),
        )
        answer_caption = label("a₁ 的最大值", 30, MUTED, "BOLD")
        answer_caption.move_to([4.25, 1.05, 0])
        answer = MathTex("9", font_size=82, color=POINT).move_to([4.25, -0.15, 0])
        answer_box = SurroundingRectangle(answer, color=POINT, buff=0.30, stroke_width=4)
        end_note = label("9 可行，10 越界", 27, INK, "BOLD")
        end_note.move_to([4.25, -1.45, 0])
        prior_tests = VGroup(boundary_title, test_nine, pass_label, test_ten, fail_label, ten_strike)

        self.play(FadeOut(prior_tests), FadeIn(reasoning_path), Create(arrows), run_time=1.0)
        self.play(FadeIn(answer_caption), FadeIn(answer), run_time=0.8)
        self.play(Create(answer_box), FadeIn(end_note), Circumscribe(answer, color=POINT), run_time=0.9)
        self.wait(0.30)
