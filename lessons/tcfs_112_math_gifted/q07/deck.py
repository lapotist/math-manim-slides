"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q7."""

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
    Brace,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


DIGIT_INCREMENT = 5
FACTOR_TARGET = 555


def add_five_to_decimal_digits(value: int) -> int | None:
    """Apply the problem's no-carry, one-card-per-digit operation."""
    digits = str(value)
    if len(digits) != 3 or any(int(digit) > 4 for digit in digits):
        return None
    return int("".join(str(int(digit) + DIGIT_INCREMENT) for digit in digits))


ADMISSIBLE_DIGIT_CASES = tuple(
    (a, a * a, transformed)
    for a in range(10, 100)
    if (transformed := add_five_to_decimal_digits(a * a)) is not None
)
DIRECT_SOLUTIONS = tuple(
    (a, transformed)
    for a, _, transformed in ADMISSIBLE_DIGIT_CASES
    if math.isqrt(transformed) ** 2 == transformed
)
POSITIVE_FACTOR_PAIRS = tuple(
    (divisor, FACTOR_TARGET // divisor)
    for divisor in range(1, math.isqrt(FACTOR_TARGET) + 1)
    if FACTOR_TARGET % divisor == 0
)
FACTOR_CANDIDATES = tuple(
    (
        x,
        y,
        (y - x) // 2,
        (x + y) // 2,
        ((x + y) // 2) ** 2,
    )
    for x, y in POSITIVE_FACTOR_PAIRS
    if x % 2 == y % 2
)

if ADMISSIBLE_DIGIT_CASES != (
    (10, 100, 655),
    (11, 121, 676),
    (12, 144, 699),
    (18, 324, 879),
    (20, 400, 955),
    (21, 441, 996),
):
    raise ValueError("the exhaustive legal digit transformations changed")
if DIRECT_SOLUTIONS != ((11, 676),):
    raise ValueError("the direct digit search must have the unique solution (11, 676)")
if POSITIVE_FACTOR_PAIRS != ((1, 555), (3, 185), (5, 111), (15, 37)):
    raise ValueError("the positive factor pairs of 555 are incomplete")
if not all(x % 2 == 1 and y % 2 == 1 for x, y in POSITIVE_FACTOR_PAIRS):
    raise ValueError("every factor pair of odd 555 must be odd-odd")
if FACTOR_CANDIDATES != (
    (1, 555, 277, 278, 77284),
    (3, 185, 91, 94, 8836),
    (5, 111, 53, 58, 3364),
    (15, 37, 11, 26, 676),
):
    raise ValueError("factor-pair decoding changed unexpectedly")
if tuple(
    (a, m)
    for _, _, a, m, _ in FACTOR_CANDIDATES
    if 10 <= a <= 99 and 10 <= m <= 31
) != ((11, 26),):
    raise ValueError("the decimal-length gates must leave exactly (a, m)=(11, 26)")
if 11**2 != 121 or add_five_to_decimal_digits(121) != 676 or 26**2 != 676:
    raise ValueError("the surviving candidate fails the original digit operation")


class CarloTcfs112MathQ07(CarloSlide):
    """Turn a digitwise shift into a complete difference-of-squares search."""

    lesson_id = "carlo.tcfs_112_math_gifted.q07"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def digit_card(
        value: str,
        color: str,
        *,
        width: float = 1.18,
        height: float = 1.28,
        font_size: float = 48,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.07,
            color=color,
            stroke_width=2.8,
            fill_color=color,
            fill_opacity=0.12,
        )
        value_tex = MathTex(value, font_size=font_size, color=color).move_to(frame)
        return VGroup(frame, value_tex)

    @classmethod
    def digit_row(
        cls,
        values: tuple[str, str, str],
        color: str,
        *,
        width: float = 1.18,
        font_size: float = 48,
    ) -> VGroup:
        row = VGroup(
            *(
                cls.digit_card(value, color, width=width, font_size=font_size)
                for value in values
            )
        )
        row.arrange(RIGHT, buff=0.17)
        return row

    @staticmethod
    def factor_token(expression: str, color: str) -> VGroup:
        frame = RoundedRectangle(
            width=3.15,
            height=1.05,
            corner_radius=0.07,
            color=color,
            stroke_width=2.7,
            fill_color=color,
            fill_opacity=0.11,
        )
        value = MathTex(expression, font_size=39, color=color).move_to(frame)
        return VGroup(frame, value)

    @staticmethod
    def factor_row(x: int, y: int, y_position: float) -> VGroup:
        frame = RoundedRectangle(
            width=11.35,
            height=0.68,
            corner_radius=0.04,
            color=HAIRLINE,
            stroke_width=1.6,
            fill_color=BG,
            fill_opacity=0.96,
        ).move_to([0, y_position, 0])
        x_tex = MathTex(str(x), font_size=31, color=CORAL).move_to([-4.30, y_position, 0])
        y_tex = MathTex(str(y), font_size=31, color=PURPLE).move_to([-2.25, y_position, 0])
        product = MathTex(
            rf"{x}\cdot {y}=555",
            font_size=30,
            color=INK,
        ).move_to([0.55, y_position, 0])
        parity = label("奇、奇｜通過", 21, REGION, "BOLD").move_to([4.00, y_position, 0])
        return VGroup(frame, x_tex, y_tex, product, parity)

    @staticmethod
    def candidate_row(
        x: int,
        y: int,
        a: int,
        m: int,
        y_position: float,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=10.55,
            height=0.68,
            corner_radius=0.04,
            color=HAIRLINE,
            stroke_width=1.6,
            fill_color=BG,
            fill_opacity=0.96,
        ).move_to([0, y_position, 0])
        values = VGroup(
            MathTex(str(x), font_size=31, color=CORAL).move_to([-3.75, y_position, 0]),
            MathTex(str(y), font_size=31, color=PURPLE).move_to([-1.45, y_position, 0]),
            MathTex(str(a), font_size=31, color=BLUE).move_to([1.25, y_position, 0]),
            MathTex(str(m), font_size=31, color=POINT).move_to([3.75, y_position, 0]),
        )
        return VGroup(frame, values)

    @staticmethod
    def gate_row(
        a: int,
        m: int,
        a_status: str,
        m_status: str,
        verdict: str,
        y_position: float,
        *,
        survives: bool = False,
    ) -> VGroup:
        frame_color = POINT if survives else HAIRLINE
        frame = RoundedRectangle(
            width=12.0,
            height=0.72,
            corner_radius=0.04,
            color=frame_color,
            stroke_width=2.3 if survives else 1.5,
            fill_color=POINT if survives else BG,
            fill_opacity=0.08 if survives else 0.96,
        ).move_to([0, y_position, 0])
        pair = MathTex(rf"({a},{m})", font_size=31, color=INK).move_to(
            [-4.55, y_position, 0]
        )
        a_color = REGION if a_status == "通過" else CORAL
        m_color = REGION if m_status == "通過" else CORAL if m_status == "淘汰" else MUTED
        a_test = label(a_status, 22, a_color, "BOLD").move_to([-1.55, y_position, 0])
        m_test = label(m_status, 22, m_color, "BOLD").move_to([1.45, y_position, 0])
        verdict_text = label(
            verdict,
            21,
            POINT if survives else CORAL,
            "BOLD" if survives else "MEDIUM",
        ).move_to([4.35, y_position, 0])
        return VGroup(frame, pair, a_test, m_test, verdict_text)

    @staticmethod
    def blank_digit_frames(color: str) -> VGroup:
        frames = VGroup(
            *(
                RoundedRectangle(
                    width=1.08,
                    height=1.18,
                    corner_radius=0.07,
                    color=color,
                    stroke_width=2.6,
                    fill_color=color,
                    fill_opacity=0.08,
                )
                for _ in range(3)
            )
        )
        frames.arrange(RIGHT, buff=0.16)
        return frames

    def construct(self) -> None:
        heading = label("第 7 題｜每位加五，平方數藏在哪裡", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 7 頁｜影片 RJcla7jv85g 00:00-02:59.10",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: make the digit operation tangible before introducing 555.
        self.begin_beat("touch_each_digit")
        title = label("先看「每位數字加 5」真的改了哪裡", 32, INK, "BOLD")
        title.move_to([0, 3.08, 0])
        example_note = label("先只看一個三位數例子", 23, MUTED, "MEDIUM")
        example_note.move_to([0, 2.30, 0])
        input_row = self.digit_row(("2", "0", "4"), BLUE).move_to([0, 1.05, 0])
        place_names = VGroup(
            label("百位", 18, MUTED, "MEDIUM"),
            label("十位", 18, MUTED, "MEDIUM"),
            label("個位", 18, MUTED, "MEDIUM"),
        )
        for place_name, card in zip(place_names, input_row, strict=True):
            place_name.next_to(card, UP, buff=0.12)
        output_row = self.digit_row(("7", "5", "9"), POINT).move_to([0, -1.45, 0])
        arrows = VGroup(
            *(
                Arrow(
                    input_card.get_bottom(),
                    output_card.get_top(),
                    buff=0.10,
                    color=REGION,
                    stroke_width=3.0,
                    max_tip_length_to_length_ratio=0.18,
                )
                for input_card, output_card in zip(input_row, output_row, strict=True)
            )
        )
        plus_fives = VGroup(
            *(
                MathTex("+5", font_size=28, color=REGION).move_to(arrow.get_center())
                for arrow in arrows
            )
        )
        one_digit_note = label("每一格換成一個新數字，所以原數字只能是 0 到 4", 27, REGION, "BOLD")
        one_digit_note.move_to([0, -2.75, 0])

        self.add(heading, source)
        self.play(FadeIn(title), FadeIn(example_note), run_time=0.55)
        self.play(LaggedStart(*(FadeIn(card) for card in input_row), lag_ratio=0.18), run_time=0.75)
        self.play(FadeIn(place_names), run_time=0.42)
        self.play(Create(arrows), FadeIn(plus_fives), run_time=0.72)
        self.play(LaggedStart(*(FadeIn(card) for card in output_row), lag_ratio=0.18), run_time=0.78)
        self.play(FadeIn(one_digit_note), run_time=0.55)
        self.wait(0.40)

        # Beat 02: convert the three visible place changes into +555.
        self.next_beat("earn_plus_555")
        new_title = label("三張卡仍是三張卡，位置也沒有改變", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(example_note),
            FadeOut(input_row),
            FadeOut(place_names),
            FadeOut(output_row),
            FadeOut(arrows),
            FadeOut(plus_fives),
            FadeOut(one_digit_note),
            run_time=0.72,
        )
        title = new_title
        divider = Line([0.45, -3.15, 0], [0.45, 2.30, 0], color=HAIRLINE, stroke_width=1.5)
        symbolic_input = self.digit_row(("h", "t", "u"), BLUE).move_to([-3.35, 1.28, 0])
        symbolic_output = self.digit_row(
            ("h+5", "t+5", "u+5"),
            POINT,
            width=1.48,
            font_size=34,
        ).move_to([-3.35, -1.30, 0])
        input_name = MathTex("a^2", font_size=38, color=BLUE).next_to(symbolic_input, LEFT, buff=0.34)
        output_name = MathTex("b", font_size=40, color=POINT).next_to(symbolic_output, LEFT, buff=0.34)
        place_effects = VGroup(
            MathTex("+500", font_size=28, color=REGION),
            MathTex("+50", font_size=28, color=REGION),
            MathTex("+5", font_size=28, color=REGION),
        )
        symbolic_arrows = VGroup()
        for source_card, target_card, effect in zip(
            symbolic_input,
            symbolic_output,
            place_effects,
            strict=True,
        ):
            arrow = Arrow(
                source_card.get_bottom(),
                target_card.get_top(),
                buff=0.10,
                color=REGION,
                stroke_width=2.8,
                max_tip_length_to_length_ratio=0.18,
            )
            effect.move_to(arrow.get_center())
            symbolic_arrows.add(arrow)
        position_sum = MathTex(
            r"b-a^2=500+50+5",
            font_size=39,
            color=INK,
        ).move_to([4.05, 0.95, 0])
        shift_equation = MathTex(
            r"b=a^2+555",
            font_size=49,
            color=INK,
        ).move_to([4.05, -0.25, 0])
        shift_equation.set_color_by_tex("555", REGION)
        domain_note = VGroup(
            label("b 是三位數，因此", 23, MUTED, "MEDIUM"),
            MathTex(r"100\le a^2\le999", font_size=31, color=BLUE),
            MathTex(r"0\le h,t,u\le4", font_size=31, color=REGION),
        ).arrange(DOWN, buff=0.18).move_to([4.05, -1.75, 0])
        self.play(Create(divider), FadeIn(symbolic_input), FadeIn(input_name), run_time=0.65)
        self.play(Create(symbolic_arrows), FadeIn(place_effects), run_time=0.72)
        self.play(FadeIn(symbolic_output), FadeIn(output_name), run_time=0.65)
        self.play(Write(position_sum), run_time=0.65)
        self.play(Write(shift_equation), run_time=0.62)
        self.play(FadeIn(domain_note), run_time=0.58)
        self.wait(0.38)

        # Beat 03: name the second square and expose a difference of squares.
        self.next_beat("name_the_second_square")
        new_title = label("b 也是平方數，先替它取一個平方根", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(divider),
            FadeOut(symbolic_input),
            FadeOut(symbolic_output),
            FadeOut(input_name),
            FadeOut(output_name),
            FadeOut(symbolic_arrows),
            FadeOut(place_effects),
            FadeOut(position_sum),
            FadeOut(domain_note),
            shift_equation.animate.move_to([-3.75, 1.45, 0]),
            run_time=0.75,
        )
        title = new_title
        square_name = self.factor_token(r"b=m^2", POINT).move_to([3.35, 1.45, 0])
        root_range = MathTex(r"10\le m\le31", font_size=34, color=POINT)
        root_range.next_to(square_name, DOWN, buff=0.28)
        substituted = MathTex(r"m^2=a^2+555", font_size=48, color=INK).move_to([0, -0.30, 0])
        difference = MathTex(r"m^2-a^2=555", font_size=52, color=INK).move_to([0, -1.55, 0])
        difference.set_color_by_tex("555", REGION)
        order = MathTex(r"555>0\quad\Longrightarrow\quad m>a>0", font_size=34, color=MUTED)
        order.move_to([0, -2.52, 0])
        prompt = label("兩個平方的差，怎麼變成可以完整列完的選項？", 25, CORAL, "BOLD")
        prompt.move_to([0, -3.18, 0])
        self.play(FadeIn(square_name), FadeIn(root_range), run_time=0.62)
        self.play(Write(substituted), run_time=0.75)
        self.play(Write(difference), run_time=0.72)
        self.play(FadeIn(order), run_time=0.52)
        self.play(FadeIn(prompt), run_time=0.50)
        self.wait(0.42)

        # Beat 04: geometrically rearrange the square difference into a rectangle.
        self.next_beat("rearrange_the_square_gap")
        new_title = label("把缺角搬過去，平方差就成了長方形", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(shift_equation),
            FadeOut(square_name),
            FadeOut(root_range),
            FadeOut(substituted),
            FadeOut(order),
            FadeOut(prompt),
            difference.animate.scale(0.72).move_to([-3.60, -2.35, 0]),
            run_time=0.72,
        )
        title = new_title
        outer = Rectangle(
            width=3.0,
            height=3.0,
            color=MUTED,
            stroke_width=2.5,
        ).move_to([-3.60, -0.18, 0])
        inner = Rectangle(
            width=2.10,
            height=2.10,
            color=BLUE,
            stroke_width=2.6,
            fill_color=BG,
            fill_opacity=1.0,
        ).move_to([-4.05, -0.63, 0])
        top_piece = Rectangle(
            width=3.0,
            height=0.90,
            color=REGION,
            stroke_width=2.5,
            fill_color=REGION,
            fill_opacity=0.25,
        ).move_to([-3.60, 0.87, 0])
        side_piece = Rectangle(
            width=0.90,
            height=2.10,
            color=POINT,
            stroke_width=2.5,
            fill_color=POINT,
            fill_opacity=0.25,
        ).move_to([-2.55, -0.63, 0])
        outer_m = MathTex("m", font_size=31, color=MUTED).next_to(outer, LEFT, buff=0.18)
        inner_a = MathTex("a", font_size=34, color=BLUE).move_to(inner)
        target_left = Rectangle(
            width=3.0,
            height=0.90,
            color=REGION,
            stroke_width=2.5,
            fill_color=REGION,
            fill_opacity=0.25,
        ).move_to([2.15, 0.25, 0])
        target_right = Rectangle(
            width=2.10,
            height=0.90,
            color=POINT,
            stroke_width=2.5,
            fill_color=POINT,
            fill_opacity=0.25,
        ).move_to([4.70, 0.25, 0])
        target_group = VGroup(target_left, target_right)
        width_brace = Brace(target_group, DOWN, color=PURPLE, buff=0.15)
        width_label = MathTex("m+a", font_size=32, color=PURPLE).next_to(
            width_brace, DOWN, buff=0.12
        )
        height_brace = Brace(target_group, LEFT, color=CORAL, buff=0.15)
        height_label = MathTex("m-a", font_size=31, color=CORAL).next_to(
            height_brace, LEFT, buff=0.12
        )
        factorization = MathTex(
            r"(m-a)(m+a)=555",
            font_size=45,
            color=INK,
        ).move_to([3.15, -1.80, 0])
        factorization.set_color_by_tex("555", REGION)
        useful_note = label("現在右邊只有有限個整數因數對", 24, REGION, "BOLD")
        useful_note.move_to([3.15, -2.62, 0])
        self.play(Create(outer), FadeIn(outer_m), run_time=0.55)
        self.play(FadeIn(top_piece), FadeIn(side_piece), Create(inner), FadeIn(inner_a), run_time=0.68)
        self.play(
            TransformFromCopy(top_piece, target_left),
            TransformFromCopy(side_piece, target_right),
            run_time=0.90,
        )
        self.play(Create(width_brace), FadeIn(width_label), Create(height_brace), FadeIn(height_label), run_time=0.65)
        self.play(Write(factorization), run_time=0.70)
        self.play(FadeIn(useful_note), run_time=0.48)
        self.wait(0.38)

        # Beat 05: establish positivity, order, and the parity gate.
        self.next_beat("set_factor_pair_rules")
        new_title = label("因數對還要通過順序與奇偶", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(outer),
            FadeOut(inner),
            FadeOut(top_piece),
            FadeOut(side_piece),
            FadeOut(outer_m),
            FadeOut(inner_a),
            FadeOut(target_group),
            FadeOut(width_brace),
            FadeOut(width_label),
            FadeOut(height_brace),
            FadeOut(height_label),
            FadeOut(difference),
            FadeOut(useful_note),
            factorization.animate.scale(0.82).move_to([0, 2.18, 0]),
            run_time=0.78,
        )
        title = new_title
        x_token = self.factor_token(r"x=m-a", CORAL).move_to([-3.60, 0.95, 0])
        y_token = self.factor_token(r"y=m+a", PURPLE).move_to([3.60, 0.95, 0])
        product = MathTex(r"xy=555", font_size=44, color=INK).move_to([0, 0.95, 0])
        positive_rule = MathTex(r"0<x<y", font_size=38, color=REGION).move_to([-4.20, -0.45, 0])
        inverse = VGroup(
            MathTex(r"a=\frac{y-x}{2}", font_size=39, color=BLUE),
            MathTex(r"m=\frac{x+y}{2}", font_size=39, color=POINT),
        ).arrange(RIGHT, buff=1.10).move_to([0.50, -0.45, 0])
        parity_rule = label("a、m 要是整數，所以 x、y 必須同奇偶", 26, MUTED, "MEDIUM")
        parity_rule.move_to([0, -1.50, 0])
        odd_factorization = VGroup(
            MathTex(r"555=3\cdot5\cdot37", font_size=34, color=REGION),
            MathTex(r"\Longrightarrow", font_size=34, color=REGION),
            label("x、y 都是奇數", 25, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.28).move_to([0, -2.30, 0])
        list_rule = label("因此只列正因數對，而且每一組都要保留", 25, CORAL, "BOLD")
        list_rule.move_to([0, -3.05, 0])
        self.play(FadeIn(x_token), FadeIn(y_token), Write(product), run_time=0.68)
        self.play(Write(positive_rule), FadeIn(inverse), run_time=0.70)
        self.play(FadeIn(parity_rule), run_time=0.48)
        self.play(Write(odd_factorization), run_time=0.70)
        self.play(FadeIn(list_rule), run_time=0.46)
        self.wait(0.38)

        # Beat 06: visibly enumerate every positive factor pair.
        self.next_beat("enumerate_every_factor_pair")
        new_title = label("從最外到最內，四組正因數一組也不漏", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(factorization),
            FadeOut(x_token),
            FadeOut(y_token),
            FadeOut(product),
            FadeOut(positive_rule),
            FadeOut(inverse),
            FadeOut(parity_rule),
            FadeOut(odd_factorization),
            FadeOut(list_rule),
            run_time=0.72,
        )
        title = new_title
        divisors = MathTex(
            r"1,3,5,15,37,111,185,555",
            font_size=35,
            color=INK,
        ).move_to([0, 2.22, 0])
        divisor_note = label("555 的全部正因數", 20, MUTED, "MEDIUM")
        divisor_note.next_to(divisors, LEFT, buff=0.35)
        headers = VGroup(
            MathTex("x", font_size=29, color=CORAL).move_to([-4.30, 1.48, 0]),
            MathTex("y", font_size=29, color=PURPLE).move_to([-2.25, 1.48, 0]),
            label("乘積", 21, MUTED, "BOLD").move_to([0.55, 1.48, 0]),
            label("奇偶檢查", 21, MUTED, "BOLD").move_to([4.00, 1.48, 0]),
        )
        factor_rows = VGroup(
            *(self.factor_row(x, y, 0.75 - 0.82 * index) for index, (x, y) in enumerate(POSITIVE_FACTOR_PAIRS))
        )
        complete_note = label("小因數超過 23 後，只會把同一組倒過來", 23, MUTED, "MEDIUM")
        complete_note.move_to([0, -2.95, 0])
        self.play(FadeIn(divisor_note), Write(divisors), run_time=0.68)
        self.play(FadeIn(headers), run_time=0.42)
        self.play(LaggedStart(*(FadeIn(row) for row in factor_rows), lag_ratio=0.18), run_time=1.20)
        self.play(FadeIn(complete_note), run_time=0.48)
        self.wait(0.40)

        # Beat 07: decode all four pairs without filtering any candidate early.
        self.next_beat("decode_all_candidates")
        new_title = label("每一組都還原成 a 與 m", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(divisor_note),
            FadeOut(divisors),
            FadeOut(headers),
            FadeOut(factor_rows),
            FadeOut(complete_note),
            run_time=0.70,
        )
        title = new_title
        decode_formulas = VGroup(
            MathTex(r"a=\frac{y-x}{2}", font_size=39, color=BLUE),
            MathTex(r"m=\frac{x+y}{2}", font_size=39, color=POINT),
        ).arrange(RIGHT, buff=1.35).move_to([0, 2.18, 0])
        candidate_headers = VGroup(
            MathTex("x", font_size=29, color=CORAL).move_to([-3.75, 1.48, 0]),
            MathTex("y", font_size=29, color=PURPLE).move_to([-1.45, 1.48, 0]),
            MathTex("a", font_size=29, color=BLUE).move_to([1.25, 1.48, 0]),
            MathTex("m", font_size=29, color=POINT).move_to([3.75, 1.48, 0]),
        )
        candidate_rows = VGroup(
            *(
                self.candidate_row(x, y, a, m, 0.75 - 0.82 * index)
                for index, (x, y, a, m, _) in enumerate(FACTOR_CANDIDATES)
            )
        )
        not_finished = label("這一步只解了方程，還沒有檢查原題的位數", 25, CORAL, "BOLD")
        not_finished.move_to([0, -2.95, 0])
        self.play(FadeIn(decode_formulas), FadeIn(candidate_headers), run_time=0.60)
        self.play(LaggedStart(*(FadeIn(row) for row in candidate_rows), lag_ratio=0.18), run_time=1.20)
        self.play(FadeIn(not_finished), run_time=0.48)
        self.wait(0.38)

        # Beat 08: apply both decimal-length gates to every candidate.
        self.next_beat("filter_by_digit_domains")
        new_title = label("先用兩個位數範圍，逐列淘汰", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(decode_formulas),
            FadeOut(candidate_headers),
            FadeOut(candidate_rows),
            FadeOut(not_finished),
            run_time=0.70,
        )
        title = new_title
        gate_explanation = VGroup(
            MathTex(r"10\le a\le99", font_size=34, color=BLUE),
            MathTex(r"100\le b=m^2\le999\ \Longleftrightarrow\ 10\le m\le31", font_size=34, color=POINT),
        ).arrange(RIGHT, buff=0.90).move_to([0, 2.25, 0])
        gate_headers = VGroup(
            label("候選 (a,m)", 21, MUTED, "BOLD").move_to([-4.55, 1.45, 0]),
            label("a 的範圍", 21, MUTED, "BOLD").move_to([-1.55, 1.45, 0]),
            label("m 的範圍", 21, MUTED, "BOLD").move_to([1.45, 1.45, 0]),
            label("判定", 21, MUTED, "BOLD").move_to([4.35, 1.45, 0]),
        )
        gate_rows = VGroup(
            self.gate_row(277, 278, "淘汰", "—", "a 不是二位數", 0.72),
            self.gate_row(91, 94, "通過", "淘汰", "b 超過三位數", -0.12),
            self.gate_row(53, 58, "通過", "淘汰", "b 超過三位數", -0.96),
            self.gate_row(11, 26, "通過", "通過", "待做數字檢查", -1.80, survives=True),
        )
        gate_note = label("只剩最後一列，但還不能跳過原本的逐位操作", 24, POINT, "BOLD")
        gate_note.move_to([0, -2.88, 0])
        self.play(FadeIn(gate_explanation), FadeIn(gate_headers), run_time=0.62)
        self.play(LaggedStart(*(FadeIn(row) for row in gate_rows), lag_ratio=0.22), run_time=1.30)
        self.play(
            gate_rows[0].animate.set_opacity(0.42),
            gate_rows[1].animate.set_opacity(0.42),
            gate_rows[2].animate.set_opacity(0.42),
            Indicate(gate_rows[3], color=POINT),
            run_time=0.78,
        )
        self.play(FadeIn(gate_note), run_time=0.48)
        self.wait(0.40)

        # Beat 09: hold before calculating the surviving digit cards.
        self.next_beat("hold_before_digit_check")
        new_title = label("只剩一組，最後回到題目原來的操作", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(gate_explanation),
            FadeOut(gate_headers),
            FadeOut(gate_rows),
            FadeOut(gate_note),
            run_time=0.72,
        )
        title = new_title
        survivor = VGroup(
            self.factor_token("a=11", BLUE),
            self.factor_token("m=26", POINT),
        ).arrange(RIGHT, buff=0.70).move_to([0, 2.05, 0])
        pre_divider = Line([1.05, -2.65, 0], [1.05, 1.20, 0], color=HAIRLINE, stroke_width=1.5)
        input_frames = self.blank_digit_frames(BLUE).move_to([-3.30, 0.55, 0])
        output_frames = self.blank_digit_frames(REGION).move_to([-3.30, -1.40, 0])
        eleven_square = MathTex(r"11^2=", font_size=40, color=BLUE).next_to(
            input_frames, LEFT, buff=0.30
        )
        pre_arrows = VGroup(
            *(
                Arrow(
                    upper.get_bottom(),
                    lower.get_top(),
                    buff=0.10,
                    color=REGION,
                    stroke_width=2.8,
                    max_tip_length_to_length_ratio=0.18,
                )
                for upper, lower in zip(input_frames, output_frames, strict=True)
            )
        )
        pre_plus = VGroup(
            *(
                MathTex("+5", font_size=27, color=REGION).move_to(arrow.get_center())
                for arrow in pre_arrows
            )
        )
        other_square = MathTex(r"26^2=?", font_size=51, color=POINT).move_to([4.20, -0.10, 0])
        pre_question = label("兩邊會落在同一個三位數嗎？", 28, CORAL, "BOLD")
        pre_question.move_to([2.80, -1.30, 0])
        pause_note = label("先自己算完，再往下一張", 22, MUTED, "MEDIUM")
        pause_note.move_to([2.80, -1.90, 0])
        self.play(FadeIn(survivor), run_time=0.58)
        self.play(Create(pre_divider), FadeIn(input_frames), FadeIn(eleven_square), run_time=0.62)
        self.play(Create(pre_arrows), FadeIn(pre_plus), FadeIn(output_frames), run_time=0.70)
        self.play(FadeIn(other_square), run_time=0.58)
        self.play(FadeIn(pre_question), FadeIn(pause_note), run_time=0.52)
        self.wait(0.72)

        # Beat 10: reveal the cards, verify the second square, then state the pair.
        self.next_beat("reveal_the_unique_pair")
        new_title = label("數字卡與平方同時對上，答案才落定", 32, INK, "BOLD")
        new_title.move_to(title)
        self.play(
            self.title_change(title, new_title),
            FadeOut(pre_question),
            FadeOut(pause_note),
            FadeOut(other_square),
            run_time=0.68,
        )
        title = new_title
        input_values = VGroup(
            *(
                MathTex(value, font_size=43, color=BLUE).move_to(frame)
                for value, frame in zip(("1", "2", "1"), input_frames, strict=True)
            )
        )
        output_values = VGroup(
            *(
                MathTex(value, font_size=43, color=REGION).move_to(frame)
                for value, frame in zip(("6", "7", "6"), output_frames, strict=True)
            )
        )
        verified_square = MathTex(r"26^2=676", font_size=50, color=POINT).move_to([4.15, 0.25, 0])
        same_value = label("同一個三位平方數", 24, REGION, "BOLD")
        same_value.move_to([4.15, -0.55, 0])
        b_value = MathTex("b=676", font_size=42, color=REGION).move_to([4.15, -1.35, 0])
        answer = MathTex(r"(a,b)=(11,676)", font_size=55, color=POINT).move_to([2.10, -2.45, 0])
        answer_frame = SurroundingRectangle(answer, color=POINT, buff=0.22, stroke_width=3.0)
        conclusion = label("四組因數查完，逐位規則也成立", 22, MUTED, "MEDIUM")
        conclusion.move_to([-3.35, -2.75, 0])
        self.play(LaggedStart(*(FadeIn(value) for value in input_values), lag_ratio=0.22), run_time=0.78)
        self.play(
            LaggedStart(
                *(
                    Succession(Indicate(arrow, color=REGION), FadeIn(value))
                    for arrow, value in zip(pre_arrows, output_values, strict=True)
                ),
                lag_ratio=0.18,
            ),
            run_time=1.15,
        )
        self.play(FadeIn(verified_square), FadeIn(same_value), run_time=0.68)
        self.play(FadeIn(b_value), Circumscribe(output_frames, color=REGION), run_time=0.65)
        self.play(Write(answer), Create(answer_frame), run_time=0.75)
        self.play(FadeIn(conclusion), run_time=0.48)
        self.wait(0.68)
