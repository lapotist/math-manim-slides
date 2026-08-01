"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q9."""

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
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


LIMIT = 2024
MINIMUM_LENGTH = 60


def enumerate_representations() -> tuple[tuple[int, int, int], ...]:
    """Enumerate directly, without using the arithmetic-series formula."""
    representations: list[tuple[int, int, int]] = []
    for length in range(MINIMUM_LENGTH, LIMIT + 1):
        if sum(range(1, length + 1)) > LIMIT:
            break
        for first in range(1, LIMIT + 1):
            total = sum(range(first, first + length))
            if total > LIMIT:
                break
            representations.append((total, length, first))
    return tuple(representations)


REPRESENTATIONS = enumerate_representations()
EXPECTED_REPRESENTATIONS = (
    (1830, 60, 1),
    (1890, 60, 2),
    (1950, 60, 3),
    (2010, 60, 4),
    (1891, 61, 1),
    (1952, 61, 2),
    (2013, 61, 3),
    (1953, 62, 1),
    (2015, 62, 2),
    (2016, 63, 1),
)
LENGTH_TOTALS = {
    length: tuple(
        total
        for total, representation_length, _ in REPRESENTATIONS
        if representation_length == length
    )
    for length in range(60, 64)
}
SORTED_TOTALS = tuple(sorted(total for total, _, _ in REPRESENTATIONS))
EXPECTED_SORTED_TOTALS = (
    1830,
    1890,
    1891,
    1950,
    1952,
    1953,
    2010,
    2013,
    2015,
    2016,
)

if REPRESENTATIONS != EXPECTED_REPRESENTATIONS:
    raise ValueError(f"unexpected consecutive-sum representations: {REPRESENTATIONS}")
if tuple(len(LENGTH_TOTALS[length]) for length in range(60, 64)) != (4, 3, 2, 1):
    raise ValueError(f"unexpected counts by length: {LENGTH_TOTALS}")
if SORTED_TOTALS != EXPECTED_SORTED_TOTALS:
    raise ValueError(f"unexpected sorted totals: {SORTED_TOTALS}")
if len(set(SORTED_TOTALS)) != 10:
    raise ValueError("candidate totals must be pairwise distinct")
if sum(range(1, 65)) != 2080 or sum(range(1, 65)) <= LIMIT:
    raise ValueError("the length-64 stopping boundary is incorrect")


