"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q5."""

from __future__ import annotations

import math

from carlo_manim import (
    BG,
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
    Brace,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ALPHA = 3
BETA = 7
PARAMETER = 10
FACTOR_TARGET = 261


def f_value(x: int) -> int:
    return (x + 1) * (5 * x * x + 45)


def g_value(x: int) -> int:
    return (x + 1) * (5 * x - 6)


def q_value(x: int, parameter: int) -> int:
    return 5 * x * x - 5 * parameter * x + 6 * parameter + 45


POSITIVE_FACTOR_PAIRS = tuple(
    (divisor, FACTOR_TARGET // divisor)
    for divisor in range(1, math.isqrt(FACTOR_TARGET) + 1)
    if FACTOR_TARGET % divisor == 0
)
ADMISSIBLE_FACTOR_PAIRS = tuple(
    pair
    for pair in POSITIVE_FACTOR_PAIRS
    if pair[0] % 5 == 4 and pair[1] % 5 == 4
)
SIGNED_FACTOR_PAIRS = tuple(
    (sign * left, sign * right)
    for sign in (-1, 1)
    for left, right in POSITIVE_FACTOR_PAIRS
)
DECODED_POSITIVE_ROOT_PAIRS = tuple(
    ((left + 6) // 5, (right + 6) // 5)
    for left, right in SIGNED_FACTOR_PAIRS
    if (left + 6) % 5 == 0
    and (right + 6) % 5 == 0
    and (left + 6) // 5 > 0
    and (right + 6) // 5 > 0
    and (left + 6) // 5 != (right + 6) // 5
)

if POSITIVE_FACTOR_PAIRS != ((1, 261), (3, 87), (9, 29)):
    raise ValueError("the positive factor pairs of 261 changed unexpectedly")
if ADMISSIBLE_FACTOR_PAIRS != ((9, 29),):
    raise ValueError("the residue filter should leave exactly one factor pair")
if DECODED_POSITIVE_ROOT_PAIRS != ((ALPHA, BETA),):
    raise ValueError("signed factor pairs should decode to exactly one positive root pair")
if ((9 + 6) // 5, (29 + 6) // 5) != (ALPHA, BETA):
    raise ValueError("the surviving factor pair did not decode to 3 and 7")
if 5 * ALPHA * BETA != 6 * (ALPHA + BETA) + 45:
    raise ValueError("the independently reconstructed Diophantine equation failed")
if PARAMETER != ALPHA + BETA:
    raise ValueError("Vieta's root-sum relation failed")
if [x for x in range(1, 200) if q_value(x, PARAMETER) == 0] != [ALPHA, BETA]:
    raise ValueError("p=10 should have exactly the two positive integer roots 3 and 7")
if any(
    f_value(x) != PARAMETER * g_value(x)
    for x in (ALPHA, BETA)
):
    raise ValueError("the final values do not satisfy the original equations")
if (f_value(ALPHA), g_value(ALPHA), f_value(BETA), g_value(BETA)) != (
    360,
    36,
    2320,
    232,
):
    raise ValueError("the direct function-value check failed")


class CarloTcfs112MathQ05(CarloSlide):
    """Use two integer roots to turn a function condition into one factor pair."""

    lesson_id = "carlo.tcfs_112_math_gifted.q05"

    @staticmethod
    def transition_title(scene: "CarloTcfs112MathQ05", old, new) -> None:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.58)

    @staticmethod
    def token(tex: str, color: str, width: float = 1.48, height: float = 0.82) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            color=color,
            stroke_width=2.6,
            fill_color=BG,
            fill_opacity=0.97,
        )
        value = MathTex(tex, font_size=36, color=color).move_to(frame)
        return VGroup(frame, value)

    @classmethod
    def match_row(cls, symbol: str, color: str) -> VGroup:
        input_token = cls.token(symbol, color, width=1.22)
        left_machine = cls.token(rf"f({symbol})", BLUE, width=2.02)
        equality = MathTex("=", font_size=44, color=INK)
        right_machine = cls.token(rf"p\,g({symbol})", PURPLE, width=2.36)
        input_token.move_to([-5.35, 0, 0])
        left_machine.move_to([-2.75, 0, 0])
        equality.move_to([-0.55, 0, 0])
        right_machine.move_to([1.55, 0, 0])
        arrow = Arrow(
            input_token.get_right(),
            left_machine.get_left(),
            buff=0.16,
            color=MUTED,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )
        return VGroup(input_token, arrow, left_machine, equality, right_machine)

    @staticmethod
    def factor_pair_row(
        left_value: int,
        right_value: int,
        residues: str,
        color: str,
    ) -> VGroup:
        left_box = RoundedRectangle(
            width=1.42,
            height=0.76,
            corner_radius=0.05,
            color=color,
            stroke_width=2.5,
        )
        left_tex = MathTex(str(left_value), font_size=34, color=color).move_to(left_box)
        times = MathTex(r"\times", font_size=32, color=MUTED)
        right_box = RoundedRectangle(
            width=1.72,
            height=0.76,
            corner_radius=0.05,
            color=color,
            stroke_width=2.5,
        )
        right_tex = MathTex(str(right_value), font_size=34, color=color).move_to(right_box)
        equals = MathTex("=261", font_size=34, color=INK)
        pair = VGroup(VGroup(left_box, left_tex), times, VGroup(right_box, right_tex), equals)
        pair.arrange(RIGHT, buff=0.25)
        residue_note = MathTex(residues, font_size=27, color=color)
        return VGroup(pair, residue_note).arrange(DOWN, buff=0.16)

    def construct(self) -> None:
        heading = label("第 5 題｜兩個整數交點，如何鎖定 p", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 5 頁｜影片 dMXJ-FbZKxU 00:00-03:42.52",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 meet_two_integer_hits: make the shared-parameter condition tangible.
        self.begin_beat("meet_two_integer_hits")
        stage_title = label("同一個 p，要在兩個正整數輸入上同時平衡", 32, INK, "BOLD")
        stage_title.move_to([0, 3.03, 0])
        f_definition = MathTex(
            r"f(x)=(x+1)(5x^2+45)",
            font_size=37,
            color=BLUE,
        )
        g_definition = MathTex(
            r"g(x)=(x+1)(5x-6)",
            font_size=37,
            color=PURPLE,
        )
        definitions = VGroup(f_definition, g_definition).arrange(RIGHT, buff=1.00)
        definitions.move_to([0, 1.95, 0])
        alpha_row = self.match_row(r"\alpha", POINT).move_to([0, 0.42, 0])
        beta_row = self.match_row(r"\beta", REGION).move_to([0, -0.86, 0])
        shared_brace = Brace(
            VGroup(alpha_row[-1], beta_row[-1]),
            RIGHT,
            color=PURPLE,
            buff=0.18,
        )
        shared_note = label("同一個 p", 25, PURPLE, "BOLD")
        shared_note.next_to(shared_brace, RIGHT, buff=0.18)
        positive_note = label("α、β 是兩個不同的正整數", 26, MUTED, "MEDIUM")
        question = label("所有可能的 p，加起來是多少？", 31, CORAL, "BOLD")
        bottom_prompt = VGroup(positive_note, question).arrange(DOWN, buff=0.28)
        bottom_prompt.move_to([0, -2.56, 0])

        self.add(heading, source)
        self.play(FadeIn(stage_title), run_time=0.52)
        self.play(FadeIn(definitions), run_time=0.62)
        self.play(Create(alpha_row[1]), GrowFromCenter(alpha_row[0]), FadeIn(alpha_row[2:]), run_time=0.75)
        self.play(Create(beta_row[1]), GrowFromCenter(beta_row[0]), FadeIn(beta_row[2:]), run_time=0.75)
        self.play(Create(shared_brace), FadeIn(shared_note), run_time=0.55)
        self.play(FadeIn(bottom_prompt), run_time=0.58)
        self.wait(0.42)

        # Beat 02 turn_matches_into_zeros: one difference records both balances.
        self.next_beat("turn_matches_into_zeros")
        next_title = label("兩次相等，可以看成同一個差值的兩個零點", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        difference = MathTex(r"H_p(x)=f(x)-p\,g(x)", font_size=52, color=BLUE)
        difference.move_to([0, 1.66, 0])
        alpha_zero = MathTex(
            r"f(\alpha)=p\,g(\alpha)",
            r"\Longrightarrow",
            r"H_p(\alpha)=0",
            font_size=39,
            color=INK,
        )
        alpha_zero[2].set_color(POINT)
        beta_zero = MathTex(
            r"f(\beta)=p\,g(\beta)",
            r"\Longrightarrow",
            r"H_p(\beta)=0",
            font_size=39,
            color=INK,
        )
        beta_zero[2].set_color(REGION)
        zero_rows = VGroup(alpha_zero, beta_zero).arrange(DOWN, buff=0.38)
        zero_rows.move_to([0, 0.20, 0])
        root_line = Line([-4.0, -1.55, 0], [4.0, -1.55, 0], color=MUTED, stroke_width=3)
        alpha_dot = Dot([-2.10, -1.55, 0], radius=0.12, color=POINT)
        beta_dot = Dot([2.10, -1.55, 0], radius=0.12, color=REGION)
        alpha_tag = MathTex(r"\alpha", font_size=34, color=POINT).next_to(alpha_dot, DOWN, buff=0.16)
        beta_tag = MathTex(r"\beta", font_size=34, color=REGION).next_to(beta_dot, DOWN, buff=0.16)
        root_note = label("我們要找的是：同一個式子的兩個正整數零點", 27, MUTED, "MEDIUM")
        root_note.move_to([0, -2.50, 0])
        zero_picture = VGroup(root_line, alpha_dot, beta_dot, alpha_tag, beta_tag, root_note)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(definitions),
            FadeOut(alpha_row),
            FadeOut(beta_row),
            FadeOut(shared_brace),
            FadeOut(shared_note),
            FadeOut(bottom_prompt),
            run_time=0.50,
        )
        self.play(Write(difference), run_time=0.58)
        self.play(Write(alpha_zero), run_time=0.68)
        self.play(Write(beta_zero), run_time=0.68)
        self.play(Create(root_line), GrowFromCenter(alpha_dot), GrowFromCenter(beta_dot), run_time=0.62)
        self.play(FadeIn(alpha_tag), FadeIn(beta_tag), FadeIn(root_note), run_time=0.50)
        self.wait(0.42)

        # Beat 03 discard_common_root: factor first, then enforce the domain.
        self.next_beat("discard_common_root")
        next_title = label("先提出共同因子，再把不合題意的零點排除", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        factorization = MathTex(
            r"H_p(x)",
            r"=(x+1)",
            r"\bigl[5x^2+45-p(5x-6)\bigr]",
            font_size=41,
            color=INK,
        )
        factorization[1].set_color(CORAL)
        factorization[2].set_color(BLUE)
        factorization.move_to([0, 1.80, 0])
        number_line = NumberLine(
            x_range=[-2, 6, 1],
            length=6.40,
            include_numbers=True,
            font_size=23,
            color=MUTED,
            include_tip=True,
        ).move_to([-3.35, -0.35, 0])
        positive_segment = Line(
            number_line.n2p(1),
            number_line.n2p(6),
            color=REGION,
            stroke_width=8,
        ).set_z_index(-1)
        minus_one = Dot(number_line.n2p(-1), radius=0.14, color=CORAL)
        invalid_cross = VGroup(
            Line(minus_one.get_center() + [-0.18, -0.18, 0], minus_one.get_center() + [0.18, 0.18, 0], color=CORAL, stroke_width=4),
            Line(minus_one.get_center() + [-0.18, 0.18, 0], minus_one.get_center() + [0.18, -0.18, 0], color=CORAL, stroke_width=4),
        )
        domain_label = label("題目只允許正整數", 25, REGION, "BOLD")
        domain_label.next_to(number_line, DOWN, buff=0.34)
        rejected = VGroup(
            MathTex(r"x+1=0", font_size=41, color=CORAL),
            MathTex(r"x=-1", font_size=43, color=CORAL),
            label("不在正整數範圍內", 27, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.32)
        rejected.move_to([3.85, -0.15, 0])
        surviving_quadratic = MathTex(
            r"Q_p(x)=5x^2-5px+(6p+45)=0",
            font_size=39,
            color=BLUE,
        )
        surviving_quadratic.move_to([0, -2.45, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(difference), FadeOut(zero_rows), FadeOut(zero_picture), run_time=0.48)
        self.play(Write(factorization), run_time=0.82)
        self.play(Create(number_line), Create(positive_segment), FadeIn(domain_label), run_time=0.68)
        self.play(GrowFromCenter(minus_one), Write(rejected[0]), run_time=0.52)
        self.play(Write(rejected[1]), Create(invalid_cross), FadeIn(rejected[2]), run_time=0.60)
        self.play(Write(surviving_quadratic), run_time=0.70)
        self.wait(0.42)

        # Beat 04 see_remaining_quadratic: turn the algebra back into two roots.
        self.next_beat("see_remaining_quadratic")
        next_title = label("剩下的二次式，必須剛好穿過 α 與 β", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[-5, 8, 2],
            x_length=6.15,
            y_length=4.05,
            axis_config={"color": MUTED, "stroke_width": 2.5, "include_ticks": False},
            tips=False,
        ).move_to([-3.40, -0.40, 0])
        curve = axes.plot(
            lambda x: 0.45 * (x - 2) * (x - 6),
            x_range=[0.25, 7.75],
            color=BLUE,
            stroke_width=4,
        )
        alpha_root = Dot(axes.c2p(2, 0), radius=0.13, color=POINT)
        beta_root = Dot(axes.c2p(6, 0), radius=0.13, color=REGION)
        alpha_root_label = MathTex(r"\alpha", font_size=35, color=POINT).next_to(alpha_root, DOWN, buff=0.17)
        beta_root_label = MathTex(r"\beta", font_size=35, color=REGION).next_to(beta_root, DOWN, buff=0.17)
        plot_note = label("兩個正整數零點", 25, MUTED, "MEDIUM")
        plot_note.move_to([-3.40, -2.67, 0])
        plot_group = VGroup(axes, curve, alpha_root, beta_root, alpha_root_label, beta_root_label, plot_note)
        quadratic_panel = VGroup(
            MathTex(r"Q_p(x)=5x^2-5px+(6p+45)", font_size=38, color=BLUE),
            MathTex(r"Q_p(x)=5(x-\alpha)(x-\beta)", font_size=42, color=INK),
            MathTex(r"\alpha,\beta\in\mathbb{Z}_{>0},\quad\alpha<\beta", font_size=34, color=MUTED),
            label("同一個二次式的兩種讀法", 27, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.48)
        quadratic_panel.move_to([3.55, -0.32, 0])
        divider = Line([0.25, -3.40, 0], [0.25, 2.48, 0], color=HAIRLINE, stroke_width=1.5)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(factorization),
            FadeOut(number_line),
            FadeOut(positive_segment),
            FadeOut(minus_one),
            FadeOut(invalid_cross),
            FadeOut(domain_label),
            FadeOut(rejected),
            FadeOut(surviving_quadratic),
            Create(divider),
            run_time=0.55,
        )
        self.play(Create(axes), Create(curve), run_time=1.00)
        self.play(GrowFromCenter(alpha_root), GrowFromCenter(beta_root), run_time=0.48)
        self.play(FadeIn(alpha_root_label), FadeIn(beta_root_label), FadeIn(plot_note), run_time=0.48)
        self.play(Write(quadratic_panel[0]), run_time=0.62)
        self.play(Write(quadratic_panel[1]), run_time=0.66)
        self.play(FadeIn(quadratic_panel[2]), FadeIn(quadratic_panel[3]), run_time=0.54)
        self.wait(0.42)

        # Beat 05 read_sum_and_product: attach Vieta relations to visible objects.
        self.next_beat("read_sum_and_product")
        next_title = label("根的和與積，把 α、β 和 p 接在一起", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        alpha_block = Rectangle(
            width=2.00,
            height=0.92,
            color=POINT,
            stroke_width=2.8,
            fill_color=POINT,
            fill_opacity=0.12,
        )
        alpha_block_label = MathTex(r"\alpha", font_size=38, color=POINT).move_to(alpha_block)
        beta_block = Rectangle(
            width=3.00,
            height=0.92,
            color=REGION,
            stroke_width=2.8,
            fill_color=REGION,
            fill_opacity=0.12,
        )
        beta_block_label = MathTex(r"\beta", font_size=38, color=REGION).move_to(beta_block)
        sum_bar = VGroup(
            VGroup(alpha_block, alpha_block_label),
            VGroup(beta_block, beta_block_label),
        ).arrange(RIGHT, buff=0)
        sum_brace = Brace(sum_bar, DOWN, color=BLUE, buff=0.16)
        sum_name = MathTex(r"\alpha+\beta", font_size=36, color=BLUE).next_to(sum_brace, DOWN, buff=0.14)
        sum_visual = VGroup(sum_bar, sum_brace, sum_name).move_to([-3.40, 0.98, 0])
        product_rectangle = Rectangle(
            width=4.20,
            height=1.70,
            color=PURPLE,
            stroke_width=2.8,
            fill_color=PURPLE,
            fill_opacity=0.10,
        ).move_to([-3.40, -1.35, 0])
        product_area = MathTex(r"\alpha\beta", font_size=43, color=PURPLE).move_to(product_rectangle)
        product_alpha = MathTex(r"\alpha", font_size=31, color=POINT).next_to(product_rectangle, LEFT, buff=0.20)
        product_beta = MathTex(r"\beta", font_size=31, color=REGION).next_to(product_rectangle, DOWN, buff=0.16)
        product_visual = VGroup(product_rectangle, product_area, product_alpha, product_beta)
        coefficient_panel = VGroup(
            MathTex(r"5(x-\alpha)(x-\beta)", font_size=38, color=INK),
            MathTex(r"=5x^2-5(\alpha+\beta)x+5\alpha\beta", font_size=36, color=INK),
            MathTex(r"\alpha+\beta=p", font_size=47, color=BLUE),
            MathTex(r"\alpha\beta=\frac{6p+45}{5}", font_size=44, color=PURPLE),
        ).arrange(DOWN, buff=0.48)
        coefficient_panel.move_to([3.62, -0.32, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(plot_group), FadeOut(quadratic_panel), run_time=0.45)
        self.play(FadeIn(sum_bar), Create(sum_brace), FadeIn(sum_name), run_time=0.65)
        self.play(Create(product_rectangle), FadeIn(product_area), FadeIn(product_alpha), FadeIn(product_beta), run_time=0.68)
        self.play(Write(coefficient_panel[0]), run_time=0.54)
        self.play(Write(coefficient_panel[1]), run_time=0.74)
        self.play(FadeIn(coefficient_panel[2]), Indicate(sum_visual, color=BLUE), run_time=0.62)
        self.play(FadeIn(coefficient_panel[3]), Indicate(product_visual, color=PURPLE), run_time=0.62)
        self.wait(0.42)

        # Beat 06 remove_parameter_p: substitute the visible sum for p.
        self.next_beat("remove_parameter_p")
        next_title = label("用 p=α+β，把參數從乘積式中移走", 32, INK, "BOLD")
        next_title.move_to(stage_title)
        p_token = self.token("p", BLUE, width=1.32)
        replacement_token = self.token(r"\alpha+\beta", POINT, width=2.36)
        replacement_arrow = Arrow(
            p_token.get_right(),
            replacement_token.get_left(),
            buff=0.20,
            color=MUTED,
            stroke_width=3.2,
            max_tip_length_to_length_ratio=0.18,
        )
        substitution_visual = VGroup(p_token, replacement_arrow, replacement_token).arrange(RIGHT, buff=0.30)
        substitution_visual.move_to([0, 1.55, 0])
        eliminate_steps = VGroup(
            MathTex(r"5\alpha\beta=6p+45", font_size=47, color=INK),
            MathTex(r"5\alpha\beta=6(\alpha+\beta)+45", font_size=47, color=INK),
            MathTex(r"5\alpha\beta-6\alpha-6\beta=45", font_size=49, color=REGION),
        ).arrange(DOWN, buff=0.56)
        eliminate_steps.move_to([0, -0.74, 0])
        elimination_note = label("現在只剩兩個正整數 α、β", 28, POINT, "BOLD")
        elimination_note.move_to([0, -2.55, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(sum_visual),
            FadeOut(product_visual),
            FadeOut(coefficient_panel),
            FadeOut(divider),
            run_time=0.48,
        )
        self.play(GrowFromCenter(p_token), Create(replacement_arrow), GrowFromCenter(replacement_token), run_time=0.68)
        self.play(Write(eliminate_steps[0]), run_time=0.58)
        self.play(Write(eliminate_steps[1]), Indicate(replacement_token, color=POINT), run_time=0.72)
        self.play(Write(eliminate_steps[2]), run_time=0.72)
        self.play(FadeIn(elimination_note), run_time=0.45)
        self.wait(0.42)

        # Beat 07 complete_factor_rectangle: make the +36 factorization visible.
        self.next_beat("complete_factor_rectangle")
        next_title = label("補回重複扣掉的 36，剩餘長方形面積是 261", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        big_rect = Rectangle(
            width=5.45,
            height=3.45,
            color=BLUE,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.08,
        ).move_to([-3.42, -0.45, 0])
        vertical_strip = Rectangle(
            width=0.92,
            height=3.45,
            color=CORAL,
            stroke_width=2.4,
            fill_color=CORAL,
            fill_opacity=0.20,
        ).align_to(big_rect, RIGHT).align_to(big_rect, DOWN)
        horizontal_strip = Rectangle(
            width=5.45,
            height=0.70,
            color=PURPLE,
            stroke_width=2.4,
            fill_color=PURPLE,
            fill_opacity=0.18,
        ).align_to(big_rect, UP).align_to(big_rect, LEFT)
        corner = Rectangle(
            width=0.92,
            height=0.70,
            color=POINT,
            stroke_width=2.4,
            fill_color=POINT,
            fill_opacity=0.38,
        ).align_to(big_rect, UP).align_to(big_rect, RIGHT)
        remainder_rect = Rectangle(
            width=4.53,
            height=2.75,
            color=REGION,
            stroke_width=3.2,
            fill_color=REGION,
            fill_opacity=0.08,
        ).align_to(big_rect, LEFT).align_to(big_rect, DOWN)
        full_width = MathTex(r"5\alpha", font_size=31, color=BLUE).next_to(big_rect, DOWN, buff=0.18)
        full_height = MathTex(r"5\beta", font_size=31, color=BLUE).rotate(math.pi / 2)
        full_height.next_to(big_rect, LEFT, buff=0.18)
        strip_width = MathTex("6", font_size=28, color=CORAL).move_to(vertical_strip)
        strip_height = MathTex("6", font_size=28, color=PURPLE).move_to(horizontal_strip)
        remaining_area = MathTex(
            r"(5\alpha-6)(5\beta-6)",
            font_size=32,
            color=REGION,
        ).move_to(remainder_rect)
        corner_area = MathTex("36", font_size=25, color=POINT).move_to(corner)
        area_picture = VGroup(
            big_rect,
            vertical_strip,
            horizontal_strip,
            corner,
            remainder_rect,
            full_width,
            full_height,
            strip_width,
            strip_height,
            remaining_area,
            corner_area,
        )
        factor_steps = VGroup(
            MathTex(r"25\alpha\beta-30\alpha-30\beta=225", font_size=36, color=INK),
            MathTex(r"25\alpha\beta-30\alpha-30\beta+36=261", font_size=34, color=INK),
            MathTex(r"(5\alpha-6)(5\beta-6)=261", font_size=43, color=REGION),
            label("兩邊加 36，不改變等式", 27, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.52)
        factor_steps.move_to([3.55, -0.35, 0])
        divider = Line([0.15, -3.40, 0], [0.15, 2.42, 0], color=HAIRLINE, stroke_width=1.5)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(substitution_visual), FadeOut(eliminate_steps), FadeOut(elimination_note), Create(divider), run_time=0.52)
        self.play(Create(big_rect), FadeIn(full_width), FadeIn(full_height), run_time=0.62)
        self.play(FadeIn(vertical_strip), FadeIn(strip_width), run_time=0.50)
        self.play(FadeIn(horizontal_strip), FadeIn(strip_height), run_time=0.50)
        self.play(FadeIn(corner), FadeIn(corner_area), run_time=0.48)
        self.play(Create(remainder_rect), FadeIn(remaining_area), run_time=0.58)
        self.play(Write(factor_steps[0]), run_time=0.66)
        self.play(Write(factor_steps[1]), FadeIn(factor_steps[3]), run_time=0.72)
        self.play(Write(factor_steps[2]), Indicate(remainder_rect, color=REGION), run_time=0.72)
        self.wait(0.42)

        # Beat 08 filter_factor_pairs: close the sign edge case, then exhaust divisors.
        self.next_beat("filter_factor_pairs")
        next_title = label("先排除負因數，再篩選 261 的三組正因數對", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        sign_floor = MathTex(
            r"5\alpha-6,\ 5\beta-6\ge -1",
            font_size=32,
            color=POINT,
        )
        sign_product = MathTex(
            r"(5\alpha-6)(5\beta-6)=261>1",
            font_size=32,
            color=BLUE,
        )
        sign_arrow = MathTex(r"\Longrightarrow", font_size=31, color=MUTED)
        sign_conclusion = label("兩因數皆為正", 25, REGION, "BOLD")
        sign_gate = VGroup(
            sign_floor,
            sign_product,
            sign_arrow,
            sign_conclusion,
        ).arrange(RIGHT, buff=0.40)
        sign_gate.move_to([0, 2.25, 0])
        prime_factorization = MathTex(r"261=3^2\cdot29", font_size=42, color=BLUE)
        prime_factorization.move_to([-3.85, 1.52, 0])
        residue_gate = VGroup(
            MathTex(r"5n-6\equiv4\pmod5", font_size=35, color=REGION),
            label("左右因數都必須餘 4", 24, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.12)
        residue_gate.move_to([2.35, 1.52, 0])
        gate_header = VGroup(sign_gate, prime_factorization, residue_gate)
        first_pair = self.factor_pair_row(1, 261, r"1,1\pmod5", CORAL)
        second_pair = self.factor_pair_row(3, 87, r"3,2\pmod5", CORAL)
        third_pair = self.factor_pair_row(9, 29, r"4,4\pmod5", REGION)
        pair_rows = VGroup(first_pair, second_pair, third_pair).arrange(DOWN, buff=0.38)
        pair_rows.move_to([-0.55, -0.98, 0])
        rejected_one = label("不合", 27, CORAL, "BOLD").next_to(first_pair, RIGHT, buff=0.42)
        rejected_two = label("不合", 27, CORAL, "BOLD").next_to(second_pair, RIGHT, buff=0.42)
        accepted = label("唯一通過", 28, REGION, "BOLD").next_to(third_pair, RIGHT, buff=0.42)
        accepted_box = SurroundingRectangle(third_pair, color=REGION, buff=0.18, stroke_width=3.2)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(area_picture), FadeOut(factor_steps), FadeOut(divider), run_time=0.48)
        self.play(FadeIn(sign_floor), FadeIn(sign_product), run_time=0.52)
        self.play(FadeIn(sign_arrow), FadeIn(sign_conclusion), run_time=0.42)
        self.play(Write(prime_factorization), FadeIn(residue_gate), run_time=0.68)
        self.play(FadeIn(first_pair), run_time=0.48)
        self.play(FadeIn(rejected_one), run_time=0.35)
        self.play(FadeIn(second_pair), run_time=0.48)
        self.play(FadeIn(rejected_two), run_time=0.35)
        self.play(FadeIn(third_pair), run_time=0.48)
        self.play(Create(accepted_box), FadeIn(accepted), run_time=0.60)
        self.wait(0.48)

        # Beat 09 decode_surviving_pair: settle every value except the final sum.
        self.next_beat("decode_surviving_pair")
        next_title = label("把唯一因數對解碼回 α、β，先停在最後一加", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        surviving_pair = VGroup(
            self.token("9", REGION, width=1.35),
            MathTex(r"\times", font_size=34, color=MUTED),
            self.token("29", REGION, width=1.55),
            MathTex("=261", font_size=36, color=INK),
        ).arrange(RIGHT, buff=0.25)
        surviving_pair.move_to([0, 1.65, 0])
        alpha_decode = MathTex(
            r"5\alpha-6=9",
            r"\Longrightarrow",
            r"\alpha=3",
            font_size=43,
            color=INK,
        )
        alpha_decode[2].set_color(POINT)
        beta_decode = MathTex(
            r"5\beta-6=29",
            r"\Longrightarrow",
            r"\beta=7",
            font_size=43,
            color=INK,
        )
        beta_decode[2].set_color(REGION)
        decode_rows = VGroup(alpha_decode, beta_decode).arrange(DOWN, buff=0.46)
        decode_rows.move_to([0, 0.18, 0])
        preanswer = VGroup(
            MathTex(r"p=\alpha+\beta", font_size=44, color=BLUE),
            MathTex(r"p=3+7", font_size=58, color=POINT),
            label("只剩最後這一步", 29, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.35)
        preanswer.move_to([0, -1.92, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(gate_header),
            FadeOut(pair_rows),
            FadeOut(rejected_one),
            FadeOut(rejected_two),
            FadeOut(accepted),
            FadeOut(accepted_box),
            run_time=0.48,
        )
        self.play(FadeIn(surviving_pair), run_time=0.52)
        self.play(Write(alpha_decode), run_time=0.68)
        self.play(Write(beta_decode), run_time=0.68)
        self.play(FadeIn(preanswer[0]), run_time=0.42)
        self.play(Write(preanswer[1]), run_time=0.55)
        self.play(FadeIn(preanswer[2]), run_time=0.42)
        self.wait(0.72)

        # Beat 10 reveal_parameter: calculate only after the settled pre-answer pause.
        self.next_beat("reveal_parameter")
        next_title = label("唯一可能的參數是 10，回到原式核對兩個輸入", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        answer = MathTex("p=10", font_size=77, color=POINT)
        answer_box = SurroundingRectangle(answer, color=POINT, buff=0.28, stroke_width=3.5)
        answer_group = VGroup(answer_box, answer).move_to([-3.65, 1.18, 0])
        exact_factorization = MathTex(
            r"H_{10}(x)=5(x+1)(x-3)(x-7)",
            font_size=38,
            color=BLUE,
        ).move_to([-3.65, -0.15, 0])
        root_check = label("正整數零點恰為 3、7", 28, REGION, "BOLD")
        root_check.move_to([-3.65, -0.83, 0])
        direct_checks = VGroup(
            MathTex(r"f(3)=360=10\,g(3)", font_size=38, color=INK),
            MathTex(r"f(7)=2320=10\,g(7)", font_size=38, color=INK),
            label("兩個原始等式都成立", 27, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.48)
        direct_checks.move_to([3.60, 0.22, 0])
        final_answer = label("所有可能 p 的總和：10", 42, POINT, "BOLD")
        final_answer.move_to([0, -2.26, 0])
        final_answer_box = SurroundingRectangle(final_answer, color=POINT, buff=0.25, stroke_width=3.2)
        final_divider = Line([0, -1.44, 0], [0, 2.28, 0], color=HAIRLINE, stroke_width=1.5)

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(surviving_pair), FadeOut(decode_rows), FadeOut(preanswer), run_time=0.42)
        self.play(GrowFromCenter(answer), Create(answer_box), Create(final_divider), run_time=0.70)
        self.play(Write(exact_factorization), FadeIn(root_check), run_time=0.70)
        self.play(Write(direct_checks[0]), run_time=0.58)
        self.play(Write(direct_checks[1]), run_time=0.58)
        self.play(FadeIn(direct_checks[2]), run_time=0.40)
        self.play(FadeIn(final_answer), Create(final_answer_box), run_time=0.70)
        self.wait(0.48)
