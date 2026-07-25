"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q2."""

from __future__ import annotations

import math

import numpy as np

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
    Arc,
    Arrow,
    Circle,
    Circumscribe,
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
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, TAU, UP


BASE = 2024
EXPONENT = 112
WEEK_LENGTH = 7
TODAY_INDEX = 3
WEEKDAYS = (
    "星期日",
    "星期一",
    "星期二",
    "星期三",
    "星期四",
    "星期五",
    "星期六",
)
TARGET_DAYS = BASE**EXPONENT
TARGET_REMAINDER = pow(BASE, EXPONENT, WEEK_LENGTH)
TARGET_WEEKDAY_INDEX = (TODAY_INDEX + TARGET_REMAINDER) % WEEK_LENGTH

if BASE != WEEK_LENGTH * 289 + 1:
    raise ValueError("2024 was not decomposed into full weeks correctly")
if BASE % WEEK_LENGTH != 1:
    raise ValueError("unexpected base remainder modulo 7")
if any(pow(BASE, power, WEEK_LENGTH) != 1 for power in (1, 2, 3, 7, EXPONENT)):
    raise ValueError("powers of the base did not preserve remainder 1")
if TARGET_REMAINDER != 1 or (TARGET_DAYS - 1) % WEEK_LENGTH != 0:
    raise ValueError("target day count should be one more than full weeks")
if WEEKDAYS[TODAY_INDEX] != "星期三" or WEEKDAYS[TARGET_WEEKDAY_INDEX] != "星期四":
    raise ValueError("weekday indexing is incorrect")
if not (
    WEEKDAYS[(TODAY_INDEX + 0) % WEEK_LENGTH] == "星期三"
    and WEEKDAYS[(TODAY_INDEX + 1) % WEEK_LENGTH] == "星期四"
    and WEEKDAYS[(TODAY_INDEX + 7) % WEEK_LENGTH] == "星期三"
    and WEEKDAYS[(TODAY_INDEX + 8) % WEEK_LENGTH] == "星期四"
    and WEEKDAYS[(TODAY_INDEX + 15) % WEEK_LENGTH] == "星期四"
):
    raise ValueError("small weekday boundary examples failed")


