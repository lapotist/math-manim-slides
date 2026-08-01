"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q1."""

from __future__ import annotations

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    REGION,
    CarloSlide,
    label,
)
from manim import (
    Axes,
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
    Square,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


TARGET_EXPONENT = 11
SOLUTIONS = tuple(
    (x, y, z)
    for z in range(1, TARGET_EXPONENT + 1)
    for y in range(1, TARGET_EXPONENT + 1)
    for x in range(1, TARGET_EXPONENT + 1)
    if x + 2 * y + 3 * z == TARGET_EXPONENT
)
EXPECTED_SOLUTIONS = (
    (6, 1, 1),
    (4, 2, 1),
    (2, 3, 1),
    (3, 1, 2),
    (1, 2, 2),
)

if SOLUTIONS != EXPECTED_SOLUTIONS:
    raise ValueError(f"unexpected positive solutions: {SOLUTIONS}")


class CarloTcfs113MathQ01(CarloSlide):
    """Count positive exponent allocations by slicing a visible budget."""

    lesson_id = "carlo.tcfs_113_math_gifted.q01"

    SLOT_SIDE = 0.48
    SLOT_STEP = 0.57
    SLOT_START_X = -6.55
    SLOT_Y = 2.02

    @classmethod
    def slot_center(cls, index: int):
        return RIGHT * (cls.SLOT_START_X + cls.SLOT_STEP * index) + UP * cls.SLOT_Y

    @classmethod
    def budget_slots(cls) -> VGroup:
        return VGroup(
            *(
                Square(
                    side_length=cls.SLOT_SIDE,
                    color=MUTED,
                    stroke_width=2,
                    fill_opacity=0,
                ).move_to(cls.slot_center(index))
                for index in range(TARGET_EXPONENT)
            )
        )

    @classmethod
    def configuration(cls, x: int, y: int, z: int) -> VGroup:
        """Color consecutive exponent units in z, y, x order."""
        colors = [REGION] * (3 * z) + [BLUE] * (2 * y) + [POINT] * x
        return VGroup(
            *(
                Square(
                    side_length=cls.SLOT_SIDE * 0.84,
                    color=color,
                    stroke_width=1.5,
                    fill_color=color,
                    fill_opacity=0.58,
                )
                .move_to(cls.slot_center(index))
                .set_z_index(3)
                for index, color in enumerate(colors)
            )
        )

    @staticmethod
    def tuple_readout(x: int, y: int, z: int, *, size: int = 38) -> MathTex:
        result = MathTex(
            r"(x,y,z)=",
            "(",
            str(x),
            ",",
            str(y),
            ",",
            str(z),
            ")",
            font_size=size,
            color=INK,
        )
        result[2].set_color(POINT if x > 0 else CORAL)
        result[4].set_color(BLUE)
        result[6].set_color(REGION)
        return result

    @staticmethod
    def solution_tuple(x: int, y: int, z: int) -> MathTex:
        result = MathTex(
            "(",
            str(x),
            ",",
            str(y),
            ",",
            str(z),
            ")",
            font_size=29,
            color=INK,
        )
        result[1].set_color(POINT)
        result[3].set_color(BLUE)
        result[5].set_color(REGION)
        return result

    @staticmethod
    def slice_line(axes: Axes, remaining: int, color: str) -> Line:
        y_end = min(4.0, remaining / 2)
        return Line(
            axes.c2p(0, remaining),
            axes.c2p(y_end, remaining - 2 * y_end),
            color=color,
            stroke_width=4,
        ).set_z_index(2)

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    def construct(self) -> None:
        heading = label("第 1 題｜11 格要怎麼分？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 1 頁｜影片 FSGAuRvRFU0",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line(
            [0.76, -3.72, 0],
            [0.76, 3.28, 0],
            color=HAIRLINE,
            stroke_width=1.5,
        )

        # Beat 01: begin with the actual power puzzle and no counting machinery.
        self.begin_beat("meet_power_puzzle")
        beat_title = label("有幾組有順序的正整數？", 34, INK, "BOLD")
        beat_title.move_to([4.42, 2.48, 0])
        original_equation = MathTex(
            "2^x",
            r"\times",
            "4^y",
            r"\times",
            "8^z",
            "=",
            "2048",
            font_size=60,
            color=INK,
        ).move_to([-3.08, 0.55, 0])
        original_equation[0].set_color(POINT)
        original_equation[2].set_color(BLUE)
        original_equation[4].set_color(REGION)
        positive_note = VGroup(
            label("三個位置都有角色", 28, MUTED, "MEDIUM"),
            MathTex(r"x,y,z\in\mathbb Z_{>0}", font_size=39, color=INK),
        ).arrange(DOWN, buff=0.3).move_to([4.42, 0.72, 0])
        order_note = label("交換位置會變成另一組答案", 26, CORAL, "BOLD")
        order_note.move_to([4.42, -0.72, 0])
        opening_question = label("先別乘開；哪一種量可以直接比較？", 24, MUTED, "MEDIUM")
        opening_question.move_to([4.42, -1.72, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(beat_title), FadeIn(original_equation), run_time=1.15)
        self.play(FadeIn(positive_note), run_time=0.7)
        self.play(FadeIn(order_note), FadeIn(opening_question), run_time=0.65)
        self.wait(0.3)

        # Beat 02: rewrite every base as 2 before talking about exponents.
        self.next_beat("make_bases_equal")
        next_title = label("先把底數都換成 2", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        expanded_equation = MathTex(
            "2^x",
            r"\times",
            r"(2^2)^y",
            r"\times",
            r"(2^3)^z",
            "=",
            r"2^{11}",
            font_size=54,
            color=INK,
        ).move_to([-3.08, 0.55, 0])
        expanded_equation[0].set_color(POINT)
        expanded_equation[2].set_color(BLUE)
        expanded_equation[4].set_color(REGION)
        conversions = MathTex(
            "4=2^2",
            r"\qquad",
            "8=2^3",
            r"\qquad",
            "2048=2^{11}",
            font_size=37,
            color=INK,
        ).move_to([-3.08, -1.08, 0])
        conversions[0].set_color(BLUE)
        conversions[2].set_color(REGION)
        base_note = label("同底數以後，只要比較指數", 28, POINT, "BOLD")
        base_note.move_to([4.42, 0.45, 0])

        self.play(
            self.title_change(beat_title, next_title),
            Succession(FadeOut(original_equation), FadeIn(expanded_equation)),
            FadeOut(positive_note),
            FadeOut(order_note),
            FadeOut(opening_question),
            run_time=1.0,
        )
        original_equation = expanded_equation
        beat_title = next_title
        self.play(FadeIn(conversions), run_time=0.9)
        self.play(FadeIn(base_note), run_time=0.55)
        self.wait(0.3)

        # Beat 03: make the exponent equation a physical eleven-unit budget.
        self.next_beat("build_exponent_budget")
        next_title = label("把指數 11 看成一排預算", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        budget_equation = MathTex(
            "x",
            "+",
            "2y",
            "+",
            "3z",
            "=",
            "11",
            font_size=49,
            color=INK,
        ).move_to([4.42, 1.26, 0])
        budget_equation[0].set_color(POINT)
        budget_equation[2].set_color(BLUE)
        budget_equation[4].set_color(REGION)
        slots = self.budget_slots()
        baseline_tiles = self.configuration(1, 1, 1)

        def legend_entry(symbol: str, units: int, color: str):
            sample = VGroup(
                *(
                    Square(
                        side_length=0.24,
                        color=color,
                        stroke_width=1.2,
                        fill_color=color,
                        fill_opacity=0.58,
                    )
                    for _ in range(units)
                )
            ).arrange(RIGHT, buff=0.035)
            math = MathTex(symbol, font_size=32, color=color)
            prose = label(f"每增加 1，就占 {units} 格", 22, MUTED, "MEDIUM")
            return VGroup(sample, math, prose).arrange(RIGHT, buff=0.14)

        legend = VGroup(
            legend_entry("x", 1, POINT),
            legend_entry("y", 2, BLUE),
            legend_entry("z", 3, REGION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        legend.move_to([4.42, -0.48, 0])
        positivity = VGroup(
            label("正整數：三種顏色至少各放一組", 25, INK, "BOLD"),
            label("先各放 1 組，已經用了 6 格", 23, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.22).move_to([-3.28, 0.98, 0])

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(conversions),
            FadeOut(base_note),
            FadeOut(original_equation),
            FadeIn(budget_equation),
            LaggedStart(*(Create(slot) for slot in slots), lag_ratio=0.05),
            run_time=1.25,
        )
        beat_title = next_title
        self.play(FadeIn(legend), run_time=0.7)
        self.play(
            LaggedStart(*(GrowFromCenter(tile) for tile in baseline_tiles), lag_ratio=0.08),
            FadeIn(positivity),
            run_time=0.9,
        )
        self.wait(0.3)

        # Build the lattice once; later slices only change its line and points.
        axes = Axes(
            x_range=[0, 4.2, 1],
            y_range=[0, 8.5, 1],
            x_length=5.05,
            y_length=3.12,
            axis_config={
                "color": MUTED,
                "stroke_width": 2,
                "include_tip": False,
                "include_ticks": False,
            },
        ).move_to([-3.65, -1.19, 0])
        lattice = VGroup(
            *(
                Dot(axes.c2p(y, x), radius=0.022, color=HAIRLINE)
                for y in range(1, 5)
                for x in range(0, 9)
            )
        )
        x_ticks = VGroup(
            *(
                MathTex(str(value), font_size=18, color=MUTED).next_to(
                    axes.c2p(0, value), LEFT, buff=0.09
                )
                for value in (0, 2, 4, 6, 8)
            )
        )
        y_ticks = VGroup(
            *(
                MathTex(str(value), font_size=18, color=MUTED).next_to(
                    axes.c2p(value, 0), DOWN, buff=0.08
                )
                for value in range(1, 5)
            )
        )
        axis_labels = VGroup(
            MathTex("y", font_size=25, color=BLUE).next_to(
                axes.x_axis.get_end(), DOWN, buff=0.08
            ),
            MathTex("x", font_size=25, color=POINT).next_to(
                axes.y_axis.get_end(), LEFT, buff=0.08
            ),
        )

        # Beat 04: hold z=1 and discover three positive lattice points by packing.
        self.next_beat("explore_z_one")
        next_title = label("第一層：先固定 z = 1", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        z_one_equations = VGroup(
            MathTex("z=1", font_size=39, color=REGION),
            MathTex("x", "+", "2y", "=", "8", font_size=45, color=INK),
        ).arrange(DOWN, buff=0.22).move_to([4.42, 0.83, 0])
        z_one_equations[1][0].set_color(POINT)
        z_one_equations[1][2].set_color(BLUE)
        config_readout = self.tuple_readout(6, 1, 1).move_to([4.42, -0.24, 0])
        change_note = label("y 多 1，x 就少 2", 26, BLUE, "BOLD")
        change_note.move_to([4.42, -1.12, 0])
        lattice_note = label("每個亮點是一組正整數解", 22, MUTED, "MEDIUM")
        lattice_note.move_to([-3.65, 0.63, 0])
        slice_line = self.slice_line(axes, 8, BLUE)
        z_one_dots = VGroup()

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(legend),
            FadeOut(positivity),
            FadeOut(budget_equation),
            FadeIn(z_one_equations),
            Create(axes),
            FadeIn(lattice),
            FadeIn(x_ticks),
            FadeIn(y_ticks),
            FadeIn(axis_labels),
            FadeIn(lattice_note),
            Create(slice_line),
            Transform(baseline_tiles, self.configuration(6, 1, 1)),
            FadeIn(config_readout),
            run_time=1.25,
        )
        beat_title = next_title
        first_dot = Dot(axes.c2p(1, 6), radius=0.09, color=POINT).set_z_index(6)
        z_one_dots.add(first_dot)
        self.play(GrowFromCenter(first_dot), run_time=0.45)
        self.play(FadeIn(change_note), run_time=0.4)

        self.next_beat("continue_z_one_slice")
        for x, y in ((4, 2), (2, 3)):
            next_readout = self.tuple_readout(x, y, 1).move_to(config_readout)
            dot = Dot(axes.c2p(y, x), radius=0.09, color=POINT).set_z_index(6)
            self.play(
                Transform(baseline_tiles, self.configuration(x, y, 1)),
                Succession(FadeOut(config_readout), FadeIn(next_readout)),
                run_time=0.75,
            )
            config_readout = next_readout
            self.play(GrowFromCenter(dot), run_time=0.38)
            z_one_dots.add(dot)
        self.wait(0.3)

        # Beat 05: test the tempting endpoint x=0 before counting the slice.
        self.next_beat("guard_positive_endpoint")
        next_title = label("再放一組 y，會碰到哪個邊界？", 32, INK, "BOLD")
        next_title.move_to(beat_title)
        zero_readout = self.tuple_readout(0, 4, 1).move_to(config_readout)
        invalid_dot = Circle(
            radius=0.105,
            color=CORAL,
            stroke_width=3,
        ).move_to(axes.c2p(4, 0)).set_z_index(7)
        positive_guard = VGroup(
            label("這格剛好填滿，但", 25, MUTED, "MEDIUM"),
            MathTex("x=0", font_size=39, color=CORAL),
        ).arrange(RIGHT, buff=0.18).move_to([4.42, -1.18, 0])
        slice_one_count = MathTex(
            "z=1",
            r"\Longrightarrow",
            "3",
            font_size=44,
            color=INK,
        ).move_to([4.42, -2.16, 0])
        slice_one_count[0].set_color(REGION)
        slice_one_count[2].set_color(POINT)

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(change_note),
            Transform(baseline_tiles, self.configuration(0, 4, 1)),
            Succession(FadeOut(config_readout), FadeIn(zero_readout)),
            GrowFromCenter(invalid_dot),
            run_time=0.9,
        )
        config_readout = zero_readout
        beat_title = next_title
        self.play(FadeIn(positive_guard), run_time=0.55)
        self.play(
            Circumscribe(z_one_dots, color=POINT, fade_out=True),
            FadeIn(slice_one_count),
            run_time=0.85,
        )
        self.wait(0.3)

        # Beat 06: spend six units on z and repeat the same packing motion.
        self.next_beat("explore_z_two")
        next_title = label("第二層：把 z 增加到 2", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        z_two_equations = VGroup(
            MathTex("z=2", font_size=39, color=REGION),
            MathTex("x", "+", "2y", "=", "5", font_size=45, color=INK),
        ).arrange(DOWN, buff=0.22).move_to(z_one_equations)
        z_two_equations[1][0].set_color(POINT)
        z_two_equations[1][2].set_color(BLUE)
        line_two = self.slice_line(axes, 5, REGION)
        first_two_readout = self.tuple_readout(3, 1, 2).move_to(config_readout)
        z_two_dots = VGroup()
        slice_two_note = label("只剩一格 x 時，就不能再加 y", 24, MUTED, "MEDIUM")
        slice_two_note.move_to([4.42, -1.13, 0])
        slice_two_count = MathTex(
            "z=2",
            r"\Longrightarrow",
            "2",
            font_size=44,
            color=INK,
        ).move_to([4.42, -2.16, 0])
        slice_two_count[0].set_color(REGION)
        slice_two_count[2].set_color(POINT)

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(positive_guard),
            FadeOut(slice_one_count),
            FadeOut(invalid_dot),
            Succession(FadeOut(z_one_equations), FadeIn(z_two_equations)),
            Transform(slice_line, line_two),
            Transform(baseline_tiles, self.configuration(3, 1, 2)),
            Succession(FadeOut(config_readout), FadeIn(first_two_readout)),
            z_one_dots.animate.set_opacity(0.25),
            run_time=1.05,
        )
        z_one_equations = z_two_equations
        config_readout = first_two_readout
        beat_title = next_title
        fourth_dot = Dot(axes.c2p(1, 3), radius=0.09, color=POINT).set_z_index(6)
        z_two_dots.add(fourth_dot)
        self.play(GrowFromCenter(fourth_dot), run_time=0.4)

        self.next_beat("complete_z_two_slice")
        second_two_readout = self.tuple_readout(1, 2, 2).move_to(config_readout)
        fifth_dot = Dot(axes.c2p(2, 1), radius=0.09, color=POINT).set_z_index(6)
        self.play(
            Transform(baseline_tiles, self.configuration(1, 2, 2)),
            Succession(FadeOut(config_readout), FadeIn(second_two_readout)),
            run_time=0.75,
        )
        config_readout = second_two_readout
        self.play(GrowFromCenter(fifth_dot), FadeIn(slice_two_note), run_time=0.5)
        z_two_dots.add(fifth_dot)
        self.play(
            Circumscribe(z_two_dots, color=POINT, fade_out=True),
            FadeIn(slice_two_count),
            run_time=0.8,
        )
        self.wait(0.3)

        # Beat 07: test z=3 at the minimum positive x and y, exposing overflow.
        self.next_beat("test_z_three_boundary")
        next_title = label("第三層：最省也要 12 格", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        overflow_frame = Square(
            side_length=self.SLOT_SIDE,
            color=CORAL,
            stroke_width=3,
            fill_color=CORAL,
            fill_opacity=0.08,
        ).move_to(self.slot_center(11)).set_z_index(1)
        line_three = self.slice_line(axes, 2, CORAL)
        minimum_dot = Dot(axes.c2p(1, 1), radius=0.085, color=CORAL).set_z_index(7)
        z_three_equations = VGroup(
            MathTex("z=3", font_size=39, color=REGION),
            MathTex("x+2y=2", font_size=43, color=INK),
            MathTex(r"x+2y\ge3", font_size=40, color=CORAL),
        ).arrange(DOWN, buff=0.2).move_to([4.42, 0.72, 0])
        overflow_equation = MathTex(
            "1",
            "+",
            "2",
            "+",
            "9",
            "=",
            "12",
            ">",
            "11",
            font_size=43,
            color=INK,
        ).move_to([4.42, -1.18, 0])
        overflow_equation[0].set_color(POINT)
        overflow_equation[2].set_color(BLUE)
        overflow_equation[4].set_color(REGION)
        overflow_equation[6].set_color(CORAL)
        no_later_slices = MathTex(
            r"z\ge3",
            r"\Longrightarrow",
            "0",
            font_size=43,
            color=INK,
        ).move_to([4.42, -2.15, 0])
        no_later_slices[0].set_color(REGION)
        no_later_slices[2].set_color(CORAL)

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(slice_two_note),
            FadeOut(slice_two_count),
            FadeOut(z_one_equations),
            FadeOut(config_readout),
            FadeIn(z_three_equations),
            Transform(slice_line, line_three),
            FadeIn(overflow_frame),
            Transform(baseline_tiles, self.configuration(1, 1, 3)),
            GrowFromCenter(minimum_dot),
            z_two_dots.animate.set_opacity(0.25),
            run_time=1.15,
        )
        beat_title = next_title
        self.play(FadeIn(overflow_equation), run_time=0.75)
        self.play(FadeIn(no_later_slices), Indicate(overflow_frame), run_time=0.75)
        self.wait(0.3)

        # Beat 08: only now combine the two surviving slice counts.
        self.next_beat("combine_slice_counts")
        next_title = label("把留下來的兩層合在一起", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        first_summary = MathTex(
            "z=1",
            r"\Longrightarrow",
            "3",
            font_size=38,
            color=INK,
        )
        second_summary = MathTex(
            "z=2",
            r"\Longrightarrow",
            "2",
            font_size=38,
            color=INK,
        )
        third_summary = MathTex(
            r"z\ge3",
            r"\Longrightarrow",
            "0",
            font_size=38,
            color=INK,
        )
        for summary, count_color in (
            (first_summary, POINT),
            (second_summary, POINT),
            (third_summary, CORAL),
        ):
            summary[0].set_color(REGION)
            summary[2].set_color(count_color)
        summaries = VGroup(first_summary, second_summary, third_summary)
        summaries.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.42, 0.56, 0])
        final_sum = MathTex(
            "3",
            "+",
            "2",
            "+",
            "0",
            "=",
            "5",
            font_size=53,
            color=INK,
        ).move_to([4.42, -1.48, 0])
        final_sum[0].set_color(POINT)
        final_sum[2].set_color(POINT)
        final_sum[4].set_color(CORAL)
        final_sum[6].set_color(POINT)
        result_box = SurroundingRectangle(
            final_sum,
            color=POINT,
            buff=0.16,
            corner_radius=0.08,
            stroke_width=3,
        )
        result_note = label("每個亮點就是一個有順序的三元組", 24, MUTED, "MEDIUM")
        result_note.move_to([4.42, -2.48, 0])

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(z_three_equations),
            FadeOut(overflow_equation),
            FadeOut(no_later_slices),
            FadeOut(overflow_frame),
            FadeOut(baseline_tiles),
            FadeOut(slice_line),
            FadeOut(minimum_dot),
            z_one_dots.animate.set_opacity(1),
            z_two_dots.animate.set_opacity(1),
            FadeIn(summaries),
            run_time=1.0,
        )
        beat_title = next_title
        self.play(FadeIn(final_sum[0:5]), run_time=0.65)
        self.wait(0.35)

        self.next_beat("reveal_slice_total")
        self.play(FadeIn(final_sum[5:7]), Create(result_box), run_time=0.7)
        self.play(FadeIn(result_note), run_time=0.45)
        self.wait(0.3)

        # Beat 09: reconnect the five points to ordered triples and the original powers.
        self.next_beat("return_to_original")
        next_title = label("五個點，正好是五個三元組", 34, INK, "BOLD")
        next_title.move_to(beat_title)
        original_return = MathTex(
            "2^x",
            r"\times",
            "4^y",
            r"\times",
            "8^z",
            "=",
            "2048",
            font_size=39,
            color=INK,
        ).move_to([-3.28, 2.02, 0])
        original_return[0].set_color(POINT)
        original_return[2].set_color(BLUE)
        original_return[4].set_color(REGION)
        tuple_objects = [self.solution_tuple(*triple) for triple in SOLUTIONS]
        first_row = VGroup(*tuple_objects[:3]).arrange(RIGHT, buff=0.34)
        second_row = VGroup(*tuple_objects[3:]).arrange(RIGHT, buff=0.52)
        tuple_grid = VGroup(first_row, second_row).arrange(DOWN, buff=0.34)
        tuple_grid.move_to([4.42, 0.18, 0])
        verification = MathTex(
            "1",
            "+",
            "2(2)",
            "+",
            "3(2)",
            "=",
            "11",
            font_size=39,
            color=INK,
        ).move_to([4.42, -1.43, 0])
        verification[0].set_color(POINT)
        verification[2].set_color(BLUE)
        verification[4].set_color(REGION)
        final_note = label("因此共有 5 組正整數有序三元組", 27, POINT, "BOLD")
        final_note.move_to([4.42, -2.45, 0])
        all_points = [*z_one_dots, *z_two_dots]

        self.play(
            self.title_change(beat_title, next_title),
            FadeOut(summaries),
            FadeOut(result_note),
            FadeOut(slots),
            FadeIn(original_return),
            final_sum.animate.scale(0.78).move_to([4.42, 1.39, 0]),
            result_box.animate.scale(0.78).move_to([4.42, 1.39, 0]),
            run_time=0.9,
        )
        beat_title = next_title
        for point, tuple_object in zip(
            (all_points[0], all_points[1]),
            (tuple_objects[0], tuple_objects[1]),
            strict=True,
        ):
            self.play(Indicate(point, color=POINT), FadeIn(tuple_object), run_time=0.38)

        self.next_beat("reveal_remaining_solution_tuples")
        for point, tuple_object in zip(
            (all_points[2], all_points[3], all_points[4]),
            (tuple_objects[2], tuple_objects[3], tuple_objects[4]),
            strict=True,
        ):
            self.play(Indicate(point, color=POINT), FadeIn(tuple_object), run_time=0.38)

        self.next_beat("verify_solution_total")
        self.play(FadeIn(verification), run_time=0.65)
        self.play(FadeIn(final_note), Circumscribe(result_box, color=POINT), run_time=0.7)
        self.wait(0.4)
