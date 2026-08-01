"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q8."""

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
    ArcBetweenPoints,
    Arrow,
    Brace,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


BALL_LABELS = tuple(range(1, 26))
MOVED_BALL = 15
TOTAL_SUM = sum(BALL_LABELS)
VALID_M = 9
PARTITION_A = tuple(range(13, 22))
PARTITION_B = tuple(value for value in BALL_LABELS if value not in PARTITION_A)


def average(values: tuple[int, ...]) -> Fraction:
    if not values:
        raise ValueError("an empty basket has no average")
    return Fraction(sum(values), len(values))


def implied_a_mean(count_a: int) -> Fraction:
    if not 2 <= count_a <= 24:
        raise ValueError("both post-move basket averages must be defined")
    return Fraction(count_a + 59, 4)


def implied_b_mean(count_a: int) -> Fraction:
    if not 2 <= count_a <= 24:
        raise ValueError("both post-move basket averages must be defined")
    return Fraction(count_a + 34, 4)


ADMISSIBLE_COUNTS = tuple(
    count_a
    for count_a in range(2, 25)
    if count_a * implied_a_mean(count_a)
    + (25 - count_a) * implied_b_mean(count_a)
    == TOTAL_SUM
)

if TOTAL_SUM != 325:
    raise ValueError("the sum of labels 1 through 25 should be 325")
if any(left + right != 26 for left, right in zip(range(1, 13), range(25, 13, -1))):
    raise ValueError("the endpoint-pair construction of 325 failed")
if ADMISSIBLE_COUNTS != (VALID_M,):
    raise ValueError("the mean equations should permit exactly m=9")
if len(PARTITION_A) != VALID_M or MOVED_BALL not in PARTITION_A:
    raise ValueError("the explicit A basket is malformed")
if set(PARTITION_A).intersection(PARTITION_B):
    raise ValueError("the explicit baskets overlap")
if tuple(sorted(PARTITION_A + PARTITION_B)) != BALL_LABELS:
    raise ValueError("the explicit baskets do not partition labels 1 through 25")
if (sum(PARTITION_A), sum(PARTITION_B)) != (153, 172):
    raise ValueError("the explicit partition totals changed")

PARTITION_A_AFTER = tuple(value for value in PARTITION_A if value != MOVED_BALL)
PARTITION_B_AFTER = tuple(sorted(PARTITION_B + (MOVED_BALL,)))
A_BEFORE_MEAN = average(PARTITION_A)
A_AFTER_MEAN = average(PARTITION_A_AFTER)
B_BEFORE_MEAN = average(PARTITION_B)
B_AFTER_MEAN = average(PARTITION_B_AFTER)

if (A_BEFORE_MEAN, A_AFTER_MEAN, B_BEFORE_MEAN, B_AFTER_MEAN) != (
    Fraction(17),
    Fraction(69, 4),
    Fraction(43, 4),
    Fraction(11),
):
    raise ValueError("the explicit partition averages changed")
if A_AFTER_MEAN - A_BEFORE_MEAN != Fraction(1, 4):
    raise ValueError("basket A does not rise by one quarter")
if B_AFTER_MEAN - B_BEFORE_MEAN != Fraction(1, 4):
    raise ValueError("basket B does not rise by one quarter")


