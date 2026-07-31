"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q13."""

from __future__ import annotations

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
    Circle,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    NumberLine,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    VGroup,
    Write,
    rate_functions,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


F_COEFFICIENTS = (1, 7, -5, 8)


def polynomial_value(coefficients: tuple[int, ...], value: int) -> int:
    """Evaluate integer coefficients ordered from highest degree to constant."""
    result = 0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def shifted_cube_coefficients(shift: int) -> tuple[int, int, int, int]:
    """Return coefficients of (a+shift)^3."""
    return (1, 3 * shift, 3 * shift**2, shift**3)


def subtract_coefficients(
    first: tuple[int, ...], second: tuple[int, ...]
) -> tuple[int, ...]:
    """Subtract equal-degree integer polynomials coefficient by coefficient."""
    if len(first) != len(second):
        raise ValueError("polynomials must have the same degree")
    return tuple(left - right for left, right in zip(first, second))


def expression(a_value: int) -> int:
    """Return F(a)=a^3+7a^2-5a+8 exactly."""
    return polynomial_value(F_COEFFICIENTS, a_value)


FIRST_DIFFERENCE = subtract_coefficients(
    F_COEFFICIENTS, shifted_cube_coefficients(1)
)
MIDDLE_DIFFERENCE = subtract_coefficients(
    F_COEFFICIENTS, shifted_cube_coefficients(2)
)
UPPER_DIFFERENCE = subtract_coefficients(
    shifted_cube_coefficients(3), F_COEFFICIENTS
)
SAMPLE_VALUES = {4: 164, 16: 5816, 18: 8018}

if FIRST_DIFFERENCE != (0, 4, -8, 7):
    raise ValueError("F(a)-(a+1)^3 identity is incorrect")
if MIDDLE_DIFFERENCE != (0, 1, -17, 0):
    raise ValueError("F(a)-(a+2)^3 identity is incorrect")
if UPPER_DIFFERENCE != (0, 2, 32, 19):
    raise ValueError("(a+3)^3-F(a) identity is incorrect")
for a_value in (1, 2, 4, 16, 17, 18, 31, 1000):
    if expression(a_value) - (a_value + 1) ** 3 != 4 * (a_value - 1) ** 2 + 3:
        raise ValueError("first exact cube difference failed")
    if expression(a_value) - (a_value + 2) ** 3 != a_value * (a_value - 17):
        raise ValueError("middle exact cube difference failed")
    if (a_value + 3) ** 3 - expression(a_value) != 2 * a_value**2 + 32 * a_value + 19:
        raise ValueError("upper exact cube difference failed")
if any(expression(a_value) != expected for a_value, expected in SAMPLE_VALUES.items()):
    raise ValueError("one of the concrete exploration values is incorrect")
if any(
    not ((a_value + 1) ** 3 < expression(a_value) < (a_value + 2) ** 3)
    for a_value in range(1, 17)
):
    raise ValueError("left consecutive-cube interval check failed")
if any(
    not ((a_value + 2) ** 3 < expression(a_value) < (a_value + 3) ** 3)
    for a_value in range(18, 1001)
):
    raise ValueError("right consecutive-cube interval check failed")
if expression(0) != 2**3:
    raise ValueError("the excluded a=0 boundary counterexample was lost")
if expression(17) != 19**3 or (19 - 1 + 1) ** 3 != expression(17):
    raise ValueError("the positive-integer solution does not verify")


