"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q6."""

from __future__ import annotations

from fractions import Fraction

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
    Arrow,
    Axes,
    Circumscribe,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


VALID_A = Fraction(-3, 5)
REJECTED_A = Fraction(1)
F_VERTEX_X = Fraction(1)
G_VERTEX_X = Fraction(2)
F_MAXIMUM = Fraction(2)
G_MINIMUM = Fraction(-1)


def f_value(a_value: Fraction, x_value: Fraction) -> Fraction:
    """Evaluate the first quadratic exactly."""
    if a_value == 0:
        raise ValueError("a=0 makes the problem expression undefined")
    return (
        a_value * x_value**2
        - 2 * a_value * x_value
        + 6 * a_value
        - Fraction(3, 1) / a_value
    )


def g_value(a_value: Fraction, x_value: Fraction) -> Fraction:
    """Evaluate the second quadratic exactly."""
    if a_value == 0:
        raise ValueError("a=0 makes the problem expression undefined")
    return (
        -a_value * x_value**2
        + 4 * a_value * x_value
        + 6 * a_value
        - Fraction(3, 1) / a_value
    )


def f_completed(a_value: Fraction, x_value: Fraction) -> Fraction:
    return (
        a_value * (x_value - 1) ** 2
        + 5 * a_value
        - Fraction(3, 1) / a_value
    )


def g_completed(a_value: Fraction, x_value: Fraction) -> Fraction:
    return (
        -a_value * (x_value - 2) ** 2
        + 10 * a_value
        - Fraction(3, 1) / a_value
    )


if VALID_A >= 0 or REJECTED_A <= 0:
    raise ValueError("candidate signs do not encode the extremum test")
if (5 * VALID_A + 3) * (VALID_A - 1) != 0:
    raise ValueError("valid parameter misses the factored equation")
if (5 * REJECTED_A + 3) * (REJECTED_A - 1) != 0:
    raise ValueError("rejected parameter misses the factored equation")
for _numerator in range(-16, 25):
    _x = Fraction(_numerator, 4)
    if f_value(VALID_A, _x) != f_completed(VALID_A, _x):
        raise ValueError("first completed-square identity failed")
    if g_value(VALID_A, _x) != g_completed(VALID_A, _x):
        raise ValueError("second completed-square identity failed")
if f_value(VALID_A, F_VERTEX_X) != F_MAXIMUM:
    raise ValueError("first vertex height is not the stated maximum")
if any(
    f_value(VALID_A, Fraction(x_value)) > F_MAXIMUM
    for x_value in range(-20, 21)
):
    raise ValueError("valid first quadratic exceeds its claimed maximum")
if f_value(REJECTED_A, F_VERTEX_X) != 2 or f_value(REJECTED_A, 0) != 3:
    raise ValueError("positive-root counterexample was not reconstructed")
if f_value(REJECTED_A, 10) <= f_value(REJECTED_A, 0):
    raise ValueError("positive candidate should rise without an upper bound")
if g_value(VALID_A, G_VERTEX_X) != G_MINIMUM:
    raise ValueError("second vertex height is not the requested minimum")
if any(
    g_value(VALID_A, Fraction(x_value)) < G_MINIMUM
    for x_value in range(-20, 21)
):
    raise ValueError("second quadratic falls below its claimed minimum")
if 10 * VALID_A != -6 or -Fraction(3, 1) / VALID_A != 5:
    raise ValueError("pre-answer contributions are incorrect")


