"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q10."""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from math import isqrt, sqrt

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
    Brace,
    BraceBetweenPoints,
    Create,
    DashedLine,
    Dot,
    DoubleArrow,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ExactPoint = tuple[Fraction, Fraction]


def triangle_vertices(index: int) -> tuple[ExactPoint, ExactPoint, ExactPoint]:
    """Return x and y/sqrt(3) coordinates for the indexed unit triangle."""
    if index < 0:
        raise ValueError("triangle indices must be nonnegative")
    shift = Fraction(index, 2)
    return (
        (shift, Fraction(0)),
        (shift + 1, Fraction(0)),
        (shift + Fraction(1, 2), Fraction(1, 2)),
    )


def overlap_vertices(index: int) -> tuple[ExactPoint, ExactPoint, ExactPoint]:
    """Return the overlap of triangles index and index+1."""
    shift = Fraction(index, 2)
    return (
        (shift + Fraction(1, 2), Fraction(0)),
        (shift + 1, Fraction(0)),
        (shift + Fraction(3, 4), Fraction(1, 4)),
    )


def union_boundary_vertices(count: int) -> tuple[ExactPoint, ...]:
    """Trace the exact clockwise boundary of the translated triangle union."""
    if count < 1:
        raise ValueError("at least one triangle is required")
    vertices: list[ExactPoint] = [
        (Fraction(0), Fraction(0)),
        (Fraction(1, 2), Fraction(1, 2)),
    ]
    for index in range(count - 1):
        vertices.extend(
            (
                (Fraction(2 * index + 3, 4), Fraction(1, 4)),
                (Fraction(index + 2, 2), Fraction(1, 2)),
            )
        )
    vertices.append((Fraction(count + 1, 2), Fraction(0)))
    return tuple(vertices)


def cross(origin: ExactPoint, first: ExactPoint, second: ExactPoint) -> Fraction:
    return (first[0] - origin[0]) * (second[1] - origin[1]) - (
        first[1] - origin[1]
    ) * (second[0] - origin[0])


def line_intersection(
    start: ExactPoint,
    end: ExactPoint,
    clip_start: ExactPoint,
    clip_end: ExactPoint,
) -> ExactPoint:
    """Intersect a segment line with a clip-edge line using exact arithmetic."""
    segment = (end[0] - start[0], end[1] - start[1])
    clip = (clip_end[0] - clip_start[0], clip_end[1] - clip_start[1])
    denominator = segment[0] * clip[1] - segment[1] * clip[0]
    if denominator == 0:
        raise ValueError("parallel lines do not have a unique intersection")
    offset = (clip_start[0] - start[0], clip_start[1] - start[1])
    parameter = (offset[0] * clip[1] - offset[1] * clip[0]) / denominator
    return (
        start[0] + parameter * segment[0],
        start[1] + parameter * segment[1],
    )


def convex_intersection(
    subject: tuple[ExactPoint, ...],
    clipper: tuple[ExactPoint, ...],
) -> tuple[ExactPoint, ...]:
    """Clip one counterclockwise convex polygon by another exactly."""
    output = list(subject)
    for clip_start, clip_end in zip(clipper, clipper[1:] + clipper[:1], strict=True):
        if not output:
            break
        incoming = output
        output = []
        previous = incoming[-1]
        previous_inside = cross(clip_start, clip_end, previous) >= 0
        for current in incoming:
            current_inside = cross(clip_start, clip_end, current) >= 0
            if current_inside != previous_inside:
                output.append(
                    line_intersection(previous, current, clip_start, clip_end)
                )
            if current_inside:
                output.append(current)
            previous = current
            previous_inside = current_inside

        deduplicated: list[ExactPoint] = []
        for point in output:
            if not deduplicated or point != deduplicated[-1]:
                deduplicated.append(point)
        if len(deduplicated) > 1 and deduplicated[0] == deduplicated[-1]:
            deduplicated.pop()
        output = deduplicated
    return tuple(output)


def polygon_area_sqrt3_coefficient(vertices: tuple[ExactPoint, ...]) -> Fraction:
    """Return c exactly when the polygon area is c*sqrt(3)."""
    if len(vertices) < 3:
        return Fraction(0)
    twice_coefficient = sum(
        first[0] * second[1] - second[0] * first[1]
        for first, second in zip(vertices, vertices[1:] + vertices[:1], strict=True)
    )
    return abs(twice_coefficient) / 2


def exact_edge_length(first: ExactPoint, second: ExactPoint) -> Fraction:
    """Return an exact rational edge length in the unscaled Euclidean plane."""
    dx = second[0] - first[0]
    dy_coefficient = second[1] - first[1]
    squared = dx * dx + 3 * dy_coefficient * dy_coefficient
    numerator_root = isqrt(squared.numerator)
    denominator_root = isqrt(squared.denominator)
    if (
        numerator_root * numerator_root != squared.numerator
        or denominator_root * denominator_root != squared.denominator
    ):
        raise ValueError(f"edge length is not rational: {squared}")
    return Fraction(numerator_root, denominator_root)


def polygon_perimeter(vertices: tuple[ExactPoint, ...]) -> Fraction:
    return sum(
        (
            exact_edge_length(first, second)
            for first, second in zip(
                vertices, vertices[1:] + vertices[:1], strict=True
            )
        ),
        start=Fraction(0),
    )


