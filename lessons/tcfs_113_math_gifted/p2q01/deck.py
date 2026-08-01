"""Manim Slides lesson for ROC 113 TCFS mathematics gifted proof Q1."""

from __future__ import annotations

from fractions import Fraction
import math

import numpy as np

from carlo_manim import (
    BG,
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
    Arc,
    Arrow,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    Integer,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


def angle_degrees(step_count: int, multiplier: int = 1) -> Fraction:
    """Return the exact closure angle selected by the sine recurrence."""
    if step_count < 3 or step_count % 2 == 0:
        raise ValueError("the displayed family uses an odd step count of at least three")
    return Fraction(180 * multiplier, step_count)


def signed_radii(step_count: int, multiplier: int = 1) -> tuple[float, ...]:
    """Return signed positions along the two alternating supporting lines."""
    theta = multiplier * math.pi / step_count
    denominator = math.sin(theta)
    radii = []
    for index in range(step_count + 1):
        radius = math.sin(index * theta) / denominator
        radii.append(0.0 if abs(radius) < 1e-12 else radius)
    return tuple(radii)


def unit_zigzag_coordinates(
    step_count: int, multiplier: int = 1
) -> tuple[np.ndarray, ...]:
    """Place a unit-step alternating path on two lines through the origin."""
    theta = multiplier * math.pi / step_count
    upper_direction = np.array([math.cos(theta), math.sin(theta), 0.0])
    lower_direction = np.array([1.0, 0.0, 0.0])
    radii = signed_radii(step_count, multiplier)
    return tuple(
        radius * (lower_direction if index % 2 else upper_direction)
        for index, radius in enumerate(radii)
    )


def step_lengths(points: tuple[np.ndarray, ...]) -> tuple[float, ...]:
    """Measure every consecutive edge in a computed zigzag."""
    return tuple(
        float(np.linalg.norm(end - start))
        for start, end in zip(points, points[1:])
    )


for _step_count in (3, 5, 7, 9, 11, 13):
    _theta = angle_degrees(_step_count)
    _half_layers = (_step_count - 1) // 2
    if _theta + 2 * _half_layers * _theta != 180:
        raise ValueError("outer-triangle degree check failed")
    if _step_count * _theta != 180:
        raise ValueError("same-ray product check failed")
    _radii = signed_radii(_step_count)
    if not all(radius > 0 for radius in _radii[1:-1]):
        raise ValueError("a same-ray intermediate radius is not positive")
    if _radii[-1] != 0:
        raise ValueError("the same-ray path did not close")
    _points = unit_zigzag_coordinates(_step_count)
    if any(abs(length - 1.0) > 1e-9 for length in step_lengths(_points)):
        raise ValueError("a same-ray edge lost the common unit length")
    if any(np.linalg.norm(point) < 1e-9 for point in _points[1:-1]):
        raise ValueError("the same-ray path returned to O too early")

if angle_degrees(5) != 36 or angle_degrees(7) != Fraction(180, 7):
    raise ValueError("one of the two requested closure angles is incorrect")

_counterexample_radii = signed_radii(5, multiplier=2)
_counterexample_points = unit_zigzag_coordinates(5, multiplier=2)
if not (_counterexample_radii[3] < 0 and _counterexample_radii[4] < 0):
    raise ValueError("the full-line counterexample lost its negative radii")
if _counterexample_radii[-1] != 0:
    raise ValueError("the full-line counterexample did not close")
if any(
    abs(length - 1.0) > 1e-9
    for length in step_lengths(_counterexample_points)
):
    raise ValueError("the full-line counterexample lost equal step lengths")
if 5 * angle_degrees(5, multiplier=2) != 360:
    raise ValueError("the full-line counterexample product is not 360")


class CarloTcfs113MathP2Q01(CarloSlide):
    """Grow equal-step angles slowly, with the same-ray scope kept explicit."""

    lesson_id = "carlo.tcfs_113_math_gifted.p2q01"

    @staticmethod
    def transition_title(scene: "CarloTcfs113MathP2Q01", old, new) -> None:
        """Replace Traditional Chinese titles without morphing glyph outlines."""
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.56)

    @staticmethod
    def display_points(
        step_count: int,
        origin: np.ndarray,
        scale: float,
        *,
        multiplier: int = 1,
    ) -> tuple[np.ndarray, ...]:
        """Map the checked unit model into one stable diagram pane."""
        return tuple(
            origin + scale * point
            for point in unit_zigzag_coordinates(step_count, multiplier)
        )

    @staticmethod
    def ray_pair(
        origin: np.ndarray,
        theta: float,
        length: float,
        *,
        color: str = MUTED,
    ) -> VGroup:
        """Draw the two specified forward rays used by the scoped family."""
        lower_direction = np.array([1.0, 0.0, 0.0])
        upper_direction = np.array([math.cos(theta), math.sin(theta), 0.0])
        return VGroup(
            Arrow(
                origin,
                origin + length * lower_direction,
                buff=0,
                color=color,
                stroke_width=2.7,
                max_tip_length_to_length_ratio=0.035,
            ),
            Arrow(
                origin,
                origin + length * upper_direction,
                buff=0,
                color=color,
                stroke_width=2.7,
                max_tip_length_to_length_ratio=0.035,
            ),
        ).set_z_index(1)

    @staticmethod
    def full_line_pair(
        origin: np.ndarray,
        theta: float,
        length: float,
    ) -> VGroup:
        """Draw two complete lines for the deliberately out-of-scope example."""
        lower_direction = np.array([1.0, 0.0, 0.0])
        upper_direction = np.array([math.cos(theta), math.sin(theta), 0.0])
        return VGroup(
            Line(
                origin - length * lower_direction,
                origin + length * lower_direction,
                color=MUTED,
                stroke_width=2.7,
            ),
            Line(
                origin - length * upper_direction,
                origin + length * upper_direction,
                color=MUTED,
                stroke_width=2.7,
            ),
        ).set_z_index(1)

    @staticmethod
    def path_segments(points: tuple[np.ndarray, ...], color: str = BLUE) -> VGroup:
        """Build separate path edges so one moving point can reveal them in order."""
        return VGroup(
            *[
                Line(start, end, color=color, stroke_width=5.0).set_z_index(5)
                for start, end in zip(points, points[1:])
            ]
        )

    @staticmethod
    def step_tick(start: np.ndarray, end: np.ndarray, color: str = POINT) -> Line:
        """Mark one edge as carrying the shared step length."""
        direction = end - start
        normal = np.array([-direction[1], direction[0], 0.0])
        normal /= np.linalg.norm(normal)
        midpoint = (start + end) / 2
        return Line(
            midpoint - normal * 0.085,
            midpoint + normal * 0.085,
            color=color,
            stroke_width=3.0,
        ).set_z_index(8)

    @classmethod
    def step_ticks(cls, points: tuple[np.ndarray, ...], color: str = POINT) -> VGroup:
        """Mark all path edges with the same compact tick."""
        return VGroup(
            *[
                cls.step_tick(start, end, color)
                for start, end in zip(points, points[1:])
            ]
        )

    @staticmethod
    def angle_marker(
        vertex: np.ndarray,
        first_point: np.ndarray,
        second_point: np.ndarray,
        tex: str,
        color: str,
        *,
        radius: float = 0.30,
        label_radius: float = 0.68,
        font_size: float = 27,
    ) -> VGroup:
        """Draw the smaller angle at a vertex and place its label on the bisector."""
        first = first_point - vertex
        second = second_point - vertex
        first /= np.linalg.norm(first)
        second /= np.linalg.norm(second)
        start = math.atan2(first[1], first[0])
        end = math.atan2(second[1], second[0])
        sweep = (end - start) % (2 * math.pi)
        if sweep > math.pi:
            start, end = end, start
            sweep = (end - start) % (2 * math.pi)
        arc = Arc(
            radius=radius,
            start_angle=start,
            angle=sweep,
            color=color,
            stroke_width=4.2,
        ).shift(vertex)
        middle = start + sweep / 2
        angle_label = MathTex(tex, font_size=font_size, color=color)
        angle_label.move_to(
            vertex
            + label_radius * np.array([math.cos(middle), math.sin(middle), 0.0])
        )
        return VGroup(arc, angle_label).set_z_index(11)

    @staticmethod
    def scope_banner(
        *,
        color: str = REGION,
        top_text: str = "同射線首次閉合",
        bottom_text: str = "非 O 落點只在兩條指定射線上",
    ) -> VGroup:
        """Keep the exact domain of the general claim visible in the diagram pane."""
        top = label(top_text, 25, color, "BOLD")
        bottom = label(bottom_text, 21, INK, "MEDIUM")
        content = VGroup(top, bottom).arrange(DOWN, buff=0.12)
        frame = SurroundingRectangle(
            content,
            buff=0.18,
            corner_radius=0.05,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.92,
        )
        return VGroup(frame, content).move_to([-3.72, -2.75, 0]).set_z_index(20)

    @staticmethod
    def origin_mark(origin: np.ndarray) -> VGroup:
        """Build the fixed origin dot and its mathematical name."""
        dot = Dot(origin, radius=0.085, color=INK).set_z_index(10)
        name = MathTex("O", font_size=27, color=INK).next_to(
            dot, DOWN + LEFT, buff=0.10
        )
        return VGroup(dot, name)

    @staticmethod
    def point_labels(
        points: tuple[np.ndarray, ...], names: tuple[str, ...]
    ) -> VGroup:
        """Place compact labels away from alternating path edges."""
        labels = []
        for index, (point, name) in enumerate(zip(points[1:-1], names), start=1):
            direction = DOWN if index % 2 else UP
            labels.append(
                MathTex(name, font_size=25, color=INK).next_to(
                    point, direction, buff=0.11
                )
            )
        return VGroup(*labels).set_z_index(12)

    @staticmethod
    def highlight_triangle(
        first: np.ndarray,
        second: np.ndarray,
        third: np.ndarray,
        *,
        color: str = PURPLE,
        opacity: float = 0.10,
    ) -> Polygon:
        """Show one equal-step triangle without hiding the whole path."""
        return Polygon(
            first,
            second,
            third,
            color=color,
            stroke_width=3.5,
            fill_color=color,
            fill_opacity=opacity,
        ).set_z_index(3)

    def construct(self) -> None:
        heading = label("第二部分第 1 題｜等步長之字路徑", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 14-16 頁｜影片 rw7Z1rw7gYA 00:00-04:34",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line(
            [0.70, -3.53, 0], [0.70, 3.43, 0], color=HAIRLINE, stroke_width=1.5
        )

        # Beat 01 meet_two_rays: fix the scoped family before any closure path appears.
        self.begin_beat("meet_two_rays")
        stage_title = label("先固定兩條射線與一步的長度", 33, INK, "BOLD")
        stage_title.move_to([4.32, 3.02, 0])
        origin5 = np.array([-6.25, -1.02, 0.0])
        theta5 = math.pi / 5
        rays5 = self.ray_pair(origin5, theta5, 5.55)
        origin_mark5 = self.origin_mark(origin5)
        theta_mark5 = self.angle_marker(
            origin5,
            origin5 + RIGHT,
            origin5 + np.array([math.cos(theta5), math.sin(theta5), 0.0]),
            r"\theta",
            POINT,
            radius=0.36,
            label_radius=0.79,
            font_size=29,
        )
        scope = self.scope_banner()
        ruler = Line([2.75, 0.55, 0], [4.05, 0.55, 0], color=BLUE, stroke_width=5)
        ruler_tick = self.step_tick(ruler.get_start(), ruler.get_end())
        intro_panel = VGroup(
            label("落點在兩條射線間交替", 29, INK, "BOLD"),
            VGroup(ruler, ruler_tick),
            label("每一步都一樣長", 27, BLUE, "BOLD"),
            label("先不猜角度", 27, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.42)
        intro_panel.move_to([4.32, -0.10, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Create(rays5), run_time=0.85)
        self.play(
            FadeIn(origin_mark5),
            Create(theta_mark5[0]),
            FadeIn(theta_mark5[1]),
            run_time=0.60,
        )
        self.play(FadeIn(scope), run_time=0.55)
        self.play(
            LaggedStart(*(FadeIn(item) for item in intro_panel), lag_ratio=0.18),
            run_time=1.00,
        )
        self.wait(0.40)

        # Beat 02 walk_five_steps: one persistent point reveals five equal edges.
        self.next_beat("walk_five_steps")
        next_title = label("讓同一個點走完五步", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        points5 = self.display_points(5, origin5, 2.28)
        segments5 = self.path_segments(points5)
        ticks5 = self.step_ticks(points5)
        waypoint_dots5 = VGroup(
            *[
                Dot(point, radius=0.055, color=BLUE).set_z_index(7)
                for point in points5[1:-1]
            ]
        )
        point_names5 = self.point_labels(points5, ("A", "B", "C", "D"))
        robot5 = Dot(points5[0], radius=0.115, color=POINT).set_z_index(15)
        counter_number5 = Integer(0, font_size=50, color=POINT)
        counter5 = VGroup(
            label("已走步數", 25, MUTED, "MEDIUM"), counter_number5
        ).arrange(DOWN, buff=0.18)
        counter5.move_to([4.32, 0.90, 0])
        five_question = VGroup(
            label("第 5 步回到 O", 29, REGION, "BOLD"),
            label("夾角 θ 是多少？", 31, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.34)
        five_question.move_to([4.32, -1.05, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(intro_panel), FadeIn(counter5), GrowFromCenter(robot5), run_time=0.65)
        for index, segment in enumerate((segments5[0], segments5[1]), start=1):
            animations = [
                Create(segment),
                robot5.animate.move_to(points5[index]),
                counter_number5.animate.set_value(index),
            ]
            if index < 5:
                animations.extend(
                    [FadeIn(waypoint_dots5[index - 1]), FadeIn(point_names5[index - 1])]
                )
            self.play(
                *animations,
                run_time=0.58,
                rate_func=rate_functions.ease_in_out_sine,
            )

        self.next_beat("finish_five_step_walk")
        for index, segment in enumerate(
            (segments5[2], segments5[3], segments5[4]), start=3
        ):
            animations = [
                Create(segment),
                robot5.animate.move_to(points5[index]),
                counter_number5.animate.set_value(index),
            ]
            if index < 5:
                animations.extend(
                    [FadeIn(waypoint_dots5[index - 1]), FadeIn(point_names5[index - 1])]
                )
            self.play(
                *animations,
                run_time=0.58,
                rate_func=rate_functions.ease_in_out_sine,
            )
        self.play(
            LaggedStart(*(Create(tick) for tick in ticks5), lag_ratio=0.12),
            FadeIn(five_question),
            run_time=0.85,
        )
        self.wait(0.45)

        # Beat 03 seed_equal_angles: the first two equal steps earn the first theta.
        self.next_beat("seed_equal_angles")
        next_title = label("先只看第一個等腰三角形", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        seed_triangle5 = self.highlight_triangle(points5[0], points5[1], points5[2])
        seed_angle_b5 = self.angle_marker(
            points5[2], points5[0], points5[1], r"\theta", POINT
        )
        seed_equal = MathTex("OA", "=", "AB", font_size=49, color=INK)
        seed_equal[0].set_color(BLUE)
        seed_equal[2].set_color(BLUE)
        seed_angle_line = MathTex(
            r"\angle AOB", "=", r"\angle OBA", "=", r"\theta",
            font_size=40,
            color=INK,
        )
        seed_angle_line[0].set_color(POINT)
        seed_angle_line[2].set_color(POINT)
        seed_angle_line[4].set_color(POINT)
        seed_note = label("相等的邊，先送出第一個等角", 25, MUTED, "MEDIUM")
        seed_panel = VGroup(seed_equal, seed_angle_line, seed_note).arrange(
            DOWN, buff=0.48
        )
        seed_panel.move_to([4.32, -0.08, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(VGroup(counter5, five_question, robot5)),
            segments5[2:].animate.set_opacity(0.14),
            ticks5[2:].animate.set_opacity(0.14),
            waypoint_dots5[2:].animate.set_opacity(0.14),
            point_names5[2:].animate.set_opacity(0.14),
            run_time=0.62,
        )
        self.play(Create(seed_triangle5), run_time=0.62)
        self.play(Indicate(VGroup(ticks5[0], ticks5[1]), color=POINT), FadeIn(seed_equal), run_time=0.72)

        self.next_beat("mark_first_equal_sides")
        self.play(
            Create(seed_angle_b5[0]),
            FadeIn(seed_angle_b5[1]),
            FadeIn(seed_angle_line),
            run_time=0.80,
        )
        self.play(FadeIn(seed_note), run_time=0.42)
        self.wait(0.40)

        # Beat 04 propagate_five_step_angles: grow from both ends to the outer triangle.
        self.next_beat("propagate_five_step_angles")
        next_title = label("從兩端各推一層，得到兩個 2θ", 31, INK, "BOLD")
        next_title.move_to(stage_title)
        forward_triangle5 = self.highlight_triangle(points5[1], points5[2], points5[3])
        reverse_triangle5 = self.highlight_triangle(points5[4], points5[3], points5[2])
        angle_c5 = self.angle_marker(
            points5[3], points5[0], points5[2], r"2\theta", PURPLE,
            radius=0.34,
            label_radius=0.75,
        )
        angle_b5 = self.angle_marker(
            points5[2], points5[0], points5[3], r"2\theta", PURPLE,
            radius=0.34,
            label_radius=0.75,
        )
        outer5 = self.highlight_triangle(
            points5[0], points5[2], points5[3], color=REGION, opacity=0.07
        )
        propagation_panel = VGroup(
            MathTex(r"\alpha_1=\theta", font_size=43, color=POINT),
            MathTex(
                r"\alpha_2=\alpha_1+\theta=2\theta",
                font_size=40,
                color=PURPLE,
            ),
            label("從終點倒著走，同樣得到 2θ", 25, REGION, "BOLD"),
            MathTex(r"\theta,\ 2\theta,\ 2\theta", font_size=47, color=INK),
        ).arrange(DOWN, buff=0.46)
        propagation_panel.move_to([4.32, -0.15, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(seed_panel),
            FadeOut(seed_triangle5),
            FadeOut(seed_angle_b5),
            segments5[2:].animate.set_opacity(1.0),
            ticks5[2:].animate.set_opacity(1.0),
            waypoint_dots5[2:].animate.set_opacity(1.0),
            point_names5[2:].animate.set_opacity(1.0),
            run_time=0.62,
        )
        self.play(Create(forward_triangle5), FadeIn(propagation_panel[0]), run_time=0.72)
        self.play(Create(angle_c5[0]), FadeIn(angle_c5[1]), FadeIn(propagation_panel[1]), run_time=0.72)

        self.next_beat("complete_five_step_propagation")
        self.play(
            Create(reverse_triangle5),
            Create(angle_b5[0]),
            FadeIn(angle_b5[1]),
            FadeIn(propagation_panel[2]),
            run_time=0.78,
        )
        self.play(
            FadeOut(forward_triangle5),
            FadeOut(reverse_triangle5),
            Create(outer5),
            FadeIn(propagation_panel[3]),
            run_time=0.75,
        )
        self.wait(0.40)

        # Beat 05 reveal_thirty_six: build the five-step answer from the visible angles.
        self.next_beat("reveal_thirty_six")
        next_title = label("最外三角形現在可以計算", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        equation5a = MathTex(
            r"\theta+2\theta+2\theta=180^\circ",
            font_size=43,
            color=INK,
        )
        equation5b = MathTex(r"5\theta=180^\circ", font_size=47, color=INK)
        answer5 = MathTex(r"\theta=36^\circ", font_size=58, color=REGION)
        answer5_box = SurroundingRectangle(
            answer5, buff=0.18, color=REGION, corner_radius=0.05, stroke_width=2.6
        )
        memory5 = MathTex(r"5\cdot36^\circ=180^\circ", font_size=36, color=POINT)
        answer_panel5 = VGroup(
            equation5a, equation5b, VGroup(answer5_box, answer5), memory5
        ).arrange(DOWN, buff=0.52)
        answer_panel5.move_to([4.32, -0.20, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(propagation_panel), run_time=0.35)
        self.play(
            FadeIn(equation5a),
            run_time=0.85,
        )

        self.next_beat("solve_five_step_angle")
        self.play(FadeIn(equation5b), run_time=0.60)
        self.play(FadeIn(answer5), Create(answer5_box), run_time=0.72)
        self.play(FadeIn(memory5), Circumscribe(answer5, color=REGION), run_time=0.78)
        self.wait(0.45)

        # Beat 06 walk_seven_steps: add one layer while preserving the same-ray rule.
        self.next_beat("walk_seven_steps")
        next_title = label("同樣規則，這次走七步", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        origin7 = np.array([-6.28, -1.08, 0.0])
        theta7 = math.pi / 7
        points7 = self.display_points(7, origin7, 1.86)
        rays7 = self.ray_pair(origin7, theta7, 5.62)
        origin_mark7 = self.origin_mark(origin7)
        theta_mark7 = self.angle_marker(
            origin7,
            origin7 + RIGHT,
            origin7 + np.array([math.cos(theta7), math.sin(theta7), 0.0]),
            r"\theta",
            POINT,
            radius=0.39,
            label_radius=0.86,
            font_size=28,
        )
        segments7 = self.path_segments(points7)
        ticks7 = self.step_ticks(points7)
        waypoint_dots7 = VGroup(
            *[
                Dot(point, radius=0.050, color=BLUE).set_z_index(7)
                for point in points7[1:-1]
            ]
        )
        point_names7 = self.point_labels(
            points7, tuple(rf"P_{{{index}}}" for index in range(1, 7))
        )
        robot7 = Dot(points7[0], radius=0.115, color=POINT).set_z_index(15)
        counter_number7 = Integer(0, font_size=50, color=POINT)
        counter7 = VGroup(
            label("已走步數", 25, MUTED, "MEDIUM"), counter_number7
        ).arrange(DOWN, buff=0.18)
        counter7.move_to([4.32, 0.95, 0])
        seven_prompt = VGroup(
            label("第 7 步回到 O", 29, REGION, "BOLD"),
            label("底角會長到幾個 θ？", 29, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.34)
        seven_prompt.move_to([4.32, -1.05, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    rays5,
                    origin_mark5,
                    theta_mark5,
                    segments5,
                    ticks5,
                    waypoint_dots5,
                    point_names5,
                    outer5,
                    angle_b5,
                    angle_c5,
                    answer_panel5,
                )
            ),
            Create(rays7),
            FadeIn(origin_mark7),
            Create(theta_mark7[0]),
            FadeIn(theta_mark7[1]),
            FadeIn(counter7),
            GrowFromCenter(robot7),
            run_time=0.88,
        )
        for index, segment in enumerate((segments7[0], segments7[1]), start=1):
            animations = [
                Create(segment),
                robot7.animate.move_to(points7[index]),
                counter_number7.animate.set_value(index),
            ]
            if index < 7:
                animations.extend(
                    [FadeIn(waypoint_dots7[index - 1]), FadeIn(point_names7[index - 1])]
                )
            self.play(
                *animations,
                run_time=0.50,
                rate_func=rate_functions.ease_in_out_sine,
            )

        self.next_beat("continue_seven_step_walk")
        for index, segment in enumerate(
            (segments7[2], segments7[3], segments7[4]), start=3
        ):
            animations = [
                Create(segment),
                robot7.animate.move_to(points7[index]),
                counter_number7.animate.set_value(index),
            ]
            animations.extend(
                [FadeIn(waypoint_dots7[index - 1]), FadeIn(point_names7[index - 1])]
            )
            self.play(
                *animations,
                run_time=0.50,
                rate_func=rate_functions.ease_in_out_sine,
            )

        self.next_beat("finish_seven_step_walk")
        for index, segment in enumerate((segments7[5], segments7[6]), start=6):
            animations = [
                Create(segment),
                robot7.animate.move_to(points7[index]),
                counter_number7.animate.set_value(index),
            ]
            if index < 7:
                animations.extend(
                    [FadeIn(waypoint_dots7[index - 1]), FadeIn(point_names7[index - 1])]
                )
            self.play(
                *animations,
                run_time=0.50,
                rate_func=rate_functions.ease_in_out_sine,
            )
        self.play(
            LaggedStart(*(Create(tick) for tick in ticks7), lag_ratio=0.09),
            FadeIn(seven_prompt),
            run_time=0.80,
        )
        self.wait(0.42)

        # Beat 07 grow_three_layers: propagate theta, two theta, and three theta.
        self.next_beat("grow_three_layers")
        next_title = label("每往內一層，底角多一個 θ", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        layer_triangles7 = [
            self.highlight_triangle(points7[index - 1], points7[index], points7[index + 1])
            for index in range(1, 4)
        ]
        layer_angles7 = [
            self.angle_marker(
                points7[index + 1],
                points7[index - 1],
                points7[index],
                rf"{index}\theta" if index > 1 else r"\theta",
                PURPLE if index > 1 else POINT,
                radius=0.31,
                label_radius=0.72,
                font_size=25,
            )
            for index in range(1, 4)
        ]
        ladder7 = VGroup(
            MathTex(r"\alpha_1=\theta", font_size=41, color=POINT),
            MathTex(r"\alpha_2=2\theta", font_size=41, color=PURPLE),
            MathTex(r"\alpha_3=3\theta", font_size=41, color=PURPLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.40)
        ladder7.move_to([4.32, 0.40, 0])
        reverse_note7 = label("從終點倒走，也得到 3θ", 25, REGION, "BOLD")
        reverse_note7.move_to([4.32, -1.48, 0])
        outer7 = self.highlight_triangle(
            points7[0], points7[3], points7[4], color=REGION, opacity=0.07
        )
        reverse_angle7 = self.angle_marker(
            points7[3], points7[0], points7[4], r"3\theta", PURPLE,
            radius=0.32,
            label_radius=0.73,
            font_size=25,
        )

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(VGroup(counter7, seven_prompt, robot7)),
            segments7.animate.set_opacity(0.32),
            ticks7.animate.set_opacity(0.32),
            waypoint_dots7.animate.set_opacity(0.32),
            point_names7.animate.set_opacity(0.32),
            run_time=0.60,
        )
        active_triangle7 = layer_triangles7[0]
        active_angle7 = layer_angles7[0]
        self.play(
            Create(active_triangle7),
            Create(active_angle7[0]),
            FadeIn(active_angle7[1]),
            FadeIn(ladder7[0]),
            run_time=0.78,
        )
        index = 1
        self.play(
            Transform(active_triangle7, layer_triangles7[index]),
            Transform(active_angle7[0], layer_angles7[index][0]),
            Succession(FadeOut(active_angle7[1]), FadeIn(layer_angles7[index][1])),
            FadeIn(ladder7[index]),
            run_time=0.82,
        )
        active_angle7 = VGroup(active_angle7[0], layer_angles7[index][1])

        self.next_beat("complete_three_layer_growth")
        index = 2
        self.play(
            Transform(active_triangle7, layer_triangles7[index]),
            Transform(active_angle7[0], layer_angles7[index][0]),
            Succession(FadeOut(active_angle7[1]), FadeIn(layer_angles7[index][1])),
            FadeIn(ladder7[index]),
            run_time=0.82,
        )
        active_angle7 = VGroup(active_angle7[0], layer_angles7[index][1])
        self.play(
            FadeOut(active_triangle7),
            Create(outer7),
            Create(reverse_angle7[0]),
            FadeIn(reverse_angle7[1]),
            FadeIn(reverse_note7),
            run_time=0.78,
        )
        self.wait(0.40)

        # Beat 08 reveal_seven_step_angle: close the seven-step outer triangle.
        self.next_beat("reveal_seven_step_angle")
        next_title = label("七步路徑的最外三角形", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        equation7a = MathTex(
            r"\theta+3\theta+3\theta=180^\circ",
            font_size=42,
            color=INK,
        )
        equation7b = MathTex(r"7\theta=180^\circ", font_size=47, color=INK)
        answer7 = MathTex(r"\theta={180^\circ\over7}", font_size=56, color=REGION)
        answer7_box = SurroundingRectangle(
            answer7, buff=0.18, color=REGION, corner_radius=0.05, stroke_width=2.6
        )
        answer_panel7 = VGroup(
            equation7a, equation7b, VGroup(answer7_box, answer7)
        ).arrange(DOWN, buff=0.56)
        answer_panel7.move_to([4.32, -0.10, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(ladder7), FadeOut(reverse_note7), run_time=0.38)
        self.play(
            FadeIn(equation7a),
            run_time=0.88,
        )

        self.next_beat("solve_seven_step_angle")
        self.play(FadeIn(equation7b), run_time=0.62)
        self.play(FadeIn(answer7), Create(answer7_box), run_time=0.76)
        self.play(Circumscribe(answer7, color=REGION), run_time=0.70)
        self.wait(0.42)

        # Beat 09 name_general_scope: name n and h only after the two concrete cases.
        self.next_beat("name_general_scope")
        next_title = label("現在才把來源圖族寫成一般奇數", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        origin9 = np.array([-6.30, -1.10, 0.0])
        theta9 = math.pi / 9
        points9 = self.display_points(9, origin9, 1.54)
        rays9 = self.ray_pair(origin9, theta9, 5.78)
        origin_mark9 = self.origin_mark(origin9)
        theta_mark9 = self.angle_marker(
            origin9,
            origin9 + RIGHT,
            origin9 + np.array([math.cos(theta9), math.sin(theta9), 0.0]),
            r"\theta",
            POINT,
            radius=0.43,
            label_radius=0.91,
            font_size=27,
        )
        segments9 = self.path_segments(points9)
        ticks9 = self.step_ticks(points9)
        waypoint_dots9 = VGroup(
            *[
                Dot(point, radius=0.045, color=BLUE).set_z_index(7)
                for point in points9[1:-1]
            ]
        )
        general_panel = VGroup(
            MathTex(r"n=2h+1", font_size=53, color=POINT),
            MathTex(r"h={n-1\over2}", font_size=47, color=PURPLE),
            label("畫面以 9 步、4 層作代表", 25, MUTED, "MEDIUM"),
            VGroup(
                label("第一次回到 O", 25, REGION, "BOLD"),
                label("中間點不穿過 O", 25, REGION, "BOLD"),
            ).arrange(DOWN, buff=0.18),
        ).arrange(DOWN, buff=0.46)
        general_panel.move_to([4.32, -0.10, 0])
        representative = MathTex(r"9=2\cdot4+1", font_size=31, color=MUTED)
        representative.move_to([-3.68, 1.30, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    rays7,
                    origin_mark7,
                    theta_mark7,
                    segments7,
                    ticks7,
                    waypoint_dots7,
                    point_names7,
                    outer7,
                    active_angle7,
                    reverse_angle7,
                    answer_panel7,
                )
            ),
            Create(rays9),
            FadeIn(origin_mark9),
            Create(theta_mark9[0]),
            FadeIn(theta_mark9[1]),
            run_time=0.85,
        )
        self.play(
            LaggedStart(*(Create(segment) for segment in segments9), lag_ratio=0.08),
            LaggedStart(*(FadeIn(dot) for dot in waypoint_dots9), lag_ratio=0.08),
            run_time=1.10,
        )
        self.play(
            LaggedStart(*(Create(tick) for tick in ticks9), lag_ratio=0.07),
            FadeIn(representative),
            run_time=0.70,
        )
        self.play(
            LaggedStart(*(FadeIn(item) for item in general_panel), lag_ratio=0.16),
            Indicate(scope, color=REGION),
            run_time=1.00,
        )
        self.wait(0.42)

        # Beat 10 build_angle_recurrence: one representative side grows by theta each layer.
        self.next_beat("build_angle_recurrence")
        next_title = label("一層一層建立角度遞推", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        layer_triangles9 = [
            self.highlight_triangle(points9[index - 1], points9[index], points9[index + 1])
            for index in range(1, 5)
        ]
        layer_angles9 = [
            self.angle_marker(
                points9[index + 1],
                points9[index - 1],
                points9[index],
                rf"\alpha_{{{index}}}",
                POINT if index == 1 else PURPLE,
                radius=0.29,
                label_radius=0.67,
                font_size=23,
            )
            for index in range(1, 5)
        ]
        recurrence_panel = VGroup(
            MathTex(r"\alpha_1=\theta", font_size=42, color=POINT),
            MathTex(
                r"\alpha_{j+1}=\alpha_j+\theta",
                font_size=43,
                color=PURPLE,
            ),
            MathTex(
                r"\theta,\ 2\theta,\ 3\theta,\ldots",
                font_size=40,
                color=INK,
            ),
            MathTex(r"\alpha_h=h\theta", font_size=48, color=REGION),
            label("從終點倒走，另一側也相同", 24, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.43)
        recurrence_panel.move_to([4.32, -0.10, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(general_panel),
            FadeOut(representative),
            segments9.animate.set_opacity(0.28),
            ticks9.animate.set_opacity(0.28),
            waypoint_dots9.animate.set_opacity(0.28),
            run_time=0.60,
        )
        active_triangle9 = layer_triangles9[0]
        active_angle9 = layer_angles9[0]
        self.play(
            Create(active_triangle9),
            Create(active_angle9[0]),
            FadeIn(active_angle9[1]),
            FadeIn(recurrence_panel[0]),
            run_time=0.80,
        )
        self.play(FadeIn(recurrence_panel[1]), run_time=0.70)

        self.next_beat("propagate_general_angles")
        for index in (1, 2):
            self.play(
                Transform(active_triangle9, layer_triangles9[index]),
                Transform(active_angle9[0], layer_angles9[index][0]),
                Succession(FadeOut(active_angle9[1]), FadeIn(layer_angles9[index][1])),
                run_time=0.78,
            )
            active_angle9 = VGroup(active_angle9[0], layer_angles9[index][1])

        self.next_beat("complete_general_propagation")
        index = 3
        self.play(
            Transform(active_triangle9, layer_triangles9[index]),
            Transform(active_angle9[0], layer_angles9[index][0]),
            Succession(FadeOut(active_angle9[1]), FadeIn(layer_angles9[index][1])),
            run_time=0.78,
        )
        active_angle9 = VGroup(active_angle9[0], layer_angles9[index][1])
        self.play(FadeIn(recurrence_panel[2]), run_time=0.62)
        self.play(FadeIn(recurrence_panel[3]), FadeIn(recurrence_panel[4]), run_time=0.76)
        self.wait(0.42)

        # Beat 11 close_outer_triangle: derive mn=180 only inside the visible scope.
        self.next_beat("close_outer_triangle")
        next_title = label("只留下最外三角形", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        outer9 = self.highlight_triangle(
            points9[0], points9[4], points9[5], color=REGION, opacity=0.08
        )
        forward_h_angle9 = self.angle_marker(
            points9[5], points9[0], points9[4], r"h\theta", REGION,
            radius=0.31,
            label_radius=0.73,
            font_size=25,
        )
        reverse_h_angle9 = self.angle_marker(
            points9[4], points9[0], points9[5], r"h\theta", REGION,
            radius=0.31,
            label_radius=0.73,
            font_size=25,
        )
        outer_equation = MathTex(
            r"\theta+h\theta+h\theta=180^\circ",
            font_size=39,
            color=INK,
        )
        n_equation = MathTex(r"n\theta=180^\circ", font_size=50, color=INK)
        product_equation = MathTex(
            r"\theta=m^\circ\quad\Longrightarrow\quad mn=180",
            font_size=45,
            color=REGION,
        )
        product_box = SurroundingRectangle(
            product_equation,
            buff=0.18,
            color=REGION,
            corner_radius=0.05,
            stroke_width=2.7,
        )
        scoped_note = label("只在綠色限定構形內", 25, REGION, "BOLD")
        product_panel = VGroup(
            outer_equation,
            n_equation,
            VGroup(product_box, product_equation),
            scoped_note,
        ).arrange(DOWN, buff=0.48)
        product_panel.move_to([4.32, -0.12, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(recurrence_panel),
            FadeOut(active_triangle9),
            FadeOut(active_angle9),
            Create(outer9),
            run_time=0.72,
        )
        self.play(
            Create(forward_h_angle9[0]),
            FadeIn(forward_h_angle9[1]),
            Create(reverse_h_angle9[0]),
            FadeIn(reverse_h_angle9[1]),
            run_time=0.66,
        )
        self.play(
            FadeIn(outer_equation),
            run_time=0.85,
        )

        self.next_beat("state_scoped_product")
        self.play(FadeIn(n_equation), run_time=0.62)
        self.play(FadeIn(product_equation), Create(product_box), run_time=0.78)
        self.play(FadeIn(scoped_note), Indicate(scope, color=REGION), run_time=0.72)
        self.wait(0.45)

        # Beat 12 mark_scope_boundary: one full-line closure shows why the qualifier matters.
        self.next_beat("mark_scope_boundary")
        next_title = label("若改成完整直線，會出現別的閉合角", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        counter_origin = np.array([-3.72, -0.22, 0.0])
        counter_theta = 2 * math.pi / 5
        counter_points = self.display_points(
            5, counter_origin, 2.02, multiplier=2
        )
        full_lines = self.full_line_pair(counter_origin, counter_theta, 3.35)
        counter_origin_mark = self.origin_mark(counter_origin)
        counter_segments = self.path_segments(counter_points)
        counter_ticks = self.step_ticks(counter_points)
        counter_dots = VGroup(
            *[
                Dot(
                    point,
                    radius=0.065,
                    color=CORAL if index in (3, 4) else BLUE,
                ).set_z_index(9)
                for index, point in enumerate(counter_points[1:-1], start=1)
            ]
        )
        counter_angle = self.angle_marker(
            counter_origin,
            counter_origin + RIGHT,
            counter_origin
            + np.array([math.cos(counter_theta), math.sin(counter_theta), 0.0]),
            r"72^\circ",
            CORAL,
            radius=0.40,
            label_radius=0.92,
            font_size=27,
        )
        negative_labels = VGroup(
            MathTex(r"P_3", font_size=25, color=CORAL).next_to(
                counter_points[3], UP, buff=0.10
            ),
            MathTex(r"P_4", font_size=25, color=CORAL).next_to(
                counter_points[4], UP + LEFT, buff=0.10
            ),
        )
        outside_banner = self.scope_banner(
            color=CORAL,
            top_text="完整直線：允許穿過 O",
            bottom_text="珊瑚色落點已在反向延長線",
        )
        counter_panel = VGroup(
            MathTex(r"n=5,\quad \theta=72^\circ", font_size=43, color=INK),
            MathTex(r"r_3<0,\quad r_4<0", font_size=43, color=CORAL),
            MathTex(r"5\cdot72^\circ=360^\circ", font_size=50, color=CORAL),
            label("完整直線問題的反例", 28, CORAL, "BOLD"),
            label("不屬於本課同射線構形", 25, INK, "BOLD"),
        ).arrange(DOWN, buff=0.43)
        counter_panel.move_to([4.32, -0.08, 0])

        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(
                VGroup(
                    rays9,
                    origin_mark9,
                    theta_mark9,
                    segments9,
                    ticks9,
                    waypoint_dots9,
                    outer9,
                    forward_h_angle9,
                    reverse_h_angle9,
                    product_panel,
                    scope,
                )
            ),
            Create(full_lines),
            FadeIn(counter_origin_mark),
            FadeIn(outside_banner),
            run_time=0.82,
        )
        self.play(
            LaggedStart(*(Create(segment) for segment in counter_segments), lag_ratio=0.13),
            LaggedStart(*(FadeIn(dot) for dot in counter_dots), lag_ratio=0.13),
            run_time=1.10,
        )

        self.next_beat("verify_full_line_counterexample")
        self.play(
            LaggedStart(*(Create(tick) for tick in counter_ticks), lag_ratio=0.10),
            Create(counter_angle[0]),
            FadeIn(counter_angle[1]),
            FadeIn(negative_labels),
            run_time=0.82,
        )
        self.play(
            LaggedStart(*(FadeIn(item) for item in counter_panel), lag_ratio=0.15),
            run_time=1.00,
        )
        self.play(Indicate(VGroup(counter_dots[2], counter_dots[3]), color=CORAL), run_time=0.70)
        self.wait(0.45)

        # Beat 13 consolidate_scoped_invariant: return to the source family and summarize.
        self.next_beat("consolidate_scoped_invariant")
        next_title = label("回到正確範圍，三個答案連在一起", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        final_origin = np.array([-6.30, -1.10, 0.0])
        final_points = self.display_points(9, final_origin, 1.54)
        final_rays = self.ray_pair(final_origin, math.pi / 9, 5.78)
        final_origin_mark = self.origin_mark(final_origin)
        final_segments = self.path_segments(final_points)
        final_ticks = self.step_ticks(final_points)
        final_dots = VGroup(
            *[
                Dot(point, radius=0.045, color=BLUE).set_z_index(7)
                for point in final_points[1:-1]
            ]
        )
        final_scope = self.scope_banner()
        result5 = MathTex(r"n=5\quad\Longrightarrow\quad\theta=36^\circ", font_size=39, color=INK)
        result7 = MathTex(
            r"n=7\quad\Longrightarrow\quad\theta={180^\circ\over7}",
            font_size=39,
            color=INK,
        )
        result_general = MathTex(
            r"n=2h+1,\ \theta=m^\circ\quad\Longrightarrow\quad mn=180",
            font_size=36,
            color=REGION,
        )
        final_box = SurroundingRectangle(
            result_general,
            buff=0.19,
            color=REGION,
            corner_radius=0.05,
            stroke_width=2.7,
        )
        final_note = label("限定：同射線、第一次回到 O", 25, REGION, "BOLD")
        final_panel = VGroup(
            result5,
            result7,
            VGroup(final_box, result_general),
            final_note,
        ).arrange(DOWN, buff=0.54)
        final_panel.move_to([4.32, -0.10, 0])

        self.transition_title(self, stage_title, next_title)
        self.play(
            FadeOut(
                VGroup(
                    full_lines,
                    counter_origin_mark,
                    counter_segments,
                    counter_ticks,
                    counter_dots,
                    counter_angle,
                    negative_labels,
                    outside_banner,
                    counter_panel,
                )
            ),
            Create(final_rays),
            FadeIn(final_origin_mark),
            FadeIn(final_scope),
            run_time=0.86,
        )
        self.play(
            LaggedStart(*(Create(segment) for segment in final_segments), lag_ratio=0.07),
            LaggedStart(*(FadeIn(dot) for dot in final_dots), lag_ratio=0.07),
            run_time=1.00,
        )
        self.play(
            LaggedStart(*(Create(tick) for tick in final_ticks), lag_ratio=0.06),
            run_time=0.62,
        )

        self.next_beat("restate_scoped_results")
        self.play(FadeIn(result5), run_time=0.62)
        self.play(FadeIn(result7), run_time=0.68)
        self.play(FadeIn(result_general), Create(final_box), run_time=0.82)
        self.play(FadeIn(final_note), Indicate(final_scope, color=REGION), run_time=0.72)
        self.wait(0.60)
