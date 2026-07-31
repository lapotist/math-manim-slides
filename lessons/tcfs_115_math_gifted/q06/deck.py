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
    VGroup,
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

CONTENT_TITLE_Y = 2.7
FACTOR_COLUMN_X = (-3.55, -2.35, -1.15, 0.05, 1.25, 2.45, 3.65, 4.85)


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
            *(
                MathTex(rf"({x},{y})", font_size=25, color=INK).move_to(
                    [slot_x, 0, 0]
                )
                for (x, y), slot_x in zip(pairs, FACTOR_COLUMN_X, strict=False)
            )
        )
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
        def sloped_label(value: int, side: Line, color: str) -> MathTex:
            direction = side.get_end() - side.get_start()
            outward = np.array([-direction[1], direction[0], 0])
            outward /= np.linalg.norm(outward)
            return MathTex(str(value), font_size=25, color=color).move_to(
                side.get_center() + outward * 0.24
            )

        labels = VGroup(
            MathTex(str(a), font_size=25, color=BLUE).next_to(base, DOWN, buff=0.11),
            sloped_label(b, left_side, REGION),
            sloped_label(c, right_side, POINT),
        )
        return VGroup(base, left_side, right_side, labels)

    @staticmethod
    def status_line(caption: str, tex: str, color: str) -> VGroup:
        dot = Dot(radius=0.06, color=color)
        caption_label = label(caption, 19, MUTED, "MEDIUM")
        equation = MathTex(tex, font_size=26, color=color)
        dot.move_to([0, 0, 0])
        caption_label.move_to([0.24 + caption_label.width / 2, 0, 0])
        equation.move_to([1.18 + equation.width / 2, 0, 0])
        return VGroup(dot, caption_label, equation)

    def construct(self) -> None:
        heading = label("第 6 題｜直接分解 480", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        original = MathTex(
            r"abc+ab+bc+ca+a+b+c=479",
            font_size=48,
            color=INK,
        ).move_to([0, 0.1, 0])
        add_one = label(
            "兩邊加 1",
            29,
            PURPLE,
            "BOLD",
        ).move_to([0, -0.85, 0])
        completed_product = MathTex(
            r"(a+1)(b+1)(c+1)=480",
            font_size=56,
            color=INK,
        ).move_to([0, 0.1, 0])

        # Beat 01 complete_product: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(original), run_time=0.75)
        self.play(FadeIn(add_one, shift=UP * 0.1), run_time=0.45)
        self.play(FadeOut(original), run_time=0.35)
        self.play(FadeIn(completed_product), run_time=0.55)

        # Beat 02 factor_triangle_condition: settled semantic step.
        self.next_slide()
        prime_factorization = MathTex(
            r"480=2^5\cdot3\cdot5",
            font_size=80,
            color=POINT,
        ).move_to([0, 0.1, 0])
        self.play(FadeOut(add_one), FadeOut(completed_product), run_time=0.4)
        self.play(FadeIn(prime_factorization), run_time=0.55)

        # Beat 03 ordered_factor_triples: settled semantic step.
        self.next_slide()
        table_title = label(
            "按最小因數 z，列出全部有序因數組",
            32,
            INK,
            "BOLD",
            t2c={"全部": POINT},
        ).move_to([0, CONTENT_TITLE_Y, 0])
        search_setup = MathTex(
            r"x=a+1,\ y=b+1,\ z=c+1;\qquad x>y>z\ge2,\quad xyz=480",
            font_size=30,
            color=INK,
        ).move_to([0, 2.0, 0])
        bound = MathTex(
            r"z^3<480,\ z\mid480\quad\Rightarrow\quad z\in\{2,3,4,5,6\}",
            font_size=29,
            color=MUTED,
        ).move_to([0, 1.4, 0])
        factor_rows = VGroup(
            *(self.factor_group_row(z, pairs) for z, pairs in FACTOR_GROUPS)
        )
        for row, y_position in zip(
            factor_rows,
            (0.73, 0.06, -0.61, -1.28, -1.95),
            strict=True,
        ):
            row.move_to([0, y_position, 0])
        table_note = label(
            "每個括號都是 (x,y)；共 19 組，沒有省略",
            21,
            MUTED,
            "MEDIUM",
            t2c={"19 組": POINT},
        ).move_to([0, -2.55, 0])
        self.play(FadeOut(prime_factorization), run_time=0.35)
        self.play(FadeIn(table_title), FadeIn(search_setup), FadeIn(bound), run_time=0.55)
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
        ).move_to([0, CONTENT_TITLE_Y, 0])
        triangle_rule = MathTex(
            r"b+c>a\quad\Longleftrightarrow\quad y+z>x+1",
            font_size=38,
            color=REGION,
        ).move_to([0, 1.9, 0])
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
            MathTex(r"(12,10,4):\ 10+4>12+1", font_size=27, color=REGION),
            MathTex(r"(10,8,6):\ 8+6>10+1", font_size=27, color=REGION),
        )
        survivor_checks[0].move_to([-2.9, -2.58, 0])
        survivor_checks[1].move_to([2.9, -2.58, 0])
        self.play(
            FadeOut(table_title),
            FadeOut(search_setup),
            FadeOut(bound),
            FadeOut(table_note),
            run_time=0.35,
        )
        self.play(FadeIn(filter_title), FadeIn(triangle_rule), run_time=0.55)
        self.play(
            *(
                token.animate.set_opacity(0.25)
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
        ).move_to([0, CONTENT_TITLE_Y, 0])
        column_x = (-3.0, 3.0)
        shifted = VGroup(
            MathTex(r"(x,y,z)=(12,10,4)", font_size=38, color=REGION).move_to(
                [column_x[0], 1.2, 0]
            ),
            MathTex(r"(x,y,z)=(10,8,6)", font_size=38, color=REGION).move_to(
                [column_x[1], 1.2, 0]
            ),
        )
        down_arrows = VGroup(
            *(
                Arrow(
                    [x, 0.75, 0],
                    [x, -0.35, 0],
                    buff=0,
                    color=PURPLE,
                    stroke_width=3.5,
                )
                for x in column_x
            )
        )
        minus_labels = VGroup(
            *(label("每個數 -1", 20, PURPLE, "BOLD").next_to(arrow, RIGHT, buff=0.12) for arrow in down_arrows)
        )
        answers = VGroup(
            MathTex(r"(a,b,c)=(11,9,3)", font_size=43, color=INK).move_to(
                [column_x[0], -1.25, 0]
            ),
            MathTex(r"(a,b,c)=(9,7,5)", font_size=43, color=INK).move_to(
                [column_x[1], -1.25, 0]
            ),
        )
        filter_scene = VGroup(
            filter_title,
            triangle_rule,
            factor_rows,
            survivor_boxes,
            survivor_checks,
        )
        self.play(FadeOut(filter_scene), run_time=0.35)
        self.play(FadeIn(restore_title), FadeIn(shifted), run_time=0.55)
        self.play(Create(down_arrows), FadeIn(minus_labels), run_time=0.55)
        self.play(FadeIn(answers, shift=DOWN * 0.08), run_time=0.55)

        # Beat 06 verify_triangles: settled semantic step.
        self.next_slide()
        verify_title = label(
            "兩組答案都代回原條件",
            33,
            INK,
            "BOLD",
            t2c={"代回": POINT},
        ).move_to([0, CONTENT_TITLE_Y, 0])
        divider = Line([0, 2.1, 0], [0, -2.05, 0], color=HAIRLINE, stroke_width=2)
        verify_column_x = (-3.55, 3.55)
        first_name = answers[0].copy().scale(0.83).move_to([verify_column_x[0], 1.95, 0])
        second_name = answers[1].copy().scale(0.83).move_to([verify_column_x[1], 1.95, 0])
        first_triangle = self.exact_triangle(11, 9, 3, width=2.8)
        second_triangle = self.exact_triangle(9, 7, 5, width=2.8)
        for triangle, x in zip(
            (first_triangle, second_triangle), verify_column_x, strict=True
        ):
            triangle.shift(
                np.array([x - triangle[0].get_x(), 0.35 - triangle[0].get_y(), 0])
            )
        first_checks = VGroup(
            self.status_line("次序", r"11>9>3\ge1", REGION),
            self.status_line("三角形", r"9+3>11", REGION),
            self.status_line("原式", r"12\cdot10\cdot4-1=479", POINT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([verify_column_x[0], -1.35, 0])
        second_checks = VGroup(
            self.status_line("次序", r"9>7>5\ge1", REGION),
            self.status_line("三角形", r"7+5>9", REGION),
            self.status_line("原式", r"10\cdot8\cdot6-1=479", POINT),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([verify_column_x[1], -1.35, 0])
        final_answer = label("答案只有這兩組", 27, POINT, "BOLD").move_to([0, -2.55, 0])
        restore_scene = VGroup(restore_title, shifted, down_arrows, minus_labels, answers)
        self.play(FadeOut(restore_scene), run_time=0.35)
        self.play(
            FadeIn(verify_title),
            Create(divider),
            FadeIn(first_name),
            FadeIn(second_name),
            *(Create(side) for side in (*first_triangle[:3], *second_triangle[:3])),
            run_time=0.8,
        )
        self.play(
            FadeIn(first_triangle[3]),
            FadeIn(second_triangle[3]),
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
