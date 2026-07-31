"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q12."""

from __future__ import annotations

from math import cos, isclose, pi, radians, sin, sqrt, tan

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
    Circle,
    Create,
    DashedLine,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    RightAngle,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


SIDE_LENGTH = 1.0
APOTHEM = sqrt(3) / 2
EXPECTED_MINIMUM = 18 - 9 * sqrt(3)


def canonical_rotation(angle_degrees: float) -> float:
    """Reduce a hexagon rotation to the reflected half-period [0, 30]."""
    remainder = angle_degrees % 60.0
    return min(remainder, 60.0 - remainder)


def regular_hexagon_vertices(angle_degrees: float = 0.0) -> tuple[np.ndarray, ...]:
    """Return a unit-side regular hexagon centered at the origin."""
    return tuple(
        np.array([cos(radians(angle_degrees + 60 * index)),
                  sin(radians(angle_degrees + 60 * index)), 0.0])
        for index in range(6)
    )


def support_normal_angles(angle_degrees: float) -> tuple[float, ...]:
    """Return the distinct outward-normal angles of both hexagons."""
    values = [
        (30.0 + 60.0 * index + offset) % 360.0
        for offset in (0.0, angle_degrees % 60.0)
        for index in range(6)
    ]
    unique: list[float] = []
    for value in sorted(values):
        if not unique or not isclose(value, unique[-1], abs_tol=1e-9):
            unique.append(value)
    if len(unique) > 1 and isclose(unique[0] + 360.0, unique[-1], abs_tol=1e-9):
        unique.pop()
    return tuple(unique)


def tangent_intersection(first_degrees: float, second_degrees: float) -> np.ndarray:
    """Intersect two unit-hexagon support lines at distance APOTHEM."""
    normals = np.array(
        [
            [cos(radians(first_degrees)), sin(radians(first_degrees))],
            [cos(radians(second_degrees)), sin(radians(second_degrees))],
        ]
    )
    point = np.linalg.solve(normals, np.array([APOTHEM, APOTHEM]))
    return np.array([point[0], point[1], 0.0])


def overlap_vertices(angle_degrees: float) -> tuple[np.ndarray, ...]:
    """Return the intersection polygon from the two sets of support lines."""
    angles = support_normal_angles(angle_degrees)
    return tuple(
        tangent_intersection(first, second if second > first else second + 360.0)
        for first, second in zip(angles, angles[1:] + angles[:1], strict=True)
    )


def polygon_area(vertices: tuple[np.ndarray, ...]) -> float:
    return 0.5 * abs(
        sum(
            first[0] * second[1] - first[1] * second[0]
            for first, second in zip(vertices, vertices[1:] + vertices[:1], strict=True)
        )
    )


def overlap_area_formula(angle_degrees: float) -> float:
    """Area over one 60-degree period, including its degenerate endpoints."""
    remainder = angle_degrees % 60.0
    if isclose(remainder, 0.0, abs_tol=1e-12) and not isclose(
        angle_degrees, 0.0, abs_tol=1e-12
    ):
        remainder = 60.0
    return 6 * APOTHEM**2 * (
        tan(radians(remainder / 2.0))
        + tan(radians((60.0 - remainder) / 2.0))
    )


def normal_gap_sequence(angle_degrees: float) -> tuple[float, ...]:
    angles = support_normal_angles(angle_degrees)
    return tuple(
        (second - first) % 360.0
        for first, second in zip(angles, angles[1:] + angles[:1], strict=True)
    )


if not all(
    isclose(
        np.linalg.norm(second - first),
        SIDE_LENGTH,
        rel_tol=0.0,
        abs_tol=1e-12,
    )
    for first, second in zip(
        regular_hexagon_vertices(),
        regular_hexagon_vertices()[1:] + regular_hexagon_vertices()[:1],
        strict=True,
    )
):
    raise ValueError("the reference hexagon must have unit side length")
if len(overlap_vertices(0.0)) != 6 or len(overlap_vertices(30.0)) != 12:
    raise ValueError("the endpoint must have six sides and the half-period twelve")
for sample in (0.0, 4.0, 12.0, 21.0, 30.0, 39.0, 56.0, 60.0):
    if not isclose(
        polygon_area(overlap_vertices(sample)),
        overlap_area_formula(sample),
        rel_tol=0.0,
        abs_tol=1e-10,
    ):
        raise ValueError(f"support polygon and area formula disagree at {sample}")
if normal_gap_sequence(18.0) != (18.0, 42.0) * 6:
    raise ValueError("a generic overlap must alternate six short and six long gaps")
if any(
    not isclose(
        polygon_area(overlap_vertices(angle)),
        polygon_area(overlap_vertices(60.0 - angle)),
        rel_tol=0.0,
        abs_tol=1e-10,
    )
    for angle in (3.0, 11.0, 19.0, 27.0)
):
    raise ValueError("reflection across a fixed symmetry axis must preserve area")
area_samples = tuple(
    polygon_area(overlap_vertices(float(angle))) for angle in range(31)
)
if min(range(31), key=area_samples.__getitem__) != 30:
    raise ValueError("the overlap area must decrease through the reduced domain")
if not isclose(area_samples[-1], EXPECTED_MINIMUM, rel_tol=0.0, abs_tol=1e-10):
    raise ValueError("the half-period overlap must be 18-9*sqrt(3)")