class CarloTcfs112MathQ02(CarloSlide):
    """Reduce an enormous day count to one visible step around a week."""

    lesson_id = "carlo.tcfs_112_math_gifted.q02"

    WHEEL_CENTER = np.array([-3.38, -0.30, 0.0])
    WHEEL_RADIUS = 2.08

    @staticmethod
    def transition_title(scene: "CarloTcfs112MathQ02", old, new) -> None:
        """Swap CJK titles without overlapping two semantic labels."""
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.58)

    @classmethod
    def day_position(cls, offset: int) -> np.ndarray:
        """Return the clockwise wheel position offset days after today."""
        angle = math.pi / 2 - TAU * offset / WEEK_LENGTH
        return cls.WHEEL_CENTER + cls.WHEEL_RADIUS * np.array(
            [math.cos(angle), math.sin(angle), 0.0]
        )

    @classmethod
    def wheel_objects(cls) -> tuple[VGroup, VGroup, VGroup, VGroup, Arrow]:
        """Build the stable seven-node wheel and its direction cue."""
        wheel = Circle(
            radius=cls.WHEEL_RADIUS,
            color=MUTED,
            stroke_width=3,
        ).move_to(cls.WHEEL_CENTER)
        nodes = VGroup(
            *[
                Dot(
                    cls.day_position(offset),
                    radius=0.078 if offset else 0.105,
                    color=POINT if offset == 0 else INK,
                )
                for offset in range(WEEK_LENGTH)
            ]
        ).set_z_index(5)
        offset_labels = VGroup()
        for offset in range(1, WEEK_LENGTH):
            radial = cls.day_position(offset) - cls.WHEEL_CENTER
            radial /= np.linalg.norm(radial)
            offset_labels.add(
                MathTex(
                    f"+{offset}",
                    font_size=23,
                    color=MUTED,
                ).move_to(cls.day_position(offset) + radial * 0.30)
            )
        today_label = VGroup(
            label("今天", 24, POINT, "BOLD"),
            label("星期三", 30, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.10)
        today_label.move_to(cls.day_position(0) + UP * 0.58)
        direction = Arrow(
            cls.WHEEL_CENTER + np.array([cls.WHEEL_RADIUS + 0.18, 0.68, 0]),
            cls.WHEEL_CENTER + np.array([cls.WHEEL_RADIUS + 0.18, -0.02, 0]),
            buff=0,
            color=BLUE,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.22,
        )
        return VGroup(wheel), nodes, offset_labels, today_label, direction

    @staticmethod
    def week_bundle(color: str = REGION) -> VGroup:
        """Represent one complete seven-day block without calendar names."""
        frame = RoundedRectangle(
            width=1.34,
            height=0.84,
            corner_radius=0.06,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.97,
        )
        dots = VGroup(
            *[Dot(radius=0.045, color=color) for _ in range(WEEK_LENGTH)]
        ).arrange(RIGHT, buff=0.075)
        dots.move_to(frame)
        return VGroup(frame, dots)

    @staticmethod
    def factor_tile(tex: str, color: str) -> VGroup:
        """Build one factor/remainder tile for the multiplication visual."""
        frame = RoundedRectangle(
            width=1.56,
            height=1.00,
            corner_radius=0.06,
            color=color,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.97,
        )
        value = MathTex(tex, font_size=34, color=color).move_to(frame)
        return VGroup(frame, value)

    def construct(self) -> None:
        heading = label("第 2 題｜把天文數字縮成星期輪上的一步", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 2 頁｜影片 HEkjXNCB3g8 00:00-00:30",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.70, -3.52, 0], [0.70, 3.40, 0], color=HAIRLINE, stroke_width=1.5)

        wheel, nodes, offset_labels, today_label, direction = self.wheel_objects()
        wheel_context = VGroup(wheel, nodes, offset_labels, today_label, direction)

        # Beat 01 meet_week_wheel: establish today and the seven-day object.
        self.begin_beat("meet_week_wheel")
        stage_title = label("先看星期幾如何繞成一圈", 33, INK, "BOLD")
        stage_title.move_to([4.25, 3.02, 0])
        target_days = MathTex(r"2024^{112}", font_size=64, color=BLUE)
        opening_question = label("這麼多天後，會停在哪裡？", 31, POINT, "BOLD")
        opening_panel = VGroup(
            label("今天是星期三", 29, MUTED, "MEDIUM"),
            target_days,
            opening_question,
        ).arrange(DOWN, buff=0.58)
        opening_panel.move_to([4.25, -0.15, 0])
        marker = Dot(self.day_position(0), radius=0.145, color=POINT).set_z_index(8)

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Create(wheel), run_time=0.80)
        self.play(FadeIn(nodes), FadeIn(offset_labels), FadeIn(today_label), FadeIn(direction), run_time=0.70)
        self.play(GrowFromCenter(marker), run_time=0.42)
        self.play(LaggedStart(*(FadeIn(item) for item in opening_panel), lag_ratio=0.18), run_time=0.90)
        self.wait(0.40)

        # Beat 02 walk_one_week: a seven-day motion returns to the same node.
        self.next_beat("walk_one_week")
        next_title = label("走滿 7 天，正好回到原點", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        seven_day_count = VGroup(
            MathTex("7", font_size=48, color=REGION),
            label("天", 32, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.16)
        one_week = VGroup(
            seven_day_count,
            label("一個完整星期", 30, REGION, "BOLD"),
            label("星期幾沒有改變", 29, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.46)
        one_week.move_to([4.25, -0.10, 0])
        full_path = Arc(
            radius=self.WHEEL_RADIUS,
            start_angle=math.pi / 2,
            angle=-TAU,
            arc_center=self.WHEEL_CENTER,
        )
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(opening_panel), FadeIn(one_week[0]), run_time=0.45)
        self.play(
            MoveAlongPath(marker, full_path),
            run_time=2.25,
            rate_func=rate_functions.linear,
        )
        self.play(FadeIn(one_week[1]), Indicate(nodes[0], color=POINT), run_time=0.58)
        self.play(FadeIn(one_week[2]), run_time=0.45)
        self.wait(0.40)

        # Beat 03 compare_same_remainder: full weeks can be removed from day counts.
        self.next_beat("compare_same_remainder")
        next_title = label("8 天和 15 天，都只多走 1 格", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        examples = VGroup(
            MathTex(r"8=7+1", font_size=46, color=INK),
            MathTex(r"15=7\cdot2+1", font_size=46, color=INK),
            MathTex(r"8\equiv15\equiv1\pmod 7", font_size=43, color=REGION),
            label("完整星期拿掉後，都剩 1 天", 28, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.43)
        examples.move_to([4.25, -0.18, 0])
        one_step_path = Arc(
            radius=self.WHEEL_RADIUS,
            start_angle=math.pi / 2,
            angle=-TAU / WEEK_LENGTH,
            arc_center=self.WHEEL_CENTER,
        )
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(one_week), run_time=0.35)
        self.play(Write(examples[0]), Write(examples[1]), run_time=0.72)
        self.play(
            MoveAlongPath(marker, one_step_path),
            run_time=1.00,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(Write(examples[2]), run_time=0.62)
        self.play(FadeIn(examples[3]), Indicate(marker, color=POINT), run_time=0.58)
        self.wait(0.38)

        # Beat 04 ask_for_remainder: replace impossible counting with one small question.
        self.next_beat("ask_for_remainder")
        next_title = label("大數不用展開，只找除以 7 的餘數", 33, INK, "BOLD")
        next_title.move_to([0, 3.02, 0])
        target = MathTex(r"N=2024^{112}", font_size=60, color=BLUE)
        division_form = MathTex(r"N=7q+r", font_size=55, color=INK)
        remainder_range = MathTex(r"0\le r<7", font_size=40, color=MUTED)
        remainder_question = MathTex("r=?", font_size=70, color=POINT)
        remainder_panel = VGroup(target, division_form, remainder_range, remainder_question).arrange(
            DOWN, buff=0.48
        )
        remainder_panel.move_to([0, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(wheel_context),
            FadeOut(marker),
            FadeOut(examples),
            FadeOut(divider),
            run_time=0.60,
        )
        self.play(Write(target), run_time=0.58)
        self.play(Write(division_form), FadeIn(remainder_range), run_time=0.62)
        self.play(FadeIn(remainder_question), run_time=0.48)
        self.wait(0.48)

        # Beat 05 split_base_into_weeks: earn the base remainder from visible bundles.
        self.next_beat("split_base_into_weeks")
        next_title = label("先把 2024 拆成完整星期，再多 1 天", 33, INK, "BOLD")
        next_title.move_to([4.25, 3.02, 0])
        bundles = VGroup(
            self.week_bundle(REGION),
            self.week_bundle(REGION),
            self.week_bundle(REGION),
            MathTex(r"\cdots", font_size=40, color=MUTED),
            label("共 289 組", 25, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.18)
        bundles.move_to([-3.20, 0.30, 0])
        extra_day = VGroup(
            Dot(radius=0.13, color=POINT),
            label("多 1 天", 25, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.18)
        extra_day.move_to([-3.20, -1.25, 0])
        split_formula = MathTex(r"2024=2023+1", font_size=48, color=INK)
        weeks_formula = MathTex(r"2024=7\cdot289+1", font_size=48, color=INK)
        base_remainder = MathTex(r"2024\equiv1\pmod 7", font_size=54, color=REGION)
        split_note = label("底數本身只比完整星期多 1", 28, POINT, "BOLD")
        split_panel = VGroup(split_formula, weeks_formula, base_remainder, split_note).arrange(
            DOWN, buff=0.46
        )
        split_panel.move_to([4.15, -0.22, 0])
        divider = Line([0.70, -3.52, 0], [0.70, 3.40, 0], color=HAIRLINE, stroke_width=1.5)
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(remainder_panel), Create(divider), run_time=0.50)
        self.play(LaggedStart(*(FadeIn(item) for item in bundles), lag_ratio=0.10), run_time=0.80)
        self.play(FadeIn(extra_day), run_time=0.48)
        self.play(Write(split_formula), run_time=0.55)
        self.play(Write(weeks_formula), run_time=0.62)
        self.play(FadeIn(base_remainder), run_time=0.65)
        self.play(FadeIn(split_note), run_time=0.45)
        self.wait(0.38)

        # Beat 06 multiply_remainders: see why every 2024 factor becomes one.
        self.next_beat("multiply_remainders")
        next_title = label("相乘時，每個因數都只留下餘數 1", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        factor_tiles = VGroup(
            self.factor_tile("2024", BLUE),
            MathTex(r"\cdot", font_size=38, color=MUTED),
            self.factor_tile("2024", BLUE),
            MathTex(r"\cdot", font_size=38, color=MUTED),
            self.factor_tile("2024", BLUE),
        ).arrange(RIGHT, buff=0.18)
        factor_tiles.move_to([-3.25, 0.78, 0])
        remainder_tiles = VGroup(
            self.factor_tile("1", REGION),
            MathTex(r"\cdot", font_size=38, color=MUTED),
            self.factor_tile("1", REGION),
            MathTex(r"\cdot", font_size=38, color=MUTED),
            self.factor_tile("1", REGION),
        ).arrange(RIGHT, buff=0.18)
        remainder_tiles.move_to([-3.25, -0.78, 0])
        down_arrows = VGroup(
            *[
                Arrow(
                    factor_tiles[index].get_bottom() + DOWN * 0.08,
                    remainder_tiles[index].get_top() + UP * 0.08,
                    buff=0.06,
                    color=POINT,
                    stroke_width=3.5,
                    max_tip_length_to_length_ratio=0.20,
                )
                for index in (0, 2, 4)
            ]
        )
        power_two = MathTex(r"2024^2\equiv1\cdot1=1\pmod 7", font_size=40, color=INK)
        power_three = MathTex(r"2024^3\equiv1\cdot1\cdot1=1\pmod 7", font_size=38, color=INK)
        many_factors = VGroup(
            MathTex(r"\underbrace{2024\cdot\ldots\cdot2024}_{112}", font_size=38, color=BLUE),
            label("每個因數的餘數都是 1", 27, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.32)
        factor_panel = VGroup(power_two, power_three, many_factors).arrange(DOWN, buff=0.54)
        factor_panel.move_to([4.15, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(bundles), FadeOut(extra_day), FadeOut(split_panel), run_time=0.42)
        self.play(FadeIn(factor_tiles), run_time=0.55)
        self.play(Create(down_arrows), FadeIn(remainder_tiles), run_time=0.78)
        self.play(Write(power_two), run_time=0.62)
        self.play(Write(power_three), run_time=0.68)
        self.play(FadeIn(many_factors), run_time=0.62)
        self.wait(0.38)

        # Beat 07 compress_modular_result: write the short modular statement after the visual.
        self.next_beat("compress_modular_result")
        next_title = label("112 個餘數 1 相乘，仍然只剩 1", 33, INK, "BOLD")
        next_title.move_to([0, 3.02, 0])
        base_mod = MathTex(r"2024\equiv1\pmod 7", font_size=51, color=BLUE)
        power_mod = MathTex(
            r"2024^{112}",
            r"\equiv",
            r"1^{112}",
            r"\equiv",
            r"1",
            r"\pmod 7",
            font_size=53,
            color=INK,
        )
        power_mod[4].set_color(REGION)
        remainder_result = MathTex("r=1", font_size=72, color=POINT)
        modular_panel = VGroup(base_mod, power_mod, remainder_result).arrange(DOWN, buff=0.62)
        modular_panel.move_to([0, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(factor_tiles),
            FadeOut(remainder_tiles),
            FadeOut(down_arrows),
            FadeOut(factor_panel),
            FadeOut(divider),
            run_time=0.48,
        )
        self.play(Write(base_mod), run_time=0.55)
        self.play(Write(power_mod), run_time=0.82)
        self.play(GrowFromCenter(remainder_result), Circumscribe(remainder_result, color=POINT), run_time=0.78)
        self.wait(0.42)

        # Beat 08 read_full_weeks_plus_one: translate the congruence back to days.
        self.next_beat("read_full_weeks_plus_one")
        next_title = label("這代表很多個完整星期，再多 1 天", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        decomposition = MathTex(r"2024^{112}=7k+1", font_size=61, color=INK)
        k_integer = MathTex(r"k\in\mathbb{Z}", font_size=38, color=MUTED)
        week_band = RoundedRectangle(
            width=8.20,
            height=1.26,
            corner_radius=0.06,
            color=REGION,
            stroke_width=3,
            fill_color=REGION,
            fill_opacity=0.10,
        )
        week_band_label = label("k 個完整星期", 30, REGION, "BOLD").move_to(week_band)
        extra_dot = Dot(radius=0.16, color=POINT)
        extra_label = label("再多 1 天", 29, POINT, "BOLD")
        extra_group = VGroup(extra_dot, extra_label).arrange(RIGHT, buff=0.28)
        whole_visual = VGroup(VGroup(week_band, week_band_label), extra_group).arrange(
            RIGHT, buff=0.55
        )
        whole_visual.move_to([0, -1.28, 0])
        decomposition_group = VGroup(decomposition, k_integer).arrange(DOWN, buff=0.30)
        decomposition_group.move_to([0, 0.82, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(modular_panel), run_time=0.38)
        self.play(Write(decomposition), FadeIn(k_integer), run_time=0.72)
        self.play(FadeIn(week_band), FadeIn(week_band_label), run_time=0.58)
        self.play(FadeIn(extra_group), run_time=0.65)
        self.wait(0.40)

        # Beat 09 land_on_unknown_day: return to the wheel and stop before naming the day.
        self.next_beat("land_on_unknown_day")
        next_title = label("完整星期回到星期三，再前進 1 格", 33, INK, "BOLD")
        next_title.move_to([4.25, 3.02, 0])
        full_week_count = VGroup(
            MathTex("7k", font_size=46, color=REGION),
            label("天", 31, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.15)
        one_extra_day = VGroup(
            MathTex("+1", font_size=47, color=POINT),
            label("天", 31, POINT, "BOLD"),
        ).arrange(RIGHT, buff=0.15)
        preanswer_panel = VGroup(
            full_week_count,
            label("回到星期三", 28, REGION, "BOLD"),
            one_extra_day,
            label("下一格是？", 33, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.42)
        preanswer_panel.move_to([4.25, -0.18, 0])
        return_marker = Dot(self.day_position(0), radius=0.145, color=POINT).set_z_index(8)
        unknown = MathTex("?", font_size=54, color=CORAL)
        target_radial = self.day_position(1) - self.WHEEL_CENTER
        target_radial /= np.linalg.norm(target_radial)
        unknown.move_to(self.day_position(1) - target_radial * 0.43)
        one_step_path = Arc(
            radius=self.WHEEL_RADIUS,
            start_angle=math.pi / 2,
            angle=-TAU / WEEK_LENGTH,
            arc_center=self.WHEEL_CENTER,
        )
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(decomposition_group),
            FadeOut(whole_visual),
            FadeIn(divider),
            FadeIn(wheel_context),
            FadeIn(return_marker),
            run_time=0.72,
        )
        self.play(FadeIn(preanswer_panel[0]), FadeIn(preanswer_panel[1]), run_time=0.50)
        self.play(Circumscribe(wheel, color=REGION), run_time=0.72)
        self.play(FadeIn(preanswer_panel[2]), run_time=0.38)
        self.play(
            MoveAlongPath(return_marker, one_step_path),
            run_time=1.00,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(unknown), FadeIn(preanswer_panel[3]), run_time=0.52)
        self.play(Indicate(return_marker, color=POINT), run_time=0.52)
        self.wait(0.65)

        # Beat 10 reveal_thursday: name the one-step landing only after the pause.
        self.next_beat("reveal_thursday")
        next_title = label("星期三的下一格，就是星期四", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        thursday = label("星期四", 31, POINT, "BOLD")
        thursday.move_to(unknown)
        answer = label("答案：星期四", 46, POINT, "BOLD")
        answer_box = SurroundingRectangle(answer, color=POINT, buff=0.28, stroke_width=3.5)
        final_note = label("371 位數的天數，最後只需要走 1 格", 28, REGION, "BOLD")
        final_panel = VGroup(VGroup(answer_box, answer), final_note).arrange(DOWN, buff=0.58)
        final_panel.move_to([4.25, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(preanswer_panel), run_time=0.38)
        self.play(Succession(FadeOut(unknown), FadeIn(thursday)), run_time=0.55)
        self.play(FadeIn(answer_box), FadeIn(answer), run_time=0.65)
        self.play(FadeIn(final_note), Circumscribe(return_marker, color=POINT), run_time=0.72)
        self.wait(0.45)