class CarloTcfs112MathQ08(CarloSlide):
    """Move one labelled ball, then account for both average increases."""

    lesson_id = "carlo.tcfs_112_math_gifted.q08"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def stage_title(text: str, size: int = 30):
        title = label(text, size, INK, "BOLD")
        title.move_to([0, 3.04, 0])
        return title

    @staticmethod
    def ball(number: int, color: str = MUTED, radius: float = 0.29) -> VGroup:
        shell = Circle(
            radius=radius,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.12,
        )
        value = MathTex(str(number), font_size=22 if number >= 10 else 24, color=color)
        value.move_to(shell)
        return VGroup(shell, value)

    @staticmethod
    def basket(name: str, color: str, width: float = 4.80, height: float = 2.05) -> VGroup:
        body = Polygon(
            [-width / 2, height / 2, 0],
            [width / 2, height / 2, 0],
            [width * 0.42, -height / 2, 0],
            [-width * 0.42, -height / 2, 0],
            color=color,
            stroke_width=3.0,
            fill_color=color,
            fill_opacity=0.07,
        )
        rim = Line(
            [-width / 2 - 0.08, height / 2, 0],
            [width / 2 + 0.08, height / 2, 0],
            color=color,
            stroke_width=5.0,
        )
        tag = MathTex(name, font_size=39, color=color).next_to(rim, UP, buff=0.12)
        return VGroup(body, rim, tag)

    @staticmethod
    def count_card(expression: str, color: str) -> VGroup:
        frame = RoundedRectangle(
            width=2.25,
            height=0.80,
            corner_radius=0.06,
            color=color,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.96,
        )
        value = MathTex(expression, font_size=35, color=color).move_to(frame)
        return VGroup(frame, value)

    @staticmethod
    def mean_gauge(symbol: str, color: str) -> VGroup:
        axis = Line([0, -0.66, 0], [0, 0.66, 0], color=MUTED, stroke_width=3)
        old_dot = Dot([0, -0.42, 0], radius=0.09, color=color)
        new_dot = Dot([0, 0.42, 0], radius=0.10, color=REGION)
        rise = Arrow(
            [0, -0.26, 0],
            [0, 0.26, 0],
            buff=0,
            color=REGION,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.24,
        )
        old_label = MathTex(symbol, font_size=29, color=color).next_to(old_dot, LEFT, buff=0.17)
        new_label = MathTex(
            rf"{symbol}+\frac14",
            font_size=28,
            color=REGION,
        ).next_to(new_dot, RIGHT, buff=0.17)
        return VGroup(axis, old_dot, new_dot, rise, old_label, new_label)

    @staticmethod
    def quarter_train(multiplier: str) -> VGroup:
        tiles = VGroup()
        for _ in range(3):
            frame = RoundedRectangle(
                width=1.05,
                height=0.72,
                corner_radius=0.05,
                color=REGION,
                stroke_width=2.3,
                fill_color=REGION,
                fill_opacity=0.11,
            )
            value = MathTex(r"\frac14", font_size=29, color=REGION).move_to(frame)
            tiles.add(VGroup(frame, value))
        dots = MathTex(r"\cdots", font_size=30, color=MUTED)
        row = VGroup(*tiles, dots).arrange(RIGHT, buff=0.20)
        brace = Brace(row, DOWN, color=REGION, buff=0.12)
        count = MathTex(multiplier, font_size=29, color=REGION).next_to(brace, DOWN, buff=0.10)
        return VGroup(row, brace, count)

    @staticmethod
    def pair_card(pair: str) -> VGroup:
        frame = RoundedRectangle(
            width=2.05,
            height=0.84,
            corner_radius=0.05,
            color=BLUE,
            stroke_width=2.4,
            fill_color=BLUE,
            fill_opacity=0.09,
        )
        expression = MathTex(pair, font_size=31, color=BLUE).move_to(frame)
        total = MathTex("26", font_size=25, color=REGION).next_to(frame, DOWN, buff=0.12)
        return VGroup(frame, expression, total)

    def construct(self) -> None:
        heading = label("第 8 題｜一顆球，讓兩邊平均都上升", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 8 頁｜影片 yxlLBTcz4kg 00:00-04:43.80",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 build_two_baskets: establish counts before doing arithmetic.
        self.begin_beat("build_two_baskets")
        stage_title = self.stage_title("25 顆編號球，被分進兩個籃子")
        shelf_items = VGroup(
            self.ball(1, MUTED, 0.24),
            self.ball(2, MUTED, 0.24),
            self.ball(3, MUTED, 0.24),
            MathTex(r"\cdots", font_size=30, color=MUTED),
            self.ball(15, POINT, 0.27),
            MathTex(r"\cdots", font_size=30, color=MUTED),
            self.ball(25, MUTED, 0.24),
        ).arrange(RIGHT, buff=0.23)
        shelf_items.move_to([0, 2.12, 0])
        shelf_note = label("編號 1 到 25", 23, MUTED, "MEDIUM").next_to(
            shelf_items, UP, buff=0.12
        )

        basket_a = self.basket("A", BLUE).move_to([-3.55, -0.38, 0])
        basket_b = self.basket("B", PURPLE).move_to([3.55, -0.38, 0])
        a_dots = VGroup(
            Dot([-4.48, -0.35, 0], radius=0.11, color=BLUE),
            Dot([-4.03, -0.66, 0], radius=0.11, color=BLUE),
            Dot([-3.57, -0.27, 0], radius=0.11, color=BLUE),
            MathTex(r"\cdots", font_size=28, color=BLUE).move_to([-2.80, -0.52, 0]),
        )
        b_dots = VGroup(
            Dot([2.65, -0.34, 0], radius=0.11, color=PURPLE),
            Dot([3.10, -0.66, 0], radius=0.11, color=PURPLE),
            Dot([3.56, -0.27, 0], radius=0.11, color=PURPLE),
            Dot([4.02, -0.63, 0], radius=0.11, color=PURPLE),
            MathTex(r"\cdots", font_size=28, color=PURPLE).move_to([4.58, -0.38, 0]),
        )
        ball_fifteen = self.ball(15, POINT, 0.34).move_to([-2.58, -0.55, 0])
        a_count = self.count_card("m", BLUE).move_to([-3.55, -1.46, 0])
        b_count = self.count_card("25-m", PURPLE).move_to([3.55, -1.46, 0])
        count_note = label("15 號球一開始在 A", 27, POINT, "BOLD")
        count_note.move_to([0, -2.48, 0])

        self.add(heading, source)
        self.play(FadeIn(stage_title), run_time=0.48)
        self.play(LaggedStart(*(FadeIn(item) for item in shelf_items), lag_ratio=0.09), FadeIn(shelf_note), run_time=0.86)
        self.play(Create(basket_a), Create(basket_b), run_time=0.72)

        # Beat 02 meet_two_baskets: continue at a settled semantic boundary.
        self.next_beat("meet_two_baskets")
        self.play(FadeIn(a_dots), FadeIn(b_dots), GrowFromCenter(ball_fifteen), run_time=0.62)
        self.play(FadeIn(a_count), FadeIn(b_count), FadeIn(count_note), run_time=0.58)
        self.wait(0.40)

        # Beat 03 move_ball_fifteen: preserve the ball while both mean gauges rise.
        self.next_beat("move_ball_fifteen")
        next_title = self.stage_title("把同一顆 15 號球從 A 移到 B")
        a_after_count = self.count_card("m-1", BLUE).move_to(a_count)
        b_after_count = self.count_card("26-m", PURPLE).move_to(b_count)
        transfer_path = ArcBetweenPoints(
            ball_fifteen.get_center(),
            [2.20, -0.54, 0],
            angle=-0.48,
        )
        transfer_arrow = Arrow(
            [-1.30, 0.20, 0],
            [1.30, 0.20, 0],
            color=POINT,
            stroke_width=3.2,
            max_tip_length_to_length_ratio=0.15,
        )
        gauge_a = self.mean_gauge(r"x_A", BLUE).move_to([-3.55, 1.48, 0])
        gauge_b = self.mean_gauge(r"x_B", PURPLE).move_to([3.55, 1.48, 0])
        surprise = label("拿走與加入之後，兩邊平均都上升 1/4", 28, REGION, "BOLD")
        surprise.move_to([0, -2.48, 0])
        domain_note = MathTex(r"2\le m\le24", font_size=27, color=MUTED)
        domain_note.next_to(surprise, DOWN, buff=0.14)

        self.play(self.title_change(stage_title, next_title), FadeOut(shelf_items), FadeOut(shelf_note), run_time=0.58)
        stage_title = next_title
        self.play(Create(transfer_arrow), run_time=0.42)
        self.play(
            MoveAlongPath(ball_fifteen, transfer_path),
            self.title_change(a_count[1], a_after_count[1]),
            self.title_change(b_count[1], b_after_count[1]),
            run_time=1.10,
        )
        a_count = VGroup(a_count[0], a_after_count[1])
        b_count = VGroup(b_count[0], b_after_count[1])

        # Beat 04 show_new_mean_gauges: continue at a settled semantic boundary.
        self.next_beat("show_new_mean_gauges")
        self.play(
            Succession(
                FadeOut(count_note),
                FadeIn(gauge_a[0:2], gauge_b[0:2]),
            ),
            run_time=0.48,
        )
        self.play(Create(gauge_a[3]), FadeIn(gauge_a[2], gauge_a[4:]), Create(gauge_b[3]), FadeIn(gauge_b[2], gauge_b[4:]), run_time=0.70)
        self.play(FadeIn(surprise), FadeIn(domain_note), run_time=0.52)
        self.wait(0.48)

        # Beat 05 measure_a_deficit: the removed ball's deficit funds the lift.
        self.next_beat("measure_a_deficit")
        next_title = self.stage_title("A：拿走低於平均的 15，剩下每份抬高 1/4", 29)
        a_level = Line([-4.10, -1.15, 0], [-4.10, 1.35, 0], color=MUTED, stroke_width=3)
        fifteen_dot = Dot([-4.10, -0.78, 0], radius=0.13, color=POINT)
        mean_a_dot = Dot([-4.10, 0.88, 0], radius=0.13, color=BLUE)
        fifteen_label = MathTex("15", font_size=34, color=POINT).next_to(fifteen_dot, LEFT, buff=0.22)
        mean_a_label = MathTex(r"x_A", font_size=35, color=BLUE).next_to(mean_a_dot, LEFT, buff=0.22)
        deficit_brace = Brace(Line(fifteen_dot.get_center(), mean_a_dot.get_center()), RIGHT, color=BLUE, buff=0.22)
        deficit_label = MathTex(r"x_A-15", font_size=34, color=BLUE).next_to(deficit_brace, RIGHT, buff=0.18)
        a_ladder = VGroup(a_level, fifteen_dot, mean_a_dot, fifteen_label, mean_a_label, deficit_brace, deficit_label)
        quarter_a = self.quarter_train("m-1").move_to([2.55, 0.55, 0])
        a_balance = MathTex(
            r"x_A-15=\frac{m-1}{4}",
            font_size=51,
            color=INK,
        ).move_to([1.85, -1.30, 0])
        a_balance.set_color_by_tex(r"x_A-15", BLUE)
        a_reason = label("15 與原平均的缺口，剛好分成 m-1 份", 26, MUTED, "MEDIUM")
        a_reason.move_to([1.85, -2.25, 0])

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            FadeOut(basket_a), FadeOut(basket_b), FadeOut(a_dots), FadeOut(b_dots),
            FadeOut(ball_fifteen), FadeOut(a_count), FadeOut(b_count), FadeOut(transfer_arrow),
            FadeOut(gauge_a), FadeOut(gauge_b), FadeOut(surprise), FadeOut(domain_note),
            run_time=0.58,
        )
        self.play(Create(a_level), GrowFromCenter(fifteen_dot), FadeIn(fifteen_label), run_time=0.55)
        self.play(GrowFromCenter(mean_a_dot), FadeIn(mean_a_label), Create(deficit_brace), FadeIn(deficit_label), run_time=0.62)

        # Beat 06 balance_a_mean_change: continue at a settled semantic boundary.
        self.next_beat("balance_a_mean_change")
        self.play(LaggedStart(*(FadeIn(item) for item in quarter_a[0]), lag_ratio=0.12), Create(quarter_a[1]), FadeIn(quarter_a[2]), run_time=0.78)
        self.play(FadeIn(a_balance), FadeIn(a_reason), run_time=0.72)
        self.wait(0.45)

        # Beat 07 derive_a_mean: reconstruct the old A mean from the visible gap.
        self.next_beat("derive_a_mean")
        next_title = self.stage_title("把缺口加回 15，就得到 A 的原平均")
        a_base = Rectangle(
            width=3.10,
            height=0.92,
            color=POINT,
            stroke_width=2.7,
            fill_color=POINT,
            fill_opacity=0.10,
        )
        a_base_label = MathTex("15", font_size=39, color=POINT).move_to(a_base)
        a_gap = Rectangle(
            width=2.25,
            height=0.92,
            color=REGION,
            stroke_width=2.7,
            fill_color=REGION,
            fill_opacity=0.11,
        )
        a_gap_label = MathTex(r"\frac{m-1}{4}", font_size=34, color=REGION).move_to(a_gap)
        a_mean_bar = VGroup(VGroup(a_base, a_base_label), VGroup(a_gap, a_gap_label)).arrange(RIGHT, buff=0)
        a_bar_brace = Brace(a_mean_bar, DOWN, color=BLUE, buff=0.15)
        a_bar_name = MathTex(r"x_A", font_size=36, color=BLUE).next_to(a_bar_brace, DOWN, buff=0.12)
        a_mean_visual = VGroup(a_mean_bar, a_bar_brace, a_bar_name).move_to([-2.90, 0.40, 0])
        a_steps = VGroup(
            MathTex(r"x_A=15+\frac{m-1}{4}", font_size=47, color=INK),
            MathTex(r"x_A=\frac{m+59}{4}", font_size=54, color=BLUE),
            label("A 的平均一定在 15 上方", 27, BLUE, "BOLD"),
        ).arrange(DOWN, buff=0.55)
        a_steps.move_to([3.10, -0.25, 0])
        divider = Line([0.25, -3.30, 0], [0.25, 2.35, 0], color=HAIRLINE, stroke_width=1.5)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(a_ladder),
            FadeOut(quarter_a),
            FadeOut(a_balance),
            FadeOut(a_reason),
            run_time=0.56,
        )
        stage_title = next_title
        self.play(Create(divider), FadeIn(a_mean_bar), Create(a_bar_brace), FadeIn(a_bar_name), run_time=0.70)
        self.play(FadeIn(a_steps[0]), run_time=0.68)
        self.play(FadeIn(a_steps[1]), Indicate(a_mean_visual, color=BLUE), run_time=0.72)

        # Beat 08 solve_a_mean: continue at a settled semantic boundary.
        self.next_beat("solve_a_mean")
        self.play(FadeIn(a_steps[2]), run_time=0.42)
        self.wait(0.45)

        # Beat 09 measure_b_surplus: the added ball's surplus funds the lift.
        self.next_beat("measure_b_surplus")
        next_title = self.stage_title("B：加入高於平均的 15，所有新份額抬高 1/4", 29)
        b_level = Line([-4.10, -1.15, 0], [-4.10, 1.35, 0], color=MUTED, stroke_width=3)
        mean_b_dot = Dot([-4.10, -0.82, 0], radius=0.13, color=PURPLE)
        b_fifteen_dot = Dot([-4.10, 0.86, 0], radius=0.13, color=POINT)
        mean_b_label = MathTex(r"x_B", font_size=35, color=PURPLE).next_to(mean_b_dot, LEFT, buff=0.22)
        b_fifteen_label = MathTex("15", font_size=34, color=POINT).next_to(b_fifteen_dot, LEFT, buff=0.22)
        surplus_brace = Brace(Line(mean_b_dot.get_center(), b_fifteen_dot.get_center()), RIGHT, color=PURPLE, buff=0.22)
        surplus_label = MathTex(r"15-x_B", font_size=34, color=PURPLE).next_to(surplus_brace, RIGHT, buff=0.18)
        b_ladder = VGroup(b_level, mean_b_dot, b_fifteen_dot, mean_b_label, b_fifteen_label, surplus_brace, surplus_label)
        quarter_b = self.quarter_train("26-m").move_to([2.55, 0.55, 0])
        b_balance = MathTex(
            r"15-x_B=\frac{26-m}{4}",
            font_size=49,
            color=INK,
        ).move_to([1.85, -1.30, 0])
        b_balance.set_color_by_tex(r"15-x_B", PURPLE)
        b_reason = label("15 高出的部分，分給加入後的 26-m 份", 26, MUTED, "MEDIUM")
        b_reason.move_to([1.85, -2.25, 0])

        self.play(self.title_change(stage_title, next_title), run_time=0.54)
        stage_title = next_title
        self.play(FadeOut(a_mean_visual), FadeOut(a_steps), FadeOut(divider), run_time=0.50)
        self.play(Create(b_level), GrowFromCenter(mean_b_dot), FadeIn(mean_b_label), run_time=0.52)
        self.play(GrowFromCenter(b_fifteen_dot), FadeIn(b_fifteen_label), Create(surplus_brace), FadeIn(surplus_label), run_time=0.62)

        # Beat 10 balance_b_mean_change: continue at a settled semantic boundary.
        self.next_beat("balance_b_mean_change")
        self.play(LaggedStart(*(FadeIn(item) for item in quarter_b[0]), lag_ratio=0.12), Create(quarter_b[1]), FadeIn(quarter_b[2]), run_time=0.78)
        self.play(FadeIn(b_balance), FadeIn(b_reason), run_time=0.72)
        self.wait(0.45)

        # Beat 11 place_old_means_on_axis: solve B and notice a fixed separation.
        self.next_beat("place_old_means_on_axis")
        next_title = self.stage_title("兩個原平均的距離，竟然與 m 無關")
        mean_axis = Line([-4.05, -1.35, 0], [-4.05, 1.45, 0], color=MUTED, stroke_width=3)
        b_mark = Dot([-4.05, -0.95, 0], radius=0.13, color=PURPLE)
        fifteen_mark = Dot([-4.05, -0.05, 0], radius=0.12, color=POINT)
        a_mark = Dot([-4.05, 0.95, 0], radius=0.13, color=BLUE)
        b_mark_label = MathTex(r"x_B", font_size=34, color=PURPLE).next_to(b_mark, LEFT, buff=0.20)
        fifteen_mark_label = MathTex("15", font_size=32, color=POINT).next_to(fifteen_mark, LEFT, buff=0.20)
        a_mark_label = MathTex(r"x_A", font_size=34, color=BLUE).next_to(a_mark, LEFT, buff=0.20)
        gap_brace = Brace(Line(b_mark.get_center(), a_mark.get_center()), RIGHT, color=REGION, buff=0.25)
        gap_label = MathTex(r"\frac{25}{4}", font_size=38, color=REGION).next_to(gap_brace, RIGHT, buff=0.18)
        mean_comparison = VGroup(
            mean_axis, b_mark, fifteen_mark, a_mark,
            b_mark_label, fifteen_mark_label, a_mark_label, gap_brace, gap_label,
        )
        mean_steps = VGroup(
            MathTex(r"x_B=15-\frac{26-m}{4}", font_size=40, color=INK),
            MathTex(r"x_B=\frac{m+34}{4}", font_size=48, color=PURPLE),
            MathTex(r"x_A-x_B=\frac{25}{4}", font_size=49, color=REGION),
            label("兩籃平均固定相差 25/4", 27, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.45)
        mean_steps.move_to([2.35, -0.22, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(b_ladder),
            FadeOut(quarter_b),
            FadeOut(b_balance),
            FadeOut(b_reason),
            run_time=0.56,
        )
        stage_title = next_title
        self.play(Create(mean_axis), GrowFromCenter(b_mark), GrowFromCenter(fifteen_mark), GrowFromCenter(a_mark), run_time=0.62)
        self.play(FadeIn(b_mark_label), FadeIn(fifteen_mark_label), FadeIn(a_mark_label), run_time=0.42)

        # Beat 12 compare_old_means: continue at a settled semantic boundary.
        self.next_beat("compare_old_means")
        self.play(FadeIn(mean_steps[0]), run_time=0.62)
        self.play(FadeIn(mean_steps[1]), run_time=0.62)
        self.play(Create(gap_brace), FadeIn(gap_label), FadeIn(mean_steps[2]), run_time=0.74)
        self.play(FadeIn(mean_steps[3]), run_time=0.42)
        self.wait(0.45)

        # Beat 13 pair_numbers_around_fifteen: pair endpoint labels before using the total.
        self.next_beat("pair_numbers_around_fifteen")
        next_title = self.stage_title("把 1 到 25 兩端配對，先算出全部總和")
        pair_cards = VGroup(
            self.pair_card("1+25"),
            self.pair_card("2+24"),
            self.pair_card("3+23"),
            MathTex(r"\cdots", font_size=34, color=MUTED),
            self.pair_card("12+14"),
        ).arrange(RIGHT, buff=0.30)
        pair_cards.move_to([0, 0.88, 0])
        center_ball = self.ball(13, POINT, 0.39).move_to([0, -0.50, 0])
        center_note = label("中間還有 13", 24, POINT, "BOLD").next_to(center_ball, DOWN, buff=0.16)
        total_formula = MathTex(r"12\cdot26+13=325", font_size=58, color=INK)
        total_formula.set_color_by_tex("325", CORAL)
        total_formula.move_to([0, -1.83, 0])
        total_note = label("所有球的號碼總和固定是 325", 28, CORAL, "BOLD")
        total_note.move_to([0, -2.58, 0])

        self.play(self.title_change(stage_title, next_title), FadeOut(mean_comparison), FadeOut(mean_steps), run_time=0.56)
        stage_title = next_title
        self.play(LaggedStart(*(FadeIn(card) for card in pair_cards), lag_ratio=0.12), run_time=0.92)
        self.play(GrowFromCenter(center_ball), FadeIn(center_note), run_time=0.48)

        # Beat 14 earn_total_325: continue at a settled semantic boundary.
        self.next_beat("earn_total_325")
        self.play(FadeIn(total_formula), run_time=0.76)
        self.play(FadeIn(total_note), run_time=0.40)
        self.wait(0.45)

        # Beat 15 reassemble_basket_totals: counts times means recover each sum.
        self.next_beat("reassemble_basket_totals")
        next_title = self.stage_title("兩籃總和相加，仍然必須是 325")
        a_total_frame = RoundedRectangle(
            width=5.10, height=2.35, corner_radius=0.07,
            color=BLUE, stroke_width=2.8, fill_color=BLUE, fill_opacity=0.08,
        )
        b_total_frame = RoundedRectangle(
            width=5.10, height=2.35, corner_radius=0.07,
            color=PURPLE, stroke_width=2.8, fill_color=PURPLE, fill_opacity=0.08,
        )
        a_total_title = label("A 籃", 27, BLUE, "BOLD")
        a_total_math = VGroup(
            MathTex("m", font_size=42, color=BLUE),
            MathTex(r"\times", font_size=32, color=MUTED),
            MathTex(r"x_A", font_size=42, color=BLUE),
            MathTex("=", font_size=34, color=INK),
            label("A 的總和", 25, BLUE, "BOLD"),
        ).arrange(RIGHT, buff=0.24)
        a_total_group = VGroup(a_total_frame, a_total_title, a_total_math)
        a_total_title.move_to(a_total_frame.get_top() + [0, -0.40, 0])
        a_total_math.move_to(a_total_frame.get_center() + [0, -0.25, 0])
        a_total_group.move_to([-3.15, 0.55, 0])

        b_total_title = label("B 籃", 27, PURPLE, "BOLD")
        b_total_math = VGroup(
            MathTex("25-m", font_size=38, color=PURPLE),
            MathTex(r"\times", font_size=32, color=MUTED),
            MathTex(r"x_B", font_size=42, color=PURPLE),
            MathTex("=", font_size=34, color=INK),
            label("B 的總和", 25, PURPLE, "BOLD"),
        ).arrange(RIGHT, buff=0.22)
        b_total_group = VGroup(b_total_frame, b_total_title, b_total_math)
        b_total_title.move_to(b_total_frame.get_top() + [0, -0.40, 0])
        b_total_math.move_to(b_total_frame.get_center() + [0, -0.25, 0])
        b_total_group.move_to([3.15, 0.55, 0])
        merge_left = Arrow([-2.25, -0.85, 0], [-0.55, -1.48, 0], color=BLUE, stroke_width=3)
        merge_right = Arrow([2.25, -0.85, 0], [0.55, -1.48, 0], color=PURPLE, stroke_width=3)
        total_325 = MathTex("325", font_size=53, color=CORAL).move_to([0, -1.63, 0])
        basket_equation = MathTex(
            r"m x_A+(25-m)x_B=325",
            font_size=48,
            color=INK,
        ).move_to([0, -2.55, 0])
        basket_equation.set_color_by_tex("325", CORAL)

        self.play(self.title_change(stage_title, next_title), FadeOut(pair_cards), FadeOut(center_ball), FadeOut(center_note), FadeOut(total_formula), FadeOut(total_note), run_time=0.58)
        stage_title = next_title
        self.play(Create(a_total_frame), FadeIn(a_total_title), Create(b_total_frame), FadeIn(b_total_title), run_time=0.62)
        self.play(FadeIn(a_total_math), FadeIn(b_total_math), run_time=0.66)

        # Beat 16 merge_basket_totals: continue at a settled semantic boundary.
        self.next_beat("merge_basket_totals")
        self.play(Create(merge_left), Create(merge_right), GrowFromCenter(total_325), run_time=0.62)
        self.play(FadeIn(basket_equation), run_time=0.72)
        self.wait(0.45)

        # Beat 17 build_b_baseline: visualize the cancellation before algebra.
        self.next_beat("build_b_baseline")
        next_title = self.stage_title("先鋪滿 25 份 B 平均，再補上 A 與 B 的差")
        baseline = Rectangle(
            width=8.80,
            height=0.92,
            color=PURPLE,
            stroke_width=3.0,
            fill_color=PURPLE,
            fill_opacity=0.11,
        ).move_to([0, 0.45, 0])
        baseline_label = MathTex(r"25x_B", font_size=43, color=PURPLE).move_to(baseline)
        extra = Rectangle(
            width=3.70,
            height=0.92,
            color=REGION,
            stroke_width=3.0,
            fill_color=REGION,
            fill_opacity=0.13,
        ).next_to(baseline, UP, buff=0)
        extra.align_to(baseline, LEFT)
        extra_label = MathTex(r"m(x_A-x_B)", font_size=35, color=REGION).move_to(extra)
        baseline_brace = Brace(baseline, DOWN, color=MUTED, buff=0.14)
        baseline_note = label("25 顆都先用 B 的平均當底", 24, MUTED, "MEDIUM")
        baseline_note.next_to(baseline_brace, DOWN, buff=0.12)
        regroup_formula = MathTex(
            r"m x_A+(25-m)x_B=25x_B+m(x_A-x_B)",
            font_size=39,
            color=INK,
        ).move_to([0, -1.65, 0])
        known_gap = MathTex(
            r"325=25x_B+\frac{25m}{4}",
            font_size=48,
            color=INK,
        ).move_to([0, -2.46, 0])
        known_gap.set_color_by_tex(r"\frac{25m}{4}", REGION)

        self.play(self.title_change(stage_title, next_title), run_time=0.54)
        stage_title = next_title
        self.play(FadeOut(a_total_group), FadeOut(b_total_group), FadeOut(merge_left), FadeOut(merge_right), FadeOut(total_325), FadeOut(basket_equation), run_time=0.52)
        self.play(Create(baseline), FadeIn(baseline_label), Create(baseline_brace), FadeIn(baseline_note), run_time=0.62)
        self.play(Create(extra), FadeIn(extra_label), run_time=0.58)

        # Beat 18 regroup_on_b_baseline: continue at a settled semantic boundary.
        self.next_beat("regroup_on_b_baseline")
        self.play(FadeIn(regroup_formula), run_time=0.72)
        self.play(FadeIn(known_gap), Indicate(extra, color=REGION), run_time=0.68)
        self.wait(0.45)

        # Beat 19 derive_last_division: settle one step before the answer.
        self.next_beat("derive_last_division")
        next_title = self.stage_title("代入 B 的平均，只剩最後一次除法")
        solve_steps = VGroup(
            MathTex(r"13=\frac{m+34}{4}+\frac{m}{4}", font_size=46, color=INK),
            MathTex(r"52=m+34+m", font_size=47, color=INK),
            MathTex(r"18=2m", font_size=53, color=REGION),
            MathTex(r"m=\frac{18}{2}", font_size=67, color=POINT),
            label("先停在最後一次除法", 29, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.42)
        solve_steps.move_to([0, -0.18, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(baseline),
            FadeOut(baseline_label),
            FadeOut(extra),
            FadeOut(extra_label),
            FadeOut(baseline_brace),
            FadeOut(baseline_note),
            FadeOut(regroup_formula),
            FadeOut(known_gap),
            run_time=0.56,
        )
        stage_title = next_title
        self.play(FadeIn(solve_steps[0]), run_time=0.66)
        self.play(FadeIn(solve_steps[1]), run_time=0.60)
        self.play(FadeIn(solve_steps[2]), run_time=0.56)

        # Beat 20 hold_last_division: continue at a settled semantic boundary.
        self.next_beat("hold_last_division")
        self.play(FadeIn(solve_steps[3]), run_time=0.62)
        self.play(FadeIn(solve_steps[4]), run_time=0.42)
        self.wait(0.72)

        # Beat 21 reveal_count: reveal only after the settled division prompt.
        self.next_beat("reveal_count")
        next_title = self.stage_title("原來 A 籃一開始有 9 顆球")
        answer = MathTex("m=9", font_size=82, color=POINT)
        answer_box = SurroundingRectangle(answer, color=POINT, buff=0.30, stroke_width=3.5)
        answer_group = VGroup(answer_box, answer).move_to([0, 1.35, 0])
        original_counts = VGroup(
            VGroup(label("A 籃", 28, BLUE, "BOLD"), self.count_card("9", BLUE)).arrange(DOWN, buff=0.24),
            VGroup(label("B 籃", 28, PURPLE, "BOLD"), self.count_card("16", PURPLE)).arrange(DOWN, buff=0.24),
        ).arrange(RIGHT, buff=2.10)
        original_counts.move_to([0, -0.45, 0])
        reveal_note = label("必要條件只留下這一個整數，但它真的做得到嗎？", 28, CORAL, "BOLD")
        reveal_note.move_to([0, -2.18, 0])

        self.play(self.title_change(stage_title, next_title), FadeOut(solve_steps), run_time=0.52)
        stage_title = next_title
        self.play(GrowFromCenter(answer), Create(answer_box), run_time=0.70)
        self.play(FadeIn(original_counts), run_time=0.62)
        self.play(FadeIn(reveal_note), run_time=0.46)
        self.wait(0.48)

        # Beat 22 build_candidate_partition: construct a partition and replay the move.
        self.next_beat("build_candidate_partition")
        next_title = self.stage_title("用一組真的分法，回到開場核對兩次上升")
        a_partition_label = MathTex(r"A=", font_size=35, color=BLUE)
        a_partition_balls = VGroup(
            *(self.ball(value, POINT if value == MOVED_BALL else BLUE, 0.27) for value in PARTITION_A)
        ).arrange(RIGHT, buff=0.14)
        a_partition = VGroup(a_partition_label, a_partition_balls).arrange(RIGHT, buff=0.20)
        a_partition.move_to([0, 1.76, 0])
        moving_verify_ball = a_partition_balls[2]
        b_partition = MathTex(
            r"B=\{1,\ldots,12,22,\ldots,25\}",
            font_size=36,
            color=PURPLE,
        ).move_to([-0.65, 0.78, 0])
        b_target = Circle(radius=0.31, color=PURPLE, stroke_width=2.5).move_to([4.20, 0.78, 0])
        b_plus = MathTex("+", font_size=34, color=MUTED).move_to([3.60, 0.78, 0])
        verify_path = ArcBetweenPoints(moving_verify_ball.get_center(), b_target.get_center(), angle=-0.42)
        stats_divider = Line([0, -2.32, 0], [0, 0.10, 0], color=HAIRLINE, stroke_width=1.5)
        a_stats = VGroup(
            label("A 籃", 27, BLUE, "BOLD"),
            MathTex(r"\frac{153}{9}=17", font_size=39, color=BLUE),
            Arrow([-0.55, 0, 0], [0.55, 0, 0], color=REGION, stroke_width=3),
            MathTex(r"\frac{138}{8}=\frac{69}{4}=17+\frac14", font_size=37, color=REGION),
        ).arrange(DOWN, buff=0.25)
        a_stats.move_to([-3.45, -1.00, 0])
        b_stats = VGroup(
            label("B 籃", 27, PURPLE, "BOLD"),
            MathTex(r"\frac{172}{16}=\frac{43}{4}", font_size=39, color=PURPLE),
            Arrow([-0.55, 0, 0], [0.55, 0, 0], color=REGION, stroke_width=3),
            MathTex(r"\frac{187}{17}=11=\frac{43}{4}+\frac14", font_size=35, color=REGION),
        ).arrange(DOWN, buff=0.25)
        b_stats.move_to([3.45, -1.00, 0])
        verified = label("兩邊都恰好上升 1/4，m=9 確實可行", 29, POINT, "BOLD")
        verified.move_to([0, -2.63, 0])

        self.play(self.title_change(stage_title, next_title), FadeOut(answer_group), FadeOut(original_counts), FadeOut(reveal_note), run_time=0.55)
        stage_title = next_title
        self.play(FadeIn(a_partition_label), LaggedStart(*(GrowFromCenter(ball) for ball in a_partition_balls), lag_ratio=0.07), run_time=0.92)
        self.play(FadeIn(b_partition), FadeIn(b_plus), Create(b_target), run_time=0.58)
        self.play(Create(stats_divider), FadeIn(a_stats[0:2]), FadeIn(b_stats[0:2]), run_time=0.62)

        # Beat 23 verify_real_partition: continue at a settled semantic boundary.
        self.next_beat("verify_real_partition")
        self.play(MoveAlongPath(moving_verify_ball, verify_path), run_time=1.00)
        self.play(
            Succession(
                FadeOut(b_target, b_plus),
                FadeIn(a_stats[2:], b_stats[2:]),
            ),
            run_time=0.78,
        )
        self.play(FadeIn(verified), run_time=0.50)
        self.wait(0.50)