class CarloTcfs113MathQ13(CarloSlide):
    """Trap F(a) between neighboring cubes and isolate the switching value."""

    lesson_id = "carlo.tcfs_113_math_gifted.q13"

    RAIL_X = (-5.72, -3.27, -0.82)
    RAIL_Y = -0.18

    @staticmethod
    def transition_title(scene: "CarloTcfs113MathQ13", old, new) -> None:
        """Swap CJK titles without overlapping two semantic labels."""
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.58)

    @classmethod
    def rail_base(cls) -> VGroup:
        """Build the stable three-stop rail used for neighboring cubes."""
        line = Line(
            [cls.RAIL_X[0] - 0.55, cls.RAIL_Y, 0],
            [cls.RAIL_X[2] + 0.55, cls.RAIL_Y, 0],
            color=MUTED,
            stroke_width=3,
        )
        ticks = VGroup(
            *[
                Line(
                    [x_coord, cls.RAIL_Y - 0.18, 0],
                    [x_coord, cls.RAIL_Y + 0.18, 0],
                    color=INK,
                    stroke_width=3.2,
                )
                for x_coord in cls.RAIL_X
            ]
        )
        return VGroup(line, ticks)

    @classmethod
    def rail_position(cls, a_value: int) -> float:
        """Map F(a) exactly within its neighboring cube interval."""
        cube_values = tuple((a_value + shift) ** 3 for shift in (1, 2, 3))
        value = expression(a_value)
        if value <= cube_values[1]:
            fraction = (value - cube_values[0]) / (cube_values[1] - cube_values[0])
            return cls.RAIL_X[0] + fraction * (cls.RAIL_X[1] - cls.RAIL_X[0])
        fraction = (value - cube_values[1]) / (cube_values[2] - cube_values[1])
        return cls.RAIL_X[1] + fraction * (cls.RAIL_X[2] - cls.RAIL_X[1])

    @classmethod
    def numeric_cube_labels(cls, a_value: int) -> VGroup:
        """Label three consecutive cube stops for one concrete integer a."""
        return VGroup(
            *[
                MathTex(
                    f"{a_value + shift}^3={((a_value + shift) ** 3)}",
                    font_size=25,
                    color=INK if shift != 2 else BLUE,
                ).move_to([x_coord, cls.RAIL_Y - 0.72, 0])
                for shift, x_coord in zip((1, 2, 3), cls.RAIL_X)
            ]
        )

    @classmethod
    def numeric_value_label(cls, a_value: int) -> MathTex:
        """Place the exact F(a) readout above its point on the rail."""
        return MathTex(
            f"F({a_value})={expression(a_value)}",
            font_size=32,
            color=POINT,
        ).move_to([cls.rail_position(a_value), cls.RAIL_Y + 0.72, 0])

    @classmethod
    def symbolic_cube_labels(cls) -> VGroup:
        """Label the rail with the three shifted cubes."""
        return VGroup(
            *[
                MathTex(
                    f"(a+{shift})^3",
                    font_size=31,
                    color=INK if shift != 2 else BLUE,
                ).move_to([x_coord, cls.RAIL_Y - 0.72, 0])
                for shift, x_coord in zip((1, 2, 3), cls.RAIL_X)
            ]
        )

    @staticmethod
    def positive_term_tile(tex: str, color: str) -> VGroup:
        """Create one compact tile for an independently positive term."""
        frame = RoundedRectangle(
            width=1.82,
            height=1.30,
            corner_radius=0.06,
            color=color,
            stroke_width=2.5,
            fill_color=BG,
            fill_opacity=0.96,
        )
        term = MathTex(tex, font_size=35, color=color)
        positive = MathTex(">0", font_size=25, color=INK)
        content = VGroup(term, positive).arrange(DOWN, buff=0.16).move_to(frame)
        return VGroup(frame, content)

    def construct(self) -> None:
        heading = label("第 13 題｜在相鄰立方數之間找唯一落點", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 13 頁｜影片 zUVNQX92b64 00:00-01:13",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)
        divider = Line([0.68, -3.52, 0], [0.68, 3.40, 0], color=HAIRLINE, stroke_width=1.5)

        # Beat 01 meet_cube_rail: start from one concrete value between two cubes.
        self.begin_beat("meet_cube_rail")
        stage_title = label("先把一個數放進立方數刻度", 33, INK, "BOLD")
        stage_title.move_to([4.25, 3.02, 0])
        definition = MathTex(
            "F(a)",
            "=",
            "a^3+7a^2-5a+8",
            font_size=42,
            color=INK,
        )
        definition[0].set_color(POINT)
        target = MathTex("F(a)=(b+1)^3", font_size=46, color=INK)
        domain = MathTex(r"a,b\in\mathbb{Z}_{>0}", font_size=38, color=REGION)
        intro_panel = VGroup(definition, target, domain).arrange(DOWN, buff=0.48)
        intro_panel.move_to([4.25, -0.15, 0])

        rail = self.rail_base()
        labels_4 = self.numeric_cube_labels(4)
        value_dot = Dot(
            [self.rail_position(4), self.RAIL_Y, 0], radius=0.105, color=POINT
        ).set_z_index(8)
        value_label = self.numeric_value_label(4)
        sample_caption = label("先試 a = 4", 29, BLUE, "BOLD")
        sample_caption.move_to([-3.27, 1.70, 0])
        gap_note = label("它落在兩個立方數之間", 27, CORAL, "BOLD")
        gap_note.move_to([-3.27, -1.70, 0])

        self.add(heading, source, divider)
        self.play(FadeIn(stage_title), Write(definition), run_time=0.85)
        self.play(Write(target), FadeIn(domain), run_time=0.75)
        self.play(FadeIn(sample_caption), Create(rail), run_time=0.70)

        self.next_beat("place_sample_value")
        self.play(FadeIn(labels_4), GrowFromCenter(value_dot), FadeIn(value_label), run_time=0.80)
        self.play(FadeIn(gap_note), Indicate(value_dot, color=POINT), run_time=0.65)
        self.wait(0.35)

        # Beat 02 scan_integers: deliberate integer samples reveal a switch near 17.
        self.next_beat("scan_integers")
        next_title = label("換幾個整數，落點會越過中間刻度", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        scan_question = label("哪一次會剛好碰到刻度？", 31, POINT, "BOLD")
        scan_question.move_to([4.25, -2.05, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(labels_4), FadeOut(value_label), FadeOut(gap_note), run_time=0.38)

        labels_16 = self.numeric_cube_labels(16)
        value_16 = self.numeric_value_label(16)
        caption_16 = label("再試 a = 16", 29, BLUE, "BOLD").move_to(sample_caption)
        self.play(Succession(FadeOut(sample_caption), FadeIn(caption_16)), run_time=0.45)
        sample_caption = caption_16
        self.play(
            value_dot.animate.move_to([self.rail_position(16), self.RAIL_Y, 0]),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(labels_16), FadeIn(value_16), run_time=0.42)
        self.wait(0.20)

        self.next_beat("scan_past_seventeen")
        self.play(FadeOut(labels_16), FadeOut(value_16), run_time=0.32)
        labels_18 = self.numeric_cube_labels(18)
        value_label = self.numeric_value_label(18)
        caption_18 = label("再試 a = 18", 29, BLUE, "BOLD").move_to(sample_caption)
        self.play(Succession(FadeOut(sample_caption), FadeIn(caption_18)), run_time=0.45)
        sample_caption = caption_18
        self.play(
            value_dot.animate.move_to([self.rail_position(18), self.RAIL_Y, 0]),
            run_time=0.85,
            rate_func=rate_functions.ease_in_out_sine,
        )
        self.play(FadeIn(labels_18), FadeIn(value_label), run_time=0.42)

        self.next_beat("ask_cube_landing_question")
        self.play(FadeIn(scan_question), run_time=0.45)
        self.wait(0.40)

        # Beat 03 name_cube_corridor: generalize only after the concrete scan.
        self.next_beat("name_cube_corridor")
        next_title = label("要成為立方數，就不能停在縫裡", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        symbolic_labels = self.symbolic_cube_labels()
        symbolic_value = MathTex("F(a)", font_size=34, color=POINT)
        symbolic_value.move_to([-4.40, self.RAIL_Y + 0.72, 0])
        corridor_note = VGroup(
            label("三個刻度是連續整數的立方", 27, MUTED, "MEDIUM"),
            label("先問 F(a) 位在哪兩格之間", 31, POINT, "BOLD"),
        ).arrange(DOWN, buff=0.34)
        corridor_note.move_to([4.25, -0.35, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(labels_18), FadeOut(value_label), FadeOut(sample_caption), run_time=0.38)
        self.play(
            value_dot.animate.move_to([-4.40, self.RAIL_Y, 0]),
            FadeIn(symbolic_labels),
            FadeIn(symbolic_value),
            run_time=0.70,
        )
        self.play(FadeOut(intro_panel), FadeOut(scan_question), run_time=0.38)
        self.play(LaggedStart(*(FadeIn(item) for item in corridor_note), lag_ratio=0.20), run_time=0.75)
        self.wait(0.40)

        # Beat 04 prove_first_floor: earn the lower neighboring-cube bound.
        self.next_beat("prove_first_floor")
        next_title = label("F(a) 永遠越過第一個刻度", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        first_line = MathTex(r"F(a)-(a+1)^3", font_size=43, color=INK)
        first_expand = MathTex(r"=4a^2-8a+7", font_size=43, color=INK)
        first_positive = MathTex(r"=4(a-1)^2+3>0", font_size=43, color=REGION)
        first_bound = MathTex(r"(a+1)^3<F(a)", font_size=50, color=POINT)
        first_panel = VGroup(first_line, first_expand, first_positive, first_bound).arrange(
            DOWN, aligned_edge=LEFT, buff=0.42
        )
        first_panel.move_to([4.25, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(corridor_note), run_time=0.32)
        self.play(Write(first_line), run_time=0.55)
        self.play(Write(first_expand), run_time=0.55)
        self.play(Write(first_positive), run_time=0.65)

        self.next_beat("state_first_floor_bound")
        self.play(
            Write(first_bound),
            value_dot.animate.move_to([-4.18, self.RAIL_Y, 0]),
            symbolic_value.animate.move_to([-4.18, self.RAIL_Y + 0.72, 0]),
            run_time=0.72,
        )
        self.play(Indicate(symbolic_labels[0], color=BLUE), run_time=0.55)
        self.wait(0.35)

        # Beat 05 find_switch_at_seventeen: the middle comparison changes sign once.
        self.next_beat("find_switch_at_seventeen")
        next_title = label("和中間刻度比較，關鍵只在 17", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        sign_line = NumberLine(
            x_range=[0, 21, 1],
            length=6.15,
            include_numbers=False,
            include_tip=True,
            color=MUTED,
            stroke_width=2.6,
        ).move_to([-3.30, -0.28, 0])
        negative_segment = Line(
            sign_line.n2p(0.45), sign_line.n2p(16.70), color=CORAL, stroke_width=7
        )
        positive_segment = Line(
            sign_line.n2p(17.30), sign_line.n2p(20.45), color=REGION, stroke_width=7
        )
        zero_open = Circle(
            radius=0.105,
            color=CORAL,
            stroke_width=3,
            fill_color=BG,
            fill_opacity=1,
        ).move_to(sign_line.n2p(0))
        seventeen_dot = Dot(sign_line.n2p(17), radius=0.105, color=POINT)
        sign_labels = VGroup(
            MathTex("0", font_size=28, color=CORAL).next_to(sign_line.n2p(0), DOWN, buff=0.18),
            MathTex("17", font_size=31, color=POINT).next_to(sign_line.n2p(17), DOWN, buff=0.18),
            MathTex("-", font_size=40, color=CORAL).move_to(sign_line.n2p(9) + UP * 0.55),
            MathTex("+", font_size=40, color=REGION).move_to(sign_line.n2p(19) + UP * 0.55),
        )
        domain_note = label("a 是正整數：0 不在範圍內", 25, CORAL, "BOLD")
        domain_note.move_to([-3.30, -1.62, 0])
        middle_identity = MathTex(
            r"F(a)-(a+2)^3",
            "=",
            r"a(a-17)",
            font_size=44,
            color=INK,
        )
        middle_identity[2].set_color(BLUE)
        middle_cases = VGroup(
            MathTex(r"1\le a<17:\quad F(a)<(a+2)^3", font_size=34, color=CORAL),
            MathTex(r"a=17:\quad F(a)=(a+2)^3", font_size=36, color=POINT),
            MathTex(r"a>17:\quad F(a)>(a+2)^3", font_size=34, color=REGION),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.44)
        middle_panel = VGroup(middle_identity, middle_cases).arrange(DOWN, buff=0.62)
        middle_panel.move_to([4.25, -0.22, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(rail),
            FadeOut(symbolic_labels),
            FadeOut(symbolic_value),
            FadeOut(value_dot),
            FadeOut(first_panel),
            Create(sign_line),
            run_time=0.70,
        )
        self.play(Create(negative_segment), Create(positive_segment), run_time=0.65)
        self.play(FadeIn(zero_open), GrowFromCenter(seventeen_dot), FadeIn(sign_labels), run_time=0.65)

        self.next_beat("classify_switch_ranges")
        self.play(Write(middle_identity), run_time=0.75)
        self.play(LaggedStart(*(Write(row) for row in middle_cases), lag_ratio=0.22), run_time=1.10)
        self.play(FadeIn(domain_note), Indicate(zero_open, color=CORAL), run_time=0.65)
        self.wait(0.40)

        # Beat 06 exclude_left_range: trap every positive a below 17 in one cube gap.
        self.next_beat("exclude_left_range")
        next_title = label("小於 17：卡在前兩個立方數之間", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        rail = self.rail_base()
        symbolic_labels = self.symbolic_cube_labels()
        value_dot = Dot([-4.20, self.RAIL_Y, 0], radius=0.105, color=POINT)
        symbolic_value = MathTex("F(a)", font_size=34, color=POINT)
        symbolic_value.move_to([-4.20, self.RAIL_Y + 0.72, 0])
        left_gap = SurroundingRectangle(
            VGroup(symbolic_labels[0], symbolic_labels[1]),
            color=CORAL,
            buff=0.28,
            stroke_width=2.8,
        )
        left_case = MathTex(r"1\le a<17", font_size=43, color=BLUE)
        left_trap = MathTex(
            r"(a+1)^3<F(a)<(a+2)^3",
            font_size=43,
            color=INK,
        )
        left_impossible = label("相鄰立方數之間，沒有另一個整數立方數", 27, CORAL, "BOLD")
        left_panel = VGroup(left_case, left_trap, left_impossible).arrange(DOWN, buff=0.55)
        left_panel.move_to([4.25, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(sign_line),
            FadeOut(negative_segment),
            FadeOut(positive_segment),
            FadeOut(zero_open),
            FadeOut(seventeen_dot),
            FadeOut(sign_labels),
            FadeOut(domain_note),
            FadeOut(middle_panel),
            Create(rail),
            FadeIn(symbolic_labels),
            FadeIn(value_dot),
            FadeIn(symbolic_value),
            run_time=0.82,
        )
        self.play(Write(left_case), run_time=0.45)
        self.play(Write(left_trap), Create(left_gap), run_time=0.72)
        self.play(FadeIn(left_impossible), Indicate(value_dot, color=CORAL), run_time=0.68)
        self.wait(0.38)

        # Beat 07 prove_third_ceiling: every positive term keeps F below the third cube.
        self.next_beat("prove_third_ceiling")
        next_title = label("第三個刻度永遠還在 F(a) 的右邊", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        positive_tiles = VGroup(
            self.positive_term_tile("2a^2", BLUE),
            MathTex("+", font_size=38, color=MUTED),
            self.positive_term_tile("32a", PURPLE),
            MathTex("+", font_size=38, color=MUTED),
            self.positive_term_tile("19", REGION),
        ).arrange(RIGHT, buff=0.18)
        positive_tiles.move_to([-3.28, -0.15, 0])
        positive_caption = label("a > 0，所以三項都為正", 27, POINT, "BOLD")
        positive_caption.move_to([-3.28, -1.36, 0])
        upper_identity = MathTex(
            r"(a+3)^3-F(a)",
            "=",
            r"2a^2+32a+19",
            font_size=42,
            color=INK,
        )
        upper_identity[2].set_color(REGION)
        upper_positive = MathTex(r"2a^2+32a+19>0", font_size=40, color=REGION)
        upper_bound = MathTex(r"F(a)<(a+3)^3", font_size=50, color=POINT)
        upper_panel = VGroup(upper_identity, upper_positive, upper_bound).arrange(
            DOWN, buff=0.52
        )
        upper_panel.move_to([4.25, -0.22, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(rail),
            FadeOut(symbolic_labels),
            FadeOut(value_dot),
            FadeOut(symbolic_value),
            FadeOut(left_gap),
            FadeOut(left_panel),
            run_time=0.42,
        )
        self.play(LaggedStart(*(FadeIn(item) for item in positive_tiles), lag_ratio=0.12), run_time=0.85)
        self.play(FadeIn(positive_caption), Write(upper_identity), run_time=0.70)

        self.next_beat("state_third_ceiling")
        self.play(Write(upper_positive), run_time=0.55)
        self.play(Write(upper_bound), run_time=0.55)
        self.wait(0.38)

        # Beat 08 exclude_right_range: trap every a above 17 in the next cube gap.
        self.next_beat("exclude_right_range")
        next_title = label("大於 17：卡在後兩個立方數之間", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        rail = self.rail_base()
        symbolic_labels = self.symbolic_cube_labels()
        value_dot = Dot([-2.32, self.RAIL_Y, 0], radius=0.105, color=POINT)
        symbolic_value = MathTex("F(a)", font_size=34, color=POINT)
        symbolic_value.move_to([-2.32, self.RAIL_Y + 0.72, 0])
        right_gap = SurroundingRectangle(
            VGroup(symbolic_labels[1], symbolic_labels[2]),
            color=CORAL,
            buff=0.28,
            stroke_width=2.8,
        )
        right_case = MathTex(r"a>17", font_size=43, color=BLUE)
        right_trap = MathTex(
            r"(a+2)^3<F(a)<(a+3)^3",
            font_size=43,
            color=INK,
        )
        right_impossible = label("這個縫裡也沒有整數立方數", 29, CORAL, "BOLD")
        right_panel = VGroup(right_case, right_trap, right_impossible).arrange(DOWN, buff=0.55)
        right_panel.move_to([4.25, -0.20, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(FadeOut(positive_tiles), FadeOut(positive_caption), FadeOut(upper_panel), run_time=0.42)
        self.play(
            Create(rail),
            FadeIn(symbolic_labels),
            FadeIn(value_dot),
            FadeIn(symbolic_value),
            run_time=0.65,
        )
        self.play(Write(right_case), run_time=0.45)

        self.next_beat("trap_right_range")
        self.play(Write(right_trap), Create(right_gap), run_time=0.72)
        self.play(FadeIn(right_impossible), Indicate(value_dot, color=CORAL), run_time=0.65)
        self.wait(0.38)

        # Beat 09 isolate_boundary: only the sign-switching integer remains.
        self.next_beat("isolate_boundary")
        next_title = label("兩邊都排除，只剩切換的那一格", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        excluded_zero = VGroup(
            MathTex("a=0", font_size=39, color=MUTED),
            label("不符合正整數條件", 23, CORAL, "BOLD"),
        ).arrange(DOWN, buff=0.18)
        excluded_zero.move_to([-4.85, 0.25, 0])
        boundary_arrow = Line([-4.10, 0.25, 0], [-1.40, 0.25, 0], color=MUTED, stroke_width=3)
        boundary_dot = Dot([-2.25, 0.25, 0], radius=0.13, color=POINT)
        boundary_label = MathTex("17", font_size=48, color=POINT).next_to(boundary_dot, UP, buff=0.20)
        boundary_note = label("唯一仍需檢查的正整數", 28, POINT, "BOLD")
        boundary_note.move_to([-2.75, -1.02, 0])
        case_rows = VGroup(
            VGroup(
                MathTex(r"1\le a<17", font_size=36, color=BLUE),
                label("在前一個立方數縫中", 24, CORAL, "BOLD"),
            ).arrange(RIGHT, buff=0.48),
            VGroup(
                MathTex(r"a=17", font_size=40, color=POINT),
                label("可能正好碰到刻度", 27, POINT, "BOLD"),
            ).arrange(RIGHT, buff=0.48),
            VGroup(
                MathTex(r"a>17", font_size=36, color=BLUE),
                label("在後一個立方數縫中", 24, CORAL, "BOLD"),
            ).arrange(RIGHT, buff=0.48),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.62)
        case_rows.move_to([4.25, -0.22, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(rail),
            FadeOut(symbolic_labels),
            FadeOut(value_dot),
            FadeOut(symbolic_value),
            FadeOut(right_gap),
            FadeOut(right_panel),
            run_time=0.42,
        )
        self.play(FadeIn(excluded_zero), Create(boundary_arrow), GrowFromCenter(boundary_dot), run_time=0.70)
        self.play(FadeIn(boundary_label), FadeIn(boundary_note), run_time=0.52)

        self.next_beat("compare_remaining_cases")
        self.play(LaggedStart(*(FadeIn(row) for row in case_rows), lag_ratio=0.22), run_time=0.95)
        self.play(Circumscribe(case_rows[1], color=POINT), run_time=0.70)
        self.wait(0.38)

        # Beat 10 verify_boundary: settle on b+1=19 but preserve the answer pause.
        self.next_beat("verify_boundary")
        next_title = label("代回切換點，最後只差一步", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        boundary_a = MathTex("a=17", font_size=50, color=POINT)
        difference_zero = MathTex(
            r"F(17)-19^3=17(17-17)=0",
            font_size=40,
            color=INK,
        )
        exact_cube = MathTex(r"F(17)=19^3", font_size=55, color=REGION)
        verify_left = VGroup(boundary_a, difference_zero, exact_cube).arrange(DOWN, buff=0.58)
        verify_left.move_to([-3.30, -0.22, 0])
        equation_match = MathTex(r"(b+1)^3=19^3", font_size=50, color=INK)
        root_match = MathTex(r"b+1=19", font_size=54, color=BLUE)
        last_question = VGroup(
            label("最後一步", 27, MUTED, "MEDIUM"),
            MathTex("b=?", font_size=66, color=POINT),
        ).arrange(DOWN, buff=0.28)
        verify_right = VGroup(equation_match, root_match, last_question).arrange(DOWN, buff=0.55)
        verify_right.move_to([4.25, -0.25, 0])
        self.transition_title(self, stage_title, next_title)
        stage_title = next_title
        self.play(
            FadeOut(excluded_zero),
            FadeOut(boundary_arrow),
            FadeOut(boundary_dot),
            FadeOut(boundary_label),
            FadeOut(boundary_note),
            FadeOut(case_rows),
            run_time=0.42,
        )
        self.play(Write(boundary_a), run_time=0.42)
        self.play(Write(difference_zero), run_time=0.72)
        self.play(Write(exact_cube), run_time=0.60)

        self.next_beat("match_cube_root")
        self.play(Write(equation_match), run_time=0.60)
        self.play(Write(root_match), run_time=0.52)
        self.play(FadeIn(last_question), run_time=0.52)
        self.wait(0.60)

        # Beat 11 reveal_pair: return to the cube rail and reveal the ordered pair.
        self.next_beat("reveal_pair")
        next_title = label("落點對齊中間刻度，答案完成", 33, INK, "BOLD")
        next_title.move_to(stage_title)
        rail = self.rail_base()
        labels_17 = self.numeric_cube_labels(17)
        final_dot = Dot(
            [self.rail_position(17), self.RAIL_Y, 0], radius=0.125, color=POINT
        ).set_z_index(8)
        final_value = self.numeric_value_label(17)
        landing_note = label("F(17) 正好落在 19³", 29, REGION, "BOLD")
        landing_note.move_to([-3.27, -1.68, 0])
        b_result = MathTex("b=18", font_size=54, color=BLUE)
        final_answer = MathTex("(a,b)=(17,18)", font_size=67, color=POINT)
        answer_box = SurroundingRectangle(
            final_answer, color=POINT, buff=0.28, stroke_width=3.5
        )
        uniqueness = label("唯一的正整數解", 29, REGION, "BOLD")
        final_panel = VGroup(b_result, VGroup(answer_box, final_answer), uniqueness).arrange(
            DOWN, buff=0.52
        )
        final_panel.move_to([4.25, -0.22, 0])
        self.transition_title(self, stage_title, next_title)
        self.play(FadeOut(verify_left), FadeOut(verify_right), run_time=0.42)
        self.play(Create(rail), FadeIn(labels_17), run_time=0.68)
        self.play(GrowFromCenter(final_dot), FadeIn(final_value), run_time=0.62)
        self.play(FadeIn(landing_note), Indicate(final_dot, color=POINT), run_time=0.62)

        self.next_beat("reveal_ordered_pair")
        self.play(Write(b_result), run_time=0.45)
        self.play(FadeIn(answer_box), Write(final_answer), run_time=0.72)
        self.play(FadeIn(uniqueness), Circumscribe(final_answer, color=POINT), run_time=0.72)
        self.wait(0.45)
