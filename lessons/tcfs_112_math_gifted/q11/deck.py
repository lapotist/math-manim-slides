"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q11."""

from __future__ import annotations

from fractions import Fraction
from math import pi

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
    Angle,
    Arc,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    RightAngle,
    Rotate,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
    ValueTracker,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ExactPoint = tuple[Fraction, Fraction]


def vector(start: ExactPoint, end: ExactPoint) -> ExactPoint:
    return (end[0] - start[0], end[1] - start[1])


def dot(first: ExactPoint, second: ExactPoint) -> Fraction:
    return first[0] * second[0] + first[1] * second[1]


def determinant(first: ExactPoint, second: ExactPoint) -> Fraction:
    return first[0] * second[1] - first[1] * second[0]


def squared_distance(first: ExactPoint, second: ExactPoint) -> Fraction:
    displacement = vector(first, second)
    return dot(displacement, displacement)


def rotate_quarter_turn_ccw(point: ExactPoint, center: ExactPoint) -> ExactPoint:
    displacement = vector(center, point)
    return (
        center[0] - displacement[1],
        center[1] + displacement[0],
    )


def condition_holds(
    point: ExactPoint,
    a: ExactPoint,
    b: ExactPoint,
    c: ExactPoint,
) -> bool:
    return 2 * squared_distance(b, point) == (
        squared_distance(c, point) - squared_distance(a, point)
    )


UNIT_D: ExactPoint = (Fraction(0), Fraction(0))
UNIT_A: ExactPoint = (Fraction(0), Fraction(1))
UNIT_B: ExactPoint = (Fraction(1), Fraction(1))
UNIT_C: ExactPoint = (Fraction(1), Fraction(0))
INTERIOR_POINTS: tuple[ExactPoint, ...] = (
    (Fraction(2, 5), Fraction(4, 5)),
    (Fraction(3, 5), Fraction(4, 5)),
)

for exact_point in INTERIOR_POINTS:
    if not condition_holds(exact_point, UNIT_A, UNIT_B, UNIT_C):
        raise ValueError("an exact interior sample no longer satisfies the condition")
    pa = vector(exact_point, UNIT_A)
    pb = vector(exact_point, UNIT_B)
    if not (dot(pa, pb) < 0 and abs(determinant(pa, pb)) == -dot(pa, pb)):
        raise ValueError("the exact interior vector signature must encode 135 degrees")

for parameter in (Fraction(1, 4), Fraction(1, 3), Fraction(2, 5), Fraction(1, 2)):
    u = (1 - parameter) / (1 + parameter * parameter)
    v = parameter * u
    path_point = (1 - u, 1 - v)
    if not (
        0 < path_point[0] < 1
        and 0 < path_point[1] < 1
        and condition_holds(path_point, UNIT_A, UNIT_B, UNIT_C)
    ):
        raise ValueError("the rational exploration path must stay valid and interior")

EXACT_P = INTERIOR_POINTS[0]
EXACT_E = rotate_quarter_turn_ccw(EXACT_P, UNIT_B)
if rotate_quarter_turn_ccw(UNIT_A, UNIT_B) != UNIT_C:
    raise ValueError("the square quarter-turn must map A to C")
if squared_distance(UNIT_B, EXACT_E) != squared_distance(UNIT_B, EXACT_P):
    raise ValueError("rotation must preserve BP as BE")
if squared_distance(UNIT_C, EXACT_E) != squared_distance(UNIT_A, EXACT_P):
    raise ValueError("rotation must preserve AP as CE")
if squared_distance(EXACT_P, EXACT_E) != 2 * squared_distance(UNIT_B, EXACT_P):
    raise ValueError("the right-isosceles diagonal must satisfy PE^2=2BP^2")
if squared_distance(UNIT_C, EXACT_P) != (
    squared_distance(UNIT_C, EXACT_E) + squared_distance(EXACT_E, EXACT_P)
):
    raise ValueError("the constructed triangle CEP must satisfy Pythagoras")
if dot(vector(EXACT_E, UNIT_C), vector(EXACT_E, EXACT_P)) != 0:
    raise ValueError("the exact construction must make angle CEP right")

OUTSIDE_P: ExactPoint = (Fraction(0), Fraction(2))
if not condition_holds(OUTSIDE_P, UNIT_A, UNIT_B, UNIT_C):
    raise ValueError("the exact outside counterexample must preserve the distance condition")
outside_pa = vector(OUTSIDE_P, UNIT_A)
outside_pb = vector(OUTSIDE_P, UNIT_B)
if not (
    dot(outside_pa, outside_pb) > 0
    and abs(determinant(outside_pa, outside_pb)) == dot(outside_pa, outside_pb)
):
    raise ValueError("the outside counterexample must encode 45 rather than 135 degrees")


