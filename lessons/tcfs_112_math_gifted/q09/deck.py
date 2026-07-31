"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q9."""

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
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DL, DOWN, LEFT, RIGHT, UP, UR


M_CANDIDATES = (16, 25, 36)
TERMINAL_DIGITS = (0, 1, 4, 5, 6, 9)
OUTER_DIGITS = (5, 6, 9)
BRANCH_DIGITS = {
    5: ((9, 8),),
    6: ((8, 8), (9, 6)),
    9: ((5, 8), (6, 6), (7, 4), (8, 2), (9, 0)),
}


def palindrome_value(a: int, b: int, c: int) -> int:
    return 10001 * a + 1010 * b + 100 * c


DIGIT_CANDIDATES = tuple(
    palindrome_value(a, b, c)
    for a in OUTER_DIGITS
    for b, c in BRANCH_DIGITS[a]
)
DISPLAY_CANDIDATES = (
    59895,
    68886,
    69696,
    95859,
    96669,
    97479,
    98289,
    99099,
)
MOD4_SURVIVORS = tuple(
    value for value in DISPLAY_CANDIDATES if value % 4 in (0, 1)
)
EXHAUSTIVE_SOLUTIONS = tuple(
    (digit_sum, value, math.isqrt(value))
    for a in range(1, 10)
    for b in range(10)
    for c in range(10)
    for value in (palindrome_value(a, b, c),)
    for digit_sum in (2 * a + 2 * b + c,)
    if math.isqrt(value) ** 2 == value
    and 10 <= digit_sum <= 99
    and math.isqrt(digit_sum) ** 2 == digit_sum
    and math.isqrt(sum(int(digit) for digit in str(digit_sum))) ** 2
    == sum(int(digit) for digit in str(digit_sum))
)

if M_CANDIDATES != tuple(square for square in range(10, 46) if math.isqrt(square) ** 2 == square):
    raise ValueError("the two-digit square audit between 10 and 45 changed")
if tuple(sum(int(digit) for digit in str(value)) for value in M_CANDIDATES) != (7, 7, 9):
    raise ValueError("the second digit-sum gate must select 36 uniquely")
if set(DIGIT_CANDIDATES) != set(DISPLAY_CANDIDATES) or len(DIGIT_CANDIDATES) != 8:
    raise ValueError("the digit equations must produce exactly eight palindromes")
if MOD4_SURVIVORS != (69696, 96669, 98289):
    raise ValueError("the modulo-four gate must leave exactly three candidates")
if not (310**2 < 96669 < 311**2):
    raise ValueError("96669 must lie strictly between two consecutive squares")
if not (313**2 < 98289 < 314**2):
    raise ValueError("98289 must lie strictly between two consecutive squares")
if 264**2 != 69696:
    raise ValueError("the surviving palindrome must be 264 squared")
if EXHAUSTIVE_SOLUTIONS != ((36, 69696, 264),):
    raise ValueError("the full digit-triple audit must have one solution")


