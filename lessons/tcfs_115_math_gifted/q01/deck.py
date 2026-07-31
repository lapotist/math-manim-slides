"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q1."""

from __future__ import annotations

import numpy as np

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    PURPLE,
    REGION,
    WHITE,
    CarloSlide,
    label,
)
from manim import (
    Arc,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    VMobject,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class CarloTcfs115MathQ01(CarloSlide):
    """Reveal the perpendicular bisectors before simplifying the invariant."""

    lesson_id = "carlo.tcfs_115_math_gifted.q01"

    @staticmethod
    def ray_to_base(origin: np.ndarray, angle: float, base_y: float) -> np.ndarray:
        """Intersect a downward ray with the horizontal baseline."""
        distance = (base_y - origin[1]) / np.sin(angle)
        return origin + distance * np.array([np.cos(angle), np.sin(angle), 0.0])

    @staticmethod
    def angle_label(
        tex: str,
        center: np.ndarray,
        radius: float,
        angle: float,
        color: str,
        *,
        size: int = 28,
    ) -> MathTex:
        result = MathTex(tex, font_size=size, color=color)
        result.move_to(
            center + radius * np.array([np.cos(angle), np.sin(angle), 0.0])
        )
        return result

    def construct(self) -> None:
        # The displayed triangle is exact: x=35 degrees, while every derivation
        # remains symbolic.  This keeps E--B--D--C and all marked angles honest.
        unit = 2.15
        base_y = -1.42
        point_d = np.array([-2.75, base_y, 0.0])
        point_a = point_d + unit * np.array([-0.5, np.sqrt(3) / 2, 0.0])
        point_e = point_d + np.array([-2 * unit, 0.0, 0.0])
        x_angle = np.deg2rad(35)
        ad_direction = -np.pi / 3
        ab_direction = ad_direction - x_angle
        ac_direction = ad_direction + x_angle
        ae_direction = -5 * np.pi / 6
        point_b = self.ray_to_base(point_a, ab_direction, base_y)
        point_c = self.ray_to_base(point_a, ac_direction, base_y)

        heading = label("第 1 題｜角平分線藏著什麼？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        dot_a = Dot(point_a, radius=0.075, color=WHITE).set_z_index(5)
        dot_b = Dot(point_b, radius=0.07, color=WHITE).set_z_index(5)
        dot_c = Dot(point_c, radius=0.07, color=WHITE).set_z_index(5)
        dot_d = Dot(point_d, radius=0.07, color=WHITE).set_z_index(5)
        dot_e = Dot(point_e, radius=0.07, color=WHITE).set_z_index(5)
        label_a = label("A", 26, INK, "BOLD").next_to(dot_a, UP, buff=0.12)
        label_b = label("B", 25, INK, "BOLD").next_to(dot_b, DOWN, buff=0.14)
        label_c = label("C", 25, INK, "BOLD").next_to(dot_c, DOWN, buff=0.14)
        label_d = label("D", 25, INK, "BOLD").next_to(dot_d, DOWN, buff=0.14)
        label_e = label("E", 25, INK, "BOLD").next_to(dot_e, DOWN, buff=0.14)

        side_ab = Line(point_a, point_b, color=INK, stroke_width=4)
        side_ac = Line(point_a, point_c, color=INK, stroke_width=4)
        base_bc = Line(point_b, point_c, color=INK, stroke_width=4)
        line_ad = Line(point_a, point_d, color=POINT, stroke_width=4)
        line_ae = Line(point_a, point_e, color=PURPLE, stroke_width=4)
        extension_eb = Line(point_e, point_b, color=MUTED, stroke_width=3)
        ac_extension = DashedLine(
            point_a,
            point_a
            + 1.25
            * np.array(
                [np.cos(ac_direction + np.pi), np.sin(ac_direction + np.pi), 0.0]
            ),
            color=HAIRLINE,
            stroke_width=2,
            dash_length=0.09,
        )

        given = MathTex(
            r"\angle B>\angle C",
            font_size=40,
            color=INK,
        ).move_to([3.45, 1.65, 0])
        target_caption = label("要求", 24, MUTED, "MEDIUM")
        target_caption.move_to([3.45, 0.82, 0])
        target = MathTex(
            r"4\angle C-2\angle B+\angle A",
            "=",
            "?",
            font_size=43,
            color=INK,
        ).move_to([3.45, 0.05, 0])
        target[2].set_color(POINT)
        opening_prompt = label("先讀圖，不急著算", 30, INK, "BOLD")
        opening_prompt.move_to([3.45, -1.05, 0])

        # Beat 01 build_triangle: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), Create(base_bc), run_time=0.8)
        self.play(
            LaggedStart(Create(side_ab), Create(side_ac), lag_ratio=0.18),
            LaggedStart(
                GrowFromCenter(dot_a),
                GrowFromCenter(dot_b),
                GrowFromCenter(dot_c),
                FadeIn(label_a),
                FadeIn(label_b),
                FadeIn(label_c),
                lag_ratio=0.09,
            ),
            run_time=1.15,
        )
        self.play(FadeIn(given), FadeIn(target_caption), Write(target), run_time=0.8)
        self.play(FadeIn(opening_prompt), run_time=0.45)

        # Beat 02 place_bisectors: settled semantic step.
        self.next_slide()

        interior_left = Arc(
            radius=0.38,
            start_angle=ab_direction,
            angle=x_angle,
            arc_center=point_a,
            color=POINT,
            stroke_width=5,
        )
        interior_right = Arc(
            radius=0.38,
            start_angle=ad_direction,
            angle=x_angle,
            arc_center=point_a,
            color=POINT,
            stroke_width=5,
        )
        exterior_size = np.pi / 2 - x_angle
        exterior_lower = Arc(
            radius=0.58,
            start_angle=ae_direction,
            angle=exterior_size,
            arc_center=point_a,
            color=PURPLE,
            stroke_width=5,
        )
        exterior_upper = Arc(
            radius=0.58,
            start_angle=ac_direction + np.pi,
            angle=exterior_size,
            arc_center=point_a,
            color=PURPLE,
            stroke_width=5,
        )
        x_left = self.angle_label(
            "x",
            point_a,
            0.69,
            (ab_direction + ad_direction) / 2,
            POINT,
        )
        x_right = self.angle_label(
            "x",
            point_a,
            0.69,
            (ad_direction + ac_direction) / 2,
            POINT,
        )
        y_lower = self.angle_label(
            "y",
            point_a,
            0.88,
            (ae_direction + ab_direction) / 2,
            PURPLE,
        )
        y_upper = self.angle_label(
            "y",
            point_a,
            0.88,
            ac_direction + np.pi + exterior_size / 2,
            PURPLE,
        )
        point_order = label(
            "底邊順序：E — B — D — C",
            24,
            MUTED,
            "MEDIUM",
            t2c={"E": PURPLE, "D": POINT},
        ).move_to([3.45, -1.88, 0])
        bisector_note = label(
            "AD 平分內角｜AE 平分外角",
            28,
            INK,
            "BOLD",
            t2c={"AD": POINT, "AE": PURPLE},
        ).move_to([3.45, -1.05, 0])

        self.play(FadeOut(opening_prompt), Create(line_ad), run_time=0.8)
        self.play(
            GrowFromCenter(dot_d),
            FadeIn(label_d),
            Create(interior_left),
            Create(interior_right),
            FadeIn(x_left),
            FadeIn(x_right),
            run_time=0.8,
        )
        self.play(Create(extension_eb), Create(line_ae), run_time=0.9)
        # Beat 03 mark_bisected_angles: settled semantic step.
        self.next_slide()
        self.play(
            GrowFromCenter(dot_e),
            FadeIn(label_e),
            Create(ac_extension),
            Create(exterior_lower),
            Create(exterior_upper),
            FadeIn(y_lower),
            FadeIn(y_upper),
            run_time=0.9,
        )
        self.play(FadeIn(bisector_note), FadeIn(point_order), run_time=0.5)

        # Beat 04 see_right_angle: settled semantic step.
        self.next_slide()

        straight_prompt = label("沿同一個平角：x、x、y、y", 28, INK, "BOLD")
        straight_prompt.move_to([3.45, -1.05, 0])
        straight_equation = MathTex(
            "2x",
            "+",
            "2y",
            "=",
            r"180^\circ",
            font_size=43,
            color=INK,
        ).move_to([3.45, -1.82, 0])
        straight_equation[0].set_color(POINT)
        straight_equation[2].set_color(PURPLE)
        perpendicular_equation = MathTex(
            "x",
            "+",
            "y",
            "=",
            r"90^\circ",
            font_size=46,
            color=INK,
        ).move_to([3.45, -2.62, 0])
        perpendicular_equation[0].set_color(POINT)
        perpendicular_equation[2].set_color(PURPLE)

        ad_unit = (point_d - point_a) / np.linalg.norm(point_d - point_a)
        ae_unit = (point_e - point_a) / np.linalg.norm(point_e - point_a)
        marker_size = 0.24
        right_marker = VMobject(color=REGION, stroke_width=5)
        right_marker.set_points_as_corners(
            [
                point_a + marker_size * ad_unit,
                point_a + marker_size * (ad_unit + ae_unit),
                point_a + marker_size * ae_unit,
            ]
        )
        perpendicular_note = MathTex(
            r"AD\perp AE",
            font_size=39,
            color=REGION,
        ).move_to([3.45, -3.27, 0])

        self.play(
            FadeOut(bisector_note),
            FadeOut(point_order),
            FadeIn(straight_prompt),
            run_time=0.45,
        )
        self.play(Indicate(interior_right, color=interior_right.get_color()), run_time=0.42)
        self.play(Indicate(interior_left, color=interior_left.get_color()), run_time=0.42)

        # Beat 05 inspect_exterior_bisectors: settled semantic step.
        self.next_slide()
        self.play(Indicate(exterior_lower, color=exterior_lower.get_color()), run_time=0.42)
        self.play(Indicate(exterior_upper, color=exterior_upper.get_color()), run_time=0.42)
        self.play(Write(straight_equation), run_time=0.75)

        # Beat 06 derive_perpendicular_bisectors: settled semantic step.
        self.next_slide()
        self.play(TransformFromCopy(straight_equation, perpendicular_equation), run_time=0.8)
        self.play(Create(right_marker), FadeIn(perpendicular_note), run_time=0.75)

        # Beat 07 complete_special_triangle: settled semantic step.
        self.next_slide()

        line_ed_focus = Line(point_e, point_d, color=INK, stroke_width=4)
        triangle_ade = Polygon(
            point_a,
            point_d,
            point_e,
            color=REGION,
            stroke_width=2,
            fill_color=REGION,
            fill_opacity=0.08,
        ).set_z_index(-2)
        remove_for_focus = VGroup(
            side_ab,
            side_ac,
            base_bc,
            extension_eb,
            ac_extension,
            dot_b,
            dot_c,
            label_b,
            label_c,
            given,
            target_caption,
            target,
            point_order,
            straight_prompt,
            straight_equation,
            perpendicular_equation,
            perpendicular_note,
            interior_left,
            interior_right,
            exterior_lower,
            exterior_upper,
            x_left,
            x_right,
            y_lower,
            y_upper,
        )
        ad_length = MathTex("AD", "=", "u", font_size=31, color=INK)
        ad_length[0].set_color(POINT)
        ad_length.move_to(point_a * 0.48 + point_d * 0.52 + RIGHT * 0.48)
        ae_length = MathTex(r"AE", "=", r"\sqrt{3}\,u", font_size=31, color=INK)
        ae_length[0].set_color(PURPLE)
        ae_length.move_to(point_a * 0.5 + point_e * 0.5 + LEFT * 0.25 + UP * 0.28)
        pythagoras_title = label("先由長度找角度", 30, INK, "BOLD")
        pythagoras_title.move_to([3.42, 1.8, 0])
        pythagoras_1 = MathTex(
            r"DE^2",
            "=",
            "u^2",
            "+",
            r"(\sqrt{3}u)^2",
            font_size=39,
            color=INK,
        ).move_to([3.42, 0.92, 0])
        pythagoras_1[2].set_color(POINT)
        pythagoras_1[4].set_color(PURPLE)
        pythagoras_2 = MathTex(
            r"DE^2=4u^2",
            font_size=39,
            color=INK,
        ).move_to([3.42, 0.08, 0])
        de_result = MathTex(r"DE=2u", font_size=45, color=REGION)
        de_result.move_to([3.42, -0.74, 0])
        half_hypotenuse = MathTex(
            r"AD=\frac12DE",
            font_size=37,
            color=POINT,
        ).move_to([3.42, -1.62, 0])

        angle_30 = Arc(
            radius=0.42,
            start_angle=0,
            angle=np.pi / 6,
            arc_center=point_e,
            color=REGION,
            stroke_width=5,
        )
        angle_30_label = self.angle_label(
            r"30^\circ", point_e, 0.72, np.pi / 12, REGION, size=25
        )
        angle_60 = Arc(
            radius=0.45,
            start_angle=2 * np.pi / 3,
            angle=np.pi / 3,
            arc_center=point_d,
            color=REGION,
            stroke_width=5,
        )
        angle_60_label = self.angle_label(
            r"60^\circ", point_d, 0.50, 5 * np.pi / 6, REGION, size=25
        )

        self.play(FadeOut(remove_for_focus), Create(line_ed_focus), FadeIn(triangle_ade))
        self.play(FadeIn(ad_length), FadeIn(ae_length), FadeIn(pythagoras_title))
        self.play(Write(pythagoras_1), run_time=0.9)
        # Beat 08 measure_special_triangle: settled semantic step.
        self.next_slide()
        self.play(TransformFromCopy(pythagoras_1, pythagoras_2), run_time=0.75)
        self.play(Write(de_result), Write(half_hypotenuse), run_time=0.75)
        # Beat 09 name_sixty_degree_angle: settled semantic step.
        self.next_slide()
        self.play(Create(angle_30), FadeIn(angle_30_label), run_time=0.55)
        self.play(Create(angle_60), FadeIn(angle_60_label), run_time=0.65)

        # Beat 10 transfer_sixty: settled semantic step.
        self.next_slide()

        isolated_calculation = VGroup(
            triangle_ade,
            line_ed_focus,
            ad_length,
            ae_length,
            pythagoras_title,
            pythagoras_1,
            pythagoras_2,
            de_result,
            half_hypotenuse,
            angle_30,
            angle_30_label,
        )
        restore_geometry = VGroup(
            side_ab,
            side_ac,
            base_bc,
            extension_eb,
            dot_b,
            dot_c,
            label_b,
            label_c,
            interior_left,
            interior_right,
            x_left,
            x_right,
        )
        same_ray = Line(point_d, point_e, color=REGION, stroke_width=7)
        same_ray_note = label("射線 DE 與 DB 完全重合", 28, INK, "BOLD")
        same_ray_note.move_to([3.45, 1.02, 0])
        transferred = MathTex(
            r"\angle ADB=60^\circ",
            font_size=42,
            color=REGION,
        ).move_to([3.45, 0.12, 0])
        angle_120 = Arc(
            radius=0.64,
            start_angle=0,
            angle=2 * np.pi / 3,
            arc_center=point_d,
            color=CORAL,
            stroke_width=5,
        )
        angle_120_label = self.angle_label(
            r"120^\circ", point_d, 0.98, np.pi / 3, CORAL, size=27
        )
        linear_pair = MathTex(
            r"\angle ADC",
            "=",
            r"180^\circ-60^\circ",
            "=",
            r"120^\circ",
            font_size=38,
            color=INK,
        ).move_to([3.45, -0.87, 0])
        linear_pair[4].set_color(CORAL)

        self.play(FadeOut(isolated_calculation), FadeIn(restore_geometry), run_time=0.85)
        self.play(Create(same_ray), FadeIn(same_ray_note), run_time=0.65)
        self.play(
            Indicate(VGroup(angle_60, angle_60_label), color=REGION),
            Write(transferred),
            run_time=0.85,
        )
        # Beat 11 transfer_sixty_to_base: settled semantic step.
        self.next_slide()
        self.play(FadeOut(same_ray), Create(angle_120), FadeIn(angle_120_label))
        self.play(Write(linear_pair), run_time=0.8)

        # Beat 12 derive_c: settled semantic step.
        self.next_slide()

        focus_acd = Polygon(
            point_a,
            point_c,
            point_d,
            color=BLUE,
            stroke_width=5,
            fill_color=BLUE,
            fill_opacity=0.09,
        ).set_z_index(-1)
        c_arc = Arc(
            radius=0.42,
            start_angle=ac_direction + np.pi,
            angle=np.pi - (ac_direction + np.pi),
            arc_center=point_c,
            color=BLUE,
            stroke_width=5,
        )
        c_angle_label = self.angle_label(
            "C", point_c, 0.69, (ac_direction + 2 * np.pi) / 2, BLUE, size=29
        )
        c_sum = MathTex(
            "x",
            "+",
            r"120^\circ",
            "+",
            r"\angle C",
            "=",
            r"180^\circ",
            font_size=39,
            color=INK,
        ).move_to([3.45, 0.55, 0])
        c_sum[0].set_color(POINT)
        c_sum[2].set_color(CORAL)
        c_sum[4].set_color(BLUE)
        c_result = MathTex(
            r"\angle C",
            "=",
            r"60^\circ-x",
            font_size=44,
            color=INK,
        ).move_to([3.45, -0.55, 0])
        c_result[0].set_color(BLUE)
        c_result[2].set_color(BLUE)

        self.play(
            FadeOut(same_ray_note),
            FadeOut(transferred),
            FadeOut(linear_pair),
            FadeIn(focus_acd),
            run_time=0.65,
        )
        self.play(
            Indicate(interior_right, color=POINT),
            Indicate(angle_120, color=CORAL),
            Create(c_arc),
            FadeIn(c_angle_label),
            run_time=0.8,
        )
        self.play(Write(c_sum), run_time=0.8)
        self.play(TransformFromCopy(c_sum, c_result), run_time=0.8)

        # Beat 13 derive_b_and_a: settled semantic step.
        self.next_slide()

        focus_abd = Polygon(
            point_a,
            point_b,
            point_d,
            color=PURPLE,
            stroke_width=5,
            fill_color=PURPLE,
            fill_opacity=0.09,
        ).set_z_index(-1)
        b_angle_size = np.pi + ab_direction
        b_arc = Arc(
            radius=0.42,
            start_angle=0,
            angle=b_angle_size,
            arc_center=point_b,
            color=PURPLE,
            stroke_width=5,
        )
        b_angle_label = self.angle_label(
            "B", point_b, 0.68, 0.82 * b_angle_size, PURPLE, size=27
        )
        b_sum = MathTex(
            "x",
            "+",
            r"60^\circ",
            "+",
            r"\angle B",
            "=",
            r"180^\circ",
            font_size=36,
            color=INK,
        ).move_to([3.45, 0.35, 0])
        b_sum[0].set_color(POINT)
        b_sum[2].set_color(REGION)
        b_sum[4].set_color(PURPLE)
        b_result = MathTex(
            r"\angle B",
            "=",
            r"120^\circ-x",
            font_size=42,
            color=INK,
        ).move_to([3.45, -0.42, 0])
        b_result[0].set_color(PURPLE)
        b_result[2].set_color(PURPLE)
        a_result = MathTex(
            r"\angle A",
            "=",
            "x+x",
            "=",
            "2x",
            font_size=42,
            color=INK,
        ).move_to([3.45, -1.42, 0])
        a_result[0].set_color(POINT)
        a_result[2].set_color(POINT)
        a_result[4].set_color(POINT)

        self.play(
            FadeOut(focus_acd),
            FadeOut(c_arc),
            FadeOut(c_angle_label),
            FadeOut(c_sum),
            FadeIn(focus_abd),
            c_result.animate.move_to([3.45, 1.38, 0]),
            run_time=0.75,
        )
        self.play(
            Indicate(interior_left, color=POINT),
            Indicate(angle_60, color=REGION),
            Create(b_arc),
            FadeIn(b_angle_label),
            run_time=0.8,
        )
        self.play(Write(b_sum), run_time=0.7)
        # Beat 14 solve_segment_lengths: settled semantic step.
        self.next_slide()
        self.play(TransformFromCopy(b_sum, b_result), run_time=0.75)
        self.play(
            Indicate(VGroup(interior_left, interior_right), color=POINT),
            Write(a_result),
            run_time=0.85,
        )

        # Beat 15 cancel_expression: settled semantic step.
        self.next_slide()

        diagram_strokes = VGroup(
            side_ab,
            side_ac,
            base_bc,
            extension_eb,
            line_ad,
            line_ae,
            interior_left,
            interior_right,
            right_marker,
            angle_60,
            angle_120,
        )
        diagram_fills = VGroup(
            dot_a,
            dot_b,
            dot_c,
            dot_d,
            dot_e,
            label_a,
            label_b,
            label_c,
            label_d,
            label_e,
            x_left,
            x_right,
            angle_60_label,
            angle_120_label,
        )
        diagram = VGroup(diagram_strokes, diagram_fills)
        central_goal = MathTex(
            r"4\angle C-2\angle B+\angle A",
            "=",
            "?",
            font_size=46,
            color=INK,
        ).move_to([0.8, 2.42, 0])
        central_goal[2].set_color(POINT)
        substitution = MathTex(
            "=",
            "4(",
            r"60^\circ-x",
            ")",
            "-2(",
            r"120^\circ-x",
            ")",
            "+",
            "2x",
            font_size=42,
            color=INK,
        ).move_to([0.8, 1.28, 0])
        substitution[2].set_color(BLUE)
        substitution[5].set_color(PURPLE)
        substitution[8].set_color(POINT)
        expanded = MathTex(
            "=",
            r"240^\circ",
            "-4x",
            r"-240^\circ",
            "+2x",
            "+2x",
            font_size=45,
            color=INK,
        ).move_to([0.8, 0.12, 0])
        expanded[1].set_color(BLUE)
        expanded[3].set_color(CORAL)
        expanded[2].set_color(BLUE)
        expanded[4].set_color(PURPLE)
        expanded[5].set_color(POINT)
        constant_box = VGroup(
            SurroundingRectangle(
                expanded[1], color=REGION, buff=0.12, stroke_width=3
            ),
            SurroundingRectangle(
                expanded[3], color=REGION, buff=0.12, stroke_width=3
            ),
        )
        variable_box = VGroup(
            *(
                SurroundingRectangle(
                    expanded[index], color=POINT, buff=0.12, stroke_width=3
                )
                for index in (2, 4, 5)
            )
        )
        constants_cancel = MathTex(
            r"240^\circ-240^\circ=0",
            font_size=37,
            color=REGION,
        ).move_to([-1.7, -1.05, 0])
        variables_cancel = MathTex(
            r"-4x+2x+2x=0",
            font_size=37,
            color=POINT,
        ).move_to([3.25, -1.05, 0])
        answer = MathTex(
            r"4\angle C-2\angle B+\angle A=0^\circ",
            font_size=52,
            color=REGION,
        ).move_to([0.8, -2.28, 0])
        answer_box = SurroundingRectangle(answer, color=POINT, buff=0.25, stroke_width=3)

        self.play(
            FadeOut(focus_abd),
            FadeOut(b_arc),
            FadeOut(b_angle_label),
            FadeOut(b_sum),
            diagram_strokes.animate.set_stroke(opacity=0.14),
            diagram_fills.animate.set_fill(opacity=0.14),
            FadeIn(central_goal),
            run_time=0.85,
        )
        punctuation = VGroup(
            substitution[0],
            substitution[1],
            substitution[3],
            substitution[4],
            substitution[6],
            substitution[7],
        )
        self.play(FadeIn(punctuation), run_time=0.4)
        self.play(
            TransformFromCopy(c_result[2], substitution[2]),
            TransformFromCopy(b_result[2], substitution[5]),
            TransformFromCopy(a_result[4], substitution[8]),
            run_time=1.05,
        )
        # Beat 16 substitute_length_relations: settled semantic step.
        self.next_slide()
        self.play(FadeOut(c_result), FadeOut(b_result), FadeOut(a_result), run_time=0.4)
        self.play(TransformFromCopy(substitution, expanded), run_time=0.95)
        self.play(Create(constant_box), Write(constants_cancel), run_time=0.7)
        # Beat 17 cancel_common_terms: settled semantic step.
        self.next_slide()
        self.play(FadeOut(constant_box), run_time=0.25)
        self.play(Create(variable_box), Write(variables_cancel), run_time=0.7)
        # Beat 18 simplify_target_expression: settled semantic step.
        self.next_slide()
        self.play(FadeOut(variable_box), run_time=0.25)
        self.play(Write(answer), Create(answer_box), run_time=0.9)

        # Beat 19 consolidate: settled semantic step.
        self.next_slide()

        calculation = VGroup(
            central_goal,
            substitution,
            expanded,
            constant_box,
            variable_box,
            constants_cancel,
            variables_cancel,
            answer,
            answer_box,
        )
        recap_title = label("三個關鍵，依序串起來", 31, INK, "BOLD")
        recap_title.move_to([3.35, 1.82, 0])
        recap_perpendicular = MathTex(
            r"AD\perp AE",
            font_size=38,
            color=REGION,
        ).move_to([3.35, 0.94, 0])
        recap_sixty = MathTex(
            r"\angle ADB=60^\circ",
            font_size=38,
            color=REGION,
        ).move_to([3.35, 0.14, 0])
        recap_angles = MathTex(
            r"C=60^\circ-x,\quad B=120^\circ-x,\quad A=2x",
            font_size=32,
            color=INK,
        ).move_to([3.35, -0.72, 0])
        final_answer = MathTex(
            r"4C-2B+A=0^\circ",
            font_size=48,
            color=POINT,
        ).move_to([3.35, -1.75, 0])
        final_box = SurroundingRectangle(
            final_answer,
            color=REGION,
            buff=0.22,
            stroke_width=3,
        )

        self.play(
            FadeOut(calculation),
            diagram_strokes.animate.set_stroke(opacity=1),
            diagram_fills.animate.set_fill(opacity=1),
            run_time=0.8,
        )
        self.play(FadeIn(recap_title), run_time=0.4)
        self.play(
            Circumscribe(right_marker, color=REGION),
            FadeIn(recap_perpendicular),
            run_time=0.75,
        )
        # Beat 20 reveal_final_value: settled semantic step.
        self.next_slide()
        self.play(
            Circumscribe(VGroup(angle_60, angle_60_label), color=REGION),
            FadeIn(recap_sixty),
            run_time=0.75,
        )
        self.play(FadeIn(recap_angles), run_time=0.65)
        self.play(Write(final_answer), Create(final_box), run_time=0.85)
