"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q6."""

from __future__ import annotations

from itertools import permutations

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
    Circumscribe,
    Create,
    Cross,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


ROOTS = (3, 12)
P_VALUE = sum(ROOTS)
Q_VALUE = ROOTS[0] * ROOTS[1]
VALUES = (-6, *ROOTS)
ALL_ORDERS = tuple(permutations(VALUES))
AP_ORDERS = tuple(
    order for order in ALL_ORDERS if order[1] - order[0] == order[2] - order[1]
)
GP_ORDERS = tuple(
    order for order in ALL_ORDERS if order[1] * order[1] == order[0] * order[2]
)
EXPECTED_AP_ORDERS = ((-6, 3, 12), (12, 3, -6))
EXPECTED_GP_ORDERS = ((3, -6, 12), (12, -6, 3))

if (P_VALUE, Q_VALUE, P_VALUE + Q_VALUE) != (15, 36, 51):
    raise ValueError("unexpected coefficient reconstruction")
if AP_ORDERS != EXPECTED_AP_ORDERS:
    raise ValueError(f"unexpected arithmetic orders: {AP_ORDERS}")
if GP_ORDERS != EXPECTED_GP_ORDERS:
    raise ValueError(f"unexpected geometric orders: {GP_ORDERS}")
if set(AP_ORDERS).intersection(GP_ORDERS):
    raise ValueError("one ordering unexpectedly satisfies both progressions")
if (3 - 3) * (3 + 6) != 0 or 3 * (2 * 3 + 6) != 36:
    raise ValueError("positive arithmetic candidate does not close")


