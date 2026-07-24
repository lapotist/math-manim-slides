"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q2."""

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
    WHITE,
    CarloSlide,
    label,
)
from manim import (
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class CarloTcfs115MathQ02(CarloSlide):
    """Carry equal area across three rectangles with shared half-triangles."""

    lesson_id = "carlo.tcfs_115_math_gifted.q02"

    @staticmethod
    def perpendicular_component(vector: np.ndarray, base: np.ndarray) -> np.ndarray:
        """Return the component of ``vector`` perpendicular to ``base``."""
        return vector - np.dot(vector, base) / np.dot(base, base) * base

    @staticmethod
    def rectangle_edges(vertices: tuple[np.ndarray, ...], color: str) -> VGroup:
        return VGroup(
            *(
                Line(start, end, color=color, stroke_width=4)
                for start, end in zip(vertices, vertices[1:] + vertices[:1])
            )
        )

    def construct(self) -> None:
        # The first rectangle uses one common visual scale for 5 and 12. Each
        # later normal vector is an exact perpendicular projection, so the old
        # point lies on the new far edge rather than merely looking aligned.
        point_o = np.array([-3.60, -2.40, 0.0])
        vector_oa1 = np.array([1.80, 0.0, 0.0])
        vector_ob1 = np.array([0.0, 4.32, 0.0])
        point_a1 = point_o + vector_oa1
        point_b1 = point_o + vector_ob1
        point_a2 = point_o + vector_oa1 + vector_ob1

        vector_oa2 = point_a2 - point_o
        vector_ob2 = self.perpendicular_component(vector_ob1, vector_oa2)
        point_b2 = point_o + vector_ob2
        point_a3 = point_a2 + vector_ob2

        vector_oa3 = point_a3 - point_o
        vector_ob3 = self.perpendicular_component(vector_ob2, vector_oa3)
        point_b3 = point_o + vector_ob3
        point_a4 = point_a3 + vector_ob3

        vertices_r1 = (point_o, point_a1, point_a2, point_b1)
        vertices_r2 = (point_o, point_a2, point_a3, point_b2)
        vertices_r3 = (point_o, point_a3, point_a4, point_b3)

        heading = label("第 2 題｜一塊三角形，連起三個長方形", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        r1_fill = Polygon(
            *vertices_r1,
            color=BLUE,
            stroke_width=0,
            fill_color=BLUE,
            fill_opacity=0.08,
        ).set_z_index(-4)
        r2_fill = Polygon(
            *vertices_r2,
            color=CORAL,
            stroke_width=0,
            fill_color=CORAL,
            fill_opacity=0.08,
        ).set_z_index(-5)
        r3_fill = Polygon(
            *vertices_r3,
            color=REGION,
            stroke_width=0,
            fill_color=REGION,
            fill_opacity=0.08,
        ).set_z_index(-6)
        r1_edges = self.rectangle_edges(vertices_r1, BLUE)
        r2_edges = self.rectangle_edges(vertices_r2, CORAL)
        r3_edges = self.rectangle_edges(vertices_r3, REGION)

        dot_o = Dot(point_o, radius=0.075, color=WHITE).set_z_index(6)
        dot_a1 = Dot(point_a1, radius=0.065, color=WHITE).set_z_index(6)
        dot_b1 = Dot(point_b1, radius=0.072, color=POINT).set_z_index(7)
        dot_a2 = Dot(point_a2, radius=0.072, color=WHITE).set_z_index(6)
        dot_b2 = Dot(point_b2, radius=0.072, color=POINT).set_z_index(7)
        dot_a3 = Dot(point_a3, radius=0.072, color=WHITE).set_z_index(6)

        label_o = label("O", 24, INK, "BOLD").next_to(dot_o, DOWN + LEFT, buff=0.10)
        label_a1 = label("A₁", 23, INK, "BOLD").next_to(dot_a1, DOWN, buff=0.13)
        label_b1 = label("B₁", 23, POINT, "BOLD").next_to(dot_b1, LEFT, buff=0.12)
        label_a2 = label("A₂", 23, INK, "BOLD").next_to(dot_a2, RIGHT, buff=0.12)
        label_b2 = label("B₂", 23, POINT, "BOLD").next_to(dot_b2, LEFT, buff=0.12)
        label_a3 = label("A₃", 23, INK, "BOLD").next_to(dot_a3, UP, buff=0.12)

        length_five = label("5", 25, BLUE, "BOLD")
        length_five.next_to(Line(point_o, point_a1), DOWN, buff=0.12)
        length_twelve = label("12", 25, BLUE, "BOLD")
        length_twelve.next_to(Line(point_o, point_b1), LEFT, buff=0.12)

        # Beat 01: establish the only rectangle whose side lengths are known.
        self.begin_beat("first_rectangle")
        first_title = label("先算唯一知道邊長的長方形", 31, INK, "BOLD")
        first_title.move_to([3.25, 2.30, 0])
        area_r1 = MathTex(
            r"R_1",
            "=",
            r"5\times12",
            "=",
            "60",
            font_size=48,
            color=INK,
        ).move_to([3.25, 0.95, 0])
        area_r1[0].set_color(BLUE)
        area_r1[4].set_color(POINT)

        self.add(heading, source)
        self.play(FadeIn(dot_o), FadeIn(label_o))
        self.play(
            Create(r1_edges[0]),
            Create(r1_edges[3]),
            FadeIn(dot_a1),
            FadeIn(dot_b1),
            FadeIn(label_a1),
            FadeIn(label_b1),
            FadeIn(length_five),
            FadeIn(length_twelve),
            run_time=1.05,
        )
        self.play(
            Create(r1_edges[1]),
            Create(r1_edges[2]),
            FadeIn(r1_fill),
            FadeIn(dot_a2),
            FadeIn(label_a2),
            run_time=0.95,
        )
        self.play(FadeIn(first_title), Write(area_r1), run_time=0.85)

        # Beat 02: preserve one yellow half rather than replacing it later.
        self.next_beat("shared_half")
        diagonal_one = Line(point_o, point_a2, color=POINT, stroke_width=4)
        other_half_one = Polygon(
            point_o,
            point_a1,
            point_a2,
            color=BLUE,
            stroke_width=1.5,
            fill_color=BLUE,
            fill_opacity=0.22,
        ).set_z_index(-1)
        shared_triangle = Polygon(
            point_o,
            point_a2,
            point_b1,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.35,
        ).set_z_index(1)
        half_title = label("對角線切成兩個相等的半部", 31, INK, "BOLD")
        half_title.move_to(first_title)
        half_r1 = MathTex(
            r"[\triangle OA_2B_1]",
            "=",
            r"\frac12R_1",
            "=",
            "30",
            font_size=43,
            color=INK,
        ).move_to([3.25, -0.35, 0])
        half_r1[0].set_color(POINT)
        half_r1[2].set_color(BLUE)

        self.play(
            ReplacementTransform(first_title, half_title),
            Create(diagonal_one),
            run_time=0.8,
        )
        self.play(FadeIn(other_half_one), FadeIn(shared_triangle), run_time=0.65)
        self.play(Indicate(other_half_one, color=BLUE), run_time=0.65)
        self.play(Indicate(shared_triangle, color=POINT), run_time=0.65)
        self.play(FadeOut(other_half_one), Write(half_r1), run_time=0.75)

        # Beat 03: grow R2 around the same unmoving yellow triangle.
        self.next_beat("grow_second")
        second_title = label("黃色三角形不動，外面換一個長方形", 30, INK, "BOLD")
        second_title.move_to(half_title)
        far_edge_r2 = Line(point_b2, point_a3, color=CORAL, stroke_width=7)
        b1_note = label("B₁ 正好在 R₂ 的對邊上", 29, CORAL, "BOLD")
        b1_note.move_to([3.25, -1.65, 0])

        self.play(ReplacementTransform(half_title, second_title), run_time=0.45)
        self.play(
            FadeIn(r2_fill),
            LaggedStart(*(Create(edge) for edge in r2_edges), lag_ratio=0.14),
            FadeIn(dot_b2),
            FadeIn(label_b2),
            FadeIn(dot_a3),
            FadeIn(label_a3),
            run_time=1.45,
        )
        self.play(Create(far_edge_r2), FadeIn(b1_note), run_time=0.7)
        self.play(Indicate(dot_b1, color=POINT), run_time=0.65)
        self.play(FadeOut(far_edge_r2), run_time=0.35)

        # Beat 04: make the shared base and full height explicit.
        self.next_beat("equal_first_second")
        projection_one = point_o + (
            np.dot(point_b1 - point_o, vector_oa2)
            / np.dot(vector_oa2, vector_oa2)
        ) * vector_oa2
        base_one = Line(point_o, point_a2, color=POINT, stroke_width=7)
        height_one = DashedLine(
            point_b1,
            projection_one,
            color=POINT,
            stroke_width=3,
            dash_length=0.11,
        )
        base_height_note = label("同一個底｜同一個完整高度", 30, POINT, "BOLD")
        base_height_note.move_to([3.25, 2.30, 0])
        bridge_one = MathTex(
            r"\frac12R_1",
            "=",
            r"[\triangle OA_2B_1]",
            "=",
            r"\frac12R_2",
            font_size=39,
            color=INK,
        ).move_to([3.25, -0.38, 0])
        bridge_one[0].set_color(BLUE)
        bridge_one[2].set_color(POINT)
        bridge_one[4].set_color(CORAL)
        equality_12 = MathTex(
            r"R_1=R_2=60",
            font_size=49,
            color=INK,
        ).move_to([3.25, -1.55, 0])
        equality_12.set_color_by_tex("R_1", BLUE)
        equality_12.set_color_by_tex("R_2", CORAL)

        self.play(
            FadeOut(second_title),
            FadeOut(b1_note),
            FadeOut(half_r1),
            FadeIn(base_height_note),
            Create(base_one),
            Create(height_one),
            run_time=0.9,
        )
        self.play(TransformFromCopy(shared_triangle, bridge_one[2]), run_time=0.7)
        self.play(Write(bridge_one[0:2]), Write(bridge_one[3:5]), run_time=0.8)
        self.play(Write(equality_12), run_time=0.7)

        # Beat 05: move the same argument one rectangle to the left.
        self.next_beat("shift_shared_half")
        diagonal_two = Line(point_o, point_a3, color=POINT, stroke_width=4)
        companion_two = Polygon(
            point_o,
            point_a2,
            point_a3,
            color=CORAL,
            stroke_width=1.5,
            fill_color=CORAL,
            fill_opacity=0.20,
        ).set_z_index(-1)
        next_shared_triangle = Polygon(
            point_o,
            point_a3,
            point_b2,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.35,
        ).set_z_index(1)
        shift_title = label("把同一座「一半」的橋往下一格搬", 30, INK, "BOLD")
        shift_title.move_to(base_height_note)
        half_r2 = MathTex(
            r"[\triangle OA_3B_2]=\frac12R_2",
            font_size=43,
            color=INK,
        ).move_to([3.25, -0.35, 0])
        half_r2.set_color_by_tex(r"\triangle OA_3B_2", POINT)
        half_r2.set_color_by_tex("R_2", CORAL)

        self.play(
            r1_edges.animate.set_opacity(0.22),
            r1_fill.animate.set_fill(opacity=0.02),
            FadeOut(base_one),
            FadeOut(height_one),
            FadeOut(bridge_one),
            FadeOut(equality_12),
            ReplacementTransform(base_height_note, shift_title),
            Create(diagonal_two),
            run_time=0.9,
        )
        self.play(
            FadeIn(companion_two),
            ReplacementTransform(shared_triangle, next_shared_triangle),
            run_time=0.9,
        )
        shared_triangle = next_shared_triangle
        self.play(Indicate(companion_two, color=CORAL), run_time=0.55)
        self.play(Indicate(shared_triangle, color=POINT), run_time=0.55)
        self.play(FadeOut(companion_two), Write(half_r2), run_time=0.7)

        # Beat 06: grow R3 so B2 lies on its opposite edge.
        self.next_beat("grow_third")
        projection_two = point_o + (
            np.dot(point_b2 - point_o, vector_oa3)
            / np.dot(vector_oa3, vector_oa3)
        ) * vector_oa3
        base_two = Line(point_o, point_a3, color=POINT, stroke_width=7)
        height_two = DashedLine(
            point_b2,
            projection_two,
            color=POINT,
            stroke_width=3,
            dash_length=0.11,
        )
        third_title = label("B₂ 在第三個長方形的對邊上", 30, REGION, "BOLD")
        third_title.move_to(shift_title)
        bridge_two = MathTex(
            r"\frac12R_2",
            "=",
            r"[\triangle OA_3B_2]",
            "=",
            r"\frac12R_3",
            font_size=39,
            color=INK,
        ).move_to([3.25, -0.35, 0])
        bridge_two[0].set_color(CORAL)
        bridge_two[2].set_color(POINT)
        bridge_two[4].set_color(REGION)
        equality_23 = MathTex(
            r"R_2=R_3",
            font_size=49,
            color=INK,
        ).move_to([3.25, -1.55, 0])
        equality_23.set_color_by_tex("R_2", CORAL)
        equality_23.set_color_by_tex("R_3", REGION)

        self.play(
            ReplacementTransform(shift_title, third_title),
            FadeOut(half_r2),
            FadeIn(r3_fill),
            LaggedStart(*(Create(edge) for edge in r3_edges), lag_ratio=0.14),
            run_time=1.4,
        )
        self.play(Create(base_two), Create(height_two), Indicate(dot_b2, color=POINT))
        self.play(TransformFromCopy(shared_triangle, bridge_two[2]), run_time=0.7)
        self.play(Write(bridge_two[0:2]), Write(bridge_two[3:5]), run_time=0.8)
        self.play(Write(equality_23), run_time=0.6)

        # Beat 07: return to all three rectangles and transfer the known 60.
        self.next_beat("three_equal_areas")
        all_equal = MathTex(
            r"R_1",
            "=",
            r"R_2",
            "=",
            r"R_3",
            "=",
            "60",
            font_size=48,
            color=INK,
        ).move_to([3.25, 0.25, 0])
        all_equal[0].set_color(BLUE)
        all_equal[2].set_color(CORAL)
        all_equal[4].set_color(REGION)
        all_equal[6].set_color(POINT)
        area_labels = VGroup(
            label("60", 29, BLUE, "BOLD").move_to([-2.70, -0.22, 0]),
            label("60", 29, CORAL, "BOLD").move_to([-3.47, 0.12, 0]),
            label("60", 29, REGION, "BOLD").move_to([-4.25, 0.20, 0]),
        ).set_z_index(8)
        equal_title = label("方向不同，面積仍然相同", 32, INK, "BOLD")
        equal_title.move_to(third_title)

        self.play(
            r1_edges.animate.set_opacity(1),
            r1_fill.animate.set_fill(opacity=0.08),
            FadeOut(diagonal_one),
            FadeOut(diagonal_two),
            FadeOut(base_two),
            FadeOut(height_two),
            FadeOut(shared_triangle),
            FadeOut(bridge_two),
            FadeOut(equality_23),
            FadeOut(length_five),
            FadeOut(length_twelve),
            ReplacementTransform(third_title, equal_title),
            run_time=0.95,
        )
        self.play(
            LaggedStart(*(FadeIn(item) for item in area_labels), lag_ratio=0.25),
            Write(all_equal),
            run_time=1.1,
        )

        # Beat 08: only after equality is visible, add the three areas.
        self.next_beat("sum_areas")
        sum_title = label("最後才做加法", 32, INK, "BOLD")
        sum_title.move_to(equal_title)
        total = MathTex(
            "60",
            "+",
            "60",
            "+",
            "60",
            "=",
            "180",
            font_size=49,
            color=INK,
        ).move_to([3.25, -0.55, 0])
        for index, color in zip((0, 2, 4), (BLUE, CORAL, REGION), strict=True):
            total[index].set_color(color)
        total[6].set_color(POINT)
        answer_box = SurroundingRectangle(total[6], color=POINT, buff=0.20, stroke_width=3)
        bridge_flash_one = Polygon(
            point_o,
            point_a2,
            point_b1,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.22,
        )
        bridge_flash_two = Polygon(
            point_o,
            point_a3,
            point_b2,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.22,
        )

        self.play(ReplacementTransform(equal_title, sum_title), FadeOut(all_equal))
        self.play(
            *(
                TransformFromCopy(area_labels[index], total[2 * index])
                for index in range(3)
            ),
            Write(VGroup(total[1], total[3], total[5], total[6])),
            run_time=1.1,
        )
        self.play(Create(answer_box), Circumscribe(total[6], color=POINT), run_time=0.8)
        self.play(FadeIn(bridge_flash_one), FadeIn(bridge_flash_two), run_time=0.45)
        self.play(
            Indicate(bridge_flash_one, color=POINT),
            Indicate(bridge_flash_two, color=POINT),
            run_time=0.75,
        )