class CarloTcfs112MathQ09(CarloSlide):
    """Shrink the palindromic-square search through visible finite gates."""

    lesson_id = "carlo.tcfs_112_math_gifted.q09"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def stage_title(text: str):
        title = label(text, 30, INK, "BOLD")
        title.move_to([0, 3.13, 0])
        return title

    @staticmethod
    def digit_card(
        value: str,
        color: str,
        *,
        width: float = 1.18,
        height: float = 1.30,
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
    def palindrome_row(
        cls,
        values: tuple[str, str, str, str, str],
        *,
        card_width: float = 1.18,
        card_height: float = 1.30,
        font_size: float = 48,
        buff: float = 0.16,
    ) -> VGroup:
        colors = (POINT, BLUE, REGION, BLUE, POINT)
        row = VGroup(
            *(
                cls.digit_card(
                    value,
                    color,
                    width=card_width,
                    height=card_height,
                    font_size=font_size,
                )
                for value, color in zip(values, colors, strict=True)
            )
        )
        row.arrange(RIGHT, buff=buff)
        return row

    @staticmethod
    def candidate_card(
        value: int,
        *,
        width: float = 2.55,
        height: float = 0.82,
        font_size: float = 33,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            color=HAIRLINE,
            stroke_width=2.0,
            fill_color=BG,
            fill_opacity=0.98,
        )
        colors = (POINT, BLUE, REGION, BLUE, POINT)
        digits = VGroup(
            *(
                MathTex(digit, font_size=font_size, color=color)
                for digit, color in zip(str(value), colors, strict=True)
            )
        ).arrange(RIGHT, buff=0.045)
        digits.move_to(frame)
        return VGroup(frame, digits)

    @staticmethod
    def choice_chip(value: str, color: str, *, width: float = 1.08) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.05,
            color=color,
            stroke_width=2.3,
            fill_color=color,
            fill_opacity=0.10,
        )
        value_tex = MathTex(value, font_size=34, color=color).move_to(frame)
        return VGroup(frame, value_tex)

    @staticmethod
    def text_chip(text: str, color: str, *, width: float) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=0.68,
            corner_radius=0.05,
            color=color,
            stroke_width=2.0,
            fill_color=color,
            fill_opacity=0.09,
        )
        text_label = label(text, 22, color, "BOLD").move_to(frame)
        return VGroup(frame, text_label)

    @staticmethod
    def strike(target, *, color: str = CORAL, stroke_width: float = 4.0) -> Line:
        return Line(
            target.get_corner(DL) + [0.08, 0.08, 0],
            target.get_corner(UR) - [0.08, 0.08, 0],
            color=color,
            stroke_width=stroke_width,
        ).set_z_index(12)

    @staticmethod
    def audit_card(value: int, digit_sum: int, valid: bool) -> VGroup:
        color = REGION if valid else CORAL
        frame = RoundedRectangle(
            width=2.65,
            height=1.62,
            corner_radius=0.07,
            color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.08,
        )
        digits = list(str(value))
        value_tex = MathTex(str(value), font_size=48, color=POINT).move_to(
            frame.get_center() + UP * 0.35
        )
        sum_tex = MathTex(
            rf"{digits[0]}+{digits[1]}={digit_sum}",
            font_size=34,
            color=color,
        ).move_to(frame.get_center() + DOWN * 0.36)
        return VGroup(frame, value_tex, sum_tex)

    @staticmethod
    def square_interval(
        left_root: int,
        candidate: int,
        right_root: int,
    ) -> VGroup:
        left_value = left_root**2
        right_value = right_root**2
        start_x, end_x = -4.85, 4.85
        line_y = -0.15
        fraction = (candidate - left_value) / (right_value - left_value)
        candidate_x = start_x + fraction * (end_x - start_x)
        baseline = Line(
            [start_x, line_y, 0],
            [end_x, line_y, 0],
            color=HAIRLINE,
            stroke_width=3.0,
        )
        ticks = VGroup(
            Line([start_x, line_y - 0.14, 0], [start_x, line_y + 0.14, 0], color=INK),
            Line([end_x, line_y - 0.14, 0], [end_x, line_y + 0.14, 0], color=INK),
        )
        dots = VGroup(
            Dot([start_x, line_y, 0], radius=0.075, color=BLUE),
            Dot([candidate_x, line_y, 0], radius=0.095, color=POINT),
            Dot([end_x, line_y, 0], radius=0.075, color=BLUE),
        )
        left_label = MathTex(
            rf"{left_root}^2={left_value}", font_size=31, color=BLUE
        ).move_to([start_x + 0.65, line_y + 0.58, 0])
        right_label = MathTex(
            rf"{right_root}^2={right_value}", font_size=31, color=BLUE
        ).move_to([end_x - 0.68, line_y + 0.58, 0])
        candidate_label = MathTex(
            str(candidate), font_size=37, color=POINT
        ).move_to([candidate_x - 0.25, line_y - 0.55, 0])
        inequality = MathTex(
            rf"{left_value}<{candidate}<{right_value}",
            font_size=39,
            color=INK,
        ).move_to([0, -1.55, 0])
        return VGroup(
            baseline,
            ticks,
            dots,
            left_label,
            right_label,
            candidate_label,
            inequality,
        )

    def construct(self) -> None:
        heading = label("第 9 題｜先縮小，再驗平方", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 9 頁｜影片 E8hGcX6oQO4 00:00-08:52.40",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 mirror_three_digits: construct the mirrored decimal object before using algebra.
        self.begin_beat("mirror_three_digits")
        stage_title = self.stage_title("五個位置，其實只有三個選擇")
        symbolic_row = self.palindrome_row(("a", "b", "c", "b", "a"))
        symbolic_row.move_to([0, 0.65, 0])
        mirror_axis = DashedLine(
            [0, -0.20, 0], [0, 1.55, 0], color=HAIRLINE, stroke_width=2.0
        )
        n_formula = MathTex(
            r"n=\overline{abcba}", font_size=49, color=INK
        ).move_to([0, -1.05, 0])
        nonzero = VGroup(
            MathTex("a\ne0", font_size=34, color=POINT),
            label("最高位不能是 0", 22, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.22).move_to([0, -1.90, 0])

        self.add(heading, source)
        self.play(FadeIn(stage_title), run_time=0.45)
        self.play(
            LaggedStart(
                FadeIn(symbolic_row[0]),
                FadeIn(symbolic_row[1]),
                FadeIn(symbolic_row[2]),
                lag_ratio=0.20,
            ),
            Create(mirror_axis),
            run_time=1.0,
        )
        self.play(
            TransformFromCopy(symbolic_row[1], symbolic_row[3]),
            TransformFromCopy(symbolic_row[0], symbolic_row[4]),
            run_time=0.9,
        )
        self.play(Write(n_formula), FadeIn(nonzero), run_time=0.85)
        self.wait(0.35)

        # Beat 02 fold_outer_digit_pair: fold the five visible cards into their three contributions.
        self.next_beat("fold_outer_digit_pair")
        next_title = self.stage_title("把鏡像位置成對相加")
        n_formula_target = n_formula.copy().move_to([-1.05, 1.82, 0])
        n_square = MathTex(r"n=q^2", font_size=34, color=PURPLE).move_to(
            [1.42, 1.82, 0]
        )
        sum_formula = MathTex(
            "m=", "2a", "+", "2b", "+", "c", font_size=51, color=INK
        ).move_to([0, -0.85, 0])
        sum_formula[1].set_color(POINT)
        sum_formula[3].set_color(BLUE)
        sum_formula[5].set_color(REGION)
        constraints = VGroup(
            self.text_chip("m 是兩位數", BLUE, width=2.55),
            self.text_chip("m 是完全平方數", PURPLE, width=3.05),
            self.text_chip("m 的數字和也是平方數", REGION, width=4.05),
        ).arrange(RIGHT, buff=0.28).move_to([0, -2.15, 0])

        self.play(self.title_change(stage_title, next_title), run_time=0.45)
        stage_title = next_title
        self.play(
            Transform(n_formula, n_formula_target),
            FadeIn(n_square),
            FadeOut(nonzero),
            run_time=0.55,
        )
        self.play(Indicate(VGroup(symbolic_row[0], symbolic_row[4]), color=POINT), run_time=0.55)
        self.play(Write(sum_formula[0]), TransformFromCopy(symbolic_row[0][1], sum_formula[1]), run_time=0.55)

        # Beat 03 fold_inner_digit_pairs: continue at a settled semantic boundary.
        self.next_beat("fold_inner_digit_pairs")
        self.play(Indicate(VGroup(symbolic_row[1], symbolic_row[3]), color=BLUE), run_time=0.55)
        self.play(Write(sum_formula[2]), TransformFromCopy(symbolic_row[1][1], sum_formula[3]), run_time=0.55)
        self.play(Indicate(symbolic_row[2], color=REGION), run_time=0.5)
        self.play(Write(sum_formula[4]), TransformFromCopy(symbolic_row[2][1], sum_formula[5]), run_time=0.55)

        # Beat 04 state_digit_sum_constraints: continue at a settled semantic boundary.
        self.next_beat("state_digit_sum_constraints")
        self.play(LaggedStart(*(FadeIn(chip) for chip in constraints), lag_ratio=0.15), run_time=0.9)
        self.wait(0.30)

        # Beat 05 list_digit_sum_squares: exhaust the much smaller two-digit square search for m.
        self.next_beat("list_digit_sum_squares")
        next_title = self.stage_title("先決定小數字 m")
        range_line = NumberLine(
            x_range=[10, 45, 5],
            length=10.5,
            include_numbers=True,
            font_size=23,
            color=HAIRLINE,
        ).move_to([0, 1.20, 0])
        range_caption = MathTex(r"10\le m\le45", font_size=37, color=INK).move_to(
            [0, 2.15, 0]
        )
        square_dots = VGroup(
            *(Dot(range_line.n2p(value), radius=0.09, color=POINT) for value in M_CANDIDATES)
        )
        audit_cards = VGroup(
            self.audit_card(16, 7, False),
            self.audit_card(25, 7, False),
            self.audit_card(36, 9, True),
        ).arrange(RIGHT, buff=0.62).move_to([0, -0.65, 0])
        first_strike = self.strike(audit_cards[0], stroke_width=4.5)
        second_strike = self.strike(audit_cards[1], stroke_width=4.5)
        m_result = MathTex(r"m=36", font_size=54, color=POINT).move_to([0, -2.20, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(symbolic_row, mirror_axis, n_formula, n_square, sum_formula, constraints),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Create(range_line), Write(range_caption), FadeIn(square_dots), run_time=0.85)
        self.play(LaggedStart(*(FadeIn(card[0], card[1]) for card in audit_cards), lag_ratio=0.18), run_time=0.85)
        self.play(FadeIn(audit_cards[0][2]), Create(first_strike), run_time=0.55)

        # Beat 06 find_the_digit_sum: continue at a settled semantic boundary.
        self.next_beat("find_the_digit_sum")
        self.play(FadeIn(audit_cards[1][2]), Create(second_strike), run_time=0.55)
        self.play(FadeIn(audit_cards[2][2]), Circumscribe(audit_cards[2], color=REGION), run_time=0.7)
        self.play(TransformFromCopy(audit_cards[2][1], m_result), run_time=0.65)
        self.wait(0.35)

        # Beat 07 list_terminal_square_digits: combine the terminal-square digit rule with the inner capacity.
        self.next_beat("list_terminal_square_digits")
        next_title = self.stage_title("先限制最外面的 a")
        outer_row = self.palindrome_row(
            ("a", "b", "c", "b", "a"),
            card_width=0.94,
            card_height=1.02,
            font_size=39,
        ).move_to([0, 1.72, 0])
        terminal_rule = MathTex(
            r"a\in\{0,1,4,5,6,9\}", font_size=39, color=INK
        ).move_to([0, 0.78, 0])
        terminal_rule.set_color_by_tex("a", POINT)
        a_chips = VGroup(
            *(self.choice_chip(str(value), POINT) for value in TERMINAL_DIGITS)
        ).arrange(RIGHT, buff=0.24).move_to([0, -0.02, 0])
        zero_strike = self.strike(a_chips[0])
        inner_max = VGroup(
            self.palindrome_row(
                ("", "9", "9", "9", ""),
                card_width=0.60,
                card_height=0.72,
                font_size=30,
                buff=0.10,
            )[1:4],
            MathTex(r"9+9+9=27", font_size=34, color=REGION),
        ).arrange(DOWN, buff=0.20).move_to([-3.35, -1.45, 0])
        bound_group = VGroup(
            MathTex(r"36=2a+(2b+c)", font_size=38, color=INK),
            MathTex(r"2b+c\le27", font_size=36, color=REGION),
            MathTex(r"a\ge5", font_size=45, color=POINT),
        ).arrange(DOWN, buff=0.23).move_to([3.05, -1.38, 0])
        low_strikes = VGroup(self.strike(a_chips[1]), self.strike(a_chips[2]))

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(range_line, range_caption, square_dots, audit_cards, first_strike, second_strike, m_result),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(FadeIn(outer_row), run_time=0.55)
        self.play(
            Indicate(VGroup(outer_row[0], outer_row[4]), color=POINT),
            Write(terminal_rule),
            run_time=0.7,
        )
        self.play(LaggedStart(*(FadeIn(chip) for chip in a_chips), lag_ratio=0.10), run_time=0.75)

        # Beat 08 derive_outer_digit_bound: continue at a settled semantic boundary.
        self.next_beat("derive_outer_digit_bound")
        self.play(Create(zero_strike), run_time=0.35)
        self.play(FadeIn(inner_max), run_time=0.7)
        self.play(LaggedStart(*(Write(item) for item in bound_group), lag_ratio=0.20), run_time=1.0)

        # Beat 09 retain_outer_digit_branches: continue at a settled semantic boundary.
        self.next_beat("retain_outer_digit_branches")
        self.play(Create(low_strikes), run_time=0.5)
        self.play(
            *(Indicate(a_chips[index], color=REGION) for index in (3, 4, 5)),
            run_time=0.65,
        )
        self.wait(0.30)

        # Beat 10 establish_a_nine_compensation: enumerate every inner state for a=9 by compensating b and c.
        self.next_beat("establish_a_nine_compensation")
        next_title = self.stage_title("固定 a=9，只動 b 與 c")
        branch_equation = MathTex(r"a=9,\qquad 2b+c=18", font_size=42, color=INK).move_to(
            [0, 2.05, 0]
        )
        branch_equation.set_color_by_tex("a=9", POINT)
        states_nine = BRANCH_DIGITS[9]
        current_b, current_c = states_nine[0]
        current_row = self.palindrome_row(
            tuple(str(value) for value in (9, current_b, current_c, current_b, 9)),
            card_width=0.88,
            card_height=0.94,
            font_size=36,
        ).move_to([0, 0.72, 0])
        pair_state = MathTex(
            rf"(b,c)=({current_b},{current_c}),\quad 2\cdot{current_b}+{current_c}=18",
            font_size=35,
            color=INK,
        ).move_to([0, -0.22, 0])
        nine_positions = (-4.80, -2.40, 0.0, 2.40, 4.80)
        branch_nine_cards: list[VGroup] = []

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(outer_row, terminal_rule, a_chips, zero_strike, inner_max, bound_group, low_strikes),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Write(branch_equation), FadeIn(current_row), Write(pair_state), run_time=0.8)
        first_card = self.candidate_card(palindrome_value(9, current_b, current_c), width=2.05, font_size=29)
        first_card.move_to([nine_positions[0], -1.55, 0])
        branch_nine_cards.append(first_card)
        self.play(Indicate(current_row, color=REGION), run_time=0.30)
        self.play(FadeIn(first_card, shift=DOWN * 0.12), run_time=0.38)

        # Beat 11 enumerate_a_nine: continue at a settled semantic boundary.
        self.next_beat("enumerate_a_nine")
        for position, (new_b, new_c) in zip(
            (nine_positions[1], nine_positions[2]),
            (states_nine[1], states_nine[2]),
            strict=True,
        ):
            new_row = self.palindrome_row(
                tuple(str(value) for value in (9, new_b, new_c, new_b, 9)),
                card_width=0.88,
                card_height=0.94,
                font_size=36,
            ).move_to(current_row)
            new_pair = MathTex(
                rf"(b,c)=({new_b},{new_c}),\quad 2\cdot{new_b}+{new_c}=18",
                font_size=35,
                color=INK,
            ).move_to(pair_state)
            candidate = self.candidate_card(
                palindrome_value(9, new_b, new_c), width=2.05, font_size=29
            ).move_to([position, -1.55, 0])
            branch_nine_cards.append(candidate)
            self.play(Transform(current_row, new_row), Transform(pair_state, new_pair), run_time=0.35)
            self.play(FadeIn(candidate, shift=DOWN * 0.12), run_time=0.36)

        self.next_beat("finish_a_nine_candidates")
        for position, (new_b, new_c) in zip(
            (nine_positions[3], nine_positions[4]),
            (states_nine[3], states_nine[4]),
            strict=True,
        ):
            new_row = self.palindrome_row(
                tuple(str(value) for value in (9, new_b, new_c, new_b, 9)),
                card_width=0.88,
                card_height=0.94,
                font_size=36,
            ).move_to(current_row)
            new_pair = MathTex(
                rf"(b,c)=({new_b},{new_c}),\quad 2\cdot{new_b}+{new_c}=18",
                font_size=35,
                color=INK,
            ).move_to(pair_state)
            candidate = self.candidate_card(
                palindrome_value(9, new_b, new_c), width=2.05, font_size=29
            ).move_to([position, -1.55, 0])
            branch_nine_cards.append(candidate)
            self.play(Transform(current_row, new_row), Transform(pair_state, new_pair), run_time=0.35)
            self.play(FadeIn(candidate, shift=DOWN * 0.12), run_time=0.36)
        self.wait(0.30)

        # Beat 12 set_up_a_six_branch: the a=6 branch has only two legal inner states.
        self.next_beat("set_up_a_six_branch")
        next_title = self.stage_title("固定 a=6，只剩兩種中央配置")
        branch_nine_group = VGroup(*branch_nine_cards)
        branch_nine_label = MathTex(r"a=9", font_size=30, color=POINT)
        branch_six_equation = MathTex(r"a=6,\qquad 2b+c=24", font_size=40, color=INK).move_to(
            [0, 0.35, 0]
        )
        branch_six_equation.set_color_by_tex("a=6", POINT)
        states_six = BRANCH_DIGITS[6]
        six_b, six_c = states_six[0]
        six_row = self.palindrome_row(
            tuple(str(value) for value in (6, six_b, six_c, six_b, 6)),
            card_width=0.72,
            card_height=0.78,
            font_size=31,
        ).move_to([-2.35, -0.65, 0])
        six_pair = MathTex(
            rf"(b,c)=({six_b},{six_c})", font_size=32, color=INK
        ).move_to([2.35, -0.65, 0])
        branch_six_cards: list[VGroup] = []

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(current_row, pair_state, branch_equation),
            run_time=0.45,
        )
        stage_title = next_title
        self.play(
            branch_nine_group.animate.scale(0.82).arrange(RIGHT, buff=0.22).move_to([0, 1.45, 0]),
            run_time=0.50,
        )
        branch_nine_label.next_to(branch_nine_group, LEFT, buff=0.22)
        self.play(
            FadeIn(branch_six_equation),
            FadeIn(branch_nine_label),
            FadeIn(six_row),
            Write(six_pair),
            run_time=0.75,
        )

        # Beat 13 enumerate_a_six: continue at a settled semantic boundary.
        self.next_beat("enumerate_a_six")
        first_six_candidate = self.candidate_card(
            palindrome_value(6, *states_six[0]), width=2.25, font_size=31
        ).move_to([-1.35, -1.85, 0])
        branch_six_cards.append(first_six_candidate)
        self.play(FadeIn(first_six_candidate, shift=DOWN * 0.12), run_time=0.38)

        new_b, new_c = states_six[1]
        new_row = self.palindrome_row(
            tuple(str(value) for value in (6, new_b, new_c, new_b, 6)),
            card_width=0.72,
            card_height=0.78,
            font_size=31,
        ).move_to(six_row)
        new_pair = MathTex(
            rf"(b,c)=({new_b},{new_c})", font_size=32, color=INK
        ).move_to(six_pair)
        self.play(Transform(six_row, new_row), Transform(six_pair, new_pair), run_time=0.4)
        second_six_candidate = self.candidate_card(
            palindrome_value(6, new_b, new_c), width=2.25, font_size=31
        ).move_to([1.35, -1.85, 0])
        branch_six_cards.append(second_six_candidate)
        self.play(FadeIn(second_six_candidate, shift=DOWN * 0.12), run_time=0.38)
        self.wait(0.30)

        # Beat 14 set_up_a_five_branch: finish a=5 and settle all eight candidates in one complete grid.
        self.next_beat("set_up_a_five_branch")
        next_title = self.stage_title("最後一個分支，只有一個候選")
        branch_six_group = VGroup(*branch_six_cards)
        branch_six_label = MathTex(r"a=6", font_size=30, color=POINT)
        branch_five_equation = MathTex(r"a=5,\qquad 2b+c=26", font_size=39, color=INK).move_to(
            [0, -0.55, 0]
        )
        branch_five_equation.set_color_by_tex("a=5", POINT)
        five_b, five_c = BRANCH_DIGITS[5][0]
        five_row = self.palindrome_row(
            tuple(str(value) for value in (5, five_b, five_c, five_b, 5)),
            card_width=0.68,
            card_height=0.74,
            font_size=29,
        ).move_to([-2.15, -1.65, 0])
        five_pair = MathTex(r"(b,c)=(9,8)", font_size=31, color=INK).move_to(
            [1.00, -1.65, 0]
        )
        five_card = self.candidate_card(59895, width=2.20, font_size=30).move_to(
            [4.25, -1.65, 0]
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(six_row, six_pair, branch_six_equation),
            run_time=0.45,
        )
        stage_title = next_title
        self.play(
            branch_nine_group.animate.scale(0.87).move_to([0.55, 1.70, 0]),
            branch_six_group.animate.scale(0.86).move_to([0.55, 0.55, 0]),
            run_time=0.50,
        )
        branch_nine_label.next_to(branch_nine_group, LEFT, buff=0.22)
        branch_six_label.next_to(branch_six_group, LEFT, buff=0.22)
        self.play(
            FadeIn(branch_five_equation),
            FadeIn(branch_six_label),
            FadeIn(five_row),
            Write(five_pair),
            run_time=0.7,
        )

        # Beat 15 enumerate_a_five: continue at a settled semantic boundary.
        self.next_beat("enumerate_a_five")
        branch_equation = branch_five_equation
        self.play(Indicate(five_row, color=REGION), run_time=0.30)
        self.play(FadeIn(five_card, shift=RIGHT * 0.12), run_time=0.38)

        # Beat 16 assemble_eight_candidates: continue at a settled semantic boundary.
        self.next_beat("assemble_eight_candidates")
        complete_title = self.stage_title("八個候選，沒有遺漏")
        count_formula = MathTex(r"1+2+5=8", font_size=39, color=POINT).move_to(
            [0, 2.12, 0]
        )
        grid_positions = (
            (-4.65, 0.65),
            (-1.55, 0.65),
            (1.55, 0.65),
            (4.65, 0.65),
            (-4.65, -0.95),
            (-1.55, -0.95),
            (1.55, -0.95),
            (4.65, -0.95),
        )
        grid_cards = {
            value: self.candidate_card(value).move_to([x, y, 0])
            for value, (x, y) in zip(DISPLAY_CANDIDATES, grid_positions, strict=True)
        }
        grid_group = VGroup(*(grid_cards[value] for value in DISPLAY_CANDIDATES))
        self.play(
            self.title_change(stage_title, complete_title),
            FadeOut(
                branch_equation,
                branch_nine_group,
                branch_six_group,
                branch_nine_label,
                branch_six_label,
                five_row,
                five_pair,
                five_card,
            ),
            run_time=0.55,
        )
        stage_title = complete_title
        self.play(Write(count_formula), LaggedStart(*(FadeIn(card) for card in grid_group), lag_ratio=0.08), run_time=1.0)
        self.wait(0.35)

        # Beat 17 prove_square_residues_mod_four: prove the mod-4 rule, then attach an actual residue to every card.
        self.next_beat("prove_square_residues_mod_four")
        next_title = self.stage_title("先用除以 4 的餘數過濾")
        even_rule = MathTex(
            r"(2r)^2=4r^2\equiv0\pmod4", font_size=31, color=BLUE
        ).move_to([-3.25, 2.12, 0])
        odd_rule = MathTex(
            r"(2r+1)^2\equiv1\pmod4", font_size=31, color=PURPLE
        ).move_to([3.25, 2.12, 0])
        residue_badges: dict[int, MathTex] = {}
        reject_lines: dict[int, Line] = {}
        rejected = tuple(value for value in DISPLAY_CANDIDATES if value not in MOD4_SURVIVORS)
        for value, (_, y) in zip(DISPLAY_CANDIDATES, grid_positions, strict=True):
            color = PURPLE if value in MOD4_SURVIVORS else CORAL
            badge = MathTex(
                rf"{value % 100}\equiv {value % 4}\pmod4",
                font_size=24,
                color=color,
            )
            badge.next_to(grid_cards[value], DOWN, buff=0.12)
            residue_badges[value] = badge
            if value in rejected:
                reject_lines[value] = self.strike(grid_cards[value], stroke_width=3.5)
        survivor_note = label("只表示仍有可能", 22, PURPLE, "BOLD").move_to(
            [0, -2.34, 0]
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(count_formula),
            run_time=0.45,
        )
        stage_title = next_title
        self.play(Write(even_rule), Write(odd_rule), run_time=0.8)

        # Beat 18 test_mod_four: continue at a settled semantic boundary.
        self.next_beat("test_mod_four")
        self.play(
            *(
                Indicate(VGroup(card[1][-2], card[1][-1]), color=POINT, scale_factor=1.15)
                for card in grid_group
            ),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *(FadeIn(residue_badges[value]) for value in DISPLAY_CANDIDATES),
                lag_ratio=0.07,
            ),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(Create(reject_lines[value]) for value in rejected), lag_ratio=0.08),
            *(
                grid_cards[value][0].animate.set_stroke(color=PURPLE, width=3.0)
                for value in MOD4_SURVIVORS
            ),
            run_time=0.9,
        )
        self.play(FadeIn(survivor_note), run_time=0.4)
        self.wait(0.30)

        # Beat 19 isolate_three_survivors: isolate the three survivors and restore the original square test.
        self.next_beat("isolate_three_survivors")
        next_title = self.stage_title("必要條件通過後，還要真的驗平方")
        survivor_order = (96669, 69696, 98289)
        survivor_positions = (-4.25, 0.0, 4.25)
        survivor_cards = {
            value: self.candidate_card(value, width=3.05, height=1.05, font_size=43).move_to(
                [x, 0.55, 0]
            )
            for value, x in zip(survivor_order, survivor_positions, strict=True)
        }
        square_condition = MathTex(r"n=q^2", font_size=45, color=PURPLE).move_to(
            [0, 1.95, 0]
        )
        gate_note = VGroup(
            label("模 4", 25, MUTED, "BOLD"),
            label("只是第一道門", 25, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.20).move_to([0, -0.70, 0])
        test_prompts = VGroup(
            *(
                MathTex(r"\square^2\ ?", font_size=34, color=MUTED).next_to(
                    survivor_cards[value], DOWN, buff=0.28
                )
                for value in survivor_order
            )
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                grid_group,
                even_rule,
                odd_rule,
                survivor_note,
                *residue_badges.values(),
                *reject_lines.values(),
            ),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Write(square_condition), run_time=0.45)
        self.play(
            LaggedStart(*(FadeIn(survivor_cards[value]) for value in survivor_order), lag_ratio=0.15),
            run_time=0.8,
        )
        self.play(FadeIn(test_prompts), FadeIn(gate_note), run_time=0.65)
        self.wait(0.35)

        # Beat 20 place_first_square_bracket: reject 96669 with an exact consecutive-square interval.
        self.next_beat("place_first_square_bracket")
        next_title = self.stage_title("96669 落在兩個相鄰平方之間")
        first_focus = self.candidate_card(96669, width=3.05, height=1.05, font_size=43).move_to(
            [0, 1.65, 0]
        )
        first_interval = self.square_interval(310, 96669, 311)
        first_reject = self.strike(first_focus, stroke_width=4.5)
        not_square_one = VGroup(
            MathTex(r"96669\ne k^2", font_size=40, color=CORAL),
            label("相鄰平方之間沒有另一個平方", 23, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.18).move_to([0, -2.40, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(square_condition, gate_note, test_prompts, *survivor_cards.values()),
            run_time=0.55,
        )
        stage_title = next_title
        self.play(FadeIn(first_focus), run_time=0.35)
        self.play(Create(first_interval[0]), FadeIn(first_interval[1], first_interval[2]), run_time=0.65)
        self.play(FadeIn(first_interval[3], first_interval[4]), run_time=0.55)

        # Beat 21 bracket_first_false: continue at a settled semantic boundary.
        self.next_beat("bracket_first_false")
        self.play(FadeIn(first_interval[5]), run_time=0.4)
        self.play(Write(first_interval[6]), run_time=0.55)
        self.play(Create(first_reject), FadeIn(not_square_one), run_time=0.65)
        self.wait(0.30)

        # Beat 22 place_second_square_bracket: apply the same exact bracket to the other false survivor.
        self.next_beat("place_second_square_bracket")
        next_title = self.stage_title("98289 也被相鄰平方夾住")
        second_focus = self.candidate_card(98289, width=3.05, height=1.05, font_size=43).move_to(
            [0, 1.65, 0]
        )
        second_interval = self.square_interval(313, 98289, 314)
        second_reject = self.strike(second_focus, stroke_width=4.5)
        not_square_two = VGroup(
            MathTex(r"98289\ne k^2", font_size=40, color=CORAL),
            label("第二個邊界候選也被排除", 23, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.18).move_to([0, -2.40, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(first_focus, first_interval, first_reject, not_square_one),
            run_time=0.55,
        )
        stage_title = next_title
        self.play(FadeIn(second_focus), run_time=0.35)
        self.play(Create(second_interval[0]), FadeIn(second_interval[1], second_interval[2]), run_time=0.65)
        self.play(FadeIn(second_interval[3], second_interval[4]), run_time=0.55)

        # Beat 23 bracket_second_false: continue at a settled semantic boundary.
        self.next_beat("bracket_second_false")
        self.play(FadeIn(second_interval[5]), run_time=0.4)
        self.play(Write(second_interval[6]), run_time=0.55)
        self.play(Create(second_reject), FadeIn(not_square_two), run_time=0.65)
        self.wait(0.30)

        # Beat 24 hold_middle_square_test: settle on the final unknown equality without declaring the pair.
        self.next_beat("hold_middle_square_test")
        next_title = self.stage_title("最後一張，等號先留白")
        hold_cards = {
            value: self.candidate_card(value, width=3.05, height=1.05, font_size=43).move_to(
                [x, 0.55, 0]
            )
            for value, x in zip(survivor_order, survivor_positions, strict=True)
        }
        hold_strikes = VGroup(
            self.strike(hold_cards[96669], stroke_width=4.5),
            self.strike(hold_cards[98289], stroke_width=4.5),
        )
        preanswer = MathTex(
            r"264^2", r"\;?\;", "69696", font_size=49, color=INK
        ).move_to([0, -1.15, 0])
        preanswer[1].set_color(POINT)
        question_note = label("請先完成這次乘法", 25, POINT, "BOLD").move_to(
            [0, -2.05, 0]
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(second_focus, second_interval, second_reject, not_square_two),
            run_time=0.55,
        )
        stage_title = next_title
        self.play(
            LaggedStart(*(FadeIn(hold_cards[value]) for value in survivor_order), lag_ratio=0.12),
            run_time=0.7,
        )
        self.play(Create(hold_strikes), run_time=0.55)
        self.play(Write(preanswer), FadeIn(question_note), run_time=0.7)
        self.wait(0.55)

        # Beat 25 reveal_square_equality: verify the square, unfold it, and recheck every original condition.
        self.next_beat("reveal_square_equality")
        next_title = self.stage_title("平方成立，再回到原來四個條件")
        equality = MathTex(r"264^2", "=", "69696", font_size=44, color=INK).move_to(
            [3.10, 1.75, 0]
        )
        equality[1].set_color(POINT)
        equality[2].set_color(POINT)
        final_digits = self.palindrome_row(
            ("6", "9", "6", "9", "6"),
            card_width=0.90,
            card_height=1.05,
            font_size=40,
            buff=0.13,
        ).move_to([-3.25, 0.30, 0])
        palindrome_caption = label("左右讀都相同", 24, REGION, "BOLD").next_to(
            final_digits, DOWN, buff=0.30
        )
        digit_sum_check = MathTex(
            r"6+9+6+9+6=36=6^2", font_size=35, color=INK
        ).move_to([3.10, 0.45, 0])
        second_sum_check = MathTex(
            r"3+6=9=3^2", font_size=38, color=REGION
        ).move_to([3.10, -0.48, 0])
        final_answer = MathTex(
            r"(m,n)=(36,69696)", font_size=47, color=POINT
        ).move_to([3.10, -1.65, 0])
        answer_box = SurroundingRectangle(
            final_answer, color=POINT, buff=0.17, stroke_width=3.0
        )
        equality_hold = MathTex(
            r"264^2", "=", "69696", font_size=49, color=INK
        ).move_to(preanswer)
        equality_hold[1].set_color(POINT)
        equality_hold[2].set_color(POINT)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(question_note, hold_strikes),
            Transform(preanswer, equality_hold),
            run_time=0.7,
        )
        stage_title = next_title
        self.play(Circumscribe(preanswer, color=POINT), run_time=0.65)
        self.play(
            FadeOut(preanswer, *hold_cards.values()),
            run_time=0.40,
        )

        # Beat 26 recheck_palindrome: continue at a settled semantic boundary.
        self.next_beat("recheck_palindrome")
        self.play(
            FadeIn(equality),
            FadeIn(final_digits),
            run_time=0.60,
        )
        self.play(FadeIn(palindrome_caption), run_time=0.4)
        self.play(
            Indicate(VGroup(final_digits[0], final_digits[4]), color=POINT),
            Indicate(VGroup(final_digits[1], final_digits[3]), color=BLUE),
            run_time=0.65,
        )

        # Beat 27 reveal_and_recheck_pair: continue at a settled semantic boundary.
        self.next_beat("reveal_and_recheck_pair")
        self.play(Write(digit_sum_check), run_time=0.65)
        self.play(Write(second_sum_check), run_time=0.55)
        self.play(Write(final_answer), Create(answer_box), run_time=0.75)
        self.wait(0.65)
