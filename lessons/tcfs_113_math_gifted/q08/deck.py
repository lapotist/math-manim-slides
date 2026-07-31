"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q8."""

from __future__ import annotations

from fractions import Fraction
from math import gcd

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
    Angle,
    Brace,
    Circumscribe,
    Create,
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
    RoundedRectangle,
    SurroundingRectangle,
    Transform,
    TransformFromCopy,
    VGroup,
    ValueTracker,
    Write,
    always_redraw,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


CE_OVER_SIDE = Fraction(36, 59)
BE_OVER_SIDE = Fraction(23, 59)
OD_OVER_SIDE = Fraction(23, 13)
DF_OVER_SIDE = CE_OVER_SIDE * OD_OVER_SIDE / (OD_OVER_SIDE + 1)
INTEGER_PAIRS = tuple((23 * scale, 13 * scale) for scale in range(1, 4))
MIN_SIDE = INTEGER_PAIRS[0][1]
MIN_AREA = MIN_SIDE**2

if CE_OVER_SIDE + BE_OVER_SIDE != 1:
    raise ValueError("right-side partition does not close")
if DF_OVER_SIDE != BE_OVER_SIDE or DF_OVER_SIDE + CE_OVER_SIDE != 1:
    raise ValueError("half-area trapezoid heights do not close")
if gcd(23, 13) != 1 or INTEGER_PAIRS[0] != (23, 13):
    raise ValueError("reduced positive-integer scale is incorrect")
if MIN_AREA != 169:
    raise ValueError("unexpected minimum square area")


