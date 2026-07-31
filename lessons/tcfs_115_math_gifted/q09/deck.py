"""Interactive Manim Slides solution for question 9."""

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
    REGION_DARK,
    WHITE,
    CarloSlide,
    label,
)
from carlo_manim.components import filled_shape
from manim import (
    Angle,
    Arc,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
    always_redraw,
    linear,
    smooth,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class Question9Slide(CarloSlide):
    """Discover the locus, prove its symmetry, and calculate one half."""

    def construct(self) -> None:
        scale = 0.53
        diagram_center = np.array([-3.75, -0.25, 0.0])

        def point(x: float, y: float) -> np.ndarray:
            return diagram_center + scale * np.array([x, y, 0.0])

        point_a = point(-2, 0)
        point_b = point(2, 0)
        small_radius = 2 * scale
        large_radius = 4 * scale
        upper_center = point(0, 2 * np.sqrt(3))
        lower_center = point(0, -2 * np.sqrt(3))

        # Sampled boundaries used throughout the explanation.
        upper_outer_points = [
            upper_center
            + large_radius * np.array([np.cos(theta), np.sin(theta), 0])
            for theta in np.linspace(4 * np.pi / 3, -np.pi / 3, 220)
        ]
        upper_inner_points = [
            diagram_center
            + small_radius * np.array([np.cos(theta), np.sin(theta), 0])
            for theta in np.linspace(0, np.pi, 100)
        ]
        lower_outer_points = [
            lower_center
            + large_radius * np.array([np.cos(theta), np.sin(theta), 0])
            for theta in np.linspace(2 * np.pi / 3, 7 * np.pi / 3, 220)
        ]
        lower_inner_points = [
            diagram_center
            + small_radius * np.array([np.cos(theta), np.sin(theta), 0])
            for theta in np.linspace(0, -np.pi, 100)
        ]

        upper_region = filled_shape(
            [*upper_outer_points, *upper_inner_points],
            REGION,
            0.12,
        )
        lower_region = filled_shape(
            [*lower_outer_points, *lower_inner_points],
            REGION,
            0.12,
        )

        upper_outer_arc = Arc(
            radius=large_radius,
            start_angle=4 * np.pi / 3,
            angle=-5 * np.pi / 3,
            arc_center=upper_center,
            color=REGION,
            stroke_width=5,
        ).set_z_index(1)
        upper_inner_arc = Arc(
            radius=small_radius,
            start_angle=0,
            angle=np.pi,
            arc_center=diagram_center,
            color=REGION,
            stroke_width=5,
        ).set_z_index(1)
        lower_outer_arc = Arc(
            radius=large_radius,
            start_angle=2 * np.pi / 3,
            angle=5 * np.pi / 3,
            arc_center=lower_center,
            color=REGION,
            stroke_width=5,
        ).set_z_index(1)
        lower_inner_arc = Arc(
            radius=small_radius,
            start_angle=0,
            angle=-np.pi,
            arc_center=diagram_center,
            color=REGION,
            stroke_width=5,
        ).set_z_index(1)

        segment_ab = Line([-2.1, 0, 0], [2.1, 0, 0], color=INK, stroke_width=7)
        dot_a = Dot(segment_ab.get_start(), radius=0.085, color=WHITE)
        dot_b = Dot(segment_ab.get_end(), radius=0.085, color=WHITE)
        label_a = label("A", 34, INK, "BOLD").next_to(dot_a, DOWN, buff=0.18)
        label_b = label("B", 34, INK, "BOLD").next_to(dot_b, DOWN, buff=0.18)
        length_label = label("AB = 4", 31, MUTED, "MEDIUM").next_to(
            segment_ab,
            UP,
            buff=0.25,
        )

        # Beat 01 fixed_segment: settled semantic step.
        self.play(Create(segment_ab), run_time=1.0)
        self.play(
            LaggedStart(
                GrowFromCenter(dot_a),
                GrowFromCenter(dot_b),
                FadeIn(label_a),
                FadeIn(label_b),
                FadeIn(length_label),
                lag_ratio=0.12,
            ),
            run_time=0.9,
        )

        # Beat 02 introduce_p: settled semantic step.
        self.next_slide()

        final_segment = Line(point_a, point_b, color=INK, stroke_width=6)
        final_dot_a = Dot(point_a, radius=0.065, color=WHITE)
        final_dot_b = Dot(point_b, radius=0.065, color=WHITE)
        final_label_a = label("A", 24, INK, "BOLD").next_to(
            final_dot_a,
            DOWN + LEFT * 0.2,
            buff=0.12,
        )
        final_label_b = label("B", 24, INK, "BOLD").next_to(
            final_dot_b,
            DOWN + RIGHT * 0.2,
            buff=0.12,
        )
        final_length_label = label("AB = 4", 22, MUTED, "MEDIUM").next_to(
            final_segment,
            DOWN,
            buff=0.16,
        )

        heading = label("第 9 題｜動點 P 的範圍", 25, MUTED, "BOLD")
        heading.to_corner(UP + RIGHT, buff=0.42)
        condition = label(
            "30° ≤ θ = ∠APB ≤ 90°",
            34,
            INK,
            "BOLD",
            t2c={"θ": POINT, "∠APB": POINT},
        )
        condition.next_to(heading, DOWN, buff=0.18).align_to(heading, RIGHT)
        explore_prompt = label("先別算，看看 P 怎麼動", 31, INK, "MEDIUM")
        explore_prompt.move_to([3.25, 1.05, 0])

        self.play(
            Transform(segment_ab, final_segment),
            Transform(dot_a, final_dot_a),
            Transform(dot_b, final_dot_b),
            Transform(label_a, final_label_a),
            Transform(label_b, final_label_b),
            Transform(length_label, final_length_label),
            FadeIn(heading, shift=DOWN * 0.08),
            FadeIn(condition, shift=DOWN * 0.08),
            run_time=1.15,
        )

        explore_start = point(0, 3.1)
        p_dot = Dot(explore_start, radius=0.09, color=POINT).set_z_index(6)
        p_label = label("P", 25, POINT, "BOLD").set_z_index(7)
        p_label.add_updater(
            lambda mob: mob.next_to(p_dot, UP + RIGHT * 0.35, buff=0.09)
        )
        ap_line = always_redraw(
            lambda: Line(
                p_dot.get_center(),
                dot_a.get_center(),
                color=MUTED,
                stroke_width=3,
            ).set_z_index(3)
        )
        bp_line = always_redraw(
            lambda: Line(
                p_dot.get_center(),
                dot_b.get_center(),
                color=MUTED,
                stroke_width=3,
            ).set_z_index(3)
        )
        p_angle = always_redraw(
            lambda: Angle(
                Line(p_dot.get_center(), dot_a.get_center()),
                Line(p_dot.get_center(), dot_b.get_center()),
                radius=0.25,
                color=POINT,
                stroke_width=4,
            ).set_z_index(5)
        )

        self.play(
            Create(ap_line),
            Create(bp_line),
            GrowFromCenter(p_dot),
            FadeIn(p_label),
            Create(p_angle),
            FadeIn(explore_prompt, shift=UP * 0.08),
            run_time=1.0,
        )

        # Beat 03 explore_p: settled semantic step.
        self.next_slide(loop=True)

        p_90 = point(0, 2)
        p_left = point(-3.0, 3.0)
        p_30 = point(0, 2 * np.sqrt(3) + 4)
        p_right = point(3.0, 3.0)

        self.play(p_dot.animate.move_to(p_90), run_time=1.35, rate_func=smooth)
        self.wait(0.35)
        self.play(p_dot.animate.move_to(p_left), run_time=1.55, rate_func=smooth)
        self.wait(0.35)
        self.play(p_dot.animate.move_to(explore_start), run_time=1.55, rate_func=smooth)
        self.wait(0.35)

        # Beat 04 explore_far_boundary: settled semantic step.
        self.next_slide(loop=True)
        self.play(p_dot.animate.move_to(p_30), run_time=1.75, rate_func=smooth)
        self.wait(0.4)
        self.play(p_dot.animate.move_to(p_right), run_time=1.75, rate_func=smooth)
        self.wait(0.35)
        self.play(p_dot.animate.move_to(explore_start), run_time=1.55, rate_func=smooth)
        self.wait(0.35)

        # Beat 05 pose_locus_question: settled semantic step.
        self.next_slide()

        locus_question = label("P 的全部範圍，會是什麼形狀？", 31, INK, "BOLD")
        locus_question.move_to([3.25, 1.05, 0])
        self.play(FadeTransform(explore_prompt, locus_question), run_time=0.7)

        # Beat 06 reveal_locus_outline: settled semantic step.
        self.next_slide()

        outline_note = label("先看輪廓，不急著算面積", 30, REGION, "BOLD")
        outline_note.move_to([3.25, 1.05, 0])
        self.play(
            FadeTransform(locus_question, outline_note),
            LaggedStart(
                Create(upper_outer_arc),
                Create(upper_inner_arc),
                Create(lower_outer_arc),
                Create(lower_inner_arc),
                lag_ratio=0.16,
            ),
            run_time=1.6,
        )

        # Beat 07 prove_reflection_symmetry: settled semantic step.
        self.next_slide()

        sample_upper = point(-2.2, 2.8)
        sample_lower = point(-2.2, -2.8)
        self.play(p_dot.animate.move_to(sample_upper), run_time=1.0, rate_func=smooth)

        p_prime = Dot(sample_lower, radius=0.09, color=PURPLE).set_z_index(6)
        p_prime_label = label("P′", 25, PURPLE, "BOLD").next_to(
            p_prime,
            DOWN + RIGHT * 0.35,
            buff=0.09,
        )
        ap_prime = Line(sample_lower, point_a, color=MUTED, stroke_width=3)
        bp_prime = Line(sample_lower, point_b, color=MUTED, stroke_width=3)
        prime_angle = Angle(
            Line(sample_lower, point_a),
            Line(sample_lower, point_b),
            radius=0.25,
            color=PURPLE,
            stroke_width=4,
            other_angle=True,
        ).set_z_index(5)
        reflection_guide = DashedLine(
            sample_upper,
            sample_lower,
            color=HAIRLINE,
            stroke_width=2,
            dash_length=0.12,
        )
        equality = label(
            "鏡射不改變角度：θ′ = θ",
            30,
            INK,
            "BOLD",
        ).move_to([3.25, 1.18, 0])
        symmetry_note = label("所以上、下的範圍完全對應", 27, REGION, "BOLD")
        symmetry_note.next_to(equality, DOWN, buff=0.24)

        self.play(Create(reflection_guide), run_time=0.5)
        self.play(
            TransformFromCopy(p_dot, p_prime),
            TransformFromCopy(ap_line, ap_prime),
            TransformFromCopy(bp_line, bp_prime),
            TransformFromCopy(p_angle, prime_angle),
            FadeIn(p_prime_label),
            run_time=1.25,
        )
        self.play(
            FadeIn(upper_region),
            FadeIn(lower_region),
            FadeTransform(outline_note, equality),
            FadeIn(symmetry_note, shift=UP * 0.08),
            run_time=0.9,
        )

        # Beat 08 isolate_upper_half: settled semantic step.
        self.next_slide()

        half_note = label("先算上半部", 39, REGION, "BOLD")
        half_note.move_to([3.25, 1.15, 0])
        half_subnote = label("算清楚一半，再回到整體", 24, MUTED, "MEDIUM")
        half_subnote.next_to(half_note, DOWN, buff=0.18)
        self.play(
            FadeOut(
                p_prime,
                p_prime_label,
                ap_prime,
                bp_prime,
                prime_angle,
                reflection_guide,
                symmetry_note,
            ),
            FadeTransform(equality, half_note),
            FadeIn(half_subnote, shift=UP * 0.08),
            upper_region.animate.set_fill(REGION, opacity=0.40),
            lower_region.animate.set_fill(REGION_DARK, opacity=0.035),
            lower_outer_arc.animate.set_stroke(opacity=0.18),
            lower_inner_arc.animate.set_stroke(opacity=0.18),
            run_time=1.0,
        )

        # Beat 09 boundary_90: settled semantic step.
        self.next_slide()

        upper_semicircle_points = [
            diagram_center
            + small_radius * np.array([np.cos(theta), np.sin(theta), 0])
            for theta in np.linspace(np.pi, 0, 120)
        ]
        excluded_semicircle = filled_shape(
            upper_semicircle_points,
            CORAL,
            0.38,
            z_index=-2,
        )
        thales_arc = Arc(
            radius=small_radius,
            start_angle=0,
            angle=np.pi,
            arc_center=diagram_center,
            color=CORAL,
            stroke_width=6,
        ).set_z_index(2)
        angle_90 = Angle(
            Line(p_90, point_a),
            Line(p_90, point_b),
            radius=0.25,
            color=CORAL,
            stroke_width=5,
        ).set_z_index(6)
        angle_90_text = label("90°", 23, CORAL, "BOLD")
        angle_90_text.move_to(p_90 + DOWN * 0.42)
        boundary_90_title = label("先找 90° 的邊界", 30, CORAL, "BOLD")
        boundary_90_title.move_to([3.25, 1.55, 0])
        boundary_90_fact = label(
            "θ ≤ 90°  ⇒  P 在半圓外",
            29,
            INK,
            "BOLD",
            t2c={"θ ≤ 90°": CORAL, "半圓外": REGION},
        )
        boundary_90_fact.next_to(boundary_90_title, DOWN, buff=0.24)

        self.play(
            FadeOut(half_subnote),
            FadeTransform(half_note, boundary_90_title),
            p_dot.animate.move_to(p_90),
            run_time=1.05,
            rate_func=smooth,
        )
        self.play(
            FadeIn(excluded_semicircle),
            Create(thales_arc),
            Create(angle_90),
            FadeIn(angle_90_text),
            run_time=1.0,
        )
        self.play(FadeIn(boundary_90_fact, shift=UP * 0.08), run_time=0.6)

        # Beat 10 boundary_30: settled semantic step.
        self.next_slide()

        outer_circle_guide = Circle(
            radius=large_radius,
            color=BLUE,
            stroke_width=2,
            stroke_opacity=0.28,
        ).move_to(upper_center)
        outer_focus_arc = Arc(
            radius=large_radius,
            start_angle=4 * np.pi / 3,
            angle=-5 * np.pi / 3,
            arc_center=upper_center,
            color=BLUE,
            stroke_width=6,
        ).set_z_index(2)
        center_dot = Dot(upper_center, radius=0.065, color=BLUE).set_z_index(5)
        center_label = label("O", 23, BLUE, "BOLD").next_to(
            center_dot,
            UP,
            buff=0.08,
        )
        oa = Line(upper_center, point_a, color=BLUE, stroke_width=3).set_z_index(2)
        ob = Line(upper_center, point_b, color=BLUE, stroke_width=3).set_z_index(2)
        center_angle = Angle(oa, ob, radius=0.30, color=BLUE, stroke_width=5)
        center_angle_text = label("60°", 21, BLUE, "BOLD")
        center_angle_text.move_to(upper_center + DOWN * 0.45)
        angle_30 = Angle(
            Line(p_30, point_a),
            Line(p_30, point_b),
            radius=0.27,
            color=BLUE,
            stroke_width=5,
        ).set_z_index(6)
        angle_30_text = label("30°", 22, BLUE, "BOLD")
        angle_30_text.next_to(p_30, DOWN, buff=0.17)
        boundary_30_title = label("再找 30° 的邊界", 30, BLUE, "BOLD")
        boundary_30_title.move_to([3.25, 1.72, 0])
        center_angle_fact = label(
            "圓周角 30°  ⇒  圓心角 60°",
            28,
            INK,
            "BOLD",
            t2c={"30°": POINT, "60°": BLUE},
        )
        center_angle_fact.next_to(boundary_30_title, DOWN, buff=0.22)

        self.play(
            FadeOut(angle_90, angle_90_text, boundary_90_fact),
            FadeTransform(boundary_90_title, boundary_30_title),
            excluded_semicircle.animate.set_fill(opacity=0.18),
            thales_arc.animate.set_stroke(opacity=0.45),
            p_dot.animate.move_to(p_30),
            run_time=1.25,
            rate_func=smooth,
        )
        self.play(
            FadeIn(outer_circle_guide),
            Create(outer_focus_arc),
            GrowFromCenter(center_dot),
            FadeIn(center_label),
            Create(oa),
            Create(ob),
            Create(center_angle),
            FadeIn(center_angle_text),
            Create(angle_30),
            FadeIn(angle_30_text),
            run_time=1.35,
        )
        self.play(FadeIn(center_angle_fact, shift=UP * 0.08), run_time=0.6)

        # Beat 11 derive_radius_sector: settled semantic step.
        self.next_slide()

        center_triangle = Polygon(
            point_a,
            upper_center,
            point_b,
            color=POINT,
            stroke_width=3,
            fill_color=POINT,
            fill_opacity=0.23,
        ).set_z_index(-1)
        radius_fact = label(
            "△AOB 是正三角形  ⇒  R = AB = 4",
            27,
            INK,
            "BOLD",
            t2c={"正三角形": POINT, "R = AB = 4": POINT},
        )
        radius_fact.next_to(center_angle_fact, DOWN, buff=0.22)
        sector_fact = label(
            "優扇形：360° − 60° = 300°",
            27,
            INK,
            "BOLD",
            t2c={"優扇形": BLUE, "300°": BLUE},
        )
        sector_fact.next_to(radius_fact, DOWN, buff=0.20)

        self.play(FadeIn(center_triangle), run_time=0.65)
        self.play(
            TransformFromCopy(center_triangle, radius_fact),
            run_time=0.8,
        )
        self.play(
            TransformFromCopy(outer_focus_arc, sector_fact),
            run_time=0.8,
        )

        # Stop the moving geometry before the calculation begins.
        for moving_mobject in (ap_line, bp_line, p_angle, p_label):
            moving_mobject.clear_updaters()

        # Beat 12 sector_area: settled semantic step.
        self.next_slide()

        major_sector = filled_shape(
            [upper_center, *upper_outer_points],
            BLUE,
            0.34,
            z_index=-3,
        )
        derivation_heading = label(
            "上半部 = 優扇形 + 正三角形 − 半圓",
            29,
            INK,
            "BOLD",
            t2c={"優扇形": BLUE, "正三角形": POINT, "半圓": CORAL},
        )
        derivation_heading.move_to([3.2, 2.05, 0])
        sector_term = label(
            "優扇形：300°/360° × π × 4² = 40π/3",
            26,
            BLUE,
            "BOLD",
        )
        sector_term.move_to([3.2, 0.95, 0])

        self.play(
            FadeOut(
                p_dot,
                p_label,
                ap_line,
                bp_line,
                p_angle,
                angle_30,
                angle_30_text,
                boundary_30_title,
                center_angle_fact,
                radius_fact,
                sector_fact,
            ),
            FadeIn(derivation_heading, shift=DOWN * 0.08),
            FadeIn(major_sector),
            run_time=0.9,
        )
        self.play(
            Indicate(outer_focus_arc, color=BLUE, scale_factor=1.02),
            TransformFromCopy(outer_focus_arc, sector_term),
            run_time=1.0,
        )

        # Beat 13 triangle_area: settled semantic step.
        self.next_slide()

        triangle_term = label(
            "加正三角形：√3/4 × 4² = 4√3",
            26,
            POINT,
            "BOLD",
        )
        triangle_term.next_to(sector_term, DOWN, buff=0.23).align_to(
            sector_term,
            LEFT,
        )
        self.play(
            Indicate(center_triangle, color=POINT, scale_factor=1.03),
            TransformFromCopy(center_triangle, triangle_term),
            run_time=1.0,
        )

        # Beat 14 subtract_semicircle: settled semantic step.
        self.next_slide()

        semicircle_term = label(
            "扣半圓：1/2 × π × 2² = 2π",
            26,
            CORAL,
            "BOLD",
        )
        semicircle_term.next_to(triangle_term, DOWN, buff=0.23).align_to(
            sector_term,
            LEFT,
        )
        self.play(
            excluded_semicircle.animate.set_fill(CORAL, opacity=0.52),
            thales_arc.animate.set_stroke(CORAL, opacity=1, width=6),
            run_time=0.65,
        )
        self.play(
            Indicate(thales_arc, color=CORAL, scale_factor=1.03),
            TransformFromCopy(thales_arc, semicircle_term),
            run_time=1.0,
        )

        # Beat 15 upper_result: settled semantic step.
        self.next_slide()

        upper_expression = label(
            "A上 = 40π/3 + 4√3 − 2π",
            31,
            INK,
            "BOLD",
            t2c={"40π/3": BLUE, "4√3": POINT, "− 2π": CORAL},
        )
        upper_expression.move_to([3.2, -1.15, 0])
        upper_result = label(
            "A上 = 34π/3 + 4√3",
            37,
            REGION,
            "BOLD",
        ).move_to([3.2, -1.15, 0])

        self.play(
            TransformFromCopy(
                VGroup(sector_term, triangle_term, semicircle_term),
                upper_expression,
            ),
            run_time=1.0,
        )
        self.play(Transform(upper_expression, upper_result), run_time=0.8)
        self.play(
            FadeOut(major_sector, excluded_semicircle),
            center_triangle.animate.set_fill(opacity=0.08),
            upper_region.animate.set_fill(REGION, opacity=0.46),
            Circumscribe(upper_region, color=REGION, fade_out=True),
            run_time=1.1,
        )

        # Beat 16 reflect_and_double: settled semantic step.
        self.next_slide()

        total_relation = label("A總 = 2 × A上", 31, INK, "BOLD")
        total_relation.move_to([3.2, -2.03, 0])
        final_answer = label(
            "A總 = 68π/3 + 8√3",
            41,
            WHITE,
            "BOLD",
            t2c={"68π/3 + 8√3": REGION},
        )
        final_answer.move_to([3.2, -2.20, 0])

        self.play(
            FadeOut(
                derivation_heading,
                sector_term,
                triangle_term,
                semicircle_term,
                center_triangle,
                center_dot,
                center_label,
                oa,
                ob,
                center_angle,
                center_angle_text,
                outer_circle_guide,
                outer_focus_arc,
                thales_arc,
            ),
            lower_region.animate.set_fill(opacity=0),
            upper_expression.animate.move_to([3.2, 0.20, 0]),
            run_time=0.85,
        )

        reflected_half = upper_region.copy().set_z_index(-4)
        self.add(reflected_half)
        self.play(
            reflected_half.animate.flip(axis=RIGHT, about_point=diagram_center),
            run_time=1.65,
            rate_func=smooth,
        )
        self.play(
            TransformFromCopy(upper_expression, total_relation),
            run_time=0.7,
        )
        self.play(
            FadeTransform(total_relation, final_answer),
            Circumscribe(
                VGroup(upper_region, reflected_half),
                color=REGION,
                fade_out=True,
            ),
            run_time=1.0,
        )

        # Restore P before the final two slides so the loop changes only P.
        p_dot.move_to(explore_start).set_opacity(1)
        final_p_label = label("P", 25, POINT, "BOLD").set_z_index(7)
        final_p_label.add_updater(
            lambda mob: mob.next_to(p_dot, UP + RIGHT * 0.35, buff=0.09)
        )
        final_ap = always_redraw(
            lambda: Line(
                p_dot.get_center(),
                dot_a.get_center(),
                color=MUTED,
                stroke_width=2.5,
            ).set_z_index(3)
        )
        final_bp = always_redraw(
            lambda: Line(
                p_dot.get_center(),
                dot_b.get_center(),
                color=MUTED,
                stroke_width=2.5,
            ).set_z_index(3)
        )
        final_angle = always_redraw(
            lambda: Angle(
                Line(p_dot.get_center(), dot_a.get_center()),
                Line(p_dot.get_center(), dot_b.get_center()),
                radius=0.23,
                color=POINT,
                stroke_width=4,
            ).set_z_index(5)
        )
        # Beat 17 restore_moving_point: settled semantic step.
        self.next_slide()
        self.play(
            FadeIn(p_dot),
            FadeIn(final_p_label),
            FadeIn(final_ap),
            FadeIn(final_bp),
            FadeIn(final_angle),
            run_time=0.75,
        )

        # Beat 18 consolidate: settled semantic step.
        self.next_slide(loop=True)

        self.play(p_dot.animate.move_to(p_left), run_time=1.7, rate_func=smooth)
        self.play(p_dot.animate.move_to(p_30), run_time=1.8, rate_func=smooth)
        self.play(p_dot.animate.move_to(p_right), run_time=1.8, rate_func=smooth)
        self.play(
            p_dot.animate.move_to(explore_start),
            run_time=1.7,
            rate_func=smooth,
        )
        self.wait(0.35)