class CarloTcfs113MathQ09(CarloSlide):
    """Discover the count by shifting one row before naming its formula."""

    lesson_id = "carlo.tcfs_113_math_gifted.q09"
    LENGTH_COLORS = {60: BLUE, 61: POINT, 62: PURPLE, 63: REGION}
    START_CARD_X = (-4.55, -1.52, 1.52, 4.55)
    DISTINCT_CARD_X = (-5.15, -2.58, 0.0, 2.58, 5.15)

    @staticmethod
    def replace_title(scene: "CarloTcfs113MathQ09", old, new) -> None:
        """Replace semantic text without superimposing two readable labels."""
        scene.play(FadeOut(old), run_time=0.24)
        scene.play(FadeIn(new), run_time=0.28)

    @staticmethod
    def sequence_expression(start: int, length: int, *, font_size: float = 46) -> MathTex:
        """Show representative endpoints of one long consecutive row."""
        expression = MathTex(
            str(start),
            "+",
            str(start + 1),
            "+",
            str(start + 2),
            "+",
            r"\cdots",
            "+",
            str(start + length - 3),
            "+",
            str(start + length - 2),
            "+",
            str(start + length - 1),
            font_size=font_size,
            color=INK,
        )
        for index in (0, 2, 4, 8, 10, 12):
            expression[index].set_color(BLUE)
        expression[6].set_color(MUTED)
        if expression.width > 13.15:
            expression.scale_to_fit_width(13.15)
        return expression

    @staticmethod
    def generic_sequence() -> MathTex:
        """Show the first, generic, and last terms used in the formula."""
        expression = MathTex(
            "x",
            "+",
            "(x+1)",
            "+",
            r"\cdots",
            "+",
            "(x+k-2)",
            "+",
            "(x+k-1)",
            font_size=43,
            color=INK,
        )
        for index in (0, 2, 6, 8):
            expression[index].set_color(BLUE)
        expression[4].set_color(MUTED)
        if expression.width > 12.7:
            expression.scale_to_fit_width(12.7)
        return expression

    @staticmethod
    def pair_expression(left: int, right: int) -> MathTex:
        pair = MathTex(
            str(left),
            "+",
            str(right),
            "=",
            "61",
            font_size=36,
            color=INK,
        )
        pair[0].set_color(BLUE)
        pair[2].set_color(BLUE)
        pair[4].set_color(POINT)
        return pair

    @staticmethod
    def start_total_card(first: int, total: int, color: str) -> VGroup:
        frame = RoundedRectangle(
            width=2.22,
            height=1.08,
            corner_radius=0.07,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.08,
        )
        first_tex = MathTex("x", "=", str(first), font_size=22, color=MUTED)
        first_tex[0].set_color(BLUE)
        first_tex.move_to(frame.get_center() + UP * 0.27)
        total_tex = MathTex(str(total), font_size=34, color=color)
        total_tex.move_to(frame.get_center() + DOWN * 0.20)
        return VGroup(frame, first_tex, total_tex)

    @staticmethod
    def card_connector(left_card: VGroup, right_card: VGroup, increment: int) -> VGroup:
        y_coord = left_card.get_y()
        arrow = Arrow(
            [left_card.get_right()[0] + 0.08, y_coord, 0],
            [right_card.get_left()[0] - 0.08, y_coord, 0],
            buff=0,
            color=MUTED,
            stroke_width=2.2,
            max_tip_length_to_length_ratio=0.24,
        )
        increment_tex = MathTex(
            "+",
            str(increment),
            font_size=20,
            color=MUTED,
        )
        increment_tex.next_to(arrow, UP, buff=0.04)
        return VGroup(arrow, increment_tex)

    @classmethod
    def length_lane(
        cls,
        length: int,
        totals: tuple[int, ...],
        y_coord: float,
    ) -> VGroup:
        """Build one fixed-width row of valid totals for a chosen length."""
        color = cls.LENGTH_COLORS[length]
        length_tex = MathTex("k", "=", str(length), font_size=30, color=INK)
        length_tex[0].set_color(color)
        length_tex[2].set_color(color)
        length_tex.move_to([-6.58, y_coord, 0])

        chips = VGroup()
        for first, (x_coord, total) in enumerate(
            zip(cls.START_CARD_X, totals, strict=False),
            start=1,
        ):
            frame = RoundedRectangle(
                width=1.72,
                height=0.72,
                corner_radius=0.06,
                color=color,
                stroke_width=2.1,
                fill_color=color,
                fill_opacity=0.07,
            ).move_to([x_coord, y_coord, 0])
            total_tex = MathTex(str(total), font_size=27, color=color)
            total_tex.move_to(frame.get_center() + UP * 0.09)
            first_tex = MathTex("x", "=", str(first), font_size=16, color=MUTED)
            first_tex.move_to(frame.get_center() + DOWN * 0.23)
            chips.add(VGroup(frame, total_tex, first_tex))

        connectors = VGroup()
        for index in range(len(chips) - 1):
            left_chip = chips[index]
            right_chip = chips[index + 1]
            arrow = Arrow(
                [left_chip.get_right()[0] + 0.06, y_coord, 0],
                [right_chip.get_left()[0] - 0.06, y_coord, 0],
                buff=0,
                color=HAIRLINE,
                stroke_width=1.8,
                max_tip_length_to_length_ratio=0.28,
            )
            increment_tex = MathTex(
                "+",
                str(length),
                font_size=15,
                color=MUTED,
            ).next_to(arrow, UP, buff=0.01)
            connectors.add(VGroup(arrow, increment_tex))

        minimum_label = label("最小", 14, color, "BOLD")
        minimum_label.next_to(chips[0], UP, buff=0.05)
        count_group = VGroup(
            MathTex(str(len(totals)), font_size=34, color=color),
            label("個首項", 18, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.12)
        count_group.move_to([6.15, y_coord, 0])
        return VGroup(length_tex, chips, connectors, minimum_label, count_group)

    @classmethod
    def distinct_total_card(cls, total: int, y_coord: float, x_coord: float) -> VGroup:
        length = next(
            representation_length
            for candidate, representation_length, _ in REPRESENTATIONS
            if candidate == total
        )
        color = cls.LENGTH_COLORS[length]
        frame = RoundedRectangle(
            width=1.78,
            height=0.94,
            corner_radius=0.06,
            color=color,
            stroke_width=2.2,
            fill_color=color,
            fill_opacity=0.08,
        ).move_to([x_coord, y_coord, 0])
        total_tex = MathTex(str(total), font_size=29, color=INK)
        total_tex.move_to(frame.get_center() + UP * 0.16)
        length_tex = MathTex("k", "=", str(length), font_size=17, color=color)
        length_tex.move_to(frame.get_center() + DOWN * 0.25)
        return VGroup(frame, total_tex, length_tex)

    @classmethod
    def count_panel(cls, length: int, count: int, x_coord: float) -> VGroup:
        color = cls.LENGTH_COLORS[length]
        frame = RoundedRectangle(
            width=2.45,
            height=1.55,
            corner_radius=0.07,
            color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.07,
        )
        length_tex = MathTex("k", "=", str(length), font_size=29, color=color)
        length_tex.move_to(frame.get_center() + UP * 0.42)
        divider = Line(
            frame.get_left() + RIGHT * 0.25,
            frame.get_right() + LEFT * 0.25,
            color=HAIRLINE,
            stroke_width=1.5,
        ).move_to(frame.get_center() + UP * 0.03)
        count_tex = MathTex(str(count), font_size=47, color=color)
        count_tex.move_to(frame.get_center() + DOWN * 0.37)
        panel = VGroup(frame, length_tex, divider, count_tex)
        panel.move_to([x_coord, 0.55, 0])
        return panel

    def construct(self) -> None:
        heading = label("第 9 題｜推動一列連續整數", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 9 頁｜影片 X6Cabjm94eY",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 meet_sixty_term_row: expose the shortest allowed row first.
        self.begin_beat("meet_sixty_term_row")
        beat_title = label("先排出最短的一列", 35, INK, "BOLD")
        beat_title.move_to([0, 3.12, 0])
        row = self.sequence_expression(1, 60).move_to([0, 0.86, 0])
        row_brace = Brace(row, DOWN, buff=0.18, color=MUTED)
        length_tag = VGroup(
            label("項數", 21, MUTED, "MEDIUM"),
            MathTex("k", "=", "60", font_size=28, color=BLUE),
        ).arrange(RIGHT, buff=0.16)
        length_tag.next_to(row_brace, DOWN, buff=0.10)
        first_caption = label("首項", 21, MUTED, "MEDIUM")
        first_value = MathTex("x", "=", "1", font_size=29, color=BLUE)
        first_info = VGroup(first_caption, first_value).arrange(RIGHT, buff=0.15)
        first_info.move_to([-5.45, 1.80, 0])
        row_context = VGroup(row, row_brace, length_tag, first_info)
        opening_question = label("這一列的總和是多少？", 30, POINT, "BOLD")
        opening_question.move_to([0, -1.35, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), run_time=0.45)
        self.play(FadeIn(row), run_time=1.0)
        self.play(Create(row_brace), FadeIn(length_tag), FadeIn(first_info), run_time=0.75)
        self.play(FadeIn(opening_question), run_time=0.45)
        self.wait(0.45)

        # Beat 02 pair_to_1830: pair endpoints before any general formula.
        self.next_beat("pair_to_1830")
        next_title = label("首尾配對，每一對都相同", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(opening_question), row_context.animate.shift(UP * 0.48), run_time=0.6)

        pair_rows = VGroup(
            self.pair_expression(1, 60),
            self.pair_expression(2, 59),
            self.pair_expression(30, 31),
        ).arrange(RIGHT, buff=0.85)
        pair_rows.move_to([0, -0.24, 0])
        pair_dots = MathTex(r"\cdots", font_size=34, color=MUTED)
        pair_dots.move_to((pair_rows[1].get_center() + pair_rows[2].get_center()) / 2)
        pair_count = VGroup(
            label("共有", 23, MUTED, "MEDIUM"),
            MathTex("30", font_size=33, color=POINT),
            label("對", 23, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.14).move_to([0, -1.25, 0])
        sum_equation = MathTex(
            "30",
            r"\times",
            "61",
            "=",
            "1830",
            font_size=49,
            color=INK,
        ).move_to([0, -2.18, 0])
        sum_equation[0].set_color(POINT)
        sum_equation[2].set_color(POINT)
        sum_equation[4].set_color(REGION)

        self.play(
            LaggedStart(*(FadeIn(pair) for pair in pair_rows), lag_ratio=0.25),
            FadeIn(pair_dots),
            run_time=1.15,
        )
        self.play(FadeIn(pair_count), run_time=0.45)
        self.play(FadeIn(sum_equation), run_time=0.8)
        self.wait(0.45)

        # Beat 03 shift_by_sixty: move the same row through all valid starts.
        self.next_beat("shift_by_sixty")
        next_title = label("整列向前一格，總和增加 60", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(pair_rows), FadeOut(pair_dots), FadeOut(pair_count), run_time=0.4)

        shift_note = VGroup(
            label("每一項", 22, MUTED, "MEDIUM"),
            MathTex("+1", font_size=30, color=BLUE),
            label("，共", 22, MUTED, "MEDIUM"),
            MathTex("60", font_size=30, color=POINT),
            label("項", 22, MUTED, "MEDIUM"),
            MathTex(r"\Longrightarrow", "+60", font_size=30, color=REGION),
        ).arrange(RIGHT, buff=0.13).move_to([0, -0.23, 0])
        cards = VGroup(
            *(
                self.start_total_card(first, total, REGION).move_to(
                    [x_coord, -2.02, 0]
                )
                for first, total, x_coord in zip(
                    range(1, 5),
                    LENGTH_TOTALS[60],
                    self.START_CARD_X,
                    strict=True,
                )
            )
        )
        connectors = VGroup(
            *(
                self.card_connector(cards[index], cards[index + 1], 60)
                for index in range(3)
            )
        )

        self.play(FadeOut(sum_equation), FadeIn(shift_note), FadeIn(cards[0]), run_time=0.55)
        for next_first in (2, 3):
            target_row = self.sequence_expression(next_first, 60).move_to(row)
            target_first = MathTex(
                "x", "=", str(next_first), font_size=29, color=BLUE
            ).move_to(first_value)
            card_index = next_first - 1
            self.play(
                Succession(FadeOut(row), FadeIn(target_row)),
                Succession(FadeOut(first_value), FadeIn(target_first)),
                FadeIn(connectors[card_index - 1]),
                FadeIn(cards[card_index]),
                run_time=0.85,
            )
            row = target_row
            first_value = target_first

        self.next_beat("finish_sixty_term_shifts")
        next_first = 4
        target_row = self.sequence_expression(next_first, 60).move_to(row)
        target_first = MathTex(
            "x", "=", str(next_first), font_size=29, color=BLUE
        ).move_to(first_value)
        card_index = next_first - 1
        self.play(
            Succession(FadeOut(row), FadeIn(target_row)),
            Succession(FadeOut(first_value), FadeIn(target_first)),
            FadeIn(connectors[card_index - 1]),
            FadeIn(cards[card_index]),
            run_time=0.85,
        )
        row = target_row
        first_value = target_first
        self.wait(0.45)

        # Beat 04 cross_2024_boundary: make the first invalid shift explicit.
        self.next_beat("cross_2024_boundary")
        next_title = label("第五個起點越過 2024", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(shift_note), FadeOut(cards), FadeOut(connectors), run_time=0.45)

        target_row = self.sequence_expression(5, 60).move_to(row)
        target_first = MathTex("x", "=", "5", font_size=29, color=BLUE).move_to(first_value)
        self.play(
            Succession(FadeOut(row), FadeIn(target_row)),
            Succession(FadeOut(first_value), FadeIn(target_first)),
            run_time=0.85,
        )
        row = target_row
        first_value = target_first
        boundary_equation = MathTex(
            "2010",
            "+",
            "60",
            "=",
            "2070",
            ">",
            "2024",
            font_size=47,
            color=INK,
        ).move_to([0, -0.27, 0])
        boundary_equation[0].set_color(REGION)
        boundary_equation[2].set_color(POINT)
        boundary_equation[4].set_color(CORAL)
        boundary_equation[5].set_color(CORAL)
        boundary_equation[6].set_color(POINT)
        valid_starts = MathTex(
            "k",
            "=",
            "60",
            r"\qquad",
            "x",
            r"\in",
            r"\{1,2,3,4\}",
            font_size=39,
            color=INK,
        ).move_to([0, -1.35, 0])
        valid_starts[0].set_color(BLUE)
        valid_starts[2].set_color(BLUE)
        valid_starts[4].set_color(BLUE)
        count_sixty = VGroup(
            label("可行首項", 24, MUTED, "MEDIUM"),
            MathTex("4", font_size=42, color=BLUE),
            label("個", 24, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.15).move_to([0, -2.28, 0])

        self.play(FadeIn(boundary_equation), run_time=0.75)
        self.play(FadeIn(valid_starts), FadeIn(count_sixty), run_time=0.6)
        self.wait(0.45)

        # Beat 05 name_general_sum: let algebra name the visible shift pattern.
        self.next_beat("name_general_sum")
        next_title = label("現在才替剛才的規律命名", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(row_context),
            FadeOut(boundary_equation),
            FadeOut(valid_starts),
            FadeOut(count_sixty),
            run_time=0.5,
        )

        generic_row = self.generic_sequence().move_to([0, 1.75, 0])
        first_marker = label("首項", 18, BLUE, "BOLD")
        first_marker.next_to(generic_row[0], UP, buff=0.16)
        last_marker = label("末項", 18, BLUE, "BOLD")
        last_marker.next_to(generic_row[-1], UP, buff=0.16)
        generic_brace = Brace(generic_row, DOWN, buff=0.16, color=MUTED)
        generic_length = VGroup(
            label("項數", 19, MUTED, "MEDIUM"),
            MathTex("k", font_size=28, color=POINT),
        ).arrange(RIGHT, buff=0.13)
        generic_length.next_to(generic_brace, DOWN, buff=0.08)
        average_caption = label("首尾平均 × 項數", 22, MUTED, "MEDIUM")
        average_caption.move_to([0, 0.36, 0])
        average_expression = MathTex(
            r"\frac{x+(x+k-1)}{2}",
            r"\times",
            "k",
            font_size=39,
            color=INK,
        ).move_to([0, -0.28, 0])
        average_expression[0].set_color(BLUE)
        average_expression[2].set_color(POINT)
        formula = MathTex(
            "S(k,x)",
            "=",
            r"\frac{k(2x+k-1)}{2}",
            font_size=43,
            color=INK,
        ).move_to([0, -1.32, 0])
        formula[0].set_color(REGION)
        shift_formula = MathTex(
            "S(k,x+1)-S(k,x)",
            "=",
            "k",
            font_size=37,
            color=INK,
        ).move_to([0, -2.35, 0])
        shift_formula[0].set_color(REGION)
        shift_formula[2].set_color(POINT)

        self.play(FadeIn(generic_row), FadeIn(first_marker), FadeIn(last_marker), run_time=0.8)
        self.play(Create(generic_brace), FadeIn(generic_length), run_time=0.5)
        self.play(Indicate(generic_row[0]), Indicate(generic_row[-1]), run_time=0.6)

        self.next_beat("state_general_sum_formula")
        self.play(FadeIn(average_caption), FadeIn(average_expression), run_time=0.7)
        self.play(FadeIn(formula), run_time=0.7)
        self.play(FadeIn(shift_formula), run_time=0.65)
        self.wait(0.45)

        formula_scene = VGroup(
            generic_row,
            first_marker,
            last_marker,
            generic_brace,
            generic_length,
            average_caption,
            average_expression,
            formula,
            shift_formula,
        )

        # Beat 06 open_length_61_lane: build the next case as a new lane.
        self.next_beat("open_length_61_lane")
        next_title = label("多放一項，可行起點少一個", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(formula_scene), run_time=0.5)

        minimum_61 = MathTex(
            "1",
            "+",
            "2",
            "+",
            r"\cdots",
            "+",
            "61",
            "=",
            "1891",
            font_size=35,
            color=INK,
        ).move_to([0, 1.72, 0])
        minimum_61[6].set_color(POINT)
        minimum_61[8].set_color(POINT)
        lane_60 = self.length_lane(60, LENGTH_TOTALS[60], 0.48)
        lane_61 = self.length_lane(61, LENGTH_TOTALS[61], -1.20)

        self.play(FadeIn(lane_60), run_time=0.65)
        self.play(FadeIn(minimum_61), run_time=0.7)
        self.play(FadeIn(lane_61), run_time=0.7)
        self.wait(0.45)

        # Beat 07 complete_length_lanes: expose the whole 4-3-2-1 staircase.
        self.next_beat("complete_length_lanes")
        next_title = label("長度 60 到 63，形成四層階梯", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(minimum_61), FadeOut(lane_60), FadeOut(lane_61), run_time=0.45)

        minimum_62 = MathTex(
            "1",
            "+",
            r"\cdots",
            "+",
            "62",
            "=",
            "1953",
            font_size=29,
            color=PURPLE,
        )
        minimum_63 = MathTex(
            "1",
            "+",
            r"\cdots",
            "+",
            "63",
            "=",
            "2016",
            font_size=29,
            color=REGION,
        )
        minimum_pair = VGroup(minimum_62, minimum_63).arrange(RIGHT, buff=1.2)
        minimum_pair.move_to([0, 2.28, 0])
        full_lanes = VGroup(
            self.length_lane(60, LENGTH_TOTALS[60], 1.15),
            self.length_lane(61, LENGTH_TOTALS[61], 0.15),
            self.length_lane(62, LENGTH_TOTALS[62], -0.85),
            self.length_lane(63, LENGTH_TOTALS[63], -1.85),
        )

        self.play(FadeIn(full_lanes[0]), FadeIn(full_lanes[1]), run_time=0.6)
        self.play(FadeIn(minimum_62), FadeIn(full_lanes[2]), run_time=0.7)
        self.play(FadeIn(minimum_63), FadeIn(full_lanes[3]), run_time=0.7)
        self.wait(0.5)

        # Beat 08 stop_at_length_64: reject the first longer case by its minimum.
        self.next_beat("stop_at_length_64")
        next_title = label("長度 64：連最小總和都越界", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(minimum_pair), FadeOut(full_lanes), run_time=0.5)

        row_64 = self.sequence_expression(1, 64, font_size=42).move_to([0, 1.55, 0])
        brace_64 = Brace(row_64, DOWN, buff=0.15, color=MUTED)
        tag_64 = MathTex("k", "=", "64", font_size=29, color=CORAL)
        tag_64.next_to(brace_64, DOWN, buff=0.08)
        pair_64 = MathTex(
            "32",
            r"\times",
            "65",
            "=",
            "2080",
            font_size=48,
            color=INK,
        ).move_to([0, -0.08, 0])
        pair_64[0].set_color(POINT)
        pair_64[2].set_color(POINT)
        pair_64[4].set_color(CORAL)
        boundary_64 = MathTex(
            "2080",
            ">",
            "2024",
            font_size=47,
            color=INK,
        ).move_to([0, -1.10, 0])
        boundary_64[0].set_color(CORAL)
        boundary_64[1].set_color(CORAL)
        boundary_64[2].set_color(POINT)
        growth_statement = VGroup(
            MathTex("S(k,1)", font_size=31, color=REGION),
            label("隨", 21, MUTED, "MEDIUM"),
            MathTex("k", font_size=31, color=POINT),
            label("增加而增加", 21, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.13).move_to([0, -1.92, 0])
        stop_statement = VGroup(
            MathTex(r"k\ge64", font_size=36, color=CORAL),
            label("全部不可能", 24, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.25).move_to([0, -2.66, 0])

        self.play(FadeIn(row_64), Create(brace_64), FadeIn(tag_64), run_time=0.85)
        self.play(FadeIn(pair_64), run_time=0.7)
        self.play(FadeIn(boundary_64), run_time=0.6)

        self.next_beat("exclude_longer_lengths")
        self.play(FadeIn(growth_statement), FadeIn(stop_statement), run_time=0.65)
        self.wait(0.45)

        boundary_scene = VGroup(
            row_64,
            brace_64,
            tag_64,
            pair_64,
            boundary_64,
            growth_statement,
            stop_statement,
        )

        # Beat 09 verify_distinct_totals: count totals, not representations.
        self.next_beat("verify_distinct_totals")
        next_title = label("先確認：沒有同一個 n 被算兩次", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(boundary_scene), run_time=0.5)

        sorted_caption = label("把所有候選總和由小到大排好", 23, MUTED, "MEDIUM")
        sorted_caption.move_to([0, 2.42, 0])
        top_cards = VGroup(
            *(
                self.distinct_total_card(total, 1.48, x_coord)
                for total, x_coord in zip(
                    SORTED_TOTALS[:5], self.DISTINCT_CARD_X, strict=True
                )
            )
        )
        bottom_cards = VGroup(
            *(
                self.distinct_total_card(total, -0.30, x_coord)
                for total, x_coord in zip(
                    SORTED_TOTALS[5:], self.DISTINCT_CARD_X, strict=True
                )
            )
        )
        top_relations = VGroup(
            *(
                MathTex("<", font_size=29, color=MUTED).move_to(
                    [
                        (self.DISTINCT_CARD_X[index] + self.DISTINCT_CARD_X[index + 1]) / 2,
                        1.48,
                        0,
                    ]
                )
                for index in range(4)
            )
        )
        bottom_relations = VGroup(
            *(
                MathTex("<", font_size=29, color=MUTED).move_to(
                    [
                        (self.DISTINCT_CARD_X[index] + self.DISTINCT_CARD_X[index + 1]) / 2,
                        -0.30,
                        0,
                    ]
                )
                for index in range(4)
            )
        )
        bridge = MathTex(
            "1952",
            "<",
            "1953",
            font_size=28,
            color=INK,
        ).move_to([0, 0.59, 0])
        bridge[0].set_color(POINT)
        bridge[2].set_color(PURPLE)
        distinct_statement = label("每張卡的總和值都不同", 26, REGION, "BOLD")
        distinct_statement.move_to([0, -1.52, 0])
        no_repeat = VGroup(
            label("因此沒有任何", 22, MUTED, "MEDIUM"),
            MathTex("n", font_size=30, color=BLUE),
            label("被重複計數", 22, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.13).move_to([0, -2.22, 0])

        self.play(FadeIn(sorted_caption), run_time=0.4)
        self.play(
            LaggedStart(*(FadeIn(card) for card in top_cards), lag_ratio=0.10),
            FadeIn(top_relations),
            run_time=0.95,
        )

        self.next_beat("compare_adjacent_total_rows")
        self.play(FadeIn(bridge), run_time=0.45)
        self.play(
            LaggedStart(*(FadeIn(card) for card in bottom_cards), lag_ratio=0.10),
            FadeIn(bottom_relations),
            run_time=0.95,
        )

        self.next_beat("confirm_distinct_totals")
        self.play(FadeIn(distinct_statement), FadeIn(no_repeat), run_time=0.6)
        self.wait(0.5)

        distinct_scene = VGroup(
            sorted_caption,
            top_cards,
            bottom_cards,
            top_relations,
            bottom_relations,
            bridge,
            distinct_statement,
            no_repeat,
        )

        # Beat 10 hold_count_expression: stop on a complete pre-answer frame.
        self.next_beat("hold_count_expression")
        next_title = label("四條長度列，最後合在一起", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(distinct_scene), run_time=0.5)

        count_panels = VGroup(
            self.count_panel(60, 4, -4.65),
            self.count_panel(61, 3, -1.55),
            self.count_panel(62, 2, 1.55),
            self.count_panel(63, 1, 4.65),
        )
        count_caption = label("各長度的可行首項數", 22, MUTED, "MEDIUM")
        count_caption.move_to([0, 1.85, 0])
        count_expression = MathTex(
            "4",
            "+",
            "3",
            "+",
            "2",
            "+",
            "1",
            "=",
            "?",
            font_size=62,
            color=INK,
        ).move_to([0, -1.25, 0])
        for index, color in zip((0, 2, 4, 6), (BLUE, POINT, PURPLE, REGION), strict=True):
            count_expression[index].set_color(color)
        count_expression[8].set_color(CORAL)
        hold_prompt = label("先在這裡停一下", 24, MUTED, "MEDIUM")
        hold_prompt.move_to([0, -2.35, 0])

        self.play(FadeIn(count_caption), FadeIn(count_panels), run_time=0.75)
        self.play(FadeIn(count_expression), run_time=0.8)
        self.play(FadeIn(hold_prompt), run_time=0.4)
        self.wait(0.9)

        # Beat 11 reveal_total_count: reveal the requested count only now.
        self.next_beat("reveal_total_count")
        next_title = label("符合條件的正整數個數", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(hold_prompt), run_time=0.3)

        question_mark = count_expression[8]
        answer = MathTex("10", font_size=62, color=REGION).move_to(question_mark)
        self.play(Succession(FadeOut(question_mark), FadeIn(answer)), run_time=0.7)
        completed_expression = VGroup(*count_expression[:8], answer)
        answer_box = SurroundingRectangle(
            completed_expression,
            buff=0.24,
            color=REGION,
            stroke_width=3,
            corner_radius=0.08,
        )
        conclusion = VGroup(
            label("不超過 2024、可寫成至少 60 個連續正整數之和的", 22, MUTED, "MEDIUM"),
            MathTex("n", font_size=30, color=BLUE),
        ).arrange(RIGHT, buff=0.13).move_to([0, -2.28, 0])
        self.play(Create(answer_box), FadeIn(conclusion), run_time=0.55)
        self.play(Circumscribe(answer, color=REGION, fade_out=True), run_time=0.8)
        self.wait(0.65)
