"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q10."""

from __future__ import annotations

from fractions import Fraction

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
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    always_redraw,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


A_COORD = (Fraction(0), Fraction(8))
B_COORD = (Fraction(16), Fraction(8))
C_COORD = (Fraction(16), Fraction(0))
D_COORD = (Fraction(0), Fraction(0))
B_PRIME_COORD = (Fraction(48, 5), Fraction(-24, 5))
Q_COORD = (Fraction(48, 5), Fraction(8))
P_COORD = (Fraction(48, 5), Fraction(16, 5))


def squared_distance(
    first: tuple[Fraction, Fraction], second: tuple[Fraction, Fraction]
) -> Fraction:
    """Return an exact squared Euclidean distance."""
    return (first[0] - second[0]) ** 2 + (first[1] - second[1]) ** 2


if B_PRIME_COORD != (
    B_COORD[0] - Fraction(2 * 16, 5),
    B_COORD[1] - Fraction(4 * 16, 5),
):
    raise ValueError("reflection of B across x+2y=16 is incorrect")
if Q_COORD[1] != 8 or not (0 < Q_COORD[0] < 16):
    raise ValueError("perpendicular foot is not on segment AB")
if P_COORD[0] + 2 * P_COORD[1] != 16:
    raise ValueError("candidate P is not on diagonal AC")
if not (Q_COORD[1] > P_COORD[1] > B_PRIME_COORD[1]):
    raise ValueError("Q, P, B' do not occur in the required order")
if squared_distance(P_COORD, B_COORD) != squared_distance(P_COORD, B_PRIME_COORD):
    raise ValueError("reflection identity PB=PB' failed")
if squared_distance(P_COORD, B_COORD) != 64:
    raise ValueError("unexpected reflected leg length")
if Q_COORD[1] - P_COORD[1] + 8 != Fraction(64, 5):
    raise ValueError("unexpected minimum path length")