class CarloTcfs112MathQ06(CarloSlide):
    """Use graph orientation to select a parameter before finding a minimum."""

    lesson_id = "carlo.tcfs_112_math_gifted.q06"

    @staticmethod
    def title_change(old, new) -> Succession:
        """Replace CJK titles without morphing their glyph outlines."""
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def stage_title(text: str):
        title = label(text, 30, INK, "BOLD")
        title.move_to([3.58, 3.07, 0])
        return title

    @staticmethod
    def graph_axes() -> tuple[Axes, VGroup]:
        axes = Axes(
            x_range=[-3, 5, 1],
            y_range=[-6, 5, 1],
            x_length=6.75,
            y_length=5.45,
            axis_config={
                "color": MUTED,
                "stroke_width": 2.0,
                "include_ticks": True,
                "include_tip": True,
            },
            tips=True,
        ).move_to([-3.45, -0.22, 0])
        axis_labels = VGroup(
            MathTex("x", font_size=24, color=MUTED).next_to(
                axes.x_axis.get_end(), DOWN, buff=0.05
            ),
            MathTex("y", font_size=24, color=MUTED).next_to(
                axes.y_axis.get_end(), LEFT, buff=0.05
            ),
        )
        return axes, axis_labels

    @staticmethod
    def candidate_card(expression: str, color: str) -> VGroup:
        frame = RoundedRectangle(
            width=2.20,
            height=0.92,
            corner_radius=0.07,
            color=color,
            stroke_width=2.5,
            fill_color=color,
            fill_opacity=0.12,
        )
        value = MathTex(expression, font_size=39, color=color).move_to(frame)
        return VGroup(frame, value)

    @staticmethod
    def term_card(expression: str, color: str) -> VGroup:
        frame = RoundedRectangle(
            width=2.35,
            height=1.02,
            corner_radius=0.07,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.97,
        )
        value = MathTex(expression, font_size=35, color=color).move_to(frame)
        return VGroup(frame, value)

    def construct(self) -> None:
        heading = label("第 6 題｜先看開口，再找極值", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 6 頁｜影片 t9wHX49OZPM 00:00-01:54.75",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.35, -3.42, 0], [0.35, 3.38, 0], color=HAIRLINE, stroke_width=1.5)
        axes, axis_labels = self.graph_axes()

        f_curve_target = axes.plot(
            lambda x: -0.6 * (x - 1) ** 2 + 2,
            x_range=[-2.45, 4.45],
            color=BLUE,
            stroke_width=5.0,
        ).set_z_index(4)
        f_curve = f_curve_target.copy()
        f_tag = MathTex("f", font_size=30, color=BLUE).move_to(axes.c2p(-1.75, -2.55))
        ceiling = DashedLine(
            axes.c2p(-2.85, 2),
            axes.c2p(4.85, 2),
            color=POINT,
            dash_length=0.10,
            stroke_width=2.5,
        ).set_z_index(2)
        y_two = MathTex("2", font_size=28, color=POINT).next_to(
            axes.c2p(-2.85, 2), LEFT, buff=0.10
        )
        f_vertex_dot = Dot(axes.c2p(1, 2), radius=0.095, color=POINT).set_z_index(8)
        highest_note = label("最高點", 22, POINT, "BOLD").next_to(
            f_vertex_dot, UP + RIGHT, buff=0.13
        )

        # Beat 01 show_highest_point_graph: turn the stated maximum into a concrete ceiling first.
        self.begin_beat("show_highest_point_graph")
        stage_title = self.stage_title("先看圖：最高只能到 2")
        f_formula = MathTex(
            r"f(x)=ax^2-2ax+6a-\frac3a",
            font_size=37,
            color=INK,
        ).move_to([3.58, 1.28, 0])
        f_formula.set_color_by_tex("a", POINT)
        domain = MathTex(r"x\in\mathbb R", font_size=38, color=REGION)
        maximum_given = VGroup(
            label("題目保證最高值", 25, MUTED, "MEDIUM"),
            MathTex("2", font_size=46, color=POINT),
        ).arrange(RIGHT, buff=0.22)
        prompt = label("哪一種開口，才可能有最高點？", 28, POINT, "BOLD")
        opening_panel = VGroup(domain, maximum_given, prompt).arrange(DOWN, buff=0.52)
        opening_panel.move_to([3.58, -0.62, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Create(axes), FadeIn(axis_labels), run_time=0.9)
        self.play(Create(f_curve), FadeIn(f_tag), run_time=1.0)
        self.play(Create(ceiling), FadeIn(y_two, f_vertex_dot, highest_note), run_time=0.75)

        # Beat 02 meet_highest_point: continue at a settled semantic boundary.
        self.next_beat("meet_highest_point")
        self.play(FadeIn(f_formula), run_time=0.75)
        self.play(LaggedStart(*(FadeIn(item) for item in opening_panel), lag_ratio=0.16), run_time=0.9)
        self.wait(0.35)

        # Beat 03 decide_opening_direction: flip one trial curve to test which sign can have a maximum.
        self.next_beat("decide_opening_direction")
        next_title = self.stage_title("先檢查開口方向")
        upward_trial = axes.plot(
            lambda x: (x - 1) ** 2 + 2,
            x_range=[-0.68, 2.68],
            color=CORAL,
            stroke_width=5.0,
        ).set_z_index(4)
        positive_test = VGroup(
            MathTex("a>0", font_size=51, color=CORAL),
            label("兩端一直升高，沒有最大值", 27, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.30).move_to([3.58, -0.35, 0])
        minimum_note = label("這裡反而是最低點", 22, CORAL, "BOLD")
        minimum_note.next_to(f_vertex_dot, UP + RIGHT, buff=0.13)
        negative_result = VGroup(
            MathTex("a<0", font_size=54, color=POINT),
            label("向下開口，才有有限最高值", 27, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.30).move_to([3.58, -0.25, 0])
        nonzero_guard = VGroup(
            MathTex(r"a\ne0", font_size=35, color=MUTED),
            label("題式中的分母也要求這一點", 22, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.20).move_to([3.58, -1.60, 0])

        self.play(self.title_change(stage_title, next_title), FadeOut(opening_panel), run_time=0.6)
        stage_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(ceiling, y_two, highest_note)),
                FadeIn(VGroup(positive_test, minimum_note)),
            ),
            Transform(f_curve, upward_trial),
            run_time=0.95,
        )
        self.wait(0.20)
        self.play(FadeOut(positive_test, minimum_note), run_time=0.35)
        self.play(
            Transform(f_curve, f_curve_target),
            FadeIn(ceiling, y_two, highest_note, negative_result, nonzero_guard),
            run_time=0.95,
        )
        self.wait(0.35)

        # Beat 04 complete_square_for_f: complete the x expression and draw the axis it names.
        self.next_beat("complete_square_for_f")
        next_title = self.stage_title("最高點的中心藏在 (x-1)^2")
        square_identity_f = MathTex(
            r"x^2-2x=(x-1)^2-1",
            font_size=43,
            color=REGION,
        ).move_to([3.58, 1.25, 0])
        completed_f = MathTex(
            r"f(x)=a(x-1)^2+5a-\frac3a",
            font_size=42,
            color=INK,
        ).move_to([3.58, 0.00, 0])
        completed_f.set_color_by_tex("(x-1)^2", REGION)
        axis_note = label("平方距離以 1 為中心", 27, REGION, "BOLD")
        axis_note.move_to([3.58, -1.28, 0])
        f_axis = DashedLine(
            axes.c2p(1, -5.5),
            axes.c2p(1, 4.55),
            color=REGION,
            dash_length=0.10,
            stroke_width=2.5,
        ).set_z_index(2)
        x_one = MathTex("1", font_size=27, color=REGION).next_to(
            axes.c2p(1, 0), DOWN, buff=0.11
        )
        f_vertex_unknown = MathTex("(1,?)", font_size=29, color=POINT)
        f_vertex_unknown.next_to(f_vertex_dot, UP + RIGHT, buff=0.12)

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(negative_result, nonzero_guard, highest_note, f_formula)),
                FadeIn(square_identity_f),
            ),
            run_time=0.7,
        )
        self.play(FadeIn(completed_f), run_time=0.8)

        # Beat 05 locate_f_axis: continue at a settled semantic boundary.
        self.next_beat("locate_f_axis")
        self.play(Create(f_axis), FadeIn(x_one, f_vertex_unknown), run_time=0.7)
        self.play(FadeIn(axis_note), Circumscribe(f_vertex_dot, color=REGION), run_time=0.65)
        self.wait(0.35)

        # Beat 06 use_maximum_height: turn the visible vertex height into one parameter equation.
        self.next_beat("use_maximum_height")
        next_title = self.stage_title("在 x=1，平方項剛好歸零")
        zero_at_one = MathTex(
            r"x=1\quad\Longrightarrow\quad(x-1)^2=0",
            font_size=40,
            color=REGION,
        ).move_to([3.58, 1.25, 0])
        height_equation = MathTex(
            r"5a-\frac3a=2",
            font_size=52,
            color=INK,
        ).move_to([3.58, -1.28, 0])
        height_equation.set_color_by_tex("2", POINT)
        f_vertex_known = MathTex("(1,2)", font_size=30, color=POINT)
        f_vertex_known.next_to(f_vertex_dot, UP + RIGHT, buff=0.12)

        self.play(self.title_change(stage_title, next_title), FadeOut(square_identity_f, axis_note), run_time=0.55)
        stage_title = next_title
        self.play(FadeIn(zero_at_one), run_time=0.65)
        self.play(
            FadeIn(height_equation),
            Succession(FadeOut(f_vertex_unknown), FadeIn(f_vertex_known)),
            run_time=0.85,
        )
        self.play(Indicate(y_two, color=POINT), Indicate(height_equation, color=POINT), run_time=0.65)
        self.wait(0.35)

        # Beat 07 derive_parameter_polynomial: solve the height equation without yet accepting either root.
        self.next_beat("derive_parameter_polynomial")
        next_title = self.stage_title("代數先給兩個候選")
        height_equation_top = height_equation.copy().move_to([3.58, 1.42, 0])
        multiply_guard = label("已知 a<0，所以可以乘以 a", 22, MUTED, "MEDIUM")
        multiply_guard.move_to([3.58, 2.15, 0])
        parameter_polynomial = MathTex(
            r"5a^2-2a-3=0",
            font_size=46,
            color=INK,
        ).move_to([3.58, 0.40, 0])
        parameter_factor = MathTex(
            r"(5a+3)(a-1)=0",
            font_size=43,
            color=INK,
        ).move_to([3.58, -0.50, 0])
        negative_card = self.candidate_card(r"a=-\frac35", POINT).move_to([2.30, -1.67, 0])
        positive_card = self.candidate_card("a=1", CORAL).move_to([4.86, -1.67, 0])
        f_context = VGroup(
            f_tag,
            ceiling,
            y_two,
            f_vertex_dot,
            f_axis,
            x_one,
            f_vertex_known,
        )

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(zero_at_one, completed_f)),
                FadeIn(multiply_guard),
            ),
            Transform(height_equation, height_equation_top),
            f_curve.animate.set_stroke(opacity=0.30),
            f_context.animate.set_opacity(0.30),
            run_time=0.65,
        )
        self.play(FadeIn(parameter_polynomial), run_time=0.75)
        self.play(FadeIn(parameter_factor), run_time=0.7)

        # Beat 08 solve_parameter_candidates: continue at a settled semantic boundary.
        self.next_beat("solve_parameter_candidates")
        self.play(FadeIn(negative_card), FadeIn(positive_card), run_time=0.6)
        self.wait(0.35)

        # Beat 09 reject_positive_opening: send both algebraic candidates back to the same graph.
        self.next_beat("reject_positive_opening")
        next_title = self.stage_title("把兩個候選真的放回圖上")
        positive_equation = MathTex(
            r"a=1:\quad f(x)=(x-1)^2+2",
            font_size=40,
            color=CORAL,
        ).move_to([3.58, 0.18, 0])
        positive_verdict = label("2 是最低值，不符合題目", 27, CORAL, "BOLD")
        positive_verdict.move_to([3.58, -0.70, 0])
        minimum_word = label("最低點", 22, CORAL, "BOLD")
        minimum_word.next_to(f_vertex_dot, UP + RIGHT, buff=0.13)

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            FadeOut(multiply_guard, height_equation, parameter_polynomial, parameter_factor),
            negative_card.animate.move_to([2.30, 1.48, 0]),
            positive_card.animate.move_to([4.86, 1.48, 0]),
            f_curve.animate.set_stroke(opacity=1.0),
            f_context.animate.set_opacity(1.0),
            run_time=0.70,
        )
        self.play(
            Indicate(positive_card, color=CORAL),
            Transform(f_curve, upward_trial),
            FadeIn(positive_equation, positive_verdict, minimum_word),
            run_time=0.95,
        )
        wrong_slash = Line(
            positive_card.get_corner(DOWN + LEFT),
            positive_card.get_corner(UP + RIGHT),
            color=CORAL,
            stroke_width=5.0,
        ).set_z_index(10)
        self.play(Create(wrong_slash), Circumscribe(f_vertex_dot, color=CORAL), run_time=0.6)

        # Beat 10 reject_wrong_opening: continue at a settled semantic boundary.
        self.next_beat("reject_wrong_opening")
        self.play(FadeOut(positive_equation, positive_verdict, minimum_word), run_time=0.35)
        negative_equation = MathTex(
            r"a=-\frac35:\quad f(x)=-\frac35(x-1)^2+2",
            font_size=38,
            color=POINT,
        ).move_to([3.58, 0.12, 0])
        choice_note = label("負根讓 2 保持最高值", 27, POINT, "BOLD")
        choice_note.move_to([3.58, -0.72, 0])
        chosen_box = SurroundingRectangle(negative_card, color=POINT, buff=0.10, stroke_width=3)
        chosen_parameter = MathTex(r"a=-\frac35", font_size=47, color=POINT)
        chosen_parameter.move_to([3.58, -1.65, 0])
        self.play(
            Transform(f_curve, f_curve_target),
            Indicate(negative_card, color=POINT),
            FadeIn(negative_equation, choice_note),
            FadeIn(chosen_box),
            run_time=0.95,
        )
        self.play(FadeIn(chosen_parameter), run_time=0.65)
        self.wait(0.35)

        # Beat 11 verify_f_algebraically: translate the selected square form back into visible graph facts.
        self.next_beat("verify_f_algebraically")
        next_title = self.stage_title("回到原圖，確認最高值真的成立")
        f_exact = MathTex(
            r"f(x)=-\frac35(x-1)^2+2",
            font_size=43,
            color=BLUE,
        ).move_to([3.58, 1.05, 0])
        f_bound = MathTex(
            r"(x-1)^2\ge0\quad\Longrightarrow\quad f(x)\le2",
            font_size=39,
            color=INK,
        ).move_to([3.58, 0.05, 0])
        f_equality = MathTex(
            r"f(x)=2\quad\Longleftrightarrow\quad x=1",
            font_size=39,
            color=REGION,
        ).move_to([3.58, -0.88, 0])
        symmetric_height = Fraction(7, 5)
        symmetric_dots = VGroup(
            Dot(axes.c2p(0, float(symmetric_height)), radius=0.075, color=REGION),
            Dot(axes.c2p(2, float(symmetric_height)), radius=0.075, color=REGION),
        ).set_z_index(8)
        symmetric_join = DashedLine(
            symmetric_dots[0].get_center(),
            symmetric_dots[1].get_center(),
            color=REGION,
            dash_length=0.08,
            stroke_width=2.2,
        )
        symmetric_labels = VGroup(
            MathTex("x=0", font_size=23, color=REGION).next_to(symmetric_dots[0], DOWN, buff=0.11),
            MathTex("x=2", font_size=23, color=REGION).next_to(symmetric_dots[1], DOWN, buff=0.11),
        )
        sample_readout = MathTex(
            r"f(0)=f(2)=\frac75<2",
            font_size=36,
            color=REGION,
        ).move_to([3.58, -1.82, 0])

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            FadeOut(
                negative_card,
                positive_card,
                wrong_slash,
                chosen_box,
                negative_equation,
                choice_note,
            ),
            chosen_parameter.animate.move_to([3.58, 2.02, 0]),
            run_time=0.60,
        )
        self.play(FadeIn(f_exact), run_time=0.75)
        self.play(FadeIn(f_bound), FadeIn(f_equality), run_time=0.85)

        # Beat 12 verify_f_in_picture: continue at a settled semantic boundary.
        self.next_beat("verify_f_in_picture")
        self.play(
            FadeIn(symmetric_dots, symmetric_labels),
            Create(symmetric_join),
            FadeIn(sample_readout),
            run_time=0.75,
        )
        self.play(Circumscribe(f_vertex_dot, color=POINT), run_time=0.6)
        self.wait(0.35)

        # Beat 13 write_g_with_chosen_parameter: carry the verified parameter into the second quadratic.
        self.next_beat("write_g_with_chosen_parameter")
        next_title = self.stage_title("同一個 a，換到第二條拋物線")
        g_formula = MathTex(
            r"g(x)=-ax^2+4ax+6a-\frac3a",
            font_size=37,
            color=INK,
        ).move_to([3.58, 1.32, 0])
        g_formula.set_color_by_tex("a", POINT)
        copied_parameter = MathTex(r"a=-\frac35", font_size=43, color=POINT)
        copied_parameter.move_to([3.58, 0.35, 0])
        leading_sign = MathTex(
            r"-a=\frac35>0",
            font_size=43,
            color=PURPLE,
        ).move_to([3.58, -0.52, 0])
        g_prompt = label("所以 g 向上開，應該找最低點", 27, PURPLE, "BOLD")
        g_prompt.move_to([3.58, -1.50, 0])
        g_curve = axes.plot(
            lambda x: 0.6 * (x - 2) ** 2 - 1,
            x_range=[-1.0, 5.0],
            color=PURPLE,
            stroke_width=5.0,
        ).set_z_index(5)
        g_tag = MathTex("g", font_size=30, color=PURPLE).move_to(axes.c2p(4.18, 2.05))
        g_vertex_dot = Dot(axes.c2p(2, -1), radius=0.095, color=PURPLE).set_z_index(9)
        g_vertex_question = label("最低點？", 22, PURPLE, "BOLD")
        g_vertex_question.next_to(g_vertex_dot, DOWN + RIGHT, buff=0.13)
        f_graph_context = VGroup(
            f_tag,
            ceiling,
            y_two,
            f_vertex_dot,
            f_axis,
            x_one,
            f_vertex_known,
        )

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            FadeOut(f_exact, f_bound, f_equality, sample_readout, symmetric_dots, symmetric_join, symmetric_labels),
            f_curve.animate.set_stroke(opacity=0.16),
            f_graph_context.animate.set_opacity(0.16),
            run_time=0.55,
        )
        self.play(FadeIn(g_formula), run_time=0.65)

        # Beat 14 transfer_parameter_to_g: continue at a settled semantic boundary.
        self.next_beat("transfer_parameter_to_g")
        self.play(
            Succession(FadeOut(chosen_parameter), FadeIn(copied_parameter)),
            run_time=0.60,
        )
        self.play(FadeIn(leading_sign), run_time=0.65)
        self.play(Create(g_curve), FadeIn(g_tag, g_vertex_dot, g_vertex_question, g_prompt), run_time=1.0)
        self.wait(0.35)

        # Beat 15 complete_square_for_g: complete the second square and mark its unknown vertex.
        self.next_beat("complete_square_for_g")
        next_title = self.stage_title("最低點的中心藏在 (x-2)^2")
        square_identity_g = MathTex(
            r"x^2-4x=(x-2)^2-4",
            font_size=42,
            color=REGION,
        ).move_to([3.58, 1.25, 0])
        completed_g = MathTex(
            r"g(x)=-a(x-2)^2+10a-\frac3a",
            font_size=41,
            color=INK,
        ).move_to([3.58, 0.02, 0])
        completed_g.set_color_by_tex("(x-2)^2", REGION)
        minimum_rule = MathTex(
            r"-a>0,\quad (x-2)^2\ge0",
            font_size=40,
            color=PURPLE,
        ).move_to([3.58, -1.24, 0])
        g_axis = DashedLine(
            axes.c2p(2, -5.5),
            axes.c2p(2, 4.55),
            color=REGION,
            dash_length=0.10,
            stroke_width=2.5,
        ).set_z_index(3)
        x_two = MathTex("2", font_size=27, color=REGION).next_to(
            axes.c2p(2, 0), DOWN, buff=0.11
        )
        g_vertex_unknown = MathTex("(2,?)", font_size=30, color=PURPLE)
        g_vertex_unknown.next_to(g_vertex_dot, DOWN + RIGHT, buff=0.12)

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(copied_parameter, leading_sign, g_prompt, g_formula)),
                FadeIn(square_identity_g),
            ),
            run_time=0.65,
        )
        self.play(FadeIn(completed_g), run_time=0.8)

        # Beat 16 locate_g_axis: continue at a settled semantic boundary.
        self.next_beat("locate_g_axis")
        self.play(
            Create(g_axis),
            FadeIn(x_two),
            Succession(FadeOut(g_vertex_question), FadeIn(g_vertex_unknown)),
            run_time=0.75,
        )
        self.play(FadeIn(minimum_rule), Circumscribe(g_vertex_dot, color=REGION), run_time=0.7)
        self.wait(0.35)

        # Beat 17 substitute_g_vertex: settle on two traceable contributions without summing them.
        self.next_beat("substitute_g_vertex")
        next_title = self.stage_title("先算兩份貢獻，不急著相加")
        at_vertex = MathTex(
            r"g(2)=10a-\frac3a",
            font_size=45,
            color=INK,
        ).move_to([3.58, 1.43, 0])
        substitution = MathTex(
            r"=10\left(-\frac35\right)-\frac3{-\frac35}",
            font_size=41,
            color=INK,
        ).move_to([3.58, 0.48, 0])
        negative_term = self.term_card("10a=-6", BLUE).move_to([2.25, -0.62, 0])
        positive_term = self.term_card(r"-\frac3a=+5", REGION).move_to([4.90, -0.62, 0])
        unsummed = MathTex("-6", "+", "5", font_size=58, color=INK)
        unsummed[0].set_color(BLUE)
        unsummed[2].set_color(REGION)
        unsummed.move_to([3.58, -1.82, 0])

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            FadeOut(square_identity_g, minimum_rule, completed_g),
            run_time=0.45,
        )
        self.play(FadeIn(at_vertex), run_time=0.70)
        self.play(FadeIn(substitution), run_time=0.75)

        # Beat 18 settle_minimum_preanswer: continue at a settled semantic boundary.
        self.next_beat("settle_minimum_preanswer")
        self.play(FadeIn(negative_term), FadeIn(positive_term), run_time=0.65)
        self.play(FadeIn(unsummed), run_time=0.65)
        self.play(Indicate(negative_term, color=BLUE), Indicate(positive_term, color=REGION), run_time=0.6)
        self.wait(0.45)

        # Beat 19 walk_signed_value_line: move five units on a number line, then return the result to g.
        self.next_beat("walk_signed_value_line")
        next_title = self.stage_title("向右補 5 格，落在真正的最低值")
        value_line = NumberLine(
            x_range=[-7, 1, 1],
            length=4.85,
            include_numbers=False,
            include_ticks=True,
            color=MUTED,
            stroke_width=2.3,
        ).move_to([3.58, 0.12, 0])
        start_dot = Dot(value_line.n2p(-6), radius=0.085, color=BLUE)
        start_label = MathTex("-6", font_size=31, color=BLUE).next_to(start_dot, DOWN, buff=0.16)
        end_dot = Dot(value_line.n2p(-1), radius=0.095, color=POINT)
        end_label = MathTex("-1", font_size=34, color=POINT).next_to(end_dot, DOWN, buff=0.16)
        five_step = Arrow(
            value_line.n2p(-6) + UP * 0.34,
            value_line.n2p(-1) + UP * 0.34,
            buff=0.0,
            color=REGION,
            stroke_width=5.0,
            max_tip_length_to_length_ratio=0.10,
        )
        five_label = MathTex("+5", font_size=32, color=REGION).next_to(five_step, UP, buff=0.08)
        g_exact = MathTex(
            r"g(x)=\frac35(x-2)^2-1\ge-1",
            font_size=40,
            color=PURPLE,
        ).move_to([3.58, 1.55, 0])
        sum_result = MathTex("-6", "+", "5", "=", "-1", font_size=48, color=INK)
        sum_result[0].set_color(BLUE)
        sum_result[2].set_color(REGION)
        sum_result[4].set_color(POINT)
        sum_result.move_to([3.58, -1.05, 0])
        final_answer = MathTex(
            r"\min_{x\in\mathbb R}g(x)=-1",
            font_size=47,
            color=POINT,
        ).move_to([3.58, -1.95, 0])
        answer_box = SurroundingRectangle(final_answer, color=POINT, buff=0.14, stroke_width=3)
        g_vertex_exact = MathTex("(2,-1)", font_size=30, color=POINT)
        g_vertex_exact.next_to(g_vertex_dot, DOWN + RIGHT, buff=0.12)

        self.play(self.title_change(stage_title, next_title), run_time=0.55)
        stage_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(at_vertex, substitution, negative_term, positive_term)),
                FadeIn(VGroup(value_line, start_dot, start_label)),
            ),
            run_time=0.65,
        )
        self.play(Create(five_step), FadeIn(five_label), run_time=0.85)
        self.play(FadeIn(end_dot, end_label), run_time=0.45)

        # Beat 20 reveal_minimum: continue at a settled semantic boundary.
        self.next_beat("reveal_minimum")
        self.play(
            Succession(FadeOut(unsummed), FadeIn(sum_result)),
            Succession(FadeOut(g_vertex_unknown), FadeIn(g_vertex_exact)),
            run_time=0.75,
        )
        self.play(FadeIn(g_exact), run_time=0.75)
        self.play(FadeIn(final_answer), FadeIn(answer_box), run_time=0.75)
        self.play(Circumscribe(g_vertex_dot, color=POINT), run_time=0.65)
        self.wait(0.45)
