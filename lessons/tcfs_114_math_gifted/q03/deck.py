"""Manim Slides lesson for TCFS 114 mathematics gifted assessment Q3."""

from __future__ import annotations

from itertools import product

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
    DoubleArrow,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    RightAngle,
    Succession,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


Point3 = tuple[float, float, float]


class CarloTcfs114MathQ03(CarloSlide):
    """Turn six cube face centres into two measurable square pyramids."""

    lesson_id = "carlo.tcfs_114_math_gifted.q03"

    @staticmethod
    def cube_edge_specs() -> tuple[tuple[Point3, Point3, int], ...]:
        """Return each cube edge once, together with its varying axis."""
        edges: list[tuple[Point3, Point3, int]] = []
        for vertex in product((-1.0, 1.0), repeat=3):
            for axis in range(3):
                if vertex[axis] != -1.0:
                    continue
                other = list(vertex)
                other[axis] = 1.0
                edges.append((vertex, tuple(other), axis))
        return tuple(edges)

    @staticmethod
    def pyramid_faces(
        apex: np.ndarray,
        base: tuple[np.ndarray, ...],
        color: str,
    ) -> VGroup:
        """Build four translucent triangular faces around one apex."""
        return VGroup(
            *(
                Polygon(
                    apex,
                    start,
                    end,
                    color=color,
                    stroke_width=2.2,
                    fill_color=color,
                    fill_opacity=0.16,
                ).set_z_index(-1)
                for start, end in zip(base, base[1:] + base[:1], strict=True)
            )
        )

    def construct(self) -> None:
        heading = label("第 3 題｜六個面心圍出多少體積？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學", 17, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)
        divider = Line(
            np.array([0.05, 3.25, 0]),
            np.array([0.05, -3.45, 0]),
            color=HAIRLINE,
            stroke_width=1.5,
        )

        diagram_center = np.array([-3.72, -0.34, 0.0])
        diagram_scale = 2.14
        view = ValueTracker(0.0)
        size = ValueTracker(1.0)

        def project(point: Point3 | np.ndarray) -> np.ndarray:
            """Interpolate from an oblique view to an exact top view."""
            x, y, z = point
            turn = view.get_value()
            horizontal = x + 0.58 * (1.0 - turn) * y
            vertical = (1.0 - turn) * z + (0.38 + 0.62 * turn) * y
            return diagram_center + diagram_scale * size.get_value() * np.array(
                [horizontal, vertical, 0.0]
            )

        def moving_line(
            start: Point3,
            end: Point3,
            *,
            color: str,
            stroke_width: float,
            z_index: int,
        ) -> Line:
            start_3d = np.array(start, dtype=float)
            end_3d = np.array(end, dtype=float)
            line = Line(
                project(start_3d),
                project(end_3d),
                color=color,
                stroke_width=stroke_width,
            ).set_z_index(z_index)

            def update_line(
                mob: Line,
                a: np.ndarray = start_3d,
                b: np.ndarray = end_3d,
            ) -> None:
                projected_start = project(a)
                projected_end = project(b)
                if np.linalg.norm(projected_end - projected_start) < 1e-7:
                    # A vertical cube edge becomes a point in the exact top
                    # view. It is fully transparent there, but Manim's Line
                    # still needs a nonzero internal direction.
                    projected_end = projected_start + np.array([0.0, 1e-7, 0.0])
                mob.put_start_and_end_on(projected_start, projected_end)

            line.add_updater(update_line)
            return line

        def moving_dot(point: Point3, color: str) -> Dot:
            point_3d = np.array(point, dtype=float)
            dot = Dot(project(point_3d), radius=0.085, color=color).set_z_index(8)
            dot.add_updater(lambda mob, p=point_3d: mob.move_to(project(p)))
            return dot

        def moving_polygon(points: tuple[Point3, ...]) -> Polygon:
            source_points = tuple(np.array(point, dtype=float) for point in points)
            polygon = Polygon(
                *(project(point) for point in source_points),
                color=BLUE,
                stroke_width=0,
                fill_color=BLUE,
                fill_opacity=0.13,
            ).set_z_index(-2)

            def update_polygon(mob: Polygon) -> None:
                corners = [project(point) for point in source_points]
                mob.set_points_as_corners([*corners, corners[0]])

            polygon.add_updater(update_polygon)
            return polygon

        base_points: tuple[Point3, ...] = (
            (-1.0, 0.0, 0.0),
            (0.0, -1.0, 0.0),
            (1.0, 0.0, 0.0),
            (0.0, 1.0, 0.0),
        )
        top_point: Point3 = (0.0, 0.0, 1.0)
        bottom_point: Point3 = (0.0, 0.0, -1.0)

        cube_horizontal = VGroup()
        cube_vertical = VGroup()
        for start, end, axis in self.cube_edge_specs():
            edge = moving_line(
                start,
                end,
                color=MUTED,
                stroke_width=2.5,
                z_index=-5,
            )
            (cube_vertical if axis == 2 else cube_horizontal).add(edge)

        base_fill = moving_polygon(base_points)
        base_edges = VGroup(
            *(
                moving_line(
                    start,
                    end,
                    color=BLUE,
                    stroke_width=5.0,
                    z_index=3,
                )
                for start, end in zip(
                    base_points,
                    base_points[1:] + base_points[:1],
                    strict=True,
                )
            )
        )
        upper_edges = VGroup(
            *(
                moving_line(
                    top_point,
                    point,
                    color=POINT,
                    stroke_width=4.2,
                    z_index=2,
                )
                for point in base_points
            )
        )
        lower_edges = VGroup(
            *(
                moving_line(
                    bottom_point,
                    point,
                    color=REGION,
                    stroke_width=4.2,
                    z_index=2,
                )
                for point in base_points
            )
        )
        base_dots = VGroup(*(moving_dot(point, BLUE) for point in base_points))
        top_dot = moving_dot(top_point, POINT)
        bottom_dot = moving_dot(bottom_point, REGION)

        # Beat 01: let the viewer locate the six points before naming the solid.
        self.begin_beat("place_face_centers")
        panel_title = label(
            "六個面的中心在哪裡？",
            34,
            INK,
            "BOLD",
            t2c={"六個": POINT, "中心": POINT},
        ).move_to([3.72, 2.18, 0])
        pair_note = label("從三對相對的面開始", 27, MUTED, "MEDIUM")
        pair_note.move_to([3.72, 1.28, 0])
        count_note = label("2 + 2 + 2 = 6 個面心", 31, INK, "BOLD")
        count_note.move_to([3.72, -0.08, 0])

        self.add(heading, source, divider)
        self.play(
            LaggedStart(
                *(Create(edge) for edge in (*cube_horizontal, *cube_vertical)),
                lag_ratio=0.06,
            ),
            FadeIn(panel_title),
            run_time=1.55,
        )
        self.play(FadeIn(pair_note), run_time=0.45)
        self.play(FadeIn(base_dots[0]), FadeIn(base_dots[2]), run_time=0.7)
        self.play(FadeIn(base_dots[1]), FadeIn(base_dots[3]), run_time=0.7)
        self.play(FadeIn(top_dot), FadeIn(bottom_dot), run_time=0.7)
        self.play(FadeIn(count_note), run_time=0.55)
        self.wait(0.3)

        # Beat 02: connect adjacent face centres and identify the regular solid.
        self.next_beat("connect_octahedron")
        connect_title = label("把相鄰面的中心連起來", 34, INK, "BOLD")
        connect_title.move_to(panel_title)
        edge_note = label("立方體的旋轉對稱 → 12 條邊等長", 27, MUTED, "MEDIUM")
        edge_note.move_to([3.72, 0.48, 0])
        solid_name = label("得到一個正八面體", 35, POINT, "BOLD")
        solid_name.move_to([3.72, -0.72, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(connect_title)),
            FadeOut(pair_note),
            FadeOut(count_note),
            run_time=0.55,
        )
        panel_title = connect_title
        self.play(FadeIn(base_fill), Create(base_edges), run_time=0.9)
        self.play(
            LaggedStart(*(Create(edge) for edge in upper_edges), lag_ratio=0.13),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*(Create(edge) for edge in lower_edges), lag_ratio=0.13),
            run_time=1.0,
        )
        self.play(FadeIn(edge_note), FadeIn(solid_name), run_time=0.65)
        self.play(Indicate(VGroup(base_edges, upper_edges, lower_edges), color=POINT))
        self.wait(0.3)

        # Beat 03: earn the convenient side length by showing scale invariance.
        self.next_beat("establish_scale_invariance")
        scale_title = label("大小可以變，比值會變嗎？", 34, INK, "BOLD")
        scale_title.move_to(panel_title)
        cube_scale = MathTex(
            "b",
            r"\longmapsto",
            r"k^3b",
            font_size=42,
            color=INK,
        )
        octa_scale = MathTex(
            "a",
            r"\longmapsto",
            r"k^3a",
            font_size=42,
            color=INK,
        )
        scale_rows = VGroup(cube_scale, octa_scale).arrange(DOWN, buff=0.28)
        scale_rows.move_to([3.72, 0.72, 0])
        cube_scale[0].set_color(MUTED)
        octa_scale[0].set_color(POINT)
        unchanged = MathTex(
            r"\frac{k^3a}{k^3b}",
            "=",
            r"\frac ab",
            font_size=46,
            color=INK,
        ).move_to([3.72, -0.7, 0])
        unchanged[2].set_color(REGION)
        choose_two = label("所以取立方體邊長 2", 29, CORAL, "BOLD")
        choose_two.move_to([3.72, -1.82, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(scale_title)),
            FadeOut(edge_note),
            FadeOut(solid_name),
            run_time=0.55,
        )
        panel_title = scale_title
        self.play(
            size.animate.set_value(0.76),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            size.animate.set_value(1.14),
            run_time=0.95,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(
            size.animate.set_value(1.0),
            run_time=0.75,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(scale_rows), run_time=0.65)
        self.play(Write(unchanged), run_time=0.75)

        dimension_start = project((-1.0, -1.0, -1.0)) + DOWN * 0.23
        dimension_end = project((1.0, -1.0, -1.0)) + DOWN * 0.23
        side_dimension = DoubleArrow(
            dimension_start,
            dimension_end,
            buff=0,
            color=CORAL,
            stroke_width=3.2,
            tip_length=0.14,
        )
        side_two = MathTex("2", font_size=35, color=CORAL)
        side_two.next_to(side_dimension, DOWN, buff=0.08)
        self.play(FadeIn(choose_two), Create(side_dimension), FadeIn(side_two))
        self.wait(0.3)

        # Beat 04: isolate the shared middle square before changing viewpoint.
        self.next_beat("isolate_middle_square")
        middle_title = label("先抓住中間那一圈", 34, INK, "BOLD")
        middle_title.move_to(panel_title)
        middle_question = label("四個側面中心連成什麼形？", 31, INK, "BOLD")
        middle_question.move_to([3.72, 0.62, 0])
        viewpoint_hint = label("斜著看會被投影騙到", 26, MUTED, "MEDIUM")
        viewpoint_hint.move_to([3.72, -0.48, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(middle_title)),
            FadeOut(scale_rows),
            FadeOut(unchanged),
            FadeOut(choose_two),
            FadeOut(side_dimension),
            FadeOut(side_two),
            cube_horizontal.animate.set_opacity(0.26),
            cube_vertical.animate.set_opacity(0.26),
            upper_edges.animate.set_opacity(0.16),
            lower_edges.animate.set_opacity(0.16),
            top_dot.animate.set_opacity(0.22),
            bottom_dot.animate.set_opacity(0.22),
            base_fill.animate.set_fill(opacity=0.28),
            run_time=0.95,
        )
        panel_title = middle_title
        self.play(FadeIn(middle_question), FadeIn(viewpoint_hint), run_time=0.55)
        self.play(Indicate(base_edges, color=BLUE), run_time=0.8)
        self.wait(0.3)

        # Beat 05: turn the same points to an exact top view.
        self.next_beat("turn_to_top_view")
        top_title = label("從正上方看同一組點", 34, INK, "BOLD")
        top_title.move_to(panel_title)
        midpoint_note = label("四個側面中心 → 四邊中點", 29, MUTED, "MEDIUM")
        midpoint_note.move_to([3.72, 0.7, 0])
        square_note = label("中間藍色圖形是正方形", 33, BLUE, "BOLD")
        square_note.move_to([3.72, -0.48, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(top_title)),
            FadeOut(middle_question),
            FadeOut(viewpoint_hint),
            upper_edges.animate.set_opacity(0),
            lower_edges.animate.set_opacity(0),
            top_dot.animate.set_opacity(0),
            bottom_dot.animate.set_opacity(0),
            cube_vertical.animate.set_opacity(0),
            cube_horizontal.animate.set_opacity(0.18),
            view.animate.set_value(1.0),
            run_time=1.8,
            rate_func=rate_functions.ease_in_out_sine,
        )
        panel_title = top_title

        outer_points = tuple(
            project(point)
            for point in (
                (-1.0, -1.0, 0.0),
                (1.0, -1.0, 0.0),
                (1.0, 1.0, 0.0),
                (-1.0, 1.0, 0.0),
            )
        )
        outer_square = Polygon(
            *outer_points,
            color=MUTED,
            stroke_width=3.2,
            fill_opacity=0,
        ).set_z_index(-1)
        left_base = project(base_points[0])
        lower_base = project(base_points[1])
        upper_base = project(base_points[3])
        angle_line_one = Line(left_base, lower_base)
        angle_line_two = Line(left_base, upper_base)
        right_angle = RightAngle(
            angle_line_one,
            angle_line_two,
            length=0.24,
            color=BLUE,
            stroke_width=3,
        )
        view_badge = label("俯視", 23, POINT, "BOLD")
        view_badge.move_to(diagram_center + np.array([-2.45, 2.43, 0]))

        self.play(Create(outer_square), FadeIn(view_badge), run_time=0.7)
        self.play(FadeIn(midpoint_note), run_time=0.5)
        self.play(Create(right_angle), FadeIn(square_note), run_time=0.7)
        self.wait(0.3)

        # Beat 06: measure one side, then name the full base area.
        self.next_beat("measure_square_base")
        measure_title = label("只量一條邊，就能得到底面積", 33, INK, "BOLD")
        measure_title.move_to(panel_title)
        corner = project((-1.0, -1.0, 0.0))
        triangle = Polygon(
            left_base,
            corner,
            lower_base,
            color=CORAL,
            stroke_width=2.8,
            fill_color=CORAL,
            fill_opacity=0.12,
        ).set_z_index(1)
        vertical_leg = Line(left_base, corner, color=CORAL, stroke_width=5).set_z_index(4)
        horizontal_leg = Line(corner, lower_base, color=CORAL, stroke_width=5).set_z_index(4)
        vertical_one = MathTex("1", font_size=32, color=CORAL)
        vertical_one.next_to(vertical_leg, LEFT, buff=0.12)
        horizontal_one = MathTex("1", font_size=32, color=CORAL)
        horizontal_one.next_to(horizontal_leg, DOWN, buff=0.12)
        side_d = MathTex("d", font_size=34, color=BLUE)
        side_d.move_to((left_base + lower_base) / 2 + np.array([0.28, 0.27, 0]))
        side_root = MathTex(r"\sqrt2", font_size=33, color=BLUE)
        side_root.move_to(side_d)

        length_equation = MathTex(
            "d^2",
            "=",
            "1^2",
            "+",
            "1^2",
            "=",
            "2",
            font_size=42,
            color=INK,
        ).move_to([3.72, 0.92, 0])
        length_equation[0].set_color(BLUE)
        length_equation[2].set_color(CORAL)
        length_equation[4].set_color(CORAL)
        side_equation = MathTex(
            "d",
            "=",
            r"\sqrt2",
            font_size=44,
            color=INK,
        ).move_to([3.72, -0.12, 0])
        side_equation[0].set_color(BLUE)
        side_equation[2].set_color(BLUE)
        area_equation = MathTex(
            "B",
            "=",
            r"(\sqrt2)^2",
            "=",
            "2",
            font_size=46,
            color=INK,
        ).move_to([3.72, -1.35, 0])
        area_equation[0].set_color(BLUE)
        area_equation[2].set_color(BLUE)
        area_equation[4].set_color(BLUE)
        area_box = SurroundingRectangle(
            area_equation,
            color=BLUE,
            buff=0.18,
            stroke_width=2.5,
        )

        self.play(
            Succession(FadeOut(panel_title), FadeIn(measure_title)),
            FadeOut(midpoint_note),
            FadeOut(square_note),
            run_time=0.55,
        )
        panel_title = measure_title
        self.play(
            FadeIn(triangle),
            Create(vertical_leg),
            Create(horizontal_leg),
            FadeIn(vertical_one),
            FadeIn(horizontal_one),
            FadeIn(side_d),
            run_time=0.8,
        )
        self.play(Write(length_equation), run_time=0.75)
        self.play(
            ReplacementTransform(side_d, side_root),
            Write(side_equation),
            run_time=0.65,
        )
        self.play(Write(area_equation), Create(area_box), run_time=0.8)
        self.wait(0.3)

        # Beat 07: return to 3D and calculate only the upper pyramid.
        self.next_beat("calculate_one_pyramid")
        one_title = label("先只算上半部", 35, INK, "BOLD")
        one_title.move_to(panel_title)
        base_badge = MathTex("B", "=", "2", font_size=42, color=INK)
        base_badge.move_to([3.72, 1.12, 0])
        base_badge[0].set_color(BLUE)
        base_badge[2].set_color(BLUE)

        self.play(
            Succession(FadeOut(panel_title), FadeIn(one_title)),
            ReplacementTransform(area_equation, base_badge),
            FadeOut(area_box),
            FadeOut(length_equation),
            FadeOut(side_equation),
            FadeOut(triangle),
            FadeOut(vertical_leg),
            FadeOut(horizontal_leg),
            FadeOut(vertical_one),
            FadeOut(horizontal_one),
            FadeOut(side_root),
            FadeOut(right_angle),
            FadeOut(outer_square),
            FadeOut(view_badge),
            run_time=0.75,
        )
        panel_title = one_title
        self.play(
            view.animate.set_value(0.0),
            cube_horizontal.animate.set_opacity(0.22),
            cube_vertical.animate.set_opacity(0.22),
            upper_edges.animate.set_opacity(1.0),
            lower_edges.animate.set_opacity(0.08),
            top_dot.animate.set_opacity(1.0),
            bottom_dot.animate.set_opacity(0.12),
            base_fill.animate.set_fill(opacity=0.22),
            run_time=1.75,
            rate_func=rate_functions.ease_in_out_sine,
        )

        projected_base = tuple(project(point) for point in base_points)
        projected_top = project(top_point)
        projected_bottom = project(bottom_point)
        base_center = project((0.0, 0.0, 0.0))
        upper_faces = self.pyramid_faces(projected_top, projected_base, POINT)
        upper_height = DashedLine(
            projected_top,
            base_center,
            color=POINT,
            stroke_width=3.2,
            dash_length=0.12,
        ).set_z_index(5)
        upper_height_one = MathTex("1", font_size=34, color=POINT)
        upper_height_one.next_to(upper_height, RIGHT, buff=0.12)

        half_equation = MathTex(
            "V_1",
            "=",
            r"\frac13",
            r"\times",
            "2",
            r"\times",
            "1",
            "=",
            r"\frac23",
            font_size=42,
            color=INK,
        ).move_to([3.72, -0.28, 0])
        half_equation[0].set_color(POINT)
        half_equation[4].set_color(BLUE)
        half_equation[6].set_color(POINT)
        half_equation[8].set_color(POINT)

        self.play(FadeIn(upper_faces), Create(upper_height), FadeIn(upper_height_one))
        self.play(Write(half_equation[0:4]), run_time=0.55)
        self.play(
            TransformFromCopy(base_badge[2], half_equation[4]),
            Write(half_equation[5]),
            TransformFromCopy(upper_height_one, half_equation[6]),
            run_time=0.7,
        )
        self.play(Write(half_equation[7:9]), run_time=0.55)
        self.wait(0.3)

        # Beat 08: reflect the first pyramid before multiplying by two.
        self.next_beat("reflect_and_double")
        reflect_title = label("沿中間正方形鏡射", 35, INK, "BOLD")
        reflect_title.move_to(panel_title)
        lower_faces = self.pyramid_faces(projected_bottom, projected_base, REGION)
        lower_height = DashedLine(
            base_center,
            projected_bottom,
            color=REGION,
            stroke_width=3.2,
            dash_length=0.12,
        ).set_z_index(5)
        lower_height_one = MathTex("1", font_size=34, color=REGION)
        lower_height_one.next_to(lower_height, RIGHT, buff=0.12)
        equal_halves = MathTex(
            "V_2",
            "=",
            "V_1",
            "=",
            r"\frac23",
            font_size=40,
            color=INK,
        ).move_to([3.72, -1.08, 0])
        equal_halves[0].set_color(REGION)
        equal_halves[2].set_color(POINT)
        octa_volume = MathTex(
            "a",
            "=",
            "2",
            r"\times",
            r"\frac23",
            "=",
            r"\frac43",
            font_size=44,
            color=INK,
        ).move_to([3.72, -2.02, 0])
        octa_volume[0].set_color(POINT)
        octa_volume[2].set_color(REGION)
        octa_volume[4].set_color(POINT)
        octa_volume[6].set_color(POINT)

        self.play(
            Succession(FadeOut(panel_title), FadeIn(reflect_title)), run_time=0.5
        )
        panel_title = reflect_title
        self.play(
            TransformFromCopy(upper_faces, lower_faces),
            TransformFromCopy(upper_height, lower_height),
            TransformFromCopy(upper_height_one, lower_height_one),
            lower_edges.animate.set_opacity(1.0),
            bottom_dot.animate.set_opacity(1.0),
            run_time=1.45,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(Write(equal_halves), run_time=0.65)
        self.play(Write(octa_volume), run_time=0.75)
        self.wait(0.3)

        # Beat 09: restore the outer cube and compute its volume separately.
        self.next_beat("calculate_cube")
        cube_title = label("現在才回到外面的立方體", 34, INK, "BOLD")
        cube_title.move_to(panel_title)
        cube_dimension = DoubleArrow(
            project((-1.0, -1.0, -1.0)) + DOWN * 0.23,
            project((1.0, -1.0, -1.0)) + DOWN * 0.23,
            buff=0,
            color=CORAL,
            stroke_width=3.2,
            tip_length=0.14,
        )
        cube_side_two = MathTex("2", font_size=35, color=CORAL)
        cube_side_two.next_to(cube_dimension, DOWN, buff=0.08)
        cube_volume = MathTex(
            "b",
            "=",
            "2^3",
            "=",
            "8",
            font_size=48,
            color=INK,
        ).move_to([3.72, -0.42, 0])
        cube_volume[0].set_color(MUTED)
        cube_volume[2].set_color(CORAL)
        cube_volume[4].set_color(CORAL)
        ready_note = label("兩個體積都準備好了", 28, MUTED, "MEDIUM")
        ready_note.move_to([3.72, -1.58, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(cube_title)),
            FadeOut(base_badge),
            FadeOut(half_equation),
            FadeOut(equal_halves),
            octa_volume.animate.move_to([3.72, 0.82, 0]),
            cube_horizontal.animate.set_opacity(0.82),
            cube_vertical.animate.set_opacity(0.82),
            upper_faces.animate.set_fill(opacity=0.08),
            lower_faces.animate.set_fill(opacity=0.08),
            run_time=0.9,
        )
        panel_title = cube_title
        self.play(Create(cube_dimension), FadeIn(cube_side_two), run_time=0.65)
        self.play(
            Write(cube_volume[0:2]),
            TransformFromCopy(cube_side_two, cube_volume[2]),
            Write(cube_volume[3:5]),
            run_time=0.8,
        )
        self.play(FadeIn(ready_note), run_time=0.45)
        self.wait(0.3)

        # Beat 10: form the ratio only after both visible volumes are known.
        self.next_beat("form_final_ratio")
        ratio_title = label("把同一個尺度下的體積相除", 34, INK, "BOLD")
        ratio_title.move_to(panel_title)
        ratio = MathTex(
            r"\frac ab",
            "=",
            r"\frac43",
            r"\div",
            "8",
            "=",
            r"\frac16",
            font_size=52,
            color=INK,
        ).move_to([3.72, -1.42, 0])
        ratio[0].set_color(REGION)
        ratio[2].set_color(POINT)
        ratio[4].set_color(CORAL)
        ratio[6].set_color(POINT)
        answer_box = SurroundingRectangle(
            ratio[6],
            color=POINT,
            buff=0.22,
            stroke_width=3,
        )
        summary = label("面心八面體正好占立方體的六分之一", 28, INK, "BOLD")
        summary.move_to([3.72, -2.65, 0])

        self.play(
            Succession(FadeOut(panel_title), FadeIn(ratio_title)),
            FadeOut(ready_note),
            FadeOut(cube_dimension),
            FadeOut(cube_side_two),
            run_time=0.55,
        )
        panel_title = ratio_title
        self.play(Write(ratio[0:2]), run_time=0.45)
        self.play(
            TransformFromCopy(octa_volume[6], ratio[2]),
            Write(ratio[3]),
            TransformFromCopy(cube_volume[4], ratio[4]),
            run_time=0.75,
        )
        self.play(Write(ratio[5:7]), Create(answer_box), run_time=0.75)
        self.play(FadeIn(summary), run_time=0.55)
        self.play(
            Circumscribe(VGroup(base_edges, upper_edges, lower_edges), color=POINT),
            run_time=0.9,
        )
        self.wait(0.4)