class CarloTcfs113MathQ06(CarloSlide):
    """Use three persistent cards to reconcile two progression orderings."""

    lesson_id = "carlo.tcfs_113_math_gifted.q06"

    CARD_WIDTH = 1.62
    CARD_HEIGHT = 0.92
    MAIN_X = (-4.35, 0.0, 4.35)

    @staticmethod
    def value_color(value: int) -> str:
        return {-6: CORAL, 3: BLUE, 12: REGION}[value]

    @staticmethod
    def value_card(
        tex: str,
        color: str,
        *,
        width: float = CARD_WIDTH,
        height: float = CARD_HEIGHT,
        font_size: float = 44,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.08,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.96,
        )
        value = MathTex(tex, font_size=font_size, color=color)
        frame.set_z_index(2)
        value.set_z_index(3)
        return VGroup(frame, value)

    @classmethod
    def guide_row(cls, y: float) -> VGroup:
        baseline = Line(
            [cls.MAIN_X[0] - 0.85, y, 0],
            [cls.MAIN_X[2] + 0.85, y, 0],
            color=HAIRLINE,
            stroke_width=2,
        )
        anchors = VGroup(
            *(Dot([x_coord, y, 0], radius=0.055, color=MUTED) for x_coord in cls.MAIN_X)
        )
        captions = VGroup(
            label("首項", 20, MUTED, "MEDIUM"),
            label("中項", 21, POINT, "BOLD"),
            label("末項", 20, MUTED, "MEDIUM"),
        )
        for caption, x_coord in zip(captions, cls.MAIN_X, strict=True):
            caption.move_to([x_coord, y - 0.82, 0])
        return VGroup(baseline, anchors, captions)

    @staticmethod
    def gap_bar(
        start_x: float,
        end_x: float,
        y: float,
        tex: str,
        color: str,
    ) -> VGroup:
        segment = Line(
            [start_x, y, 0],
            [end_x, y, 0],
            color=color,
            stroke_width=5,
        )
        caps = VGroup(
            Line([start_x, y - 0.12, 0], [start_x, y + 0.12, 0], color=color, stroke_width=3),
            Line([end_x, y - 0.12, 0], [end_x, y + 0.12, 0], color=color, stroke_width=3),
        )
        equal_tick = Line(
            [(start_x + end_x) / 2 - 0.06, y - 0.11, 0],
            [(start_x + end_x) / 2 + 0.06, y + 0.11, 0],
            color=POINT,
            stroke_width=3,
        )
        gap_label = MathTex(tex, font_size=31, color=color)
        gap_label.move_to([(start_x + end_x) / 2, y + 0.42, 0])
        return VGroup(segment, caps, equal_tick, gap_label)

    @classmethod
    def permutation_panel(
        cls,
        order: tuple[int, int, int],
        center: tuple[float, float, float],
    ) -> VGroup:
        cards = VGroup(
            *(
                cls.value_card(
                    str(value),
                    cls.value_color(value),
                    width=0.98,
                    height=0.58,
                    font_size=27,
                )
                for value in order
            )
        ).arrange(RIGHT, buff=0.18)
        is_ap = order in AP_ORDERS
        is_gp = order in GP_ORDERS
        if is_ap:
            status = label("等差", 22, POINT, "BOLD")
            difference = order[1] - order[0]
            detail = MathTex("d", "=", str(difference), font_size=25, color=POINT)
        elif is_gp:
            status = label("等比", 22, REGION, "BOLD")
            ratio = "-2" if order[0] == 3 else r"-\frac{1}{2}"
            detail = MathTex("r", "=", ratio, font_size=25, color=REGION)
        else:
            status = label("兩者皆非", 20, CORAL, "MEDIUM")
            detail = MathTex(r"\times", font_size=27, color=CORAL)
            cards.set_opacity(0.38)
        panel = VGroup(cards, status, detail).arrange(DOWN, buff=0.15)
        panel.move_to(center)
        return panel

    @staticmethod
    def replace_title(scene: "CarloTcfs113MathQ06", old, new) -> None:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=0.55)

    def routed_swap(
        self,
        upper_card: VGroup,
        lower_card: VGroup,
        upper_target: tuple[float, float, float],
        lower_target: tuple[float, float, float],
        *,
        lift: float = 0.78,
    ) -> None:
        """Swap two cards on separate tracks so their labels never collide."""
        self.play(
            upper_card.animate.shift(UP * lift),
            lower_card.animate.shift(DOWN * lift),
            run_time=0.32,
        )
        self.play(
            upper_card.animate.move_to([upper_target[0], upper_target[1] + lift, 0]),
            lower_card.animate.move_to([lower_target[0], lower_target[1] - lift, 0]),
            run_time=0.62,
        )
        self.play(
            upper_card.animate.move_to(upper_target),
            lower_card.animate.move_to(lower_target),
            run_time=0.32,
        )

    def construct(self) -> None:
        heading = label("第 6 題｜同三個數，兩種排列", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 6 頁｜影片 Hypdc2fqjfM",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        card_a = self.value_card("a", BLUE).move_to([2.45, -0.38, 0])
        card_b = self.value_card("b", REGION).move_to([-2.45, -0.38, 0])
        card_neg = self.value_card("-6", CORAL).move_to([0, -0.38, 0])

        # Beat 01: present one set of cards and two promised reorderings.
        self.begin_beat("meet_three_cards")
        beat_title = label("同三張卡，能排成兩種數列？", 35, INK, "BOLD")
        beat_title.move_to([0, 3.08, 0])
        polynomial = MathTex(
            "x^2",
            "-",
            "p",
            "x",
            "+",
            "q",
            "=",
            "0",
            font_size=51,
            color=INK,
        ).move_to([0, 1.62, 0])
        polynomial[2].set_color(POINT)
        polynomial[5].set_color(PURPLE)
        givens = VGroup(
            label("p、q 是正整數", 23, MUTED, "MEDIUM"),
            label("a、b 是方程式的兩個實根", 23, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.9).move_to([0, 0.78, 0])
        two_modes = VGroup(
            label("等差排列", 28, BLUE, "BOLD"),
            MathTex(r"\longleftrightarrow", font_size=37, color=MUTED),
            label("等比排列", 28, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.48).move_to([0, -1.72, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), FadeIn(polynomial), run_time=0.95)
        self.play(FadeIn(givens), FadeIn(card_a), FadeIn(card_b), FadeIn(card_neg), run_time=0.85)
        self.play(FadeIn(two_modes), run_time=0.55)
        self.wait(0.35)

        # Beat 02: prove directly that neither real root can lie at x<=0.
        self.next_beat("force_positive_roots")
        next_title = label("先判斷：兩張根卡會落在哪一側？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        sign_line = Line([-5.8, 0.02, 0], [5.8, 0.02, 0], color=MUTED, stroke_width=3)
        negative_half = Line([-5.8, 0.02, 0], [0, 0.02, 0], color=CORAL, stroke_width=7, stroke_opacity=0.42)
        zero_tick = Line([0, -0.13, 0], [0, 0.17, 0], color=INK, stroke_width=3)
        zero_label = MathTex("0", font_size=27, color=INK).move_to([0, -0.38, 0])
        side_labels = VGroup(
            MathTex(r"x\le0", font_size=31, color=CORAL).move_to([-3.5, -0.4, 0]),
            MathTex(r"x>0", font_size=31, color=REGION).move_to([3.5, -0.4, 0]),
        )
        sign_terms = MathTex(
            "x^2",
            r"\ge0",
            r"\qquad",
            "-px",
            r"\ge0",
            r"\qquad",
            "q",
            ">0",
            font_size=36,
            color=INK,
        ).move_to([0, -1.35, 0])
        sign_terms[3].set_color(POINT)
        sign_terms[6].set_color(PURPLE)
        no_negative_root = MathTex(
            "x^2-px+q",
            ">0",
            r"\Longrightarrow",
            "a,b",
            ">0",
            font_size=40,
            color=INK,
        ).move_to([0, -2.28, 0])
        no_negative_root[3].set_color(BLUE)
        no_negative_root[4].set_color(REGION)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(givens), FadeOut(two_modes), polynomial.animate.scale(0.78).move_to([0, 2.2, 0]), run_time=0.65)
        self.play(Create(sign_line), Create(negative_half), FadeIn(zero_tick), FadeIn(zero_label), FadeIn(side_labels), run_time=0.75)
        self.play(FadeIn(sign_terms), run_time=0.85)

        self.next_beat("exclude_nonpositive_roots")
        self.play(FadeIn(no_negative_root), run_time=0.75)
        self.play(
            card_neg.animate.move_to([-4.5, 0.42, 0]),
            card_a.animate.move_to([2.0, 0.42, 0]),
            card_b.animate.move_to([4.5, 0.42, 0]),
            run_time=1.0,
        )
        self.wait(0.35)

        # Beat 03: test each positive card as the geometric middle term.
        self.next_beat("test_gp_middle")
        next_title = label("等比數列的中項，哪張卡能坐？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        guide = self.guide_row(0.42)
        gp_rule = MathTex("v^2", "=", "uw", font_size=43, color=INK)
        gp_rule[0].set_color(POINT)
        gp_rule.move_to([0, 2.16, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(polynomial),
            FadeOut(sign_line),
            FadeOut(negative_half),
            FadeOut(zero_tick),
            FadeOut(zero_label),
            FadeOut(side_labels),
            FadeOut(sign_terms),
            FadeOut(no_negative_root),
            FadeIn(guide),
            FadeIn(gp_rule),
            card_neg.animate.move_to([self.MAIN_X[0], 0.42, 0]),
            card_a.animate.move_to([self.MAIN_X[1], 0.42, 0]),
            card_b.animate.move_to([self.MAIN_X[2], 0.42, 0]),
            run_time=0.95,
        )
        a_requirement = MathTex("a^2", "=", "(-6)b", font_size=39, color=INK)
        a_requirement[0].set_color(BLUE)
        a_requirement[2].set_color(CORAL)
        a_requirement.move_to([0, -1.28, 0])
        a_signs = MathTex(r"a^2\ge0", r"\qquad", r"(-6)b<0", font_size=31, color=INK)
        a_signs[0].set_color(BLUE)
        a_signs[2].set_color(CORAL)
        a_signs.move_to([0, -1.92, 0])
        self.play(FadeIn(a_requirement), FadeIn(a_signs), run_time=0.75)
        a_cross = Cross(a_requirement, stroke_color=CORAL, stroke_width=5)
        self.play(Create(a_cross), run_time=0.45)
        a_record = VGroup(a_requirement, a_signs, a_cross)
        self.play(a_record.animate.scale(0.68).move_to([-3.35, -1.72, 0]), run_time=0.55)

        self.next_beat("move_b_to_gp_middle")
        self.play(
            card_a.animate.shift(UP * 0.78),
            card_neg.animate.shift(DOWN * 0.78),
            run_time=0.32,
        )
        self.play(
            card_a.animate.move_to([self.MAIN_X[0], 0.42 + 0.78, 0]),
            card_b.animate.move_to([self.MAIN_X[1], 0.42, 0]),
            card_neg.animate.move_to([self.MAIN_X[2], 0.42 - 0.78, 0]),
            run_time=0.72,
        )
        self.play(
            card_a.animate.move_to([self.MAIN_X[0], 0.42, 0]),
            card_neg.animate.move_to([self.MAIN_X[2], 0.42, 0]),
            run_time=0.32,
        )

        self.next_beat("reject_b_as_gp_middle")
        b_requirement = MathTex("b^2", "=", "a(-6)", font_size=39, color=INK)
        b_requirement[0].set_color(REGION)
        b_requirement[2].set_color(CORAL)
        b_requirement.move_to([2.25, -1.46, 0])
        b_signs = MathTex(r"b^2\ge0", r"\qquad", r"a(-6)<0", font_size=31, color=INK)
        b_signs[0].set_color(REGION)
        b_signs[2].set_color(CORAL)
        b_signs.move_to([2.25, -2.08, 0])
        self.play(FadeIn(b_requirement), FadeIn(b_signs), run_time=0.75)
        b_cross = Cross(b_requirement, stroke_color=CORAL, stroke_width=5)
        self.play(Create(b_cross), run_time=0.45)
        self.wait(0.35)

        # Beat 04: the only negative card must be the geometric middle.
        self.next_beat("lock_gp_product")
        next_title = label("只剩負數卡能當等比中項", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        middle_note = label("兩端互換，乘積仍然相同", 23, MUTED, "MEDIUM")
        middle_note.move_to([0, -2.35, 0])
        gp_equation = MathTex("(-6)^2", "=", "ab", font_size=48, color=INK)
        gp_equation[0].set_color(CORAL)
        gp_equation[2].set_color(BLUE)
        gp_equation.move_to([0, -1.18, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(a_record),
            FadeOut(b_requirement),
            FadeOut(b_signs),
            FadeOut(b_cross),
            run_time=0.5,
        )
        self.routed_swap(
            card_b,
            card_neg,
            (self.MAIN_X[2], 0.42, 0),
            (self.MAIN_X[1], 0.42, 0),
        )
        self.play(FadeIn(gp_equation), FadeIn(middle_note), run_time=0.75)
        product_badge = MathTex("ab", "=", "36", font_size=49, color=INK)
        product_badge[0].set_color(BLUE)
        product_badge[2].set_color(REGION)
        product_badge.move_to(gp_equation)
        self.play(Succession(FadeOut(gp_equation), FadeIn(product_badge)), run_time=0.7)
        gp_equation = product_badge
        self.play(Circumscribe(gp_equation, color=POINT), run_time=0.55)
        self.wait(0.35)

        # Beat 05: reorder the same cards on an equal-difference line.
        self.next_beat("reorder_for_ap")
        next_title = label("同三張卡，現在改排成等差", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        ap_y = 0.18
        ap_line = Line([-5.35, ap_y, 0], [5.35, ap_y, 0], color=HAIRLINE, stroke_width=3)
        ap_ticks = VGroup(
            *(
                Line([x_coord, ap_y - 0.14, 0], [x_coord, ap_y + 0.14, 0], color=MUTED, stroke_width=2)
                for x_coord in self.MAIN_X
            )
        )
        order_rule = MathTex("-6", "<", "a", r"\le", "b", font_size=39, color=INK)
        order_rule[0].set_color(CORAL)
        order_rule[2].set_color(BLUE)
        order_rule[4].set_color(REGION)
        order_rule.move_to([-4.35, 2.13, 0])
        product_corner = gp_equation.copy().scale(0.68).move_to([4.65, 2.13, 0])
        gap_left = self.gap_bar(self.MAIN_X[0], self.MAIN_X[1], 1.30, "a+6", BLUE)
        gap_right = self.gap_bar(self.MAIN_X[1], self.MAIN_X[2], 1.30, "b-a", REGION)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(guide),
            FadeOut(gp_rule),
            FadeOut(middle_note),
            Transform(gp_equation, product_corner),
            FadeIn(ap_line),
            FadeIn(ap_ticks),
            FadeIn(order_rule),
            run_time=0.7,
        )
        self.routed_swap(
            card_a,
            card_neg,
            (self.MAIN_X[1], ap_y, 0),
            (self.MAIN_X[0], ap_y, 0),
        )
        self.play(card_b.animate.move_to([self.MAIN_X[2], ap_y, 0]), run_time=0.35)
        self.play(Create(gap_left), Create(gap_right), run_time=0.9)
        self.wait(0.35)

        # Beat 06: turn the two visible equal gaps into one linear relation.
        self.next_beat("earn_ap_relation")
        next_title = label("等差，只是在說兩段距離相等", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        ap_equation = MathTex("a+6", "=", "b-a", font_size=47, color=INK)
        ap_equation[0].set_color(BLUE)
        ap_equation[2].set_color(REGION)
        ap_equation.move_to([0, -1.30, 0])
        linear_relation = MathTex("b", "=", "2a+6", font_size=47, color=INK)
        linear_relation[0].set_color(REGION)
        linear_relation[2].set_color(BLUE)
        linear_relation.move_to([0, -2.18, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeIn(ap_equation),
            run_time=0.85,
        )
        self.play(FadeIn(linear_relation), run_time=0.8)
        self.wait(0.4)

        # Beat 07: combine the two earned relations and keep only the positive root.
        self.next_beat("solve_root_pair")
        next_title = label("兩個條件一起用，根才會定下來", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        substitution = MathTex("a(2a+6)", "=", "36", font_size=44, color=INK)
        substitution[0].set_color(BLUE)
        substitution[2].set_color(REGION)
        substitution.move_to([0, -1.18, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            Succession(
                FadeOut(VGroup(ap_equation, linear_relation)),
                FadeIn(substitution),
            ),
            run_time=0.7,
        )
        quadratic = MathTex("a^2+3a-18", "=", "0", font_size=44, color=INK).move_to(substitution)
        self.play(Succession(FadeOut(substitution), FadeIn(quadratic)), run_time=0.65)
        factorization = MathTex("(a-3)(a+6)", "=", "0", font_size=44, color=INK).move_to(substitution)
        self.play(Succession(FadeOut(quadratic), FadeIn(factorization)), run_time=0.65)

        self.next_beat("choose_positive_root")
        positive_candidate = MathTex("a", "=", "3", font_size=39, color=INK)
        positive_candidate[0].set_color(BLUE)
        positive_candidate[2].set_color(BLUE)
        negative_candidate = MathTex("a", "=", "-6", font_size=39, color=INK)
        negative_candidate[0].set_color(BLUE)
        negative_candidate[2].set_color(CORAL)
        candidates = VGroup(positive_candidate, negative_candidate).arrange(RIGHT, buff=1.25)
        candidates.move_to([0, -2.12, 0])
        self.play(FadeIn(candidates), run_time=0.55)
        rejected = Cross(negative_candidate, stroke_color=CORAL, stroke_width=5)
        self.play(Create(rejected), Indicate(positive_candidate, color=REGION), run_time=0.65)

        self.next_beat("settle_root_pair")
        numeric_left_gap = self.gap_bar(self.MAIN_X[0], self.MAIN_X[1], 1.30, "9", BLUE)
        numeric_right_gap = self.gap_bar(self.MAIN_X[1], self.MAIN_X[2], 1.30, "9", REGION)
        numeric_card_a = self.value_card("3", BLUE).move_to(card_a)
        numeric_card_b = self.value_card("12", REGION).move_to(card_b)
        self.play(
            Succession(FadeOut(card_a[1]), FadeIn(numeric_card_a[1])),
            Succession(FadeOut(card_b[1]), FadeIn(numeric_card_b[1])),
            Succession(FadeOut(gap_left[3]), FadeIn(numeric_left_gap[3])),
            Succession(FadeOut(gap_right[3]), FadeIn(numeric_right_gap[3])),
            run_time=0.9,
        )
        card_a = VGroup(card_a[0], numeric_card_a[1])
        card_b = VGroup(card_b[0], numeric_card_b[1])
        gap_left = VGroup(gap_left[0], gap_left[1], gap_left[2], numeric_left_gap[3])
        gap_right = VGroup(gap_right[0], gap_right[1], gap_right[2], numeric_right_gap[3])
        root_pair = MathTex(r"\{a,b\}", "=", r"\{3,12\}", font_size=39, color=INK)
        root_pair[0].set_color(BLUE)
        root_pair[2].set_color(REGION)
        root_pair.move_to([4.65, -2.15, 0])
        self.play(FadeIn(root_pair), run_time=0.55)
        self.wait(0.4)

        # Beat 08: verify both promised progressions with the settled values.
        self.next_beat("verify_both_progressions")
        next_title = label("把 3、12 放回兩種排列檢查", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        shift_up = UP * 0.38
        ap_tag = label("等差", 25, POINT, "BOLD").move_to([-6.25, 0.56, 0])
        ap_check = MathTex(
            "3-(-6)",
            "=",
            "9",
            "=",
            "12-3",
            font_size=34,
            color=INK,
        ).move_to([0, -0.50, 0])
        ap_check[0].set_color(BLUE)
        ap_check[4].set_color(REGION)

        gp_y = -1.55
        gp_line = Line([-5.35, gp_y, 0], [5.35, gp_y, 0], color=HAIRLINE, stroke_width=3)
        gp_ticks = VGroup(
            *(
                Line([x_coord, gp_y - 0.12, 0], [x_coord, gp_y + 0.12, 0], color=MUTED, stroke_width=2)
                for x_coord in self.MAIN_X
            )
        )
        gp_card_a = self.value_card("3", BLUE, width=1.40, height=0.78, font_size=38).move_to([self.MAIN_X[0], gp_y, 0])
        gp_card_neg = self.value_card("-6", CORAL, width=1.40, height=0.78, font_size=38).move_to([self.MAIN_X[1], gp_y, 0])
        gp_card_b = self.value_card("12", REGION, width=1.40, height=0.78, font_size=38).move_to([self.MAIN_X[2], gp_y, 0])
        gp_tag = label("等比", 25, REGION, "BOLD").move_to([-6.25, gp_y, 0])
        gp_check = MathTex(
            r"\frac{-6}{3}",
            "=",
            "-2",
            "=",
            r"\frac{12}{-6}",
            font_size=34,
            color=INK,
        ).move_to([0, -2.72, 0])
        gp_check[0].set_color(BLUE)
        gp_check[4].set_color(REGION)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(order_rule),
            FadeOut(gp_equation),
            FadeOut(factorization),
            FadeOut(candidates),
            FadeOut(rejected),
            FadeOut(root_pair),
            ap_line.animate.shift(shift_up),
            ap_ticks.animate.shift(shift_up),
            card_neg.animate.shift(shift_up),
            card_a.animate.shift(shift_up),
            card_b.animate.shift(shift_up),
            gap_left.animate.shift(shift_up),
            gap_right.animate.shift(shift_up),
            FadeIn(ap_tag),
            run_time=0.9,
        )
        self.play(FadeIn(gp_line), FadeIn(gp_ticks), FadeIn(gp_tag), run_time=0.5)
        self.play(
            LaggedStart(
                FadeIn(gp_card_a),
                FadeIn(gp_card_neg),
                FadeIn(gp_card_b),
                lag_ratio=0.24,
                run_time=1.2,
            )
        )
        self.play(FadeIn(ap_check), FadeIn(gp_check), run_time=0.8)
        self.wait(0.4)

        # Beat 09: enumerate all six orders after the structure is understood.
        self.next_beat("audit_all_orderings")
        next_title = label("六種順序，一個也不藏起來", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        order_count = MathTex("3!", "=", "6", font_size=39, color=MUTED)
        order_count.move_to([0, 2.28, 0])
        panel_centers = (
            (-4.65, 0.82, 0),
            (0, 0.82, 0),
            (4.65, 0.82, 0),
            (-4.65, -1.50, 0),
            (0, -1.50, 0),
            (4.65, -1.50, 0),
        )
        panels = VGroup(
            *(
                self.permutation_panel(order, center)
                for order, center in zip(ALL_ORDERS, panel_centers, strict=True)
            )
        )
        ap_geometry = VGroup(ap_line, ap_ticks, card_neg, card_a, card_b, gap_left, gap_right)
        gp_geometry = VGroup(gp_line, gp_ticks, gp_card_a, gp_card_neg, gp_card_b)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(ap_geometry),
            FadeOut(gp_geometry),
            FadeOut(ap_tag),
            FadeOut(gp_tag),
            FadeOut(ap_check),
            FadeOut(gp_check),
            FadeIn(order_count),
            run_time=0.65,
        )
        self.play(LaggedStart(*(FadeIn(panel) for panel in panels), lag_ratio=0.12), run_time=1.4)
        self.wait(0.45)

        # Beat 10: only now recover p and q from the settled roots.
        self.next_beat("recover_p_q")
        next_title = label("根已經確定，現在才找回 p、q", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        roots_note = label("方程式的兩個根", 24, MUTED, "MEDIUM")
        roots_note.move_to([-4.55, 2.08, 0])
        neg_note = label("−6 是第三張排列卡", 21, CORAL, "MEDIUM")
        neg_note.move_to([-4.55, -0.25, 0])
        card_a.move_to([-5.55, 1.18, 0])
        card_b.move_to([-3.55, 1.18, 0])
        card_neg.move_to([-4.55, -1.02, 0])

        root_equation = MathTex(
            "x^2",
            "-",
            "p",
            "x",
            "+",
            "q",
            "=",
            "(x-3)(x-12)",
            font_size=42,
            color=INK,
        ).move_to([2.0, 1.43, 0])
        root_equation[2].set_color(POINT)
        root_equation[5].set_color(PURPLE)
        expansion = MathTex(
            "(x-3)(x-12)",
            "=",
            "x^2",
            "-",
            "15x",
            "+",
            "36",
            font_size=42,
            color=INK,
        ).move_to([2.0, 0.30, 0])
        expansion[4].set_color(POINT)
        expansion[6].set_color(PURPLE)
        coefficients = MathTex(
            "p",
            "=",
            "15",
            r"\qquad",
            "q",
            "=",
            "36",
            font_size=44,
            color=INK,
        ).move_to([2.0, -1.05, 0])
        coefficients[0].set_color(POINT)
        coefficients[2].set_color(POINT)
        coefficients[4].set_color(PURPLE)
        coefficients[6].set_color(PURPLE)
        final_sum = MathTex(
            "p+q",
            "=",
            "15+36",
            "=",
            "51",
            font_size=52,
            color=INK,
        ).move_to([2.0, -2.36, 0])
        final_sum[0].set_color(POINT)
        final_sum[-1].set_color(REGION)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(order_count), FadeOut(panels), run_time=0.55)
        self.play(FadeIn(roots_note), FadeIn(neg_note), FadeIn(card_a), FadeIn(card_b), FadeIn(card_neg), run_time=0.7)
        self.play(FadeIn(root_equation), run_time=0.85)
        self.play(FadeIn(expansion), run_time=0.75)

        self.next_beat("read_original_coefficients")
        self.play(FadeIn(coefficients), run_time=0.65)
        self.wait(0.35)

        self.next_beat("reveal_p_q_sum")
        self.play(FadeIn(final_sum), run_time=0.8)
        self.play(Circumscribe(final_sum[-1], color=POINT), run_time=0.65)
        self.wait(0.5)