class CarloTcfs113MathQ10(CarloSlide):
    """Turn a reflected broken path into an attainable perpendicular distance."""

    lesson_id = "carlo.tcfs_113_math_gifted.q10"

    DRAWING_ORIGIN = np.array([-6.20, -0.48, 0.0])
    DRAWING_SCALE = 0.39

    @classmethod
    def to_scene(cls, x_coord: float, y_coord: float) -> np.ndarray:
        """Map problem coordinates into the stable left drawing area."""
        return cls.DRAWING_ORIGIN + cls.DRAWING_SCALE * np.array(
            [x_coord, y_coord, 0.0]
        )

    @classmethod
    def diagonal_point(cls, parameter: float) -> np.ndarray:
        """Return A + parameter(C-A) in scene coordinates."""
        return cls.to_scene(16 * parameter, 8 * (1 - parameter))

    @classmethod
    def top_point(cls, parameter: float) -> np.ndarray:
        """Return A + parameter(B-A) in scene coordinates."""
        return cls.to_scene(16 * parameter, 8)

    @staticmethod
    def segment_ticks(
        start: np.ndarray,
        end: np.ndarray,
        *,
        color: str,
        count: int = 1,
        width: float = 0.18,
        spacing: float = 0.12,
    ) -> VGroup:
        """Mark equal segments with one or two short perpendicular ticks."""
        direction = end - start
        direction = direction / np.linalg.norm(direction)
        normal = np.array([-direction[1], direction[0], 0.0])
        midpoint = (start + end) / 2
        offsets = [0.0] if count == 1 else [-spacing / 2, spacing / 2]
        return VGroup(
            *(
                Line(
                    midpoint + offset * direction - width * normal / 2,
                    midpoint + offset * direction + width * normal / 2,
                    color=color,
                    stroke_width=3.2,
                ).set_z_index(9)
                for offset in offsets
            )
        )

    @staticmethod
    def right_angle_mark(
        vertex: np.ndarray,
        first_direction: np.ndarray,
        second_direction: np.ndarray,
        *,
        color: str,
        size: float = 0.22,
    ) -> VGroup:
        """Draw a small square between two perpendicular ray directions."""
        first = first_direction / np.linalg.norm(first_direction)
        second = second_direction / np.linalg.norm(second_direction)
        first_point = vertex + size * first
        corner = vertex + size * (first + second)
        second_point = vertex + size * second
        return VGroup(
            Line(first_point, corner, color=color, stroke_width=3),
            Line(corner, second_point, color=color, stroke_width=3),
        ).set_z_index(9)

    @staticmethod
    def transition_title(scene: "CarloTcfs113MathQ10", old, new) -> None:
        """Swap CJK titles without morphing individual glyphs."""
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.58)

    def construct(self) -> None:
        a_point = self.to_scene(0, 8)
        b_point = self.to_scene(16, 8)
        c_point = self.to_scene(16, 0)
        d_point = self.to_scene(0, 0)
        b_prime = self.to_scene(float(B_PRIME_COORD[0]), float(B_PRIME_COORD[1]))
        h_point = self.to_scene(64 / 5, 8 / 5)

        heading = label("第 10 題｜把折線鏡射成最短路徑", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 10 頁｜影片 X6Cabjm94eY 01:26-05:50",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.80, -3.50, 0], [0.80, 3.40, 0], color=HAIRLINE, stroke_width=1.5)

        rectangle = Polygon(
            a_point,
            b_point,
            c_point,
            d_point,
            color=INK,
            stroke_width=3.2,
            fill_opacity=0,
        ).set_z_index(2)
        diagonal = Line(a_point, c_point, color=BLUE, stroke_width=4.6).set_z_index(3)
        quiet_dots = VGroup(
            Dot(a_point, radius=0.065, color=INK),
            Dot(c_point, radius=0.065, color=INK),
            Dot(d_point, radius=0.065, color=INK),
        ).set_z_index(7)
        b_dot = Dot(b_point, radius=0.085, color=CORAL).set_z_index(8)
        vertex_labels = VGroup(
            MathTex("A", font_size=29, color=INK).next_to(a_point, UP + LEFT, buff=0.09),
            MathTex("B", font_size=29, color=CORAL).next_to(b_point, UP + RIGHT, buff=0.09),
            MathTex("C", font_size=29, color=INK).next_to(c_point, DOWN + RIGHT, buff=0.09),
            MathTex("D", font_size=29, color=INK).next_to(d_point, DOWN + LEFT, buff=0.09),
        ).set_z_index(9)
        top_length = MathTex("16", font_size=30, color=MUTED).next_to(
            Line(a_point, b_point), UP, buff=0.22
        )
        side_length = MathTex("8", font_size=30, color=MUTED).next_to(
            Line(b_point, c_point), RIGHT, buff=0.18
        )
        diagonal_label = MathTex("AC", font_size=26, color=BLUE).move_to(
            self.to_scene(2.2, 6.2)
        )

        p_tracker = ValueTracker(0.55)
        q_tracker = ValueTracker(0.35)
        p_dot = always_redraw(
            lambda: Dot(
                self.diagonal_point(p_tracker.get_value()), radius=0.095, color=POINT
            ).set_z_index(10)
        )
        p_label = always_redraw(
            lambda: MathTex("P", font_size=30, color=POINT)
            .next_to(
                self.diagonal_point(p_tracker.get_value()), DOWN + LEFT, buff=0.12
            )
            .set_z_index(11)
        )
        q_dot = always_redraw(
            lambda: Dot(
                self.top_point(q_tracker.get_value()), radius=0.095, color=CORAL
            ).set_z_index(10)
        )
        q_label = always_redraw(
            lambda: MathTex("Q", font_size=30, color=CORAL)
            .next_to(self.top_point(q_tracker.get_value()), UP, buff=0.12)
            .set_z_index(11)
        )
        qp_leg = always_redraw(
            lambda: Line(
                self.top_point(q_tracker.get_value()),
                self.diagonal_point(p_tracker.get_value()),
                color=PURPLE,
                stroke_width=5,
            ).set_z_index(5)
        )
        pb_leg = always_redraw(
            lambda: Line(
                self.diagonal_point(p_tracker.get_value()),
                b_point,
                color=CORAL,
                stroke_width=5,
            ).set_z_index(5)
        )

        # Beat 01: establish the rectangle and the original broken path.
        self.begin_beat("meet_broken_path")
        beat_title = label("先看清楚要縮短的折線", 33, INK, "BOLD")
        beat_title.move_to([4.25, 3.02, 0])
        objective = MathTex(r"PQ+PB\longrightarrow\min", font_size=48, color=INK)
        objective[0][0:2].set_color(PURPLE)
        route_note = label("Q 到 P，再走到 B", 27, MUTED, "MEDIUM")
        freedom_note = label("P 在 AC 上；Q 在 AB 上", 26, INK, "BOLD")
        opening_panel = VGroup(objective, route_note, freedom_note).arrange(DOWN, buff=0.48)
        opening_panel.move_to([4.25, -0.02, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(beat_title), Create(rectangle), run_time=0.85)
        self.play(
            FadeIn(quiet_dots),
            GrowFromCenter(b_dot),
            FadeIn(vertex_labels),
            FadeIn(top_length),
            FadeIn(side_length),
            run_time=0.65,
        )
        self.play(Create(diagonal), FadeIn(diagonal_label), run_time=0.8)
        self.play(
            GrowFromCenter(p_dot),
            GrowFromCenter(q_dot),
            FadeIn(p_label),
            FadeIn(q_label),
            Create(qp_leg),
            Create(pb_leg),
            run_time=0.9,
        )

        self.next_beat("state_path_objective")
        self.play(LaggedStart(*(FadeIn(item) for item in opening_panel), lag_ratio=0.16), run_time=0.9)
        self.wait(0.4)

        # Beat 02: move P and Q separately so both freedoms are felt.
        self.next_beat("explore_two_movers")
        next_title = label("兩個點都能動，折線一直改變", 32, INK, "BOLD")
        next_title.move_to(beat_title)
        moving_p = VGroup(
            label("先只移動 P", 27, POINT, "BOLD"),
            label("兩段長度同時改變", 24, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.26)
        moving_q = VGroup(
            label("再移動 Q", 27, CORAL, "BOLD"),
            label("直接逐點嘗試，何時才該停？", 24, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.26)
        exploration_panel = VGroup(moving_p, moving_q).arrange(DOWN, buff=0.72)
        exploration_panel.move_to([4.25, -0.04, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            Succession(FadeOut(opening_panel), FadeIn(moving_p)),
            run_time=0.65,
        )
        self.play(p_tracker.animate.set_value(0.24), run_time=1.0)
        self.play(p_tracker.animate.set_value(0.76), run_time=1.15)
        self.play(p_tracker.animate.set_value(0.47), run_time=0.9)

        self.next_beat("move_q_along_top_edge")
        self.play(FadeIn(moving_q), run_time=0.45)
        self.play(q_tracker.animate.set_value(0.79), run_time=1.0)
        self.play(q_tracker.animate.set_value(0.16), run_time=1.15)
        self.play(
            p_tracker.animate.set_value(0.55),
            q_tracker.animate.set_value(0.35),
            run_time=1.0,
        )
        self.wait(0.4)

        # Beat 03: construct the reflection of B across AC.
        self.next_beat("reflect_b_across_diagonal")
        next_title = label("把 B 對 AC 鏡射到 B'", 33, INK, "BOLD")
        next_title.move_to(beat_title)
        reflection_line = DashedLine(
            b_point,
            b_prime,
            color=REGION,
            dash_length=0.12,
            stroke_width=2.8,
        ).set_z_index(4)
        h_dot = Dot(h_point, radius=0.07, color=REGION).set_z_index(9)
        h_label = MathTex("H", font_size=25, color=REGION).next_to(
            h_point, DOWN + RIGHT, buff=0.10
        ).set_z_index(10)
        b_prime_dot = Dot(b_prime, radius=0.095, color=REGION).set_z_index(10)
        b_prime_label = MathTex(r"B^\prime", font_size=30, color=REGION).next_to(
            b_prime, DOWN + RIGHT, buff=0.10
        ).set_z_index(11)
        reflection_right_angle = self.right_angle_mark(
            h_point,
            a_point - h_point,
            b_point - h_point,
            color=REGION,
        )
        bh_tick = self.segment_ticks(b_point, h_point, color=REGION)
        hb_prime_tick = self.segment_ticks(h_point, b_prime, color=REGION)
        reflection_name = VGroup(
            label("鏡面是 AC", 27, BLUE, "BOLD"),
            MathTex(r"BB^\prime\perp AC", font_size=40, color=INK),
            MathTex(r"BH=HB^\prime", font_size=40, color=REGION),
        ).arrange(DOWN, buff=0.38)
        reflection_name.move_to([4.25, -0.10, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(exploration_panel), Create(reflection_line), run_time=0.65)
        self.play(
            TransformFromCopy(b_dot, b_prime_dot),
            FadeIn(b_prime_label),
            GrowFromCenter(h_dot),
            FadeIn(h_label),
            run_time=0.9,
        )
        self.play(Create(reflection_right_angle), FadeIn(bh_tick), FadeIn(hb_prime_tick), run_time=0.65)
        self.play(LaggedStart(*(FadeIn(item) for item in reflection_name), lag_ratio=0.18), run_time=0.9)
        self.wait(0.4)

        # Beat 04: use P on the mirror to replace PB by PB'.
        self.next_beat("replace_equal_leg")
        next_title = label("鏡面上的 P 到 B、B' 一樣遠", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        pb_prime_leg = always_redraw(
            lambda: Line(
                self.diagonal_point(p_tracker.get_value()),
                b_prime,
                color=REGION,
                stroke_width=5,
            ).set_z_index(5)
        )
        current_p = self.diagonal_point(p_tracker.get_value())
        pb_equal_tick = self.segment_ticks(current_p, b_point, color=CORAL, count=2)
        pb_prime_equal_tick = self.segment_ticks(current_p, b_prime, color=REGION, count=2)
        mirror_identity = MathTex(r"P\in AC\quad\Longrightarrow\quad PB=PB^\prime", font_size=38, color=INK)
        mirror_identity[0][0].set_color(POINT)
        path_rewrite = MathTex(r"PQ+PB=PQ+PB^\prime", font_size=44, color=INK)
        rewrite_note = label("總長沒有改變", 27, REGION, "BOLD")
        rewrite_panel = VGroup(mirror_identity, path_rewrite, rewrite_note).arrange(DOWN, buff=0.46)
        rewrite_panel.move_to([4.25, -0.05, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(reflection_name), TransformFromCopy(pb_leg, pb_prime_leg), run_time=0.8)
        self.play(FadeIn(pb_equal_tick), FadeIn(pb_prime_equal_tick), FadeIn(mirror_identity), run_time=0.8)
        self.play(FadeIn(path_rewrite), FadeIn(rewrite_note), run_time=0.8)
        self.play(FadeOut(pb_leg), FadeOut(pb_equal_tick), FadeOut(pb_prime_equal_tick), run_time=0.5)
        self.wait(0.4)

        # Beat 05: invoke the triangle inequality, then move P into equality.
        self.next_beat("straighten_reflected_path")
        next_title = label("把鏡射後的折線拉直", 33, INK, "BOLD")
        next_title.move_to(beat_title)
        direct_qb_prime = always_redraw(
            lambda: Line(
                self.top_point(q_tracker.get_value()),
                b_prime,
                color=BLUE,
                stroke_width=3.4,
            ).set_z_index(4)
        )
        triangle_bound = MathTex(r"PQ+PB^\prime\ge QB^\prime", font_size=46, color=INK)
        equality_condition = VGroup(
            MathTex(r"Q,P,B^\prime", font_size=38, color=REGION),
            label("共線", 27, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.22)
        equality_equation = MathTex(r"PQ+PB^\prime=QB^\prime", font_size=43, color=REGION)
        straight_panel = VGroup(triangle_bound, equality_condition, equality_equation).arrange(
            DOWN, buff=0.48
        )
        straight_panel.move_to([4.25, -0.02, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(rewrite_panel), Create(direct_qb_prime), run_time=0.75)
        self.play(FadeIn(triangle_bound), run_time=0.75)
        self.play(p_tracker.animate.set_value(56 / 135), run_time=1.25)

        self.next_beat("attain_straight_path")
        self.play(FadeIn(equality_condition), run_time=0.55)
        self.play(FadeIn(equality_equation), Circumscribe(equality_equation, color=REGION), run_time=0.85)
        self.wait(0.4)

        # Beat 06: with P chosen to straighten, only Q remains free.
        self.next_beat("slide_q_along_top_edge")
        next_title = label("拉直之後，只讓 Q 沿 AB 滑動", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        one_freedom = VGroup(
            MathTex(r"Q\in AB", font_size=43, color=CORAL),
            label("每個 Q 都連向固定的 B'", 27, INK, "BOLD"),
            label("哪一條 QB' 最短？", 28, BLUE, "BOLD"),
        ).arrange(DOWN, buff=0.48)
        one_freedom.move_to([4.25, -0.04, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            Succession(FadeOut(straight_panel), FadeIn(one_freedom)),
            FadeOut(qp_leg),
            FadeOut(pb_prime_leg),
            FadeOut(p_dot),
            FadeOut(p_label),
            FadeOut(reflection_right_angle),
            FadeOut(bh_tick),
            FadeOut(hb_prime_tick),
            FadeOut(h_dot),
            FadeOut(h_label),
            FadeOut(reflection_line),
            run_time=0.85,
        )
        self.play(q_tracker.animate.set_value(0.82), run_time=1.05)
        self.play(q_tracker.animate.set_value(0.18), run_time=1.25)
        self.play(q_tracker.animate.set_value(0.60), run_time=1.1)
        self.wait(0.4)

        # Beat 07: identify the perpendicular foot before introducing coordinates.
        self.next_beat("settle_perpendicular_foot")
        next_title = label("固定點到直線：垂線最短", 33, INK, "BOLD")
        next_title.move_to(beat_title)
        q_final_scene = self.top_point(0.60)
        perpendicular_mark = self.right_angle_mark(
            q_final_scene,
            a_point - q_final_scene,
            b_prime - q_final_scene,
            color=BLUE,
            size=0.24,
        )
        perpendicular_rule = MathTex(r"QB^\prime\perp AB", font_size=45, color=BLUE)
        foot_note = label("垂足落在 A、B 之間", 28, REGION, "BOLD")
        shortest_note = label("所以最小值就是這條垂直距離", 27, INK, "BOLD")
        perpendicular_panel = VGroup(perpendicular_rule, foot_note, shortest_note).arrange(
            DOWN, buff=0.48
        )
        perpendicular_panel.move_to([4.25, -0.04, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(one_freedom), Create(perpendicular_mark), run_time=0.65)
        self.play(FadeIn(perpendicular_rule), run_time=0.6)
        self.play(Indicate(q_dot, color=REGION, scale_factor=1.55), FadeIn(foot_note), run_time=0.7)
        self.play(FadeIn(shortest_note), Circumscribe(direct_qb_prime, color=BLUE), run_time=0.8)
        self.wait(0.4)

        # Beat 08: add coordinates only after the geometry is settled.
        self.next_beat("introduce_coordinates")
        next_title = label("現在才放座標，把長度算準", 32, INK, "BOLD")
        next_title.move_to(beat_title)
        coordinate_labels = VGroup(
            MathTex("A=(0,8)", font_size=24, color=INK).next_to(a_point, LEFT + UP, buff=0.09),
            MathTex("B=(16,8)", font_size=24, color=CORAL).next_to(b_point, LEFT + UP, buff=0.09),
            MathTex("C=(16,0)", font_size=24, color=INK).next_to(c_point, LEFT + DOWN, buff=0.09),
            MathTex("D=(0,0)", font_size=24, color=INK).next_to(d_point, LEFT + DOWN, buff=0.09),
        ).set_z_index(11)
        intercept_form = MathTex(r"\frac{x}{16}+\frac{y}{8}=1", font_size=42, color=INK)
        diagonal_equation = MathTex(r"AC:\ x+2y=16", font_size=47, color=BLUE)
        coordinate_note = label("A 到 C 的直線方程", 26, MUTED, "MEDIUM")
        coordinate_panel = VGroup(coordinate_note, intercept_form, diagonal_equation).arrange(
            DOWN, buff=0.46
        )
        coordinate_panel.move_to([4.25, -0.02, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            Succession(FadeOut(perpendicular_panel), FadeIn(coordinate_note)),
            FadeOut(vertex_labels),
            FadeOut(top_length),
            FadeOut(side_length),
            FadeOut(diagonal_label),
            FadeIn(coordinate_labels),
            run_time=0.75,
        )
        self.play(FadeIn(intercept_form), run_time=0.7)
        self.play(FadeIn(diagonal_equation), Circumscribe(diagonal_equation, color=BLUE), run_time=0.85)
        self.wait(0.4)

        # Beat 09: calculate the reflection with the line normal.
        self.next_beat("compute_reflected_point")
        next_title = label("沿法向量算出鏡射點 B'", 32, INK, "BOLD")
        next_title.move_to(beat_title)
        normal_arrow = Arrow(
            h_point,
            h_point + 0.72 * (b_point - h_point) / np.linalg.norm(b_point - h_point),
            color=REGION,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.18,
        ).set_z_index(8)
        normal_label = MathTex(r"n=(1,2)", font_size=25, color=REGION).next_to(
            normal_arrow, LEFT, buff=0.09
        )
        line_function = MathTex(r"L(x,y)=x+2y-16", font_size=34, color=INK)
        normal_data = MathTex(r"n=(1,2),\quad n\cdot n=5", font_size=34, color=REGION)
        at_b = MathTex(r"L(B)=16", font_size=35, color=CORAL)
        reflect_formula = MathTex(
            r"B^\prime=B-2\frac{L(B)}{n\cdot n}n", font_size=36, color=INK
        )
        substitution = MathTex(
            r"=(16,8)-\frac{32}{5}(1,2)", font_size=36, color=INK
        )
        reflected_coordinate = MathTex(
            r"B^\prime=\left(\frac{48}{5},-\frac{24}{5}\right)",
            font_size=41,
            color=REGION,
        )
        reflection_derivation = VGroup(
            line_function,
            normal_data,
            at_b,
            reflect_formula,
            substitution,
            reflected_coordinate,
        ).arrange(DOWN, buff=0.25)
        reflection_derivation.move_to([4.25, -0.12, 0])
        graph_b_prime_coordinate = MathTex(
            r"B^\prime=\left(\frac{48}{5},-\frac{24}{5}\right)",
            font_size=23,
            color=REGION,
        ).next_to(b_prime, RIGHT + DOWN, buff=0.09).set_z_index(11)

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(coordinate_panel), Create(normal_arrow), FadeIn(normal_label), run_time=0.65)
        self.play(FadeIn(line_function), FadeIn(normal_data), run_time=0.7)
        self.play(FadeIn(at_b), run_time=0.45)

        self.next_beat("apply_reflection_formula")
        self.play(FadeIn(reflect_formula), run_time=0.7)
        self.play(FadeIn(substitution), run_time=0.65)
        self.play(
            FadeIn(reflected_coordinate),
            FadeOut(b_prime_label),
            FadeIn(graph_b_prime_coordinate),
            run_time=0.75,
        )
        self.play(Circumscribe(reflected_coordinate, color=REGION), run_time=0.75)
        self.wait(0.4)

        # Beat 10: put P back and verify every equality constraint exactly.
        self.next_beat("verify_attainable_configuration")
        next_title = label("垂足與交點都真的在線段上", 32, INK, "BOLD")
        next_title.move_to(beat_title)
        p_tracker.set_value(0.60)
        final_p = self.diagonal_point(0.60)
        final_qp = Line(q_final_scene, final_p, color=PURPLE, stroke_width=5).set_z_index(6)
        final_pb_prime = Line(final_p, b_prime, color=REGION, stroke_width=5).set_z_index(6)
        final_p_dot = Dot(final_p, radius=0.095, color=POINT).set_z_index(10)
        final_p_label = MathTex("P", font_size=29, color=POINT).next_to(
            final_p, LEFT, buff=0.12
        ).set_z_index(11)
        q_coordinate = MathTex(r"Q=\left(\frac{48}{5},8\right)", font_size=36, color=CORAL)
        q_inside = MathTex(r"0<\frac{48}{5}<16", font_size=34, color=REGION)
        p_coordinate = MathTex(
            r"P=\left(\frac{48}{5},\frac{16}{5}\right)", font_size=36, color=POINT
        )
        p_on_line = MathTex(r"\frac{48}{5}+2\left(\frac{16}{5}\right)=16", font_size=32, color=BLUE)
        vertical_order = MathTex(
            r"8>\frac{16}{5}>-\frac{24}{5}", font_size=36, color=REGION
        )
        unsimplified_distance = MathTex(
            r"QB^\prime=8-\left(-\frac{24}{5}\right)", font_size=42, color=INK
        )
        feasibility_panel = VGroup(
            q_coordinate,
            q_inside,
            p_coordinate,
            p_on_line,
            vertical_order,
            unsimplified_distance,
        ).arrange(DOWN, buff=0.26)
        feasibility_panel.move_to([4.25, -0.47, 0])

        self.transition_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(reflection_derivation),
            FadeOut(normal_arrow),
            FadeOut(normal_label),
            Create(final_qp),
            Create(final_pb_prime),
            GrowFromCenter(final_p_dot),
            FadeIn(final_p_label),
            run_time=0.85,
        )
        self.play(FadeIn(q_coordinate), FadeIn(q_inside), run_time=0.7)
        self.play(FadeIn(p_coordinate), FadeIn(p_on_line), run_time=0.75)

        self.next_beat("verify_collinear_order")
        self.play(FadeIn(vertical_order), run_time=0.55)
        self.play(FadeIn(unsimplified_distance), run_time=0.7)
        self.play(Circumscribe(unsimplified_distance, color=POINT), run_time=0.8)
        self.wait(0.65)

        # Beat 11: simplify only after the complete pre-answer frame has settled.
        self.next_beat("reveal_minimum_length")
        next_title = label("最後只剩下高度差的化簡", 33, INK, "BOLD")
        next_title.move_to(beat_title)
        arithmetic_one = MathTex(
            r"8-\left(-\frac{24}{5}\right)=\frac{40}{5}+\frac{24}{5}",
            font_size=40,
            color=INK,
        )
        arithmetic_two = MathTex(r"=\frac{64}{5}", font_size=54, color=REGION)
        final_answer = MathTex(
            r"\min(PQ+PB)=\frac{64}{5}", font_size=51, color=REGION
        )
        final_box = SurroundingRectangle(
            final_answer,
            color=REGION,
            buff=0.20,
            stroke_width=3,
            corner_radius=0.08,
        )
        final_panel = VGroup(arithmetic_one, arithmetic_two, VGroup(final_answer, final_box)).arrange(
            DOWN, buff=0.50
        )
        final_panel.move_to([4.25, -0.08, 0])

        self.transition_title(self, beat_title, next_title)
        self.play(FadeOut(feasibility_panel), run_time=0.45)
        self.play(FadeIn(arithmetic_one), run_time=0.75)
        self.play(FadeIn(arithmetic_two), run_time=0.55)

        self.next_beat("state_minimum_length")
        self.play(FadeIn(final_answer), Create(final_box), run_time=0.85)
        self.play(
            Indicate(final_qp, color=PURPLE),
            Indicate(final_pb_prime, color=REGION),
            Circumscribe(final_answer, color=REGION),
            run_time=0.85,
        )
        self.wait(0.5)
