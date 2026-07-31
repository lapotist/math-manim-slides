"""Concise Manim Slides lesson for TCFS 115 mathematics gifted Q6."""

from __future__ import annotations

import math

import numpy as np

from manim import (
    Arrow,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP
from math_manim import BLUE, HAIRLINE, INK, MUTED, POINT, PURPLE, REGION, MathSlide, label


FACTOR_GROUPS = (
    (2, ((80, 3), (60, 4), (48, 5), (40, 6), (30, 8), (24, 10), (20, 12), (16, 15))),
    (3, ((40, 4), (32, 5), (20, 8), (16, 10))),
    (4, ((24, 5), (20, 6), (15, 8), (12, 10))),
    (5, ((16, 6), (12, 8))),
    (6, ((10, 8),)),
)


class Tcfs115Q06Slide(MathSlide):
    """Factor 480, check every ordered factor triple, and restore the sides."""

    lesson_id = "carlo.tcfs_115_math_gifted.q06"

    @staticmethod
    def factor_group_row(z: int, pairs: tuple[tuple[int, int], ...]) -> VGroup:
        body = Rectangle(
            width=11.4,
            height=0.58,
            color=HAIRLINE,
            stroke_width=1.5,
            fill_color=HAIRLINE,
            fill_opacity=0.05,
        )
        z_label = MathTex(rf"z={z}", font_size=28, color=POINT).move_to([-5.15, 0, 0])
        pair_tokens = VGroup(
            *(MathTex(rf"({x},{y})", font_size=25, color=INK) for x, y in pairs)
        ).arrange(RIGHT, buff=0.28)
        if pair_tokens.width > 9.65:
            pair_tokens.scale_to_fit_width(9.65)
        pair_tokens.move_to([0.45, 0, 0])
        return VGroup(body, z_label, pair_tokens)

    @staticmethod
    def exact_triangle(a: int, b: int, c: int, *, width: float = 3.15) -> VGroup:
        scale = width / a
        apex_x = (b * b + a * a - c * c) / (2 * a)
        apex_y = math.sqrt(b * b - apex_x * apex_x)
        left_point = np.array([-width / 2, -0.5, 0])
        right_point = np.array([width / 2, -0.5, 0])
        apex = left_point + np.array([apex_x * scale, apex_y * scale, 0])
        base = Line(left_point, right_point, color=BLUE, stroke_width=4)
        left_side = Line(left_point, apex, color=REGION, stroke_width=4)
        right_side = Line(apex, right_point, color=POINT, stroke_width=4)
        labels = VGroup(
            MathTex(str(a), font_size=25, color=BLUE).next_to(base, DOWN, buff=0.09),
            MathTex(str(b), font_size=25, color=REGION).next_to(
                left_side.get_center(), LEFT, buff=0.11
            ),
            MathTex(str(c), font_size=25, color=POINT).next_to(
                right_side.get_center(), RIGHT, buff=0.11
            ),
        )
        return VGroup(base, left_side, right_side, labels)

    @staticmethod
    def status_line(caption: str, tex: str, color: str) -> VGroup:
        dot = Dot(radius=0.06, color=color)
        caption_label = label(caption, 19, MUTED, "MEDIUM")
        equation = MathTex(tex, font_size=26, color=color)
        return VGroup(dot, caption_label, equation).arrange(RIGHT, buff=0.12)

    def construct(self) -> None:
        heading = label("第 6 題｜直接分解 480", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        original = MathTex(
            r"abc+ab+bc+ca+a+b+c=479",
            font_size=43,
            color=INK,
        ).move_to([0, 0.55, 0])
        add_one = label(
            "兩邊加 1",
            29,
            PURPLE,
            "BOLD",
        ).move_to([0, -0.6, 0])
        completed_product = MathTex(
            r"(a+1)(b+1)(c+1)=480",
            font_size=52,
            color=INK,
        ).move_to([0, 0.55, 0])

        # Beat 01 complete_product: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), Write(original), run_time=1.1)
        self.play(FadeIn(add_one, shift=UP * 0.1), run_time=0.45)
        self.play(FadeOut(original), run_time=0.35)
        self.play(FadeIn(completed_product), run_time=0.55)

        # Beat 02 factor_triangle_condition: settled semantic step.
        self.next_slide()
        prime_factorization = MathTex(
            r"480=2^5\cdot3\cdot5",
            font_size=66,
            color=POINT,
        )
        self.play(FadeOut(add_one), FadeOut(completed_product), run_time=0.4)
        self.play(Write(prime_factorization), run_time=0.75)

        # Beat 03 ordered_factor_triples: settled semantic step.
        self.next_slide()
        table_title = label(
            "按最小因數 z，列出全部有序因數組",
            32,
            INK,
            "BOLD",
            t2c={"全部": POINT},
        ).move_to([0, 3.0, 0])
        search_setup = MathTex(
            r"x=a+1,\ y=b+1,\ z=c+1;\qquad x>y>z\ge2,\quad xyz=480",
            font_size=30,
            color=INK,
        ).move_to([0, 2.3, 0])
        bound = MathTex(
            r"z^3<480,\ z\mid480\quad\Rightarrow\quad z\in\{2,3,4,5,6\}",
            font_size=29,
            color=MUTED,
        ).move_to([0, 1.72, 0])
        factor_rows = VGroup(
            *(self.factor_group_row(z, pairs) for z, pairs in FACTOR_GROUPS)
        )
        for row, y_position in zip(
            factor_rows,
            (1.0, 0.33, -0.34, -1.01, -1.68),
            strict=True,
        ):
            row.move_to([0, y_position, 0])
        table_note = label(
            "每個括號都是 (x,y)；共 19 組，沒有省略",
            21,
            MUTED,
            "MEDIUM",
            t2c={"19 組": POINT},
        ).move_to([0, -2.4, 0])
        self.play(
            FadeOut(prime_factorization),
            FadeIn(table_title),
            FadeIn(search_setup),
            FadeIn(bound),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*(FadeIn(row, shift=RIGHT * 0.08) for row in factor_rows), lag_ratio=0.14),
            run_time=1.1,
        )
        self.play(FadeIn(table_note), run_time=0.4)

        # Beat 04 filter_triangles: settled semantic step.
        self.next_slide()
        filter_title = label(
            "逐組檢查三角形條件",
            32,
            INK,
            "BOLD",
            t2c={"三角形條件": REGION},
        ).move_to([0, 3.0, 0])
        triangle_rule = MathTex(
            r"b+c>a\quad\Longleftrightarrow\quad y+z>x+1",
            font_size=38,
            color=REGION,
        ).move_to([0, 2.2, 0])
        invalid_tokens = VGroup()
        valid_tokens = VGroup()
        for row, (z, pairs) in zip(factor_rows, FACTOR_GROUPS, strict=True):
            for token, (x, y) in zip(row[2], pairs, strict=True):
                if y + z > x + 1:
                    valid_tokens.add(token)
                else:
                    invalid_tokens.add(token)
        survivor_boxes = VGroup(
            *(
                SurroundingRectangle(token, color=REGION, buff=0.08, stroke_width=2.4)
                for token in valid_tokens
            )
        )
        survivor_checks = VGroup(
            MathTex(r"10+4>12+1", font_size=31, color=REGION),
            MathTex(r"8+6>10+1", font_size=31, color=REGION),
        ).arrange(RIGHT, buff=1.25).move_to([0, -2.48, 0])
        self.play(
            FadeOut(table_title),
            FadeOut(search_setup),
            FadeOut(bound),
            FadeOut(table_note),
            FadeIn(filter_title),
            Write(triangle_rule),
            run_time=0.65,
        )
        self.play(
            *(
                token.animate.set_opacity(0.16)
                for token in invalid_tokens
            ),
            *(token.animate.set_color(REGION) for token in valid_tokens),
            run_time=0.9,
        )
        self.play(FadeIn(survivor_boxes), FadeIn(survivor_checks), run_time=0.65)
        self.wait(0.2)

        # Beat 05 restore_sides: settled semantic step.
        self.next_slide()
        restore_title = label(
            "最後把每個數減 1",
            33,
            INK,
            "BOLD",
            t2c={"減 1": PURPLE},
        ).move_to([0, 2.8, 0])
        shifted = VGroup(
            MathTex(r"(x,y,z)=(12,10,4)", font_size=38, color=REGION),
            MathTex(r"(x,y,z)=(10,8,6)", font_size=38, color=REGION),
        ).arrange(RIGHT, buff=0.75).move_to([0, 1.25, 0])
        down_arrows = VGroup(
            *(
                Arrow(
                    item.get_bottom(),
                    item.get_bottom() + DOWN * 1.15,
                    buff=0.12,
                    color=PURPLE,
                    stroke_width=3.5,
                )
                for item in shifted
            )
        )
        minus_labels = VGroup(
            *(label("每個數 -1", 20, PURPLE, "BOLD").next_to(arrow, RIGHT, buff=0.12) for arrow in down_arrows)
        )
        answers = VGroup(
            MathTex(r"(a,b,c)=(11,9,3)", font_size=43, color=INK),
            MathTex(r"(a,b,c)=(9,7,5)", font_size=43, color=INK),
        ).arrange(RIGHT, buff=0.95).move_to([0, -1.15, 0])
        filter_scene = VGroup(
            filter_title,
            triangle_rule,
            factor_rows,
            survivor_boxes,
            survivor_checks,
        )
        self.play(FadeOut(filter_scene), FadeIn(restore_title), FadeIn(shifted), run_time=0.7)
        self.play(Create(down_arrows), FadeIn(minus_labels), run_time=0.55)
        self.play(
            TransformFromCopy(shifted[0], answers[0]),
            TransformFromCopy(shifted[1], answers[1]),
            run_time=0.8,
        )

        # Beat 06 verify_triangles: settled semantic step.
        self.next_slide()
        verify_title = label(
            "兩組答案都代回原條件",
            33,
            INK,
            "BOLD",
            t2c={"代回": POINT},
        ).move_to([0, 3.0, 0])
        divider = Line([0, 2.35, 0], [0, -2.5, 0], color=HAIRLINE, stroke_width=2)
        first_name = answers[0].copy().scale(0.83).move_to([-3.65, 2.05, 0])
        second_name = answers[1].copy().scale(0.83).move_to([3.65, 2.05, 0])
        first_triangle = self.exact_triangle(11, 9, 3).scale(0.88).move_to([-3.65, 0.72, 0])
        second_triangle = self.exact_triangle(9, 7, 5).scale(0.88).move_to([3.65, 0.72, 0])
        first_checks = VGroup(
            self.status_line("次序", r"11>9>3\ge1", REGION),
            self.status_line("三角形", r"9+3>11", REGION),
            self.status_line("原式", r"12\cdot10\cdot4-1=479", POINT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([-3.65, -1.45, 0])
        second_checks = VGroup(
            self.status_line("次序", r"9>7>5\ge1", REGION),
            self.status_line("三角形", r"7+5>9", REGION),
            self.status_line("原式", r"10\cdot8\cdot6-1=479", POINT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([3.65, -1.45, 0])
        final_answer = label("答案只有這兩組", 27, POINT, "BOLD").move_to([0, -2.48, 0])
        restore_scene = VGroup(restore_title, shifted, down_arrows, minus_labels, answers)
        self.play(FadeOut(restore_scene), FadeIn(verify_title), Create(divider), run_time=0.65)
        self.play(
            FadeIn(first_name),
            FadeIn(second_name),
            Create(first_triangle),
            Create(second_triangle),
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *(FadeIn(row, shift=RIGHT * 0.06) for row in (*first_checks, *second_checks)),
                lag_ratio=0.1,
            ),
            run_time=1.0,
        )
        self.play(
            Circumscribe(first_name, color=REGION, time_width=0.5),
            Circumscribe(second_name, color=REGION, time_width=0.5),
            FadeIn(final_answer),
            run_time=0.75,
        )
        self.wait(0.25)