class CarloTcfs113MathQ08(CarloSlide):
    """Discover the minimum square through area, similarity, and integrality."""

    lesson_id = "carlo.tcfs_113_math_gifted.q08"

    SIDE = 3.10
    BASE_Y = -1.42
    D_X = -0.62
    C_X = D_X + SIDE
    O_X = D_X - SIDE * float(OD_OVER_SIDE)
    TOP_Y = BASE_Y + SIDE

    @classmethod
    def base_points(cls) -> dict[str, list[float]]:
        return {
            "O": [cls.O_X, cls.BASE_Y, 0],
            "D": [cls.D_X, cls.BASE_Y, 0],
            "C": [cls.C_X, cls.BASE_Y, 0],
            "A": [cls.D_X, cls.TOP_Y, 0],
            "B": [cls.C_X, cls.TOP_Y, 0],
        }

    @classmethod
    def moving_points(cls, ce_fraction: float) -> tuple[list[float], list[float]]:
        e_height = cls.SIDE * ce_fraction
        f_height = e_height * float(Fraction(23, 36))
        e_point = [cls.C_X, cls.BASE_Y + e_height, 0]
        f_point = [cls.D_X, cls.BASE_Y + f_height, 0]
        return e_point, f_point

    @staticmethod
    def lower_area_fraction(ce_fraction: float) -> float:
        return ce_fraction * float(Fraction(59, 72))

    @staticmethod
    def replace_title(scene: "CarloTcfs113MathQ08", old, new) -> None:
        scene.play(FadeOut(old), FadeIn(new), run_time=0.55)

    @staticmethod
    def right_angle_mark(vertex: list[float], *, color: str) -> VGroup:
        x_coord, y_coord, _ = vertex
        size = 0.20
        return VGroup(
            Line(
                [x_coord - size, y_coord, 0],
                [x_coord - size, y_coord + size, 0],
                color=color,
                stroke_width=3,
            ),
            Line(
                [x_coord - size, y_coord + size, 0],
                [x_coord, y_coord + size, 0],
                color=color,
                stroke_width=3,
            ),
        )

    @staticmethod
    def pair_card(scale: int) -> VGroup:
        od_value, side_value = 23 * scale, 13 * scale
        frame = RoundedRectangle(
            width=3.55,
            height=1.28,
            corner_radius=0.08,
            color=HAIRLINE,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.97,
        )
        scale_tex = MathTex("t", "=", str(scale), font_size=30, color=MUTED)
        values = MathTex(
            "(OD,s)",
            "=",
            f"({od_value},{side_value})",
            font_size=35,
            color=INK,
        )
        values[0].set_color(POINT)
        values[2].set_color(REGION if scale == 1 else INK)
        content = VGroup(scale_tex, values).arrange(DOWN, buff=0.18)
        content.move_to(frame)
        return VGroup(frame, content)

    def construct(self) -> None:
        points = self.base_points()
        target_fraction = float(CE_OVER_SIDE)
        target_e, target_f = self.moving_points(target_fraction)

        heading = label("第 8 題｜平分正方形的直線", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 8 頁｜影片 xRrA7_xEStU",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        axis = Line(
            [self.O_X - 0.42, self.BASE_Y, 0],
            [self.C_X + 0.45, self.BASE_Y, 0],
            color=MUTED,
            stroke_width=2.4,
        )
        square = Polygon(
            points["D"],
            points["C"],
            points["B"],
            points["A"],
            color=INK,
            stroke_width=3.2,
            fill_opacity=0,
        ).set_z_index(3)
        vertex_labels = VGroup(
            MathTex("O", font_size=31, color=POINT).next_to(points["O"], DOWN + LEFT, buff=0.10),
            MathTex("D", font_size=31, color=INK).next_to(points["D"], DOWN, buff=0.12),
            MathTex("C", font_size=31, color=INK).next_to(points["C"], DOWN, buff=0.12),
            MathTex("A", font_size=31, color=INK).next_to(points["A"], UP + LEFT, buff=0.08),
            MathTex("B", font_size=31, color=INK).next_to(points["B"], UP + RIGHT, buff=0.08),
        ).set_z_index(8)

        ce_tracker = ValueTracker(0.30)
        upper_region = always_redraw(
            lambda: Polygon(
                points["A"],
                points["B"],
                self.moving_points(ce_tracker.get_value())[0],
                self.moving_points(ce_tracker.get_value())[1],
                stroke_opacity=0,
                fill_color=PURPLE,
                fill_opacity=0.24,
            ).set_z_index(0)
        )
        lower_region = always_redraw(
            lambda: Polygon(
                points["D"],
                points["C"],
                self.moving_points(ce_tracker.get_value())[0],
                self.moving_points(ce_tracker.get_value())[1],
                stroke_opacity=0,
                fill_color=REGION,
                fill_opacity=0.28,
            ).set_z_index(0)
        )
        cut_line = always_redraw(
            lambda: Line(
                points["O"],
                self.moving_points(ce_tracker.get_value())[0],
                color=POINT,
                stroke_width=4.5,
            ).set_z_index(5)
        )
        e_dot = always_redraw(
            lambda: Dot(
                self.moving_points(ce_tracker.get_value())[0],
                radius=0.09,
                color=POINT,
            ).set_z_index(7)
        )
        e_label = always_redraw(
            lambda: MathTex("E", font_size=31, color=POINT)
            .next_to(self.moving_points(ce_tracker.get_value())[0], RIGHT, buff=0.13)
            .set_z_index(8)
        )

        lower_caption = label("下方面積", 23, REGION, "BOLD").move_to([4.20, 0.55, 0])
        upper_caption = label("上方面積", 23, PURPLE, "BOLD").move_to([4.20, -0.28, 0])
        lower_number = DecimalNumber(
            self.lower_area_fraction(ce_tracker.get_value()),
            num_decimal_places=2,
            font_size=37,
            color=REGION,
        ).move_to([5.42, 0.55, 0])
        upper_number = DecimalNumber(
            1 - self.lower_area_fraction(ce_tracker.get_value()),
            num_decimal_places=2,
            font_size=37,
            color=PURPLE,
        ).move_to([5.42, -0.28, 0])
        lower_number.add_updater(
            lambda mob: mob.set_value(self.lower_area_fraction(ce_tracker.get_value()))
        )
        upper_number.add_updater(
            lambda mob: mob.set_value(1 - self.lower_area_fraction(ce_tracker.get_value()))
        )
        area_units = VGroup(
            MathTex("s^2", font_size=30, color=MUTED).move_to([6.15, 0.55, 0]),
            MathTex("s^2", font_size=30, color=MUTED).move_to([6.15, -0.28, 0]),
        )
        area_readout = VGroup(
            lower_caption,
            upper_caption,
            lower_number,
            upper_number,
            area_units,
        )

        # Beat 01: vary only E and let the two areas respond.
        self.begin_beat("explore_moving_cut")
        beat_title = label("讓 E 上下移動，哪一條線會平分？", 35, INK, "BOLD")
        beat_title.move_to([0, 2.87, 0])
        self.add(heading, source)
        self.play(FadeIn(beat_title), Create(axis), Create(square), FadeIn(vertex_labels), run_time=0.9)
        self.play(
            FadeIn(upper_region),
            FadeIn(lower_region),
            Create(cut_line),
            GrowFromCenter(e_dot),
            FadeIn(e_label),
            FadeIn(area_readout),
            run_time=0.9,
        )
        self.play(ce_tracker.animate.set_value(0.81), run_time=1.35)
        self.play(ce_tracker.animate.set_value(0.43), run_time=1.15)
        self.wait(0.4)

        # Beat 02: settle at equal areas, freeze the geometry, then name F.
        self.next_beat("settle_equal_halves")
        next_title = label("兩個面積一起停在一半，交點叫 F", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(ce_tracker.animate.set_value(target_fraction), run_time=1.35)
        self.play(Indicate(lower_number, color=POINT), Indicate(upper_number, color=POINT), run_time=0.7)
        for moving in (upper_region, lower_region, cut_line, e_dot, e_label):
            moving.clear_updaters()
        lower_number.clear_updaters()
        upper_number.clear_updaters()

        f_dot = Dot(target_f, radius=0.09, color=BLUE).set_z_index(7)
        f_label = MathTex("F", font_size=31, color=BLUE).next_to(target_f, LEFT, buff=0.13).set_z_index(8)
        lower_exact = VGroup(
            label("下方", 23, REGION, "BOLD"),
            MathTex("=", r"\frac12s^2", font_size=37, color=REGION),
        ).arrange(RIGHT, buff=0.18)
        upper_exact = VGroup(
            label("上方", 23, PURPLE, "BOLD"),
            MathTex("=", r"\frac12s^2", font_size=37, color=PURPLE),
        ).arrange(RIGHT, buff=0.18)
        exact_areas = VGroup(lower_exact, upper_exact).arrange(DOWN, buff=0.36)
        exact_areas.move_to([4.75, 0.10, 0])
        equal_note = label("面積相等", 25, POINT, "BOLD").move_to([4.75, -1.22, 0])
        self.play(FadeOut(area_readout), FadeIn(exact_areas), FadeIn(equal_note), run_time=0.7)
        self.play(GrowFromCenter(f_dot), FadeIn(f_label), run_time=0.55)
        self.wait(0.4)

        # Beat 03: use the given 36:23 partition to locate E exactly.
        self.next_beat("resolve_right_side_ratio")
        next_title = label("右邊分成 36 份與 23 份", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        ce_segment = Line(points["C"], target_e, color=REGION, stroke_width=8).set_z_index(4)
        be_segment = Line(target_e, points["B"], color=BLUE, stroke_width=8).set_z_index(4)
        ce_tag = MathTex("CE", font_size=27, color=REGION).move_to(
            [self.C_X - 0.34, (self.BASE_Y + target_e[1]) / 2, 0]
        )
        be_tag = MathTex("BE", font_size=27, color=BLUE).move_to(
            [self.C_X - 0.34, (self.TOP_Y + target_e[1]) / 2, 0]
        )
        side_brace = Brace(Line(points["A"], points["B"]), direction=UP, color=MUTED)
        side_label = MathTex("s", font_size=33, color=INK).next_to(side_brace, UP, buff=0.08)

        ratio = MathTex("CE", ":", "BE", "=", "36", ":", "23", font_size=43, color=INK)
        ratio[0].set_color(REGION)
        ratio[2].set_color(BLUE)
        ratio[4].set_color(REGION)
        ratio[6].set_color(BLUE)
        ratio.move_to([4.72, 1.23, 0])
        whole_side = MathTex("CE", "+", "BE", "=", "s", font_size=38, color=INK)
        whole_side[0].set_color(REGION)
        whole_side[2].set_color(BLUE)
        whole_side.move_to([4.72, 0.36, 0])
        ce_value = MathTex("CE", "=", r"\frac{36}{59}s", font_size=39, color=INK)
        ce_value[0].set_color(REGION)
        ce_value[2].set_color(REGION)
        be_value = MathTex("BE", "=", r"\frac{23}{59}s", font_size=39, color=INK)
        be_value[0].set_color(BLUE)
        be_value[2].set_color(BLUE)
        partition_values = VGroup(ce_value, be_value).arrange(DOWN, buff=0.34)
        partition_values.move_to([4.72, -0.78, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(exact_areas), FadeOut(equal_note), run_time=0.45)
        self.play(
            Create(ce_segment),
            Create(be_segment),
            FadeIn(ce_tag),
            FadeIn(be_tag),
            GrowFromCenter(side_brace),
            FadeIn(side_label),
            run_time=0.8,
        )
        self.play(Write(ratio), run_time=0.65)
        self.play(TransformFromCopy(ratio, whole_side), run_time=0.55)

        self.next_beat("state_right_side_lengths")
        self.play(FadeIn(partition_values), run_time=0.7)
        self.wait(0.4)

        # Beat 04: isolate the lower trapezoid and write its two area forms.
        self.next_beat("isolate_half_trapezoid")
        next_title = label("下方梯形正好是半個正方形", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        df_segment = Line(points["D"], target_f, color=BLUE, stroke_width=8).set_z_index(4)
        df_tag = MathTex("DF", font_size=27, color=BLUE).move_to(
            [self.D_X + 0.34, (self.BASE_Y + target_f[1]) / 2, 0]
        )
        lower_outline = Polygon(
            points["D"],
            points["C"],
            target_e,
            target_f,
            color=REGION,
            stroke_width=4.5,
            fill_opacity=0,
        ).set_z_index(5)
        trapezoid_area = MathTex(
            "A_{lower}",
            "=",
            r"\frac12(DF+CE)s",
            font_size=40,
            color=INK,
        ).move_to([4.72, 0.30, 0])
        trapezoid_area[0].set_color(REGION)
        half_square = MathTex(
            "A_{lower}",
            "=",
            r"\frac12s^2",
            font_size=40,
            color=INK,
        ).move_to([4.72, -0.74, 0])
        half_square[0].set_color(REGION)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        ce_corner = ce_value.copy().scale(0.76).move_to([4.85, 1.65, 0])
        self.play(
            FadeOut(ratio),
            FadeOut(whole_side),
            FadeOut(partition_values),
            FadeIn(ce_corner),
            upper_region.animate.set_opacity(0.06),
            lower_region.animate.set_opacity(0.38),
            run_time=0.7,
        )
        self.play(Create(df_segment), FadeIn(df_tag), Create(lower_outline), run_time=0.75)
        self.play(Write(trapezoid_area), run_time=0.75)
        self.play(TransformFromCopy(trapezoid_area[0], half_square[0]), Write(VGroup(*half_square[1:])), run_time=0.7)
        self.wait(0.4)

        # Beat 05: convert half-area into the missing left height.
        self.next_beat("earn_left_height")
        next_title = label("兩條高度的平均必須是 s / 2", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        average_height = MathTex(
            r"\frac{DF+CE}{2}",
            "=",
            r"\frac{s}{2}",
            font_size=43,
            color=INK,
        ).move_to([4.72, 0.55, 0])
        average_height[0].set_color(BLUE)
        height_sum = MathTex("DF", "+", "CE", "=", "s", font_size=43, color=INK)
        height_sum[0].set_color(BLUE)
        height_sum[2].set_color(REGION)
        height_sum.move_to([4.72, -0.28, 0])
        df_value = MathTex(
            "DF",
            "=",
            "s-CE",
            "=",
            r"\frac{23}{59}s",
            font_size=39,
            color=INK,
        ).move_to([4.72, -1.28, 0])
        df_value[0].set_color(BLUE)
        df_value[2].set_color(BLUE)
        df_value[4].set_color(BLUE)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(trapezoid_area), FadeOut(half_square), FadeIn(average_height), run_time=0.75)
        self.play(TransformFromCopy(average_height, height_sum), run_time=0.65)
        self.play(TransformFromCopy(height_sum, df_value), run_time=0.75)
        self.play(Indicate(df_segment, color=POINT), Indicate(ce_segment, color=POINT), run_time=0.65)
        self.wait(0.4)

        # Beat 06: reveal the two similar right triangles only after both heights are known.
        self.next_beat("see_similar_triangles")
        next_title = label("現在才比較 ODF 與 OCE", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        big_triangle = Polygon(
            points["O"],
            points["C"],
            target_e,
            color=REGION,
            stroke_width=4,
            fill_color=REGION,
            fill_opacity=0.08,
        ).set_z_index(2)
        small_triangle = Polygon(
            points["O"],
            points["D"],
            target_f,
            color=BLUE,
            stroke_width=4,
            fill_color=BLUE,
            fill_opacity=0.17,
        ).set_z_index(3)
        right_at_d = self.right_angle_mark(points["D"], color=BLUE).set_z_index(7)
        right_at_c = self.right_angle_mark(points["C"], color=REGION).set_z_index(7)
        shared_angle = Angle(
            Line(points["O"], points["D"]),
            Line(points["O"], target_f),
            radius=0.52,
            color=POINT,
            stroke_width=4,
        ).set_z_index(7)
        similarity_note = label("同一個銳角，而且各有一個直角", 23, MUTED, "MEDIUM")
        similarity_note.move_to([4.70, 0.62, 0])
        similarity = MathTex(
            r"\triangle ODF",
            r"\sim",
            r"\triangle OCE",
            font_size=43,
            color=INK,
        ).move_to([4.70, -0.32, 0])
        similarity[0].set_color(BLUE)
        similarity[2].set_color(REGION)
        height_badges = VGroup(
            ce_corner.copy(),
            MathTex("DF", "=", r"\frac{23}{59}s", font_size=31, color=BLUE),
        ).arrange(RIGHT, buff=0.55).move_to([4.70, 1.50, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(average_height),
            FadeOut(height_sum),
            FadeOut(df_value),
            FadeOut(ce_corner),
            FadeIn(height_badges),
            upper_region.animate.set_opacity(0.11),
            lower_region.animate.set_opacity(0.15),
            run_time=0.65,
        )
        self.play(Create(big_triangle), Create(small_triangle), run_time=0.8)
        self.play(Create(right_at_d), Create(right_at_c), Create(shared_angle), run_time=0.65)
        self.play(FadeIn(similarity_note), Write(similarity), run_time=0.7)
        self.wait(0.4)

        # Beat 07: transfer the height ratio to OD and the square side.
        self.next_beat("derive_base_ratio")
        next_title = label("對應邊把高度比傳到底邊", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        proportion = MathTex(
            r"\frac{OD}{OD+s}",
            "=",
            r"\frac{DF}{CE}",
            "=",
            r"\frac{23}{36}",
            font_size=39,
            color=INK,
        ).move_to([4.72, 0.55, 0])
        proportion[0].set_color(POINT)
        proportion[2].set_color(BLUE)
        proportion[4].set_color(REGION)
        cross_multiply = MathTex(
            "36OD",
            "=",
            "23(OD+s)",
            font_size=39,
            color=INK,
        ).move_to([4.72, -0.35, 0])
        reduced = MathTex("13OD", "=", "23s", font_size=41, color=INK).move_to(cross_multiply)
        final_ratio = MathTex(
            "OD",
            ":",
            "s",
            "=",
            "23",
            ":",
            "13",
            font_size=47,
            color=INK,
        ).move_to([4.72, -1.38, 0])
        final_ratio[0].set_color(POINT)
        final_ratio[2].set_color(PURPLE)
        final_ratio[4].set_color(POINT)
        final_ratio[6].set_color(PURPLE)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        sim_corner = similarity.copy().scale(0.74).move_to([4.72, 1.50, 0])
        self.play(
            FadeOut(similarity_note),
            FadeOut(height_badges),
            Transform(similarity, sim_corner),
            run_time=0.55,
        )
        self.play(Write(proportion), run_time=0.8)
        self.play(TransformFromCopy(proportion, cross_multiply), run_time=0.7)

        self.next_beat("reduce_base_ratio")
        self.play(Transform(cross_multiply, reduced), run_time=0.6)
        self.play(TransformFromCopy(reduced, final_ratio), run_time=0.7)
        self.play(Circumscribe(final_ratio, color=POINT), run_time=0.55)
        self.wait(0.4)

        # Beat 08: use coprimality to turn the ratio into integer scale pairs.
        self.next_beat("enforce_integer_scale")
        next_title = label("整數尺度只能一格一格放大", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        coprime = MathTex(r"\gcd(23,13)", "=", "1", font_size=37, color=MUTED)
        coprime.move_to([0, 1.73, 0])
        scale_rule = MathTex(
            "OD",
            "=",
            "23t",
            r"\qquad",
            "s",
            "=",
            "13t",
            r"\qquad",
            r"t\in\mathbb{Z}_{>0}",
            font_size=42,
            color=INK,
        ).move_to([0, 0.95, 0])
        scale_rule[0].set_color(POINT)
        scale_rule[2].set_color(POINT)
        scale_rule[4].set_color(PURPLE)
        scale_rule[6].set_color(PURPLE)
        pair_cards = VGroup(*(self.pair_card(scale) for scale in (1, 2, 3)))
        pair_cards.arrange(RIGHT, buff=0.55).move_to([0, -0.50, 0])
        scale_question = label("哪一格給最小的正方形邊長？", 29, POINT, "BOLD")
        scale_question.move_to([0, -2.12, 0])

        core_geometry = VGroup(
            axis,
            square,
            vertex_labels,
            upper_region,
            lower_region,
            cut_line,
            e_dot,
            e_label,
            f_dot,
            f_label,
            ce_segment,
            be_segment,
            ce_tag,
            be_tag,
            side_brace,
            side_label,
            df_segment,
            df_tag,
            lower_outline,
        )
        triangle_evidence = VGroup(
            big_triangle,
            small_triangle,
            right_at_d,
            right_at_c,
            shared_angle,
            similarity,
            proportion,
            cross_multiply,
            final_ratio,
        )

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(core_geometry), FadeOut(triangle_evidence), run_time=0.7)
        self.play(FadeIn(coprime), Write(scale_rule), run_time=0.75)
        self.play(LaggedStart(*(FadeIn(card) for card in pair_cards), lag_ratio=0.16), run_time=1.0)
        self.play(FadeIn(scale_question), run_time=0.55)
        self.wait(0.45)

        # Beat 09: select t=1 and check every original condition before the answer.
        self.next_beat("verify_minimal_configuration")
        next_title = label("先把 t = 1 放回原圖逐條檢查", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        selected = SurroundingRectangle(pair_cards[0], color=POINT, buff=0.10, stroke_width=4)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(Create(selected), pair_cards[1:].animate.set_opacity(0.25), run_time=0.65)

        od_brace = Brace(Line(points["O"], points["D"]), direction=DOWN, color=POINT)
        od_label = MathTex("OD", "=", "23", font_size=31, color=POINT).next_to(
            od_brace, DOWN, buff=0.08
        )
        numeric_side = MathTex("s", "=", "13", font_size=33, color=PURPLE).move_to(side_label)
        integer_check = MathTex(
            "OD",
            "=",
            "23",
            r"\qquad",
            "AD",
            "=",
            "13",
            font_size=35,
            color=INK,
        )
        integer_check[0].set_color(POINT)
        integer_check[2].set_color(POINT)
        integer_check[4].set_color(PURPLE)
        integer_check[6].set_color(PURPLE)
        ratio_check = MathTex(
            r"\frac{CE}{BE}",
            "=",
            r"\frac{36s/59}{23s/59}",
            "=",
            r"\frac{36}{23}",
            font_size=31,
            color=INK,
        )
        ratio_check[0].set_color(REGION)
        ratio_check[2].set_color(BLUE)
        half_check = MathTex(
            "DF+CE",
            "=",
            r"\frac{23+36}{59}s",
            "=",
            "s",
            font_size=32,
            color=INK,
        )
        half_check[0].set_color(REGION)
        checks = VGroup(integer_check, ratio_check, half_check).arrange(DOWN, buff=0.48)
        checks.move_to([4.62, -0.08, 0])
        check_note = label("整數、線段比、平分面積都成立", 23, POINT, "BOLD")
        check_note.move_to([4.62, -1.78, 0])

        self.play(
            FadeOut(coprime),
            FadeOut(scale_rule),
            FadeOut(pair_cards),
            FadeOut(selected),
            FadeOut(scale_question),
            FadeIn(core_geometry),
            run_time=0.8,
        )
        self.play(GrowFromCenter(od_brace), FadeIn(od_label), Transform(side_label, numeric_side), run_time=0.7)

        self.next_beat("recheck_ratio_and_area")
        self.play(LaggedStart(*(FadeIn(check) for check in checks), lag_ratio=0.18), run_time=1.0)
        self.play(FadeIn(check_note), run_time=0.55)
        self.wait(0.5)

        # Beat 10: reveal the requested area only after the full pre-answer check.
        self.next_beat("reveal_minimum_area")
        next_title = label("最後才計算正方形面積", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        final_fill = Polygon(
            points["D"],
            points["C"],
            points["B"],
            points["A"],
            color=PURPLE,
            stroke_width=5,
            fill_color=PURPLE,
            fill_opacity=0.18,
        ).set_z_index(1)
        area_name = MathTex(
            "A_{ABCD}",
            "=",
            "s^2",
            font_size=43,
            color=INK,
        )
        area_name[0].set_color(PURPLE)
        area_name[2].set_color(PURPLE)
        area_value = MathTex(
            "=",
            "13^2",
            "=",
            "169",
            font_size=51,
            color=INK,
        )
        area_value[1].set_color(PURPLE)
        area_value[3].set_color(REGION)
        area_formula = VGroup(area_name, area_value).arrange(DOWN, buff=0.30)
        area_formula.move_to([4.68, -0.02, 0])
        final_frame = SurroundingRectangle(area_formula, color=POINT, buff=0.22, stroke_width=4)
        final_note = label("最小面積（平方單位）", 24, MUTED, "MEDIUM")
        final_note.next_to(final_frame, DOWN, buff=0.24)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(checks), FadeOut(check_note), FadeIn(final_fill), run_time=0.65)
        self.play(Write(area_name), run_time=0.6)
        self.play(
            Write(area_value[0]),
            TransformFromCopy(side_label, area_value[1]),
            Write(VGroup(*area_value[2:])),
            run_time=0.8,
        )

        self.next_beat("frame_minimum_area")
        self.play(Create(final_frame), FadeIn(final_note), run_time=0.65)
        self.play(Circumscribe(area_value[-1], color=REGION), run_time=0.6)
        self.wait(0.5)