class CarloTcfs112MathQ12(CarloSlide):
    """Discover the minimum overlap through support-line gap balancing."""

    lesson_id = "carlo.tcfs_112_math_gifted.q12"

    @staticmethod
    def stage_title(text: str, size: int = 30):
        title = label(text, size, INK, "BOLD")
        title.move_to([0, 3.10, 0])
        return title

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def map_point(point: np.ndarray, center: np.ndarray, scale: float) -> np.ndarray:
        return center + scale * point

    @classmethod
    def hexagon(
        cls,
        angle_degrees: float,
        center: np.ndarray,
        scale: float,
        color: str,
        *,
        fill_opacity: float = 0.04,
        stroke_width: float = 3.2,
    ) -> Polygon:
        return Polygon(
            *(cls.map_point(point, center, scale) for point in regular_hexagon_vertices(angle_degrees)),
            color=color,
            stroke_width=stroke_width,
            fill_color=color,
            fill_opacity=fill_opacity,
        )

    @classmethod
    def overlap(
        cls,
        angle_degrees: float,
        center: np.ndarray,
        scale: float,
        *,
        fill_opacity: float = 0.42,
        stroke_width: float = 2.5,
    ) -> Polygon:
        return Polygon(
            *(cls.map_point(point, center, scale) for point in overlap_vertices(angle_degrees)),
            color=REGION,
            stroke_width=stroke_width,
            fill_color=REGION,
            fill_opacity=fill_opacity,
        ).set_z_index(-2)

    @staticmethod
    def angle_readout(tracker: ValueTracker) -> VGroup:
        value = DecimalNumber(
            tracker.get_value(),
            num_decimal_places=0,
            font_size=46,
            color=POINT,
        )
        return VGroup(
            MathTex(r"\theta=", font_size=44, color=INK),
            value,
            MathTex(r"^\circ", font_size=39, color=POINT),
        ).arrange(RIGHT, buff=0.08)

    @classmethod
    def mini_overlap_diagram(
        cls,
        angle_degrees: float,
        center: np.ndarray,
        scale: float,
    ) -> VGroup:
        return VGroup(
            cls.overlap(angle_degrees, center, scale, fill_opacity=0.35, stroke_width=1.8),
            cls.hexagon(0.0, center, scale, POINT, fill_opacity=0.0, stroke_width=2.4),
            cls.hexagon(angle_degrees, center, scale, BLUE, fill_opacity=0.0, stroke_width=2.4),
            Dot(center, radius=0.045, color=INK),
        )

    @classmethod
    def support_spokes(
        cls,
        angle_degrees: float,
        center: np.ndarray,
        scale: float,
    ) -> VGroup:
        base_angles = {(30.0 + 60.0 * index) % 360.0 for index in range(6)}
        lines = []
        for angle in support_normal_angles(angle_degrees):
            unit = np.array([cos(radians(angle)), sin(radians(angle)), 0.0])
            color = POINT if any(isclose(angle, base, abs_tol=1e-9) for base in base_angles) else BLUE
            line = Line(
                center,
                center + scale * APOTHEM * unit,
                color=color,
                stroke_width=2.0,
            )
            lines.append(line)
        return VGroup(*lines)

    @classmethod
    def tangent_wedges(
        cls,
        angle_degrees: float,
        center: np.ndarray,
        scale: float,
    ) -> VGroup:
        angles = support_normal_angles(angle_degrees)
        wedges = []
        for index, (first, second) in enumerate(
            zip(angles, angles[1:] + angles[:1], strict=True)
        ):
            second_unwrapped = second if second > first else second + 360.0
            tangent_first = np.array(
                [APOTHEM * cos(radians(first)), APOTHEM * sin(radians(first)), 0.0]
            )
            tangent_second = np.array(
                [
                    APOTHEM * cos(radians(second_unwrapped)),
                    APOTHEM * sin(radians(second_unwrapped)),
                    0.0,
                ]
            )
            vertex = tangent_intersection(first, second_unwrapped)
            color = POINT if index % 2 == 0 else BLUE
            wedge = Polygon(
                center,
                cls.map_point(tangent_first, center, scale),
                cls.map_point(vertex, center, scale),
                cls.map_point(tangent_second, center, scale),
                color=color,
                stroke_width=1.0,
                fill_color=color,
                fill_opacity=0.22,
            ).set_z_index(-3)
            wedges.append(wedge)
        return VGroup(*wedges)

    @staticmethod
    def chip(text: str, color: str, width: float) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=0.72,
            corner_radius=0.06,
            color=color,
            stroke_width=2.2,
            fill_color=color,
            fill_opacity=0.10,
        )
        content = label(text, 23, color, "BOLD").move_to(frame)
        return VGroup(frame, content)

    def construct(self) -> None:
        heading = label("第 12 題｜旋轉中的重疊面積", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 12 頁｜影片 3clUyeUgvOg 00:00-08:23.75",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        diagram_center = np.array([-3.65, -0.35, 0.0])
        diagram_scale = 2.55

        # Beat 01 meet_unit_hexagon: establish the one concrete object and its unit side.
        self.begin_beat("meet_unit_hexagon")
        stage_title = self.stage_title("先固定一個邊長 1 的正六邊形")
        fixed_hex = self.hexagon(0.0, diagram_center, diagram_scale, POINT, fill_opacity=0.08)
        center_dot = Dot(diagram_center, radius=0.075, color=INK)
        center_name = MathTex("G", font_size=29, color=INK).next_to(center_dot, DOWN, buff=0.10)
        top_left = self.map_point(regular_hexagon_vertices()[1], diagram_center, diagram_scale)
        top_right = self.map_point(regular_hexagon_vertices()[2], diagram_center, diagram_scale)
        unit_edge = Line(top_left, top_right, color=POINT, stroke_width=6.0)
        unit_label = MathTex("1", font_size=36, color=POINT).next_to(unit_edge, UP, buff=0.13)
        opening_question = VGroup(
            label("繞中心旋轉時", 29, INK, "BOLD"),
            label("重疊面積何時最小？", 34, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.26).move_to([3.45, -0.15, 0])

        self.add(heading, source)
        self.play(FadeIn(stage_title), run_time=0.45)
        self.play(Create(fixed_hex), GrowFromCenter(center_dot), FadeIn(center_name), run_time=0.9)
        self.play(Create(unit_edge), FadeIn(unit_label), run_time=0.55)
        self.play(FadeIn(opening_question), run_time=0.65)
        self.wait(0.35)

        # Beat 02 rotate_to_half_period: watch the overlap shrink to the period midpoint.
        self.next_beat("rotate_to_half_period")
        next_title = self.stage_title("只轉動第二個六邊形")
        angle_tracker = ValueTracker(0.0)
        moving_hex = always_redraw(
            lambda: self.hexagon(
                angle_tracker.get_value(),
                diagram_center,
                diagram_scale,
                BLUE,
                fill_opacity=0.02,
            ).set_z_index(2)
        )
        moving_overlap = always_redraw(
            lambda: self.overlap(
                angle_tracker.get_value(), diagram_center, diagram_scale
            )
        )
        angle_display = always_redraw(
            lambda: self.angle_readout(angle_tracker).move_to([3.45, 0.55, 0])
        )
        overlap_note = label("綠色：兩個六邊形共有的部分", 23, REGION, "BOLD").move_to(
            [3.45, -0.45, 0]
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(opening_question, unit_edge, unit_label),
            run_time=0.55,
        )
        stage_title = next_title
        self.add(moving_overlap, moving_hex, angle_display)
        self.play(FadeIn(overlap_note), run_time=0.40)
        self.play(angle_tracker.animate.set_value(12.0), run_time=0.82)
        self.wait(0.18)
        self.play(angle_tracker.animate.set_value(30.0), run_time=0.82)
        self.wait(0.18)

        # Beat 03 rotate_and_watch_overlap: watch the overlap grow back to full coincidence.
        self.next_beat("rotate_and_watch_overlap")
        self.play(angle_tracker.animate.set_value(48.0), run_time=0.82)
        self.wait(0.18)
        self.play(angle_tracker.animate.set_value(60.0), run_time=0.82)
        self.wait(0.18)
        self.wait(0.25)

        # Beat 04 reflect_half_period: prove the 60-degree period and reflection reduction.
        self.next_beat("reflect_half_period")
        next_title = self.stage_title("一個週期，只需看前半段")
        left_center = np.array([-3.25, 0.10, 0.0])
        right_center = np.array([3.25, 0.10, 0.0])
        left_diagram = self.mini_overlap_diagram(18.0, left_center, 1.85)
        right_diagram = self.mini_overlap_diagram(42.0, right_center, 1.85)
        left_angle = MathTex(r"\theta=18^\circ", font_size=34, color=POINT).next_to(
            left_diagram, DOWN, buff=0.28
        )
        right_angle = MathTex(r"60^\circ-\theta=42^\circ", font_size=34, color=BLUE).next_to(
            right_diagram, DOWN, buff=0.28
        )
        period_formula = MathTex(
            r"A(\theta+60^\circ)=A(\theta)", font_size=37, color=INK
        ).move_to([0, 2.26, 0])
        reflection_formula = MathTex(
            r"A(\theta)=A(60^\circ-\theta)", font_size=37, color=REGION
        ).move_to([0, -2.30, 0])
        reduced_domain = MathTex(
            r"0^\circ\le\theta\le30^\circ", font_size=43, color=POINT
        ).move_to([0, -3.02, 0])
        mirror_axis = DashedLine([0, -1.65, 0], [0, 1.78, 0], color=HAIRLINE, stroke_width=2)

        frozen_dynamic = VGroup(
            self.overlap(60.0, diagram_center, diagram_scale),
            self.hexagon(60.0, diagram_center, diagram_scale, BLUE, fill_opacity=0.02),
        )
        self.remove(moving_overlap, moving_hex, angle_display)
        self.add(frozen_dynamic)
        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(fixed_hex, center_dot, center_name, frozen_dynamic, overlap_note),
            FadeIn(period_formula),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(FadeIn(left_diagram, left_angle), Create(mirror_axis), run_time=0.75)
        self.play(
            ReplacementTransform(left_diagram.copy(), right_diagram),
            FadeIn(right_angle),
            run_time=0.9,
        )

        # Beat 05 reduce_one_period_by_reflection: continue at a settled semantic boundary.
        self.next_beat("reduce_one_period_by_reflection")
        self.play(Write(reflection_formula), run_time=0.60)
        self.play(TransformFromCopy(reflection_formula, reduced_domain), run_time=0.65)
        self.wait(0.35)

        # Beat 06 construct_common_incircle: reveal the common incircle and earn the apothem.
        self.next_beat("construct_common_incircle")
        next_title = self.stage_title("所有邊都碰到同一個圓")
        generic_angle = 18.0
        generic_fixed = self.hexagon(0.0, diagram_center, diagram_scale, POINT, fill_opacity=0.0)
        generic_moving = self.hexagon(generic_angle, diagram_center, diagram_scale, BLUE, fill_opacity=0.0)
        generic_overlap = self.overlap(generic_angle, diagram_center, diagram_scale)
        incircle = Circle(
            radius=diagram_scale * APOTHEM,
            color=PURPLE,
            stroke_width=2.6,
        ).move_to(diagram_center)
        radius_angle = 90.0
        tangent_point = diagram_center + diagram_scale * APOTHEM * np.array(
            [cos(radians(radius_angle)), sin(radians(radius_angle)), 0.0]
        )
        radius_line = Line(diagram_center, tangent_point, color=PURPLE, stroke_width=3.3)
        radius_label = MathTex("r", font_size=34, color=PURPLE).next_to(
            radius_line, LEFT, buff=0.13
        )
        right_triangle = VGroup(
            Line([1.65, -1.30, 0], [5.55, -1.30, 0], color=HAIRLINE, stroke_width=2.5),
            Line([3.60, -1.30, 0], [3.60, 2.08, 0], color=PURPLE, stroke_width=3.0),
            Line([1.65, -1.30, 0], [3.60, 2.08, 0], color=POINT, stroke_width=3.0),
        )
        half_label = MathTex(r"\frac12", font_size=32, color=INK).move_to([2.63, -1.62, 0])
        one_label = MathTex("1", font_size=34, color=POINT).move_to([2.42, 0.58, 0])
        r_label = MathTex("r", font_size=34, color=PURPLE).move_to([3.89, 0.42, 0])
        right_mark = RightAngle(right_triangle[0], right_triangle[1], length=0.24, color=MUTED)
        r_derivation = VGroup(
            MathTex(r"r^2+\left(\frac12\right)^2=1", font_size=35, color=INK),
            MathTex(r"r=\frac{\sqrt3}{2}", font_size=45, color=PURPLE),
        ).arrange(DOWN, buff=0.27).move_to([5.05, 0.45, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                left_diagram,
                right_diagram,
                left_angle,
                right_angle,
                period_formula,
                reflection_formula,
                reduced_domain,
                mirror_axis,
            ),
            FadeIn(generic_overlap, generic_fixed, generic_moving),
            run_time=0.70,
        )
        stage_title = next_title
        self.play(Create(incircle), run_time=0.75)
        self.play(Create(radius_line), FadeIn(radius_label), run_time=0.50)
        self.play(Create(right_triangle), FadeIn(half_label, one_label, r_label, right_mark), run_time=0.75)

        # Beat 07 find_common_incircle: continue at a settled semantic boundary.
        self.next_beat("find_common_incircle")
        self.play(Write(r_derivation[0]), run_time=0.55)
        self.play(TransformFromCopy(r_derivation[0], r_derivation[1]), run_time=0.60)
        self.wait(0.35)

        # Beat 08 draw_alternating_normal_gaps: expose the alternating normal gaps that define the overlap.
        self.next_beat("draw_alternating_normal_gaps")
        next_title = self.stage_title("十二條邊，間隔一小一大")
        spokes = self.support_spokes(generic_angle, diagram_center, diagram_scale)
        arc_short = Arc(
            radius=0.62,
            start_angle=radians(30.0),
            angle=radians(generic_angle),
            arc_center=diagram_center,
            color=POINT,
            stroke_width=5.0,
        )
        arc_long = Arc(
            radius=0.88,
            start_angle=radians(30.0 + generic_angle),
            angle=radians(60.0 - generic_angle),
            arc_center=diagram_center,
            color=BLUE,
            stroke_width=5.0,
        )
        short_label = MathTex(r"\theta", font_size=31, color=POINT).move_to(
            diagram_center + np.array([0.72, 0.56, 0.0])
        )
        long_label = MathTex(r"60^\circ-\theta", font_size=27, color=BLUE).move_to(
            diagram_center + np.array([0.05, 1.17, 0.0])
        )
        gap_chips = VGroup(
            self.chip("6 個小間隔", POINT, 2.45),
            self.chip("6 個大間隔", BLUE, 2.45),
        ).arrange(DOWN, buff=0.30).move_to([3.85, 0.70, 0])
        gap_formula = VGroup(
            MathTex(r"6\times\theta", font_size=38, color=POINT),
            MathTex(r"6\times(60^\circ-\theta)", font_size=38, color=BLUE),
        ).arrange(DOWN, buff=0.36).move_to([3.85, -1.02, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(right_triangle, half_label, one_label, r_label, right_mark, r_derivation),
            run_time=0.55,
        )
        stage_title = next_title
        self.play(LaggedStart(*(Create(line) for line in spokes), lag_ratio=0.05), run_time=0.95)
        self.play(Create(arc_short), FadeIn(short_label), run_time=0.45)
        self.play(Create(arc_long), FadeIn(long_label), run_time=0.55)

        # Beat 09 read_alternating_normal_gaps: continue at a settled semantic boundary.
        self.next_beat("read_alternating_normal_gaps")
        self.play(LaggedStart(*(FadeIn(chip) for chip in gap_chips), lag_ratio=0.18), run_time=0.70)
        self.play(Write(gap_formula), run_time=0.75)
        self.wait(0.30)

        # Beat 10 balance_the_gaps: visually balance the two gap types at the half-period.
        self.next_beat("balance_the_gaps")
        next_title = self.stage_title("把一大一小，調成一樣")
        balanced_overlap = self.overlap(30.0, diagram_center, diagram_scale)
        balanced_moving = self.hexagon(30.0, diagram_center, diagram_scale, BLUE, fill_opacity=0.0)
        balanced_spokes = self.support_spokes(30.0, diagram_center, diagram_scale)
        equal_statement = MathTex(
            r"\theta=60^\circ-\theta=30^\circ",
            font_size=43,
            color=REGION,
        ).move_to([3.55, 0.65, 0])
        equal_chips = VGroup(
            self.chip("12 個相同間隔", REGION, 3.15),
            label("這時會最小嗎？", 28, INK, "BOLD"),
        ).arrange(DOWN, buff=0.40).move_to([3.55, -0.70, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(arc_short, arc_long, short_label, long_label, gap_chips, gap_formula),
            ReplacementTransform(generic_overlap, balanced_overlap),
            Transform(generic_moving, balanced_moving),
            ReplacementTransform(spokes, balanced_spokes),
            run_time=1.0,
        )
        stage_title = next_title
        generic_overlap = balanced_overlap
        spokes = balanced_spokes
        self.play(Write(equal_statement), run_time=0.65)
        self.play(FadeIn(equal_chips), run_time=0.65)
        self.wait(0.40)

        # Beat 11 construct_tangent_corner: isolate and calculate one tangent-corner contribution.
        self.next_beat("construct_tangent_corner")
        next_title = self.stage_title("先量一個相鄰切線形成的角落")
        wedge_origin = np.array([-3.50, -2.08, 0.0])
        wedge_radius = 2.30
        delta = 50.0
        first_normal = 90.0 - delta / 2.0
        second_normal = 90.0 + delta / 2.0
        t_first = wedge_origin + wedge_radius * np.array(
            [cos(radians(first_normal)), sin(radians(first_normal)), 0.0]
        )
        t_second = wedge_origin + wedge_radius * np.array(
            [cos(radians(second_normal)), sin(radians(second_normal)), 0.0]
        )
        unit_vertex = tangent_intersection(first_normal, second_normal)
        vertex = wedge_origin + wedge_radius / APOTHEM * unit_vertex
        corner_fill = Polygon(
            wedge_origin,
            t_first,
            vertex,
            t_second,
            color=REGION,
            stroke_width=2.0,
            fill_color=REGION,
            fill_opacity=0.24,
        )
        radius_first = Line(wedge_origin, t_first, color=PURPLE, stroke_width=3.0)
        radius_second = Line(wedge_origin, t_second, color=PURPLE, stroke_width=3.0)
        tangent_first = Line(t_first, vertex, color=POINT, stroke_width=4.0)
        tangent_second = Line(vertex, t_second, color=POINT, stroke_width=4.0)
        bisector = DashedLine(wedge_origin, vertex, color=MUTED, stroke_width=2.0)
        delta_arc = Arc(
            radius=0.68,
            start_angle=radians(first_normal),
            angle=radians(delta),
            arc_center=wedge_origin,
            color=REGION,
            stroke_width=4.5,
        )
        delta_label = MathTex(r"\delta", font_size=33, color=REGION).move_to(
            wedge_origin + np.array([0.0, 0.92, 0.0])
        )
        radius_mark = MathTex("r", font_size=32, color=PURPLE).move_to(
            (wedge_origin + t_first) / 2 + np.array([-0.22, 0.05, 0.0])
        )
        tangent_mark = MathTex(
            r"r\tan\frac{\delta}{2}", font_size=31, color=POINT
        ).move_to((t_first + vertex) / 2 + np.array([0.68, 0.08, 0.0]))
        right_angle = RightAngle(radius_first, tangent_first, length=0.22, color=MUTED)
        wedge_point_labels = VGroup(
            MathTex("G", font_size=27, color=INK).next_to(wedge_origin, DOWN, buff=0.08),
            MathTex("V", font_size=27, color=INK).next_to(vertex, UP, buff=0.10),
            MathTex("T_1", font_size=24, color=MUTED).next_to(t_first, RIGHT, buff=0.10),
            MathTex("T_2", font_size=24, color=MUTED).next_to(t_second, LEFT, buff=0.10),
        )
        wedge_formula = VGroup(
            MathTex(r"\angle T_1GV=\angle VGT_2=\frac{\delta}{2}", font_size=34, color=INK),
            MathTex(r"GT_1=GT_2=r", font_size=36, color=PURPLE),
            MathTex(
                r"2\left(\frac12\right)r\left(r\tan\frac{\delta}{2}\right)",
                font_size=39,
                color=INK,
            ),
            MathTex(r"=r^2\tan\frac{\delta}{2}", font_size=47, color=REGION),
        ).arrange(DOWN, buff=0.34).move_to([3.60, -0.15, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                generic_fixed,
                generic_moving,
                generic_overlap,
                incircle,
                radius_line,
                radius_label,
                spokes,
                equal_statement,
                equal_chips,
            ),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(FadeIn(corner_fill), Create(radius_first), Create(radius_second), run_time=0.65)
        self.play(Create(tangent_first), Create(tangent_second), Create(bisector), run_time=0.70)
        self.play(
            Create(delta_arc),
            FadeIn(delta_label, radius_mark, right_angle, wedge_point_labels),
            run_time=0.55,
        )

        # Beat 12 measure_one_tangent_corner: continue at a settled semantic boundary.
        self.next_beat("measure_one_tangent_corner")
        self.play(FadeIn(tangent_mark), Write(wedge_formula[0]), run_time=0.65)
        self.play(Write(wedge_formula[1]), Write(wedge_formula[2]), run_time=0.75)
        self.play(TransformFromCopy(wedge_formula[2], wedge_formula[3]), run_time=0.65)
        self.wait(0.35)

        # Beat 13 collect_small_overlap_wedges: tile the overlap with six corners of each gap type.
        self.next_beat("collect_small_overlap_wedges")
        next_title = self.stage_title("十二個角落，拼回整個重疊區")
        generic_overlap = self.overlap(generic_angle, diagram_center, diagram_scale, fill_opacity=0.08)
        generic_fixed = self.hexagon(0.0, diagram_center, diagram_scale, POINT, fill_opacity=0.0)
        generic_moving = self.hexagon(generic_angle, diagram_center, diagram_scale, BLUE, fill_opacity=0.0)
        wedges = self.tangent_wedges(generic_angle, diagram_center, diagram_scale)
        area_term_small = MathTex(
            r"6r^2\tan\frac{\theta}{2}", font_size=39, color=POINT
        ).move_to([3.60, 0.78, 0])
        plus_sign = MathTex("+", font_size=42, color=INK).move_to([3.60, 0.05, 0])
        area_term_large = MathTex(
            r"6r^2\tan\frac{60^\circ-\theta}{2}", font_size=39, color=BLUE
        ).move_to([3.60, -0.70, 0])
        area_formula = MathTex(
            r"A(\theta)=6r^2\left(\tan\frac{\theta}{2}+"
            r"\tan\frac{60^\circ-\theta}{2}\right)",
            font_size=37,
            color=REGION,
        ).move_to([3.60, -1.75, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                corner_fill,
                radius_first,
                radius_second,
                tangent_first,
                tangent_second,
                bisector,
                delta_arc,
                delta_label,
                radius_mark,
                tangent_mark,
                right_angle,
                wedge_point_labels,
                wedge_formula,
            ),
            FadeIn(generic_overlap, generic_fixed, generic_moving),
            run_time=0.70,
        )
        stage_title = next_title
        self.play(LaggedStart(*(FadeIn(wedge) for wedge in wedges), lag_ratio=0.055), run_time=1.0)
        self.play(
            Indicate(VGroup(*wedges[::2]), color=POINT, scale_factor=1.015),
            run_time=0.45,
        )
        self.play(FadeIn(area_term_small, shift=RIGHT * 0.10), run_time=0.45)

        # Beat 14 assemble_overlap_area: continue at a settled semantic boundary.
        self.next_beat("assemble_overlap_area")
        self.play(
            Indicate(VGroup(*wedges[1::2]), color=BLUE, scale_factor=1.015),
            run_time=0.45,
        )
        self.play(
            Write(plus_sign),
            FadeIn(area_term_large, shift=RIGHT * 0.10),
            run_time=0.55,
        )
        self.play(
            FadeOut(area_term_small, plus_sign, area_term_large),
            FadeIn(area_formula, shift=UP * 0.10),
            run_time=0.65,
        )
        self.wait(0.35)

        # Beat 15 derive_equal_gap_bound: prove, without guessing, that equal gaps minimize the sum.
        self.next_beat("derive_equal_gap_bound")
        next_title = self.stage_title("固定總角度時，兩個間隔越平均越小")
        angle_origin = np.array([-3.55, -1.48, 0.0])
        angle_radius = 2.35
        start_angle = 60.0
        split_angle = 69.0
        end_angle = 90.0
        start_ray = Line(
            angle_origin,
            angle_origin + angle_radius * np.array([cos(radians(start_angle)), sin(radians(start_angle)), 0.0]),
            color=POINT,
            stroke_width=3.4,
        )
        split_ray = Line(
            angle_origin,
            angle_origin + angle_radius * np.array([cos(radians(split_angle)), sin(radians(split_angle)), 0.0]),
            color=INK,
            stroke_width=3.0,
        )
        end_ray = Line(
            angle_origin,
            angle_origin + angle_radius * np.array([cos(radians(end_angle)), sin(radians(end_angle)), 0.0]),
            color=BLUE,
            stroke_width=3.4,
        )
        x_arc = Arc(
            radius=0.78,
            start_angle=radians(start_angle),
            angle=radians(split_angle - start_angle),
            arc_center=angle_origin,
            color=POINT,
            stroke_width=5.0,
        )
        y_arc = Arc(
            radius=1.02,
            start_angle=radians(split_angle),
            angle=radians(end_angle - split_angle),
            arc_center=angle_origin,
            color=BLUE,
            stroke_width=5.0,
        )
        x_label = MathTex("x", font_size=32, color=POINT).move_to([-2.98, -0.60, 0])
        y_label = MathTex("y", font_size=32, color=BLUE).move_to([-3.48, -0.24, 0])
        fixed_sum = MathTex(r"x+y=30^\circ", font_size=39, color=INK).move_to(
            [-3.15, 1.48, 0]
        )
        equality_ray = Line(
            angle_origin,
            angle_origin + angle_radius * np.array([cos(radians(75.0)), sin(radians(75.0)), 0.0]),
            color=REGION,
            stroke_width=4.2,
        )
        equality_condition = VGroup(
            label("等號成立", 23, POINT, "BOLD"),
            MathTex(
                r"\Longleftrightarrow\quad x=y=15^\circ,\quad\theta=30^\circ",
                font_size=38,
                color=POINT,
            ),
        ).arrange(RIGHT, buff=0.18)
        proof_lines = VGroup(
            MathTex(
                r"\tan x+\tan y=\frac{\sin(x+y)}{\cos x\cos y}"
                r"=\frac{1}{2\cos x\cos y}",
                font_size=35,
                color=INK,
            ),
            MathTex(
                r"2\cos x\cos y=\frac{\sqrt3}{2}+\cos(x-y)",
                font_size=36,
                color=PURPLE,
            ),
            MathTex(
                r"2\cos x\cos y\le\frac{\sqrt3}{2}+1",
                font_size=36,
                color=REGION,
            ),
            equality_condition,
        ).arrange(DOWN, buff=0.36).move_to([3.35, -0.32, 0])
        minimum_note = label("分母最大，面積才最小", 23, REGION, "BOLD").next_to(
            proof_lines, DOWN, buff=0.18
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(generic_overlap, generic_fixed, generic_moving, wedges),
            area_formula.animate.scale(0.73).move_to([3.30, 2.22, 0]),
            FadeIn(start_ray, split_ray, end_ray, x_arc, y_arc, x_label, y_label, fixed_sum),
            run_time=0.75,
        )
        stage_title = next_title
        self.play(Write(proof_lines[0]), run_time=0.72)
        self.play(Write(proof_lines[1]), run_time=0.65)
        self.play(Write(proof_lines[2]), FadeIn(minimum_note), run_time=0.70)

        # Beat 16 prove_equal_gaps_minimize: continue at a settled semantic boundary.
        self.next_beat("prove_equal_gaps_minimize")
        self.play(
            Transform(split_ray, equality_ray),
            FadeOut(x_arc, y_arc, x_label, y_label),
            run_time=0.65,
        )
        self.play(FadeIn(proof_lines[3]), run_time=0.55)
        self.wait(0.35)

        # Beat 17 substitute_equal_half_period: substitute the half-period and the earned apothem.
        self.next_beat("substitute_equal_half_period")
        next_title = self.stage_title("回到十二個完全相同的角落")
        min_center = np.array([-3.65, -0.40, 0.0])
        min_scale = 2.45
        min_overlap = self.overlap(30.0, min_center, min_scale, fill_opacity=0.12)
        min_fixed = self.hexagon(0.0, min_center, min_scale, POINT, fill_opacity=0.0)
        min_moving = self.hexagon(30.0, min_center, min_scale, BLUE, fill_opacity=0.0)
        min_wedges = self.tangent_wedges(30.0, min_center, min_scale)
        substitution = VGroup(
            MathTex(r"r=\frac{\sqrt3}{2}\quad\Longrightarrow\quad r^2=\frac34", font_size=39, color=PURPLE),
            MathTex(r"A_{\min}=6r^2(\tan15^\circ+\tan15^\circ)", font_size=37, color=INK),
            MathTex(r"=12\left(\frac34\right)\tan15^\circ", font_size=41, color=INK),
            MathTex(r"=9\tan15^\circ", font_size=49, color=REGION),
        ).arrange(DOWN, buff=0.36).move_to([3.55, -0.20, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                area_formula,
                start_ray,
                split_ray,
                end_ray,
                fixed_sum,
                proof_lines,
                minimum_note,
            ),
            FadeIn(min_overlap, min_fixed, min_moving),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(LaggedStart(*(FadeIn(wedge) for wedge in min_wedges), lag_ratio=0.04), run_time=0.85)
        self.play(Write(substitution[0]), run_time=0.55)
        self.play(Write(substitution[1]), run_time=0.65)

        # Beat 18 substitute_half_period: continue at a settled semantic boundary.
        self.next_beat("substitute_half_period")
        self.play(TransformFromCopy(substitution[1], substitution[2]), run_time=0.60)
        self.play(TransformFromCopy(substitution[2], substitution[3]), run_time=0.55)
        self.wait(0.35)

        # Beat 19 construct_fifteen_degree_difference: calculate tan(15 degrees) only after the angle is visible.
        self.next_beat("construct_fifteen_degree_difference")
        next_title = self.stage_title("最後只差十五度的正切值")
        angle_origin = np.array([-4.55, -1.70, 0.0])
        ray_length = 3.15
        base_ray = Line(angle_origin, angle_origin + RIGHT * ray_length, color=HAIRLINE, stroke_width=2.5)
        ray_30 = Line(
            angle_origin,
            angle_origin + ray_length * np.array([cos(pi / 6), sin(pi / 6), 0.0]),
            color=BLUE,
            stroke_width=3.4,
        )
        ray_45 = Line(
            angle_origin,
            angle_origin + ray_length * np.array([cos(pi / 4), sin(pi / 4), 0.0]),
            color=POINT,
            stroke_width=3.4,
        )
        arc_30 = Arc(
            radius=0.82,
            start_angle=0,
            angle=pi / 6,
            arc_center=angle_origin,
            color=BLUE,
            stroke_width=4.5,
        )
        arc_15 = Arc(
            radius=1.12,
            start_angle=pi / 6,
            angle=pi / 12,
            arc_center=angle_origin,
            color=REGION,
            stroke_width=5.0,
        )
        angle_labels = VGroup(
            MathTex(r"30^\circ", font_size=31, color=BLUE).move_to([-2.84, -1.08, 0]),
            MathTex(r"15^\circ", font_size=31, color=REGION).move_to([-3.42, -0.44, 0]),
            MathTex(r"45^\circ", font_size=31, color=POINT).move_to([-2.10, 0.56, 0]),
        )
        tangent_derivation = VGroup(
            MathTex(r"15^\circ=45^\circ-30^\circ", font_size=39, color=INK),
            MathTex(
                r"\tan15^\circ=\frac{\tan45^\circ-\tan30^\circ}"
                r"{1+\tan45^\circ\tan30^\circ}",
                font_size=36,
                color=INK,
            ),
            MathTex(
                r"=\frac{1-1/\sqrt3}{1+1/\sqrt3}", font_size=40, color=PURPLE
            ),
            MathTex(r"=2-\sqrt3", font_size=51, color=REGION),
        ).arrange(DOWN, buff=0.34).move_to([3.35, -0.10, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(min_overlap, min_fixed, min_moving, min_wedges, substitution[:3]),
            substitution[3].animate.move_to([-3.55, 1.55, 0]),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Create(base_ray), Create(ray_30), Create(ray_45), run_time=0.65)
        self.play(Create(arc_30), Create(arc_15), FadeIn(angle_labels), run_time=0.60)

        # Beat 20 calculate_tan_fifteen: continue at a settled semantic boundary.
        self.next_beat("calculate_tan_fifteen")
        self.play(Write(tangent_derivation[0]), run_time=0.45)
        self.play(Write(tangent_derivation[1]), run_time=0.70)
        self.play(Write(tangent_derivation[2]), run_time=0.55)
        self.play(TransformFromCopy(tangent_derivation[2], tangent_derivation[3]), run_time=0.60)
        self.wait(0.35)

        # Beat 21 hold_before_expansion: settle immediately before expanding the exact answer.
        self.next_beat("hold_before_expansion")
        next_title = self.stage_title("所有幾何都已經回到同一行")
        hold_center = np.array([-3.45, -0.35, 0.0])
        hold_overlap = self.overlap(30.0, hold_center, 2.30, fill_opacity=0.38)
        hold_fixed = self.hexagon(0.0, hold_center, 2.30, POINT, fill_opacity=0.0)
        hold_moving = self.hexagon(30.0, hold_center, 2.30, BLUE, fill_opacity=0.0)
        theta_tag = MathTex(r"\theta=30^\circ", font_size=37, color=POINT).next_to(
            hold_overlap, DOWN, buff=0.25
        )
        hold_formula = MathTex(
            r"A_{\min}=9(2-\sqrt3)=\ ?",
            font_size=55,
            color=INK,
        ).move_to([3.50, 0.10, 0])
        hold_box = SurroundingRectangle(
            hold_formula,
            color=REGION,
            buff=0.28,
            stroke_width=2.6,
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(
                substitution[3],
                base_ray,
                ray_30,
                ray_45,
                arc_30,
                arc_15,
                angle_labels,
                tangent_derivation,
            ),
            FadeIn(hold_overlap, hold_fixed, hold_moving, theta_tag),
            run_time=0.65,
        )
        stage_title = next_title
        self.play(Write(hold_formula), Create(hold_box), run_time=0.85)
        self.wait(0.80)

        # Beat 22 reveal_minimum_overlap: expand the answer and reconnect it to the rotation.
        self.next_beat("reveal_minimum_overlap")
        next_title = self.stage_title("每個週期的中點，重疊面積最小")
        final_formula = MathTex(
            r"A_{\min}=18-9\sqrt3",
            font_size=61,
            color=REGION,
        ).move_to([3.50, 0.35, 0])
        final_box = SurroundingRectangle(
            final_formula,
            color=POINT,
            buff=0.31,
            stroke_width=3.2,
        )
        route = VGroup(
            MathTex(r"0^\circ\longrightarrow30^\circ\longrightarrow60^\circ", font_size=38, color=INK),
            label("重合　　最小　　重合", 22, MUTED, "BOLD"),
        ).arrange(DOWN, buff=0.16).move_to([3.50, -1.10, 0])
        final_note = label("六十度週期；反射後只需檢查前半段", 22, PURPLE, "BOLD").move_to(
            [3.50, -2.10, 0]
        )

        self.play(self.title_change(stage_title, next_title), run_time=0.45)
        stage_title = next_title
        self.play(FadeOut(hold_formula, hold_box), run_time=0.28)
        self.play(Write(final_formula), Create(final_box), run_time=0.82)

        # Beat 23 reveal_and_return_to_rotation: continue at a settled semantic boundary.
        self.next_beat("reveal_and_return_to_rotation")
        self.play(Indicate(hold_overlap, color=REGION, scale_factor=1.04), run_time=0.55)
        self.play(FadeIn(route), run_time=0.65)
        self.play(FadeIn(final_note), run_time=0.50)
        self.wait(0.65)
