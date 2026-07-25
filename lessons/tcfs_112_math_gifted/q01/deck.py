"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q1."""

from __future__ import annotations

from itertools import permutations

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
    Circle,
    Circumscribe,
    Create,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    Rectangle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Swap,
    Transform,
    TransformFromCopy,
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
    """Find the progression through symmetric motion, then maximize its numeral."""

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
    def product_card(
        distance: str,
        expression: str,
        color: str,
        *,
        width: float = 3.65,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=1.22,
            corner_radius=0.08,
            color=color,
            stroke_width=2.2,
            fill_color=BG,
            fill_opacity=0.96,
        )
        distance_tex = MathTex(rf"d={distance}", font_size=31, color=color)
        product_tex = MathTex(expression, font_size=33, color=INK)
        content = VGroup(distance_tex, product_tex).arrange(DOWN, buff=0.13)
        content.move_to(frame)
        return VGroup(frame, content)

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
        return VGroup(frame, glyph)

    @staticmethod
    def progression_row(distance: int, values: tuple[int, int, int], y: float) -> VGroup:
        distance_tex = MathTex(rf"d={distance}", font_size=39, color=PURPLE)
        cards = VGroup(
            CarloTcfs112MathQ01.digit_card(str(values[0]), BLUE, scale=0.82),
            CarloTcfs112MathQ01.digit_card(str(values[1]), POINT, scale=0.82),
            CarloTcfs112MathQ01.digit_card(str(values[2]), REGION, scale=0.82),
        ).arrange(RIGHT, buff=0.24)
        row = VGroup(distance_tex, cards).arrange(RIGHT, buff=0.62)
        row.move_to([0, y, 0])
        return row

    @staticmethod
    def place_column(name: str, weight: int, color: str, x: float) -> VGroup:
        slot = RoundedRectangle(
            width=2.55,
            height=2.15,
            corner_radius=0.08,
            color=color,
            stroke_width=2.6,
            fill_color=BG,
            fill_opacity=0.96,
        )
        name_label = label(name, 26, color, "BOLD").next_to(slot, UP, buff=0.18)
        weight_tex = MathTex(rf"\times {weight}", font_size=34, color=MUTED)
        weight_tex.next_to(slot, DOWN, buff=0.16)
        group = VGroup(slot, name_label, weight_tex).move_to([x, -0.10, 0])
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

        # Beat 01: move only the outer points while the center stays fixed.
        self.begin_beat("move_equal_spacing")
        beat_title = label("三個點保持等距，總和會怎麼變？", 35, INK, "BOLD")
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
        observation = label("左右各移一格，總和還會是 15 嗎？", 27, MUTED, "MEDIUM")
        observation.move_to([0, -2.28, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), Create(number_line), FadeIn(number_line_group[1]), run_time=0.9)
        self.play(
            LaggedStart(FadeIn(left_marker), FadeIn(middle_marker), FadeIn(right_marker), lag_ratio=0.18),
            run_time=0.9,
        )
        self.play(Create(guides), Write(sum_line), run_time=0.9)
        self.play(FadeIn(observation), run_time=0.45)

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
            Transform(left_marker, target_left),
            Transform(right_marker, target_right),
            Transform(guides, target_guides),
            Transform(sum_line, target_sum),
            run_time=1.25,
        )
        self.play(Indicate(sum_line[6], color=POINT), run_time=0.55)
        self.wait(0.35)

        # Beat 02: derive the fixed center before using the product.
        self.next_beat("lock_middle_at_five")
        next_title = label("總和就是中間數的三倍", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        generic_left = self.term_marker(number_line, 3, "m-d", BLUE, label_size=35)
        generic_middle = self.term_marker(number_line, 5, "m", POINT)
        generic_right = self.term_marker(number_line, 7, "m+d", REGION, label_size=35)
        generic_guides = self.spacing_guides(number_line, 3, 5, 7, "d")
        generic_sum = MathTex(
            "(", "m", "-", "d", ")", "+", "m", "+", "(", "m", "+", "d", ")", "=", "15",
            font_size=42,
            color=INK,
        )
        generic_sum[1].set_color(BLUE)
        generic_sum[3].set_color(PURPLE)
        generic_sum[6].set_color(POINT)
        generic_sum[9].set_color(REGION)
        generic_sum[11].set_color(PURPLE)
        generic_sum[14].set_color(POINT)
        generic_sum.move_to([0, -1.38, 0])
        middle_result = MathTex("3m", "=", "15", r"\quad\Rightarrow\quad", "m", "=", "5", font_size=45, color=INK)
        middle_result[0].set_color(POINT)
        middle_result[2].set_color(POINT)
        middle_result[4].set_color(POINT)
        middle_result[6].set_color(POINT)
        middle_result.move_to([0, -2.30, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(observation), FadeOut(sum_line), run_time=0.45)
        self.play(
            Transform(left_marker, generic_left),
            Transform(middle_marker, generic_middle),
            Transform(right_marker, generic_right),
            Transform(guides, generic_guides),
            run_time=0.9,
        )
        self.play(Write(generic_sum), run_time=0.85)
        self.play(
            Circumscribe(generic_sum[3], color=PURPLE),
            Circumscribe(generic_sum[11], color=PURPLE),
            run_time=0.7,
        )
        self.play(Write(middle_result), run_time=0.75)
        self.wait(0.35)

        # Beat 03: compare concrete products before introducing the equation.
        self.next_beat("compare_product_cases")
        next_title = label("總和固定了；哪個間距會讓積變成 80？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        case_left = self.term_marker(number_line, 4, "4", BLUE)
        case_middle = self.term_marker(number_line, 5, "5", POINT)
        case_right = self.term_marker(number_line, 6, "6", REGION)
        case_guides = self.spacing_guides(number_line, 4, 5, 6, "1")
        card_one = self.product_card("1", r"4\cdot5\cdot6=120", BLUE)
        card_two = self.product_card("2", r"3\cdot5\cdot7=105", REGION)
        target_card = self.product_card("?", r"(\cdot)\,(\cdot)\,(\cdot)=80", CORAL)
        cards = VGroup(card_one, card_two, target_card).arrange(RIGHT, buff=0.42)
        cards.move_to([0, -2.12, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(generic_sum), FadeOut(middle_result), run_time=0.5)
        self.play(
            Transform(left_marker, case_left),
            Transform(middle_marker, case_middle),
            Transform(right_marker, case_right),
            Transform(guides, case_guides),
            run_time=0.85,
        )
        self.play(FadeIn(card_one), run_time=0.55)

        case_two_left = self.term_marker(number_line, 3, "3", BLUE)
        case_two_right = self.term_marker(number_line, 7, "7", REGION)
        case_two_guides = self.spacing_guides(number_line, 3, 5, 7, "2")
        self.play(
            Transform(left_marker, case_two_left),
            Transform(right_marker, case_two_right),
            Transform(guides, case_two_guides),
            run_time=1.0,
        )
        self.play(FadeIn(card_two), run_time=0.5)
        self.play(FadeIn(target_card), run_time=0.5)
        self.play(Indicate(target_card, color=CORAL), run_time=0.6)
        self.wait(0.35)

        # Beat 04: name the distance and build the product from visible terms.
        self.next_beat("name_common_distance")
        next_title = label("把共同距離叫做 d", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        named_left = self.term_marker(number_line, 3, "5-d", BLUE, label_size=35)
        named_middle = self.term_marker(number_line, 5, "5", POINT)
        named_right = self.term_marker(number_line, 7, "5+d", REGION, label_size=35)
        named_guides = self.spacing_guides(number_line, 3, 5, 7, "d")
        product_equation = MathTex(
            "(5-d)", r"\cdot", "5", r"\cdot", "(5+d)", "=", "80",
            font_size=48,
            color=INK,
        )
        product_equation[0].set_color(BLUE)
        product_equation[2].set_color(POINT)
        product_equation[4].set_color(REGION)
        product_equation[6].set_color(CORAL)
        product_equation.move_to([0, -1.65, 0])
        pairing_note = label("先配對左右兩項", 27, PURPLE, "BOLD")
        pairing_note.move_to([0, -2.50, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(cards), run_time=0.5)
        self.play(
            Transform(left_marker, named_left),
            Transform(middle_marker, named_middle),
            Transform(right_marker, named_right),
            Transform(guides, named_guides),
            run_time=0.9,
        )
        self.play(
            TransformFromCopy(left_marker[2], product_equation[0]),
            TransformFromCopy(middle_marker[2], product_equation[2]),
            TransformFromCopy(right_marker[2], product_equation[4]),
            run_time=0.75,
        )
        self.play(Write(VGroup(product_equation[1], product_equation[3], product_equation[5], product_equation[6])), run_time=0.65)
        self.play(FadeIn(pairing_note), run_time=0.45)
        self.wait(0.35)

        # Beat 05: expose the cancellation inside the symmetric factor pair.
        self.next_beat("pair_symmetric_factors")
        next_title = label("左右因子展開，中間項剛好相消", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        expansion = MathTex(
            "(5-d)(5+d)", "=", "25", "+", "5d", "-", "5d", "-", "d^2",
            font_size=44,
            color=INK,
        )
        expansion[0].set_color(PURPLE)
        expansion[4].set_color(BLUE)
        expansion[6].set_color(REGION)
        expansion[8].set_color(PURPLE)
        expansion.move_to([0, 0.32, 0])
        cross_left = Line(
            expansion[4].get_corner(LEFT + DOWN),
            expansion[4].get_corner(RIGHT + UP),
            color=CORAL,
            stroke_width=4,
        )
        cross_right = Line(
            expansion[6].get_corner(LEFT + DOWN),
            expansion[6].get_corner(RIGHT + UP),
            color=CORAL,
            stroke_width=4,
        )
        pair_result = MathTex("(5-d)(5+d)", "=", "25-d^2", font_size=45, color=INK)
        pair_result[0].set_color(PURPLE)
        pair_result[2].set_color(PURPLE)
        pair_result.move_to([0, -0.92, 0])
        reduced_product = MathTex("5", "(", "25-d^2", ")", "=", "80", font_size=50, color=INK)
        reduced_product[0].set_color(POINT)
        reduced_product[2].set_color(PURPLE)
        reduced_product[5].set_color(CORAL)
        reduced_product.move_to([0, -2.03, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(
            FadeOut(pairing_note),
            FadeOut(number_line_group),
            FadeOut(left_marker),
            FadeOut(middle_marker),
            FadeOut(right_marker),
            FadeOut(guides),
            product_equation.animate.move_to([0, 1.65, 0]),
            run_time=0.7,
        )
        pair_frame = SurroundingRectangle(
            VGroup(product_equation[0], product_equation[4]),
            color=PURPLE,
            buff=0.18,
            stroke_width=2.5,
        )
        self.play(Create(pair_frame), run_time=0.45)
        self.play(Write(expansion), run_time=0.95)
        self.play(Create(cross_left), Create(cross_right), run_time=0.55)
        self.play(Write(pair_result), run_time=0.6)
        self.play(TransformFromCopy(pair_result[2], reduced_product[2]), Write(VGroup(reduced_product[0], reduced_product[1], reduced_product[3], reduced_product[4], reduced_product[5])), run_time=0.7)
        self.wait(0.35)

        # Beat 06: solve only for the magnitude, then return to the number line.
        self.next_beat("solve_distance_magnitude")
        next_title = label("乘積 80 決定距離的大小", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        step_one = MathTex("25-d^2", "=", "16", font_size=47, color=INK)
        step_one[0].set_color(PURPLE)
        step_one.move_to([0, 0.78, 0])
        step_two = MathTex("d^2", "=", "9", font_size=47, color=INK)
        step_two[0].set_color(PURPLE)
        step_two.move_to([0, -0.05, 0])
        step_three = MathTex(r"|d|", "=", "3", font_size=53, color=INK)
        step_three[0].set_color(PURPLE)
        step_three[2].set_color(PURPLE)
        step_three.move_to([0, -0.92, 0])
        solved_line_group = self.base_number_line(y=-2.35, length=8.8)
        solved_line = solved_line_group[0]
        solved_markers = VGroup(
            self.term_marker(solved_line, 2, "2", BLUE, label_size=34),
            self.term_marker(solved_line, 5, "5", POINT, label_size=34),
            self.term_marker(solved_line, 8, "8", REGION, label_size=34),
        )

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(
            FadeOut(product_equation),
            FadeOut(pair_frame),
            FadeOut(expansion),
            FadeOut(cross_left),
            FadeOut(cross_right),
            FadeOut(pair_result),
            reduced_product.animate.move_to([0, 1.72, 0]),
            run_time=0.7,
        )
        self.play(Write(step_one), run_time=0.6)
        self.play(Write(step_two), run_time=0.55)
        self.play(Write(step_three), run_time=0.6)
        self.play(Create(solved_line), FadeIn(solved_line_group[1]), run_time=0.6)
        self.play(LaggedStart(*(FadeIn(marker) for marker in solved_markers), lag_ratio=0.16), run_time=0.75)
        self.wait(0.35)

        # Beat 07: retain both algebraic signs and identify the same digit set.
        self.next_beat("check_both_signs")
        next_title = label("d 的正負，只會交換左右順序", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        positive_row = self.progression_row(3, (2, 5, 8), 0.88)
        negative_row = self.progression_row(-3, (8, 5, 2), -0.65)
        swap_label = VGroup(
            DoubleArrow(
                LEFT * 0.9,
                RIGHT * 0.9,
                color=PURPLE,
                stroke_width=3,
                tip_length=0.16,
            ),
            label("左右互換", 22, PURPLE, "BOLD"),
        ).arrange(DOWN, buff=0.08).move_to([4.68, 0.08, 0])
        digit_set = MathTex(r"\{2,5,8\}", font_size=50, color=INK)
        digit_set.move_to([4.70, -1.15, 0])
        checks = VGroup(
            MathTex("2+5+8=15", font_size=39, color=POINT),
            MathTex(r"2\cdot5\cdot8=80", font_size=39, color=CORAL),
        ).arrange(RIGHT, buff=1.2).move_to([0, -2.35, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(
            FadeOut(reduced_product),
            FadeOut(step_one),
            FadeOut(step_two),
            FadeOut(step_three),
            FadeOut(solved_line_group),
            FadeOut(solved_markers),
            run_time=0.55,
        )
        self.play(FadeIn(positive_row), run_time=0.65)
        self.play(FadeIn(negative_row), run_time=0.65)
        self.play(FadeIn(swap_label), Write(digit_set), run_time=0.65)
        self.play(Write(checks), run_time=0.75)
        self.wait(0.35)

        # Beat 08: prove that the largest digit must occupy the hundreds place.
        self.next_beat("place_largest_hundreds")
        next_title = label("8 若不在百位，交換一定會變大", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        high_pedestal = RoundedRectangle(
            width=2.65,
            height=1.80,
            corner_radius=0.08,
            color=POINT,
            stroke_width=2.5,
        ).move_to([-2.35, 0.45, 0])
        low_pedestal = RoundedRectangle(
            width=2.65,
            height=1.80,
            corner_radius=0.08,
            color=MUTED,
            stroke_width=2.5,
        ).move_to([2.35, 0.45, 0])
        high_weight = MathTex(r"\times100", font_size=38, color=POINT).next_to(high_pedestal, DOWN, buff=0.18)
        low_weight = MathTex(r"\times w", font_size=38, color=MUTED).next_to(low_pedestal, DOWN, buff=0.18)
        x_card = self.digit_card("x", MUTED, scale=0.92).move_to(high_pedestal)
        eight_card = self.digit_card("8", REGION, scale=0.92).move_to(low_pedestal)
        conditions = MathTex(r"x\in\{2,5\}", r"\qquad", r"w\in\{10,1\}", font_size=36, color=INK)
        conditions[0].set_color(MUTED)
        conditions[2].set_color(MUTED)
        conditions.move_to([0, -1.58, 0])
        gain = MathTex("(8-x)", "(100-w)", ">", "0", font_size=47, color=INK)
        gain[0].set_color(REGION)
        gain[1].set_color(POINT)
        gain[3].set_color(POINT)
        gain.move_to([0, -2.42, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(FadeOut(positive_row), FadeOut(negative_row), FadeOut(swap_label), FadeOut(digit_set), FadeOut(checks), run_time=0.55)
        self.play(Create(high_pedestal), Create(low_pedestal), Write(high_weight), Write(low_weight), run_time=0.7)
        self.play(FadeIn(x_card), FadeIn(eight_card), Write(conditions), run_time=0.65)
        self.play(Swap(x_card, eight_card), run_time=1.0)
        self.play(Write(gain), run_time=0.65)
        self.play(Circumscribe(eight_card, color=POINT), run_time=0.65)
        self.wait(0.35)

        # Beat 09: settle all three separated place-value columns without joining them.
        self.next_beat("settle_remaining_places")
        next_title = label("百位固定 8；再比較十位和個位", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        hundreds = self.place_column("百位", 100, POINT, -4.15)
        tens = self.place_column("十位", 10, REGION, 0)
        ones = self.place_column("個位", 1, BLUE, 4.15)
        places = VGroup(hundreds, tens, ones)
        placed_eight = self.digit_card("8", REGION, scale=0.88).move_to(hundreds[0])
        placed_five = self.digit_card("5", POINT, scale=0.88).move_to(tens[0])
        placed_two = self.digit_card("2", BLUE, scale=0.88).move_to(ones[0])
        forward_value = MathTex(r"5\cdot10+2", "=", "52", font_size=39, color=INK)
        forward_value[0].set_color(REGION)
        forward_value[2].set_color(REGION)
        reverse_value = MathTex(r"2\cdot10+5", "=", "25", font_size=39, color=INK)
        reverse_value[0].set_color(MUTED)
        reverse_value[2].set_color(MUTED)
        comparison = VGroup(forward_value, MathTex(">", font_size=40, color=POINT), reverse_value)
        comparison.arrange(RIGHT, buff=0.48).move_to([0, -2.64, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        beat_title = next_title
        self.play(
            FadeOut(high_pedestal),
            FadeOut(low_pedestal),
            FadeOut(high_weight),
            FadeOut(low_weight),
            FadeOut(x_card),
            FadeOut(eight_card),
            FadeOut(conditions),
            FadeOut(gain),
            run_time=0.55,
        )
        self.play(LaggedStart(*(FadeIn(place) for place in places), lag_ratio=0.15), run_time=0.8)
        self.play(FadeIn(placed_eight), run_time=0.45)
        self.play(Write(comparison), run_time=0.75)
        self.play(FadeIn(placed_five), FadeIn(placed_two), run_time=0.7)
        self.play(Indicate(forward_value[2], color=REGION), run_time=0.55)
        self.wait(0.4)

        # Beat 10: only now join the three cards and reveal the numeral.
        self.next_beat("reveal_maximum_number")
        next_title = label("把三個位值收成一個數", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        final_cards = VGroup(
            self.digit_card("8", REGION, scale=1.08),
            self.digit_card("5", POINT, scale=1.08),
            self.digit_card("2", BLUE, scale=1.08),
        ).arrange(RIGHT, buff=0.10).move_to([0, 0.60, 0])
        answer_frame = SurroundingRectangle(final_cards, color=POINT, buff=0.18, stroke_width=3)
        answer_label = label("最大三位數", 28, POINT, "BOLD").next_to(answer_frame, UP, buff=0.22)
        place_expansion = MathTex(
            r"8\cdot100", "+", r"5\cdot10", "+", "2", "=", "852",
            font_size=49,
            color=INK,
        )
        place_expansion[0].set_color(REGION)
        place_expansion[2].set_color(POINT)
        place_expansion[4].set_color(BLUE)
        place_expansion[6].set_color(POINT)
        place_expansion.move_to([0, -1.42, 0])
        closing = label("先找中心，再讓大數字占大位值", 27, MUTED, "MEDIUM")
        closing.move_to([0, -2.42, 0])

        self.play(self.title_change(beat_title, next_title), run_time=0.55)
        self.play(FadeOut(comparison), FadeOut(places), run_time=0.55)
        self.play(
            Transform(placed_eight, final_cards[0]),
            Transform(placed_five, final_cards[1]),
            Transform(placed_two, final_cards[2]),
            run_time=0.95,
        )
        self.play(Create(answer_frame), FadeIn(answer_label), run_time=0.55)
        self.play(Write(place_expansion), run_time=0.75)
        self.play(FadeIn(closing), Circumscribe(place_expansion[6], color=POINT), run_time=0.7)
        self.wait(0.45)
