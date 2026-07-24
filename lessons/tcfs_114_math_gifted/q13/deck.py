"""Manim Slides lesson for ROC 114 TCFSH gifted mathematics Q13."""

from __future__ import annotations

import numpy as np

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    REGION,
    WHITE,
    CarloSlide,
    label,
)
from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class CarloTcfs114MathQ13(CarloSlide):
    """Turn the source inconsistency into a visible, verifiable contradiction."""

    lesson_id = "carlo.tcfs_114_math_gifted.q13"

    @staticmethod
    def stage_title(text: str, color: str = INK):
        title = label(text, 31, color, "BOLD")
        title.move_to([0, 3.15, 0])
        return title

    @staticmethod
    def divider(x: float) -> Line:
        return Line([x, 2.2, 0], [x, -2.45, 0], color=HAIRLINE, stroke_width=2)

    def construct(self) -> None:
        heading = label("114 中一中資優｜填充第 13 題", 24, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.34)
        source = label("解題來源：正哥愛數學", 16, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.22)
        self.add(heading, source)

        # Beat 01 meet_claim: Ask whether the stated total is even attainable.
        self.begin_beat("meet_claim")
        title = self.stage_title("先別找 a：345 真的可能出現嗎？")
        equation = MathTex(
            r"\lfloor x\rfloor\{x\}=a x^2,\qquad a>0",
            font_size=62,
            color=INK,
        ).move_to([0, 1.15, 0])
        total = MathTex(
            r"\sum_{i=1}^{m}x_i=345",
            font_size=56,
            color=POINT,
        ).move_to([0, -0.35, 0])
        question = label("先檢查『存在』，再談『求值』", 30, MUTED, "BOLD")
        question.move_to([0, -1.65, 0])
        self.play(FadeIn(title), Write(equation), run_time=1.0)
        self.play(Write(total), run_time=0.8)
        self.play(FadeIn(question), run_time=0.6)

        # Beat 02 split_number: Give floor and fractional part a concrete picture.
        self.next_beat("split_number")
        split_title = self.stage_title("x = 整數台階 + 不滿 1 的餘量")
        number_line = NumberLine(
            x_range=[0, 7, 1],
            length=10.5,
            include_numbers=True,
            font_size=25,
            color=MUTED,
        ).move_to([0, -0.45, 0])
        n_value = 4
        x_value = 4.38
        n_dot = Dot(number_line.n2p(n_value), radius=0.08, color=BLUE)
        x_dot = Dot(number_line.n2p(x_value), radius=0.10, color=POINT)
        n_tag = MathTex(r"n=\lfloor x\rfloor", font_size=38, color=BLUE)
        n_tag.next_to(n_dot, UP, buff=0.22)
        x_tag = MathTex("x", font_size=38, color=POINT).next_to(x_dot, DOWN, buff=0.20)
        integer_span = Line(number_line.n2p(0), number_line.n2p(n_value), color=BLUE, stroke_width=8)
        remainder_span = Line(number_line.n2p(n_value), number_line.n2p(x_value), color=POINT, stroke_width=10)
        split_formula = MathTex(
            r"x=n+r,\qquad r=\{x\},\qquad 0\le r<1",
            font_size=47,
            color=INK,
        ).move_to([0, 1.45, 0])
        strip_formula = MathTex(r"n\le x<n+1", font_size=43, color=REGION)
        strip_formula.move_to([0, -2.0, 0])
        self.play(
            ReplacementTransform(title, split_title),
            FadeOut(equation, total, question),
            FadeIn(number_line),
            run_time=0.8,
        )
        self.play(Create(integer_span), FadeIn(n_dot, n_tag), run_time=0.65)
        self.play(Create(remainder_span), FadeIn(x_dot, x_tag), run_time=0.65)
        self.play(Write(split_formula), FadeIn(strip_formula), run_time=0.75)

        # Beat 03 sign_filter: Keep zero but remove every other nonpositive case.
        self.next_beat("sign_filter")
        sign_title = self.stage_title("非零解只能落在 n ≥ 1 的區間")
        left_divider = self.divider(-2.65)
        right_divider = self.divider(2.65)
        neg_head = MathTex("x<0", font_size=44, color=CORAL).move_to([-5.2, 1.45, 0])
        neg_lhs = MathTex(
            r"\lfloor x\rfloor\{x\}\le0",
            font_size=36,
            color=CORAL,
        ).move_to([-5.2, 0.35, 0])
        neg_rhs = MathTex(r"a x^2>0", font_size=36, color=POINT).move_to([-5.2, -0.45, 0])
        neg_no = label("不可能", 27, CORAL, "BOLD").move_to([-5.2, -1.55, 0])
        zero_head = MathTex("x=0", font_size=44, color=BLUE).move_to([0, 1.45, 0])
        zero_eq = MathTex("0=0", font_size=42, color=BLUE).move_to([0, 0.25, 0])
        zero_note = label("是解，但總和只加 0", 26, MUTED, "BOLD").move_to([0, -1.15, 0])
        pos_head = MathTex("0<x<1", font_size=44, color=CORAL).move_to([5.2, 1.45, 0])
        pos_lhs = MathTex(r"\lfloor x\rfloor\{x\}=0", font_size=34, color=CORAL)
        pos_lhs.move_to([5.2, 0.35, 0])
        pos_rhs = MathTex(r"a x^2>0", font_size=36, color=POINT).move_to([5.2, -0.45, 0])
        pos_no = MathTex(r"\Rightarrow n\ge1", font_size=39, color=REGION)
        pos_no.move_to([5.2, -1.55, 0])
        self.play(
            ReplacementTransform(split_title, sign_title),
            FadeOut(
                number_line,
                n_dot,
                x_dot,
                n_tag,
                x_tag,
                integer_span,
                remainder_span,
                split_formula,
                strip_formula,
            ),
            Create(left_divider),
            Create(right_divider),
            run_time=0.8,
        )
        self.play(FadeIn(neg_head, zero_head, pos_head), run_time=0.45)
        self.play(Write(neg_lhs), Write(neg_rhs), FadeIn(neg_no), run_time=0.7)
        self.play(Write(zero_eq), FadeIn(zero_note), run_time=0.55)
        self.play(Write(pos_lhs), Write(pos_rhs), Write(pos_no), run_time=0.7)

        # Beat 04 normalize_strip: Compress every integer strip into y(1-y).
        self.next_beat("normalize_strip")
        norm_title = self.stage_title("每一個整數區間，其實共用同一個比例")
        strip = MathTex(r"n\le x<n+1,\qquad n\ge1", font_size=43, color=REGION)
        strip.move_to([0, 1.65, 0])
        line_one = MathTex(r"n(x-n)=a x^2", font_size=52, color=INK).move_to([0, 0.50, 0])
        line_two = MathTex(
            r"a=\frac nx\left(1-\frac nx\right)",
            font_size=52,
            color=INK,
        ).move_to([0, -0.55, 0])
        line_three = MathTex(r"y=\frac nx\quad\Longrightarrow\quad a=y(1-y)", font_size=52, color=POINT)
        line_three.move_to([0, -1.65, 0])
        self.play(
            ReplacementTransform(sign_title, norm_title),
            FadeOut(
                left_divider,
                right_divider,
                neg_head,
                neg_lhs,
                neg_rhs,
                neg_no,
                zero_head,
                zero_eq,
                zero_note,
                pos_head,
                pos_lhs,
                pos_rhs,
                pos_no,
            ),
            FadeIn(strip),
            run_time=0.8,
        )
        self.play(Write(line_one), run_time=0.6)
        self.play(TransformFromCopy(line_one, line_two), run_time=0.75)
        self.play(TransformFromCopy(line_two, line_three), run_time=0.75)

        # Beat 05 choose_branch: Reject the symmetric root that leaves its strip.
        self.next_beat("choose_branch")
        branch_title = self.stage_title("對稱的兩個比例，只有一個待得住")
        axes = Axes(
            x_range=[0, 1.05, 0.25],
            y_range=[0, 0.30, 0.10],
            x_length=6.0,
            y_length=3.4,
            axis_config={"color": MUTED, "stroke_width": 2},
            tips=False,
        ).move_to([-3.8, -0.25, 0])
        curve = axes.plot(lambda y: y * (1 - y), x_range=[0, 1], color=REGION, stroke_width=5)
        level = 0.16
        t_value = 0.20
        horizontal = DashedLine(
            axes.c2p(0, level),
            axes.c2p(1, level),
            color=POINT,
            dash_length=0.09,
        )
        t_dot = Dot(axes.c2p(t_value, level), radius=0.08, color=CORAL)
        other_dot = Dot(axes.c2p(1 - t_value, level), radius=0.08, color=BLUE)
        t_label = MathTex("t", font_size=34, color=CORAL).next_to(t_dot, DOWN, buff=0.12)
        other_label = MathTex("1-t", font_size=34, color=BLUE).next_to(other_dot, DOWN, buff=0.12)
        graph_label = MathTex("a=y(1-y)", font_size=35, color=REGION).next_to(axes, UP, buff=0.08)
        bad = MathTex(
            r"\frac nx=t\Rightarrow x=\frac nt\ge2n\ge n+1",
            font_size=39,
            color=CORAL,
        ).move_to([3.85, 0.80, 0])
        bad_note = label("離開自己的區間", 25, CORAL, "BOLD").move_to([3.85, 0.05, 0])
        good = MathTex(
            r"\frac nx=1-t\Rightarrow x_n=\frac n{1-t}=cn",
            font_size=39,
            color=BLUE,
        ).move_to([3.85, -0.95, 0])
        c_note = MathTex(r"c=\frac1{1-t}>1", font_size=37, color=POINT).move_to([3.85, -1.70, 0])
        self.play(
            ReplacementTransform(norm_title, branch_title),
            FadeOut(strip, line_one, line_two, line_three),
            FadeIn(axes, graph_label),
            Create(curve),
            run_time=0.9,
        )
        self.play(Create(horizontal), FadeIn(t_dot, other_dot, t_label, other_label), run_time=0.7)
        self.play(Write(bad), FadeIn(bad_note), run_time=0.75)
        self.play(Write(good), Write(c_note), run_time=0.8)

        # Beat 06 march_candidates: Show why valid indices form one initial block.
        self.next_beat("march_candidates")
        march_title = self.stage_title("偏移量只增不減，所以候選解連續出現")
        march_line = NumberLine(
            x_range=[0, 7, 1],
            length=11.2,
            include_numbers=True,
            font_size=23,
            color=MUTED,
        ).move_to([0, -0.40, 0])
        example_c = 1.12
        candidate_dots = VGroup(
            *[
                Dot(march_line.n2p(example_c * n), radius=0.075, color=POINT)
                for n in range(1, 7)
            ]
        )
        integer_ticks = VGroup(
            *[
                Dot(march_line.n2p(n), radius=0.055, color=BLUE)
                for n in range(1, 7)
            ]
        )
        arrows = VGroup(
            *[
                Line(
                    march_line.n2p(n) + UP * 0.13,
                    march_line.n2p(example_c * n) + UP * 0.13,
                    color=REGION,
                    stroke_width=5,
                )
                for n in range(1, 7)
            ]
        )
        example_note = label("示意：c=1.12（只看偏移如何累積）", 25, MUTED, "MEDIUM")
        example_note.move_to([0, 1.70, 0])
        offset = MathTex(r"x_n-n=(c-1)n", font_size=48, color=REGION).move_to([0, -1.45, 0])
        monotone = label("一旦碰到右端點，後面的格子都不再可行", 29, POINT, "BOLD")
        monotone.move_to([0, -2.20, 0])
        self.play(
            ReplacementTransform(branch_title, march_title),
            FadeOut(
                axes,
                curve,
                horizontal,
                t_dot,
                other_dot,
                t_label,
                other_label,
                graph_label,
                bad,
                bad_note,
                good,
                c_note,
            ),
            FadeIn(march_line, example_note, integer_ticks),
            run_time=0.9,
        )
        self.play(Create(arrows), FadeIn(candidate_dots), run_time=1.1)
        self.play(Write(offset), FadeIn(monotone), run_time=0.8)

        # Beat 07 sum_candidates: Translate the visible arithmetic progression.
        self.next_beat("sum_candidates")
        sum_title = self.stage_title("若最後編號是 N，345 就固定了 c")
        sequence = MathTex(
            r"x_1=c,\quad x_2=2c,\quad\ldots,\quad x_N=Nc",
            font_size=49,
            color=BLUE,
        ).move_to([0, 1.35, 0])
        sum_one = MathTex(
            r"0+x_1+x_2+\cdots+x_N",
            "=",
            r"c(1+2+\cdots+N)",
            font_size=45,
            color=INK,
        ).move_to([0, 0.10, 0])
        sum_one[0].set_color(MUTED)
        sum_one[2].set_color(REGION)
        sum_two = MathTex(
            r"\frac{cN(N+1)}2=345",
            font_size=56,
            color=POINT,
        ).move_to([0, -1.10, 0])
        solve_c = MathTex(
            r"c=\frac{690}{N(N+1)}",
            font_size=55,
            color=POINT,
        ).move_to([0, -2.05, 0])
        self.play(
            ReplacementTransform(march_title, sum_title),
            FadeOut(march_line, example_note, integer_ticks, candidate_dots, arrows, offset, monotone),
            FadeIn(sequence),
            run_time=0.75,
        )
        self.play(Write(sum_one), run_time=0.75)
        self.play(TransformFromCopy(sum_one, sum_two), run_time=0.7)
        self.play(TransformFromCopy(sum_two, solve_c), run_time=0.65)

        # Beat 08 build_two_bounds: Let the same N pass two necessary gates.
        self.next_beat("build_two_bounds")
        bounds_title = self.stage_title("同一個 N，必須同時通過兩扇門")
        middle = self.divider(0)
        left_head = MathTex("c>1", font_size=47, color=BLUE).move_to([-4.0, 1.45, 0])
        left_a = MathTex(r"\frac{690}{N(N+1)}>1", font_size=41, color=INK).move_to([-4.0, 0.45, 0])
        left_b = MathTex(r"N(N+1)<690", font_size=44, color=POINT).move_to([-4.0, -0.50, 0])
        left_c = MathTex(r"\Longrightarrow N\le25", font_size=48, color=CORAL).move_to([-4.0, -1.55, 0])
        right_head = MathTex(r"x_N<N+1", font_size=47, color=BLUE).move_to([4.0, 1.45, 0])
        right_a = MathTex(r"cN<N+1", font_size=41, color=INK).move_to([4.0, 0.45, 0])
        right_b = MathTex(r"\frac{690}{N+1}<N+1", font_size=42, color=POINT).move_to([4.0, -0.50, 0])
        right_c = MathTex(r"\Longrightarrow690<(N+1)^2", font_size=43, color=CORAL)
        right_c.move_to([4.0, -1.55, 0])
        self.play(
            ReplacementTransform(sum_title, bounds_title),
            FadeOut(sequence, sum_one, sum_two, solve_c),
            Create(middle),
            FadeIn(left_head, right_head),
            run_time=0.75,
        )
        self.play(Write(left_a), Write(right_a), run_time=0.65)
        self.play(Write(left_b), Write(right_b), run_time=0.7)
        self.play(Write(left_c), Write(right_c), run_time=0.7)

        # Beat 09 meet_contradiction: Make the incompatible numerical bounds collide.
        self.next_beat("meet_contradiction")
        contradiction_title = self.stage_title("兩個必要條件彼此矛盾")
        implication = MathTex(
            r"N\le25",
            r"\Longrightarrow",
            r"(N+1)^2\le26^2=676",
            font_size=53,
            color=INK,
        ).move_to([0, 1.05, 0])
        implication[0].set_color(BLUE)
        impossible = MathTex(
            r"690<(N+1)^2\le676",
            font_size=65,
            color=CORAL,
        ).move_to([0, -0.20, 0])
        cross_box = SurroundingRectangle(impossible, color=CORAL, buff=0.25, stroke_width=4)
        conclusion = label("原題 345：不存在正的 a", 38, POINT, "BOLD")
        conclusion.move_to([0, -1.75, 0])
        self.play(
            ReplacementTransform(bounds_title, contradiction_title),
            FadeOut(
                middle,
                left_head,
                left_a,
                left_b,
                left_c,
                right_head,
                right_a,
                right_b,
                right_c,
            ),
            Write(implication),
            run_time=0.8,
        )
        self.play(Write(impossible), Create(cross_box), run_time=0.8)
        self.play(FadeIn(conclusion), Indicate(conclusion, color=POINT), run_time=0.8)

        # Beat 10 separate_correction: Keep the source's corrected variant distinct.
        self.next_beat("separate_correction")
        correction_title = self.stage_title("來源後段改談 420：這是另一個問題")
        split = self.divider(0)
        original_head = label("原題", 30, MUTED, "BOLD").move_to([-4.0, 1.35, 0])
        original_sum = MathTex(r"\sum x=345", font_size=55, color=CORAL).move_to([-4.0, 0.25, 0])
        original_result = label("無正的 a", 34, CORAL, "BOLD").move_to([-4.0, -1.05, 0])
        corrected_head = label("更正版", 30, MUTED, "BOLD").move_to([4.0, 1.35, 0])
        corrected_sum = MathTex(r"\sum x=420", font_size=55, color=REGION).move_to([4.0, 0.25, 0])
        corrected_prompt = label("現在才計算新的 a", 30, REGION, "BOLD").move_to([4.0, -1.05, 0])
        source_note = label("公開影片先指出矛盾，再切換到更正版", 24, MUTED, "MEDIUM")
        source_note.move_to([0, -2.25, 0])
        self.play(
            ReplacementTransform(contradiction_title, correction_title),
            FadeOut(implication, impossible, cross_box, conclusion),
            Create(split),
            FadeIn(original_head, corrected_head),
            run_time=0.75,
        )
        self.play(Write(original_sum), FadeIn(original_result), run_time=0.6)
        self.play(Write(corrected_sum), FadeIn(corrected_prompt), run_time=0.6)
        self.play(FadeIn(source_note), run_time=0.45)

        # Beat 11 solve_corrected: Close the corrected case and verify its boundary.
        self.next_beat("solve_corrected")
        solved_title = self.stage_title("420 版本：算完，還要檢查下一格")
        bracket = MathTex(
            r"28\cdot29=812<840<841=29^2",
            font_size=48,
            color=POINT,
        ).move_to([0, 1.60, 0])
        values = MathTex(
            r"N=28,\qquad c=\frac{840}{28\cdot29}=\frac{210}{203}",
            font_size=45,
            color=INK,
        ).move_to([0, 0.65, 0])
        parameter = MathTex(
            r"t=1-\frac1c=\frac1{30},\qquad a=t(1-t)=\frac{29}{900}",
            font_size=45,
            color=REGION,
        ).move_to([0, -0.25, 0])
        boundary = MathTex(
            r"x_{29}=c\cdot29=30\notin[29,30)",
            font_size=43,
            color=BLUE,
        ).move_to([0, -1.15, 0])
        original_final = label("345：無正 a", 31, CORAL, "BOLD")
        corrected_final = label("420：a = 29/900", 31, REGION, "BOLD")
        original_box = SurroundingRectangle(original_final, color=CORAL, buff=0.22, stroke_width=3)
        corrected_box = SurroundingRectangle(corrected_final, color=REGION, buff=0.22, stroke_width=3)
        final_group = VGroup(
            VGroup(original_box, original_final),
            VGroup(corrected_box, corrected_final),
        ).arrange(RIGHT, buff=1.20).move_to([0, -2.20, 0])
        self.play(
            ReplacementTransform(correction_title, solved_title),
            FadeOut(
                split,
                original_head,
                original_sum,
                original_result,
                corrected_head,
                corrected_sum,
                corrected_prompt,
                source_note,
            ),
            Write(bracket),
            run_time=0.8,
        )
        self.play(Write(values), run_time=0.7)
        self.play(Write(parameter), run_time=0.75)
        self.play(Write(boundary), run_time=0.65)
        self.play(FadeIn(final_group), run_time=0.75)
