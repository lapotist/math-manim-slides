"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q3."""

from __future__ import annotations

from fractions import Fraction

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
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


SHARES = {
    "a": Fraction(1, 4),
    "b": Fraction(3, 20),
    "c": Fraction(7, 20),
    "d": Fraction(1, 4),
}
PAIR_TOTALS = {
    ("a", "b"): Fraction(2, 5),
    ("a", "c"): Fraction(3, 5),
    ("a", "d"): Fraction(1, 2),
}
KNOWN_C_AMOUNT = Fraction(315)
TOTAL_AMOUNT = KNOWN_C_AMOUNT / SHARES["c"]
AMOUNTS = {key: share * TOTAL_AMOUNT for key, share in SHARES.items()}
FIVE_PERCENT_AMOUNT = TOTAL_AMOUNT / 20

if sum(SHARES.values()) != 1:
    raise ValueError("shares do not form one whole pool")
if any(share <= 0 for share in SHARES.values()):
    raise ValueError("all award shares must be positive")
if any(SHARES[left] + SHARES[right] != total for (left, right), total in PAIR_TOTALS.items()):
    raise ValueError("pair-share clue check failed")
if 3 * SHARES["a"] + SHARES["b"] + SHARES["c"] + SHARES["d"] != Fraction(3, 2):
    raise ValueError("overlapping-pair sum check failed")
if TOTAL_AMOUNT != 900 or FIVE_PERCENT_AMOUNT != 45:
    raise ValueError("money scale check failed")
if AMOUNTS != {"a": 225, "b": 135, "c": 315, "d": 225}:
    raise ValueError(f"unexpected award amounts: {AMOUNTS}")


PERSONS = {
    "a": ("小公", POINT),
    "b": ("小誠", BLUE),
    "c": ("小勤", REGION),
    "d": ("小樸", PURPLE),
}


