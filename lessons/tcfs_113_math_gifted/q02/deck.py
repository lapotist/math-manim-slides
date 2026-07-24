"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q2."""

from __future__ import annotations

from itertools import product

from carlo_manim import (
    BLUE,
    CORAL,
    HAIRLINE,
    INK,
    MUTED,
    POINT,
    REGION,
    CarloSlide,
    label,
)
from manim import (
    Arrow,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, PI, RIGHT, UP


def enumerate_balanced_words() -> dict[int, tuple[str, ...]]:
    """Enumerate all six-bit words with fixed leading 1 by k=a3+a5."""
    cases: dict[int, list[str]] = {0: [], 1: [], 2: []}
    for tail in product((0, 1), repeat=5):
        bits = (1, *tail)
        if sum(bits[0::2]) != sum(bits[1::2]):
            continue
        k = bits[2] + bits[4]
        cases[k].append("".join(str(bit) for bit in bits))
    return {k: tuple(words) for k, words in cases.items()}


BALANCED_WORDS = enumerate_balanced_words()
DISPLAY_WORDS = {
    0: ("110000", "100100", "100001"),
    1: ("111100", "111001", "101101", "110110", "110011", "100111"),
    2: ("111111",),
}

if {k: len(words) for k, words in BALANCED_WORDS.items()} != {0: 3, 1: 6, 2: 1}:
    raise ValueError("balanced-word case counts are incorrect")
if any(set(BALANCED_WORDS[k]) != set(DISPLAY_WORDS[k]) for k in DISPLAY_WORDS):
    raise ValueError("displayed words do not match exhaustive enumeration")
if sum(len(words) for words in BALANCED_WORDS.values()) != 10:
    raise ValueError("balanced-word total is incorrect")


class CarloTcfs113MathQ02(CarloSlide):
    """Count balanced six-bit numbers by making all three cases visible."""

    lesson_id = "carlo.tcfs_113_math_gifted.q02"

    @staticmethod
    def binary_slot(
        index: int,
        value: str,
        color: str,
        *,
        width: float = 1.28,
        height: float = 1.34,
        font_size: float = 42,
    ) -> VGroup:
        """Build one indexed bit slot with stable team coloring."""
        is_one = value == "1"
        box = Rectangle(
            width=width,
            height=height,
            stroke_color=color,
            stroke_width=3.2 if is_one else 2.2,
            fill_color=color,
            fill_opacity=0.13 if is_one else 0.025,
        )
        glyph_size = 30 if value == "0/1" else font_size
        glyph_color = color if is_one else MUTED if value == "0" else INK
        glyph = MathTex(value, font_size=glyph_size, color=glyph_color)
        glyph.move_to(box)
        index_label = MathTex(
            rf"a_{{{index}}}",
            font_size=24,
            color=color,
        ).next_to(box, DOWN, buff=0.12)
        return VGroup(box, glyph, index_label)

    @classmethod
    def linear_slots(cls, values: tuple[str, ...], *, y: float = 0.65) -> VGroup:
        slots = VGroup(
            *(
                cls.binary_slot(
                    index,
                    value,
                    POINT if index % 2 else BLUE,
                    width=1.38,
                    height=1.48,
                    font_size=46,
                )
                for index, value in enumerate(values, start=1)
            )
        )
        slots.arrange(RIGHT, buff=0.43).move_to([0, y, 0])
        return slots

    @classmethod
    def team_slots(cls, values: tuple[str, ...]) -> VGroup:
        odd = VGroup(
            *(cls.binary_slot(index, values[index - 1], POINT) for index in (1, 3, 5))
        ).arrange(RIGHT, buff=0.34).move_to([-3.82, 0.85, 0])
        even = VGroup(
            *(cls.binary_slot(index, values[index - 1], BLUE) for index in (2, 4, 6))
        ).arrange(RIGHT, buff=0.34).move_to([3.82, 0.85, 0])
        equals = MathTex("=", font_size=55, color=INK).move_to([0, 0.95, 0])
        return VGroup(odd, even, equals)

    @staticmethod
    def team_titles() -> VGroup:
        return VGroup(
            label("奇數位置", 25, POINT, "BOLD").move_to([-3.82, 2.23, 0]),
            label("偶數位置", 25, BLUE, "BOLD").move_to([3.82, 2.23, 0]),
        )

    @staticmethod
    def bit_pattern(bits: tuple[int | str, ...], color: str, *, cell: float = 0.42) -> VGroup:
        """Build a compact, unindexed bit pattern for a set of choices."""
        cells = VGroup()
        for bit in bits:
            text = str(bit)
            is_one = text == "1"
            box = Rectangle(
                width=cell,
                height=cell * 1.14,
                stroke_color=color,
                stroke_width=1.8,
                fill_color=color,
                fill_opacity=0.15 if is_one else 0.02,
            )
            glyph = MathTex(
                text,
                font_size=cell * 53,
                color=color if is_one else MUTED if text == "0" else INK,
            ).move_to(box)
            cells.add(VGroup(box, glyph))
        cells.arrange(RIGHT, buff=cell * 0.14)
        return cells

    @classmethod
    def mini_word(cls, word: str, *, cell: float = 0.43) -> VGroup:
        """Render one full six-bit word while preserving odd/even colors."""
        cells = VGroup()
        for index, character in enumerate(word, start=1):
            color = POINT if index % 2 else BLUE
            box = Rectangle(
                width=cell,
                height=cell * 1.18,
                stroke_color=color,
                stroke_width=1.7,
                fill_color=color,
                fill_opacity=0.14 if character == "1" else 0.015,
            )
            glyph = MathTex(
                character,
                font_size=cell * 54,
                color=color if character == "1" else MUTED,
            ).move_to(box)
            cells.add(VGroup(box, glyph))
        cells.arrange(RIGHT, buff=cell * 0.13)
        return cells

    @classmethod
    def choice_set(
        cls,
        patterns: tuple[tuple[int, ...], ...],
        color: str,
    ) -> VGroup:
        return VGroup(*(cls.bit_pattern(pattern, color) for pattern in patterns)).arrange(
            RIGHT, buff=0.18
        )

    @classmethod
    def case_summary(
        cls,
        k: int,
        odd_patterns: tuple[tuple[int, ...], ...],
        even_patterns: tuple[tuple[int, ...], ...],
        count_tex: str,
        x: float,
    ) -> VGroup:
        head = MathTex(rf"k={k}", font_size=42, color=REGION)
        odd_label = label("左隊剩下兩格", 18, POINT, "BOLD")
        odd_choices = cls.choice_set(odd_patterns, POINT)
        even_label = label("右隊三格", 18, BLUE, "BOLD")
        even_choices = cls.choice_set(even_patterns, BLUE)
        count = MathTex(count_tex, font_size=43, color=REGION)
        column = VGroup(
            head,
            odd_label,
            odd_choices,
            even_label,
            even_choices,
            count,
        ).arrange(DOWN, buff=0.20)
        column.move_to([x, -0.02, 0])
        return column

    def construct(self) -> None:
        heading = label("第 2 題｜六個數位怎麼保持平衡？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 2 頁｜影片 FSGAuRvRFU0 00:51-02:29",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 meet_six_slots: establish six places before showing the balance.
        self.begin_beat("meet_six_slots")
        beat_title = label("先把六個數位排出來", 31, INK, "BOLD")
        beat_title.move_to([0, 3.13, 0])
        linear = self.linear_slots(("1", "0/1", "0/1", "0/1", "0/1", "0/1"))
        fixed = VGroup(
            MathTex(r"a_1=1", font_size=42, color=POINT),
            MathTex(r"a_2,\ldots,a_6\in\{0,1\}", font_size=40, color=BLUE),
        ).arrange(RIGHT, buff=1.15).move_to([0, -1.50, 0])
        opening_prompt = label(
            "先看位置，暫時不要計數",
            26,
            MUTED,
            "MEDIUM",
        ).move_to([0, -2.50, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), run_time=0.45)
        self.play(
            LaggedStart(*(GrowFromCenter(slot) for slot in linear), lag_ratio=0.10),
            run_time=1.45,
        )
        self.play(FadeIn(fixed), FadeIn(opening_prompt), run_time=0.75)
        self.wait(0.45)

        # Beat 02 separate_teams: preserve each slot while sorting alternating positions.
        self.next_beat("separate_teams")
        next_title = label("把交錯的位置拆成兩隊", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        target_teams = self.team_slots(("1", "0/1", "0/1", "0/1", "0/1", "0/1"))
        team_titles = self.team_titles()
        balance = MathTex(
            r"a_1+a_3+a_5",
            "=",
            r"a_2+a_4+a_6",
            font_size=48,
            color=INK,
        ).move_to([0, -1.18, 0])
        balance[0].set_color(POINT)
        balance[2].set_color(BLUE)
        balance_note = label(
            "兩隊的 1 要一樣多",
            28,
            REGION,
            "BOLD",
        ).move_to([0, -2.28, 0])

        target_positions = {
            0: target_teams[0][0].get_center(),
            2: target_teams[0][1].get_center(),
            4: target_teams[0][2].get_center(),
            1: target_teams[1][0].get_center(),
            3: target_teams[1][1].get_center(),
            5: target_teams[1][2].get_center(),
        }
        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(fixed),
            FadeOut(opening_prompt),
            linear[0].animate.move_to(target_positions[0]),
            linear[1].animate(path_arc=-PI / 2).move_to(target_positions[1]),
            linear[2].animate.move_to(target_positions[2]),
            linear[3].animate.move_to(target_positions[3]),
            linear[4].animate(path_arc=PI / 2).move_to(target_positions[4]),
            linear[5].animate.move_to(target_positions[5]),
            run_time=1.35,
        )
        beat_title = next_title
        teams = VGroup(
            VGroup(linear[0], linear[2], linear[4]),
            VGroup(linear[1], linear[3], linear[5]),
            target_teams[2],
        )
        self.remove(linear)
        self.add(teams)
        self.play(FadeIn(team_titles), Write(balance), run_time=0.9)
        self.play(FadeIn(balance_note), run_time=0.5)
        self.wait(0.35)

        # Beat 03 name_balance_cases: isolate the only free count on the odd team.
        self.next_beat("name_balance_cases")
        next_title = label("左隊已經先有一個 1", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        k_definition = VGroup(
            MathTex(r"k=a_3+a_5", font_size=47, color=POINT),
            label("剩下兩格中的 1 數", 22, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.18).move_to([-3.82, -1.28, 0])
        right_need = VGroup(
            label("右隊需要", 22, MUTED, "MEDIUM"),
            MathTex(r"1+k", font_size=47, color=BLUE),
            label("個 1", 22, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.22).move_to([3.82, -1.28, 0])
        case_markers = VGroup(
            MathTex("k=0", font_size=39, color=REGION),
            MathTex("k=1", font_size=39, color=REGION),
            MathTex("k=2", font_size=39, color=REGION),
        ).arrange(RIGHT, buff=1.35).move_to([0, -2.52, 0])
        marker_lines = VGroup(
            *(
                Line(
                    marker.get_left() + DOWN * 0.16,
                    marker.get_right() + DOWN * 0.16,
                    color=REGION,
                    stroke_width=3,
                )
                for marker in case_markers
            )
        )
        case_prompt = label("三種情況，一種一種數", 23, MUTED, "MEDIUM")
        case_prompt.move_to([0, -3.25, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(balance),
            FadeOut(balance_note),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(Circumscribe(teams[0][0], color=POINT), run_time=0.9)
        self.play(FadeIn(k_definition), FadeIn(right_need), run_time=0.8)
        self.play(
            LaggedStart(
                *(FadeIn(marker, shift=UP * 0.08) for marker in case_markers),
                lag_ratio=0.23,
            ),
            Create(marker_lines),
            run_time=1.1,
        )
        self.play(FadeIn(case_prompt), run_time=0.4)

        # Beat 04 own_case_zero: move the even-team 1 through all three positions.
        self.next_beat("own_case_zero")
        next_title = label("情況一｜k = 0", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        case_zero_teams = self.team_slots(("1", "?", "0", "?", "0", "?"))
        case_zero_math = VGroup(
            MathTex(r"1+0+0=1", font_size=40, color=POINT).move_to(
                [-3.82, -0.72, 0]
            ),
            MathTex(r"a_2+a_4+a_6=1", font_size=40, color=BLUE).move_to(
                [3.82, -0.72, 0]
            ),
        )
        case_zero_words = VGroup(
            *(self.mini_word(word, cell=0.46) for word in DISPLAY_WORDS[0])
        ).arrange(RIGHT, buff=0.85).move_to([0, -2.05, 0])
        case_zero_count = VGroup(
            label("右隊的 1 有三個位置可放", 23, MUTED, "MEDIUM"),
            label("3 種", 36, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.48).move_to([0, -3.05, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            ReplacementTransform(teams, case_zero_teams),
            FadeOut(k_definition),
            FadeOut(right_need),
            FadeOut(case_markers),
            FadeOut(marker_lines),
            FadeOut(case_prompt),
            run_time=0.9,
        )
        beat_title = next_title
        teams = case_zero_teams
        self.play(FadeIn(case_zero_math), run_time=0.6)
        self.play(
            LaggedStart(
                *(FadeIn(word, shift=UP * 0.10) for word in case_zero_words),
                lag_ratio=0.28,
            ),
            run_time=1.35,
        )
        self.play(FadeIn(case_zero_count), run_time=0.55)

        # Beat 05 open_case_one: own the two odd-team choices before multiplying.
        self.next_beat("open_case_one")
        next_title = label("情況二｜k = 1，先選左隊", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        case_one_teams = self.team_slots(("1", "?", "?", "?", "?", "?"))
        case_one_math = VGroup(
            MathTex(r"a_3+a_5=1", font_size=41, color=POINT).move_to(
                [-3.82, -0.65, 0]
            ),
            MathTex(r"a_2+a_4+a_6=2", font_size=41, color=BLUE).move_to(
                [3.82, -0.65, 0]
            ),
        )
        pair_choices = VGroup(
            self.bit_pattern((1, 0), POINT, cell=0.58),
            self.bit_pattern((0, 1), POINT, cell=0.58),
        ).arrange(RIGHT, buff=1.05).move_to([-2.10, -1.66, 0])
        pair_caption = MathTex(r"(a_3,a_5)", font_size=31, color=POINT)
        pair_caption.next_to(pair_choices, UP, buff=0.18)
        case_one_prompt = label(
            "右隊三格放兩個 1，有幾種？",
            25,
            CORAL,
            "BOLD",
        ).move_to([3.20, -1.67, 0])
        partial_product = MathTex(r"2\times ?", font_size=48, color=CORAL)
        partial_product.move_to([0, -2.92, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            ReplacementTransform(teams, case_one_teams),
            FadeOut(case_zero_math),
            FadeOut(case_zero_words),
            FadeOut(case_zero_count),
            run_time=0.85,
        )
        beat_title = next_title
        teams = case_one_teams
        self.play(FadeIn(case_one_math), run_time=0.55)
        self.play(
            FadeIn(pair_caption),
            LaggedStart(*(GrowFromCenter(choice) for choice in pair_choices), lag_ratio=0.28),
            run_time=0.95,
        )
        self.play(FadeIn(case_one_prompt), Write(partial_product), run_time=0.7)

        # Beat 06 own_case_one: display the complete two-by-three Cartesian product.
        self.next_beat("own_case_one")
        next_title = label("k = 1｜兩種左隊，各配三種右隊", 30, INK, "BOLD")
        next_title.move_to(beat_title)
        x_positions = (-3.65, 0.0, 3.65)
        y_positions = (0.55, -1.05)
        case_one_words = VGroup()
        for row, y in enumerate(y_positions):
            for column, x in enumerate(x_positions):
                word = DISPLAY_WORDS[1][row * 3 + column]
                case_one_words.add(self.mini_word(word, cell=0.45).move_to([x, y, 0]))
        even_headers = VGroup(
            self.bit_pattern((1, 1, 0), BLUE, cell=0.36).move_to(
                [x_positions[0], 1.58, 0]
            ),
            self.bit_pattern((1, 0, 1), BLUE, cell=0.36).move_to(
                [x_positions[1], 1.58, 0]
            ),
            self.bit_pattern((0, 1, 1), BLUE, cell=0.36).move_to(
                [x_positions[2], 1.58, 0]
            ),
        )
        odd_headers = VGroup(
            self.bit_pattern((1, 0), POINT, cell=0.38).move_to([-6.05, y_positions[0], 0]),
            self.bit_pattern((0, 1), POINT, cell=0.38).move_to([-6.05, y_positions[1], 0]),
        )
        axis_labels = VGroup(
            label("右隊三種", 19, BLUE, "BOLD").move_to([0, 2.18, 0]),
            label("左隊兩種", 19, POINT, "BOLD").rotate(1.5708).move_to(
                [-6.80, -0.25, 0]
            ),
        )
        product_result = VGroup(
            MathTex(r"2\times3=6", font_size=53, color=REGION),
            label("六個完整字串", 22, MUTED, "MEDIUM"),
        ).arrange(RIGHT, buff=0.42).move_to([0, -2.55, 0])
        case_one_grid = VGroup(
            case_one_words,
            even_headers,
            odd_headers,
            axis_labels,
        )

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(teams),
            FadeOut(team_titles),
            FadeOut(case_one_math),
            FadeOut(pair_choices),
            FadeOut(pair_caption),
            FadeOut(case_one_prompt),
            FadeOut(partial_product),
            run_time=0.7,
        )
        beat_title = next_title
        self.play(FadeIn(axis_labels), FadeIn(even_headers), FadeIn(odd_headers), run_time=0.7)
        self.play(
            LaggedStart(
                *(FadeIn(word, shift=UP * 0.08) for word in case_one_words),
                lag_ratio=0.12,
            ),
            run_time=1.55,
        )
        self.play(FadeIn(product_result), run_time=0.55)

        # Beat 07 own_case_two: test the opposite extreme where every slot is forced.
        self.next_beat("own_case_two")
        next_title = label("情況三｜k = 2", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        case_two_teams = self.team_slots(("1", "1", "1", "1", "1", "1"))
        case_two_math = VGroup(
            MathTex(r"1+1+1=3", font_size=43, color=POINT).move_to(
                [-3.82, -0.72, 0]
            ),
            MathTex(r"1+1+1=3", font_size=43, color=BLUE).move_to(
                [3.82, -0.72, 0]
            ),
        )
        unique_word = self.mini_word(DISPLAY_WORDS[2][0], cell=0.54)
        unique_word.move_to([0, -1.90, 0])
        unique_count = VGroup(
            label("每一格都被決定", 23, MUTED, "MEDIUM"),
            label("只有 1 種", 34, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.42).move_to([0, -2.88, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(case_one_grid),
            FadeOut(product_result),
            FadeIn(team_titles),
            FadeIn(case_two_teams),
            run_time=0.85,
        )
        beat_title = next_title
        teams = case_two_teams
        self.play(FadeIn(case_two_math), run_time=0.55)
        self.play(GrowFromCenter(unique_word), run_time=0.65)
        self.play(FadeIn(unique_count), run_time=0.5)

        # Beat 08 compare_three_cases: retain every local choice while withholding total.
        self.next_beat("compare_three_cases")
        next_title = label("三個案例，都已經數完了", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        summary_zero = self.case_summary(
            0,
            ((0, 0),),
            ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            r"1\times3=3",
            -5.05,
        )
        summary_one = self.case_summary(
            1,
            ((1, 0), (0, 1)),
            ((1, 1, 0), (1, 0, 1), (0, 1, 1)),
            r"2\times3=6",
            0,
        )
        summary_two = self.case_summary(
            2,
            ((1, 1),),
            ((1, 1, 1),),
            r"1\times1=1",
            5.05,
        )
        summaries = VGroup(summary_zero, summary_one, summary_two)
        separators = VGroup(
            Line([-2.52, -2.42, 0], [-2.52, 2.25, 0], color=HAIRLINE),
            Line([2.52, -2.42, 0], [2.52, 2.25, 0], color=HAIRLINE),
        )
        total_question = MathTex(r"3+6+1=?", font_size=50, color=CORAL)
        total_question.move_to([0, -3.08, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(teams),
            FadeOut(team_titles),
            FadeOut(case_two_math),
            FadeOut(unique_word),
            FadeOut(unique_count),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(
            FadeIn(separators),
            LaggedStart(
                *(FadeIn(summary, shift=UP * 0.10) for summary in summaries),
                lag_ratio=0.20,
            ),
            run_time=1.35,
        )
        self.play(Write(total_question), run_time=0.65)

        # Beat 09 compress_with_binomials: name the choices only after seeing them.
        self.next_beat("compress_with_binomials")
        next_title = label("現在才把選法壓成組合數", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        odd_selector = VGroup(
            label("左隊：2 格中選 k 格", 23, POINT, "BOLD"),
            self.bit_pattern(("?", "?"), POINT, cell=0.60),
            MathTex(r"\binom{2}{k}", font_size=54, color=POINT),
        ).arrange(DOWN, buff=0.24).move_to([-3.55, 1.10, 0])
        even_selector = VGroup(
            label("右隊：3 格中選 1+k 格", 23, BLUE, "BOLD"),
            self.bit_pattern(("?", "?", "?"), BLUE, cell=0.60),
            MathTex(r"\binom{3}{1+k}", font_size=54, color=BLUE),
        ).arrange(DOWN, buff=0.24).move_to([3.55, 1.10, 0])
        selector_times = MathTex(r"\times", font_size=48, color=INK).move_to([0, 0.54, 0])
        formula_cases = VGroup(
            MathTex(r"\binom20\binom31=3", font_size=42, color=REGION).move_to(
                [-4.70, -1.55, 0]
            ),
            MathTex(r"\binom21\binom32=6", font_size=42, color=REGION).move_to(
                [0, -1.55, 0]
            ),
            MathTex(r"\binom22\binom33=1", font_size=42, color=REGION).move_to(
                [4.70, -1.55, 0]
            ),
        )
        formula_labels = VGroup(
            MathTex("k=0", font_size=31, color=MUTED).next_to(
                formula_cases[0], UP, buff=0.18
            ),
            MathTex("k=1", font_size=31, color=MUTED).next_to(
                formula_cases[1], UP, buff=0.18
            ),
            MathTex("k=2", font_size=31, color=MUTED).next_to(
                formula_cases[2], UP, buff=0.18
            ),
        )
        formula_question = MathTex(r"3+6+1=?", font_size=50, color=CORAL)
        formula_question.move_to([0, -2.80, 0])
        compression = VGroup(
            odd_selector,
            even_selector,
            selector_times,
            formula_cases,
            formula_labels,
            formula_question,
        )

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(summaries),
            FadeOut(separators),
            FadeOut(total_question),
            run_time=0.7,
        )
        beat_title = next_title
        self.play(FadeIn(odd_selector), run_time=0.65)
        self.play(FadeIn(even_selector), FadeIn(selector_times), run_time=0.65)
        self.play(
            LaggedStart(
                *(
                    FadeIn(VGroup(formula_labels[index], formula_cases[index]), shift=UP * 0.08)
                    for index in range(3)
                ),
                lag_ratio=0.25,
            ),
            run_time=1.25,
        )
        self.play(Write(formula_question), run_time=0.55)

        # Beat 10 reveal_total: reunite the original slots, then add disjoint cases.
        self.next_beat("reveal_total")
        next_title = label("三種情況合起來，沒有重複", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        final_slots = self.linear_slots(("1", "0/1", "0/1", "0/1", "0/1", "0/1"), y=1.45)
        final_balance = MathTex(
            r"a_1+a_3+a_5",
            "=",
            r"a_2+a_4+a_6",
            font_size=42,
            color=INK,
        ).move_to([0, -0.02, 0])
        final_balance[0].set_color(POINT)
        final_balance[2].set_color(BLUE)
        case_counts = VGroup(
            VGroup(
                MathTex("k=0", font_size=29, color=MUTED),
                MathTex("3", font_size=45, color=REGION),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                MathTex("k=1", font_size=29, color=MUTED),
                MathTex("6", font_size=45, color=REGION),
            ).arrange(DOWN, buff=0.12),
            VGroup(
                MathTex("k=2", font_size=29, color=MUTED),
                MathTex("1", font_size=45, color=REGION),
            ).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=1.55).move_to([0, -1.12, 0])
        completeness = label(
            "每個合法六位數恰好落在一種 k",
            24,
            MUTED,
            "MEDIUM",
        ).move_to([0, -2.08, 0])
        final_sum = MathTex("3", "+", "6", "+", "1", "=", "10", font_size=61, color=INK)
        final_sum.move_to([0, -2.88, 0])
        for index in (0, 2, 4):
            final_sum[index].set_color(REGION)
        final_sum[6].set_color(POINT)
        answer_box = SurroundingRectangle(
            final_sum[6],
            color=POINT,
            buff=0.15,
            stroke_width=3,
        )

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(compression),
            run_time=0.65,
        )
        beat_title = next_title
        self.play(FadeIn(final_slots), FadeIn(final_balance), run_time=0.9)
        self.play(
            LaggedStart(*(FadeIn(case, shift=UP * 0.08) for case in case_counts), lag_ratio=0.2),
            run_time=0.8,
        )
        self.play(FadeIn(completeness), run_time=0.45)
        self.play(
            TransformFromCopy(case_counts[0][1], final_sum[0]),
            Write(final_sum[1]),
            TransformFromCopy(case_counts[1][1], final_sum[2]),
            Write(final_sum[3]),
            TransformFromCopy(case_counts[2][1], final_sum[4]),
            Write(final_sum[5]),
            run_time=1.0,
        )
        self.play(FadeIn(final_sum[6]), Create(answer_box), run_time=0.7)
        self.play(Indicate(final_sum[6], color=POINT), run_time=0.7)
        self.wait(0.65)