SINGLE_TRIANGLE_AREA = Fraction(1, 4)
ADJACENT_OVERLAP_AREA = Fraction(1, 16)
TARGET_COUNT = 112
TARGET_PERIMETER = Fraction(3 * (TARGET_COUNT + 1), 2)
TARGET_AREA_COEFFICIENT = Fraction(3 * TARGET_COUNT + 1, 16)


if tuple(
    (
        triangle_vertices(index + 1)[vertex][0]
        - triangle_vertices(index)[vertex][0],
        triangle_vertices(index + 1)[vertex][1]
        - triangle_vertices(index)[vertex][1],
    )
    for index in range(4)
    for vertex in range(3)
) != ((Fraction(1, 2), Fraction(0)),) * 12:
    raise ValueError("successive triangles must translate horizontally by exactly 1/2")

for first_index in range(5):
    for second_index in range(first_index, 5):
        intersection = convex_intersection(
            triangle_vertices(first_index), triangle_vertices(second_index)
        )
        expected_area = (
            SINGLE_TRIANGLE_AREA
            if first_index == second_index
            else ADJACENT_OVERLAP_AREA
            if second_index == first_index + 1
            else Fraction(0)
        )
        if polygon_area_sqrt3_coefficient(intersection) != expected_area:
            raise ValueError("the exact pairwise triangle-intersection audit failed")

for indices in combinations(range(6), 3):
    common = convex_intersection(
        convex_intersection(
            triangle_vertices(indices[0]), triangle_vertices(indices[1])
        ),
        triangle_vertices(indices[2]),
    )
    if polygon_area_sqrt3_coefficient(common) != 0:
        raise ValueError("three distinct triangles cannot share positive area")

SMALL_CASE_AUDIT = tuple(
    (
        count,
        polygon_perimeter(union_boundary_vertices(count)),
        polygon_area_sqrt3_coefficient(union_boundary_vertices(count)),
    )
    for count in range(1, 4)
)
if SMALL_CASE_AUDIT != (
    (1, Fraction(3), Fraction(1, 4)),
    (2, Fraction(9, 2), Fraction(7, 16)),
    (3, Fraction(6), Fraction(5, 8)),
):
    raise ValueError("the n=1,2,3 exact union polygons changed")
if any(
    polygon_area_sqrt3_coefficient(union_boundary_vertices(count))
    != count * SINGLE_TRIANGLE_AREA - (count - 1) * ADJACENT_OVERLAP_AREA
    for count in range(1, 9)
):
    raise ValueError("polygon areas disagree with adjacent-overlap inclusion-exclusion")
if TARGET_PERIMETER != Fraction(339, 2):
    raise ValueError("the target perimeter must be 339/2")
if TARGET_AREA_COEFFICIENT != Fraction(337, 16):
    raise ValueError("the target area must be 337*sqrt(3)/16")