class CarloTcfs112MathQ03(CarloSlide):
    """Use overlap counting to determine four prize shares and one award."""

    lesson_id = "carlo.tcfs_112_math_gifted.q03"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def person_token(key: str, *, scale: float = 1.0) -> VGroup:
        name, color = PERSONS[key]
        frame = RoundedRectangle(
            width=1.72 * scale,
            height=0.90 * scale,
            corner_radius=0.07,
            color=color,
            stroke_width=2.6,
            fill_color=color,
            fill_opacity=0.12,
        )
        name_text = label(name, 20 * scale, color, "BOLD")
        symbol = MathTex(key, font_size=29 * scale, color=color)
        content = VGroup(name_text, symbol).arrange(RIGHT, buff=0.16 * scale)
        content.move_to(frame)
        return VGroup(frame, content)

    @classmethod
    def pair_row(cls, second_key: str, percent: int, y: float) -> VGroup:
        first = cls.person_token("a", scale=0.88)
        second = cls.person_token(second_key, scale=0.88)
        plus = MathTex("+", font_size=35, color=MUTED)
        equals = MathTex("=", font_size=35, color=MUTED)
        total = MathTex(rf"{percent}\%", font_size=39, color=CORAL)
        row = VGroup(first, plus, second, equals, total).arrange(RIGHT, buff=0.30)
        row.move_to([0, y, 0])
        return row

    @staticmethod
    def share_summary_card(
        key: str,
        percent: int,
        calculation: str,
    ) -> VGroup:
        name, color = PERSONS[key]
        frame = RoundedRectangle(
            width=3.35,
            height=1.38,
            corner_radius=0.08,
            color=color,
            stroke_width=2.3,
            fill_color=BG,
            fill_opacity=0.97,
        )
        title = VGroup(
            label(name, 21, color, "BOLD"),
            MathTex(rf"{key}={percent}\%", font_size=31, color=color),
        ).arrange(RIGHT, buff=0.18)
        detail = MathTex(calculation, font_size=27, color=MUTED)
        content = VGroup(title, detail).arrange(DOWN, buff=0.15).move_to(frame)
        return VGroup(frame, content)

    @staticmethod
    def share_segment(key: str, percent: int, total_width: float = 12.0) -> VGroup:
        name, color = PERSONS[key]
        width = total_width * percent / 100
        frame = Rectangle(
            width=width,
            height=1.22,
            color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.18,
        )
        content = VGroup(
            label(name, 18 if width < 2.0 else 21, color, "BOLD"),
            MathTex(rf"{percent}\%", font_size=26 if width < 2.0 else 31, color=color),
        ).arrange(DOWN, buff=0.08).move_to(frame)
        return VGroup(frame, content)

    @staticmethod
    def money_strip(
        key: str,
        percent: int,
        money: str,
        *,
        width: float,
        y: float,
    ) -> VGroup:
        name, color = PERSONS[key]
        frame = RoundedRectangle(
            width=width,
            height=1.02,
            corner_radius=0.06,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.17,
        )
        percent_tex = MathTex(rf"{percent}\%", font_size=37, color=color).move_to(frame)
        name_text = label(name, 24, color, "BOLD").next_to(frame, LEFT, buff=0.32)
        money_tex = MathTex(money, font_size=39, color=CORAL).next_to(frame, RIGHT, buff=0.34)
        group = VGroup(frame, percent_tex, name_text, money_tex)
        group.move_to([0, y, 0])
        return group

    @staticmethod
    def unit_block(color: str, text: str, *, scale: float = 1.0) -> VGroup:
        frame = RoundedRectangle(
            width=0.90 * scale,
            height=0.92 * scale,
            corner_radius=0.05,
            color=color,
            stroke_width=2.3,
            fill_color=color,
            fill_opacity=0.15,
        )
        value = MathTex(text, font_size=25 * scale, color=color).move_to(frame)
        return VGroup(frame, value)

    @classmethod
    def unit_row(cls, count: int, color: str, text: str, y: float, *, scale: float = 1.0) -> VGroup:
        row = VGroup(*(cls.unit_block(color, text, scale=scale) for _ in range(count)))
        row.arrange(RIGHT, buff=0.10 * scale).move_to([0.55, y, 0])
        return row

    def construct(self) -> None:
        heading = label("第 3 題｜重疊比例分獎金", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 3 頁｜影片 SlZg1LfjbrE",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: establish one shared prize pool and the known/unknown money roles.
        self.begin_beat("meet_shared_pool")
        beat_title = label("同一筆 100% 獎金，分給四個人", 35, INK, "BOLD")
        beat_title.move_to([0, 3.12, 0])
        pool = RoundedRectangle(
            width=11.8,
            height=1.35,
            corner_radius=0.08,
            color=HAIRLINE,
            stroke_width=2.8,
            fill_color=BG,
            fill_opacity=0.96,
        ).move_to([0, 1.20, 0])
        pool_label = MathTex(r"100\%", font_size=49, color=INK).move_to(pool)
        roster = VGroup(*(self.person_token(key) for key in ("a", "b", "c", "d")))
        roster.arrange(RIGHT, buff=0.55).move_to([0, -0.38, 0])
        unknowns = VGroup(
            *(MathTex(r"?\%", font_size=28, color=PERSONS[key][1]).next_to(token, DOWN, buff=0.16) for key, token in zip(("a", "b", "c", "d"), roster))
        )
        known_c = VGroup(
            label("已知", 20, CORAL, "BOLD"),
            MathTex("315", font_size=38, color=CORAL),
        ).arrange(RIGHT, buff=0.16).move_to([1.30, -2.10, 0])
        ask_d = VGroup(
            label("要求", 20, PURPLE, "BOLD"),
            MathTex("?", font_size=38, color=PURPLE),
        ).arrange(RIGHT, buff=0.16).move_to([3.18, -2.10, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), Create(pool), Write(pool_label), run_time=0.9)
        self.play(LaggedStart(*(FadeIn(token) for token in roster), lag_ratio=0.15), run_time=0.9)
        self.play(FadeIn(unknowns), run_time=0.5)
        self.play(TransformFromCopy(roster[2], known_c), TransformFromCopy(roster[3], ask_d), run_time=0.75)
        self.wait(0.35)

        # Beat 02: reveal the three overlapping pair clues one at a time.
        self.next_beat("reveal_pair_clues")
        next_title = label("三條線索，都重複出現小公", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        row_ab = self.pair_row("b", 40, 1.45)
        row_ac = self.pair_row("c", 60, 0.15)
        row_ad = self.pair_row("d", 50, -1.15)
        pair_rows = VGroup(row_ab, row_ac, row_ad)
        repeat_note = label("小公出現 3 次；其餘各 1 次", 27, POINT, "BOLD")
        repeat_note.move_to([0, -2.42, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(pool), FadeOut(pool_label), FadeOut(roster), FadeOut(unknowns), FadeOut(known_c), FadeOut(ask_d), run_time=0.55)
        self.play(FadeIn(row_ab), run_time=0.6)
        self.play(FadeIn(row_ac), run_time=0.6)
        self.play(FadeIn(row_ad), run_time=0.6)
        self.play(
            Circumscribe(row_ab[0], color=POINT),
            Circumscribe(row_ac[0], color=POINT),
            Circumscribe(row_ad[0], color=POINT),
            run_time=0.7,
        )
        self.play(FadeIn(repeat_note), run_time=0.45)
        self.wait(0.35)

        # Beat 03: turn visible occurrence counts into one aggregate equation.
        self.next_beat("stack_three_clues")
        next_title = label("把三條雙人比例一起相加", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        aggregate = MathTex(
            "3a", "+", "b", "+", "c", "+", "d", "=", r"150\%",
            font_size=43,
            color=INK,
        )
        aggregate[0].set_color(POINT)
        aggregate[2].set_color(BLUE)
        aggregate[4].set_color(REGION)
        aggregate[6].set_color(PURPLE)
        aggregate[8].set_color(CORAL)
        aggregate.move_to([3.05, -1.15, 0])
        rhs_sum = MathTex(r"40\%+60\%+50\%=150\%", font_size=31, color=CORAL)
        rhs_sum.move_to([3.05, 0.18, 0])
        occurrence_note = label("出現次數：小公 3 次；其餘各 1 次", 23, MUTED, "MEDIUM")
        occurrence_note.move_to([3.05, 1.32, 0])
        compact_pair_rows = pair_rows.copy().scale(0.80).move_to([-3.55, 0.15, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(repeat_note), run_time=0.4)
        self.play(Transform(pair_rows, compact_pair_rows), run_time=0.65)
        self.play(FadeIn(occurrence_note), Write(rhs_sum), run_time=0.65)
        self.play(Write(aggregate), run_time=0.9)
        self.play(Indicate(aggregate[0], color=POINT), Indicate(aggregate[8], color=CORAL), run_time=0.65)
        self.wait(0.35)

        # Beat 04: subtract one complete pool at the token level first.
        self.next_beat("remove_one_whole_pool")
        next_title = label("移去一整池，只剩兩份小公", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        counted_tokens = VGroup(
            self.person_token("a", scale=0.76),
            self.person_token("a", scale=0.76),
            self.person_token("a", scale=0.76),
            self.person_token("b", scale=0.76),
            self.person_token("c", scale=0.76),
            self.person_token("d", scale=0.76),
        ).arrange(RIGHT, buff=0.17).move_to([-0.65, 1.18, 0])
        counted_total = MathTex(r"=150\%", font_size=38, color=CORAL).next_to(counted_tokens, RIGHT, buff=0.28)
        whole_tokens = VGroup(*(self.person_token(key, scale=0.76) for key in ("a", "b", "c", "d")))
        whole_tokens.arrange(RIGHT, buff=0.17).move_to([-0.65, -0.32, 0])
        minus = MathTex("-", font_size=46, color=MUTED).next_to(whole_tokens, LEFT, buff=0.28)
        whole_total = MathTex(r"=100\%", font_size=38, color=MUTED).next_to(whole_tokens, RIGHT, buff=0.28)
        subtract_line = Line([-5.0, -1.05, 0], [5.0, -1.05, 0], color=HAIRLINE, stroke_width=2)
        result_tokens = VGroup(self.person_token("a", scale=0.88), self.person_token("a", scale=0.88))
        result_tokens.arrange(RIGHT, buff=0.30).move_to([0, -1.62, 0])
        result_equation = MathTex("2a", "=", r"50\%", font_size=51, color=INK)
        result_equation[0].set_color(POINT)
        result_equation[2].set_color(CORAL)
        result_equation.move_to([0, -2.50, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(pair_rows), FadeOut(rhs_sum), FadeOut(occurrence_note), FadeOut(aggregate), run_time=0.55)
        self.play(FadeIn(counted_tokens), Write(counted_total), run_time=0.65)
        self.play(FadeIn(whole_tokens), Write(minus), Write(whole_total), Create(subtract_line), run_time=0.7)
        self.play(
            Transform(counted_tokens[0], result_tokens[0]),
            Transform(counted_tokens[1], result_tokens[1]),
            FadeOut(VGroup(*counted_tokens[2:])),
            FadeOut(whole_tokens),
            FadeOut(minus),
            FadeOut(counted_total),
            FadeOut(whole_total),
            FadeOut(subtract_line),
            run_time=1.0,
        )
        remaining_a = VGroup(counted_tokens[0], counted_tokens[1])
        self.play(Write(result_equation), run_time=0.65)
        self.wait(0.35)

        # Beat 05: split the remaining 50 percent equally between two a tokens.
        self.next_beat("split_fifty_between_two_a")
        next_title = label("兩份相同的小公，平分 50%", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        half_left = Rectangle(
            width=3.25,
            height=1.18,
            color=POINT,
            stroke_width=2.6,
            fill_color=POINT,
            fill_opacity=0.17,
        ).move_to([-1.63, -0.05, 0])
        half_right = half_left.copy().move_to([1.63, -0.05, 0])
        half_labels = VGroup(
            MathTex(r"25\%", font_size=43, color=POINT).move_to(half_left),
            MathTex(r"25\%", font_size=43, color=POINT).move_to(half_right),
        )
        split_tokens = VGroup(self.person_token("a", scale=0.86), self.person_token("a", scale=0.86))
        split_tokens[0].move_to([-1.63, 1.22, 0])
        split_tokens[1].move_to([1.63, 1.22, 0])
        split_line = Line([0, -0.64, 0], [0, 0.54, 0], color=INK, stroke_width=3)
        a_result = MathTex("a", "=", r"25\%", font_size=54, color=INK)
        a_result[0].set_color(POINT)
        a_result[2].set_color(POINT)
        a_result.move_to([0, -1.72, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(result_equation), run_time=0.4)
        self.play(Transform(remaining_a[0], split_tokens[0]), Transform(remaining_a[1], split_tokens[1]), run_time=0.75)
        self.play(Create(half_left), Create(half_right), Create(split_line), run_time=0.7)
        self.play(Write(half_labels), run_time=0.55)
        self.play(Write(a_result), run_time=0.6)
        self.wait(0.35)

        # Beat 06: recover and check all four positive shares.
        self.next_beat("recover_four_shares")
        next_title = label("回代三條線索，四段剛好拼成 100%", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        share_cards = VGroup(
            self.share_summary_card("a", 25, r"a=25\%"),
            self.share_summary_card("b", 15, r"40-25=15"),
            self.share_summary_card("c", 35, r"60-25=35"),
            self.share_summary_card("d", 25, r"50-25=25"),
        ).arrange(RIGHT, buff=0.27).move_to([0, 1.25, 0])
        segments = VGroup(
            self.share_segment("a", 25),
            self.share_segment("b", 15),
            self.share_segment("c", 35),
            self.share_segment("d", 25),
        ).arrange(RIGHT, buff=0).move_to([0, -0.62, 0])
        sum_check = MathTex("25", "+", "15", "+", "35", "+", "25", "=", r"100\%", font_size=42, color=INK)
        sum_check[0].set_color(POINT)
        sum_check[2].set_color(BLUE)
        sum_check[4].set_color(REGION)
        sum_check[6].set_color(PURPLE)
        sum_check[8].set_color(INK)
        sum_check.move_to([0, -2.20, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(
            FadeOut(remaining_a),
            FadeOut(half_left),
            FadeOut(half_right),
            FadeOut(half_labels),
            FadeOut(split_line),
            FadeOut(a_result),
            run_time=0.5,
        )
        self.play(FadeIn(share_cards[0]), run_time=0.45)
        self.play(FadeIn(share_cards[1]), run_time=0.45)
        self.play(FadeIn(share_cards[2]), run_time=0.45)
        self.play(FadeIn(share_cards[3]), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(segment) for segment in segments), lag_ratio=0.14), run_time=0.85)
        self.play(Write(sum_check), run_time=0.7)
        self.wait(0.35)

        # Beat 07: anchor the percentage scale to the known 315 dollars.
        self.next_beat("anchor_known_money")
        next_title = label("小勤的 35% 是 315 元", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        c_strip = self.money_strip("c", 35, "315", width=7.0, y=0.72)
        d_strip = self.money_strip("d", 25, "?", width=5.0, y=-0.78)
        scale_question = label("同一比例尺：35% 要怎麼縮成 25%？", 27, MUTED, "MEDIUM")
        scale_question.move_to([0, -2.18, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(share_cards), FadeOut(sum_check), run_time=0.45)
        self.play(TransformFromCopy(segments[2], c_strip), TransformFromCopy(segments[3], d_strip), FadeOut(segments), run_time=0.85)
        self.play(FadeIn(scale_question), run_time=0.5)
        self.play(Indicate(c_strip[3], color=CORAL), Indicate(d_strip[1], color=PURPLE), run_time=0.6)
        self.wait(0.35)

        # Beat 08: decompose both percentages into equal five-percent units.
        self.next_beat("group_into_five_percent_units")
        next_title = label("把兩段都切成 5% 等份", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        c_units = self.unit_row(7, REGION, r"5\%", 0.78)
        d_units = self.unit_row(5, PURPLE, r"5\%", -0.78)
        c_name = label("小勤", 25, REGION, "BOLD").move_to([-4.75, 0.78, 0])
        d_name = label("小樸", 25, PURPLE, "BOLD").move_to([-4.75, -0.78, 0])
        c_known = MathTex("315", font_size=38, color=CORAL).move_to([5.05, 0.78, 0])
        d_unknown = MathTex("?", font_size=38, color=PURPLE).move_to([4.12, -0.78, 0])
        unit_equations = VGroup(
            MathTex(r"35\%=7\cdot5\%", font_size=35, color=REGION),
            MathTex(r"25\%=5\cdot5\%", font_size=35, color=PURPLE),
        ).arrange(DOWN, buff=0.22).move_to([0, -2.22, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(c_strip), FadeOut(d_strip), FadeOut(scale_question), run_time=0.5)
        self.play(FadeIn(c_name), FadeIn(d_name), FadeIn(c_known), FadeIn(d_unknown), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(unit) for unit in c_units), lag_ratio=0.10), run_time=0.8)
        self.play(LaggedStart(*(FadeIn(unit) for unit in d_units), lag_ratio=0.10), run_time=0.7)
        self.play(Write(unit_equations), run_time=0.75)
        self.wait(0.35)

        # Beat 09: find one unit, then settle five equal values without multiplying.
        self.next_beat("settle_unit_value_preanswer")
        next_title = label("每一個 5% 方塊值 45 元", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        c_units_money = self.unit_row(7, REGION, "45", 0.78)
        d_units_money = self.unit_row(5, PURPLE, "45", -0.78)
        unit_value = MathTex("315", r"\div", "7", "=", "45", font_size=42, color=INK)
        unit_value[0].set_color(CORAL)
        unit_value[4].set_color(REGION)
        unit_value.move_to([0, -2.05, 0])
        preanswer = MathTex("5", r"\cdot", "45", font_size=47, color=PURPLE)
        preanswer.move_to([4.15, -2.05, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(unit_equations), run_time=0.4)
        self.play(Write(unit_value), run_time=0.65)
        self.play(Transform(c_units, c_units_money), run_time=0.8)
        self.play(Transform(d_units, d_units_money), FadeOut(d_unknown), run_time=0.8)
        self.play(Write(preanswer), run_time=0.55)
        self.play(Indicate(d_units, color=PURPLE), run_time=0.55)
        self.wait(0.45)

        # Beat 10: only now multiply the five settled unit values.
        self.next_beat("reveal_xiaopu_award")
        next_title = label("五個等份收成小樸的獎金", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        final_units = self.unit_row(5, PURPLE, "45", 0.65, scale=1.12)
        final_frame = SurroundingRectangle(final_units, color=PURPLE, buff=0.18, stroke_width=3)
        final_label = label("小樸的 25%", 27, PURPLE, "BOLD").next_to(final_frame, UP, buff=0.22)
        answer = MathTex("5", r"\cdot", "45", "=", "225", font_size=57, color=INK)
        answer[0].set_color(PURPLE)
        answer[2].set_color(PURPLE)
        answer[4].set_color(CORAL)
        answer.move_to([0, -1.12, 0])
        check = MathTex("225", "+", "135", "+", "315", "+", "225", "=", "900", font_size=37, color=INK)
        check[0].set_color(POINT)
        check[2].set_color(BLUE)
        check[4].set_color(REGION)
        check[6].set_color(PURPLE)
        check.move_to([0, -2.22, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        self.play(
            FadeOut(c_units),
            FadeOut(c_name),
            FadeOut(c_known),
            FadeOut(d_name),
            FadeOut(unit_value),
            FadeOut(preanswer),
            run_time=0.55,
        )
        self.play(Transform(d_units, final_units), run_time=0.9)
        self.play(Create(final_frame), FadeIn(final_label), run_time=0.55)
        self.play(Write(answer), run_time=0.7)
        self.play(Write(check), Circumscribe(answer[4], color=CORAL), run_time=0.75)
        self.wait(0.45)
