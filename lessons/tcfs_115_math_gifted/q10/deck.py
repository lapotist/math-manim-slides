"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q10."""

from __future__ import annotations

from fractions import Fraction

from carlo_manim import (
    BG,
    BLUE,
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
    AnimationGroup,
    Arrow,
    Circle,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


A_COLOR = BLUE
B_COLOR = REGION
C_COLOR = POINT
D_COLOR = PURPLE


class Tcfs115Q10Slide(CarloSlide):
    """Complete four bounds to one total, then compare exact interval endpoints."""

    lesson_id = "carlo.tcfs_115_math_gifted.q10"

    @staticmethod
    def raw_row(lhs: str, target: str, rhs: str, color: str, *, size: int = 37) -> MathTex:
        row = MathTex(lhs, "<", target, "<", rhs, font_size=size, color=INK)
        row[2].set_color(color)
        return row

    @staticmethod
    def coefficient_bound(
        left: str,
        right: str,
        color: str,
        *,
        size: int = 43,
    ) -> MathTex:
        row = MathTex(left, "<", "k", "<", right, font_size=size, color=INK)
        row[0].set_color(color)
        row[4].set_color(color)
        return row

    @staticmethod
    def normalized_bound(
        left: str,
        variable: str,
        right: str,
        color: str,
        *,
        size: int = 42,
    ) -> MathTex:
        row = MathTex(left, "<", variable, "<", right, font_size=size, color=INK)
        row[0].set_color(color).set_opacity(0.88)
        row[2].set_color(color)
        row[4].set_color(color).set_opacity(0.88)
        return row

    @staticmethod
    def total_model() -> VGroup:
        blocks = VGroup()
        for symbol, color in (
            ("a", A_COLOR),
            ("b", B_COLOR),
            ("c", C_COLOR),
            ("d", D_COLOR),
        ):
            body = Rectangle(
                width=1.35,
                height=0.66,
                color=color,
                stroke_width=3,
                fill_color=color,
                fill_opacity=0.16,
            )
            symbol_tex = MathTex(symbol, font_size=34, color=color).move_to(body)
            blocks.add(VGroup(body, symbol_tex))
        blocks.arrange(RIGHT, buff=0)
        outline = SurroundingRectangle(blocks, color=INK, buff=0.09, stroke_width=2.5)
        total = MathTex("k", font_size=39, color=INK).next_to(outline, RIGHT, buff=0.28)
        return VGroup(blocks, outline, total)

    @staticmethod
    def total_formula(*, size: int = 38) -> MathTex:
        formula = MathTex(
            "k",
            "=",
            "a",
            "+",
            "b",
            "+",
            "c",
            "+",
            "d",
            font_size=size,
            color=INK,
        )
        formula[2].set_color(A_COLOR)
        formula[4].set_color(B_COLOR)
        formula[6].set_color(C_COLOR)
        formula[8].set_color(D_COLOR)
        return formula

    @staticmethod
    def unit_x(value: Fraction) -> float:
        """Map an exact normalized value to the common horizontal scale."""
        minimum = Fraction(1, 8)
        maximum = Fraction(9, 20)
        proportion = (value - minimum) / (maximum - minimum)
        return -5.45 + float(proportion) * 10.9

    @classmethod
    def interval_band(
        cls,
        variable: str,
        left_value: Fraction,
        right_value: Fraction,
        left_tex: str,
        right_tex: str,
        color: str,
        y: float,
    ) -> VGroup:
        """Draw an open interval on the lesson-wide exact rational scale."""
        x_left = cls.unit_x(left_value)
        x_right = cls.unit_x(right_value)
        baseline = Line(
            [-5.55, y, 0],
            [5.55, y, 0],
            color=HAIRLINE,
            stroke_width=1.7,
        )
        ribbon = Rectangle(
            width=x_right - x_left,
            height=0.22,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.19,
        ).move_to([(x_left + x_right) / 2, y, 0])
        segment = Line(
            [x_left, y, 0],
            [x_right, y, 0],
            color=color,
            stroke_width=7,
        )
        left_dot = Circle(
            radius=0.085,
            color=color,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=1,
        ).move_to([x_left, y, 0])
        right_dot = left_dot.copy().move_to([x_right, y, 0])
        left_label = MathTex(left_tex, font_size=27, color=color)
        left_label.next_to(left_dot, UP, buff=0.11)
        right_label = MathTex(right_tex, font_size=27, color=color)
        right_label.next_to(right_dot, UP, buff=0.11)
        variable_label = MathTex(variable, font_size=35, color=color)
        variable_label.move_to([-6.15, y, 0])
        return VGroup(
            baseline,
            ribbon,
            segment,
            left_dot,
            right_dot,
            left_label,
            right_label,
            variable_label,
        )

    @classmethod
    def mini_band(
        cls,
        variable: str,
        left_value: Fraction,
        right_value: Fraction,
        left_tex: str,
        right_tex: str,
        color: str,
    ) -> VGroup:
        band = cls.interval_band(
            variable,
            left_value,
            right_value,
            left_tex,
            right_tex,
            color,
            0,
        )
        band.scale(0.54).move_to([2.55, -2.08, 0])
        return band

    @staticmethod
    def action_group(complement: str, color: str) -> VGroup:
        instruction = label("三邊同加", 23, MUTED, "MEDIUM")
        term = MathTex(rf"+\left({complement}\right)", font_size=32, color=color)
        return VGroup(instruction, term).arrange(RIGHT, buff=0.25)

    def construct(self) -> None:
        heading = label("第 10 題｜同一個總量排出四數順序", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學｜PDF 第 6 頁", 16, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        title_1 = label("先看四列：每一列都夾住一個主角", 34, INK, "BOLD")
        title_1.move_to(UP * 3.05)
        raw_rows = VGroup(
            self.raw_row(r"5b-c-d", "a", r"6b-c-d", A_COLOR),
            self.raw_row(r"\frac75c-a-d", "b", r"\frac85c-a-d", B_COLOR),
            self.raw_row(r"\frac72d-a-b", "c", r"\frac92d-a-b", C_COLOR),
            self.raw_row(r"\frac{14}{5}a-b-c", "d", r"\frac{16}{5}a-b-c", D_COLOR),
        ).arrange(DOWN, buff=0.52)
        raw_rows.move_to(UP * 0.1)
        row_numbers = VGroup(
            *(label(str(index), 20, MUTED, "BOLD") for index in range(1, 5))
        )
        for number, row in zip(row_numbers, raw_rows, strict=True):
            number.next_to(row, LEFT, buff=0.42)
        prompt_1 = label(
            "若不逐對硬比，四列能補成哪一個共同整體？",
            28,
            MUTED,
            "MEDIUM",
            t2c={"共同整體": POINT},
        ).move_to(DOWN * 2.72)

        # Beat 01 meet_four_bounds: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(title_1), run_time=0.75)
        self.play(
            LaggedStart(
                *(FadeIn(VGroup(number, row)) for number, row in zip(row_numbers, raw_rows, strict=True)),
                lag_ratio=0.16,
            ),
            run_time=1.6,
        )
        self.play(
            LaggedStart(
                *(Circumscribe(row[2], color=color) for row, color in zip(
                    raw_rows,
                    (A_COLOR, B_COLOR, C_COLOR, D_COLOR),
                    strict=True,
                )),
                lag_ratio=0.24,
            ),
            run_time=1.7,
        )
        self.play(FadeIn(prompt_1), run_time=0.55)
        self.wait(0.25)

        # Beat 02 name_shared_total: settled semantic step.
        self.next_slide()
        title_2 = label("把四個正數裝進同一個總量", 34, INK, "BOLD")
        title_2.move_to(title_1)
        total_model = self.total_model().move_to(UP * 1.82)
        total_formula = self.total_formula().move_to(UP * 1.02)
        positive = MathTex("k>0", font_size=35, color=POINT)
        positive.next_to(total_formula, RIGHT, buff=0.75)
        model_note = label("加法積木｜只表示組成，不代表大小", 19, MUTED, "MEDIUM")
        model_note.next_to(total_model, UP, buff=0.16)

        first_row = raw_rows[0]
        first_number = row_numbers[0]
        other_rows = VGroup(*raw_rows[1:], *row_numbers[1:])
        add_terms = VGroup(
            *(
                MathTex(r"+(b+c+d)", font_size=25, color=MUTED)
                for _ in range(3)
            )
        )
        added_row = MathTex(
            r"5b-c-d+(b+c+d)",
            "<",
            "k",
            "<",
            r"6b-c-d+(b+c+d)",
            font_size=31,
            color=INK,
        ).move_to(DOWN * 1.55)
        added_row.scale_to_fit_width(13.1)
        k_box = SurroundingRectangle(added_row[2], color=POINT, buff=0.14, stroke_width=3)
        completion_note = label(
            "中央的 a+(b+c+d) 正好補成 k",
            23,
            MUTED,
            "MEDIUM",
            t2c={"正好補成 k": POINT},
        ).next_to(added_row, DOWN, buff=0.28)

        self.play(
            ReplacementTransform(title_1, title_2),
            FadeOut(VGroup(other_rows, prompt_1)),
            first_row.animate.move_to(DOWN * 0.05),
            first_number.animate.next_to(first_row.copy().move_to(DOWN * 0.05), LEFT, buff=0.42),
            FadeIn(total_model),
            FadeIn(model_note),
            run_time=0.9,
        )
        self.play(Write(total_formula), FadeIn(positive), run_time=0.8)
        for term, x_position in zip(add_terms, (-3.45, 0.0, 3.45), strict=True):
            term.move_to([x_position, -0.68, 0])
        add_chips = VGroup(
            *(
                VGroup(
                    Rectangle(
                        width=2.25,
                        height=0.54,
                        color=HAIRLINE,
                        stroke_width=2,
                        fill_color=HAIRLINE,
                        fill_opacity=0.10,
                    ).move_to(term),
                    term,
                )
                for term in add_terms
            )
        )
        add_arrows = VGroup(
            *(
                Arrow(
                    component.get_bottom(),
                    chip.get_top(),
                    buff=0.08,
                    color=MUTED,
                    stroke_width=2.2,
                    tip_length=0.12,
                )
                for component, chip in zip(
                    (first_row[0], first_row[2], first_row[4]),
                    add_chips,
                    strict=True,
                )
            )
        )
        self.play(
            LaggedStart(*(FadeIn(chip, shift=DOWN * 0.08) for chip in add_chips), lag_ratio=0.18),
            Create(add_arrows),
            run_time=0.9,
        )
        # Beat 03 write_shared_total: settled semantic step.
        self.next_slide()
        self.play(
            TransformFromCopy(VGroup(first_row, add_terms, total_formula[0]), added_row),
            run_time=1.1,
        )
        self.play(Create(k_box), FadeIn(completion_note), run_time=0.65)
        self.wait(0.3)

        # Beat 04 normalize_b: settled semantic step.
        self.next_slide()
        title_3 = label("先把第一列完整走完", 34, INK, "BOLD").move_to(title_2)
        summary_header = label("已得到的比例範圍", 24, MUTED, "BOLD")
        summary_header.move_to([-4.65, 2.08, 0])
        divider = Line([-2.15, -2.55, 0], [-2.15, 2.32, 0], color=HAIRLINE, stroke_width=2)
        k_guard = MathTex(r"k=a+b+c+d>0", font_size=29, color=INK)
        k_guard.move_to([-4.65, 1.53, 0])
        k_guard.set_color_by_tex("k", POINT)
        simplify_note = label("收合同類項", 23, MUTED, "MEDIUM")
        simplify_note.move_to([2.45, 1.25, 0])
        coefficient_b = self.coefficient_bound("6b", "7b", B_COLOR, size=48)
        coefficient_b.move_to([2.45, 0.55, 0])
        divide_note_b = label("利用 k>0，改寫成 b 的上下界", 23, MUTED, "MEDIUM")
        divide_note_b.move_to([2.45, -0.23, 0])
        normalized_b = self.normalized_bound(r"\frac{k}{7}", "b", r"\frac{k}{6}", B_COLOR, size=47)
        normalized_b.move_to([2.45, -1.00, 0])
        b_summary = self.normalized_bound(r"\frac{k}{7}", "b", r"\frac{k}{6}", B_COLOR, size=29)
        b_summary.move_to([-4.65, 0.72, 0])
        b_mini = self.mini_band(
            "b",
            Fraction(1, 7),
            Fraction(1, 6),
            r"\frac17",
            r"\frac16",
            B_COLOR,
        )
        open_note = label("空心端點：嚴格不等式", 19, MUTED, "MEDIUM")
        open_note.next_to(b_mini, DOWN, buff=0.08)

        beat_2_context = VGroup(
            total_model,
            total_formula,
            positive,
            model_note,
            first_row,
            first_number,
            add_chips,
            add_arrows,
            k_box,
            completion_note,
        )
        self.play(
            ReplacementTransform(title_2, title_3),
            FadeOut(beat_2_context),
            added_row.animate.scale(0.78).move_to([2.45, 1.78, 0]),
            FadeIn(summary_header),
            Create(divider),
            FadeIn(k_guard),
            run_time=0.85,
        )
        self.play(FadeIn(simplify_note), ReplacementTransform(added_row, coefficient_b), run_time=0.9)
        self.play(FadeIn(divide_note_b), run_time=0.45)
        # Beat 05 finish_b_normalization: settled semantic step.
        self.next_slide()
        self.play(Write(normalized_b), run_time=0.9)
        self.play(TransformFromCopy(normalized_b, b_summary), run_time=0.65)
        self.play(
            FadeOut(VGroup(simplify_note, coefficient_b, divide_note_b, normalized_b)),
            FadeIn(b_mini),
            FadeIn(open_note),
            run_time=0.65,
        )
        self.wait(0.3)

        # Beat 06 normalize_c: settled semantic step.
        self.next_slide()
        title_4 = label("第二列也只是在補齊 k", 34, INK, "BOLD").move_to(title_3)
        raw_c = self.raw_row(r"\frac75c-a-d", "b", r"\frac85c-a-d", B_COLOR, size=34)
        raw_c.move_to([2.45, 1.48, 0]).scale_to_fit_width(8.1)
        action_c = self.action_group("a+c+d", C_COLOR).move_to([2.45, 0.72, 0])
        coefficient_c = self.coefficient_bound(
            r"\frac{12}{5}c",
            r"\frac{13}{5}c",
            C_COLOR,
            size=43,
        ).move_to([2.45, -0.05, 0])
        normalized_c = self.normalized_bound(
            r"\frac{5k}{13}",
            "c",
            r"\frac{5k}{12}",
            C_COLOR,
            size=44,
        ).move_to([2.45, -1.00, 0])
        c_summary = self.normalized_bound(
            r"\frac{5k}{13}",
            "c",
            r"\frac{5k}{12}",
            C_COLOR,
            size=29,
        ).move_to([-4.65, -0.15, 0])
        c_mini = self.mini_band(
            "c",
            Fraction(5, 13),
            Fraction(5, 12),
            r"\frac5{13}",
            r"\frac5{12}",
            C_COLOR,
        )

        self.play(
            ReplacementTransform(title_3, title_4),
            FadeOut(VGroup(b_mini, open_note)),
            b_summary.animate.set_opacity(0.38),
            FadeIn(raw_c),
            run_time=0.7,
        )
        self.play(FadeIn(action_c), run_time=0.55)
        self.play(Write(coefficient_c), run_time=0.85)
        # Beat 07 finish_c_normalization: settled semantic step.
        self.next_slide()
        self.play(Write(normalized_c), run_time=0.85)
        self.play(TransformFromCopy(normalized_c, c_summary), run_time=0.65)
        self.play(
            FadeOut(VGroup(raw_c, action_c, coefficient_c, normalized_c)),
            FadeIn(c_mini),
            b_summary.animate.set_opacity(1),
            run_time=0.65,
        )
        self.wait(0.3)

        # Beat 08 normalize_d: settled semantic step.
        self.next_slide()
        title_5 = label("第三列：d 的係數各增加 1", 34, INK, "BOLD").move_to(title_4)
        raw_d = self.raw_row(r"\frac72d-a-b", "c", r"\frac92d-a-b", C_COLOR, size=34)
        raw_d.move_to([2.45, 1.48, 0]).scale_to_fit_width(8.1)
        action_d = self.action_group("a+b+d", D_COLOR).move_to([2.45, 0.72, 0])
        coefficient_d = self.coefficient_bound(
            r"\frac92d",
            r"\frac{11}{2}d",
            D_COLOR,
            size=43,
        ).move_to([2.45, -0.05, 0])
        normalized_d = self.normalized_bound(
            r"\frac{2k}{11}",
            "d",
            r"\frac{2k}{9}",
            D_COLOR,
            size=44,
        ).move_to([2.45, -1.00, 0])
        d_summary = self.normalized_bound(
            r"\frac{2k}{11}",
            "d",
            r"\frac{2k}{9}",
            D_COLOR,
            size=29,
        ).move_to([-4.65, -1.02, 0])
        d_mini = self.mini_band(
            "d",
            Fraction(2, 11),
            Fraction(2, 9),
            r"\frac2{11}",
            r"\frac29",
            D_COLOR,
        )

        self.play(
            ReplacementTransform(title_4, title_5),
            FadeOut(c_mini),
            VGroup(b_summary, c_summary).animate.set_opacity(0.38),
            FadeIn(raw_d),
            run_time=0.7,
        )
        self.play(FadeIn(action_d), run_time=0.55)
        self.play(Write(coefficient_d), run_time=0.85)
        # Beat 09 finish_d_normalization: settled semantic step.
        self.next_slide()
        self.play(Write(normalized_d), run_time=0.85)
        self.play(TransformFromCopy(normalized_d, d_summary), run_time=0.65)
        self.play(
            FadeOut(VGroup(raw_d, action_d, coefficient_d, normalized_d)),
            FadeIn(d_mini),
            VGroup(b_summary, c_summary).animate.set_opacity(1),
            run_time=0.65,
        )
        self.wait(0.3)

        # Beat 10 normalize_a: settled semantic step.
        self.next_slide()
        title_6 = label("最後一列完成同一個模式", 34, INK, "BOLD").move_to(title_5)
        raw_a = self.raw_row(
            r"\frac{14}{5}a-b-c",
            "d",
            r"\frac{16}{5}a-b-c",
            D_COLOR,
            size=33,
        )
        raw_a.move_to([2.45, 1.48, 0]).scale_to_fit_width(8.1)
        action_a = self.action_group("a+b+c", A_COLOR).move_to([2.45, 0.72, 0])
        coefficient_a = self.coefficient_bound(
            r"\frac{19}{5}a",
            r"\frac{21}{5}a",
            A_COLOR,
            size=43,
        ).move_to([2.45, -0.05, 0])
        normalized_a = self.normalized_bound(
            r"\frac{5k}{21}",
            "a",
            r"\frac{5k}{19}",
            A_COLOR,
            size=44,
        ).move_to([2.45, -1.00, 0])
        a_summary = self.normalized_bound(
            r"\frac{5k}{21}",
            "a",
            r"\frac{5k}{19}",
            A_COLOR,
            size=29,
        ).move_to([-4.65, -1.89, 0])
        a_mini = self.mini_band(
            "a",
            Fraction(5, 21),
            Fraction(5, 19),
            r"\frac5{21}",
            r"\frac5{19}",
            A_COLOR,
        )

        self.play(
            ReplacementTransform(title_5, title_6),
            FadeOut(d_mini),
            VGroup(b_summary, c_summary, d_summary).animate.set_opacity(0.38),
            FadeIn(raw_a),
            run_time=0.7,
        )
        self.play(FadeIn(action_a), run_time=0.55)
        self.play(Write(coefficient_a), run_time=0.85)
        # Beat 11 finish_a_normalization: settled semantic step.
        self.next_slide()
        self.play(Write(normalized_a), run_time=0.85)
        self.play(TransformFromCopy(normalized_a, a_summary), run_time=0.65)
        self.play(
            FadeOut(VGroup(raw_a, action_a, coefficient_a, normalized_a)),
            FadeIn(a_mini),
            VGroup(b_summary, c_summary, d_summary).animate.set_opacity(1),
            run_time=0.65,
        )
        self.wait(0.3)

        # Beat 12 place_four_intervals: settled semantic step.
        self.next_slide()
        title_7 = label("同一把尺上，四段範圍落在哪裡？", 34, INK, "BOLD").move_to(title_6)
        coordinate_note = VGroup(
            label("共同座標", 22, MUTED, "BOLD"),
            label("每個數 ÷ k", 24, POINT, "BOLD"),
            MathTex("k>0", font_size=29, color=INK),
        ).arrange(RIGHT, buff=0.30).move_to(UP * 2.12)
        b_band = self.interval_band(
            "b",
            Fraction(1, 7),
            Fraction(1, 6),
            r"\frac17",
            r"\frac16",
            B_COLOR,
            1.08,
        )
        d_band = self.interval_band(
            "d",
            Fraction(2, 11),
            Fraction(2, 9),
            r"\frac2{11}",
            r"\frac29",
            D_COLOR,
            0.26,
        )
        a_band = self.interval_band(
            "a",
            Fraction(5, 21),
            Fraction(5, 19),
            r"\frac5{21}",
            r"\frac5{19}",
            A_COLOR,
            -0.56,
        )
        c_band = self.interval_band(
            "c",
            Fraction(5, 13),
            Fraction(5, 12),
            r"\frac5{13}",
            r"\frac5{12}",
            C_COLOR,
            -1.38,
        )
        bands = VGroup(b_band, d_band, a_band, c_band)
        summaries = VGroup(b_summary, d_summary, a_summary, c_summary)
        prompt_7 = label(
            "要保證前一段在左邊，只需比較哪兩個端點？",
            27,
            MUTED,
            "MEDIUM",
            t2c={"哪兩個端點": POINT},
        ).move_to(DOWN * 2.64)

        self.play(
            ReplacementTransform(title_6, title_7),
            FadeOut(VGroup(summary_header, divider, k_guard, a_mini)),
            summaries.animate.arrange(RIGHT, buff=0.48).scale(0.72).move_to(UP * 2.05),
            run_time=0.85,
        )
        self.play(FadeOut(summaries), FadeIn(coordinate_note), run_time=0.55)
        self.play(
            LaggedStart(
                *(
                    AnimationGroup(
                        FadeIn(VGroup(*band[0:5], band[7])),
                        TransformFromCopy(band[3], band[5]),
                        TransformFromCopy(band[4], band[6]),
                    )
                    for band in bands[:2]
                ),
                lag_ratio=0.3,
            ),
            run_time=1.1,
        )

        # Beat 13 finish_interval_bands: settled semantic step.
        self.next_slide()
        self.play(
            LaggedStart(
                *(
                    AnimationGroup(
                        FadeIn(VGroup(*band[0:5], band[7])),
                        TransformFromCopy(band[3], band[5]),
                        TransformFromCopy(band[4], band[6]),
                    )
                    for band in bands[2:]
                ),
                lag_ratio=0.3,
            ),
            run_time=1.1,
        )
        self.play(FadeIn(prompt_7), run_time=0.5)
        self.wait(0.3)

        # Beat 14 separate_b_d: settled semantic step.
        self.next_slide()
        title_8 = label("第一個空隙：b 的右端仍小於 d 的左端", 32, INK, "BOLD")
        title_8.move_to(title_7)
        compare_8 = MathTex(
            r"\frac16",
            "=",
            r"\frac{10}{60}",
            "<",
            r"\frac{10}{55}",
            "=",
            r"\frac2{11}",
            font_size=38,
            color=INK,
        ).move_to(UP * 2.08)
        compare_8[0:3].set_color(B_COLOR)
        compare_8[3].set_color(POINT)
        compare_8[4:7].set_color(D_COLOR)
        x_b_right = self.unit_x(Fraction(1, 6))
        x_d_left = self.unit_x(Fraction(2, 11))
        gap_8 = Rectangle(
            width=x_d_left - x_b_right,
            height=3.20,
            stroke_width=0,
            fill_color=POINT,
            fill_opacity=0.08,
        ).move_to([(x_b_right + x_d_left) / 2, -0.15, 0]).set_z_index(-1)
        gap_label_8 = label("空隙 1", 19, POINT, "BOLD")
        gap_label_8.move_to([(x_b_right + x_d_left) / 2, -1.91, 0])
        chain_8 = MathTex(
            "b",
            "<",
            r"\frac{k}{6}",
            "<",
            r"\frac{2k}{11}",
            "<",
            "d",
            font_size=40,
            color=INK,
        ).move_to(DOWN * 2.52)
        chain_8[0:3].set_color(B_COLOR)
        chain_8[3].set_color(POINT)
        chain_8[4:7].set_color(D_COLOR)

        self.play(
            ReplacementTransform(title_7, title_8),
            FadeOut(VGroup(coordinate_note, prompt_7)),
            a_band.animate.set_opacity(0.13),
            c_band.animate.set_opacity(0.13),
            run_time=0.65,
        )
        self.play(
            Indicate(VGroup(b_band[4], b_band[6]), color=B_COLOR),
            Indicate(VGroup(d_band[3], d_band[5]), color=D_COLOR),
            run_time=0.75,
        )
        self.play(Write(compare_8), FadeIn(gap_8), FadeIn(gap_label_8), run_time=0.9)
        self.play(Write(chain_8), run_time=0.85)
        self.wait(0.3)

        # Beat 15 separate_d_a: settled semantic step.
        self.next_slide()
        title_9 = label("第二個空隙：d 的右端仍小於 a 的左端", 32, INK, "BOLD")
        title_9.move_to(title_8)
        compare_9 = MathTex(
            r"\frac29",
            "=",
            r"\frac{10}{45}",
            "<",
            r"\frac{10}{42}",
            "=",
            r"\frac5{21}",
            font_size=38,
            color=INK,
        ).move_to(UP * 2.08)
        compare_9[0:3].set_color(D_COLOR)
        compare_9[3].set_color(POINT)
        compare_9[4:7].set_color(A_COLOR)
        x_d_right = self.unit_x(Fraction(2, 9))
        x_a_left = self.unit_x(Fraction(5, 21))
        gap_9 = Rectangle(
            width=x_a_left - x_d_right,
            height=3.20,
            stroke_width=0,
            fill_color=POINT,
            fill_opacity=0.08,
        ).move_to([(x_d_right + x_a_left) / 2, -0.15, 0]).set_z_index(-1)
        gap_label_9 = label("空隙 2", 19, POINT, "BOLD")
        gap_label_9.move_to([(x_d_right + x_a_left) / 2, -1.91, 0])
        chain_9 = MathTex(
            "b",
            "<",
            "d",
            "<",
            r"\frac{2k}{9}",
            "<",
            r"\frac{5k}{21}",
            "<",
            "a",
            font_size=39,
            color=INK,
        ).move_to(DOWN * 2.52)
        chain_9[0].set_color(B_COLOR)
        chain_9[2:5].set_color(D_COLOR)
        chain_9[5].set_color(POINT)
        chain_9[6:9].set_color(A_COLOR)

        self.play(
            ReplacementTransform(title_8, title_9),
            FadeOut(VGroup(compare_8, chain_8)),
            b_band.animate.set_opacity(0.13),
            d_band.animate.set_opacity(1),
            a_band.animate.set_opacity(1),
            gap_8.animate.set_opacity(0.32),
            gap_label_8.animate.set_opacity(0.38),
            run_time=0.7,
        )
        self.play(
            Indicate(VGroup(d_band[4], d_band[6]), color=D_COLOR),
            Indicate(VGroup(a_band[3], a_band[5]), color=A_COLOR),
            run_time=0.75,
        )
        self.play(Write(compare_9), FadeIn(gap_9), FadeIn(gap_label_9), run_time=0.9)
        self.play(Write(chain_9), run_time=0.85)
        self.wait(0.3)

        # Beat 16 separate_a_c: settled semantic step.
        self.next_slide()
        title_10 = label("最後一個空隙：共同正分子下比較分母", 32, INK, "BOLD")
        title_10.move_to(title_9)
        compare_10 = MathTex(
            r"\frac{5k}{19}",
            "<",
            r"\frac{5k}{13}",
            r"\qquad (k>0,\ 19>13)",
            font_size=39,
            color=INK,
        ).move_to(UP * 2.08)
        compare_10[0].set_color(A_COLOR)
        compare_10[1].set_color(POINT)
        compare_10[2].set_color(C_COLOR)
        compare_10[3].set_color(MUTED)
        x_a_right = self.unit_x(Fraction(5, 19))
        x_c_left = self.unit_x(Fraction(5, 13))
        gap_10 = Rectangle(
            width=x_c_left - x_a_right,
            height=3.20,
            stroke_width=0,
            fill_color=POINT,
            fill_opacity=0.055,
        ).move_to([(x_a_right + x_c_left) / 2, -0.15, 0]).set_z_index(-1)
        gap_label_10 = label("空隙 3", 19, POINT, "BOLD")
        gap_label_10.move_to([(x_a_right + x_c_left) / 2, -1.91, 0])
        chain_10 = MathTex(
            "a",
            "<",
            r"\frac{5k}{19}",
            "<",
            r"\frac{5k}{13}",
            "<",
            "c",
            font_size=40,
            color=INK,
        ).move_to(DOWN * 2.52)
        chain_10[0:3].set_color(A_COLOR)
        chain_10[3].set_color(POINT)
        chain_10[4:7].set_color(C_COLOR)
        ascending = MathTex(
            "b",
            "<",
            "d",
            "<",
            "a",
            "<",
            "c",
            font_size=46,
            color=INK,
        ).move_to(DOWN * 2.50)
        ascending[0].set_color(B_COLOR)
        ascending[2].set_color(D_COLOR)
        ascending[4].set_color(A_COLOR)
        ascending[6].set_color(C_COLOR)

        self.play(
            ReplacementTransform(title_9, title_10),
            FadeOut(VGroup(compare_9, chain_9)),
            d_band.animate.set_opacity(0.13),
            a_band.animate.set_opacity(1),
            c_band.animate.set_opacity(1),
            gap_9.animate.set_opacity(0.32),
            gap_label_9.animate.set_opacity(0.38),
            run_time=0.7,
        )
        self.play(
            Indicate(VGroup(a_band[4], a_band[6]), color=A_COLOR),
            Indicate(VGroup(c_band[3], c_band[5]), color=C_COLOR),
            run_time=0.75,
        )
        self.play(Write(compare_10), FadeIn(gap_10), FadeIn(gap_label_10), run_time=0.9)
        # Beat 17 compare_a_and_c: settled semantic step.
        self.next_slide()
        self.play(Write(chain_10), run_time=0.8)
        self.play(
            ReplacementTransform(chain_10, ascending),
            bands.animate.set_opacity(1),
            run_time=0.75,
        )
        self.wait(0.3)

        # Beat 18 consolidate: settled semantic step.
        self.next_slide()
        title_11 = label("同一把尺，讓順序自己排開", 34, INK, "BOLD").move_to(title_10)
        final_answer = MathTex(
            "c",
            ">",
            "a",
            ">",
            "d",
            ">",
            "b",
            font_size=66,
            color=INK,
        ).move_to(UP * 2.02)
        final_answer[0].set_color(C_COLOR)
        final_answer[2].set_color(A_COLOR)
        final_answer[4].set_color(D_COLOR)
        final_answer[6].set_color(B_COLOR)
        direction_note = label("由小到大", 20, MUTED, "MEDIUM")
        direction_note.move_to([0, -1.86, 0])
        recap = label(
            "補齊 k  →  放上共同尺度  →  比較三個相鄰空隙",
            25,
            MUTED,
            "MEDIUM",
            t2c={"k": POINT, "三個相鄰空隙": POINT},
        ).move_to(DOWN * 3.02)
        final_box = SurroundingRectangle(final_answer, color=POINT, buff=0.22, stroke_width=3)

        self.play(
            ReplacementTransform(title_10, title_11),
            FadeOut(compare_10),
            FadeOut(VGroup(gap_label_8, gap_label_9, gap_label_10)),
            ascending.animate.move_to(DOWN * 2.30),
            FadeIn(direction_note),
            run_time=0.7,
        )
        self.play(
            TransformFromCopy(ascending[6], final_answer[0]),
            FadeIn(final_answer[1]),
            TransformFromCopy(ascending[4], final_answer[2]),
            FadeIn(final_answer[3]),
            TransformFromCopy(ascending[2], final_answer[4]),
            FadeIn(final_answer[5]),
            TransformFromCopy(ascending[0], final_answer[6]),
            run_time=1.2,
        )
        self.play(Create(final_box), FadeIn(recap), Circumscribe(final_answer, color=POINT), run_time=0.9)
        self.wait(0.4)