class CarloTcfs112MathQ10(CarloSlide):
    """Build the translated triangle union before counting its edge and area."""

    lesson_id = "carlo.tcfs_112_math_gifted.q10"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def stage_title(text: str, size: int = 31):
        title = label(text, size, INK, "BOLD")
        title.move_to([0, 3.05, 0])
        return title

    @staticmethod
    def screen_point(
        point: ExactPoint,
        origin: np.ndarray,
        scale: float,
    ) -> np.ndarray:
        return origin + np.array(
            [scale * float(point[0]), scale * sqrt(3) * float(point[1]), 0.0]
        )

    @classmethod
    def triangle(
        cls,
        index: int,
        origin: np.ndarray,
        scale: float,
        color: str = BLUE,
        *,
        fill_opacity: float = 0.08,
        stroke_width: float = 2.8,
    ) -> Polygon:
        return Polygon(
            *(
                cls.screen_point(point, origin, scale)
                for point in triangle_vertices(index)
            ),
            color=color,
            stroke_width=stroke_width,
            fill_color=color,
            fill_opacity=fill_opacity,
        )

    @classmethod
    def overlap(
        cls,
        index: int,
        origin: np.ndarray,
        scale: float,
        *,
        fill_opacity: float = 0.40,
    ) -> Polygon:
        return Polygon(
            *(
                cls.screen_point(point, origin, scale)
                for point in overlap_vertices(index)
            ),
            color=PURPLE,
            stroke_width=3.0,
            fill_color=PURPLE,
            fill_opacity=fill_opacity,
        )

    @classmethod
    def boundary(
        cls,
        count: int,
        origin: np.ndarray,
        scale: float,
        color: str = CORAL,
        *,
        fill_color: str = REGION,
        fill_opacity: float = 0.04,
        stroke_width: float = 4.2,
    ) -> Polygon:
        return Polygon(
            *(
                cls.screen_point(point, origin, scale)
                for point in union_boundary_vertices(count)
            ),
            color=color,
            stroke_width=stroke_width,
            fill_color=fill_color,
            fill_opacity=fill_opacity,
        )

    @classmethod
    def union_diagram(
        cls,
        count: int,
        origin: np.ndarray,
        scale: float,
        *,
        boundary_color: str = CORAL,
        area_opacity: float = 0.08,
    ) -> VGroup:
        triangles = VGroup(
            *(
                cls.triangle(
                    index,
                    origin,
                    scale,
                    MUTED,
                    fill_opacity=0.025,
                    stroke_width=1.5,
                )
                for index in range(count)
            )
        )
        outline = cls.boundary(
            count,
            origin,
            scale,
            boundary_color,
            fill_opacity=area_opacity,
            stroke_width=3.6,
        )
        return VGroup(triangles, outline)

    @staticmethod
    def formula_card(expression: str, color: str, width: float = 6.1) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=1.55,
            corner_radius=0.07,
            color=color,
            stroke_width=2.8,
            fill_color=color,
            fill_opacity=0.08,
        )
        formula = MathTex(expression, font_size=43, color=color).move_to(frame)
        return VGroup(frame, formula)

    def construct(self) -> None:
        heading = label("第 10 題｜半格平移的正三角形", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 10 頁｜影片 W9yrKSMoY-0 00:00-03:39.10",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: establish one concrete unit triangle.
        self.begin_beat("meet_one_unit_triangle")
        title = self.stage_title("先只看一個邊長為 1 的正三角形")
        origin_1 = np.array([-1.70, -1.45, 0.0])
        scale_1 = 3.40
        triangle_1 = self.triangle(0, origin_1, scale_1, BLUE, fill_opacity=0.11)
        base_1 = Line(
            self.screen_point((Fraction(0), Fraction(0)), origin_1, scale_1),
            self.screen_point((Fraction(1), Fraction(0)), origin_1, scale_1),
        )
        base_brace = Brace(base_1, DOWN, color=BLUE, buff=0.12)
        base_label = MathTex("1", font_size=34, color=BLUE).next_to(
            base_brace, DOWN, buff=0.10
        )
        n_one = MathTex("n=1", font_size=38, color=POINT).move_to([0, 2.02, 0])
        first_prompt = label("下一個三角形，要從哪裡開始？", 27, CORAL, "BOLD")
        first_prompt.move_to([0, -2.72, 0])
        beat_1 = VGroup(triangle_1, base_brace, base_label, n_one, first_prompt)
        self.add(heading, source)
        self.play(FadeIn(title), run_time=0.50)
        self.play(Create(triangle_1), FadeIn(n_one), run_time=0.80)
        self.play(Create(base_brace), FadeIn(base_label), run_time=0.55)
        self.play(FadeIn(first_prompt), run_time=0.48)
        self.wait(0.40)

        # Beat 02: physically translate the same triangle by half a side.
        self.next_beat("slide_the_second_half_side")
        new_title = self.stage_title("第二個三角形只向右移動半個邊長")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_1),
            run_time=0.68,
        )
        title = new_title
        origin_2 = np.array([-2.25, -1.30, 0.0])
        scale_2 = 3.00
        fixed_triangle = self.triangle(0, origin_2, scale_2, BLUE, fill_opacity=0.08)
        moving_triangle = self.triangle(0, origin_2, scale_2, POINT, fill_opacity=0.10)
        shift_y = -2.15
        shift_arrow = DoubleArrow(
            [origin_2[0], shift_y, 0],
            [origin_2[0] + scale_2 / 2, shift_y, 0],
            color=POINT,
            stroke_width=2.8,
            tip_length=0.15,
        )
        shift_label = MathTex(r"\frac12", font_size=34, color=POINT).next_to(
            shift_arrow, DOWN, buff=0.10
        )
        overlap_2 = self.overlap(0, origin_2, scale_2)
        half_note = label("起點平移 1/2，所以兩個三角形會重疊", 26, PURPLE, "BOLD")
        half_note.move_to([0, -2.90, 0])
        beat_2 = VGroup(
            fixed_triangle,
            moving_triangle,
            shift_arrow,
            shift_label,
            overlap_2,
            half_note,
        )
        self.play(Create(fixed_triangle), FadeIn(moving_triangle), run_time=0.62)
        self.play(
            moving_triangle.animate.shift(RIGHT * scale_2 / 2),
            Create(shift_arrow),
            FadeIn(shift_label),
            run_time=1.05,
        )
        self.play(FadeIn(overlap_2), run_time=0.55)
        self.play(FadeIn(half_note), run_time=0.48)
        self.wait(0.42)

        # Beat 03: repeat the same move once, then trace only the union boundary.
        self.next_beat("add_the_third_and_trace")
        new_title = self.stage_title("第三個也移半格；最後描的是聯集的外輪廓")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_2),
            run_time=0.70,
        )
        title = new_title
        origin_3 = np.array([-3.00, -1.35, 0.0])
        scale_3 = 3.00
        first_three = self.triangle(0, origin_3, scale_3, BLUE, fill_opacity=0.06)
        second_three = self.triangle(1, origin_3, scale_3, BLUE, fill_opacity=0.06)
        third_three = self.triangle(1, origin_3, scale_3, POINT, fill_opacity=0.10)
        count_path = VGroup(
            MathTex("n=1", font_size=29, color=MUTED),
            MathTex(r"\longrightarrow n=2", font_size=29, color=MUTED),
            MathTex(r"\longrightarrow n=3", font_size=29, color=POINT),
        ).arrange(RIGHT, buff=0.24).move_to([0, 2.18, 0])
        outline_3 = self.boundary(3, origin_3, scale_3, CORAL, fill_opacity=0.05)
        boundary_note = label("內部原邊淡出；珊瑚色才是要量的輪廓", 25, CORAL, "BOLD")
        boundary_note.move_to([0, -2.72, 0])
        beat_3 = VGroup(first_three, second_three, third_three, count_path, outline_3, boundary_note)
        self.play(Create(first_three), Create(second_three), FadeIn(count_path[:2]), run_time=0.74)
        self.play(FadeIn(third_three), run_time=0.35)
        self.play(third_three.animate.shift(RIGHT * scale_3 / 2), FadeIn(count_path[2]), run_time=0.92)
        self.play(
            first_three.animate.set_opacity(0.30),
            second_three.animate.set_opacity(0.30),
            third_three.animate.set_opacity(0.30),
            Create(outline_3),
            run_time=1.05,
        )
        self.play(FadeIn(boundary_note), run_time=0.48)
        self.wait(0.42)

        # Beat 04: compare one addition and measure its net boundary change.
        self.next_beat("measure_one_perimeter_increment")
        new_title = self.stage_title("加一個三角形，底邊與斜邊分開看")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_3),
            run_time=0.70,
        )
        title = new_title
        scale_4 = 2.35
        origin_old = np.array([-6.05, -1.15, 0.0])
        origin_new = np.array([0.25, -1.15, 0.0])
        old_union = self.union_diagram(2, origin_old, scale_4, boundary_color=MUTED)
        new_union = self.union_diagram(3, origin_new, scale_4, boundary_color=MUTED)
        old_name = MathTex("n=2", font_size=33, color=MUTED).move_to([-4.28, 1.55, 0])
        new_name = MathTex("n=3", font_size=33, color=POINT).move_to([2.60, 1.55, 0])
        old_apex = self.screen_point((Fraction(1), Fraction(1, 2)), origin_old, scale_4)
        old_right = self.screen_point((Fraction(3, 2), Fraction(0)), origin_old, scale_4)
        old_last_side = DashedLine(old_apex, old_right, color=CORAL, stroke_width=4.0)
        old_side_text = MathTex("1", font_size=31, color=CORAL).next_to(
            old_last_side, RIGHT, buff=0.08
        )
        replacement_exact = (
            (Fraction(1), Fraction(1, 2)),
            (Fraction(5, 4), Fraction(1, 4)),
            (Fraction(3, 2), Fraction(1, 2)),
            (Fraction(2), Fraction(0)),
        )
        replacement = VGroup(
            *(
                Line(
                    self.screen_point(first, origin_new, scale_4),
                    self.screen_point(second, origin_new, scale_4),
                    color=CORAL,
                    stroke_width=5.0,
                )
                for first, second in zip(
                    replacement_exact[:-1], replacement_exact[1:], strict=True
                )
            )
        )
        bottom_extension = Line(
            self.screen_point((Fraction(3, 2), Fraction(0)), origin_new, scale_4),
            self.screen_point((Fraction(2), Fraction(0)), origin_new, scale_4),
            color=POINT,
            stroke_width=6.0,
        )
        old_measure = VGroup(
            label("舊斜邊", 22, CORAL, "BOLD"),
            MathTex("=1", font_size=31, color=CORAL),
        ).arrange(RIGHT, buff=0.12).move_to([-4.25, -2.12, 0])
        new_measure = VGroup(
            label("新斜邊", 22, CORAL, "BOLD"),
            MathTex(r"=\frac12+\frac12+1=2", font_size=30, color=CORAL),
        ).arrange(RIGHT, buff=0.12).move_to([2.70, -2.12, 0])
        increment = VGroup(
            VGroup(
                MathTex(r"\Delta", font_size=34, color=CORAL),
                label("斜邊", 22, CORAL, "BOLD"),
                MathTex("=+1", font_size=34, color=CORAL),
            ).arrange(RIGHT, buff=0.08),
            VGroup(
                MathTex(r"\Delta", font_size=34, color=POINT),
                label("底邊", 22, POINT, "BOLD"),
                MathTex(r"=+\frac12", font_size=34, color=POINT),
            ).arrange(RIGHT, buff=0.08),
            MathTex(r"\Delta r=\frac32", font_size=39, color=INK),
        ).arrange(RIGHT, buff=0.70).move_to([0, -2.94, 0])
        beat_4 = VGroup(
            old_union,
            new_union,
            old_name,
            new_name,
            old_last_side,
            old_side_text,
            replacement,
            bottom_extension,
            old_measure,
            new_measure,
            increment,
        )
        self.play(FadeIn(old_union), FadeIn(old_name), run_time=0.58)
        self.play(FadeIn(new_union), FadeIn(new_name), run_time=0.58)
        self.play(Create(old_last_side), FadeIn(old_side_text), FadeIn(old_measure), run_time=0.58)
        self.play(Create(replacement), FadeIn(new_measure), run_time=0.80)
        self.play(Create(bottom_extension), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(item) for item in increment), lag_ratio=0.22), run_time=0.85)
        self.wait(0.42)

        # Beat 05: count every exposed slanted and bottom piece for general n.
        self.next_beat("generalize_the_perimeter")
        new_title = self.stage_title("把所有外露小段數完，得到一般周長")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_4),
            run_time=0.72,
        )
        title = new_title
        count_demo = 6
        scale_5 = 1.62
        origin_5 = np.array([-6.55, -1.20, 0.0])
        demo_triangles = VGroup(
            *(
                self.triangle(
                    index,
                    origin_5,
                    scale_5,
                    MUTED,
                    fill_opacity=0.02,
                    stroke_width=1.2,
                )
                for index in range(count_demo)
            )
        )
        boundary_points_5 = union_boundary_vertices(count_demo)
        slants = VGroup(
            *(
                Line(
                    self.screen_point(first, origin_5, scale_5),
                    self.screen_point(second, origin_5, scale_5),
                    color=CORAL,
                    stroke_width=4.2,
                )
                for first, second in zip(
                    boundary_points_5[:-1], boundary_points_5[1:], strict=True
                )
            )
        )
        bottom = Line(
            self.screen_point(boundary_points_5[-1], origin_5, scale_5),
            self.screen_point(boundary_points_5[0], origin_5, scale_5),
            color=POINT,
            stroke_width=5.2,
        )
        diagram_key = VGroup(
            label("斜邊", 20, CORAL, "BOLD"),
            label("底邊", 20, POINT, "BOLD"),
        ).arrange(RIGHT, buff=0.45).move_to([-3.75, -2.18, 0])
        slant_formula = VGroup(
            label("斜邊", 23, CORAL, "BOLD"),
            MathTex(
                r"=2\cdot1+2(n-1)\cdot\frac12=n+1",
                font_size=37,
                color=CORAL,
            ),
        ).arrange(RIGHT, buff=0.15).move_to([3.55, 1.05, 0])
        base_formula = VGroup(
            label("底邊", 23, POINT, "BOLD"),
            MathTex(
                r"=1+(n-1)\cdot\frac12=\frac{n+1}{2}",
                font_size=37,
                color=POINT,
            ),
        ).arrange(RIGHT, buff=0.15).move_to([3.55, -0.20, 0])
        perimeter_formula = MathTex(
            r"r_n=(n+1)+\frac{n+1}{2}=\frac{3(n+1)}2",
            font_size=48,
            color=INK,
        ).move_to([3.55, -1.65, 0])
        perimeter_formula.set_color_by_tex("r_n", CORAL)
        beat_5 = VGroup(
            demo_triangles,
            slants,
            bottom,
            diagram_key,
            slant_formula,
            base_formula,
            perimeter_formula,
        )
        self.play(FadeIn(demo_triangles), run_time=0.50)
        self.play(Create(slants), FadeIn(diagram_key[0]), run_time=0.90)
        self.play(Create(bottom), FadeIn(diagram_key[1]), run_time=0.55)
        self.play(Write(slant_formula), run_time=0.72)
        self.play(Write(base_formula), run_time=0.72)
        self.play(Write(perimeter_formula), run_time=0.82)
        self.wait(0.42)

        # Beat 06: earn the area of one unit triangle from its altitude.
        self.next_beat("measure_one_triangle_area")
        new_title = self.stage_title("面積要重新開始：先量一個正三角形")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_5),
            run_time=0.72,
        )
        title = new_title
        scale_6 = 4.10
        origin_6 = np.array([-5.45, -1.55, 0.0])
        area_triangle = self.triangle(0, origin_6, scale_6, BLUE, fill_opacity=0.11)
        apex_6 = self.screen_point((Fraction(1, 2), Fraction(1, 2)), origin_6, scale_6)
        foot_6 = self.screen_point((Fraction(1, 2), Fraction(0)), origin_6, scale_6)
        left_6 = self.screen_point((Fraction(0), Fraction(0)), origin_6, scale_6)
        altitude = DashedLine(apex_6, foot_6, color=REGION, stroke_width=3.2)
        right_angle = MathTex(r"\square", font_size=20, color=REGION).move_to(
            foot_6 + np.array([-0.17, 0.17, 0])
        )
        half_brace = BraceBetweenPoints(left_6, foot_6, direction=DOWN, color=POINT)
        half_label = MathTex(r"\frac12", font_size=31, color=POINT).next_to(
            half_brace, DOWN, buff=0.08
        )
        side_one = MathTex("1", font_size=31, color=BLUE).move_to([-4.45, 0.15, 0])
        height_h = MathTex("h", font_size=34, color=REGION).next_to(
            altitude, RIGHT, buff=0.12
        )
        height_equation = MathTex(
            r"h^2+\left(\frac12\right)^2=1^2",
            font_size=40,
            color=INK,
        ).move_to([3.35, 1.12, 0])
        height_result = MathTex(r"h=\frac{\sqrt3}{2}", font_size=44, color=REGION).move_to(
            [3.35, 0.05, 0]
        )
        one_area = MathTex(
            r"A_\triangle=\frac12\cdot1\cdot\frac{\sqrt3}{2}=\frac{\sqrt3}{4}",
            font_size=46,
            color=INK,
        ).move_to([3.35, -1.45, 0])
        one_area.set_color_by_tex(r"A_\triangle", REGION)
        beat_6 = VGroup(
            area_triangle,
            altitude,
            right_angle,
            half_brace,
            half_label,
            side_one,
            height_h,
            height_equation,
            height_result,
            one_area,
        )
        self.play(Create(area_triangle), run_time=0.72)
        self.play(Create(altitude), FadeIn(right_angle), FadeIn(height_h), run_time=0.58)
        self.play(Create(half_brace), FadeIn(half_label), FadeIn(side_one), run_time=0.55)
        self.play(Write(height_equation), run_time=0.68)
        self.play(Write(height_result), run_time=0.55)
        self.play(Write(one_area), run_time=0.78)
        self.wait(0.42)

        # Beat 07: identify and measure exactly one adjacent overlap.
        self.next_beat("measure_one_adjacent_overlap")
        new_title = self.stage_title("相鄰兩個三角形，只重疊一個半邊長的小三角形")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_6),
            run_time=0.72,
        )
        title = new_title
        scale_7 = 3.45
        origin_7 = np.array([-6.05, -1.45, 0.0])
        overlap_triangles = VGroup(
            self.triangle(0, origin_7, scale_7, BLUE, fill_opacity=0.08),
            self.triangle(1, origin_7, scale_7, POINT, fill_opacity=0.08),
        )
        overlap_region = self.overlap(0, origin_7, scale_7, fill_opacity=0.48)
        overlap_base_start = self.screen_point(
            (Fraction(1, 2), Fraction(0)), origin_7, scale_7
        )
        overlap_base_end = self.screen_point((Fraction(1), Fraction(0)), origin_7, scale_7)
        overlap_brace = BraceBetweenPoints(
            overlap_base_start,
            overlap_base_end,
            direction=DOWN,
            color=PURPLE,
        )
        overlap_half = MathTex(r"\frac12", font_size=31, color=PURPLE).next_to(
            overlap_brace, DOWN, buff=0.08
        )
        overlap_name = label("三邊都是 1/2", 25, PURPLE, "BOLD")
        overlap_name.move_to([-3.45, 1.65, 0])
        scaling_note = label("邊長縮成 1/2，面積縮成 (1/2)²", 25, MUTED, "MEDIUM")
        scaling_note.move_to([3.45, 1.25, 0])
        overlap_area = MathTex(
            r"A_\cap=\left(\frac12\right)^2\cdot\frac{\sqrt3}{4}",
            font_size=44,
            color=INK,
        ).move_to([3.45, 0.10, 0])
        overlap_result = MathTex(
            r"A_\cap=\frac{\sqrt3}{16}",
            font_size=51,
            color=PURPLE,
        ).move_to([3.45, -1.20, 0])
        beat_7 = VGroup(
            overlap_triangles,
            overlap_region,
            overlap_brace,
            overlap_half,
            overlap_name,
            scaling_note,
            overlap_area,
            overlap_result,
        )
        self.play(Create(overlap_triangles), run_time=0.72)
        self.play(FadeIn(overlap_region), FadeIn(overlap_name), run_time=0.58)
        self.play(Create(overlap_brace), FadeIn(overlap_half), run_time=0.48)
        self.play(FadeIn(scaling_note), run_time=0.45)
        self.play(Write(overlap_area), run_time=0.72)
        self.play(Write(overlap_result), run_time=0.58)
        self.wait(0.42)

        # Beat 08: show why inclusion-exclusion stops after adjacent pairs.
        self.next_beat("rule_out_hidden_triple_overlap")
        new_title = self.stage_title("三個一起看：相隔兩格只碰到一個點")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_7),
            run_time=0.72,
        )
        title = new_title
        scale_8 = 2.80
        origin_8 = np.array([-6.10, -1.35, 0.0])
        first_8 = self.triangle(0, origin_8, scale_8, BLUE, fill_opacity=0.08)
        middle_8 = self.triangle(1, origin_8, scale_8, MUTED, fill_opacity=0.03)
        third_8 = self.triangle(2, origin_8, scale_8, POINT, fill_opacity=0.08)
        overlaps_8 = VGroup(
            self.overlap(0, origin_8, scale_8, fill_opacity=0.30),
            self.overlap(1, origin_8, scale_8, fill_opacity=0.30),
        )
        touch_point = self.screen_point((Fraction(1), Fraction(0)), origin_8, scale_8)
        touch_dot = Dot(touch_point, radius=0.09, color=CORAL)
        touch_label = label("第一個與第三個只共用這一點", 23, CORAL, "BOLD")
        touch_label.next_to(touch_dot, DOWN, buff=0.25).shift(LEFT * 0.15)
        separation = VGroup(
            MathTex(
                r"|j-i|\ge2\quad\Longrightarrow\quad T_i\cap T_j",
                font_size=34,
                color=INK,
            ),
            label("只有一點或不相交", 22, INK, "MEDIUM"),
        ).arrange(DOWN, buff=0.16).move_to([3.55, 0.90, 0])
        triple_zero = VGroup(
            label("三重重疊的面積", 27, CORAL, "BOLD"),
            MathTex("=0", font_size=43, color=CORAL),
        ).arrange(RIGHT, buff=0.14).move_to([3.55, -0.35, 0])
        consequence = label("所以只需要扣掉相鄰的 n−1 塊重疊", 26, PURPLE, "BOLD")
        consequence.move_to([3.55, -1.55, 0])
        beat_8 = VGroup(
            first_8,
            middle_8,
            third_8,
            overlaps_8,
            touch_dot,
            touch_label,
            separation,
            triple_zero,
            consequence,
        )
        self.play(Create(first_8), Create(middle_8), Create(third_8), run_time=0.75)
        self.play(FadeIn(overlaps_8), run_time=0.58)
        self.play(GrowFromCenter(touch_dot), FadeIn(touch_label), run_time=0.52)
        self.play(Write(separation), run_time=0.72)
        self.play(Write(triple_zero), run_time=0.58)
        self.play(FadeIn(consequence), run_time=0.48)
        self.wait(0.42)

        # Beat 09: audit n=1,2,3 and then generalize the inclusion-exclusion count.
        self.next_beat("audit_small_areas_and_generalize")
        new_title = self.stage_title("先核對 1、2、3 個，再寫一般面積")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_8),
            run_time=0.72,
        )
        title = new_title
        centers = (-4.85, 0.0, 4.85)
        mini_scale = 1.55
        mini_unions = VGroup()
        mini_labels = VGroup()
        mini_areas = VGroup()
        area_expressions = (
            r"\frac{4\sqrt3}{16}",
            r"\frac{8\sqrt3}{16}-\frac{\sqrt3}{16}=\frac{7\sqrt3}{16}",
            r"\frac{12\sqrt3}{16}-\frac{2\sqrt3}{16}=\frac{10\sqrt3}{16}",
        )
        for index, (count, center) in enumerate(zip((1, 2, 3), centers, strict=True)):
            width = Fraction(count + 1, 2)
            mini_origin = np.array(
                [center - mini_scale * float(width) / 2, 0.15, 0.0]
            )
            mini_unions.add(
                self.union_diagram(
                    count,
                    mini_origin,
                    mini_scale,
                    boundary_color=CORAL,
                    area_opacity=0.18,
                )
            )
            mini_labels.add(
                MathTex(rf"n={count}", font_size=29, color=POINT).move_to(
                    [center, 1.75, 0]
                )
            )
            mini_areas.add(
                MathTex(
                    area_expressions[index],
                    font_size=29 if count > 1 else 34,
                    color=REGION,
                ).move_to([center, -0.65, 0])
            )
        area_general = MathTex(
            r"s_n=n\cdot\frac{\sqrt3}{4}-(n-1)\cdot\frac{\sqrt3}{16}",
            font_size=42,
            color=INK,
        ).move_to([0, -1.78, 0])
        area_general.set_color_by_tex("s_n", REGION)
        area_simplified = MathTex(
            r"s_n=\frac{(3n+1)\sqrt3}{16}",
            font_size=50,
            color=REGION,
        ).move_to([0, -2.76, 0])
        beat_9 = VGroup(
            mini_unions,
            mini_labels,
            mini_areas,
            area_general,
            area_simplified,
        )
        self.play(
            LaggedStart(
                *(
                    FadeIn(VGroup(diagram, name))
                    for diagram, name in zip(mini_unions, mini_labels, strict=True)
                ),
                lag_ratio=0.20,
            ),
            run_time=1.00,
        )
        self.play(LaggedStart(*(Write(item) for item in mini_areas), lag_ratio=0.18), run_time=1.05)
        self.play(Write(area_general), run_time=0.78)
        self.play(Write(area_simplified), run_time=0.68)
        self.wait(0.42)

        # Beat 10: a genuine pause with both requested values still hidden.
        self.next_beat("hold_before_both_values")
        new_title = self.stage_title("現在代入 112，但先把兩個結果都留白")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_9),
            run_time=0.72,
        )
        title = new_title
        perimeter_hold = self.formula_card(
            r"r_{112}=\frac{3(112+1)}2=?",
            CORAL,
        ).move_to([-3.35, 0.35, 0])
        area_hold = self.formula_card(
            r"s_{112}=\frac{(3\cdot112+1)\sqrt3}{16}=?",
            REGION,
        ).move_to([3.35, 0.35, 0])
        hold_prompt = label("先算 112+1，也先算 3×112+1", 29, POINT, "BOLD")
        hold_prompt.move_to([0, -1.25, 0])
        hold_silence = label("兩個值都算好，再往下看", 23, MUTED, "MEDIUM")
        hold_silence.move_to([0, -2.00, 0])
        beat_10 = VGroup(perimeter_hold, area_hold, hold_prompt, hold_silence)
        self.play(FadeIn(perimeter_hold), run_time=0.58)
        self.play(FadeIn(area_hold), run_time=0.58)
        self.play(FadeIn(hold_prompt), FadeIn(hold_silence), run_time=0.52)
        self.wait(0.85)

        # Beat 11: trace the outline before revealing the perimeter value.
        self.next_beat("reveal_the_perimeter")
        new_title = self.stage_title("先沿著外輪廓走一圈，落下周長")
        self.play(
            self.title_change(title, new_title),
            FadeOut(beat_10),
            run_time=0.70,
        )
        title = new_title
        scale_11 = 1.62
        origin_11 = np.array([-7.00, -0.70, 0.0])
        strip_triangles = VGroup(
            *(
                self.triangle(
                    index,
                    origin_11,
                    scale_11,
                    MUTED,
                    fill_opacity=0.02,
                    stroke_width=1.0,
                )
                for index in range(8)
            )
        )
        strip_outline = self.boundary(
            8,
            origin_11,
            scale_11,
            CORAL,
            fill_opacity=0.02,
            stroke_width=5.0,
        )
        schematic = label("同樣的邊界規則延伸到第 112 個", 22, MUTED, "MEDIUM")
        schematic.move_to([-3.35, -2.15, 0])
        perimeter_substitute = MathTex(
            r"r_{112}=\frac{3(112+1)}2=\frac{3\cdot113}{2}",
            font_size=42,
            color=INK,
        ).move_to([4.45, 0.72, 0])
        perimeter_answer = MathTex(
            r"r=\frac{339}{2}",
            font_size=58,
            color=CORAL,
        ).move_to([4.45, -0.75, 0])
        beat_11 = VGroup(
            strip_triangles,
            strip_outline,
            schematic,
            perimeter_substitute,
            perimeter_answer,
        )
        self.play(FadeIn(strip_triangles), run_time=0.52)
        self.play(Create(strip_outline), FadeIn(schematic), run_time=1.05)
        self.play(Write(perimeter_substitute), run_time=0.78)
        self.play(Write(perimeter_answer), run_time=0.58)
        self.play(Indicate(perimeter_answer, color=CORAL), run_time=0.65)
        self.wait(0.42)

        # Beat 12: fill the same union before revealing the area value.
        self.next_beat("reveal_the_area")
        new_title = self.stage_title("再把同一個聯集填滿，落下面積")
        self.play(
            self.title_change(title, new_title),
            FadeOut(perimeter_substitute),
            FadeOut(perimeter_answer),
            FadeOut(schematic),
            strip_outline.animate.set_color(MUTED).set_stroke(width=2.0),
            run_time=0.72,
        )
        title = new_title
        area_fill = self.boundary(
            8,
            origin_11,
            scale_11,
            REGION,
            fill_color=REGION,
            fill_opacity=0.30,
            stroke_width=3.0,
        )
        area_schematic = label("每個新三角形，只多出 3/4 個單位三角形的面積", 22, MUTED, "MEDIUM")
        area_schematic.move_to([-3.35, -2.15, 0])
        area_substitute = MathTex(
            r"s_{112}=\frac{(3\cdot112+1)\sqrt3}{16}",
            font_size=42,
            color=INK,
        ).move_to([4.45, 0.72, 0])
        area_answer = MathTex(
            r"s=\frac{337\sqrt3}{16}",
            font_size=55,
            color=REGION,
        ).move_to([4.45, -0.75, 0])
        beat_12 = VGroup(area_fill, area_schematic, area_substitute, area_answer)
        self.play(FadeIn(area_fill), FadeIn(area_schematic), run_time=0.72)
        self.play(Write(area_substitute), run_time=0.78)
        self.play(Write(area_answer), run_time=0.58)
        self.play(Indicate(area_answer, color=REGION), run_time=0.65)
        self.wait(0.42)

        # Beat 13: reconnect both values to the original traced union.
        self.next_beat("return_to_the_traced_union")
        new_title = self.stage_title("回到原圖：輪廓給 r，填色給 s")
        self.play(
            self.title_change(title, new_title),
            FadeOut(strip_triangles),
            FadeOut(strip_outline),
            FadeOut(beat_12),
            run_time=0.72,
        )
        title = new_title
        final_scale = 1.72
        final_origin = np.array([-3.87, -0.35, 0.0])
        final_triangles = VGroup(
            *(
                self.triangle(
                    index,
                    final_origin,
                    final_scale,
                    MUTED,
                    fill_opacity=0.015,
                    stroke_width=1.0,
                )
                for index in range(8)
            )
        )
        final_region = self.boundary(
            8,
            final_origin,
            final_scale,
            CORAL,
            fill_color=REGION,
            fill_opacity=0.24,
            stroke_width=4.8,
        )
        perimeter_tag = label("外輪廓：r", 24, CORAL, "BOLD").move_to([-5.10, 1.82, 0])
        area_tag = label("聯集內部：s", 24, REGION, "BOLD").move_to([5.05, 1.82, 0])
        final_pair = MathTex(
            r"(r,s)=\left(\frac{339}{2},\frac{337\sqrt3}{16}\right)",
            font_size=58,
            color=INK,
        ).move_to([0, -2.02, 0])
        final_pair.set_color_by_tex("339", CORAL)
        final_pair.set_color_by_tex("337", REGION)
        final_frame = SurroundingRectangle(
            final_pair,
            color=POINT,
            stroke_width=2.8,
            buff=0.24,
            corner_radius=0.06,
        )
        final_note = label("半格平移先決定輪廓，也決定每次只扣一塊重疊", 22, MUTED, "MEDIUM")
        final_note.move_to([0, -3.63, 0])
        self.play(FadeIn(final_triangles), FadeIn(final_region), run_time=0.72)
        self.play(FadeIn(perimeter_tag), FadeIn(area_tag), run_time=0.52)
        self.play(Write(final_pair), Create(final_frame), run_time=0.82)
        self.play(FadeIn(final_note), run_time=0.48)
        self.wait(0.62)


if __name__ == "__main__":
    raise SystemExit(
        "Render with: pixi run manim-slides render --quality h "
        "lessons/tcfs_112_math_gifted/q10/deck.py CarloTcfs112MathQ10"
    )
