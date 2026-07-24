"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Part 2 Q1."""

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
    WHITE,
    CarloSlide,
    label,
)
from manim import (
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


X_COLOR = BLUE
Y_COLOR = POINT
Z_COLOR = REGION
EQUATION_COLORS = (WHITE, BLUE, PURPLE)


class Tcfs115Part2Q01Slide(CarloSlide):
    """Reveal the symmetric factorization, then solve and verify both branches."""

    lesson_id = "carlo.tcfs_115_math_gifted.p2q01"

    @staticmethod
    def colored_math(tex: str, *, size: int = 40, color: str = INK) -> MathTex:
        """Typeset an equation while keeping the three variables recognizable."""
        equation = MathTex(
            tex,
            font_size=size,
            color=color,
            substrings_to_isolate=["x", "y", "z"],
        )
        equation.set_color_by_tex("x", X_COLOR)
        equation.set_color_by_tex("y", Y_COLOR)
        equation.set_color_by_tex("z", Z_COLOR)
        return equation

    @staticmethod
    def equation_row(
        number: int,
        tex: str,
        *,
        y: float,
        size: int = 38,
        badge_x: float = -6.25,
    ) -> VGroup:
        """Build one source equation with a fixed numbered badge."""
        badge_color = EQUATION_COLORS[number - 1]
        badge = Circle(radius=0.22, color=badge_color, stroke_width=3)
        badge.move_to([badge_x, y, 0])
        numeral = MathTex(str(number), font_size=24, color=badge_color)
        numeral.move_to(badge)
        equation = Tcfs115Part2Q01Slide.colored_math(tex, size=size)
        equation.next_to(badge, RIGHT, buff=0.32)
        return VGroup(badge, numeral, equation)

    @staticmethod
    def variable_marks(equation: MathTex, symbol: str, color: str) -> VGroup:
        """Outline every occurrence of one isolated variable."""
        matches = [
            equation.id_to_vgroup_dict[match_id]
            for tex_string, match_id in equation.matched_strings_and_ids
            if tex_string == symbol
        ]
        return VGroup(
            *(
                SurroundingRectangle(part, color=color, buff=0.055, stroke_width=2.4)
                for part in matches
            )
        )

    @staticmethod
    def branch_ribbon(*, active: str) -> VGroup:
        """Keep both zero-product branches visible while one is explored."""
        left_box = Rectangle(
            width=3.8,
            height=0.68,
            color=POINT,
            stroke_width=2.5,
            fill_color=POINT,
            fill_opacity=0.11,
        ).move_to([-2.05, 2.17, 0])
        right_box = Rectangle(
            width=4.25,
            height=0.68,
            color=REGION,
            stroke_width=2.5,
            fill_color=REGION,
            fill_opacity=0.11,
        ).move_to([2.25, 2.17, 0])
        left_text = MathTex(r"y=z", font_size=31, color=POINT).move_to(left_box)
        right_text = MathTex(
            r"x+y+z=3", font_size=31, color=REGION
        ).move_to(right_box)
        if active == "left":
            right_box.set_opacity(0.26)
            right_text.set_opacity(0.26)
        elif active == "right":
            left_box.set_opacity(0.26)
            left_text.set_opacity(0.26)
        return VGroup(left_box, left_text, right_box, right_text)

    @staticmethod
    def branch_card(
        factor_tex: str,
        result_tex: str,
        caption: str,
        color: str,
        *,
        center: tuple[float, float, float],
        width: float = 5.6,
        height: float = 1.85,
    ) -> VGroup:
        """Build a simple two-line case card for the branch diagram."""
        body = Rectangle(
            width=width,
            height=height,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.07,
        ).move_to(center)
        factor = MathTex(factor_tex, font_size=34, color=MUTED)
        result = MathTex(result_tex, font_size=42, color=color)
        contents = VGroup(factor, result).arrange(DOWN, buff=0.25).move_to(body)
        note = label(caption, 20, MUTED, "MEDIUM")
        note.next_to(body, DOWN, buff=0.16)
        return VGroup(body, contents, note)

    @staticmethod
    def candidate_pair(y_tex: str, z_tex: str, *, center: tuple[float, float, float]) -> VGroup:
        """Show one actual pairing on the sum branch."""
        body = Rectangle(
            width=5.45,
            height=1.35,
            color=REGION,
            stroke_width=2.5,
            fill_color=REGION,
            fill_opacity=0.07,
        ).move_to(center)
        y_value = MathTex(y_tex, font_size=34, color=Y_COLOR)
        z_value = MathTex(z_tex, font_size=34, color=Z_COLOR)
        values = VGroup(y_value, z_value).arrange(DOWN, buff=0.16).move_to(body)
        return VGroup(body, values)

    def construct(self) -> None:
        heading = label("第二部分第 1 題｜先相減，再分兩路", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label(
            "解題來源：正哥愛數學｜第二部分第 1 題｜PDF 第 9 頁",
            16,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.24)
        self.add(heading, source)

        equation_1 = r"x^2+xy+y^2=3(x+y)"
        equation_2 = r"x^2+xz+z^2=3(x+z)"
        equation_3 = r"y^2+yz+z^2=\frac52(y+z)+1"

        # Beat 01 meet_three_equations: meet the system before choosing a tactic.
        self.begin_beat("meet_three_equations")
        title_1 = label("三條二次式，但題目只問 y", 35, INK, "BOLD")
        title_1.move_to(UP * 2.88)
        subtitle_1 = label("先不急著同時解出 x、y、z", 25, MUTED, "MEDIUM")
        subtitle_1.move_to(UP * 2.28)
        rows_1 = VGroup(
            self.equation_row(1, equation_1, y=1.15, size=41),
            self.equation_row(2, equation_2, y=0.05, size=41),
            self.equation_row(3, equation_3, y=-1.05, size=39),
        )
        prompt_1 = label(
            "哪兩條式子最像，適合先相減？",
            30,
            POINT,
            "BOLD",
        ).move_to(DOWN * 2.55)
        body = VGroup(title_1, subtitle_1, rows_1, prompt_1)
        self.play(FadeIn(title_1), FadeIn(subtitle_1), run_time=0.7)
        self.play(
            LaggedStart(*(FadeIn(row) for row in rows_1), lag_ratio=0.22),
            run_time=1.5,
        )
        self.play(FadeIn(prompt_1), run_time=0.55)
        self.play(
            LaggedStart(
                Indicate(rows_1[0][2], color=WHITE),
                Indicate(rows_1[1][2], color=BLUE),
                Indicate(rows_1[2][2], color=PURPLE),
                lag_ratio=0.16,
            ),
            run_time=1.35,
        )
        self.wait(0.35)

        # Beat 02 notice_twin_pair: align the first two equations as one template.
        self.next_beat("notice_twin_pair")
        title_2 = label("第一式與第二式，共用同一個模具", 34, INK, "BOLD")
        title_2.move_to(UP * 2.88)
        row_21 = self.equation_row(1, equation_1, y=1.20, size=43)
        row_22 = self.equation_row(2, equation_2, y=0.00, size=43)
        y_marks = self.variable_marks(row_21[2], "y", Y_COLOR)
        z_marks = self.variable_marks(row_22[2], "z", Z_COLOR)
        swap = MathTex(
            "y", r"\longleftrightarrow", "z", font_size=54, color=INK
        ).move_to(DOWN * 1.32)
        swap[0].set_color(Y_COLOR)
        swap[2].set_color(Z_COLOR)
        swap_note = label("只換伙伴；位置與係數完全相同", 27, MUTED, "MEDIUM")
        swap_note.next_to(swap, DOWN, buff=0.28)
        prompt_2 = label("相減後，會留下哪個共同的差？", 27, POINT, "BOLD")
        prompt_2.move_to(DOWN * 2.80)
        body_2 = VGroup(
            title_2, row_21, row_22, y_marks, z_marks, swap, swap_note, prompt_2
        )
        self.play(FadeOut(body), FadeIn(title_2), run_time=0.65)
        self.play(FadeIn(row_21), FadeIn(row_22), run_time=0.75)
        self.play(Create(y_marks), Create(z_marks), run_time=0.9)
        self.play(Write(swap), FadeIn(swap_note), run_time=0.75)
        self.play(FadeIn(prompt_2), run_time=0.45)
        self.wait(0.35)
        body = body_2

        # Beat 03 subtract_first_two: let the common factor grow from the difference.
        self.next_beat("subtract_first_two")
        title_3 = label("做 (1) - (2)：共同因子一步步長出來", 33, INK, "BOLD")
        title_3.move_to(UP * 2.95)
        row_31 = self.equation_row(1, equation_1, y=2.10, size=29, badge_x=-5.65)
        row_32 = self.equation_row(2, equation_2, y=1.45, size=29, badge_x=-5.65)
        difference_1 = MathTex(
            r"x(y-z)+(y^2-z^2)=3(y-z)",
            font_size=39,
            color=INK,
            tex_to_color_map={r"y-z": POINT},
        ).move_to(UP * 0.48)
        difference_2 = MathTex(
            r"x(y-z)+(y-z)(y+z)=3(y-z)",
            font_size=39,
            color=INK,
            tex_to_color_map={r"y-z": POINT},
        ).move_to(DOWN * 0.43)
        difference_3 = MathTex(
            r"(y-z)(x+y+z)=3(y-z)",
            font_size=42,
            color=INK,
            tex_to_color_map={r"y-z": POINT},
        ).move_to(DOWN * 1.38)
        factorization = MathTex(
            r"(y-z)(x+y+z-3)=0",
            font_size=47,
            color=INK,
            tex_to_color_map={r"y-z": POINT, r"x+y+z-3": REGION},
        ).move_to(DOWN * 2.45)
        factor_frame = SurroundingRectangle(
            factorization, color=WHITE, buff=0.18, stroke_width=2.6
        )
        body_3 = VGroup(
            title_3,
            row_31,
            row_32,
            difference_1,
            difference_2,
            difference_3,
            factorization,
            factor_frame,
        )
        self.play(FadeOut(body), FadeIn(title_3), FadeIn(row_31), FadeIn(row_32))
        self.play(
            TransformFromCopy(VGroup(row_31[2], row_32[2]), difference_1),
            run_time=1.05,
        )
        self.play(Write(difference_2), run_time=0.8)
        self.play(Write(difference_3), run_time=0.8)
        self.play(Write(factorization), Create(factor_frame), run_time=0.9)
        self.wait(0.35)
        body = body_3

        # Beat 04 split_branches: use the zero product to open both complete cases.
        self.next_beat("split_branches")
        title_4 = label("零乘積打開兩條路", 35, INK, "BOLD")
        title_4.move_to(UP * 2.95)
        trunk = factorization.copy().scale(0.90).move_to(UP * 1.85)
        left_card = self.branch_card(
            r"y-z=0",
            r"y=z",
            "左支：兩個變數相等",
            POINT,
            center=(-3.35, -0.20, 0),
        )
        right_card = self.branch_card(
            r"x+y+z-3=0",
            r"x+y+z=3",
            "右支：三個變數的總和固定",
            REGION,
            center=(3.35, -0.20, 0),
        )
        left_arrow = Arrow(
            trunk.get_bottom() + LEFT * 0.75,
            left_card[0].get_top(),
            color=POINT,
            buff=0.16,
            stroke_width=4,
        )
        right_arrow = Arrow(
            trunk.get_bottom() + RIGHT * 0.75,
            right_card[0].get_top(),
            color=REGION,
            buff=0.16,
            stroke_width=4,
        )
        union_note = label(
            "兩支可以重疊；但所有解都在這兩支的聯集裡",
            26,
            MUTED,
            "MEDIUM",
        ).move_to(DOWN * 2.72)
        body_4 = VGroup(
            title_4, trunk, left_card, right_card, left_arrow, right_arrow, union_note
        )
        self.play(FadeOut(body), FadeIn(title_4), FadeIn(trunk), run_time=0.7)
        self.play(GrowArrow(left_arrow), FadeIn(left_card), run_time=0.85)
        self.play(GrowArrow(right_arrow), FadeIn(right_card), run_time=0.85)
        self.play(FadeIn(union_note), run_time=0.5)
        self.wait(0.35)
        body = body_4

        # Beat 05 enter_equal_branch: substitute z=y into the third equation.
        self.next_beat("enter_equal_branch")
        title_5 = label("先走左支：把 z 與 y 合在一起", 34, INK, "BOLD")
        title_5.move_to(UP * 3.00)
        ribbon_5 = self.branch_ribbon(active="left")
        row_53 = self.equation_row(3, equation_3, y=1.22, size=36, badge_x=-5.75)
        substitution_5 = self.colored_math(
            r"z=y\quad\Longrightarrow\quad y^2+y\cdot y+y^2=\frac52(y+y)+1",
            size=37,
        ).move_to(UP * 0.18)
        collected_5 = MathTex(r"3y^2=5y+1", font_size=45, color=INK)
        collected_5.set_color_by_tex("y", Y_COLOR)
        collected_5.move_to(DOWN * 0.85)
        polynomial_5 = MathTex(r"3y^2-5y-1=0", font_size=48, color=INK)
        polynomial_5.set_color_by_tex("y", Y_COLOR)
        polynomial_5.move_to(DOWN * 1.82)
        polynomial_frame_5 = SurroundingRectangle(
            polynomial_5, color=POINT, buff=0.18, stroke_width=3
        )
        note_5 = label("三個未知數，現在只剩 y", 26, POINT, "BOLD")
        note_5.move_to(DOWN * 2.72)
        body_5 = VGroup(
            title_5,
            ribbon_5,
            row_53,
            substitution_5,
            collected_5,
            polynomial_5,
            polynomial_frame_5,
            note_5,
        )
        self.play(FadeOut(body), FadeIn(title_5), FadeIn(ribbon_5), run_time=0.7)
        self.play(FadeIn(row_53), run_time=0.6)
        self.play(Write(substitution_5), run_time=0.9)
        self.play(Write(collected_5), run_time=0.65)
        self.play(Write(polynomial_5), Create(polynomial_frame_5), FadeIn(note_5), run_time=0.85)
        self.wait(0.35)
        body = body_5

        # Beat 06 solve_equal_branch: stage -B before completing the quadratic formula.
        self.next_beat("solve_equal_branch")
        title_6 = label("左支：二次公式的分子先算 -B", 34, INK, "BOLD")
        title_6.move_to(UP * 3.00)
        ribbon_6 = self.branch_ribbon(active="left")
        polynomial_6 = polynomial_5.copy().scale(0.91).move_to(UP * 1.34)
        coefficients_6 = MathTex(
            r"A=3,\qquad B=-5,\qquad C=-1", font_size=38, color=INK
        ).move_to([-2.45, 0.56, 0])
        b_step_6 = MathTex(r"-B=-(-5)=5", font_size=40, color=POINT)
        b_step_6.move_to([3.95, 0.56, 0])
        formula_6 = MathTex(
            r"y=\frac{-B\pm\sqrt{B^2-4AC}}{2A}",
            font_size=35,
            color=INK,
        ).move_to(DOWN * 0.12)
        substitute_6 = MathTex(
            r"y=\frac{5\pm\sqrt{25+12}}{6}", font_size=37, color=INK
        ).move_to(DOWN * 1.18)
        answer_6 = MathTex(
            r"y=\frac{5\pm\sqrt{37}}{6}", font_size=49, color=POINT
        ).move_to(DOWN * 2.50)
        answer_frame_6 = SurroundingRectangle(
            answer_6, color=POINT, buff=0.20, stroke_width=3
        )
        body_6 = VGroup(
            title_6,
            ribbon_6,
            polynomial_6,
            coefficients_6,
            b_step_6,
            formula_6,
            substitute_6,
            answer_6,
            answer_frame_6,
        )
        self.play(FadeOut(body), FadeIn(title_6), FadeIn(ribbon_6), FadeIn(polynomial_6))
        self.play(Write(coefficients_6), run_time=0.65)
        self.play(Write(b_step_6), run_time=0.65)
        self.play(Indicate(b_step_6, color=POINT), run_time=0.55)
        self.play(Write(formula_6), run_time=0.75)
        self.play(Write(substitute_6), run_time=0.75)
        self.play(Write(answer_6), Create(answer_frame_6), run_time=0.85)
        self.wait(0.35)
        body = body_6

        # Beat 07 enter_sum_branch: return to the fork and compress x+y+z into S.
        self.next_beat("enter_sum_branch")
        title_7 = label("回到分岔點，再走右支", 35, INK, "BOLD")
        title_7.move_to(UP * 3.00)
        ribbon_7 = self.branch_ribbon(active="right")
        left_memory_box = Rectangle(
            width=4.55,
            height=1.25,
            color=POINT,
            stroke_width=2.3,
            fill_color=POINT,
            fill_opacity=0.05,
        ).move_to([-4.20, 0.90, 0])
        left_memory = MathTex(
            r"y=\frac{5\pm\sqrt{37}}6", font_size=35, color=POINT
        ).move_to(left_memory_box)
        left_memory_group = VGroup(left_memory_box, left_memory).set_opacity(0.34)

        x_chip = Rectangle(
            width=1.25, height=0.68, color=X_COLOR, fill_color=X_COLOR, fill_opacity=0.13
        )
        y_chip = Rectangle(
            width=1.25, height=0.68, color=Y_COLOR, fill_color=Y_COLOR, fill_opacity=0.13
        )
        z_chip = Rectangle(
            width=1.25, height=0.68, color=Z_COLOR, fill_color=Z_COLOR, fill_opacity=0.13
        )
        chips = VGroup(x_chip, y_chip, z_chip).arrange(RIGHT, buff=0.16)
        chips.move_to([3.25, 0.72, 0])
        chip_labels = VGroup(
            MathTex("x", font_size=34, color=X_COLOR).move_to(x_chip),
            MathTex("y", font_size=34, color=Y_COLOR).move_to(y_chip),
            MathTex("z", font_size=34, color=Z_COLOR).move_to(z_chip),
        )
        sum_frame = SurroundingRectangle(chips, color=REGION, buff=0.24, stroke_width=3)
        sum_label = MathTex(r"S=x+y+z=3", font_size=37, color=REGION)
        sum_label.next_to(sum_frame, UP, buff=0.18)
        sum_model = VGroup(chips, chip_labels, sum_frame, sum_label)

        row_72 = self.equation_row(2, equation_2, y=-0.72, size=32, badge_x=-5.90)
        row_73 = self.equation_row(3, equation_3, y=-1.62, size=32, badge_x=-5.90)
        prompt_7 = label(
            "第二式減第三式：已知總和能把差式壓縮嗎？",
            27,
            POINT,
            "BOLD",
        ).move_to(DOWN * 2.72)
        body_7 = VGroup(
            title_7,
            ribbon_7,
            left_memory_group,
            sum_model,
            row_72,
            row_73,
            prompt_7,
        )
        self.play(FadeOut(body), FadeIn(title_7), FadeIn(ribbon_7), run_time=0.7)
        self.play(FadeIn(left_memory_group), FadeIn(sum_model), run_time=0.8)
        self.play(FadeIn(row_72), FadeIn(row_73), run_time=0.75)
        self.play(FadeIn(prompt_7), run_time=0.5)
        self.wait(0.35)
        body = body_7

        # Beat 08 derive_x_one: use S=3 to cancel every y-term and isolate x.
        self.next_beat("derive_x_one")
        title_8 = label("右支：(2) - (3) 把 x 固定下來", 34, INK, "BOLD")
        title_8.move_to(UP * 3.02)
        branch_tag_8 = MathTex(r"S=x+y+z=3", font_size=28, color=REGION)
        branch_tag_8.move_to([5.55, 2.55, 0])
        left_heading_8 = label("左側", 24, MUTED, "BOLD").move_to([-3.65, 2.15, 0])
        right_heading_8 = label("右側", 24, MUTED, "BOLD").move_to([3.55, 2.15, 0])
        divider_8 = Line([0, 2.05, 0], [0, -0.15, 0], color=HAIRLINE, stroke_width=2)
        left_81 = self.colored_math(r"x^2+xz-y^2-yz", size=34).move_to([-3.65, 1.48, 0])
        left_82 = self.colored_math(
            r"=(x+y)(x-y)+z(x-y)", size=32
        ).move_to([-3.65, 0.78, 0])
        left_83 = self.colored_math(
            r"=(x+y+z)(x-y)=S(x-y)", size=32
        ).move_to([-3.65, 0.08, 0])
        right_81 = self.colored_math(
            r"3(x+z)-\frac52(y+z)-1", size=33
        ).move_to([3.55, 1.43, 0])
        right_82 = self.colored_math(
            r"=\frac52(x-y)+\frac12(x+z)-1", size=31
        ).move_to([3.55, 0.55, 0])
        substitutions_8 = self.colored_math(
            r"S=3,\qquad x+z=3-y", size=36
        ).move_to(DOWN * 0.52)
        equation_81 = self.colored_math(
            r"3(x-y)=\frac52(x-y)+\frac12(3-y)-1", size=36
        ).move_to(DOWN * 1.22)
        equation_82 = self.colored_math(
            r"6(x-y)=5(x-y)+(3-y)-2", size=37
        ).move_to(DOWN * 1.93)
        equation_83 = self.colored_math(
            r"6x-6y=5x-6y+1\quad\Longrightarrow\quad x=1", size=40
        ).move_to(DOWN * 2.70)
        result_frame_8 = SurroundingRectangle(
            equation_83, color=BLUE, buff=0.15, stroke_width=3
        )
        body_8 = VGroup(
            title_8,
            branch_tag_8,
            left_heading_8,
            right_heading_8,
            divider_8,
            left_81,
            left_82,
            left_83,
            right_81,
            right_82,
            substitutions_8,
            equation_81,
            equation_82,
            equation_83,
            result_frame_8,
        )
        self.play(FadeOut(body), FadeIn(title_8), FadeIn(branch_tag_8), run_time=0.7)
        self.play(FadeIn(left_heading_8), FadeIn(right_heading_8), Create(divider_8))
        self.play(Write(left_81), Write(right_81), run_time=0.75)
        self.play(Write(left_82), Write(right_82), run_time=0.8)
        self.play(Write(left_83), run_time=0.65)
        self.play(Write(substitutions_8), run_time=0.65)
        self.play(Write(equation_81), run_time=0.75)
        self.play(Write(equation_82), run_time=0.7)
        self.play(Write(equation_83), Create(result_frame_8), run_time=0.9)
        self.wait(0.35)
        body = body_8

        # Beat 09 solve_sum_branch: solve the remaining quadratic and pair y with z.
        self.next_beat("solve_sum_branch")
        title_9 = label("右支：x=1 後，只剩一個二次式", 34, INK, "BOLD")
        title_9.move_to(UP * 3.02)
        tag_9 = VGroup(
            MathTex(r"x=1", font_size=35, color=BLUE),
            MathTex(r"x+y+z=3", font_size=32, color=REGION),
        ).arrange(RIGHT, buff=0.75).move_to(UP * 2.22)
        substitution_91 = MathTex(
            r"1+y+y^2=3+3y", font_size=42, color=INK
        ).move_to(UP * 1.28)
        polynomial_9 = MathTex(r"y^2-2y-2=0", font_size=45, color=INK)
        polynomial_9.move_to(UP * 0.46)
        square_9 = MathTex(r"(y-1)^2=3", font_size=44, color=INK)
        square_9.move_to(DOWN * 0.33)
        roots_9 = MathTex(r"y=1\pm\sqrt3", font_size=49, color=POINT)
        roots_9.move_to(DOWN * 1.12)
        pair_left_9 = self.candidate_pair(
            r"y=1+\sqrt3", r"z=1-\sqrt3", center=(-3.10, -2.43, 0)
        )
        pair_right_9 = self.candidate_pair(
            r"y=1-\sqrt3", r"z=1+\sqrt3", center=(3.10, -2.43, 0)
        )
        left_pair_arrow = Arrow(
            roots_9.get_bottom() + LEFT * 0.35,
            pair_left_9[0].get_top(),
            color=REGION,
            buff=0.12,
            stroke_width=3,
        )
        right_pair_arrow = Arrow(
            roots_9.get_bottom() + RIGHT * 0.35,
            pair_right_9[0].get_top(),
            color=REGION,
            buff=0.12,
            stroke_width=3,
        )
        body_9 = VGroup(
            title_9,
            tag_9,
            substitution_91,
            polynomial_9,
            square_9,
            roots_9,
            pair_left_9,
            pair_right_9,
            left_pair_arrow,
            right_pair_arrow,
        )
        self.play(FadeOut(body), FadeIn(title_9), FadeIn(tag_9), run_time=0.7)
        self.play(Write(substitution_91), run_time=0.7)
        self.play(Write(polynomial_9), run_time=0.65)
        self.play(Write(square_9), run_time=0.6)
        self.play(Write(roots_9), run_time=0.7)
        self.play(
            GrowArrow(left_pair_arrow), GrowArrow(right_pair_arrow),
            FadeIn(pair_left_9), FadeIn(pair_right_9),
            run_time=0.9,
        )
        self.wait(0.35)
        body = body_9

        # Beat 10 verify_candidates: confirm that all four y-values reach the system.
        self.next_beat("verify_candidates")
        title_10 = label("必要候選還不夠：確認兩支都真的可達", 33, INK, "BOLD")
        title_10.move_to(UP * 3.02)
        divider_10 = Line([0, 2.40, 0], [0, -2.75, 0], color=HAIRLINE, stroke_width=2)
        left_heading_10 = label("左支｜z=y", 28, POINT, "BOLD").move_to([-3.75, 2.18, 0])
        left_values_10 = MathTex(
            r"y=\frac{5\pm\sqrt{37}}6", font_size=35, color=POINT
        ).move_to([-3.75, 1.47, 0])
        left_x_equation_10 = self.colored_math(
            r"x^2+(y-3)x+(y^2-3y)=0", size=31
        ).move_to([-3.75, 0.63, 0])
        left_delta_101 = self.colored_math(
            r"\Delta=(y-3)^2-4(y^2-3y)", size=30
        ).move_to([-3.75, -0.11, 0])
        left_delta_102 = self.colored_math(
            r"=-3y^2+6y+9=y+8", size=32
        ).move_to([-3.75, -0.79, 0])
        left_minimum_10 = MathTex(
            r"y_-\approx-0.180\quad\Longrightarrow\quad\Delta>0",
            font_size=31,
            color=INK,
        ).move_to([-3.75, -1.48, 0])
        left_badge_10 = label("兩個值都有實數 x", 24, POINT, "BOLD")
        left_badge_10.move_to([-3.75, -2.30, 0])
        left_badge_frame_10 = SurroundingRectangle(
            left_badge_10, color=POINT, buff=0.15, stroke_width=2.5
        )

        right_heading_10 = label("右支｜x=1", 28, REGION, "BOLD").move_to([3.75, 2.18, 0])
        right_invariants_10 = MathTex(
            r"y+z=2,\qquad yz=-2", font_size=35, color=INK
        ).move_to([3.75, 1.45, 0])
        right_root_rule_10 = MathTex(
            r"t^2-2t-2=0\quad(t=y,z)", font_size=31, color=INK
        ).move_to([3.75, 0.75, 0])
        right_check_1210 = MathTex(
            r"1+t+t^2=3(1+t)", font_size=32, color=INK
        ).move_to([3.75, 0.03, 0])
        right_check_12_note = label("第一、二式成立", 21, REGION, "BOLD")
        right_check_12_note.move_to([3.75, -0.43, 0])
        right_check_310 = MathTex(
            r"y^2+yz+z^2=(y+z)^2-yz=6", font_size=29, color=INK
        ).move_to([3.75, -1.05, 0])
        right_rhs_310 = MathTex(
            r"\frac52(y+z)+1=6", font_size=30, color=INK
        ).move_to([3.75, -1.60, 0])
        right_badge_10 = label("兩個配對都回到三條原式", 24, REGION, "BOLD")
        right_badge_10.move_to([3.75, -2.30, 0])
        right_badge_frame_10 = SurroundingRectangle(
            right_badge_10, color=REGION, buff=0.15, stroke_width=2.5
        )
        body_10 = VGroup(
            title_10,
            divider_10,
            left_heading_10,
            left_values_10,
            left_x_equation_10,
            left_delta_101,
            left_delta_102,
            left_minimum_10,
            left_badge_10,
            left_badge_frame_10,
            right_heading_10,
            right_invariants_10,
            right_root_rule_10,
            right_check_1210,
            right_check_12_note,
            right_check_310,
            right_rhs_310,
            right_badge_10,
            right_badge_frame_10,
        )
        self.play(FadeOut(body), FadeIn(title_10), Create(divider_10), run_time=0.7)
        self.play(FadeIn(left_heading_10), FadeIn(right_heading_10), run_time=0.5)
        self.play(Write(left_values_10), Write(right_invariants_10), run_time=0.7)
        self.play(Write(left_x_equation_10), Write(right_root_rule_10), run_time=0.75)
        self.play(Write(left_delta_101), Write(right_check_1210), run_time=0.75)
        self.play(
            Write(left_delta_102), FadeIn(right_check_12_note),
            Write(right_check_310), Write(right_rhs_310), run_time=0.9,
        )
        self.play(Write(left_minimum_10), run_time=0.6)
        self.play(
            FadeIn(left_badge_10), Create(left_badge_frame_10),
            FadeIn(right_badge_10), Create(right_badge_frame_10),
            run_time=0.75,
        )
        self.wait(0.35)
        body = body_10

        # Beat 11 correct_source_sign: reconcile the printed sign using the root sum.
        self.next_beat("correct_source_sign")
        title_11 = label("來源符號校正｜用根和快速核對", 34, INK, "BOLD")
        title_11.move_to(UP * 3.00)
        polynomial_11 = MathTex(r"3y^2-5y-1=0", font_size=47, color=INK)
        polynomial_11.move_to(UP * 2.05)
        source_note_11 = label(
            "來源答案欄的第一組分子排成 -5；同頁分支方程要求核對",
            25,
            MUTED,
            "MEDIUM",
        ).move_to(UP * 1.28)
        root_sum_11 = MathTex(
            r"y_1+y_2=-\frac BA=\frac53", font_size=43, color=POINT
        ).move_to(UP * 0.58)
        plus_check_11 = MathTex(
            r"\frac{5+\sqrt{37}}6+\frac{5-\sqrt{37}}6=\frac{10}{6}=\frac53",
            font_size=36,
            color=INK,
        ).move_to(DOWN * 0.75)
        plus_frame_11 = SurroundingRectangle(
            plus_check_11, color=REGION, buff=0.16, stroke_width=2.7
        )
        plus_note_11 = label("符合分支方程的根和", 22, REGION, "BOLD")
        plus_note_11.next_to(plus_frame_11, LEFT, buff=0.28)
        minus_check_11 = MathTex(
            r"\frac{-5+\sqrt{37}}6+\frac{-5-\sqrt{37}}6=-\frac53",
            font_size=36,
            color=MUTED,
        ).move_to(DOWN * 1.95)
        minus_frame_11 = SurroundingRectangle(
            minus_check_11, color=CORAL, buff=0.16, stroke_width=2.5
        )
        minus_note_11 = label("不符合這個分支方程", 22, CORAL, "BOLD")
        minus_note_11.next_to(minus_frame_11, LEFT, buff=0.28)
        resolution_11 = label(
            "因此依原式採用分子 +5，並保留這項校正紀錄",
            27,
            POINT,
            "BOLD",
        ).move_to(DOWN * 3.00)
        body_11 = VGroup(
            title_11,
            polynomial_11,
            source_note_11,
            root_sum_11,
            plus_check_11,
            plus_frame_11,
            plus_note_11,
            minus_check_11,
            minus_frame_11,
            minus_note_11,
            resolution_11,
        )
        self.play(FadeOut(body), FadeIn(title_11), Write(polynomial_11), run_time=0.75)
        self.play(FadeIn(source_note_11), run_time=0.55)
        self.play(Write(root_sum_11), run_time=0.75)
        self.play(
            Write(plus_check_11), Create(plus_frame_11), FadeIn(plus_note_11),
            run_time=0.9,
        )
        self.play(
            Write(minus_check_11), Create(minus_frame_11), FadeIn(minus_note_11),
            run_time=0.9,
        )
        self.play(FadeIn(resolution_11), run_time=0.6)
        self.wait(0.35)
        body = body_11

        # Beat 12 consolidate: reconnect each pair of answers to its own branch.
        self.next_beat("consolidate")
        title_12 = label("交換結構 → 零乘積 → 兩支完整答案", 34, INK, "BOLD")
        title_12.move_to(UP * 3.02)
        trunk_12 = MathTex(
            r"(y-z)(x+y+z-3)=0", font_size=43, color=INK
        ).move_to(UP * 2.03)
        trunk_frame_12 = SurroundingRectangle(
            trunk_12, color=WHITE, buff=0.16, stroke_width=2.5
        )
        left_card_12 = self.branch_card(
            r"y=z",
            r"y=\frac{5\pm\sqrt{37}}6",
            "左支：兩個可達值",
            POINT,
            center=(-3.35, 0.18, 0),
            width=5.85,
            height=1.95,
        )
        right_card_12 = self.branch_card(
            r"x+y+z=3",
            r"y=1\pm\sqrt3",
            "右支：兩個可達值",
            REGION,
            center=(3.35, 0.18, 0),
            width=5.85,
            height=1.95,
        )
        left_arrow_12 = Arrow(
            trunk_frame_12.get_bottom() + LEFT * 0.78,
            left_card_12[0].get_top(),
            color=POINT,
            buff=0.13,
            stroke_width=3.5,
        )
        right_arrow_12 = Arrow(
            trunk_frame_12.get_bottom() + RIGHT * 0.78,
            right_card_12[0].get_top(),
            color=REGION,
            buff=0.13,
            stroke_width=3.5,
        )
        final_left_12 = MathTex(
            r"y=\frac{5\pm\sqrt{37}}6", font_size=44, color=POINT
        )
        final_or_12 = label("或", 28, INK, "BOLD")
        final_right_12 = MathTex(r"y=1\pm\sqrt3", font_size=44, color=REGION)
        final_answer_12 = VGroup(final_left_12, final_or_12, final_right_12)
        final_answer_12.arrange(RIGHT, buff=0.58).move_to(DOWN * 2.34)
        final_frame_12 = SurroundingRectangle(
            final_answer_12, color=WHITE, buff=0.22, stroke_width=3
        )
        correction_12 = label(
            "註：第一組已依分支方程校正為 +5",
            18,
            MUTED,
            "MEDIUM",
        )
        correction_12.to_corner(DOWN + LEFT, buff=0.24)
        body_12 = VGroup(
            title_12,
            trunk_12,
            trunk_frame_12,
            left_card_12,
            right_card_12,
            left_arrow_12,
            right_arrow_12,
            final_answer_12,
            final_frame_12,
            correction_12,
        )
        self.play(FadeOut(body), FadeIn(title_12), Write(trunk_12), Create(trunk_frame_12))
        self.play(
            GrowArrow(left_arrow_12), GrowArrow(right_arrow_12),
            FadeIn(left_card_12), FadeIn(right_card_12),
            run_time=1.0,
        )
        self.play(Write(final_answer_12), Create(final_frame_12), run_time=0.9)
        self.play(FadeIn(correction_12), run_time=0.45)
        self.wait(0.45)
