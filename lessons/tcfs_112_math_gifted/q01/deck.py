"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q1."""

from __future__ import annotations

from itertools import permutations

from carlo_manim import (
    BG,
    BLUE,
    CORAL,
    INK,
    MUTED,
    POINT,
    PURPLE,
    REGION,
    CarloSlide,
    label,
)
from manim import (
    Circle,
    Circumscribe,
    Create,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    MathTex,
    NumberLine,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


TARGET_SUM = 15
TARGET_PRODUCT = 80
SIGNED_PROGRESSIONS = {
    distance: (5 - distance, 5, 5 + distance) for distance in (-3, 3)
}
DIGIT_SET = (2, 5, 8)
PERMUTATION_VALUES = tuple(
    sorted(int("".join(str(digit) for digit in order)) for order in permutations(DIGIT_SET))
)

if any(sum(terms) != TARGET_SUM for terms in SIGNED_PROGRESSIONS.values()):
    raise ValueError("arithmetic-progression sum check failed")
if any(
    terms[0] * terms[1] * terms[2] != TARGET_PRODUCT
    for terms in SIGNED_PROGRESSIONS.values()
):
    raise ValueError("arithmetic-progression product check failed")
if {tuple(sorted(terms)) for terms in SIGNED_PROGRESSIONS.values()} != {DIGIT_SET}:
    raise ValueError("signed distances do not give the same digit set")
if PERMUTATION_VALUES != (258, 285, 528, 582, 825, 852):
    raise ValueError(f"unexpected permutation values: {PERMUTATION_VALUES}")
if max(PERMUTATION_VALUES) != 852 or PERMUTATION_VALUES.count(852) != 1:
    raise ValueError("852 must be the unique maximum")
if (8 - 5) * (100 - 10) != 270 or (5 - 2) * (10 - 1) != 27:
    raise ValueError("place-value swap checks failed")


class CarloTcfs112MathQ01(CarloSlide):
    """Find the three terms, then order the known digits by place value."""

    lesson_id = "carlo.tcfs_112_math_gifted.q01"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def base_number_line(*, y: float = 0.55, length: float = 10.8) -> VGroup:
        line = NumberLine(
            x_range=[0, 10, 1],
            length=length,
            include_ticks=True,
            include_numbers=False,
            color=MUTED,
            stroke_width=2.4,
            tick_size=0.09,
        ).move_to([0, y, 0])
        anchors = VGroup(
            *(
                MathTex(str(value), font_size=25, color=MUTED).next_to(
                    line.n2p(value), DOWN, buff=0.20
                )
                for value in (0, 5, 10)
            )
        )
        return VGroup(line, anchors)

    @staticmethod
    def term_marker(
        line: NumberLine,
        value: float,
        text: str,
        color: str,
        *,
        label_size: float = 39,
    ) -> VGroup:
        dot = Dot(line.n2p(value), radius=0.135, color=color).set_z_index(4)
        halo = Circle(
            radius=0.235,
            color=color,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.72,
        ).move_to(dot).set_z_index(3)
        value_label = MathTex(text, font_size=label_size, color=color)
        value_label.next_to(dot, UP, buff=0.20).set_z_index(5)
        return VGroup(dot, halo, value_label)

    @staticmethod
    def spacing_guides(
        line: NumberLine,
        left_value: float,
        middle_value: float,
        right_value: float,
        text: str,
    ) -> VGroup:
        y_shift = UP * 0.72
        left_arrow = DoubleArrow(
            line.n2p(left_value) + y_shift,
            line.n2p(middle_value) + y_shift,
            buff=0.14,
            tip_length=0.12,
            stroke_width=2.4,
            color=PURPLE,
        )
        right_arrow = DoubleArrow(
            line.n2p(middle_value) + y_shift,
            line.n2p(right_value) + y_shift,
            buff=0.14,
            tip_length=0.12,
            stroke_width=2.4,
            color=PURPLE,
        )
        left_label = MathTex(text, font_size=27, color=PURPLE).next_to(
            left_arrow, UP, buff=0.06
        )
        right_label = MathTex(text, font_size=27, color=PURPLE).next_to(
            right_arrow, UP, buff=0.06
        )
        return VGroup(left_arrow, right_arrow, left_label, right_label)

    @staticmethod
    def digit_card(digit: str, color: str, *, scale: float = 1.0) -> VGroup:
        frame = RoundedRectangle(
            width=1.10 * scale,
            height=1.30 * scale,
            corner_radius=0.07,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.13,
        )
        glyph = MathTex(digit, font_size=54 * scale, color=color).move_to(frame)
        frame.set_z_index(2)
        glyph.set_z_index(3)
        return VGroup(frame, glyph)

    @staticmethod
    def place_slot(name: str, weight: int, color: str, x: float) -> VGroup:
        slot = RoundedRectangle(
            width=1.62,
            height=1.78,
            corner_radius=0.08,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.96,
        )
        name_label = label(name, 25, color, "BOLD").next_to(slot, UP, buff=0.16)
        weight_tex = MathTex(rf"\times {weight}", font_size=31, color=MUTED)
        weight_tex.next_to(slot, DOWN, buff=0.14)
        group = VGroup(slot, name_label, weight_tex).move_to([x, -0.30, 0])
        return group

    def construct(self) -> None:
        heading = label("第 1 題｜三個等距數排成最大值", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 1 頁｜影片 GGVENizPImM",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: one concrete motion makes the fixed middle term visible.
        self.begin_beat("find_middle_term")
        beat_title = label("三個等差數，先找中間", 35, INK, "BOLD")
        beat_title.move_to([0, 3.12, 0])
        number_line_group = self.base_number_line()
        number_line = number_line_group[0]
        left_marker = self.term_marker(number_line, 4, "4", BLUE)
        middle_marker = self.term_marker(number_line, 5, "5", POINT)
        right_marker = self.term_marker(number_line, 6, "6", REGION)
        guides = self.spacing_guides(number_line, 4, 5, 6, "1")
        sum_line = MathTex("4", "+", "5", "+", "6", "=", "15", font_size=49, color=INK)
        sum_line[0].set_color(BLUE)
        sum_line[2].set_color(POINT)
        sum_line[4].set_color(REGION)
        sum_line[6].set_color(POINT)
        sum_line.move_to([0, -1.35, 0])
        center_note = VGroup(
            label("左右等距移動，中間仍是三數的平均", 27, MUTED, "MEDIUM"),
            MathTex(r"15\div3=5", font_size=53, color=POINT),
        ).arrange(DOWN, buff=0.22).move_to([0, -2.05, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), Create(number_line), FadeIn(number_line_group[1]), run_time=0.9)
        self.play(
            LaggedStart(FadeIn(left_marker), FadeIn(middle_marker), FadeIn(right_marker), lag_ratio=0.18),
            Create(guides),
            Write(sum_line),
            run_time=0.9,
        )
        target_left = self.term_marker(number_line, 3, "3", BLUE)
        target_right = self.term_marker(number_line, 7, "7", REGION)
        target_guides = self.spacing_guides(number_line, 3, 5, 7, "2")
        target_sum = MathTex("3", "+", "5", "+", "7", "=", "15", font_size=49, color=INK)
        target_sum[0].set_color(BLUE)
        target_sum[2].set_color(POINT)
        target_sum[4].set_color(REGION)
        target_sum[6].set_color(POINT)
        target_sum.move_to(sum_line)
        self.play(
            Transform(left_marker[0], target_left[0]),
            Transform(left_marker[1], target_left[1]),
            Succession(FadeOut(left_marker[2]), FadeIn(target_left[2])),
            Transform(right_marker[0], target_right[0]),
            Transform(right_marker[1], target_right[1]),
            Succession(FadeOut(right_marker[2]), FadeIn(target_right[2])),
            Transform(guides[0], target_guides[0]),
            Transform(guides[1], target_guides[1]),
            Succession(
                FadeOut(VGroup(guides[2], guides[3])),
                FadeIn(VGroup(target_guides[2], target_guides[3])),
            ),
            Succession(FadeOut(sum_line), FadeIn(target_sum)),
            run_time=1.25,
        )
        self.play(FadeIn(center_note), Indicate(middle_marker[2], color=POINT), run_time=0.75)
        self.wait(0.35)

        # Beat 02: the product condition contains the only substantial algebra.
        self.next_beat("solve_common_distance")
        next_title = label("乘積只要找出共同距離", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        distance_note = VGroup(
            MathTex(r"d\ge0", font_size=35, color=PURPLE),
            label("表示兩側到 5 的距離", 27, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.24).move_to([0, 1.92, 0])
        product_line = MathTex(
            "(5-d)", r"\cdot", "5", r"\cdot", "(5+d)", "=", "80",
            font_size=50,
            color=INK,
        ).move_to([0, 0.86, 0])
        product_line[0].set_color(BLUE)
        product_line[2].set_color(POINT)
        product_line[4].set_color(REGION)
        product_line[6].set_color(CORAL)
        divide_line = MathTex("(5-d)(5+d)", "=", "16", font_size=47, color=INK)
        divide_line[0].set_color(PURPLE)
        divide_line.move_to([0, -0.16, 0])
        square_line = MathTex("25-d^2", "=", "16", font_size=47, color=INK)
        square_line[0].set_color(PURPLE)
        square_line.move_to([0, -1.08, 0])
        distance_result = MathTex("d", "=", "3", r"\quad(d\ge0)", font_size=53, color=INK)
        distance_result[0].set_color(PURPLE)
        distance_result[2].set_color(PURPLE)
        distance_result.move_to([0, -2.15, 0])

        active_left = VGroup(left_marker[0], left_marker[1], target_left[2])
        active_right = VGroup(right_marker[0], right_marker[1], target_right[2])
        active_guides = VGroup(guides[0], guides[1], target_guides[2], target_guides[3])
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(number_line_group),
            FadeOut(active_left),
            FadeOut(middle_marker),
            FadeOut(active_right),
            FadeOut(active_guides),
            FadeOut(target_sum),
            FadeOut(center_note),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(FadeIn(distance_note), Write(product_line), run_time=0.75)
        self.play(LaggedStart(Write(divide_line), Write(square_line), lag_ratio=0.45), run_time=1.1)
        self.play(Write(distance_result), run_time=0.65)
        self.wait(0.35)

        # Beat 03: substitute once and check the original conditions.
        self.next_beat("check_digit_set")
        next_title = label("代回並核對原條件", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        cards = VGroup(
            self.digit_card("2", BLUE, scale=0.96),
            self.digit_card("5", POINT, scale=0.96),
            self.digit_card("8", REGION, scale=0.96),
        ).arrange(RIGHT, buff=0.34).move_to([0, 0.48, 0])
        checks = VGroup(
            MathTex("2+5+8=15", font_size=43, color=POINT),
            MathTex(r"2\cdot5\cdot8=80", font_size=43, color=CORAL),
        ).arrange(DOWN, buff=0.40).move_to([0, -1.55, 0])

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(distance_note),
            FadeOut(product_line),
            FadeOut(divide_line),
            FadeOut(square_line),
            FadeOut(distance_result),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(LaggedStart(*(FadeIn(card) for card in cards), lag_ratio=0.16), run_time=0.75)
        self.play(FadeIn(checks), run_time=0.75)
        self.wait(0.35)

        # Beat 04: known digits only need the familiar place-value rule.
        self.next_beat("order_by_place_value")
        next_title = label("排最大值：大數放大位值", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        hundreds = self.place_slot("百位", 100, POINT, -2.30)
        tens = self.place_slot("十位", 10, REGION, 0)
        ones = self.place_slot("個位", 1, BLUE, 2.30)
        places = VGroup(hundreds, tens, ones)
        ordering = MathTex("8", ">", "5", ">", "2", font_size=49, color=INK)
        ordering[0].set_color(REGION)
        ordering[2].set_color(POINT)
        ordering[4].set_color(BLUE)
        ordering.move_to([0, 1.54, 0])

        self.play(self.title_change(beat_title, next_title), FadeOut(checks), run_time=0.6)
        beat_title = next_title
        self.play(LaggedStart(*(FadeIn(place) for place in places), lag_ratio=0.15), Write(ordering), run_time=0.8)
        self.play(
            cards[2].animate.move_to(hundreds[0]),
            cards[1].animate.move_to(tens[0]),
            cards[0].animate.move_to(ones[0]),
            run_time=1.0,
        )
        self.wait(0.4)

        # Beat 05: join the already ordered cards and state the answer.
        self.next_beat("reveal_maximum")
        next_title = label("收攏三張數字卡", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(places),
            FadeOut(ordering),
            cards[2].animate.move_to([-1.05, 0.55, 0]),
            cards[1].animate.move_to([0, 0.55, 0]),
            cards[0].animate.move_to([1.05, 0.55, 0]),
            run_time=0.85,
        )

        ordered_cards = VGroup(cards[2], cards[1], cards[0])
        answer_frame = SurroundingRectangle(ordered_cards, color=POINT, buff=0.18, stroke_width=3)
        answer_label = label("最大三位數", 28, POINT, "BOLD").next_to(answer_frame, UP, buff=0.22)
        place_expansion = MathTex(
            "8", r"\cdot100", "+", "5", r"\cdot10", "+", "2", "=", "852",
            font_size=49,
            color=INK,
        )
        place_expansion[0].set_color(REGION)
        place_expansion[3].set_color(POINT)
        place_expansion[6].set_color(BLUE)
        place_expansion[8].set_color(POINT)
        place_expansion.move_to([0, -1.42, 0])
        closing = label("先找中間與距離，再由大到小排列", 27, MUTED, "MEDIUM")
        closing.move_to([0, -2.42, 0])

        self.play(Create(answer_frame), FadeIn(answer_label), run_time=0.55)
        self.play(FadeIn(place_expansion), run_time=0.75)
        self.play(FadeIn(closing), Circumscribe(place_expansion[8], color=POINT), run_time=0.7)
        self.wait(0.45)
