"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q3."""

from __future__ import annotations

from itertools import combinations

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
    PI,
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
    RoundedRectangle,
    Succession,
    Transform,
    Triangle,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


OFFSETS = tuple(range(6))
TRIPLES = tuple(combinations(OFFSETS, 3))


def satisfies_median_condition(triple: tuple[int, int, int]) -> bool:
    """Return whether the middle entry is at least the arithmetic mean."""
    a, b, c = triple
    return 3 * b >= a + b + c


VALID_TRIPLES = tuple(triple for triple in TRIPLES if satisfies_median_condition(triple))
GAP_PAIRS = tuple(
    (left_gap, right_gap, 6 - (left_gap + right_gap))
    for right_gap in range(1, 6)
    for left_gap in range(right_gap, 6)
    if left_gap + right_gap <= 5
)
EXPECTED_GAP_PAIRS = (
    (1, 1, 4),
    (2, 1, 3),
    (3, 1, 2),
    (4, 1, 1),
    (2, 2, 2),
    (3, 2, 1),
)

if len(TRIPLES) != 20:
    raise ValueError(f"expected 20 triples, found {len(TRIPLES)}")
if GAP_PAIRS != EXPECTED_GAP_PAIRS:
    raise ValueError(f"unexpected gap-pair count: {GAP_PAIRS}")
if sum(count for _, _, count in GAP_PAIRS) != 13:
    raise ValueError("gap-pair translation count must total 13")
if len(VALID_TRIPLES) != 13:
    raise ValueError(f"exhaustive check found {len(VALID_TRIPLES)} valid triples")


