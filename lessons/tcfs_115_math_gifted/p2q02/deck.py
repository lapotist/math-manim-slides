"""Manim Slides lesson for TCFS 115 mathematics gifted assessment Part 2 Q2."""

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
    Circle,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    SurroundingRectangle,
    Succession,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


class Tcfs115Part2Q02Slide(CarloSlide):
    """Build the angle-bisector length formula from two AA similarities."""

    lesson_id = "carlo.tcfs_115_math_gifted.p2q02"

    @staticmethod
    def point_on_circle(center: np.ndarray, radius: float, degrees: float) -> np.ndarray:
        angle = np.deg2rad(degrees)
        return center + radius * np.array([np.cos(angle), np.sin(angle), 0.0])

    @staticmethod
    def minor_angle_arc(
        vertex: np.ndarray,
        first: np.ndarray,
        second: np.ndarray,
        *,
        radius: float,
        color: str,
    ) -> Arc:
        first_angle = np.arctan2(first[1] - vertex[1], first[0] - vertex[0])
        second_angle = np.arctan2(second[1] - vertex[1], second[0] - vertex[0])
        sweep = (second_angle - first_angle) % (2 * np.pi)
        if sweep > np.pi:
            first_angle, second_angle = second_angle, first_angle
            sweep = (second_angle - first_angle) % (2 * np.pi)
        return Arc(
            radius=radius,
            start_angle=first_angle,
            angle=sweep,
            arc_center=vertex,
            color=color,
            stroke_width=5,
        )

    @staticmethod
    def mini_triangle(names: tuple[str, str, str], center: np.ndarray) -> VGroup:
        top = center + UP * 1.05
        lower_left = center + LEFT * 1.0 + DOWN * 0.72
        lower_right = center + RIGHT * 1.05 + DOWN * 0.72
        body = Polygon(
            top,
            lower_left,
            lower_right,
            color=INK,
            stroke_width=3,
            fill_color=BLUE,
            fill_opacity=0.05,
        )
        dots = VGroup(
            Dot(top, radius=0.055, color=POINT),
            Dot(lower_left, radius=0.055, color=REGION),
            Dot(lower_right, radius=0.055, color=PURPLE),
        )
        labels = VGroup(
            label(names[0], 22, POINT, "BOLD").next_to(dots[0], UP, buff=0.08),
            label(names[1], 22, REGION, "BOLD").next_to(dots[1], DOWN, buff=0.08),
            label(names[2], 22, PURPLE, "BOLD").next_to(dots[2], DOWN, buff=0.08),
        )
        caption = label("".join(names), 23, INK, "BOLD")
        caption.next_to(body, DOWN, buff=0.48)
        return VGroup(body, dots, labels, caption)

    @staticmethod
    def receipt(tex: str, color: str, center: np.ndarray) -> VGroup:
        equation = MathTex(tex, font_size=39, color=INK)
        frame = Rectangle(
            width=equation.width + 0.50,
            height=equation.height + 0.42,
            color=color,
            stroke_width=3,
            fill_color=color,
            fill_opacity=0.07,
        )
        result = VGroup(frame, equation).move_to(center)
        return result

    def construct(self) -> None:
        center = np.array([-3.65, -0.25, 0.0])
        radius = 3.0
        point_a = self.point_on_circle(center, radius, 100)
        point_b = self.point_on_circle(center, radius, 218)
        point_c = self.point_on_circle(center, radius, 335)

        length_ab = np.linalg.norm(point_a - point_b)
        length_ac = np.linalg.norm(point_a - point_c)
        point_d = (length_ac * point_b + length_ab * point_c) / (length_ab + length_ac)
        direction_ad = point_d - point_a
        second_parameter = (
            -2 * np.dot(point_a - center, direction_ad)
            / np.dot(direction_ad, direction_ad)
        )
        point_e = point_a + second_parameter * direction_ad

        heading = label("第二部分第 2 題｜兩組相似，拼出角平分線長度", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.38)
        source = label("解題來源：正哥愛數學｜PDF 第 10 頁", 16, MUTED, "MEDIUM")
        source.to_corner(DOWN + RIGHT, buff=0.24)
        self.add(heading, source)

        side_ab = Line(point_a, point_b, color=INK, stroke_width=4)
        side_bc = Line(point_b, point_c, color=INK, stroke_width=4)
        side_ca = Line(point_c, point_a, color=INK, stroke_width=4)
        line_ad = Line(point_a, point_d, color=BLUE, stroke_width=5)
        line_de = Line(point_d, point_e, color=REGION, stroke_width=4)
        chord_ce = Line(point_c, point_e, color=INK, stroke_width=3.5)
        circumcircle = Circle(radius=radius, color=HAIRLINE, stroke_width=2.5)
        circumcircle.move_to(center).set_z_index(-4)

        dot_a = Dot(point_a, radius=0.075, color=WHITE).set_z_index(6)
        dot_b = Dot(point_b, radius=0.075, color=WHITE).set_z_index(6)
        dot_c = Dot(point_c, radius=0.075, color=WHITE).set_z_index(6)
        dot_d = Dot(point_d, radius=0.075, color=BLUE).set_z_index(7)
        dot_e = Dot(point_e, radius=0.075, color=REGION).set_z_index(7)
        name_a = label("A", 24, INK, "BOLD").next_to(dot_a, UP, buff=0.10)
        name_b = label("B", 24, INK, "BOLD").next_to(dot_b, LEFT, buff=0.10)
        name_c = label("C", 24, INK, "BOLD").next_to(dot_c, RIGHT, buff=0.10)
        name_d = label("D", 24, BLUE, "BOLD").next_to(dot_d, UP + RIGHT, buff=0.09)
        name_e = label("E", 24, REGION, "BOLD").next_to(dot_e, DOWN, buff=0.10)

        # Beat 01: keep the initial object deliberately sparse.
        self.begin_beat("build_triangle")
        opening = label("先只看一般三角形 ABC", 33, INK, "BOLD")
        opening.move_to([3.30, 1.75, 0])
        question = label("哪一條局部關係，能把特殊線段連到三邊？", 28, MUTED, "MEDIUM")
        question.move_to([3.30, 0.55, 0])

        self.play(
            LaggedStart(Create(side_ab), Create(side_bc), Create(side_ca), lag_ratio=0.18),
            run_time=1.25,
        )
        self.play(
            FadeIn(dot_a), FadeIn(dot_b), FadeIn(dot_c),
            FadeIn(name_a), FadeIn(name_b), FadeIn(name_c),
            FadeIn(opening), FadeIn(question),
            run_time=0.8,
        )
        self.wait(0.30)

        # Beat 02: establish AD through its defining equal angles.
        self.next_beat("place_angle_bisector")
        angle_bad = self.minor_angle_arc(
            point_a, point_b, point_d, radius=0.38, color=POINT
        )
        angle_dac = self.minor_angle_arc(
            point_a, point_d, point_c, radius=0.50, color=POINT
        )
        ad_tag = MathTex("AD", font_size=31, color=BLUE)
        ad_tag.move_to((point_a + point_d) / 2 + RIGHT * 0.24)
        bisector_title = label("AD 平分 ∠BAC", 33, INK, "BOLD")
        bisector_title.move_to(opening)
        equal_angles = MathTex(
            r"\angle BAD=\angle DAC",
            font_size=43,
            color=POINT,
        ).move_to([3.30, 0.45, 0])
        target_note = label("先記住這條藍色長度；公式稍後才出現", 26, MUTED, "MEDIUM")
        target_note.move_to([3.30, -0.75, 0])

        self.play(
            Succession(FadeOut(opening), FadeIn(bisector_title)),
            FadeOut(question),
            Create(line_ad),
            FadeIn(dot_d), FadeIn(name_d), FadeIn(ad_tag),
            run_time=0.9,
        )
        self.play(Create(angle_bad), Create(angle_dac), run_time=0.7)
        self.play(FadeIn(equal_angles), FadeIn(target_note), run_time=0.7)
        self.wait(0.30)

        # Beat 03: the circle creates a second intersection on the same ray.
        self.next_beat("add_circle_and_e")
        circle_title = label("沿 AD 延長：第二次遇到圓的點叫 E", 31, INK, "BOLD")
        circle_title.move_to(bisector_title)
        collinear = VGroup(
            label("A — D — E 共線", 27, BLUE, "BOLD"),
            label("B — D — C 共線", 27, MUTED, "BOLD"),
        ).arrange(DOWN, buff=0.22).move_to([3.30, 0.10, 0])
        arc_prompt = label("哪些角會被同一段弧鎖定？", 29, POINT, "BOLD")
        arc_prompt.move_to([3.30, -1.25, 0])

        self.play(
            Succession(FadeOut(bisector_title), FadeIn(circle_title)),
            FadeOut(equal_angles), FadeOut(target_note),
            Create(circumcircle),
            run_time=1.0,
        )
        self.play(Create(line_de), FadeIn(dot_e), FadeIn(name_e), run_time=0.8)
        self.play(Create(chord_ce), FadeIn(collinear), FadeIn(arc_prompt), run_time=0.75)
        self.wait(0.30)

        # Beat 04: identify the candidates before supplying angle marks.
        self.next_beat("pose_hidden_similarity")
        triangle_abd = Polygon(
            point_a, point_b, point_d,
            color=POINT, stroke_width=3, fill_color=POINT, fill_opacity=0.10,
        ).set_z_index(-1)
        triangle_aec = Polygon(
            point_a, point_e, point_c,
            color=BLUE, stroke_width=3, fill_color=BLUE, fill_opacity=0.08,
        ).set_z_index(-2)
        triangle_ced = Polygon(
            point_c, point_e, point_d,
            color=REGION, stroke_width=3, fill_color=REGION, fill_opacity=0.10,
        ).set_z_index(-1)
        candidates = VGroup(
            label("△ABD", 29, POINT, "BOLD"),
            label("△AEC", 29, BLUE, "BOLD"),
            label("△CED", 29, REGION, "BOLD"),
        ).arrange(DOWN, buff=0.32).move_to([3.30, 0.15, 0])
        hidden_title = label("三個方向不同的三角形，形狀會相同嗎？", 30, INK, "BOLD")
        hidden_title.move_to(circle_title)

        self.play(
            Succession(FadeOut(circle_title), FadeIn(hidden_title)),
            FadeOut(collinear), FadeOut(arc_prompt),
            run_time=0.5,
        )
        self.play(FadeIn(triangle_abd), FadeIn(candidates[0]), run_time=0.45)
        self.play(Indicate(triangle_abd, color=triangle_abd.get_color()), run_time=0.45)

        self.next_beat("inspect_second_triangle")
        self.play(FadeIn(triangle_aec), FadeIn(candidates[1]), run_time=0.45)
        self.play(Indicate(triangle_aec, color=triangle_aec.get_color()), run_time=0.45)

        self.next_beat("inspect_third_triangle")
        self.play(FadeIn(triangle_ced), FadeIn(candidates[2]), run_time=0.45)
        self.play(Indicate(triangle_ced, color=triangle_ced.get_color()), run_time=0.45)
        self.wait(0.30)

        # Beat 05: first AA proof, with chord AC highlighted before the angles.
        self.next_beat("prove_first_similarity")
        angle_cae = self.minor_angle_arc(
            point_a, point_c, point_e, radius=0.66, color=POINT
        )
        angle_abd = self.minor_angle_arc(
            point_b, point_a, point_d, radius=0.36, color=POINT
        )
        angle_aec = self.minor_angle_arc(
            point_e, point_a, point_c, radius=0.40, color=POINT
        )
        arc_ac = Arc(
            radius=radius,
            start_angle=np.deg2rad(335),
            angle=np.deg2rad(125),
            arc_center=center,
            color=POINT,
            stroke_width=6,
        )
        first_proof_title = label("第一組：ABD 與 AEC", 31, POINT, "BOLD")
        first_proof_title.move_to(hidden_title)
        first_angle_eq = MathTex(
            r"\angle BAD=\angle CAE",
            font_size=37,
            color=INK,
        )
        second_angle_eq = MathTex(
            r"\angle ABD=\angle AEC",
            font_size=37,
            color=INK,
        )
        first_similarity = MathTex(
            r"\triangle ABD\sim\triangle AEC",
            font_size=43,
            color=POINT,
        )
        first_proof = VGroup(first_angle_eq, second_angle_eq, first_similarity)
        first_proof.arrange(DOWN, buff=0.38).move_to([3.30, -0.05, 0])
        first_pairing = label("配對：A↔A｜B↔E｜D↔C", 23, MUTED, "MEDIUM")
        first_pairing.next_to(first_proof, DOWN, buff=0.28)

        self.play(
            Succession(FadeOut(hidden_title), FadeIn(first_proof_title)),
            FadeOut(candidates),
            triangle_ced.animate.set_opacity(0.15),
            run_time=0.6,
        )
        self.play(Create(angle_cae), FadeIn(first_angle_eq), run_time=0.7)
        self.play(Create(arc_ac), run_time=0.7)
        # Smaller step: record_first_similarity_ratio.
        self.next_beat("record_first_similarity_ratio")
        self.play(Create(angle_abd), Create(angle_aec), FadeIn(second_angle_eq), run_time=0.8)
        self.play(FadeIn(first_similarity), FadeIn(first_pairing), run_time=0.75)
        self.wait(0.30)

        # Beat 06: second AA proof uses arc BE and the vertical angles at D.
        self.next_beat("prove_second_similarity")
        angle_bce = self.minor_angle_arc(
            point_c, point_b, point_e, radius=0.48, color=REGION
        )
        angle_adb = self.minor_angle_arc(
            point_d, point_a, point_b, radius=0.36, color=PURPLE
        )
        angle_cde = self.minor_angle_arc(
            point_d, point_c, point_e, radius=0.48, color=PURPLE
        )
        arc_be = Arc(
            radius=radius,
            start_angle=np.deg2rad(218),
            angle=np.deg2rad(58.5),
            arc_center=center,
            color=REGION,
            stroke_width=6,
        )
        second_proof_title = label("第二組：ABD 與 CED", 31, REGION, "BOLD")
        second_proof_title.move_to(first_proof_title)
        second_angle_one = MathTex(
            r"\angle BAD=\angle BCE",
            font_size=37,
            color=INK,
        )
        second_angle_two = MathTex(
            r"\angle ADB=\angle CDE",
            font_size=37,
            color=INK,
        )
        second_similarity = MathTex(
            r"\triangle ABD\sim\triangle CED",
            font_size=43,
            color=REGION,
        )
        second_proof = VGroup(second_angle_one, second_angle_two, second_similarity)
        second_proof.arrange(DOWN, buff=0.38).move_to([3.30, -0.05, 0])
        second_pairing = label("配對：A↔C｜B↔E｜D↔D", 23, MUTED, "MEDIUM")
        second_pairing.next_to(second_proof, DOWN, buff=0.28)

        self.play(
            Succession(FadeOut(first_proof_title), FadeIn(second_proof_title)),
            FadeOut(first_proof), FadeOut(first_pairing),
            FadeOut(arc_ac), FadeOut(angle_cae), FadeOut(angle_abd), FadeOut(angle_aec),
            triangle_ced.animate.set_stroke(opacity=1).set_fill(opacity=0.10),
            triangle_aec.animate.set_opacity(0.15),
            run_time=0.75,
        )
        self.play(Create(arc_be), Create(angle_bce), FadeIn(second_angle_one), run_time=0.8)
        self.play(Create(angle_adb), Create(angle_cde), FadeIn(second_angle_two), run_time=0.8)
        self.play(FadeIn(second_similarity), FadeIn(second_pairing), run_time=0.7)
        self.wait(0.30)

        # Beat 07: redraw the three similar shapes in one common orientation.
        self.next_beat("align_three_triangles")
        mini_abd = self.mini_triangle(("A", "B", "D"), np.array([-4.70, -0.20, 0.0]))
        mini_ced = self.mini_triangle(("C", "E", "D"), np.array([-1.80, -0.20, 0.0]))
        mini_aec = self.mini_triangle(("A", "E", "C"), np.array([1.10, -0.20, 0.0]))
        similarity_chain = MathTex(
            r"\triangle ABD\sim\triangle CED\sim\triangle AEC",
            font_size=38,
            color=INK,
        ).move_to([-1.80, 2.55, 0])
        product_prompt = label("哪兩組比例，能交出題目需要的乘積？", 26, POINT, "BOLD")
        product_prompt.move_to([4.70, -2.40, 0])
        geometry_group = VGroup(
            side_ab, side_bc, side_ca, line_ad, line_de, chord_ce, circumcircle,
            dot_a, dot_b, dot_c, dot_d, dot_e,
            name_a, name_b, name_c, name_d, name_e, ad_tag,
            angle_bad, angle_dac, triangle_abd, triangle_aec, triangle_ced,
            arc_be, angle_bce, angle_adb, angle_cde,
        )

        self.play(
            Succession(
                FadeOut(
                    VGroup(
                        geometry_group,
                        second_proof_title,
                        second_proof,
                        second_pairing,
                    )
                ),
                FadeIn(VGroup(mini_abd, mini_ced, mini_aec, similarity_chain)),
            ),
            run_time=1.2,
        )
        self.play(FadeIn(product_prompt), run_time=0.5)
        self.wait(0.30)

        # Beat 08: the first correspondence yields AB*AC.
        self.next_beat("build_first_product")
        first_ratio = MathTex(
            r"\frac{AB}{AE}=\frac{AD}{AC}",
            font_size=43,
            color=INK,
        ).move_to([4.65, 1.35, 0])
        first_receipt = self.receipt(
            r"AB\cdot AC=AD\cdot AE",
            BLUE,
            np.array([4.65, 0.05, 0.0]),
        )
        receipt_one_note = label("第一張收據：出現 AB·AC", 24, BLUE, "BOLD")
        receipt_one_note.next_to(first_receipt, DOWN, buff=0.24)

        self.play(
            FadeOut(product_prompt),
            mini_ced.animate.set_opacity(0.18),
            Indicate(mini_abd, color=POINT), Indicate(mini_aec, color=BLUE),
            run_time=0.8,
        )
        self.play(FadeIn(first_ratio), run_time=0.65)
        self.play(FadeIn(first_receipt), FadeIn(receipt_one_note), run_time=0.8)
        self.wait(0.30)

        # Beat 09: the second correspondence yields BD*DC.
        self.next_beat("build_second_product")
        second_ratio = MathTex(
            r"\frac{AD}{CD}=\frac{BD}{DE}",
            font_size=43,
            color=INK,
        ).move_to([4.65, 1.35, 0])
        second_receipt = self.receipt(
            r"AD\cdot DE=BD\cdot DC",
            REGION,
            np.array([4.65, -1.45, 0.0]),
        )
        receipt_two_note = label("第二張收據：出現 BD·DC", 24, REGION, "BOLD")
        receipt_two_note.next_to(second_receipt, DOWN, buff=0.24)

        self.play(
            FadeOut(first_ratio),
            FadeOut(receipt_one_note),
            mini_ced.animate.set_opacity(1),
            mini_aec.animate.set_opacity(0.18),
            Indicate(mini_abd, color=POINT), Indicate(mini_ced, color=REGION),
            run_time=0.8,
        )
        self.play(FadeIn(second_ratio), run_time=0.65)
        self.play(FadeIn(second_receipt), FadeIn(receipt_two_note), run_time=0.8)
        self.wait(0.30)

        # Beat 10: the collinear order is the bridge between both receipts.
        self.next_beat("split_ae")
        receipt_one_small = first_receipt.copy().scale(0.68).move_to([5.75, 2.40, 0])
        receipt_two_small = second_receipt.copy().scale(0.68).move_to([5.75, -2.35, 0])
        split_title = label("關鍵橋樑：A — D — E", 31, INK, "BOLD")
        split_title.move_to([2.55, 2.75, 0])
        split_equation = MathTex(r"AE=AD+DE", font_size=43, color=INK)
        split_equation.set_color_by_tex("AD", BLUE)
        split_equation.set_color_by_tex("DE", REGION)
        split_equation.move_to([2.55, 1.75, 0])
        expansion_one = MathTex(
            r"AB\cdot AC=AD\cdot AE",
            font_size=39,
            color=INK,
        ).move_to([2.55, 0.75, 0])
        expansion_two = MathTex(
            r"=AD(AD+DE)",
            font_size=39,
            color=INK,
        ).move_to([2.55, -0.20, 0])
        expansion_three = MathTex(
            r"=AD^2+AD\cdot DE",
            font_size=39,
            color=INK,
        ).move_to([2.55, -1.15, 0])
        expansion_three.set_color_by_tex(r"AD\cdot DE", REGION)
        split_highlight = SurroundingRectangle(
            expansion_three,
            color=REGION,
            buff=0.17,
            stroke_width=2.5,
        )

        self.play(
            FadeOut(VGroup(mini_abd, mini_ced, mini_aec, similarity_chain)),
            FadeOut(second_ratio), FadeOut(receipt_two_note),
            Succession(
                FadeOut(VGroup(first_receipt, second_receipt)),
                FadeIn(VGroup(receipt_one_small, receipt_two_small)),
            ),
            FadeIn(geometry_group),
            FadeIn(split_title),
            run_time=0.9,
        )
        self.play(Indicate(line_ad, color=BLUE), Indicate(line_de, color=REGION), FadeIn(split_equation))
        self.play(FadeIn(expansion_one), run_time=0.7)
        # Smaller step: combine_ae_parts.
        self.next_beat("combine_ae_parts")
        self.play(FadeIn(expansion_two), run_time=0.6)
        self.play(FadeIn(expansion_three), Create(split_highlight), run_time=0.75)
        self.wait(0.30)

        # Beat 11: substitute the second receipt, then move the same product.
        self.next_beat("isolate_ad_square")
        substituted = MathTex(
            r"AB\cdot AC=AD^2+BD\cdot DC",
            font_size=42,
            color=INK,
        ).move_to([3.45, 0.45, 0])
        substituted.set_color_by_tex(r"BD\cdot DC", REGION)
        squared = MathTex(
            r"AD^2=AB\cdot AC-BD\cdot DC",
            font_size=45,
            color=INK,
        ).move_to([3.45, -0.95, 0])
        squared.set_color_by_tex("AD^2", BLUE)
        squared.set_color_by_tex(r"BD\cdot DC", REGION)

        self.play(
            Succession(
                FadeOut(
                    VGroup(
                        split_title,
                        split_equation,
                        expansion_one,
                        expansion_two,
                        expansion_three,
                        split_highlight,
                        receipt_one_small,
                        receipt_two_small,
                    )
                ),
                FadeIn(substituted),
            ),
            run_time=0.9,
        )
        self.play(FadeIn(squared), run_time=0.8)
        self.wait(0.30)

        # Beat 12: length positivity selects one root.
        self.next_beat("take_positive_root")
        positive = MathTex(r"AD>0", font_size=39, color=BLUE)
        positive.move_to([3.35, 1.35, 0])
        final_formula = MathTex(
            r"AD=\sqrt{AB\cdot AC-BD\cdot DC}",
            font_size=47,
            color=INK,
        ).move_to([3.35, -0.10, 0])
        final_formula.set_color_by_tex("AD", BLUE)
        root_note = label("根號內就是 AD²，因此必定非負", 24, MUTED, "MEDIUM")
        root_note.next_to(final_formula, DOWN, buff=0.32)
        formula_frame = SurroundingRectangle(
            final_formula,
            color=POINT,
            buff=0.23,
            stroke_width=3,
        )

        self.play(
            FadeOut(substituted),
            Succession(FadeOut(ad_tag), FadeIn(positive)),
            Indicate(line_ad, color=BLUE),
        )
        self.play(Succession(FadeOut(squared), FadeIn(final_formula)), run_time=0.85)
        self.play(Create(formula_frame), FadeIn(root_note), run_time=0.65)
        self.wait(0.30)

        # Beat 13: preserve a traceable proof structure, not an isolated answer.
        self.next_beat("consolidate")
        recap_one = self.receipt(
            r"AB\cdot AC=AD\cdot AE",
            BLUE,
            np.array([2.85, 1.65, 0.0]),
        ).scale(0.88)
        recap_two = self.receipt(
            r"AD\cdot DE=BD\cdot DC",
            REGION,
            np.array([2.85, 0.35, 0.0]),
        ).scale(0.88)
        recap_bridge = MathTex(r"AE=AD+DE", font_size=36, color=POINT)
        recap_bridge.move_to([2.85, -0.80, 0])
        recap_formula = final_formula.copy().scale(0.87).move_to([3.05, -2.05, 0])
        recap_frame = SurroundingRectangle(
            recap_formula,
            color=POINT,
            buff=0.18,
            stroke_width=3,
        )
        recap_arrows = VGroup(
            Line(recap_one.get_bottom(), recap_bridge.get_top(), color=MUTED, stroke_width=2),
            Line(recap_two.get_bottom(), recap_bridge.get_top(), color=MUTED, stroke_width=2),
        )

        self.play(
            Succession(
                FadeOut(VGroup(final_formula, formula_frame, root_note, positive)),
                FadeIn(VGroup(recap_one, recap_two)),
            ),
            run_time=0.8,
        )
        self.play(FadeIn(recap_bridge), Create(recap_arrows), run_time=0.65)
        self.play(FadeIn(recap_formula), Create(recap_frame), Circumscribe(line_ad, color=BLUE), run_time=0.85)
        self.wait(0.30)
