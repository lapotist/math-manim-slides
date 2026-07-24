"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q12."""

from __future__ import annotations

import math

import numpy as np

from carlo_manim import (
    BLUE,
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
    CurvedArrow,
    DashedLine,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RightAngle,
    Rotate,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
    always_redraw,
    rate_functions,
)
from manim.constants import DOWN, LEFT, PI, RIGHT, UP


class Tcfs115Q12Slide(CarloSlide):
    """Turn a weighted distance into a straight, attainable shortest path."""

    lesson_id = "carlo.tcfs_115_math_gifted.q12"

    @staticmethod
    def tick(start: np.ndarray, end: np.ndarray, *, color: str = MUTED) -> Line:
        """Return one congruence tick centered on a segment."""
        direction = end - start
        normal = np.array([-direction[1], direction[0], 0.0])
        normal /= np.linalg.norm(normal)
        midpoint = (start + end) / 2
        return Line(
            midpoint - 0.10 * normal,
            midpoint + 0.10 * normal,
            color=color,
            stroke_width=2.4,
        )

    @staticmethod
    def point_tag(text: str, point: np.ndarray, direction: np.ndarray) -> object:
        return label(text, 23, INK, "BOLD").next_to(point, direction, buff=0.10)

    def construct(self) -> None:
        scale = 0.80
        point_a = np.array([-2.10, 0.55, 0.0])

        def model_point(x: float, y: float) -> np.ndarray:
            return point_a + scale * np.array([x, y, 0.0])

        def rotate_clockwise(point: np.ndarray) -> np.ndarray:
            vector = point - point_a
            return point_a + np.array([vector[1], -vector[0], 0.0])

        point_b = model_point(2, -2 * math.sqrt(3))
        point_c = model_point(-2, -2 * math.sqrt(3))
        point_c_prime = rotate_clockwise(point_c)
        point_b_prime = rotate_clockwise(point_b)
        point_e = (point_b + point_c) / 2
        equality_depth = 2 * math.sqrt(3) - 2
        point_p_equal = model_point(0, -equality_depth)
        point_p_prime_equal = rotate_clockwise(point_p_equal)

        heading = label("第 12 題｜把加權距離接成最短路徑", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜第壹部分第 12 題・PDF 第 8 頁",
            16,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        edge_ab = Line(point_a, point_b, color=MUTED, stroke_width=3.2)
        edge_bc = Line(point_b, point_c, color=MUTED, stroke_width=3.2)
        edge_ca = Line(point_c, point_a, color=MUTED, stroke_width=3.2)
        triangle_edges = VGroup(edge_ab, edge_bc, edge_ca)
        congruence_ticks = VGroup(
            self.tick(point_a, point_b),
            self.tick(point_b, point_c),
            self.tick(point_c, point_a),
        )
        vertex_dots = VGroup(
            Dot(point_a, radius=0.065, color=WHITE),
            Dot(point_b, radius=0.065, color=WHITE),
            Dot(point_c, radius=0.065, color=WHITE),
        )
        vertex_labels = VGroup(
            self.point_tag("A", point_a, UP),
            self.point_tag("B", point_b, DOWN + RIGHT * 0.25),
            self.point_tag("C", point_c, DOWN + LEFT * 0.25),
        )
        side_note = label(
            "正三角形｜三邊都是 4",
            23,
            MUTED,
            "MEDIUM",
            t2c={"4": POINT},
        ).move_to([-2.10, -3.02, 0])

        point_p_generic = model_point(0.55, -1.55)
        p_dot = Dot(point_p_generic, radius=0.085, color=BLUE).set_z_index(8)
        p_label = label("P", 23, BLUE, "BOLD").set_z_index(9)
        p_label.add_updater(lambda mob: mob.next_to(p_dot, RIGHT, buff=0.10))
        ap_line = always_redraw(
            lambda: Line(
                point_a,
                p_dot.get_center(),
                color=BLUE,
                stroke_width=4.0,
            ).set_z_index(3)
        )
        bp_line = always_redraw(
            lambda: Line(
                point_b,
                p_dot.get_center(),
                color=POINT,
                stroke_width=4.0,
            ).set_z_index(3)
        )
        cp_line = always_redraw(
            lambda: Line(
                point_c,
                p_dot.get_center(),
                color=REGION,
                stroke_width=4.0,
            ).set_z_index(3)
        )
        objective = MathTex(
            r"\sqrt{2}AP",
            "+",
            "BP",
            "+",
            "CP",
            font_size=45,
            color=INK,
        ).move_to([3.45, 1.60, 0])
        objective[0].set_color(BLUE)
        objective[2].set_color(POINT)
        objective[4].set_color(REGION)
        objective_caption = label("要讓這個總和最小", 29, INK, "BOLD").next_to(
            objective, UP, buff=0.30
        )

        # Beat 01 build_equilateral: establish the fixed triangle and three distances.
        self.play(FadeIn(heading), FadeIn(source), run_time=0.45)
        self.play(Create(edge_bc), run_time=0.65)
        self.play(Create(edge_ab), Create(edge_ca), run_time=0.85)
        self.play(
            FadeIn(vertex_dots),
            FadeIn(vertex_labels),
            Create(congruence_ticks),
            FadeIn(side_note),
            run_time=0.80,
        )
        self.play(GrowFromCenter(p_dot), FadeIn(p_label), run_time=0.55)
        self.play(
            LaggedStart(Create(ap_line), Create(bp_line), Create(cp_line), lag_ratio=0.18),
            run_time=1.15,
        )
        self.play(FadeIn(objective_caption), Write(objective), run_time=0.90)

        bar_starts = (
            np.array([2.15, 0.10, 0.0]),
            np.array([2.15, -0.73, 0.0]),
            np.array([2.15, -1.56, 0.0]),
        )
        bar_guides = VGroup(
            *(Line(start, start + RIGHT * 3.20, color=HAIRLINE, stroke_width=3) for start in bar_starts)
        )
        bar_labels = VGroup(
            MathTex(r"\sqrt2 AP", font_size=28, color=BLUE).next_to(bar_starts[0], LEFT, buff=0.18),
            MathTex("BP", font_size=28, color=POINT).next_to(bar_starts[1], LEFT, buff=0.18),
            MathTex("CP", font_size=28, color=REGION).next_to(bar_starts[2], LEFT, buff=0.18),
        )

        def contribution_bar(start: np.ndarray, color: str, factor: float, fixed: np.ndarray) -> object:
            return always_redraw(
                lambda: Line(
                    start,
                    start
                    + RIGHT
                    * min(
                        3.15,
                        0.72
                        * factor
                        * np.linalg.norm(p_dot.get_center() - fixed)
                        / scale,
                    ),
                    color=color,
                    stroke_width=8,
                ).set_z_index(5)
            )

        contribution_bars = VGroup(
            contribution_bar(bar_starts[0], BLUE, math.sqrt(2), point_a),
            contribution_bar(bar_starts[1], POINT, 1.0, point_b),
            contribution_bar(bar_starts[2], REGION, 1.0, point_c),
        )
        explore_note = label(
            "只移動 P，看三項怎麼互相拉扯",
            25,
            INK,
            "BOLD",
            t2c={"P": BLUE, "三項": POINT},
        ).move_to([3.65, -2.30, 0])

        # Beat 02 explore_p: loop through deliberate interior states and return exactly.
        self.next_slide(loop=True)
        self.add(bar_guides, bar_labels, contribution_bars, explore_note)
        self.wait(0.35)
        self.play(
            p_dot.animate.move_to(model_point(0.08, -0.52)),
            run_time=1.50,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.35)
        self.play(
            p_dot.animate.move_to(model_point(-0.15, -3.05)),
            run_time=1.70,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.35)
        self.play(
            p_dot.animate.move_to(model_point(1.20, -2.45)),
            run_time=1.65,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.35)
        self.play(
            p_dot.animate.move_to(point_p_generic),
            run_time=1.65,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.wait(0.40)

        schematic_bp = Line([1.15, -0.72, 0], [2.55, -0.72, 0], color=POINT, stroke_width=6)
        schematic_cp = Line([4.72, -0.72, 0], [6.15, -0.72, 0], color=REGION, stroke_width=6)
        schematic_labels = VGroup(
            MathTex("BP", font_size=27, color=POINT).next_to(schematic_bp, DOWN, buff=0.13),
            MathTex("CP", font_size=27, color=REGION).next_to(schematic_cp, DOWN, buff=0.13),
        )
        missing_box = DashedVMobject(
            Rectangle(width=1.66, height=0.76, color=BLUE, stroke_width=2.4),
            num_dashes=18,
        ).move_to([3.63, -0.72, 0])
        missing_term = MathTex(r"\sqrt2 AP", font_size=30, color=BLUE).move_to(missing_box)
        missing_note = label("還不是一條可接的線段", 22, BLUE, "MEDIUM").next_to(
            missing_box, UP, buff=0.18
        )
        straightening_prompt = label(
            "怎樣把第一項，變成真正的線段？",
            29,
            INK,
            "BOLD",
            t2c={"第一項": BLUE},
        ).move_to([3.65, 2.65, 0])

        # Beat 03 pose_straightening: isolate the one term that cannot yet form a path.
        self.next_slide()
        self.play(
            FadeOut(bar_guides),
            FadeOut(bar_labels),
            FadeOut(contribution_bars),
            FadeOut(explore_note),
            FadeOut(objective_caption),
            run_time=0.60,
        )
        self.play(FadeIn(straightening_prompt), run_time=0.55)
        self.play(Create(schematic_bp), FadeIn(schematic_labels[0]), run_time=0.55)
        self.play(FadeIn(missing_box), FadeIn(missing_term), FadeIn(missing_note), run_time=0.65)
        self.play(Create(schematic_cp), FadeIn(schematic_labels[1]), run_time=0.55)
        self.play(Indicate(objective[0], color=BLUE), run_time=0.75)
        self.wait(0.35)

        rotating_copy = VGroup(
            Line(point_a, point_b, color=MUTED, stroke_width=2.6),
            Line(point_b, point_c, color=MUTED, stroke_width=2.6),
            Line(point_c, point_a, color=MUTED, stroke_width=2.6),
            Line(point_a, point_p_generic, color=BLUE, stroke_width=4.0),
            Line(point_b, point_p_generic, color=POINT, stroke_width=3.4),
            Line(point_c, point_p_generic, color=REGION, stroke_width=4.0),
            Dot(point_b, radius=0.06, color=MUTED),
            Dot(point_c, radius=0.075, color=PURPLE),
            Dot(point_p_generic, radius=0.085, color=PURPLE),
        ).set_opacity(0.72)
        ap_direction = point_p_generic - point_a
        ap_direction /= np.linalg.norm(ap_direction)
        ap_prime_direction = rotate_clockwise(point_a + ap_direction) - point_a
        rotation_arrow = CurvedArrow(
            point_a + 0.58 * ap_direction,
            point_a + 0.58 * ap_prime_direction,
            angle=-PI / 2,
            color=PURPLE,
            stroke_width=3.2,
            tip_length=0.14,
        )
        rotated_point_p = rotate_clockwise(point_p_generic)
        prime_p_label = label("P′", 22, PURPLE, "BOLD").set_z_index(9)
        prime_p_label.add_updater(
            lambda mob: mob.next_to(rotating_copy[8], DOWN + LEFT * 0.15, buff=0.09)
        )
        prime_c_label = label("C′", 22, PURPLE, "BOLD").next_to(
            point_c_prime, UP + LEFT * 0.15, buff=0.10
        )
        prime_b_label = label("B′", 19, MUTED, "MEDIUM").next_to(
            point_b_prime, DOWN + LEFT * 0.15, buff=0.08
        )
        rotation_angle_label = MathTex(r"90^\circ", font_size=23, color=PURPLE).move_to(
            point_a + 0.68 * (ap_direction + ap_prime_direction)
        )
        rotation_facts = VGroup(
            MathTex("AP'", "=", "AP", font_size=33, color=INK),
            MathTex("C'P'", "=", "CP", font_size=33, color=INK),
            MathTex(r"\angle PAP'", "=", r"90^\circ", font_size=33, color=INK),
        ).arrange(DOWN, buff=0.23, aligned_edge=LEFT).move_to([3.48, 0.35, 0])
        rotation_facts[0][0].set_color(PURPLE)
        rotation_facts[0][2].set_color(BLUE)
        rotation_facts[1][0].set_color(PURPLE)
        rotation_facts[1][2].set_color(REGION)
        rotation_facts[2][0].set_color(PURPLE)
        rotation_facts[2][2].set_color(PURPLE)

        # Beat 04 rotate_copy: perform the distance-preserving 90-degree map visibly.
        self.next_slide()
        self.play(
            FadeOut(VGroup(schematic_bp, schematic_cp, schematic_labels, missing_box, missing_term, missing_note)),
            FadeOut(straightening_prompt),
            run_time=0.55,
        )
        self.add(rotating_copy)
        self.play(
            Rotate(rotating_copy, angle=-PI / 2, about_point=point_a),
            Create(rotation_arrow),
            run_time=1.80,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            rotating_copy[0].animate.set_opacity(0.14),
            rotating_copy[1].animate.set_opacity(0.14),
            rotating_copy[4].animate.set_opacity(0.14),
            rotating_copy[6].animate.set_opacity(0.20),
            rotating_copy[2].animate.set_opacity(0.42),
            rotating_copy[3].animate.set_opacity(1.0),
            rotating_copy[5].animate.set_opacity(1.0),
            rotating_copy[7].animate.set_opacity(1.0),
            rotating_copy[8].animate.set_opacity(1.0),
            FadeIn(prime_p_label),
            FadeIn(prime_c_label),
            FadeIn(prime_b_label, target_position=point_b_prime),
            run_time=0.70,
        )
        self.play(FadeIn(rotation_angle_label), run_time=0.45)
        self.play(
            TransformFromCopy(rotating_copy[3], rotation_facts[0]),
            TransformFromCopy(rotating_copy[5], rotation_facts[1]),
            FadeIn(rotation_facts[2]),
            run_time=1.00,
        )

        pp_line = Line(point_p_generic, rotated_point_p, color=PURPLE, stroke_width=5.0).set_z_index(5)
        right_triangle_fill = Polygon(
            point_a,
            point_p_generic,
            rotated_point_p,
            color=PURPLE,
            fill_color=PURPLE,
            fill_opacity=0.08,
            stroke_width=0,
        ).set_z_index(-1)
        pythagoras = MathTex(
            "PP'^2",
            "=",
            "AP^2",
            "+",
            "AP'^2",
            font_size=34,
            color=INK,
        )
        pythagoras[0].set_color(PURPLE)
        pythagoras[2].set_color(BLUE)
        pythagoras[4].set_color(PURPLE)
        pythagoras_two = MathTex("PP'^2", "=", "2AP^2", font_size=36, color=INK)
        pythagoras_two[0].set_color(PURPLE)
        pythagoras_two[2].set_color(BLUE)
        pp_relation = MathTex("PP'", "=", r"\sqrt2 AP", font_size=40, color=INK)
        pp_relation[0].set_color(PURPLE)
        pp_relation[2].set_color(BLUE)
        pythagoras_group = VGroup(pythagoras, pythagoras_two, pp_relation).arrange(
            DOWN, buff=0.30, aligned_edge=LEFT
        ).move_to([3.52, 0.22, 0])

        # Beat 05 earn_sqrt_two: earn the weighted segment from visible right-triangle data.
        self.next_slide()
        self.play(FadeOut(rotation_facts), FadeIn(right_triangle_fill), run_time=0.55)
        self.play(
            Indicate(ap_line, color=BLUE),
            Indicate(rotating_copy[3], color=PURPLE),
            run_time=0.75,
        )
        self.play(Create(pp_line), run_time=0.70)
        self.play(TransformFromCopy(VGroup(ap_line, rotating_copy[3]), pythagoras), run_time=0.90)
        self.play(Write(pythagoras_two), run_time=0.70)
        self.play(Write(pp_relation), run_time=0.70)
        self.play(TransformFromCopy(pp_line, objective[0]), run_time=0.65)

        compact_relation = pp_relation.copy().scale(0.78).move_to([3.50, 2.54, 0])
        path_bp = Line(point_b, point_p_generic, color=POINT, stroke_width=6.0).set_z_index(7)
        path_pp = Line(point_p_generic, rotated_point_p, color=PURPLE, stroke_width=6.0).set_z_index(7)
        path_pc_prime = Line(rotated_point_p, point_c_prime, color=REGION, stroke_width=6.0).set_z_index(7)
        path_equation = MathTex(
            r"\sqrt2 AP+BP+CP",
            "=",
            "BP",
            "+",
            "PP'",
            "+",
            "P'C'",
            font_size=34,
            color=INK,
        ).move_to([3.62, 0.35, 0])
        path_equation[0].set_color(MUTED)
        path_equation[2].set_color(POINT)
        path_equation[4].set_color(PURPLE)
        path_equation[6].set_color(REGION)
        path_caption = label(
            "現在三項有同一個起點與終點",
            25,
            INK,
            "BOLD",
        ).move_to([3.62, -0.58, 0])

        # Beat 06 assemble_broken_path: connect the three preserved lengths in order.
        self.next_slide()
        self.play(
            FadeOut(pythagoras),
            FadeOut(pythagoras_two),
            ReplacementTransform(pp_relation, compact_relation),
            objective.animate.set_opacity(0.28),
            triangle_edges.animate.set_opacity(0.42),
            congruence_ticks.animate.set_opacity(0.25),
            run_time=0.65,
        )
        self.play(Create(path_bp), TransformFromCopy(path_bp, path_equation[2]), run_time=0.60)
        self.play(Create(path_pp), TransformFromCopy(path_pp, path_equation[4]), run_time=0.60)
        self.play(Create(path_pc_prime), TransformFromCopy(path_pc_prime, path_equation[6]), run_time=0.65)
        self.play(FadeIn(path_equation[0:2]), FadeIn(path_equation[3]), FadeIn(path_equation[5]), run_time=0.55)
        self.play(FadeIn(path_caption), run_time=0.45)

        generic_ghost = VGroup(path_bp.copy(), path_pp.copy(), path_pc_prime.copy()).set_opacity(0.17)
        direct_line = Line(point_b, point_c_prime, color=INK, stroke_width=3.0).set_z_index(2)
        lower_bound = MathTex(
            "BP+PP'+P'C'",
            r"\ge",
            "BC'",
            font_size=37,
            color=INK,
        ).move_to([3.55, 0.45, 0])
        lower_bound[0].set_color(MUTED)
        lower_bound[2].set_color(WHITE)
        equality_note = label(
            "等號：B、P、P′、C′ 依序共線",
            26,
            INK,
            "BOLD",
        ).move_to([3.55, -0.40, 0])
        attainable_note = label(
            "交點 P 確實在正三角形內｜下界可達",
            24,
            REGION,
            "BOLD",
            t2c={"P": BLUE},
        ).move_to([3.55, -1.04, 0])
        minimum_line = MathTex("p", "=", "BC'", font_size=43, color=INK).move_to(
            [3.55, -1.82, 0]
        )
        minimum_line[0].set_color(POINT)

        # Beat 07 straighten_path: show the lower bound and then attain it exactly.
        self.next_slide()
        self.add(generic_ghost)
        self.play(
            FadeOut(path_caption),
            FadeOut(path_equation),
            FadeOut(rotation_arrow),
            Create(direct_line),
            Write(lower_bound),
            run_time=0.90,
        )
        self.play(FadeIn(equality_note), run_time=0.45)
        self.play(
            Transform(path_bp, Line(point_b, point_p_equal, color=POINT, stroke_width=6.0)),
            Transform(path_pp, Line(point_p_equal, point_p_prime_equal, color=PURPLE, stroke_width=6.0)),
            Transform(path_pc_prime, Line(point_p_prime_equal, point_c_prime, color=REGION, stroke_width=6.0)),
            p_dot.animate.move_to(point_p_equal),
            rotating_copy[8].animate.move_to(point_p_prime_equal),
            run_time=1.65,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(attainable_note), run_time=0.55)
        self.play(Write(minimum_line), run_time=0.55)

        point_d = model_point(-math.sqrt(3), 3)
        measure_c_prime_dot = Dot(point_c_prime, radius=0.075, color=PURPLE).set_z_index(7)
        measure_c_prime_label = label("C′", 22, PURPLE, "BOLD").next_to(
            measure_c_prime_dot, UP + LEFT * 0.15, buff=0.10
        )
        ac_prime = Line(point_a, point_c_prime, color=PURPLE, stroke_width=3.8)
        extended_bd = Line(point_b, point_d, color=MUTED, stroke_width=3.0)
        cd_line = Line(point_c_prime, point_d, color=BLUE, stroke_width=4.0)
        d_dot = Dot(point_d, radius=0.065, color=WHITE)
        d_label = label("D", 21, INK, "BOLD").next_to(d_dot, UP + RIGHT * 0.20, buff=0.09)
        right_mark_d = RightAngle(
            Line(point_d, point_a),
            Line(point_d, point_c_prime),
            length=0.20,
            color=POINT,
            stroke_width=2.4,
        )
        arc_60 = Arc(
            radius=0.36,
            start_angle=-2 * PI / 3,
            angle=PI / 3,
            arc_center=point_a,
            color=REGION,
            stroke_width=3.2,
        )
        arc_90 = Arc(
            radius=0.53,
            start_angle=-2 * PI / 3,
            angle=-PI / 2,
            arc_center=point_a,
            color=PURPLE,
            stroke_width=3.2,
        )
        arc_150 = Arc(
            radius=0.68,
            start_angle=5 * PI / 6,
            angle=5 * PI / 6,
            arc_center=point_a,
            color=POINT,
            stroke_width=3.8,
        )
        arc_30 = Arc(
            radius=0.39,
            start_angle=2 * PI / 3,
            angle=PI / 6,
            arc_center=point_a,
            color=BLUE,
            stroke_width=3.2,
        )
        angle_30_label = MathTex(r"30^\circ", font_size=22, color=BLUE).move_to(
            point_a + np.array([-0.50, 0.57, 0])
        )
        angle_facts = VGroup(
            MathTex(r"\angle BAC", "=", r"60^\circ", font_size=30, color=INK),
            MathTex(r"\angle CAC'", "=", r"90^\circ", font_size=30, color=INK),
            MathTex(r"\angle BAC'", "=", r"150^\circ", font_size=33, color=INK),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([3.48, 2.02, 0])
        angle_facts[0][2].set_color(REGION)
        angle_facts[1][2].set_color(PURPLE)
        angle_facts[2][2].set_color(POINT)
        special_triangle_facts = VGroup(
            MathTex("AC'", "=", "4", font_size=31, color=INK),
            MathTex("C'D", "=", "2", font_size=31, color=INK),
            MathTex("AD", "=", r"2\sqrt3", font_size=31, color=INK),
            MathTex("BD", "=", r"4+2\sqrt3", font_size=33, color=INK),
        ).arrange(DOWN, buff=0.19, aligned_edge=LEFT).move_to([3.48, -0.35, 0])
        special_triangle_facts[0][0].set_color(PURPLE)
        special_triangle_facts[1][0].set_color(BLUE)
        special_triangle_facts[1][2].set_color(BLUE)
        special_triangle_facts[2][0].set_color(REGION)
        special_triangle_facts[3][0].set_color(POINT)
        point_order = label(
            "直線上的順序：B ─ A ─ D",
            23,
            MUTED,
            "MEDIUM",
            t2c={"B ─ A ─ D": POINT},
        ).move_to([3.48, -1.78, 0])

        # Beat 08 measure_bc_prime: measure the straight endpoint distance geometrically.
        self.next_slide()
        self.play(
            FadeOut(objective),
            FadeOut(compact_relation),
            FadeOut(lower_bound),
            FadeOut(equality_note),
            FadeOut(attainable_note),
            FadeOut(minimum_line),
            FadeOut(generic_ghost),
            FadeOut(path_bp),
            FadeOut(path_pp),
            FadeOut(path_pc_prime),
            FadeOut(pp_line),
            FadeOut(right_triangle_fill),
            FadeOut(rotation_angle_label),
            FadeOut(prime_p_label),
            FadeOut(prime_c_label),
            FadeOut(prime_b_label),
            FadeOut(rotating_copy),
            FadeOut(p_dot),
            FadeOut(p_label),
            FadeOut(ap_line),
            FadeOut(bp_line),
            FadeOut(cp_line),
            triangle_edges.animate.set_opacity(1.0),
            congruence_ticks.animate.set_opacity(1.0),
            run_time=0.85,
        )
        self.play(FadeIn(measure_c_prime_dot), FadeIn(measure_c_prime_label), Create(ac_prime), run_time=0.70)
        self.play(Create(arc_60), FadeIn(angle_facts[0]), run_time=0.55)
        self.play(Create(arc_90), FadeIn(angle_facts[1]), run_time=0.55)
        self.play(
            FadeOut(arc_60),
            FadeOut(arc_90),
            Create(arc_150),
            FadeIn(angle_facts[2]),
            run_time=0.65,
        )
        self.play(Create(extended_bd), FadeIn(d_dot), FadeIn(d_label), run_time=0.65)
        self.play(Create(cd_line), Create(right_mark_d), run_time=0.65)
        self.play(Create(arc_30), FadeIn(angle_30_label), run_time=0.50)
        self.play(
            LaggedStart(*(FadeIn(item) for item in special_triangle_facts), lag_ratio=0.16),
            FadeIn(point_order),
            run_time=1.15,
        )

        bc_square = MathTex(
            "BC'^2",
            "=",
            "BD^2",
            "+",
            "C'D^2",
            font_size=34,
            color=INK,
        )
        bc_substitution = MathTex(
            "=",
            r"(4+2\sqrt3)^2",
            "+",
            "2^2",
            font_size=34,
            color=INK,
        )
        bc_expanded = MathTex("=", r"32+16\sqrt3", font_size=36, color=INK)
        candidate_square = MathTex(
            r"(2\sqrt6+2\sqrt2)^2",
            "=",
            r"24+8+16\sqrt3",
            font_size=31,
            color=INK,
        )
        candidate_match = MathTex("=", r"32+16\sqrt3", font_size=33, color=INK)
        minimum_result = MathTex(
            "p",
            "=",
            "BC'",
            "=",
            r"2\sqrt6+2\sqrt2",
            font_size=39,
            color=INK,
        )
        minimum_result[0].set_color(POINT)
        minimum_result[4].set_color(POINT)
        minimum_derivation = VGroup(
            bc_square,
            bc_substitution,
            bc_expanded,
            candidate_square,
            candidate_match,
            minimum_result,
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to([3.62, 0.20, 0])
        positive_note = label("BC′ 是長度，所以取正值", 22, MUTED, "MEDIUM").next_to(
            minimum_result, DOWN, buff=0.18
        )

        # Beat 09 compute_minimum: square, recognize the radical, and take the positive root.
        self.next_slide()
        self.play(
            FadeOut(angle_facts),
            FadeOut(special_triangle_facts),
            FadeOut(point_order),
            TransformFromCopy(VGroup(extended_bd, cd_line), bc_square),
            run_time=0.90,
        )
        self.play(Write(bc_substitution), run_time=0.70)
        self.play(Write(bc_expanded), run_time=0.60)
        self.play(Write(candidate_square), run_time=0.75)
        self.play(Write(candidate_match), run_time=0.55)
        self.play(Write(minimum_result), FadeIn(positive_note), run_time=0.75)

        equality_p = Dot(point_p_equal, radius=0.085, color=BLUE).set_z_index(8)
        equality_p_label = label("P", 22, BLUE, "BOLD").next_to(
            equality_p, RIGHT, buff=0.10
        )
        equality_p_prime = Dot(point_p_prime_equal, radius=0.085, color=PURPLE).set_z_index(8)
        equality_p_prime_label = label("P′", 22, PURPLE, "BOLD").next_to(
            equality_p_prime, UP + LEFT * 0.20, buff=0.10
        )
        ell_line = direct_line.copy().set_color(INK).set_stroke(width=4.0)
        ell_label = MathTex(r"\ell=BC'", font_size=28, color=INK).move_to(
            [-4.15, 0.88, 0]
        )
        equality_path = VGroup(
            Line(point_b, point_p_equal, color=POINT, stroke_width=6.0),
            Line(point_p_equal, point_p_prime_equal, color=PURPLE, stroke_width=6.0),
            Line(point_p_prime_equal, point_c_prime, color=REGION, stroke_width=6.0),
        ).set_z_index(5)
        inverse_line = ell_line.copy().set_color(PURPLE).set_stroke(width=3.2)
        constraints = VGroup(
            MathTex("P", r"\in", r"\ell", font_size=34, color=INK),
            MathTex("P'=R(P)", r"\in", r"\ell", font_size=34, color=INK),
            MathTex(r"\Longrightarrow", "P", r"\in", r"R^{-1}(\ell)", font_size=34, color=INK),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to([3.50, 0.80, 0])
        constraints[0][0].set_color(BLUE)
        constraints[1][0].set_color(PURPLE)
        constraints[2][1].set_color(BLUE)
        constraints[2][3].set_color(PURPLE)
        intersection_ring = SurroundingRectangle(
            equality_p,
            color=BLUE,
            buff=0.13,
            corner_radius=0.15,
            stroke_width=3,
        )
        uniqueness_note = label(
            "兩條直線的唯一交點，才是等號時的 P",
            24,
            INK,
            "BOLD",
            t2c={"唯一交點": POINT, "P": BLUE},
        ).move_to([3.50, -1.00, 0])
        symmetry_axis = DashedLine(point_a, point_e, color=BLUE, stroke_width=2.8, dash_length=0.13)
        axis_note = label("交點恰好落在對稱軸上", 23, BLUE, "MEDIUM").move_to(
            [3.50, -1.67, 0]
        )

        # Beat 10 pin_down_p: inverse-rotate the equality line and take its unique intersection.
        self.next_slide()
        self.play(
            FadeOut(VGroup(*minimum_derivation, positive_note)),
            FadeOut(ac_prime),
            FadeOut(extended_bd),
            FadeOut(cd_line),
            FadeOut(d_dot),
            FadeOut(d_label),
            FadeOut(right_mark_d),
            FadeOut(arc_150),
            FadeOut(arc_30),
            FadeOut(angle_30_label),
            FadeIn(ell_line),
            FadeIn(ell_label),
            FadeIn(equality_path),
            FadeIn(equality_p),
            FadeIn(equality_p_label),
            FadeIn(equality_p_prime),
            FadeIn(equality_p_prime_label),
            run_time=0.90,
        )
        self.play(FadeIn(constraints[0]), FadeIn(constraints[1]), run_time=0.65)
        self.add(inverse_line)
        self.play(
            Rotate(inverse_line, angle=PI / 2, about_point=point_a),
            run_time=1.50,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(constraints[2]), run_time=0.55)
        self.play(Create(intersection_ring), FadeIn(uniqueness_note), run_time=0.65)
        self.play(Create(symmetry_axis), FadeIn(axis_note), run_time=0.65)

        ap_equal = Line(point_a, point_p_equal, color=BLUE, stroke_width=4.6).set_z_index(4)
        ap_prime_equal = Line(point_a, point_p_prime_equal, color=PURPLE, stroke_width=4.2).set_z_index(4)
        pp_equal = Line(point_p_equal, point_p_prime_equal, color=PURPLE, stroke_width=5.0).set_z_index(5)
        bp_equal = Line(point_b, point_p_equal, color=POINT, stroke_width=5.0).set_z_index(5)
        base_angle_45 = Arc(
            radius=0.31,
            start_angle=PI / 2,
            angle=PI / 4,
            arc_center=point_p_equal,
            color=PURPLE,
            stroke_width=3.5,
        )
        angle_apb = Arc(
            radius=0.48,
            start_angle=-PI / 4,
            angle=3 * PI / 4,
            arc_center=point_p_equal,
            color=POINT,
            stroke_width=3.5,
        )
        angle_45_label = MathTex(r"45^\circ", font_size=20, color=PURPLE).move_to(
            point_p_equal + np.array([-0.55, 0.64, 0])
        )
        angle_135_label = MathTex(r"135^\circ", font_size=20, color=POINT).move_to(
            point_p_equal + np.array([0.69, 0.15, 0])
        )
        point_e_dot = Dot(point_e, radius=0.065, color=WHITE)
        point_e_label = label("E", 21, INK, "BOLD").next_to(point_e_dot, DOWN, buff=0.10)
        half_base_ticks = VGroup(
            self.tick(point_b, point_e, color=POINT),
            self.tick(point_e, point_c, color=POINT),
        )
        angle_receipt = VGroup(
            MathTex(r"\angle APP'", "=", r"45^\circ", font_size=34, color=INK),
            MathTex(r"\angle APB", "=", r"180^\circ-45^\circ", "=", r"135^\circ", font_size=32, color=INK),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to([3.50, 0.60, 0])
        angle_receipt[0][2].set_color(PURPLE)
        angle_receipt[1][4].set_color(POINT)
        midpoint_note = label(
            "A、P、E 共線；E 是 BC 的中點",
            24,
            INK,
            "BOLD",
            t2c={"P": BLUE, "E": POINT},
        ).move_to([3.50, -0.82, 0])

        # Beat 11 read_equality_angles: read 45 degrees from the rotated triangle.
        self.next_slide()
        self.play(
            FadeOut(constraints),
            FadeOut(uniqueness_note),
            FadeOut(axis_note),
            FadeOut(intersection_ring),
            inverse_line.animate.set_opacity(0.18),
            ell_line.animate.set_opacity(0.24),
            equality_path.animate.set_opacity(0.24),
            run_time=0.65,
        )
        self.play(Create(ap_equal), Create(ap_prime_equal), Create(pp_equal), run_time=0.75)
        self.play(Create(base_angle_45), FadeIn(angle_45_label), FadeIn(angle_receipt[0]), run_time=0.65)
        self.play(Create(bp_equal), Create(angle_apb), FadeIn(angle_135_label), FadeIn(angle_receipt[1]), run_time=0.75)
        self.play(
            FadeIn(point_e_dot),
            FadeIn(point_e_label),
            Create(half_base_ticks),
            FadeIn(midpoint_note),
            run_time=0.70,
        )

        pe_line = Line(point_p_equal, point_e, color=REGION, stroke_width=5.0).set_z_index(5)
        be_line = Line(point_b, point_e, color=POINT, stroke_width=5.0).set_z_index(5)
        right_mark_e = RightAngle(
            Line(point_e, point_b),
            Line(point_e, point_p_equal),
            length=0.20,
            color=WHITE,
            stroke_width=2.4,
        )
        angle_bpe = Arc(
            radius=0.32,
            start_angle=-PI / 2,
            angle=PI / 4,
            arc_center=point_p_equal,
            color=REGION,
            stroke_width=3.5,
        )
        bpe_45_label = MathTex(r"45^\circ", font_size=20, color=REGION).move_to(
            point_p_equal + np.array([0.48, -0.42, 0])
        )
        ap_calculation = VGroup(
            MathTex("BE", "=", r"\frac{BC}{2}", "=", "2", font_size=31, color=INK),
            MathTex(r"\angle BPE=45^\circ", ",", r"\angle BEP=90^\circ", font_size=29, color=INK),
            MathTex(r"\Longrightarrow", "PE", "=", "BE", "=", "2", font_size=31, color=INK),
            MathTex("AE^2", "=", "AB^2", "-", "BE^2", "=", "4^2-2^2", font_size=30, color=INK),
            MathTex("AE", "=", r"2\sqrt3", font_size=33, color=INK),
            MathTex("q", "=", "AP", "=", "AE-PE", "=", r"2\sqrt3-2", font_size=36, color=INK),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([3.55, 0.15, 0])
        ap_calculation[0][0].set_color(POINT)
        ap_calculation[0][4].set_color(POINT)
        ap_calculation[2][1].set_color(REGION)
        ap_calculation[2][5].set_color(REGION)
        ap_calculation[4][0].set_color(BLUE)
        ap_calculation[4][2].set_color(BLUE)
        ap_calculation[5][0].set_color(BLUE)
        ap_calculation[5][2].set_color(BLUE)
        ap_calculation[5][6].set_color(BLUE)

        # Beat 12 compute_ap: use the visible 45-degree triangle and equilateral altitude.
        self.next_slide()
        self.play(
            FadeOut(angle_receipt),
            FadeOut(midpoint_note),
            FadeOut(angle_apb),
            FadeOut(angle_135_label),
            FadeOut(base_angle_45),
            FadeOut(angle_45_label),
            FadeOut(ap_prime_equal),
            FadeOut(pp_equal),
            run_time=0.60,
        )
        self.play(Create(pe_line), Create(be_line), Create(right_mark_e), run_time=0.65)
        self.play(Create(angle_bpe), FadeIn(bpe_45_label), run_time=0.50)
        self.play(FadeIn(ap_calculation[0]), run_time=0.55)
        self.play(FadeIn(ap_calculation[1]), run_time=0.55)
        self.play(FadeIn(ap_calculation[2]), run_time=0.55)
        self.play(FadeIn(ap_calculation[3]), run_time=0.60)
        self.play(FadeIn(ap_calculation[4]), run_time=0.50)
        self.play(FadeIn(ap_calculation[5]), run_time=0.65)

        recap = VGroup(
            MathTex(r"\sqrt2 AP", "=", "PP'", font_size=34, color=INK),
            MathTex("BP+PP'+P'C'", r"\ge", "BC'", font_size=34, color=INK),
            MathTex("P", "=", r"\ell\cap R^{-1}(\ell)", font_size=34, color=INK),
        ).arrange(DOWN, buff=0.34, aligned_edge=LEFT).move_to([3.48, 0.75, 0])
        recap[0][0].set_color(BLUE)
        recap[0][2].set_color(PURPLE)
        recap[1][0].set_color(MUTED)
        recap[1][2].set_color(POINT)
        recap[2][0].set_color(BLUE)
        recap[2][2].set_color(PURPLE)
        final_answer = MathTex(
            "(p,q)",
            "=",
            r"\left(2\sqrt6+2\sqrt2,\;2\sqrt3-2\right)",
            font_size=39,
            color=INK,
        ).move_to([3.45, -1.78, 0])
        final_answer[0].set_color(POINT)
        final_answer[2].set_color(BLUE)
        final_box = SurroundingRectangle(
            final_answer,
            color=POINT,
            buff=0.20,
            corner_radius=0.08,
            stroke_width=2.5,
        )

        # Beat 13 consolidate: reconnect rotation, straightening, equality, and both values.
        self.next_slide()
        self.play(
            FadeOut(ap_calculation),
            FadeOut(right_mark_e),
            FadeOut(angle_bpe),
            FadeOut(bpe_45_label),
            FadeOut(pe_line),
            FadeOut(be_line),
            inverse_line.animate.set_opacity(0.38),
            ell_line.animate.set_opacity(0.58),
            equality_path.animate.set_opacity(0.65),
            run_time=0.70,
        )
        self.play(
            LaggedStart(*(FadeIn(item, shift=UP * 0.07) for item in recap), lag_ratio=0.22),
            run_time=1.15,
        )
        self.play(Write(final_answer), Create(final_box), run_time=0.90)
        self.play(Circumscribe(equality_p, color=BLUE), run_time=0.70)
        self.wait(0.35)
