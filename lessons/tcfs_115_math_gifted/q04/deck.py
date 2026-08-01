"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q4."""

from __future__ import annotations

import numpy as np

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    REGION,
    REGION_DARK,
    CarloSlide,
    label,
)
from manim import (
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    LaggedStart,
    Line,
    NumberLine,
    Polygon,
    Rectangle,
    ReplacementTransform,
    Square,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, ORIGIN, RIGHT, UP


class CarloTcfs115MathQ04(CarloSlide):
    """Compress a one-hundred-step ant walk into twenty-five blocks."""

    lesson_id = "carlo.tcfs_115_math_gifted.q04"

    @staticmethod
    def signed_term(tex: str, color: str, *, width: float = 1.35) -> VGroup:
        box = Rectangle(
            width=width,
            height=0.72,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.09,
        )
        term = label(tex, 32, color, "BOLD")
        return VGroup(box, term)

    @classmethod
    def term_group(cls, numbers: tuple[int, int, int, int]) -> VGroup:
        signs = ("+", "-", "-", "+")
        colors = (REGION, CORAL, CORAL, REGION)
        terms = VGroup(
            *(
                cls.signed_term(f"{sign}{number}²", color)
                for sign, number, color in zip(signs, numbers, colors, strict=True)
            )
        ).arrange(RIGHT, buff=0.08)
        bracket = Line(
            terms.get_corner(DOWN + LEFT) + DOWN * 0.13,
            terms.get_corner(DOWN + RIGHT) + DOWN * 0.13,
            color=POINT,
            stroke_width=4,
        )
        return VGroup(terms, bracket)

    @staticmethod
    def block(*, width: float = 1.0, height: float = 0.48) -> VGroup:
        body = Rectangle(
            width=width,
            height=height,
            color=REGION,
            stroke_width=2,
            fill_color=REGION_DARK,
            fill_opacity=0.88,
        )
        text = label("+4", 23, INK, "BOLD")
        return VGroup(body, text)

    @staticmethod
    def square_gap(
        outer_side: int,
        inner_side: int,
        color: str,
        *,
        scale: float,
    ) -> VGroup:
        outer_length = outer_side * scale
        inner_length = inner_side * scale
        outer = Square(outer_length, color=INK, stroke_width=3)
        outer.move_to(ORIGIN)
        lower_left = outer.get_corner(DOWN + LEFT)
        inner = Square(inner_length, color=MUTED, stroke_width=3)
        inner.move_to(lower_left + (RIGHT + UP) * inner_length / 2)

        x0, y0, _ = lower_left
        x1 = x0 + inner_length
        x2 = x0 + outer_length
        y1 = y0 + inner_length
        y2 = y0 + outer_length
        band = Polygon(
            np.array([x0, y1, 0]),
            np.array([x1, y1, 0]),
            np.array([x1, y0, 0]),
            np.array([x2, y0, 0]),
            np.array([x2, y2, 0]),
            np.array([x0, y2, 0]),
            color=color,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.65,
        )
        outer_label = label(str(outer_side), 24, INK, "BOLD")
        outer_label.next_to(outer, RIGHT, buff=0.12)
        inner_label = label(str(inner_side), 22, MUTED, "BOLD")
        inner_label.move_to(inner.get_center())
        return VGroup(band, outer, inner, outer_label, inner_label)

    def construct(self) -> None:
        heading = label("第 4 題｜螞蟻最後停在哪裡？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.4)
        source = label("解題來源：正哥愛數學", 18, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.28)

        number_line = NumberLine(
            x_range=[-13, 5, 1],
            length=12.7,
            include_ticks=True,
            tick_size=0.055,
            include_tip=True,
            color=MUTED,
            stroke_width=2.5,
        ).move_to(DOWN * 1.28)
        number_labels = VGroup()
        for value in (-12, -3, 0, 1, 4):
            number = label(str(value), 23, INK, "MEDIUM")
            number.next_to(number_line.n2p(value), DOWN, buff=0.17)
            number_labels.add(number)

        ant = Dot(number_line.n2p(0), radius=0.105, color=POINT).set_z_index(5)
        ant_label = label("螞蟻", 23, POINT, "BOLD").next_to(ant, DOWN, buff=0.5)
        first_arrow = Arrow(
            number_line.n2p(0) + UP * 0.28,
            number_line.n2p(1) + UP * 0.28,
            buff=0.02,
            color=REGION,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.28,
        )
        first_move = label("+1²", 31, REGION, "BOLD")
        first_move.next_to(first_arrow, UP, buff=0.12)
        first_prompt = label(
            "第 1 次：向右走 1²",
            35,
            INK,
            "BOLD",
            t2c={"向右": REGION},
        ).move_to(UP * 1.55)
        direction_note = label("向右記作正", 23, REGION, "MEDIUM")
        direction_note.next_to(first_prompt, DOWN, buff=0.18)

        # Beat 01 start_at_one: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), Create(number_line), run_time=1.0)
        self.play(FadeIn(number_labels), FadeIn(ant), FadeIn(ant_label), run_time=0.7)
        self.play(
            GrowArrow(first_arrow),
            ant.animate.move_to(number_line.n2p(1)),
            ant_label.animate.next_to(number_line.n2p(1), DOWN, buff=0.5),
            run_time=1.25,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(first_move), FadeIn(first_prompt), FadeIn(direction_note))

        # Beat 02 walk_first_block: settled semantic step.
        self.next_slide()

        self.play(FadeOut(first_prompt), FadeOut(direction_note), run_time=0.45)

        move_specs = (
            (1, -3, "−2²", CORAL, 0.72),
            (-3, -12, "−3²", CORAL, 1.2),
            (-12, 4, "+4²", REGION, 1.55),
        )
        move_arrows = VGroup(first_arrow)
        move_labels = VGroup(first_move)
        move_captions = VGroup()
        def prepare_move(index, start, end, tex, color, height, current):
            y_level = number_line.get_y() + height
            arrow = Arrow(
                np.array([number_line.n2p(start)[0], y_level, 0]),
                np.array([number_line.n2p(end)[0], y_level, 0]),
                buff=0.03,
                color=color,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.12,
            )
            guide_start = DashedLine(
                number_line.n2p(start),
                np.array([number_line.n2p(start)[0], y_level, 0]),
                color=HAIRLINE,
                stroke_width=1.5,
                dash_length=0.08,
            )
            guide_end = DashedLine(
                number_line.n2p(end),
                np.array([number_line.n2p(end)[0], y_level, 0]),
                color=HAIRLINE,
                stroke_width=1.5,
                dash_length=0.08,
            )
            move_label = label(tex, 29, color, "BOLD")
            move_label.next_to(arrow, UP, buff=0.08)
            caption = label(
                f"第 {index} 次：{current} → {end}",
                30,
                INK,
                "BOLD",
                t2c={"→": color},
            ).move_to(UP * 2.8)
            move_captions.add(caption)
            return arrow, guide_start, guide_end, move_label, caption

        arrow, guide_start, guide_end, move_label, caption = prepare_move(
            2, *move_specs[0], 1
        )
        self.play(FadeIn(caption), Create(guide_start), run_time=0.35)
        self.play(
            GrowArrow(arrow),
            ant.animate.move_to(number_line.n2p(-3)),
            ant_label.animate.next_to(number_line.n2p(-3), DOWN, buff=0.5),
            run_time=1.35,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(Create(guide_end), FadeIn(move_label), run_time=0.4)
        move_arrows.add(arrow, guide_start, guide_end)
        move_labels.add(move_label)

        # Beat 03 continue_first_block: settled semantic step.
        self.next_slide()
        arrow, guide_start, guide_end, move_label, caption = prepare_move(
            3, *move_specs[1], -3
        )
        self.play(FadeOut(move_captions[-2]), run_time=0.25)
        self.play(FadeIn(caption), Create(guide_start), run_time=0.35)
        self.play(
            GrowArrow(arrow),
            ant.animate.move_to(number_line.n2p(-12)),
            ant_label.animate.next_to(number_line.n2p(-12), DOWN, buff=0.5),
            run_time=1.35,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(Create(guide_end), FadeIn(move_label), run_time=0.4)
        move_arrows.add(arrow, guide_start, guide_end)
        move_labels.add(move_label)

        # Beat 04 finish_first_block: settled semantic step.
        self.next_slide()
        arrow, guide_start, guide_end, move_label, caption = prepare_move(
            4, *move_specs[2], -12
        )
        self.play(FadeOut(move_captions[-2]), run_time=0.25)
        self.play(FadeIn(caption), Create(guide_start), run_time=0.35)
        self.play(
            GrowArrow(arrow),
            ant.animate.move_to(number_line.n2p(4)),
            ant_label.animate.next_to(number_line.n2p(4), DOWN, buff=0.5),
            run_time=1.7,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(Create(guide_end), FadeIn(move_label), run_time=0.4)
        move_arrows.add(arrow, guide_start, guide_end)
        move_labels.add(move_label)

        net_move = label(
            "走了很遠，但一整組只從 0 到 4",
            31,
            INK,
            "BOLD",
            t2c={"0 到 4": REGION},
        ).move_to(UP * 2.8)
        first_identity = label(
            "1² − 2² − 3² + 4² = 4",
            36,
            INK,
            "BOLD",
            t2c={"1²": REGION, "2²": CORAL, "3²": CORAL, "4²": REGION},
        ).move_to(UP * 2.15)

        # Beat 05 sum_first_block: settled semantic step.
        self.next_slide()
        self.play(
            FadeOut(move_captions[-1]),
            FadeIn(net_move),
            FadeIn(first_identity),
            run_time=0.8,
        )

        # Beat 06 write_signed_squares: settled semantic step.
        self.next_slide()

        group_one = self.term_group((1, 2, 3, 4)).scale(0.82)
        group_two = self.term_group((5, 6, 7, 8)).scale(0.82)
        group_last = self.term_group((97, 98, 99, 100)).scale(0.74)
        group_one.move_to(UP * 1.05)
        group_two.move_to(DOWN * 0.15)
        group_last.move_to(DOWN * 1.55)
        ellipsis_one = label("+   ⋯   +", 34, MUTED, "BOLD")
        ellipsis_one.move_to(DOWN * 0.82)
        symbolic_note = label(
            "從現在起：每個方塊代表一項，不代表實際長度",
            28,
            MUTED,
            "MEDIUM",
        ).move_to(UP * 2.65)
        rhythm = label(
            "向右、向左、向左、向右｜每 4 步重複",
            31,
            INK,
            "BOLD",
            t2c={"向右": REGION, "向左": CORAL},
        ).next_to(symbolic_note, DOWN, buff=0.18)

        line_context = VGroup(
            number_line,
            number_labels,
            ant,
            ant_label,
            move_arrows,
            move_labels,
            net_move,
            first_identity,
        )
        self.play(
            FadeOut(line_context),
            FadeIn(symbolic_note),
            FadeIn(rhythm),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *(FadeIn(group_one[0][index]) for index in range(4)),
                lag_ratio=0.14,
            ),
            FadeIn(group_one[1]),
            run_time=1.3,
        )
        self.play(FadeIn(group_two, shift=DOWN * 0.12), run_time=0.8)
        self.play(FadeIn(ellipsis_one), FadeIn(group_last, shift=DOWN * 0.12), run_time=0.9)

        # Beat 07 pair_square_gaps: settled semantic step.
        self.next_slide()

        pair_title = label("第一組：把相鄰的平方配在一起", 32, INK, "BOLD")
        pair_title.move_to(UP * 3.08)
        pair_equation = VGroup(
            label("1² − 2² − 3² + 4²", 36, INK, "BOLD"),
            label("=", 35, INK, "BOLD"),
            label("(4² − 3²)", 36, REGION, "BOLD"),
            label("−", 37, INK, "BOLD"),
            label("(2² − 1²)", 36, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.18).move_to(UP * 2.3)

        gap_large = self.square_gap(4, 3, REGION, scale=0.62)
        gap_large.move_to(np.array([-4.55, -0.45, 0]))
        gap_small = self.square_gap(2, 1, CORAL, scale=0.72)
        gap_small.move_to(np.array([-1.35, -0.75, 0]))
        gap_minus = label("−", 48, INK, "BOLD").move_to([-2.75, -0.65, 0])
        large_value = label("4² − 3² = 7", 31, REGION, "BOLD")
        large_value.next_to(gap_large, DOWN, buff=0.24)
        small_value = label("2² − 1² = 3", 31, CORAL, "BOLD")
        small_value.next_to(gap_small, DOWN, buff=0.24)
        gap_result = label("7 − 3 = 4", 49, INK, "BOLD")
        gap_result.move_to([3.45, -0.25, 0])
        result_box = SurroundingRectangle(gap_result, color=POINT, buff=0.24, stroke_width=3)
        band_note = label("相鄰平方的差，就是新增的 L 形邊帶", 27, MUTED, "MEDIUM")
        band_note.move_to([3.45, 0.7, 0])

        self.play(
            FadeOut(symbolic_note),
            FadeOut(rhythm),
            FadeOut(group_two),
            FadeOut(ellipsis_one),
            FadeOut(group_last),
            Succession(FadeOut(group_one), FadeIn(pair_equation[0])),
            FadeIn(pair_title),
            FadeIn(VGroup(*pair_equation[1:])),
            run_time=1.2,
        )
        self.play(
            LaggedStart(
                Create(gap_large[1]),
                Create(gap_large[2]),
                Create(gap_small[1]),
                Create(gap_small[2]),
                lag_ratio=0.13,
            ),
            FadeIn(gap_large[3:]),
            FadeIn(gap_small[3:]),
            FadeIn(gap_minus),
            FadeIn(band_note),
            run_time=1.25,
        )
        self.play(FadeIn(gap_large[0]), FadeIn(gap_small[0]), run_time=0.75)
        # Beat 08 compare_paired_gaps: settled semantic step.
        self.next_slide()
        self.play(FadeIn(large_value), FadeIn(small_value), run_time=0.8)
        self.play(FadeIn(gap_result), Create(result_box), run_time=0.65)

        # Beat 09 prove_generic_block: settled semantic step.
        self.next_slide()

        generic_title = label("不是第一組碰巧：任一組都一樣", 32, INK, "BOLD")
        generic_title.move_to(UP * 3.15)
        generic = label(
            "n² − (n+1)² − (n+2)² + (n+3)²",
            36,
            INK,
            "BOLD",
        ).move_to(UP * 2.25)
        paired = label(
            "= [(n+3)² − (n+2)²] − [(n+1)² − n²]",
            34,
            INK,
            "BOLD",
        ).next_to(generic, DOWN, buff=0.38)
        gaps = label(
            "= (2n+5) − (2n+1)",
            40,
            INK,
            "BOLD",
            t2c={"2n": BLUE},
        ).next_to(paired, DOWN, buff=0.42)
        cancellation = label(
            "= (2n − 2n) + (5 − 1)",
            40,
            INK,
            "BOLD",
            t2c={"2n": BLUE},
        ).move_to(gaps)
        always_four = label("= 4", 53, REGION, "BOLD")
        always_four.next_to(cancellation, DOWN, buff=0.42)
        four_box = SurroundingRectangle(always_four, color=POINT, buff=0.18, stroke_width=3)
        n_note = label("n 是每一組的第一個數", 24, MUTED, "MEDIUM")
        n_note.next_to(generic, RIGHT, buff=0.35)

        old_pair = VGroup(
            pair_title,
            pair_equation,
            gap_large,
            gap_small,
            gap_minus,
            large_value,
            small_value,
            gap_result,
            result_box,
            band_note,
        )
        self.play(FadeOut(old_pair), FadeIn(generic_title), FadeIn(generic), FadeIn(n_note), run_time=1.0)
        self.play(FadeIn(paired), run_time=1.1)
        self.play(FadeIn(gaps), run_time=0.85)
        # Beat 10 state_generic_block_total: settled semantic step.
        self.next_slide()
        self.play(
            Circumscribe(gaps, color=BLUE, fade_out=True),
            Succession(FadeOut(gaps), FadeIn(cancellation)),
            run_time=1.2,
        )
        self.play(FadeIn(always_four), Create(four_box), run_time=0.7)

        # Beat 11 align_last_move: settled semantic step.
        self.next_slide()

        overview_title = label("最後一次，剛好落在完整一組的末端", 32, INK, "BOLD")
        overview_title.move_to(UP * 3.12)
        overview_one = self.term_group((1, 2, 3, 4)).scale(0.72)
        overview_two = self.term_group((5, 6, 7, 8)).scale(0.72)
        overview_last = self.term_group((97, 98, 99, 100)).scale(0.64)
        overview_one.move_to([-4.85, 0.45, 0])
        overview_two.move_to([0, 0.45, 0])
        overview_last.move_to([4.75, 0.45, 0])
        overview_dots_left = label("⋯", 39, MUTED, "BOLD").move_to([-2.4, 0.45, 0])
        overview_dots_right = label("⋯", 39, MUTED, "BOLD").move_to([2.42, 0.45, 0])
        n_values = label("n = 1, 5, 9, …, 97", 38, INK, "BOLD")
        n_values.move_to(DOWN * 1.2)
        closing_note = label("第 100 次是第四格｜沒有剩餘項", 31, POINT, "BOLD")
        closing_note.move_to(DOWN * 2.15)
        last_highlight = SurroundingRectangle(
            overview_last[0][3], color=POINT, buff=0.08, stroke_width=4
        )
        block_value_text = VGroup(
            label("每組", 26, INK, "BOLD"),
            label("+4", 32, INK, "BOLD"),
        ).arrange(RIGHT, buff=0.14)
        block_value_badge = VGroup(
            Rectangle(
                width=2.0,
                height=0.78,
                color=REGION,
                fill_color=REGION_DARK,
                fill_opacity=0.75,
            ),
            block_value_text,
        ).move_to(UP * 2.15)

        proof_context = VGroup(
            generic_title,
            generic,
            paired,
            cancellation,
            always_four,
            four_box,
            n_note,
        )
        self.play(
            FadeOut(proof_context),
            FadeIn(overview_title),
            FadeIn(block_value_badge),
            run_time=0.75,
        )
        self.play(
            LaggedStart(
                FadeIn(overview_one),
                FadeIn(overview_dots_left),
                FadeIn(overview_two),
                FadeIn(overview_dots_right),
                FadeIn(overview_last),
                lag_ratio=0.13,
            ),
            run_time=1.3,
        )
        self.play(FadeIn(n_values), run_time=0.7)
        self.play(Create(last_highlight), FadeIn(closing_note), run_time=0.8)

        # Beat 12 count_blocks: settled semantic step.
        self.next_slide()

        count_title = label("100 步，每 4 步壓成一塊", 32, INK, "BOLD")
        count_title.move_to(UP * 3.12)
        bricks = VGroup(*(self.block() for _ in range(25)))
        bricks.arrange_in_grid(rows=5, cols=5, buff=(0.14, 0.13))
        bricks.move_to([-3.45, -0.15, 0])
        group_count = VGroup(
            label("100 ÷ 4 = 25", 44, INK, "BOLD"),
            label("組", 34, INK, "BOLD"),
        ).arrange(RIGHT, buff=0.18)
        group_count.move_to([3.55, 0.65, 0])
        total_move = label("25 × 4 = 100", 49, INK, "BOLD")
        total_move.move_to([3.55, -0.55, 0])
        total_box = SurroundingRectangle(total_move, color=POINT, buff=0.22, stroke_width=3)

        overview_misc = VGroup(
            overview_title,
            overview_dots_left,
            overview_dots_right,
            overview_last,
            n_values,
            closing_note,
            last_highlight,
            block_value_badge,
        )
        self.play(FadeOut(overview_misc), FadeIn(count_title), run_time=0.6)
        self.play(
            Succession(FadeOut(overview_one), FadeIn(bricks[0])),
            Succession(FadeOut(overview_two), FadeIn(bricks[1])),
            run_time=0.9,
        )
        self.play(
            LaggedStart(*(FadeIn(brick, shift=UP * 0.08) for brick in bricks[2:]), lag_ratio=0.035),
            FadeIn(group_count),
            run_time=1.8,
        )
        # Beat 13 sum_complete_blocks: settled semantic step.
        self.next_slide()
        self.play(FadeIn(total_move), Create(total_box), run_time=0.75)

        # Beat 14 arrive_at_hundred: settled semantic step.
        self.next_slide()

        final_title = label("把 25 塊 +4 接回數線", 32, INK, "BOLD")
        final_title.move_to(UP * 3.12)
        final_line = NumberLine(
            x_range=[0, 100, 20],
            length=12.5,
            include_numbers=False,
            include_tip=True,
            color=MUTED,
            stroke_width=3,
        ).move_to(DOWN * 1.7)
        final_number_labels = VGroup()
        for value in range(0, 101, 20):
            number = label(str(value), 24, INK, "MEDIUM")
            number.next_to(final_line.n2p(value), DOWN, buff=0.18)
            final_number_labels.add(number)
        strip_segments = VGroup()
        segment_width = (final_line.n2p(100)[0] - final_line.n2p(0)[0]) / 25
        for index in range(25):
            segment = Rectangle(
                width=segment_width,
                height=0.44,
                color=REGION,
                stroke_width=1.4,
                fill_color=REGION_DARK,
                fill_opacity=0.9,
            )
            left_x = final_line.n2p(0)[0] + index * segment_width
            segment.move_to([left_x + segment_width / 2, final_line.get_y() + 0.42, 0])
            strip_segments.add(segment)
        final_ant = Dot(final_line.n2p(0), radius=0.11, color=POINT).set_z_index(5)
        first_block_note = label("第一組：0 → 4", 25, REGION, "BOLD")
        first_block_note.next_to(strip_segments[0], UP, buff=0.3).align_to(strip_segments[0], LEFT)
        final_answer = label("最後座標", 27, MUTED, "MEDIUM")
        final_answer.move_to(UP * 1.55)
        answer_value = label("100", 68, POINT, "BOLD")
        answer_value.next_to(final_answer, DOWN, buff=0.2)
        answer_box = SurroundingRectangle(answer_value, color=POINT, buff=0.22, stroke_width=3)
        answer_reason = label("25 組 × 每組向右 4", 28, INK, "BOLD")
        answer_reason.next_to(answer_value, DOWN, buff=0.3)

        count_context = VGroup(count_title, group_count, total_move, total_box)
        self.play(
            FadeOut(count_context),
            FadeIn(final_title),
            Create(final_line),
            FadeIn(final_number_labels),
            FadeIn(final_ant),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *(
                    Succession(FadeOut(brick), FadeIn(segment))
                    for brick, segment in zip(bricks, strip_segments, strict=True)
                ),
                lag_ratio=0.035,
            ),
            run_time=2.2,
        )
        self.play(FadeIn(first_block_note), Circumscribe(strip_segments[0], color=REGION), run_time=0.8)
        # Beat 15 reveal_hundredth_term: settled semantic step.
        self.next_slide()
        self.play(
            final_ant.animate.move_to(final_line.n2p(100)),
            FadeOut(first_block_note),
            run_time=2.0,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            FadeIn(final_answer),
            FadeIn(answer_value),
            Create(answer_box),
            FadeIn(answer_reason),
            run_time=0.9,
        )
