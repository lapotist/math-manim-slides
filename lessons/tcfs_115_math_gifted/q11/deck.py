"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Q11."""

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
    CarloSlide,
    label,
)
from manim import (
    Arc,
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    ReplacementTransform,
    RightAngle,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


AUX = PURPLE
SECTION = REGION
TARGET = REGION


class Tcfs115Q11Slide(CarloSlide):
    """Follow one section plane across a cube, then unfold its ratio chain."""

    lesson_id = "carlo.tcfs_115_math_gifted.q11"

    @staticmethod
    def marker(
        point: np.ndarray,
        name: str,
        color: str,
        direction: np.ndarray,
        *,
        radius: float = 0.075,
        size: float = 24,
        buff: float = 0.08,
    ) -> VGroup:
        dot = Dot(point, radius=radius, color=color).set_z_index(7)
        text = MathTex(name, font_size=size, color=color)
        text.next_to(dot, direction, buff=buff)
        text.set_z_index(8)
        return VGroup(dot, text)

    @staticmethod
    def tick_on_segment(
        start: np.ndarray,
        end: np.ndarray,
        fraction: float,
        *,
        color: str = POINT,
        length: float = 0.16,
    ) -> Line:
        vector = end - start
        unit = vector / np.linalg.norm(vector)
        normal = np.array([-unit[1], unit[0], 0.0])
        center = start + fraction * vector
        return Line(
            center - normal * length / 2,
            center + normal * length / 2,
            color=color,
            stroke_width=3,
        ).set_z_index(6)

    @staticmethod
    def triangle(points: list[np.ndarray], color: str) -> Polygon:
        return Polygon(
            *points,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.13,
        ).set_z_index(-1)

    @staticmethod
    def minor_arc(
        vertex: np.ndarray,
        first_point: np.ndarray,
        second_point: np.ndarray,
        color: str,
        *,
        radius: float,
    ) -> Arc:
        """Mark the smaller angle between two rays with a deliberate arc."""
        first = first_point - vertex
        second = second_point - vertex
        start_angle = float(np.arctan2(first[1], first[0]))
        end_angle = float(np.arctan2(second[1], second[0]))
        sweep = (end_angle - start_angle + np.pi) % (2 * np.pi) - np.pi
        return Arc(
            radius=radius,
            start_angle=start_angle,
            angle=sweep,
            arc_center=vertex,
            color=color,
            stroke_width=4,
        )

    @staticmethod
    def measurement_label(
        tex: str,
        point: np.ndarray,
        direction: np.ndarray,
        color: str,
        *,
        size: float = 28,
        buff: float = 0.1,
    ) -> MathTex:
        text = MathTex(tex, font_size=size, color=color)
        text.next_to(point, direction, buff=buff)
        return text

    @classmethod
    def cube_diagram(cls) -> dict[str, object]:
        """Return one exact affine projection of the normalized coordinate cube."""
        side = 3.05
        depth = np.array([0.95, 0.72, 0.0])
        b = np.array([-5.65, -2.05, 0.0])

        def project(x: float, y: float, z: float) -> np.ndarray:
            return b + (1 - x) * depth + y * side * RIGHT + z * side * UP

        coords = {
            "A": project(0, 0, 0),
            "B": project(1, 0, 0),
            "C": project(1, 1, 0),
            "D": project(0, 1, 0),
            "E": project(0, 0, 1),
            "F": project(1, 0, 1),
            "G": project(1, 1, 1),
            "H": project(0, 1, 1),
            "P": project(1 / 2, 0, 1),
            "Q": project(0, 2 / 5, 1),
            "R": project(0, 1, 1 / 2),
            "L": project(1, -2 / 5, 1),
            "I": project(-3 / 4, 1, 1),
            "M": project(3 / 4, 1, 0),
            "J": project(1, 1, -1 / 6),
            "N": project(1, 0, 2 / 3),
        }

        faces = {
            "top": Polygon(
                coords["E"], coords["F"], coords["G"], coords["H"],
                stroke_width=0,
                fill_color=BLUE,
                fill_opacity=0.035,
            ).set_z_index(-5),
            "right": Polygon(
                coords["C"], coords["D"], coords["H"], coords["G"],
                stroke_width=0,
                fill_color=PURPLE,
                fill_opacity=0.025,
            ).set_z_index(-5),
            "front": Polygon(
                coords["B"], coords["C"], coords["G"], coords["F"],
                stroke_width=0,
                fill_color=REGION,
                fill_opacity=0.025,
            ).set_z_index(-5),
            "back": Polygon(
                coords["A"], coords["D"], coords["H"], coords["E"],
                stroke_width=0,
                fill_color=BLUE,
                fill_opacity=0.02,
            ).set_z_index(-6),
        }
        face_group = VGroup(*faces.values())

        hidden_names = (("A", "B"), ("A", "D"), ("A", "E"))
        hidden_edges = VGroup(
            *(
                DashedLine(
                    coords[start],
                    coords[end],
                    color=HAIRLINE,
                    stroke_width=2,
                    dash_length=0.11,
                )
                for start, end in hidden_names
            )
        )
        visible_names = (
            ("B", "C"),
            ("C", "D"),
            ("D", "H"),
            ("H", "E"),
            ("E", "F"),
            ("F", "G"),
            ("G", "H"),
            ("B", "F"),
            ("C", "G"),
        )
        visible_edges = VGroup(
            *(
                Line(coords[start], coords[end], color=MUTED, stroke_width=2.6)
                for start, end in visible_names
            )
        )

        directions = {
            "A": LEFT + DOWN,
            "B": LEFT + DOWN,
            "C": RIGHT + DOWN,
            "D": RIGHT + DOWN,
            "E": LEFT + UP,
            "F": LEFT,
            "G": RIGHT,
            "H": RIGHT + UP,
        }
        vertex_markers = {
            name: cls.marker(
                coords[name],
                name,
                INK,
                directions[name],
                radius=0.035,
                size=21,
                buff=0.06,
            )
            for name in "ABCDEFGH"
        }
        vertex_group = VGroup(*vertex_markers.values())
        group = VGroup(face_group, hidden_edges, visible_edges, vertex_group)
        return {
            "coords": coords,
            "faces": faces,
            "face_group": face_group,
            "hidden_edges": hidden_edges,
            "visible_edges": visible_edges,
            "vertices": vertex_markers,
            "vertex_group": vertex_group,
            "group": group,
        }

    @classmethod
    def flat_face(
        cls,
        kind: str,
        origin: np.ndarray,
        side: float,
        *,
        label_scale: float = 1.0,
    ) -> dict[str, object]:
        """Build an undistorted top, right, or front face with exact points."""
        if kind == "top":
            raw = {
                "F": (0, 0),
                "G": (1, 0),
                "H": (1, 1),
                "E": (0, 1),
                "P": (0, 1 / 2),
                "Q": (2 / 5, 1),
                "L": (-2 / 5, 0),
                "I": (1, 7 / 4),
            }
            corners = ("F", "G", "H", "E")
            section_ends = ("L", "I")
            extension_ends = (("L", "G"), ("G", "I"))
            special = ("P", "Q", "L", "I")
            special_colors = {"P": POINT, "Q": POINT, "L": AUX, "I": AUX}
            directions = {
                "F": DOWN,
                "G": DOWN + RIGHT,
                "H": RIGHT,
                "E": LEFT + UP,
                "P": LEFT,
                "Q": UP,
                "L": LEFT + DOWN,
                "I": RIGHT + UP,
            }
            face_color = BLUE
        elif kind == "right":
            raw = {
                "D": (0, 0),
                "C": (1, 0),
                "G": (1, 1),
                "H": (0, 1),
                "I": (-3 / 4, 1),
                "R": (0, 1 / 2),
                "M": (3 / 4, 0),
                "J": (1, -1 / 6),
            }
            corners = ("D", "C", "G", "H")
            section_ends = ("I", "J")
            extension_ends = (("I", "G"), ("G", "J"))
            special = ("I", "R", "M", "J")
            special_colors = {"I": AUX, "R": POINT, "M": BLUE, "J": AUX}
            directions = {
                "D": LEFT + DOWN,
                "C": RIGHT + DOWN,
                "G": RIGHT + UP,
                "H": UP,
                "I": LEFT + UP,
                "R": LEFT,
                "M": DOWN,
                "J": RIGHT + DOWN,
            }
            face_color = PURPLE
        elif kind == "front":
            raw = {
                "B": (0, 0),
                "C": (1, 0),
                "G": (1, 1),
                "F": (0, 1),
                "L": (-2 / 5, 1),
                "J": (1, -1 / 6),
                "N": (0, 2 / 3),
            }
            corners = ("B", "C", "G", "F")
            section_ends = ("L", "J")
            extension_ends = (("L", "G"), ("G", "J"))
            special = ("L", "J", "N")
            special_colors = {"L": AUX, "J": AUX, "N": TARGET}
            directions = {
                "B": LEFT + DOWN,
                "C": RIGHT + DOWN,
                "G": RIGHT + UP,
                "F": UP,
                "L": LEFT + UP,
                "J": RIGHT + DOWN,
                "N": LEFT,
            }
            face_color = REGION
        else:
            raise ValueError(f"unknown face kind: {kind}")

        coords = {
            name: origin + np.array([x * side, y * side, 0.0])
            for name, (x, y) in raw.items()
        }
        face = Polygon(
            *(coords[name] for name in corners),
            color=HAIRLINE,
            stroke_width=0,
            fill_color=face_color,
            fill_opacity=0.055,
        ).set_z_index(-5)
        boundary = VGroup(
            *(
                Line(
                    coords[corners[index]],
                    coords[corners[(index + 1) % 4]],
                    color=MUTED,
                    stroke_width=2.5,
                )
                for index in range(4)
            )
        )
        extensions = VGroup(
            *(
                DashedLine(
                    coords[start],
                    coords[end],
                    color=HAIRLINE,
                    stroke_width=1.6,
                    dash_length=max(0.07, side * 0.035),
                )
                for start, end in extension_ends
            )
        )
        section = Line(
            coords[section_ends[0]],
            coords[section_ends[1]],
            color=SECTION,
            stroke_width=4.5,
        ).set_z_index(2)

        base_markers = {
            name: cls.marker(
                coords[name],
                name,
                INK,
                directions[name],
                radius=0.025 * label_scale,
                size=17 * label_scale,
                buff=0.045 * label_scale,
            )
            for name in corners
        }
        special_markers = {
            name: cls.marker(
                coords[name],
                name,
                special_colors[name],
                directions[name],
                radius=0.055 * label_scale,
                size=20 * label_scale,
                buff=0.055 * label_scale,
            )
            for name in special
        }
        marker_group = VGroup(*base_markers.values(), *special_markers.values())
        side_label = MathTex("a", font_size=22 * label_scale, color=POINT)
        side_label.move_to((coords[corners[0]] + coords[corners[1]]) / 2 + DOWN * 0.2 * label_scale)
        details = VGroup(boundary, extensions, section, marker_group, side_label)
        group = VGroup(face, details)
        return {
            "coords": coords,
            "face": face,
            "boundary": boundary,
            "extensions": extensions,
            "section": section,
            "base_markers": base_markers,
            "special_markers": special_markers,
            "markers": marker_group,
            "side_label": side_label,
            "details": details,
            "group": group,
        }

    @staticmethod
    def summary_face(kind: str, center: np.ndarray, color: str) -> VGroup:
        """Make a compact exact face icon for the final three-step recap."""
        side = 1.25
        lower_left = center + np.array([-side / 2, -side / 2, 0.0])
        square = Polygon(
            lower_left,
            lower_left + side * RIGHT,
            lower_left + side * (RIGHT + UP),
            lower_left + side * UP,
            color=MUTED,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.045,
        )
        if kind == "top":
            start = lower_left + np.array([-0.28 * side, 0.0, 0.0])
            end = lower_left + np.array([side, 1.53 * side, 0.0])
        elif kind == "right":
            start = lower_left + np.array([-0.48 * side, side, 0.0])
            end = lower_left + np.array([side, -0.11 * side, 0.0])
        else:
            start = lower_left + np.array([-0.28 * side, side, 0.0])
            end = lower_left + np.array([side, -0.11 * side, 0.0])
        section = Line(start, end, color=SECTION, stroke_width=3)
        return VGroup(square, section)

    def construct(self) -> None:
        heading = label("第 11 題｜讓同一個截平面走過三個面", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學｜PDF 第 7 頁", 16, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)

        cube = self.cube_diagram()
        coords = cube["coords"]

        cube_prompt = label("斜平面穿過一個正方形面，會留下什麼？", 30, INK, "BOLD")
        cube_prompt.move_to([3.55, 0.82, 0])
        intersection_fact = VGroup(
            label("兩個平面相交", 24, MUTED, "MEDIUM"),
            Arrow(LEFT * 0.1, RIGHT * 0.5, color=MUTED, stroke_width=2.5, buff=0),
            label("一條直線", 29, SECTION, "BOLD"),
        ).arrange(RIGHT, buff=0.24).move_to([3.55, -0.32, 0])

        # Beat 01 build_cube: settled semantic step.
        self.play(FadeIn(heading), FadeIn(source), FadeIn(cube["face_group"]), run_time=0.7)
        self.play(
            Create(cube["hidden_edges"]),
            LaggedStart(*(Create(edge) for edge in cube["visible_edges"]), lag_ratio=0.08),
            run_time=1.7,
        )
        self.play(
            LaggedStart(*(FadeIn(marker) for marker in cube["vertex_group"]), lag_ratio=0.06),
            FadeIn(cube_prompt),
            run_time=1.0,
        )
        self.play(GrowArrow(intersection_fact[1]), FadeIn(intersection_fact[0]), FadeIn(intersection_fact[2]))

        # Beat 02 place_pqr: settled semantic step.
        self.next_slide()

        p_marker = self.marker(coords["P"], "P", POINT, LEFT + UP)
        q_marker = self.marker(coords["Q"], "Q", POINT, UP)
        r_marker = self.marker(coords["R"], "R", POINT, RIGHT)
        pqr_markers = VGroup(p_marker, q_marker, r_marker)
        plane_patch = Polygon(
            coords["P"],
            coords["Q"],
            coords["R"],
            color=SECTION,
            stroke_width=1.5,
            fill_color=SECTION,
            fill_opacity=0.09,
        ).set_z_index(-2)
        midpoint_ticks = VGroup(
            self.tick_on_segment(coords["E"], coords["F"], 1 / 4),
            self.tick_on_segment(coords["E"], coords["F"], 3 / 4),
            self.tick_on_segment(coords["H"], coords["D"], 1 / 4),
            self.tick_on_segment(coords["H"], coords["D"], 3 / 4),
        )
        point_data = VGroup(
            VGroup(MathTex("P:", font_size=29, color=POINT), MathTex(r"EP=PF=\frac a2", font_size=32, color=INK)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex("R:", font_size=29, color=POINT), MathTex(r"HR=RD=\frac a2", font_size=32, color=INK)).arrange(RIGHT, buff=0.2),
            VGroup(MathTex("Q:", font_size=29, color=POINT), MathTex(r"EQ:QH=2:3", font_size=32, color=INK)).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([3.55, 0.5, 0])
        plane_note = label("三個不共線的點，固定唯一平面", 27, SECTION, "BOLD")
        plane_note.move_to([3.55, -1.45, 0])

        self.play(FadeOut(cube_prompt), FadeOut(intersection_fact), run_time=0.45)
        self.play(
            FadeIn(plane_patch),
            LaggedStart(*(GrowFromCenter(marker[0]) for marker in pqr_markers), lag_ratio=0.16),
            LaggedStart(*(FadeIn(marker[1]) for marker in pqr_markers), lag_ratio=0.16),
            run_time=1.25,
        )
        self.play(Create(midpoint_ticks), LaggedStart(*(FadeIn(row) for row in point_data), lag_ratio=0.15))
        self.play(FadeIn(plane_note), run_time=0.55)

        # Beat 03 trace_known_section: settled semantic step.
        self.next_slide()

        pq = Line(coords["P"], coords["Q"], color=SECTION, stroke_width=6).set_z_index(3)
        qr = Line(coords["Q"], coords["R"], color=SECTION, stroke_width=6).set_z_index(3)
        trace_notes = VGroup(
            label("上表面：P、Q", 25, BLUE, "BOLD"),
            MathTex(r"P,Q\ \Longrightarrow\ PQ", font_size=34, color=INK),
            label("後表面：Q、R", 25, BLUE, "BOLD"),
            MathTex(r"Q,R\ \Longrightarrow\ QR", font_size=34, color=INK),
            label("同一面上的兩點，決定該面的截線方向", 24, SECTION, "BOLD"),
        ).arrange(DOWN, buff=0.27).move_to([3.7, 0.02, 0])

        self.play(FadeOut(point_data), FadeOut(plane_note), plane_patch.animate.set_opacity(0.04))
        self.play(cube["faces"]["top"].animate.set_fill(BLUE, opacity=0.16), FadeIn(trace_notes[0]))
        self.play(Create(pq), Write(trace_notes[1]), run_time=0.85)
        # Beat 04 mark_known_section: settled semantic step.
        self.next_slide()
        self.play(cube["faces"]["back"].animate.set_fill(BLUE, opacity=0.12), FadeIn(trace_notes[2]))
        self.play(Create(qr), Write(trace_notes[3]), run_time=0.85)
        self.play(FadeIn(trace_notes[4]), run_time=0.55)

        # Beat 05 extend_top_line: settled semantic step.
        self.next_slide()

        fg_extension = DashedLine(
            coords["L"], coords["G"], color=HAIRLINE, stroke_width=2, dash_length=0.12
        )
        gh_extension = DashedLine(
            coords["G"], coords["I"], color=HAIRLINE, stroke_width=2, dash_length=0.12
        )
        lp_extension = Line(coords["L"], coords["P"], color=SECTION, stroke_width=5)
        qi_extension = Line(coords["Q"], coords["I"], color=SECTION, stroke_width=5)
        l_marker = self.marker(coords["L"], "L", AUX, LEFT + DOWN)
        i_marker = self.marker(coords["I"], "I", AUX, RIGHT + UP)
        li_markers = VGroup(l_marker, i_marker)
        top_definitions = VGroup(
            label("先延長上表面的 PQ", 28, INK, "BOLD"),
            label("L = PQ 與 FG 延長線的交點", 24, AUX, "MEDIUM"),
            label("I = PQ 與 GH 延長線的交點", 24, AUX, "MEDIUM"),
            MathTex(r"L\,-\,P\,-\,Q\,-\,I", font_size=35, color=SECTION),
            label("點在正方形外，仍在同一個面所在的平面", 21, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.33).move_to([3.65, 0.05, 0])

        self.play(
            FadeOut(trace_notes),
            cube["faces"]["back"].animate.set_fill(BLUE, opacity=0.025),
            qr.animate.set_opacity(0.28),
            run_time=0.6,
        )
        self.play(Create(fg_extension), Create(gh_extension), FadeIn(top_definitions[0]), run_time=0.8)
        self.play(Create(lp_extension), GrowFromCenter(l_marker[0]), FadeIn(l_marker[1]), FadeIn(top_definitions[1]))
        # Beat 06 land_top_extension: settled semantic step.
        self.next_slide()
        self.play(Create(qi_extension), GrowFromCenter(i_marker[0]), FadeIn(i_marker[1]), FadeIn(top_definitions[2]))
        self.play(Write(top_definitions[3]), FadeIn(top_definitions[4]), run_time=0.75)

        # Beat 07 extend_right_line: settled semantic step.
        self.next_slide()

        ir_line = Line(coords["I"], coords["J"], color=SECTION, stroke_width=5).set_z_index(3)
        cg_extension = DashedLine(
            coords["G"], coords["J"], color=HAIRLINE, stroke_width=2, dash_length=0.11
        )
        m_marker = self.marker(coords["M"], "M", BLUE, LEFT + UP)
        j_marker = self.marker(coords["J"], "J", AUX, RIGHT + DOWN)
        mj_markers = VGroup(m_marker, j_marker)
        right_definitions = VGroup(
            label("換到右表面 CDHG", 28, INK, "BOLD"),
            label("I、R 都在這個面的延伸平面", 24, MUTED, "MEDIUM"),
            label("延長 IR，先通過題目給的 M", 24, BLUE, "MEDIUM"),
            label("J = IR 與 CG 延長線的交點", 24, AUX, "MEDIUM"),
            MathTex(r"I\,-\,R\,-\,M\,-\,J", font_size=35, color=SECTION),
        ).arrange(DOWN, buff=0.35).move_to([3.65, 0.02, 0])

        self.play(
            FadeOut(top_definitions),
            cube["faces"]["top"].animate.set_fill(BLUE, opacity=0.035),
            cube["faces"]["right"].animate.set_fill(PURPLE, opacity=0.16),
            VGroup(pq, lp_extension, qi_extension).animate.set_opacity(0.3),
            run_time=0.65,
        )
        self.play(FadeIn(right_definitions[0]), FadeIn(right_definitions[1]), Create(cg_extension))
        self.play(Create(ir_line), FadeIn(right_definitions[2]), run_time=0.9)
        # Beat 08 land_right_extension: settled semantic step.
        self.next_slide()
        self.play(GrowFromCenter(m_marker[0]), FadeIn(m_marker[1]), run_time=0.45)
        self.play(GrowFromCenter(j_marker[0]), FadeIn(j_marker[1]), FadeIn(right_definitions[3]))
        self.play(Write(right_definitions[4]), run_time=0.55)

        # Beat 09 locate_n: settled semantic step.
        self.next_slide()

        lj_line = Line(coords["L"], coords["J"], color=SECTION, stroke_width=6).set_z_index(3)
        n_marker = self.marker(coords["N"], "N", TARGET, LEFT)
        fn_segment = Line(coords["F"], coords["N"], color=TARGET, stroke_width=9).set_z_index(4)
        front_definitions = VGroup(
            label("前表面 BCGF 需要兩個共同點", 28, INK, "BOLD"),
            label("L 在 FG 延長線，J 在 CG 延長線", 24, AUX, "MEDIUM"),
            label("L、J 同時也在截平面", 24, SECTION, "MEDIUM"),
            label("所以 LJ 就是前表面的截線", 25, SECTION, "BOLD"),
            MathTex(r"N=LJ\cap FB", font_size=39, color=TARGET),
            label("先找到位置，比例仍然未知", 22, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.31).move_to([3.65, 0.02, 0])

        self.play(
            FadeOut(right_definitions),
            cube["faces"]["right"].animate.set_fill(PURPLE, opacity=0.03),
            cube["faces"]["front"].animate.set_fill(REGION, opacity=0.16),
            ir_line.animate.set_opacity(0.32),
            FadeIn(front_definitions[0]),
            run_time=0.7,
        )
        self.play(FadeIn(front_definitions[1]), Indicate(l_marker[0]), Indicate(j_marker[0]))
        self.play(FadeIn(front_definitions[2]), run_time=0.55)
        # Beat 10 confirm_point_n: settled semantic step.
        self.next_slide()
        self.play(Create(lj_line), FadeIn(front_definitions[3]), run_time=0.95)
        self.play(GrowFromCenter(n_marker[0]), FadeIn(n_marker[1]), Write(front_definitions[4]))
        self.play(Create(fn_segment), FadeIn(front_definitions[5]), Circumscribe(n_marker, color=TARGET), run_time=0.9)

        # Beat 11 unfold_three_faces: settled semantic step.
        self.next_slide()

        top_flat = self.flat_face("top", np.array([-6.15, -2.0, 0.0]), 1.75, label_scale=0.88)
        right_flat = self.flat_face("right", np.array([-0.85, -2.0, 0.0]), 1.75, label_scale=0.88)
        front_flat = self.flat_face("front", np.array([4.2, -2.0, 0.0]), 1.75, label_scale=0.88)
        face_captions = VGroup(
            label("上表面", 24, BLUE, "BOLD").move_to([-5.28, 2.18, 0]),
            label("右表面", 24, PURPLE, "BOLD").move_to([0.02, 2.18, 0]),
            label("前表面", 24, REGION, "BOLD").move_to([5.08, 2.18, 0]),
        )
        unfold_prompt = label("比例不在透視圖上猜；讓長度一個面接一個面傳遞", 28, INK, "BOLD")
        unfold_prompt.move_to([0, 3.15, 0])
        spatial_geometry = VGroup(
            cube["group"],
            plane_patch,
            pqr_markers,
            midpoint_ticks,
            pq,
            qr,
            fg_extension,
            gh_extension,
            lp_extension,
            qi_extension,
            li_markers,
            ir_line,
            cg_extension,
            mj_markers,
            lj_line,
            n_marker,
            fn_segment,
        )
        mini_spatial = spatial_geometry.copy().scale(0.22).move_to([6.65, 2.85, 0])

        self.play(FadeOut(front_definitions), run_time=0.5)
        self.play(
            TransformFromCopy(cube["faces"]["top"], top_flat["face"]),
            TransformFromCopy(cube["faces"]["right"], right_flat["face"]),
            TransformFromCopy(cube["faces"]["front"], front_flat["face"]),
            run_time=1.15,
        )
        self.play(
            ReplacementTransform(spatial_geometry, mini_spatial),
            FadeIn(top_flat["details"]),
            FadeIn(right_flat["details"]),
            FadeIn(front_flat["details"]),
            FadeIn(face_captions),
            FadeIn(unfold_prompt),
            run_time=1.25,
        )

        # Beat 12 top_left_ratio: settled semantic step.
        self.next_slide()

        top_large = self.flat_face("top", np.array([-5.25, -2.25, 0.0]), 2.7, label_scale=1.08)
        tc = top_large["coords"]
        title_8 = label("上表面｜先把 EQ 傳到 LF", 29, INK, "BOLD")
        title_8.move_to([3.35, 2.78, 0])
        tri_peq = self.triangle([tc["P"], tc["E"], tc["Q"]], POINT)
        tri_pfl = self.triangle([tc["P"], tc["F"], tc["L"]], BLUE)
        right_e = RightAngle(Line(tc["E"], tc["P"]), Line(tc["E"], tc["Q"]), length=0.17, color=MUTED)
        right_f = RightAngle(Line(tc["F"], tc["P"]), Line(tc["F"], tc["L"]), length=0.17, color=MUTED)
        angle_p_top = self.minor_arc(tc["P"], tc["E"], tc["Q"], POINT, radius=0.25)
        angle_p_bottom = self.minor_arc(tc["P"], tc["F"], tc["L"], BLUE, radius=0.25)
        angle_marks_8 = VGroup(right_e, right_f, angle_p_top, angle_p_bottom)
        similarity_8 = MathTex(
            r"\triangle PEQ", r"\sim", r"\triangle PFL", font_size=38, color=INK
        )
        similarity_8[0].set_color(POINT)
        similarity_8[2].set_color(BLUE)
        reason_8 = label("兩個直角，加上 P 的對頂角", 22, MUTED, "MEDIUM")
        half_8 = MathTex(r"PE=PF=\frac a2", font_size=37, color=INK)
        equal_8 = MathTex(r"LF=EQ", font_size=39, color=SECTION)
        result_8 = MathTex(r"LF=EQ=\frac{2a}{5}", font_size=45, color=SECTION)
        panel_8 = VGroup(similarity_8, reason_8, half_8, equal_8, result_8)
        panel_8.arrange(DOWN, buff=0.34).move_to([3.4, 0.0, 0])
        eq_length_8 = self.measurement_label(
            r"\frac{2a}{5}", (tc["E"] + tc["Q"]) / 2, UP, POINT, size=25
        )
        pe_length_8 = self.measurement_label(
            r"\frac a2", (tc["E"] + tc["P"]) / 2, LEFT, POINT, size=24
        )
        pf_length_8 = self.measurement_label(
            r"\frac a2", (tc["P"] + tc["F"]) / 2, LEFT, BLUE, size=24
        )
        lf_length_8 = self.measurement_label(
            r"\frac{2a}{5}", (tc["L"] + tc["F"]) / 2, DOWN, SECTION, size=25
        )
        diagram_lengths_8 = VGroup(eq_length_8, pe_length_8, pf_length_8, lf_length_8)

        self.play(
            FadeOut(right_flat["group"]),
            FadeOut(front_flat["group"]),
            FadeOut(face_captions),
            FadeOut(unfold_prompt),
            FadeOut(mini_spatial),
            ReplacementTransform(top_flat["group"], top_large["group"]),
            FadeIn(title_8),
            run_time=1.0,
        )
        self.play(FadeIn(tri_peq), FadeIn(tri_pfl), Create(angle_marks_8), run_time=0.85)
        self.play(Write(similarity_8), FadeIn(reason_8), run_time=0.8)
        # Beat 13 record_top_left_ratio: settled semantic step.
        self.next_slide()
        self.play(FadeIn(pe_length_8), FadeIn(pf_length_8), Write(half_8))
        self.play(FadeIn(eq_length_8), Write(equal_8), run_time=0.65)
        self.play(TransformFromCopy(eq_length_8, lf_length_8), ReplacementTransform(equal_8, result_8), run_time=0.85)

        # Beat 14 top_right_ratio: settled semantic step.
        self.next_slide()

        title_9 = label("上表面｜再把 2:3 傳到 I", 29, INK, "BOLD").move_to(title_8)
        tri_ihq = self.triangle([tc["I"], tc["H"], tc["Q"]], BLUE)
        right_h = RightAngle(Line(tc["H"], tc["I"]), Line(tc["H"], tc["Q"]), length=0.17, color=MUTED)
        angle_q_left = self.minor_arc(tc["Q"], tc["P"], tc["E"], POINT, radius=0.25)
        angle_q_right = self.minor_arc(tc["Q"], tc["I"], tc["H"], BLUE, radius=0.25)
        angle_marks_9 = VGroup(right_e.copy(), right_h, angle_q_left, angle_q_right)
        similarity_9 = MathTex(
            r"\triangle PEQ", r"\sim", r"\triangle IHQ", font_size=38, color=INK
        )
        similarity_9[0].set_color(POINT)
        similarity_9[2].set_color(BLUE)
        ratio_9 = MathTex(r"EQ:QH=PE:HI=2:3", font_size=36, color=INK)
        hi_result_9 = MathTex(r"HI=\frac{3a}{4}", font_size=41, color=BLUE)
        ig_build_9 = MathTex(r"IG=IH+HG", font_size=37, color=INK)
        ig_result_9 = MathTex(r"IG=\frac{3a}{4}+a=\frac{7a}{4}", font_size=43, color=SECTION)
        panel_9 = VGroup(similarity_9, ratio_9, hi_result_9, ig_build_9, ig_result_9)
        panel_9.arrange(DOWN, buff=0.33).move_to([3.45, -0.02, 0])
        hi_length_9 = self.measurement_label(
            r"\frac{3a}{4}", (tc["I"] + tc["H"]) / 2, RIGHT, BLUE, size=24
        )
        hg_length_9 = self.measurement_label(
            "a", (tc["H"] + tc["G"]) / 2, RIGHT, POINT, size=25
        )
        ig_line_9 = Line(tc["I"], tc["G"], color=SECTION, stroke_width=7).set_opacity(0.52)
        ig_length_9 = self.measurement_label(
            r"\frac{7a}{4}", (tc["I"] + tc["G"]) / 2, RIGHT, SECTION, size=27, buff=0.38
        )

        self.play(
            Transform(title_8, title_9),
            FadeOut(VGroup(tri_pfl, angle_marks_8, similarity_8, reason_8, half_8, result_8)),
            FadeOut(VGroup(pe_length_8, pf_length_8, lf_length_8)),
            FadeIn(tri_ihq),
            Create(angle_marks_9),
            run_time=0.85,
        )
        self.play(Write(similarity_9), Write(ratio_9), run_time=0.85)
        self.play(Write(hi_result_9), FadeIn(hi_length_9), run_time=0.7)
        # Beat 15 record_top_right_ratio: settled semantic step.
        self.next_slide()
        self.play(Write(ig_build_9), FadeIn(hg_length_9), run_time=0.65)
        self.play(Create(ig_line_9), Write(ig_result_9), FadeIn(ig_length_9), run_time=0.9)

        # Beat 16 right_face_ratio: settled semantic step.
        self.next_slide()

        right_large = self.flat_face("right", np.array([-5.05, -1.95, 0.0]), 2.85, label_scale=1.08)
        rc = right_large["coords"]
        title_10 = label("右表面｜相似三角形把長度傳到 GJ", 29, INK, "BOLD")
        title_10.move_to([3.42, 2.75, 0])
        tri_ihr = self.triangle([rc["I"], rc["H"], rc["R"]], POINT)
        tri_igj = self.triangle([rc["I"], rc["G"], rc["J"]], BLUE)
        right_h_10 = RightAngle(Line(rc["H"], rc["I"]), Line(rc["H"], rc["R"]), length=0.18, color=MUTED)
        right_g_10 = RightAngle(Line(rc["G"], rc["I"]), Line(rc["G"], rc["J"]), length=0.18, color=MUTED)
        angle_i_small = self.minor_arc(rc["I"], rc["H"], rc["R"], POINT, radius=0.25)
        angle_i_large = self.minor_arc(rc["I"], rc["G"], rc["J"], BLUE, radius=0.36)
        angle_marks_10 = VGroup(right_h_10, right_g_10, angle_i_small, angle_i_large)
        similarity_10 = MathTex(r"\triangle IHR\sim\triangle IGJ", font_size=39, color=INK)
        known_10 = MathTex(
            r"HI=\frac{3a}{4},\quad IG=\frac{7a}{4},\quad HR=\frac a2",
            font_size=34,
            color=INK,
        )
        proportion_10 = MathTex(r"HI:IG=HR:GJ", font_size=38, color=SECTION)
        substitute_10 = MathTex(
            r"\frac{3a}{4}:\frac{7a}{4}=\frac a2:GJ", font_size=39, color=INK
        )
        gj_result_10 = MathTex(r"GJ=\frac{7a}{6}", font_size=47, color=SECTION)
        panel_10 = VGroup(similarity_10, known_10, proportion_10, substitute_10, gj_result_10)
        panel_10.arrange(DOWN, buff=0.32).move_to([3.42, -0.02, 0])
        hi_length_10 = self.measurement_label(
            r"HI=\frac{3a}{4}", (rc["I"] + rc["H"]) / 2, UP, BLUE, size=23
        )
        ig_length_10 = self.measurement_label(
            r"IG=\frac{7a}{4}", (rc["I"] + rc["G"]) / 2, UP, SECTION, size=24, buff=0.3
        )
        hr_length_10 = self.measurement_label(
            r"\frac a2", (rc["H"] + rc["R"]) / 2, RIGHT, POINT, size=24
        )
        gj_length_10 = self.measurement_label(
            r"\frac{7a}{6}", (rc["G"] + rc["J"]) / 2, RIGHT, SECTION, size=26
        )

        top_ratio_objects = VGroup(
            top_large["group"],
            tri_peq,
            tri_ihq,
            angle_marks_9,
            similarity_9,
            ratio_9,
            hi_result_9,
            ig_build_9,
            ig_result_9,
            eq_length_8,
            hi_length_9,
            hg_length_9,
            ig_line_9,
            ig_length_9,
            title_8,
        )
        self.play(FadeOut(top_ratio_objects), FadeIn(right_large["group"]), FadeIn(title_10), run_time=0.9)
        self.play(FadeIn(tri_ihr), FadeIn(tri_igj), Create(angle_marks_10), Write(similarity_10))
        self.play(
            TransformFromCopy(hi_result_9, known_10),
            FadeIn(hi_length_10),
            FadeIn(ig_length_10),
            FadeIn(hr_length_10),
            run_time=0.85,
        )
        # Beat 17 record_right_face_ratio: settled semantic step.
        self.next_slide()
        self.play(Write(proportion_10), run_time=0.6)
        self.play(Write(substitute_10), run_time=0.7)
        self.play(Write(gj_result_10), TransformFromCopy(gj_result_10, gj_length_10), run_time=0.8)

        # Beat 18 front_face_ratio: settled semantic step.
        self.next_slide()

        front_large = self.flat_face("front", np.array([-5.35, -1.95, 0.0]), 3.0, label_scale=1.08)
        fc = front_large["coords"]
        title_11 = label("前表面｜最後把長度傳到 FN", 29, INK, "BOLD")
        title_11.move_to([3.42, 2.75, 0])
        tri_lfn = self.triangle([fc["L"], fc["F"], fc["N"]], POINT)
        tri_lgj = self.triangle([fc["L"], fc["G"], fc["J"]], BLUE)
        right_f_11 = RightAngle(Line(fc["F"], fc["L"]), Line(fc["F"], fc["N"]), length=0.18, color=MUTED)
        right_g_11 = RightAngle(Line(fc["G"], fc["L"]), Line(fc["G"], fc["J"]), length=0.18, color=MUTED)
        angle_l_small = self.minor_arc(fc["L"], fc["F"], fc["N"], POINT, radius=0.25)
        angle_l_large = self.minor_arc(fc["L"], fc["G"], fc["J"], BLUE, radius=0.36)
        angle_marks_11 = VGroup(right_f_11, right_g_11, angle_l_small, angle_l_large)
        similarity_11 = MathTex(r"\triangle LFN\sim\triangle LGJ", font_size=39, color=INK)
        lg_build_11 = MathTex(
            r"LG=LF+FG=\frac{2a}{5}+a=\frac{7a}{5}", font_size=35, color=INK
        )
        proportion_11 = MathTex(r"LF:LG=FN:GJ", font_size=38, color=SECTION)
        substitute_11 = MathTex(
            r"\frac{2a}{5}:\frac{7a}{5}=FN:\frac{7a}{6}", font_size=38, color=INK
        )
        fn_result_11 = MathTex(r"FN=\frac a3", font_size=49, color=TARGET)
        panel_11 = VGroup(similarity_11, lg_build_11, proportion_11, substitute_11, fn_result_11)
        panel_11.arrange(DOWN, buff=0.32).move_to([3.4, -0.02, 0])
        lf_length_11 = self.measurement_label(
            r"LF=\frac{2a}{5}", (fc["L"] + fc["F"]) / 2, UP, POINT, size=23
        )
        fg_length_11 = self.measurement_label(
            "a", (fc["F"] + fc["G"]) / 2, UP, POINT, size=24
        )
        lg_length_11 = self.measurement_label(
            r"LG=\frac{7a}{5}", (fc["L"] + fc["G"]) / 2, DOWN, SECTION, size=24, buff=0.28
        )
        gj_length_11 = self.measurement_label(
            r"GJ=\frac{7a}{6}", (fc["G"] + fc["J"]) / 2, RIGHT, SECTION, size=24
        )
        fn_length_11 = self.measurement_label(
            r"\frac a3", (fc["F"] + fc["N"]) / 2, LEFT, TARGET, size=28
        )

        right_ratio_objects = VGroup(
            right_large["group"],
            tri_ihr,
            tri_igj,
            angle_marks_10,
            similarity_10,
            known_10,
            proportion_10,
            substitute_10,
            gj_result_10,
            hi_length_10,
            ig_length_10,
            hr_length_10,
            gj_length_10,
            title_10,
        )
        self.play(FadeOut(right_ratio_objects), FadeIn(front_large["group"]), FadeIn(title_11), run_time=0.9)
        self.play(FadeIn(tri_lfn), FadeIn(tri_lgj), Create(angle_marks_11), Write(similarity_11))
        self.play(FadeIn(lf_length_11), FadeIn(fg_length_11), Write(lg_build_11), run_time=0.85)
        # Beat 19 record_front_face_ratio: settled semantic step.
        self.next_slide()
        self.play(FadeIn(lg_length_11), Write(proportion_11), FadeIn(gj_length_11), run_time=0.75)
        self.play(Write(substitute_11), run_time=0.7)
        self.play(Write(fn_result_11), TransformFromCopy(fn_result_11, fn_length_11), run_time=0.8)

        # Beat 20 finish_ratio: settled semantic step.
        self.next_slide()

        f_bar = np.array([-3.9, 2.35, 0.0])
        b_bar = np.array([-3.9, -2.45, 0.0])
        n_bar = b_bar + (2 / 3) * (f_bar - b_bar)
        fn_bar = Line(f_bar, n_bar, color=TARGET, stroke_width=18)
        nb_bar = Line(n_bar, b_bar, color=BLUE, stroke_width=18)
        bar_ticks = VGroup(
            Line(f_bar + LEFT * 0.2, f_bar + RIGHT * 0.2, color=INK, stroke_width=3),
            Line(n_bar + LEFT * 0.24, n_bar + RIGHT * 0.24, color=INK, stroke_width=3),
            Line(b_bar + LEFT * 0.2, b_bar + RIGHT * 0.2, color=INK, stroke_width=3),
        )
        bar_labels = VGroup(
            MathTex("F", font_size=30, color=INK).next_to(f_bar, LEFT, buff=0.25),
            MathTex("N", font_size=30, color=TARGET).next_to(n_bar, LEFT, buff=0.25),
            MathTex("B", font_size=30, color=INK).next_to(b_bar, LEFT, buff=0.25),
            MathTex(r"\frac a3", font_size=35, color=TARGET).next_to((f_bar + n_bar) / 2, RIGHT, buff=0.38),
            MathTex(r"\frac{2a}{3}", font_size=35, color=BLUE).next_to((n_bar + b_bar) / 2, RIGHT, buff=0.38),
            MathTex("FB=a", font_size=35, color=POINT).move_to([-5.55, -0.05, 0]),
        )
        bar_group = VGroup(fn_bar, nb_bar, bar_ticks, bar_labels)
        title_12 = label("回到同一條邊：先看見 1 份和 2 份", 30, INK, "BOLD")
        title_12.move_to([2.75, 2.85, 0])
        known_fn_12 = MathTex(r"FN=\frac a3", font_size=42, color=TARGET)
        whole_12 = MathTex("FB=a", font_size=39, color=POINT)
        nb_build_12 = MathTex(
            r"NB=FB-FN=a-\frac a3=\frac{2a}{3}", font_size=39, color=BLUE
        )
        partition_12 = MathTex(r"FN:NB=1:2", font_size=45, color=INK)
        final_ratio_12 = MathTex(r"\frac{FN}{NB}=\frac12", font_size=58, color=TARGET)
        final_box_12 = SurroundingRectangle(final_ratio_12, color=TARGET, buff=0.25, stroke_width=3)
        ratio_panel_12 = VGroup(whole_12, known_fn_12, nb_build_12, partition_12, final_ratio_12, final_box_12)
        whole_12.move_to([3.15, 1.55, 0])
        known_fn_12.move_to([3.15, 0.72, 0])
        nb_build_12.move_to([3.15, -0.2, 0])
        partition_12.move_to([3.15, -1.22, 0])
        final_ratio_12.move_to([3.15, -2.35, 0])
        final_box_12.move_to(final_ratio_12)

        front_ratio_objects = VGroup(
            front_large["group"],
            tri_lfn,
            tri_lgj,
            angle_marks_11,
            similarity_11,
            lg_build_11,
            proportion_11,
            substitute_11,
            fn_result_11,
            lf_length_11,
            fg_length_11,
            lg_length_11,
            gj_length_11,
            fn_length_11,
            title_11,
        )
        self.play(FadeOut(front_ratio_objects), FadeIn(title_12), Create(fn_bar), run_time=0.8)
        self.play(FadeIn(bar_ticks[0]), FadeIn(bar_ticks[1]), FadeIn(bar_labels[0]), FadeIn(bar_labels[1]))
        self.play(TransformFromCopy(fn_result_11, bar_labels[3]), Write(known_fn_12), run_time=0.75)
        # Beat 21 combine_face_ratios: settled semantic step.
        self.next_slide()
        self.play(Create(nb_bar), FadeIn(bar_ticks[2]), FadeIn(bar_labels[2]), FadeIn(bar_labels[5]), Write(whole_12))
        self.play(Write(nb_build_12), FadeIn(bar_labels[4]), run_time=0.85)
        # Beat 22 simplify_space_ratio: settled semantic step.
        self.next_slide()
        self.play(Write(partition_12), run_time=0.65)
        self.play(Write(final_ratio_12), Create(final_box_12), run_time=0.8)

        # Beat 23 consolidate: settled semantic step.
        self.next_slide()

        recap_cube = mini_spatial.copy().scale(1.8).move_to([-5.35, -0.35, 0])
        recap_title = label("一條截線，跨過三個面", 31, INK, "BOLD")
        recap_title.move_to([1.9, 3.05, 0])
        top_icon = self.summary_face("top", np.array([-0.45, 1.15, 0.0]), BLUE)
        right_icon = self.summary_face("right", np.array([2.15, 1.15, 0.0]), PURPLE)
        front_icon = self.summary_face("front", np.array([4.8, 1.15, 0.0]), REGION)
        icons = VGroup(top_icon, right_icon, front_icon)
        icon_captions = VGroup(
            label("上表面", 21, BLUE, "BOLD").next_to(top_icon, UP, buff=0.18),
            label("右表面", 21, PURPLE, "BOLD").next_to(right_icon, UP, buff=0.18),
            label("前表面", 21, REGION, "BOLD").next_to(front_icon, UP, buff=0.18),
        )
        flow_arrows = VGroup(
            Arrow(top_icon.get_right() + RIGHT * 0.1, right_icon.get_left() + LEFT * 0.1, color=MUTED, buff=0.08, stroke_width=2.5),
            Arrow(right_icon.get_right() + RIGHT * 0.1, front_icon.get_left() + LEFT * 0.1, color=MUTED, buff=0.08, stroke_width=2.5),
        )
        recap_values = VGroup(
            MathTex(r"LF=\frac{2a}{5},\ IG=\frac{7a}{4}", font_size=29, color=BLUE),
            MathTex(r"GJ=\frac{7a}{6}", font_size=31, color=PURPLE),
            MathTex(r"FN=\frac a3", font_size=31, color=REGION),
        )
        for value, icon in zip(recap_values, icons, strict=True):
            value.next_to(icon, DOWN, buff=0.26)
        path_recap = VGroup(
            MathTex(r"PQ\to L,I", font_size=31, color=SECTION),
            MathTex(r"IR\to J", font_size=31, color=SECTION),
            MathTex(r"LJ\cap FB=N", font_size=31, color=TARGET),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-5.25, -2.62, 0])
        nb_recap = MathTex(r"NB=\frac{2a}{3}", font_size=37, color=BLUE)
        nb_recap.move_to([2.15, -1.48, 0])
        final_recap = MathTex(r"\frac{FN}{NB}=\frac12", font_size=59, color=TARGET)
        final_recap.move_to([2.15, -2.7, 0])
        final_recap_box = SurroundingRectangle(final_recap, color=TARGET, buff=0.24, stroke_width=3)

        self.play(FadeOut(VGroup(title_12, bar_group, ratio_panel_12)), FadeIn(recap_cube), FadeIn(recap_title), run_time=0.85)
        self.play(FadeIn(icons), FadeIn(icon_captions), run_time=0.75)
        self.play(LaggedStart(*(GrowArrow(arrow) for arrow in flow_arrows), lag_ratio=0.3), run_time=0.75)
        # Beat 24 reveal_space_ratio: settled semantic step.
        self.next_slide()
        self.play(LaggedStart(*(Write(value) for value in recap_values), lag_ratio=0.22), run_time=1.0)
        self.play(FadeIn(path_recap), Write(nb_recap), run_time=0.75)
        self.play(TransformFromCopy(final_ratio_12, final_recap), Create(final_recap_box), run_time=0.85)