class CarloTcfs113MathQ03(CarloSlide):
    """Count triples by discovering and translating a two-gap pattern."""

    lesson_id = "carlo.tcfs_113_math_gifted.q03"

    LINE_Y = 0.45
    LINE_LEFT = -5.5
    LINE_STEP = 2.2

    @classmethod
    def point(cls, index: float, *, y: float | None = None):
        return [
            cls.LINE_LEFT + cls.LINE_STEP * index,
            cls.LINE_Y if y is None else y,
            0,
        ]

    @classmethod
    def number_axis(cls) -> VGroup:
        baseline = Line(
            cls.point(0),
            cls.point(5),
            color=MUTED,
            stroke_width=3,
        )
        ticks = VGroup(
            *(
                Line(
                    cls.point(index, y=cls.LINE_Y - 0.13),
                    cls.point(index, y=cls.LINE_Y + 0.13),
                    color=MUTED,
                    stroke_width=2,
                )
                for index in OFFSETS
            )
        )
        anchors = VGroup(
            *(
                Dot(cls.point(index), radius=0.065, color=MUTED)
                for index in OFFSETS
            )
        )
        years = VGroup(
            *(
                MathTex(str(2024 + index), font_size=25, color=MUTED).move_to(
                    cls.point(index, y=cls.LINE_Y - 0.48)
                )
                for index in OFFSETS
            )
        )
        return VGroup(baseline, ticks, anchors, years)

    @classmethod
    def triple_group(cls, triple: tuple[int, int, int]) -> VGroup:
        colors = (BLUE, POINT, CORAL)
        roles = ("a", "b", "c")
        dots = VGroup(
            *(
                Dot(cls.point(index), radius=0.16, color=color).set_z_index(4)
                for index, color in zip(triple, colors, strict=True)
            )
        )
        role_labels = VGroup(
            *(
                MathTex(role, font_size=33, color=color).move_to(
                    cls.point(index, y=cls.LINE_Y + 0.52)
                )
                for index, role, color in zip(triple, roles, colors, strict=True)
            )
        )
        return VGroup(dots, role_labels)

    @classmethod
    def gap_group(cls, triple: tuple[int, int, int]) -> VGroup:
        a, b, c = triple
        gap_y = cls.LINE_Y + 1.05

        def gap_visual(start: int, end: int, color: str) -> VGroup:
            return VGroup(
                Line(cls.point(start, y=gap_y), cls.point(end, y=gap_y), color=color, stroke_width=6),
                Line(
                    cls.point(start, y=gap_y - 0.12),
                    cls.point(start, y=gap_y + 0.12),
                    color=color,
                    stroke_width=3,
                ),
                Line(
                    cls.point(end, y=gap_y - 0.12),
                    cls.point(end, y=gap_y + 0.12),
                    color=color,
                    stroke_width=3,
                ),
            )

        left_visual = gap_visual(a, b, BLUE)
        right_visual = gap_visual(b, c, CORAL)
        left_label = MathTex("L", "=", str(b - a), font_size=31, color=INK)
        left_label[0].set_color(BLUE)
        left_label.move_to(cls.point((a + b) / 2, y=gap_y + 0.43))
        right_label = MathTex("R", "=", str(c - b), font_size=31, color=INK)
        right_label[0].set_color(CORAL)
        right_label.move_to(cls.point((b + c) / 2, y=gap_y + 0.43))
        return VGroup(left_visual, right_visual, left_label, right_label)

    @classmethod
    def mean_group(cls, triple: tuple[int, int, int]) -> VGroup:
        mean_index = sum(triple) / 3
        x_coord = cls.point(mean_index)[0]
        connector = DashedLine(
            [x_coord, cls.LINE_Y - 0.12, 0],
            [x_coord, cls.LINE_Y, 0],
            dash_length=0.04,
            color=PURPLE,
            stroke_width=3,
        )
        marker = (
            Triangle(color=PURPLE, fill_color=PURPLE, fill_opacity=1, stroke_width=0)
            .scale(0.105)
            .rotate(PI)
            .move_to([x_coord, cls.LINE_Y - 0.19, 0])
        )
        mean_label = MathTex(r"\mu", font_size=31, color=PURPLE).move_to(
            [x_coord, cls.LINE_Y - 0.78, 0]
        )
        return VGroup(connector, marker, mean_label)

    @staticmethod
    def relation(symbol: str) -> MathTex:
        result = MathTex("b", symbol, r"\mu", font_size=48, color=INK)
        result[0].set_color(POINT)
        result[2].set_color(PURPLE)
        return result

    @staticmethod
    def pair_panel(
        left_gap: int,
        right_gap: int,
        count: int,
        center: tuple[float, float, float],
    ) -> VGroup:
        pair_tex = MathTex(
            "L",
            "=",
            str(left_gap),
            r"\quad",
            "R",
            "=",
            str(right_gap),
            font_size=28,
            color=INK,
        )
        pair_tex[0].set_color(BLUE)
        pair_tex[4].set_color(CORAL)
        pair_tex.move_to([center[0], center[1] + 0.58, 0])

        mini_left = center[0] - 1.0
        mini_y = center[1]
        mini_step = 0.4
        mini_line = Line(
            [mini_left, mini_y, 0],
            [mini_left + 5 * mini_step, mini_y, 0],
            color=HAIRLINE,
            stroke_width=2,
        )
        mini_dots = VGroup(
            *(
                Dot([mini_left + index * mini_step, mini_y, 0], radius=0.042, color=MUTED)
                for index in OFFSETS
            )
        )
        selected = VGroup(
            Dot([mini_left, mini_y, 0], radius=0.085, color=BLUE),
            Dot([mini_left + left_gap * mini_step, mini_y, 0], radius=0.085, color=POINT),
            Dot(
                [mini_left + (left_gap + right_gap) * mini_step, mini_y, 0],
                radius=0.085,
                color=CORAL,
            ),
        )
        mini = VGroup(mini_line, mini_dots, selected)

        span = left_gap + right_gap
        count_tex = MathTex("6-", str(span), "=", str(count), font_size=31, color=INK)
        count_tex[-1].set_color(REGION)
        count_tex.move_to([center[0], center[1] - 0.58, 0])
        return VGroup(pair_tex, mini, count_tex)

    @staticmethod
    def combination_card(triple: tuple[int, int, int]) -> VGroup:
        valid = satisfies_median_condition(triple)
        status_color = REGION if valid else CORAL
        outline = RoundedRectangle(
            width=2.32,
            height=0.78,
            corner_radius=0.06,
            color=status_color,
            fill_opacity=0,
            stroke_width=1.5,
            stroke_opacity=0.72 if valid else 0.38,
        )
        line_y = 0.14
        left_x = -0.82
        step = 0.328
        baseline = Line(
            [left_x, line_y, 0],
            [left_x + 5 * step, line_y, 0],
            color=HAIRLINE,
            stroke_width=1.4,
        )
        anchors = VGroup(
            *(
                Dot([left_x + index * step, line_y, 0], radius=0.03, color=MUTED)
                for index in OFFSETS
            )
        )
        selected = VGroup(
            *(
                Dot(
                    [left_x + index * step, line_y, 0],
                    radius=0.065,
                    color=status_color,
                )
                for index in triple
            )
        )
        short_values = ",".join(str(2024 + index)[-2:] for index in triple)
        values = MathTex(short_values, font_size=17, color=status_color)
        values.move_to([0, -0.21, 0])
        card = VGroup(outline, baseline, anchors, selected, values)
        if not valid:
            baseline.set_opacity(0.36)
            anchors.set_opacity(0.36)
            selected.set_opacity(0.7)
            values.set_opacity(0.7)
        return card

    @staticmethod
    def replace_title(scene: "CarloTcfs113MathQ03", old, new) -> None:
        scene.play(FadeOut(old), FadeIn(new), run_time=0.55)

    def construct(self) -> None:
        heading = label("第 3 題｜中位數和平均數", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 3 頁｜影片 W-NGUVPlcOc",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: establish the six fixed choices and one concrete triple.
        self.begin_beat("choose_three_points")
        beat_title = label("六個數裡，任選三個不同的數", 35, INK, "BOLD")
        beat_title.move_to([0, 3.08, 0])
        choice_note = label("不計順序；選完後由小到大排好", 25, MUTED, "MEDIUM")
        choice_note.move_to([0, 2.24, 0])
        axis = self.number_axis()
        triple = self.triple_group((0, 3, 5))
        order = MathTex("a", "<", "b", "<", "c", font_size=47, color=INK)
        order[0].set_color(BLUE)
        order[2].set_color(POINT)
        order[4].set_color(CORAL)
        order.move_to([0, -1.42, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), Create(axis[0]), FadeIn(VGroup(*axis[1:])), run_time=1.0)
        self.play(FadeIn(choice_note), FadeIn(triple), FadeIn(order), run_time=0.9)
        self.wait(0.35)

        # Beat 02: preserve the three roles while deliberately moving the values.
        self.next_beat("move_the_median")
        next_title = label("只追蹤排在中間的黃色點 b", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        moving_note = label("兩端跟著改變，b 始終是這一組的中位數", 25, MUTED, "MEDIUM")
        moving_note.move_to([0, -1.42, 0])
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            Succession(FadeOut(VGroup(choice_note, order)), FadeIn(moving_note)),
            run_time=0.55,
        )
        for state in ((1, 3, 4), (0, 2, 5), (0, 1, 4)):
            self.play(Transform(triple, self.triple_group(state)), run_time=0.85)
            self.wait(0.18)

        # Beat 03: reveal both gaps and place the arithmetic mean on the line.
        self.next_beat("locate_the_mean")
        next_title = label("平均數落在 b 的哪一邊？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        gap = self.gap_group((0, 1, 4))
        mean = self.mean_group((0, 1, 4))
        mean_note = label("紫色記號是三個數的算術平均數", 24, MUTED, "MEDIUM")
        mean_note.move_to([0, -1.28, 0])
        numeric_relation = MathTex(
            "b=2025",
            "<",
            r"\mu=2025\frac{2}{3}",
            font_size=41,
            color=INK,
        ).move_to([0, -2.08, 0])
        numeric_relation[0].set_color(POINT)
        numeric_relation[2].set_color(PURPLE)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(moving_note), FadeIn(gap), run_time=0.75)
        self.play(FadeIn(mean), FadeIn(mean_note), run_time=0.65)
        self.play(FadeIn(numeric_relation), run_time=0.7)
        self.wait(0.35)

        # Beat 04: hold the endpoints and move b across equality into validity.
        self.next_beat("cross_the_boundary")
        next_title = label("固定兩端，只把 b 往右移", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        relation = self.relation("=").move_to([0, -1.92, 0])
        boundary_note = label("左右一樣長：剛好落在邊界", 25, POINT, "BOLD")
        boundary_note.move_to([0, -2.62, 0])
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(mean_note), FadeOut(numeric_relation), run_time=0.35)
        self.play(
            Transform(triple, self.triple_group((0, 2, 4))),
            Transform(gap, self.gap_group((0, 2, 4))),
            Transform(mean, self.mean_group((0, 2, 4))),
            FadeIn(relation),
            run_time=1.05,
        )
        self.play(FadeIn(boundary_note), Circumscribe(relation, color=POINT), run_time=0.7)
        self.wait(0.3)

        self.next_beat("cross_into_valid_side")
        valid_relation = self.relation(">").move_to(relation)
        valid_note = label("b 已經在平均數右邊", 25, REGION, "BOLD")
        valid_note.move_to(boundary_note)
        self.play(
            Transform(triple, self.triple_group((0, 3, 4))),
            Transform(gap, self.gap_group((0, 3, 4))),
            Transform(mean, self.mean_group((0, 3, 4))),
            Succession(FadeOut(relation), FadeIn(valid_relation)),
            Succession(FadeOut(boundary_note), FadeIn(valid_note)),
            run_time=1.05,
        )
        relation = valid_relation
        self.wait(0.35)

        # Beat 05: translate the visible left/right relation into the gap rule.
        self.next_beat("earn_gap_rule")
        next_title = label("把位置關係翻成左右距離", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        formula = MathTex(
            "b",
            r"\ge",
            r"\frac{a+b+c}{3}",
            font_size=45,
            color=INK,
        ).move_to([0, -1.72, 0])
        formula[0].set_color(POINT)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(valid_note), FadeOut(relation), FadeIn(formula), run_time=0.75)
        tripled_formula = MathTex("3b", r"\ge", "a+b+c", font_size=45, color=INK)
        tripled_formula.move_to(formula)
        self.play(Succession(FadeOut(formula), FadeIn(tripled_formula)), run_time=0.65)
        formula = tripled_formula
        reduced_formula = MathTex("2b", r"\ge", "a+c", font_size=45, color=INK)
        reduced_formula.move_to(formula)
        self.play(
            Succession(FadeOut(formula), FadeIn(reduced_formula)),
            FadeOut(mean),
            run_time=0.65,
        )
        formula = reduced_formula

        self.next_beat("derive_gap_inequality")
        distance_formula = MathTex("b-a", r"\ge", "c-b", font_size=45, color=INK)
        distance_formula[0].set_color(BLUE)
        distance_formula[2].set_color(CORAL)
        distance_formula.move_to([-1.75, -1.72, 0])
        self.play(Succession(FadeOut(formula), FadeIn(distance_formula)), run_time=0.7)
        formula = distance_formula

        equivalence = MathTex(r"\Longleftrightarrow", font_size=42, color=MUTED)
        equivalence.move_to([0.85, -1.72, 0])
        rule = MathTex("L", r"\ge", "R", font_size=53, color=INK)
        rule[0].set_color(BLUE)
        rule[2].set_color(CORAL)
        rule.move_to([3.25, -1.72, 0])
        self.play(
            FadeIn(equivalence),
            FadeIn(rule),
            run_time=0.85,
        )
        self.wait(0.4)

        # Beat 06: keep one gap pair fixed and count its translations.
        self.next_beat("slide_one_gap_pair")
        next_title = label("同一組間距，可以整組平移幾次？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        compact_rule = rule.copy().scale(0.78).move_to([5.55, 2.35, 0])
        ghost = VGroup(
            *(
                Dot(
                    self.point(index),
                    radius=0.21,
                    color=MUTED,
                    fill_opacity=0,
                    stroke_width=3,
                    stroke_opacity=0.55,
                )
                for index in (0, 3, 4)
            )
        )
        span_formula = MathTex("L+R", "=", "4", font_size=41, color=INK)
        span_formula[0][0].set_color(BLUE)
        span_formula.move_to([0, -1.18, 0])
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(formula),
            FadeOut(equivalence),
            Transform(rule, compact_rule),
            FadeIn(ghost),
            FadeIn(span_formula),
            run_time=0.7,
        )
        self.play(
            Transform(triple, self.triple_group((1, 4, 5))),
            Transform(gap, self.gap_group((1, 4, 5))),
            run_time=1.15,
        )
        translation_count = MathTex(
            "6",
            "-",
            "(L+R)",
            "=",
            "6-4",
            "=",
            "2",
            font_size=43,
            color=INK,
        ).move_to([0, -2.18, 0])
        translation_count[-1].set_color(REGION)
        self.play(FadeIn(VGroup(*translation_count[:-2])), run_time=0.75)
        self.play(FadeIn(VGroup(*translation_count[-2:])), run_time=0.5)
        self.wait(0.4)

        # Beat 07: enumerate the R=1 row only after the translation rule is visible.
        self.next_beat("count_r_one")
        next_title = label("先固定 R=1：L 可以是 1、2、3、4", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        constraint = MathTex(
            "L",
            r"\ge",
            "R",
            r"\qquad",
            "L+R",
            r"\le",
            "5",
            font_size=40,
            color=INK,
        ).move_to([0, 2.15, 0])
        constraint[0].set_color(BLUE)
        constraint[2].set_color(CORAL)
        panels_r1 = VGroup(
            *(
                self.pair_panel(left_gap, right_gap, count, (x, 0.55, 0))
                for (left_gap, right_gap, count), x in zip(
                    GAP_PAIRS[:4], (-5.55, -1.85, 1.85, 5.55), strict=True
                )
            )
        )
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(axis),
            FadeOut(triple),
            FadeOut(gap),
            FadeOut(ghost),
            FadeOut(rule),
            FadeOut(span_formula),
            FadeOut(translation_count),
            FadeIn(constraint),
            run_time=0.7,
        )
        self.play(
            LaggedStart(*(FadeIn(panel) for panel in panels_r1), lag_ratio=0.18),
            run_time=1.35,
        )
        self.wait(0.35)

        # Beat 08: finish R=2 and rule out all R>=3 by the five-step span limit.
        self.next_beat("finish_gap_pairs")
        next_title = label("R=2 還有兩組；R=3 已經放不下", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        panels_r2 = VGroup(
            self.pair_panel(*GAP_PAIRS[4], (-2.35, -1.55, 0)),
            self.pair_panel(*GAP_PAIRS[5], (1.1, -1.55, 0)),
        )
        impossible = MathTex(
            "R",
            r"\ge",
            "3",
            r"\Longrightarrow",
            "L+R",
            r"\ge",
            "6>5",
            font_size=34,
            color=INK,
        ).move_to([5.15, -1.55, 0])
        impossible[0].set_color(CORAL)
        impossible[4].set_color(CORAL)
        impossible[6].set_color(CORAL)
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(panels_r1.animate.set_opacity(0.42), run_time=0.45)
        self.play(FadeIn(panels_r2), run_time=0.8)
        self.play(FadeIn(impossible), run_time=0.75)
        self.wait(0.4)

        # Beat 09: collect exactly the six visible translation contributions.
        self.next_beat("sum_translations")
        next_title = label("六組間距，各自貢獻幾個位置？", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        all_panels = [*panels_r1, *panels_r2]
        summary = MathTex(
            "4",
            "+",
            "3",
            "+",
            "2",
            "+",
            "1",
            "+",
            "2",
            "+",
            "1",
            "=",
            "13",
            font_size=58,
            color=INK,
        ).move_to([0, -0.9, 0])
        term_indices = (0, 2, 4, 6, 8, 10)
        pair_headers = VGroup(
            *(
                MathTex(f"({left_gap},{right_gap})", font_size=27, color=MUTED).move_to(
                    [summary[index].get_x(), 0.38, 0]
                )
                for (left_gap, right_gap, _), index in zip(
                    GAP_PAIRS, term_indices, strict=True
                )
            )
        )
        source_digits = VGroup(*(panel[2][-1] for panel in all_panels))
        panel_shells = VGroup(
            *(
                VGroup(panel[0], panel[1], *panel[2][:-1])
                for panel in all_panels
            )
        )
        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            panels_r1.animate.set_opacity(1),
            FadeOut(constraint),
            FadeOut(impossible),
            run_time=0.45,
        )
        self.play(FadeOut(panel_shells), FadeIn(pair_headers), run_time=0.55)
        self.play(
            LaggedStart(
                *(FadeIn(summary[index]) for index in term_indices),
                lag_ratio=0.18,
                run_time=2.4,
            ),
        )
        plus_signs = VGroup(*(summary[index] for index in (1, 3, 5, 7, 9)))
        self.play(FadeOut(source_digits), FadeIn(plus_signs), run_time=0.8)
        self.wait(0.35)

        self.next_beat("reveal_translation_total")
        self.play(FadeIn(VGroup(summary[11], summary[12])), run_time=0.6)
        self.play(Circumscribe(summary[12], color=POINT), run_time=0.65)
        self.wait(0.4)

        # Beat 10: independently expose all twenty combinations as a final check.
        self.next_beat("check_all_twenty")
        next_title = label("最後，把全部 20 組掃過一次", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        summary_group = VGroup(*summary)
        choose_count = MathTex(r"\binom{6}{3}=20", font_size=39, color=INK)
        choose_count.move_to([-5.55, 2.25, 0])
        cards = VGroup(*(self.combination_card(triple) for triple in TRIPLES))
        card_xs = (-5.6, -2.8, 0, 2.8, 5.6)
        card_ys = (1.18, 0.22, -0.74, -1.70)
        for card, (x_coord, y_coord) in zip(
            cards,
            ((x, y) for y in card_ys for x in card_xs),
            strict=True,
        ):
            card.move_to([x_coord, y_coord, 0])

        status = VGroup(
            label("符合 13 組", 24, REGION, "BOLD"),
            label("不符合 7 組", 21, CORAL, "MEDIUM"),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([5.55, 2.25, 0])
        final_statement = VGroup(
            label("中位數 ≥ 平均數", 27, INK, "BOLD"),
            MathTex(r"\Longleftrightarrow", font_size=35, color=MUTED),
            MathTex("L", r"\ge", "R", font_size=39, color=INK),
            label("答案 13 組", 30, POINT, "BOLD"),
        ).arrange(RIGHT, buff=0.34).move_to([0, -3.02, 0])
        final_statement[2][0].set_color(BLUE)
        final_statement[2][2].set_color(CORAL)

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(pair_headers),
            summary_group.animate.scale(0.72).move_to([0, 2.25, 0]),
            FadeIn(choose_count),
            run_time=0.75,
        )
        self.play(
            LaggedStart(*(FadeIn(card) for card in cards), lag_ratio=0.035),
            run_time=1.7,
        )
        self.play(FadeIn(status), FadeIn(final_statement), run_time=0.8)
        self.play(Indicate(final_statement[-1], color=POINT), run_time=0.75)
        self.wait(0.5)