class CarloTcfs112MathQ11(CarloSlide):
    """Turn the coefficient two into a visible rotated diagonal."""

    lesson_id = "carlo.tcfs_112_math_gifted.q11"

    @staticmethod
    def stage_title(text: str):
        title = label(text, 31, INK, "BOLD")
        title.move_to([0, 3.72, 0])
        return title

    @staticmethod
    def segment_label(
        expression: str,
        start: np.ndarray,
        end: np.ndarray,
        offset: np.ndarray,
        color: str,
        *,
        size: int = 29,
    ) -> MathTex:
        result = MathTex(expression, font_size=size, color=color)
        result.move_to((start + end) / 2 + offset)
        return result

    @staticmethod
    def tick_marks(
        start: np.ndarray,
        end: np.ndarray,
        color: str,
        *,
        count: int = 1,
    ) -> VGroup:
        direction = end - start
        unit = direction / np.linalg.norm(direction)
        normal = np.array([-unit[1], unit[0], 0.0])
        midpoint = (start + end) / 2
        offsets = [0.0] if count == 1 else [-0.10, 0.10]
        return VGroup(
            *(
                Line(
                    midpoint + unit * offset - normal * 0.105,
                    midpoint + unit * offset + normal * 0.105,
                    color=color,
                    stroke_width=3.2,
                )
                for offset in offsets
            )
        )

    @staticmethod
    def formula_card(
        expression: str,
        *,
        center: np.ndarray,
        width: float = 6.0,
        font_size: int = 39,
        stroke_color: str = HAIRLINE,
    ) -> VGroup:
        formula = MathTex(expression, font_size=font_size, color=INK)
        formula.move_to(center)
        frame = RoundedRectangle(
            width=width,
            height=max(1.10, formula.height + 0.48),
            corner_radius=0.08,
            color=stroke_color,
            stroke_width=1.8,
            fill_color="#171B1F",
            fill_opacity=0.90,
        ).move_to(center)
        return VGroup(frame, formula)

    @staticmethod
    def replace_title(scene: "CarloTcfs112MathQ11", old, text: str):
        new = scene.stage_title(text)
        scene.play(FadeOut(old), run_time=0.24)
        scene.play(FadeIn(new), run_time=0.34)
        return new

    def construct(self) -> None:
        left = -5.70
        bottom = -2.18
        side = 4.08
        d = np.array([left, bottom, 0.0])
        a = d + np.array([0.0, side, 0.0])
        b = d + np.array([side, side, 0.0])
        c = d + np.array([side, 0.0, 0.0])

        def p_from_parameter(parameter: float) -> np.ndarray:
            u = (1.0 - parameter) / (1.0 + parameter * parameter)
            v = parameter * u
            return d + np.array([(1.0 - u) * side, (1.0 - v) * side, 0.0])

        tracker = ValueTracker(1.0 / 3.0)
        p = p_from_parameter(tracker.get_value())

        # Beat 01 meet_square_and_inner_point: establish only the square, the interior point, and three distances.
        self.begin_beat("meet_square_and_inner_point")
        title = self.stage_title("正方形裡的一個點")
        square = Polygon(a, b, c, d, color=INK, stroke_width=3.2)
        square.set_fill(BLUE, opacity=0.025)
        vertex_labels = VGroup(
            MathTex("A", font_size=30, color=INK).next_to(a, LEFT + UP, buff=0.10),
            MathTex("B", font_size=30, color=INK).next_to(b, RIGHT + UP, buff=0.10),
            MathTex("C", font_size=30, color=INK).next_to(c, RIGHT + DOWN, buff=0.10),
            MathTex("D", font_size=30, color=INK).next_to(d, LEFT + DOWN, buff=0.10),
        )
        p_dot = Dot(p, radius=0.095, color=POINT, z_index=5)
        p_name = MathTex("P", font_size=31, color=POINT).move_to(p + np.array([-0.22, 0.28, 0]))
        ap = Line(p, a, color=BLUE, stroke_width=4.2)
        bp = Line(p, b, color=POINT, stroke_width=4.2)
        cp = Line(p, c, color=PURPLE, stroke_width=4.2)
        ap_name = self.segment_label("AP", p, a, np.array([-0.28, 0.08, 0]), BLUE)
        bp_name = self.segment_label("BP", p, b, np.array([0.10, 0.24, 0]), POINT)
        cp_name = self.segment_label("CP", p, c, np.array([0.26, -0.08, 0]), PURPLE)
        interior_note = label("P 在正方形內部", 25, POINT, "BOLD")
        interior_note.move_to([3.35, 1.25, 0])
        no_diagonal_note = label("不假設 A、P、C 共線", 23, MUTED, "MEDIUM")
        no_diagonal_note.move_to([3.35, 0.52, 0])
        self.play(FadeIn(title), Create(square), FadeIn(vertex_labels), run_time=0.85)
        self.play(FadeIn(p_dot), FadeIn(p_name), FadeIn(interior_note), run_time=0.58)
        self.play(
            LaggedStart(Create(ap), Create(bp), Create(cp), lag_ratio=0.20),
            run_time=1.10,
        )
        self.play(FadeIn(ap_name), FadeIn(bp_name), FadeIn(cp_name), FadeIn(no_diagonal_note))
        self.wait(0.45)

        # Beat 02 test_two_valid_positions: move along an exact constraint-preserving arc, then return.
        self.next_beat("test_two_valid_positions")
        title = self.replace_title(self, title, "條件成立時，P 不只一個位置")
        condition = self.formula_card(
            r"2BP^2=CP^2-AP^2",
            center=np.array([3.35, 0.65, 0]),
            width=6.0,
            font_size=43,
            stroke_color=PURPLE,
        )
        condition[1].set_color_by_tex("BP", POINT)
        condition[1].set_color_by_tex("CP", PURPLE)
        condition[1].set_color_by_tex("AP", BLUE)
        valid_note = label("沿條件移動，再回到代表位置", 23, MUTED, "MEDIUM")
        valid_note.move_to([3.35, -0.55, 0])

        p_dot.add_updater(lambda mob: mob.move_to(p_from_parameter(tracker.get_value())))
        p_name.add_updater(
            lambda mob: mob.move_to(
                p_from_parameter(tracker.get_value()) + np.array([-0.22, 0.28, 0])
            )
        )
        ap.add_updater(
            lambda mob: mob.put_start_and_end_on(p_from_parameter(tracker.get_value()), a)
        )
        bp.add_updater(
            lambda mob: mob.put_start_and_end_on(p_from_parameter(tracker.get_value()), b)
        )
        cp.add_updater(
            lambda mob: mob.put_start_and_end_on(p_from_parameter(tracker.get_value()), c)
        )
        ap_name.add_updater(
            lambda mob: mob.move_to(
                (p_from_parameter(tracker.get_value()) + a) / 2
                + np.array([-0.28, 0.08, 0])
            )
        )
        bp_name.add_updater(
            lambda mob: mob.move_to(
                (p_from_parameter(tracker.get_value()) + b) / 2
                + np.array([0.10, 0.24, 0])
            )
        )
        cp_name.add_updater(
            lambda mob: mob.move_to(
                (p_from_parameter(tracker.get_value()) + c) / 2
                + np.array([0.26, -0.08, 0])
            )
        )
        self.play(
            Succession(
                FadeOut(VGroup(interior_note, no_diagonal_note)),
                FadeIn(condition),
            ),
            run_time=0.66,
        )
        self.play(FadeIn(valid_note), tracker.animate.set_value(0.5), run_time=1.45)
        self.play(tracker.animate.set_value(1.0 / 3.0), run_time=1.45)
        self.play(Indicate(condition[1], color=REGION), run_time=0.65)
        for moving_object in (p_dot, p_name, ap, bp, cp, ap_name, bp_name, cp_name):
            moving_object.clear_updaters()
        p = p_from_parameter(1.0 / 3.0)
        self.wait(0.42)

        # Beat 03 ask_for_target_angle: isolate the angle without assigning a value.
        self.next_beat("ask_for_target_angle")
        title = self.replace_title(self, title, "三段平方距離，鎖定哪一個角？")
        target_angle = Angle(
            Line(p, b),
            Line(p, a),
            radius=0.58,
            color=CORAL,
            stroke_width=5.0,
            other_angle=False,
        )
        target_question = MathTex("?", font_size=45, color=CORAL)
        target_question.move_to(p + np.array([0.00, 0.48, 0]))
        target_name = MathTex(r"\angle APB", font_size=47, color=CORAL)
        target_name.move_to([3.35, -0.92, 0])
        self.play(
            FadeOut(valid_note),
            cp.animate.set_opacity(0.34),
            cp_name.animate.set_opacity(0.34),
            square.animate.set_stroke(opacity=0.48),
            run_time=0.55,
        )
        self.play(Create(target_angle), FadeIn(target_question), FadeIn(target_name), run_time=0.78)
        self.play(Indicate(target_name, color=CORAL), run_time=0.60)
        self.wait(0.65)

        # Beat 04 demonstrate_quarter_turn: rotate a full colored copy of triangle ABP about fixed B.
        self.next_beat("demonstrate_quarter_turn")
        title = self.replace_title(self, title, "讓正方形的直角搬動整個三角形")
        self.play(
            FadeOut(condition),
            FadeOut(target_name),
            FadeOut(target_question),
            target_angle.animate.set_stroke(opacity=0.25),
            cp.animate.set_opacity(1.0),
            cp_name.animate.set_opacity(1.0),
            run_time=0.62,
        )
        ba_probe = Line(b, a, color=MUTED, stroke_width=5.0)
        quarter_arc = Arc(
            radius=0.56,
            start_angle=pi,
            angle=pi / 2,
            arc_center=b,
            color=REGION,
            stroke_width=4.2,
        )
        quarter_value = MathTex(r"90^\circ", font_size=28, color=REGION)
        quarter_value.move_to(b + np.array([-0.62, -0.58, 0]))
        self.play(Create(ba_probe), run_time=0.45)
        self.play(
            Rotate(ba_probe, angle=pi / 2, about_point=b),
            Create(quarter_arc),
            FadeIn(quarter_value),
            run_time=1.05,
        )
        self.play(FadeOut(ba_probe), run_time=0.30)

        # Beat 05 rotate_point_about_b: continue at a settled semantic boundary.
        self.next_beat("rotate_point_about_b")

        rot_ba = Line(b, a, color=MUTED, stroke_width=3.0)
        rot_ap = Line(a, p, color=BLUE, stroke_width=5.0)
        rot_pb = Line(p, b, color=POINT, stroke_width=5.0)
        rot_a_dot = Dot(a, radius=0.065, color=MUTED)
        rot_p_dot = Dot(p, radius=0.085, color=POINT)
        rotating_triangle = VGroup(rot_ba, rot_ap, rot_pb, rot_a_dot, rot_p_dot)
        self.add(rotating_triangle)
        self.play(
            Rotate(rotating_triangle, angle=pi / 2, about_point=b),
            run_time=1.55,
        )
        e = b + np.array([-(p - b)[1], (p - b)[0], 0.0])
        e_name = MathTex("E", font_size=31, color=POINT).move_to(
            e + np.array([0.28, -0.02, 0])
        )
        rotation_caption = label("同一個四分之一圈", 25, REGION, "BOLD")
        rotation_caption.move_to([3.35, 0.82, 0])
        mapping = MathTex(r"A\mapsto C,\qquad P\mapsto E", font_size=42, color=INK)
        mapping.move_to([3.35, -0.02, 0])
        self.play(FadeIn(e_name), FadeIn(rotation_caption), FadeIn(mapping), run_time=0.72)
        self.wait(0.45)

        # Beat 06 match_rotated_lengths: record the two preserved lengths and the preserved target angle.
        self.next_beat("match_rotated_lengths")
        title = self.replace_title(self, title, "旋轉保留長度，也保留角")
        ce = rot_ap
        eb = rot_pb
        ap_ticks = self.tick_marks(p, a, BLUE, count=2)
        ce_ticks = self.tick_marks(c, e, BLUE, count=2)
        bp_ticks = self.tick_marks(p, b, POINT)
        eb_ticks = self.tick_marks(e, b, POINT)
        angle_e = Angle(
            Line(e, b),
            Line(e, c),
            radius=0.66,
            color=CORAL,
            stroke_width=4.2,
            other_angle=False,
        )
        preserved_one = MathTex(r"AP=CE", font_size=43, color=INK)
        preserved_one.set_color_by_tex("AP", BLUE)
        preserved_one.set_color_by_tex("CE", BLUE)
        preserved_one.move_to([3.35, 1.22, 0])
        preserved_two = MathTex(r"BP=BE", font_size=43, color=INK)
        preserved_two.set_color_by_tex("BP", POINT)
        preserved_two.set_color_by_tex("BE", POINT)
        preserved_two.move_to([3.35, 0.30, 0])
        preserved_angle = MathTex(r"\angle APB=\angle CEB", font_size=42, color=CORAL)
        preserved_angle.move_to([3.35, -0.82, 0])
        self.play(FadeOut(rotation_caption), FadeOut(mapping), run_time=0.38)
        self.play(
            LaggedStart(
                FadeIn(ap_ticks),
                FadeIn(ce_ticks),
                FadeIn(preserved_one),
                lag_ratio=0.22,
            ),
            run_time=0.92,
        )
        self.play(
            LaggedStart(
                FadeIn(bp_ticks),
                FadeIn(eb_ticks),
                FadeIn(preserved_two),
                lag_ratio=0.22,
            ),
            run_time=0.92,
        )
        self.play(
            Create(angle_e),
            FadeIn(preserved_angle),
            target_angle.animate.set_stroke(opacity=1.0),
            run_time=0.85,
        )
        self.wait(0.48)

        # Beat 07 construct_rotated_diagonal: build PE and make the coefficient two visible.
        self.next_beat("construct_rotated_diagonal")
        title = self.replace_title(self, title, "直角等腰三角形，把 2 變成一條邊")
        self.play(
            FadeOut(preserved_one),
            FadeOut(preserved_two),
            FadeOut(preserved_angle),
            FadeOut(angle_e),
            FadeOut(quarter_arc),
            FadeOut(quarter_value),
            run_time=0.50,
        )
        triangle_bpe = Polygon(
            b,
            p,
            e,
            color=POINT,
            stroke_width=1.8,
            fill_color=POINT,
            fill_opacity=0.08,
        )
        right_b = RightAngle(
            Line(b, p),
            Line(b, e),
            length=0.23,
            color=REGION,
            stroke_width=3.4,
        )
        pe = Line(p, e, color=REGION, stroke_width=5.0)
        pe_name = self.segment_label(
            "PE", p, e, np.array([0.02, 0.28, 0]), REGION, size=30
        )
        diagonal_steps = VGroup(
            MathTex(r"PE^2=PB^2+BE^2", font_size=42, color=INK),
            MathTex(r"PE^2=BP^2+BP^2", font_size=42, color=INK),
            MathTex(r"PE^2=2BP^2", font_size=50, color=REGION),
        ).arrange(DOWN, buff=0.42)
        diagonal_steps.move_to([3.40, 0.10, 0])
        for formula in diagonal_steps[:2]:
            formula.set_color_by_tex("PE", REGION)
            formula.set_color_by_tex("PB", POINT)
            formula.set_color_by_tex("BP", POINT)
            formula.set_color_by_tex("BE", POINT)
        self.play(FadeIn(triangle_bpe), Create(right_b), run_time=0.65)
        self.play(Create(pe), FadeIn(pe_name), run_time=0.72)

        # Beat 08 measure_the_new_diagonal: continue at a settled semantic boundary.
        self.next_beat("measure_the_new_diagonal")
        self.play(
            Indicate(bp, color=POINT),
            Indicate(eb, color=POINT),
            FadeIn(diagonal_steps[0]),
            run_time=0.78,
        )
        self.play(FadeIn(diagonal_steps[1]), run_time=0.64)
        self.play(FadeIn(diagonal_steps[2]), Indicate(pe, color=REGION), run_time=0.75)
        self.wait(0.50)

        # Beat 09 match_condition_lengths: substitute the visible rotated lengths into the given equation.
        self.next_beat("match_condition_lengths")
        title = self.replace_title(self, title, "把題設完整搬進三角形 CEP")
        self.play(FadeOut(diagonal_steps[0]), FadeOut(diagonal_steps[1]), run_time=0.42)
        moved_condition = MathTex(
            r"CP^2=AP^2+2BP^2",
            font_size=43,
            color=INK,
        )
        moved_condition.set_color_by_tex("CP", PURPLE)
        moved_condition.set_color_by_tex("AP", BLUE)
        moved_condition.set_color_by_tex("BP", POINT)
        moved_condition.move_to([3.40, 1.12, 0])
        final_condition = MathTex(
            r"CP^2=CE^2+PE^2",
            font_size=50,
            color=INK,
        )
        final_condition.set_color_by_tex("CP", PURPLE)
        final_condition.set_color_by_tex("CE", BLUE)
        final_condition.set_color_by_tex("PE", REGION)
        final_condition.move_to([3.40, -0.25, 0])
        substitution_note = label("旋轉像與新斜邊，逐項換回圖上", 22, MUTED, "MEDIUM")
        substitution_note.move_to([3.40, -1.30, 0])
        self.play(FadeIn(moved_condition), run_time=0.70)
        self.play(
            Indicate(ap, color=BLUE),
            Indicate(ce, color=BLUE),
            run_time=0.62,
        )
        self.play(Indicate(diagonal_steps[2], color=REGION), run_time=0.56)

        # Beat 10 translate_the_condition: continue at a settled semantic boundary.
        self.next_beat("translate_the_condition")
        self.play(FadeOut(diagonal_steps[2]), run_time=0.34)
        self.play(FadeIn(final_condition), run_time=0.82)
        self.play(FadeIn(substitution_note), run_time=0.45)
        self.wait(0.48)

        # Beat 11 earn_the_right_angle: use the converse of Pythagoras only after all three sides are visible.
        self.next_beat("earn_the_right_angle")
        title = self.replace_title(self, title, "等式落定後，直角才有根據")
        triangle_cep = Polygon(
            c,
            e,
            p,
            color=REGION,
            stroke_width=2.5,
            fill_color=REGION,
            fill_opacity=0.12,
        )
        self.play(
            FadeOut(substitution_note),
            FadeOut(moved_condition),
            FadeOut(triangle_bpe),
            bp.animate.set_opacity(0.20),
            eb.animate.set_opacity(0.20),
            square.animate.set_stroke(opacity=0.24),
            ap.animate.set_opacity(0.22),
            run_time=0.56,
        )
        self.play(FadeIn(triangle_cep), Indicate(final_condition, color=REGION), run_time=0.75)
        right_e = RightAngle(
            Line(e, c),
            Line(e, p),
            length=0.25,
            color=REGION,
            stroke_width=3.6,
        )
        right_statement = MathTex(r"\angle CEP=90^\circ", font_size=49, color=REGION)
        right_statement.move_to([3.40, -1.22, 0])
        converse_note = label("CP 的平方等於另外兩邊平方和", 23, MUTED, "MEDIUM")
        converse_note.move_to([3.40, 1.03, 0])
        self.play(FadeIn(converse_note), run_time=0.42)
        self.play(Create(right_e), FadeIn(right_statement), run_time=0.82)
        self.wait(0.52)

        # Beat 12 show_forty_five_and_ninety: assemble 90 and 45, but hold the sum behind a question mark.
        self.next_beat("show_forty_five_and_ninety")
        title = self.replace_title(self, title, "兩塊角已經齊了，先停在最後加法")
        self.play(
            FadeOut(final_condition),
            FadeOut(converse_note),
            FadeOut(right_statement),
            FadeOut(triangle_cep),
            bp.animate.set_opacity(1.0),
            eb.animate.set_opacity(1.0),
            ap.animate.set_opacity(0.46),
            square.animate.set_stroke(opacity=0.42),
            run_time=0.58,
        )
        self.play(FadeIn(triangle_bpe), run_time=0.42)
        base_angle = Angle(
            Line(e, p),
            Line(e, b),
            radius=0.48,
            color=POINT,
            stroke_width=4.2,
        )
        base_value = MathTex(r"45^\circ", font_size=29, color=POINT)
        base_value.move_to(e + np.array([-0.43, 0.48, 0]))
        right_value = MathTex(r"90^\circ", font_size=29, color=REGION)
        right_value.move_to(e + np.array([-0.55, -0.36, 0]))
        combined_angle = Angle(
            Line(e, b),
            Line(e, c),
            radius=0.95,
            color=CORAL,
            stroke_width=5.0,
            other_angle=False,
        )
        preanswer = VGroup(
            MathTex(r"\angle APB=\angle CEB", font_size=41, color=CORAL),
            MathTex(r"=90^\circ+45^\circ", font_size=48, color=INK),
            MathTex(r"=?", font_size=55, color=CORAL),
        ).arrange(DOWN, buff=0.36)
        preanswer.move_to([3.42, 0.02, 0])
        self.play(Create(base_angle), FadeIn(base_value), run_time=0.65)
        self.play(FadeIn(right_value), Indicate(right_e, color=REGION), run_time=0.55)

        # Beat 13 assemble_preanswer_angles: continue at a settled semantic boundary.
        self.next_beat("assemble_preanswer_angles")
        self.play(Create(combined_angle), run_time=0.68)
        self.play(FadeIn(preanswer[0]), FadeIn(preanswer[1]), run_time=0.82)
        self.play(FadeIn(preanswer[2]), run_time=0.48)
        self.wait(1.15)

        # Beat 14 reveal_the_angle: reveal the number only now and reconnect it to the original P.
        self.next_beat("reveal_the_angle")
        title = self.replace_title(self, title, "把旋轉後的合角送回原來的 P")
        answer = MathTex(r"\angle APB=135^\circ", font_size=61, color=CORAL)
        answer.move_to([3.42, 0.12, 0])
        answer_frame = SurroundingRectangle(
            answer,
            color=POINT,
            stroke_width=2.8,
            buff=0.25,
            corner_radius=0.07,
        )
        self.play(FadeOut(preanswer), run_time=0.36)
        self.play(FadeIn(answer), run_time=0.72)
        self.play(Create(answer_frame), Indicate(combined_angle, color=CORAL), run_time=0.72)
        self.play(
            target_angle.animate.set_stroke(opacity=1.0),
            Indicate(target_angle, color=CORAL),
            run_time=0.70,
        )

        # Beat 15 name_quarter_turn_insight: continue at a settled semantic boundary.
        self.next_beat("name_quarter_turn_insight")
        answer_note = label("四分之一圈保留了整個角", 23, MUTED, "MEDIUM")
        answer_note.move_to([3.42, -1.08, 0])
        self.play(FadeIn(answer_note), run_time=0.42)
        self.wait(0.66)

        # Beat 16 set_up_interior_vectors: independently verify the quadrant with coordinates and vectors.
        self.next_beat("set_up_interior_vectors")
        title = self.replace_title(self, title, "用內部條件做一次獨立向量核對")
        old_stage = VGroup(
            square,
            vertex_labels,
            p_dot,
            p_name,
            ap,
            bp,
            cp,
            ap_name,
            bp_name,
            cp_name,
            target_angle,
            rotating_triangle,
            e_name,
            ap_ticks,
            ce_ticks,
            bp_ticks,
            eb_ticks,
            triangle_bpe,
            right_b,
            pe,
            pe_name,
            right_e,
            base_angle,
            base_value,
            right_value,
            combined_angle,
            answer,
            answer_frame,
            answer_note,
        )
        self.play(FadeOut(old_stage), run_time=0.68)

        d2 = np.array([-6.18, -2.12, 0.0])
        side2 = 3.72
        a2 = d2 + np.array([0.0, side2, 0.0])
        b2 = d2 + np.array([side2, side2, 0.0])
        c2 = d2 + np.array([side2, 0.0, 0.0])
        p2 = d2 + np.array([0.40 * side2, 0.80 * side2, 0.0])
        square2 = Polygon(a2, b2, c2, d2, color=MUTED, stroke_width=2.7)
        point2 = Dot(p2, radius=0.09, color=POINT)
        point2_name = MathTex("P", font_size=29, color=POINT).move_to(
            p2 + np.array([-0.22, 0.27, 0])
        )
        coordinate_labels = VGroup(
            MathTex("A", font_size=27, color=INK).next_to(a2, LEFT + UP, buff=0.08),
            MathTex("B", font_size=27, color=INK).next_to(b2, RIGHT + UP, buff=0.08),
            MathTex("C", font_size=27, color=INK).next_to(c2, RIGHT + DOWN, buff=0.08),
            MathTex("D", font_size=27, color=INK).next_to(d2, LEFT + DOWN, buff=0.08),
        )
        horizontal_foot = np.array([b2[0], p2[1], 0.0])
        vertical_foot = np.array([p2[0], b2[1], 0.0])
        u_line = DashedLine(p2, horizontal_foot, color=BLUE, stroke_width=3.0)
        v_line = DashedLine(p2, vertical_foot, color=REGION, stroke_width=3.0)
        u_name = MathTex("u", font_size=31, color=BLUE).move_to(
            (p2 + horizontal_foot) / 2 + DOWN * 0.19
        )
        v_name = MathTex("v", font_size=31, color=REGION).move_to(
            (p2 + vertical_foot) / 2 + LEFT * 0.20
        )
        pa_arrow = Arrow(p2, a2, buff=0.08, color=BLUE, stroke_width=4.1)
        pb_arrow = Arrow(p2, b2, buff=0.08, color=POINT, stroke_width=4.1)
        positive = MathTex(r"u>0,\qquad v>0", font_size=37, color=INK)
        positive.set_color_by_tex("u", BLUE)
        positive.set_color_by_tex("v", REGION)
        positive.move_to([-4.30, -2.88, 0])
        self.play(Create(square2), FadeIn(coordinate_labels), FadeIn(point2), FadeIn(point2_name))
        self.play(Create(u_line), Create(v_line), FadeIn(u_name), FadeIn(v_name), FadeIn(positive), run_time=0.78)
        self.play(GrowArrow(pa_arrow), GrowArrow(pb_arrow), run_time=0.76)

        # Beat 17 derive_negative_dot_product: continue at a settled semantic boundary.
        self.next_beat("derive_negative_dot_product")

        vector_steps = VGroup(
            MathTex(r"u^2+v^2=s(u-v)", font_size=37, color=INK),
            MathTex(
                r"\overrightarrow{PA}=(u-s,v),\quad\overrightarrow{PB}=(u,v)",
                font_size=34,
                color=INK,
            ),
            MathTex(
                r"\overrightarrow{PA}\cdot\overrightarrow{PB}=-sv<0",
                font_size=38,
                color=CORAL,
            ),
            MathTex(
                r"\left|\det(\overrightarrow{PA},\overrightarrow{PB})\right|=sv",
                font_size=35,
                color=REGION,
            ),
        ).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        vector_steps.move_to([3.25, 0.62, 0])
        quadrant_note = label("內積為負：先鎖定鈍角", 23, CORAL, "BOLD")
        quadrant_note.move_to([3.30, -1.35, 0])
        trig_check = MathTex(
            r"\sin\theta=-\cos\theta\quad\Longrightarrow\quad\theta=135^\circ",
            font_size=42,
            color=INK,
        )
        trig_check.set_color_by_tex("135", CORAL)
        trig_check.move_to([3.30, -2.25, 0])
        self.play(FadeIn(vector_steps[0]), run_time=0.58)
        self.play(FadeIn(vector_steps[1]), run_time=0.70)
        self.play(FadeIn(vector_steps[2]), FadeIn(quadrant_note), run_time=0.72)

        # Beat 18 verify_with_interior_vectors: continue at a settled semantic boundary.
        self.next_beat("verify_with_interior_vectors")
        self.play(FadeIn(vector_steps[3]), run_time=0.68)
        self.play(FadeIn(trig_check), run_time=0.78)
        self.play(Indicate(positive, color=POINT), Indicate(trig_check, color=CORAL), run_time=0.68)
        self.wait(0.58)

        # Beat 19 return_to_original_square: return to the original object and consolidate the earned route.
        self.next_beat("return_to_original_square")
        title = self.replace_title(self, title, "回到原圖：記住四分之一圈的用途")
        coordinate_stage = VGroup(
            square2,
            coordinate_labels,
            point2,
            point2_name,
            u_line,
            v_line,
            u_name,
            v_name,
            pa_arrow,
            pb_arrow,
            positive,
            vector_steps,
            quadrant_note,
            trig_check,
        )
        self.play(FadeOut(coordinate_stage), run_time=0.68)

        final_square = Polygon(a, b, c, d, color=INK, stroke_width=3.0)
        final_square.set_fill(BLUE, opacity=0.025)
        final_p = Dot(p, radius=0.095, color=POINT)
        final_p_name = MathTex("P", font_size=30, color=POINT).move_to(
            p + np.array([-0.22, 0.28, 0])
        )
        final_ap = Line(p, a, color=BLUE, stroke_width=4.2)
        final_bp = Line(p, b, color=POINT, stroke_width=4.2)
        final_cp = Line(p, c, color=PURPLE, stroke_width=4.2)
        final_target = Angle(
            Line(p, b),
            Line(p, a),
            radius=0.58,
            color=CORAL,
            stroke_width=5.0,
            other_angle=False,
        )
        final_vertices = VGroup(
            MathTex("A", font_size=28, color=INK).next_to(a, LEFT + UP, buff=0.09),
            MathTex("B", font_size=28, color=INK).next_to(b, RIGHT + UP, buff=0.09),
            MathTex("C", font_size=28, color=INK).next_to(c, RIGHT + DOWN, buff=0.09),
            MathTex("D", font_size=28, color=INK).next_to(d, LEFT + DOWN, buff=0.09),
        )
        final_answer = MathTex(r"\angle APB=135^\circ", font_size=60, color=CORAL)
        final_answer.move_to([3.42, 1.14, 0])
        final_frame = SurroundingRectangle(
            final_answer,
            color=POINT,
            stroke_width=2.8,
            buff=0.24,
            corner_radius=0.07,
        )

        step_texts = (
            ("四分之一圈", r"AP\mapsto CE", BLUE),
            ("直角等腰", r"PE^2=2BP^2", REGION),
            ("兩塊角", r"90^\circ+45^\circ", CORAL),
        )
        summary_steps = VGroup()
        for heading_text, expression, color in step_texts:
            frame = RoundedRectangle(
                width=2.70,
                height=1.32,
                corner_radius=0.07,
                color=HAIRLINE,
                stroke_width=1.6,
                fill_color="#171B1F",
                fill_opacity=0.90,
            )
            heading = label(heading_text, 20, color, "BOLD")
            formula = MathTex(expression, font_size=30, color=INK)
            content = VGroup(heading, formula).arrange(DOWN, buff=0.16)
            content.move_to(frame)
            summary_steps.add(VGroup(frame, content))
        summary_steps.arrange(RIGHT, buff=0.22)
        summary_steps.move_to([3.45, -0.58, 0])
        final_footer = label("解題來源：正哥愛數學｜原創重繪與獨立核對", 18, MUTED, "MEDIUM")
        final_footer.move_to([0, -4.07, 0])
        self.play(
            Create(final_square),
            FadeIn(final_vertices),
            FadeIn(final_p),
            FadeIn(final_p_name),
            run_time=0.72,
        )
        self.play(
            LaggedStart(Create(final_ap), Create(final_bp), Create(final_cp), lag_ratio=0.18),
            run_time=0.92,
        )
        self.play(Create(final_target), FadeIn(final_answer), Create(final_frame), run_time=0.88)

        # Beat 20 summarize_quarter_turn_route: continue at a settled semantic boundary.
        self.next_beat("summarize_quarter_turn_route")
        self.play(LaggedStart(*(FadeIn(step) for step in summary_steps), lag_ratio=0.20), run_time=0.95)
        self.play(FadeIn(final_footer), run_time=0.42)
        self.wait(0.72)


if __name__ == "__main__":
    raise SystemExit(
        "Render with: pixi run manim-slides render --quality h "
        "--media_dir build/media/carlo_tcfs_112_math_gifted_q11 "
        "lessons/tcfs_112_math_gifted/q11/deck.py CarloTcfs112MathQ11"
    )
