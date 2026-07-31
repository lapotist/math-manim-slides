"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q5."""

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
    Circle,
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
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


SCALARS = (1, 2, 3, 4, 5, 6, 7)
WEIGHTS = (1, 2, 4, 8, 16, 32, 64)
TARGET = 113
SELECTED_INDICES = (0, 4, 5, 6)


def expand_sparse_factors() -> tuple[int, ...]:
    """Multiply all seven factors through a coefficient array."""
    coefficients = [1]
    for scalar, weight in zip(SCALARS, WEIGHTS, strict=True):
        expanded = [0] * (len(coefficients) + weight)
        for exponent, coefficient in enumerate(coefficients):
            expanded[exponent] += coefficient
            expanded[exponent + weight] += coefficient * scalar
        coefficients = expanded
    return tuple(coefficients)


def target_subsets() -> tuple[tuple[int, ...], ...]:
    """Return every factor-index subset whose exponent sum is TARGET."""
    matches: list[tuple[int, ...]] = []
    for choices in product((0, 1), repeat=len(WEIGHTS)):
        if sum(choice * weight for choice, weight in zip(choices, WEIGHTS, strict=True)) != TARGET:
            continue
        matches.append(tuple(index for index, choice in enumerate(choices) if choice))
    return tuple(matches)


EXPANDED_COEFFICIENTS = expand_sparse_factors()
TARGET_SUBSETS = target_subsets()

if len(EXPANDED_COEFFICIENTS) != 128:
    raise ValueError("expanded polynomial must have degree 127")
if TARGET_SUBSETS != (SELECTED_INDICES,):
    raise ValueError("x^113 must have exactly one binary factor selection")
if EXPANDED_COEFFICIENTS[TARGET] != 210:
    raise ValueError("programmatic coefficient expansion disagrees with 210")
if EXPANDED_COEFFICIENTS[TARGET] != 1 * 5 * 6 * 7:
    raise ValueError("selected scalar product disagrees with coefficient expansion")


class CarloTcfs113MathQ05(CarloSlide):
    """Discover one sparse coefficient through visible binary choices."""

    lesson_id = "carlo.tcfs_113_math_gifted.q05"

    @staticmethod
    def factor_latex(index: int) -> str:
        scalar = SCALARS[index]
        weight = WEIGHTS[index]
        if index == 0:
            return r"(1+x)"
        return rf"(1+{scalar}x^{{{weight}}})"

    @staticmethod
    def term_latex(index: int) -> str:
        scalar = SCALARS[index]
        weight = WEIGHTS[index]
        if index == 0:
            return "x"
        return rf"{scalar}x^{{{weight}}}"

    @staticmethod
    def option_box(tex: str, color: str) -> VGroup:
        box = Rectangle(
            width=1.50,
            height=0.58,
            stroke_color=color,
            stroke_width=2,
            fill_color=color,
            fill_opacity=0.025,
        )
        glyph = MathTex(tex, font_size=29, color=color).move_to(box)
        return VGroup(box, glyph)

    @classmethod
    def choice_tile(cls, index: int) -> VGroup:
        """Make one stable two-state factor tile."""
        spacer = Rectangle(
            width=1.78,
            height=3.0,
            stroke_opacity=0,
            fill_opacity=0,
        )
        factor = MathTex(cls.factor_latex(index), font_size=28, color=INK)
        factor.move_to([0, 1.12, 0])
        skip = cls.option_box("1", MUTED).move_to([0, 0.25, 0])
        choose = cls.option_box(cls.term_latex(index), POINT).move_to([0, -0.53, 0])
        weight = MathTex(rf"+{WEIGHTS[index]}", font_size=27, color=POINT)
        weight.move_to([0, -1.27, 0])
        return VGroup(spacer, factor, skip, choose, weight)

    @classmethod
    def tile_row(
        cls,
        indices: tuple[int, ...],
        x_positions: tuple[float, ...],
        *,
        y: float = 0.30,
    ) -> VGroup:
        if len(indices) != len(x_positions):
            raise ValueError("tile indices and x positions must have equal length")
        return VGroup(
            *(
                cls.choice_tile(index).move_to([x, y, 0])
                for index, x in zip(indices, x_positions, strict=True)
            )
        )

    @staticmethod
    def selection_marker(tile: VGroup, *, choose: bool) -> SurroundingRectangle:
        target = tile[3] if choose else tile[2]
        return SurroundingRectangle(
            target,
            color=POINT if choose else BLUE,
            buff=0.055,
            stroke_width=3.2,
        ).set_z_index(5)

    @staticmethod
    def weight_chip(value: int, color: str, *, size: float = 0.72) -> VGroup:
        box = Rectangle(
            width=size,
            height=size,
            stroke_color=color,
            stroke_width=2.4,
            fill_color=color,
            fill_opacity=0.08,
        )
        number = MathTex(str(value), font_size=size * 42, color=color).move_to(box)
        return VGroup(box, number)

    @staticmethod
    def coefficient_badge(value: int) -> VGroup:
        circle = Circle(
            radius=0.26,
            stroke_color=REGION,
            stroke_width=3,
            fill_color=REGION,
            fill_opacity=0.10,
        )
        number = MathTex(str(value), font_size=27, color=REGION).move_to(circle)
        return VGroup(circle, number)

    @staticmethod
    def place_column(weight: int, bit: int) -> VGroup:
        weight_label = MathTex(str(weight), font_size=35, color=POINT)
        bit_box = Rectangle(
            width=0.92,
            height=0.78,
            stroke_color=REGION if bit else MUTED,
            stroke_width=2.6,
            fill_color=REGION if bit else MUTED,
            fill_opacity=0.12 if bit else 0.025,
        )
        bit_label = MathTex(
            str(bit),
            font_size=38,
            color=REGION if bit else MUTED,
        ).move_to(bit_box)
        return VGroup(weight_label, VGroup(bit_box, bit_label)).arrange(DOWN, buff=0.19)

    @classmethod
    def factor_strip(cls) -> VGroup:
        items = VGroup()
        for index in range(len(WEIGHTS)):
            items.add(MathTex(cls.factor_latex(index), font_size=31, color=INK))
            if index < len(WEIGHTS) - 1:
                items.add(MathTex(r"\cdot", font_size=28, color=MUTED))
        items.arrange(RIGHT, buff=0.10)
        if items.width > 14.35:
            items.scale_to_fit_width(14.35)
        return items

    def construct(self) -> None:
        heading = label("第 5 題｜哪一條乘積路徑會走到指定次方？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 5 頁｜影片 Hypdc2fqjfM 00:00-01:29",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 meet_product: present the factors without exposing a path.
        self.begin_beat("meet_product")
        beat_title = label("先看七個因式，不急著乘開", 31, INK, "BOLD")
        beat_title.move_to([0, 3.13, 0])
        strip = self.factor_strip().move_to([0, 0.65, 0])
        target_prompt = VGroup(
            label("乘開後，哪一條路會產生", 28, MUTED, "MEDIUM"),
            MathTex(r"x^{113}", font_size=50, color=CORAL),
            label("？", 30, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.28).move_to([0, -1.35, 0])
        avoid_full_expansion = label(
            "先追蹤一次選擇，不展開整個多項式",
            25,
            MUTED,
            "MEDIUM",
        ).move_to([0, -2.35, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), run_time=0.45)
        self.play(
            LaggedStart(*(FadeIn(item, shift=UP * 0.07) for item in strip), lag_ratio=0.08),
            run_time=1.65,
        )
        self.play(FadeIn(target_prompt), FadeIn(avoid_full_expansion), run_time=0.8)
        self.wait(0.4)

        # Beat 02 make_choice_tiles: turn each factor into one binary decision.
        self.next_beat("make_choice_tiles")
        next_title = label("每個因式，都只有選或不選", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        full_x = (-6.38, -4.25, -2.12, 0.0, 2.12, 4.25, 6.38)
        open_tiles = self.tile_row(tuple(range(7)), full_x)
        tile_instruction = label(
            "上格選 1：略過　　下格選含 x 的項：加入權重",
            24,
            MUTED,
            "MEDIUM",
            t2c={"略過": BLUE, "加入權重": POINT},
        ).move_to([0, 2.32, 0])
        exponent_rule = VGroup(
            label("乘積的次方", 25, MUTED, "MEDIUM"),
            MathTex("=", font_size=39, color=INK),
            label("所有選中權重的和", 27, POINT, "BOLD"),
        ).arrange(RIGHT, buff=0.27).move_to([0, -2.22, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(strip),
            FadeOut(target_prompt),
            FadeOut(avoid_full_expansion),
            run_time=0.35,
        )
        self.play(
            FadeIn(next_title),
            LaggedStart(*(FadeIn(tile, shift=UP * 0.08) for tile in open_tiles), lag_ratio=0.10),
            FadeIn(tile_instruction),
            run_time=1.35,
        )
        beat_title = next_title
        self.play(FadeIn(exponent_rule), run_time=0.55)
        self.wait(0.25)

        # Beat 03 try_target_thirteen: make two deliberate choices in a small model.
        self.next_beat("try_target_thirteen")
        next_title = label("先試一個小目標：13", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        small_x = (-3.60, -1.20, 1.20, 3.60)
        small_tiles = self.tile_row((0, 1, 2, 3), small_x)
        small_target = VGroup(
            label("目標次方", 23, MUTED, "MEDIUM"),
            MathTex("13", font_size=49, color=CORAL),
        ).arrange(RIGHT, buff=0.28).move_to([0, 2.28, 0])
        marker_eight = self.selection_marker(small_tiles[3], choose=True)
        marker_four = self.selection_marker(small_tiles[2], choose=True)
        partial_sum = MathTex(r"8+4=12", font_size=50, color=POINT)
        partial_sum.move_to([-1.30, -2.18, 0])
        remainder = VGroup(
            label("還差", 24, MUTED, "MEDIUM"),
            MathTex("1", font_size=43, color=CORAL),
        ).arrange(RIGHT, buff=0.20).move_to([2.02, -2.18, 0])
        two_question = label("權重 2：選，還是略過？", 24, CORAL, "BOLD")
        two_question.move_to([0, -3.02, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(open_tiles),
            FadeOut(tile_instruction),
            FadeOut(exponent_rule),
            run_time=0.35,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(small_tiles),
            FadeIn(small_target),
            run_time=0.60,
        )
        beat_title = next_title

        self.next_beat("build_thirteen_to_twelve")
        self.play(Create(marker_eight), run_time=0.55)
        self.play(Create(marker_four), Write(partial_sum), run_time=0.75)

        self.next_beat("ask_about_weight_two")
        self.play(FadeIn(remainder), FadeIn(two_question), run_time=0.55)
        self.play(Circumscribe(small_tiles[1], color=CORAL), run_time=0.8)
        self.wait(0.25)

        # Beat 04 complete_small_subset: visibly reject overshoot and fill the last unit.
        self.next_beat("complete_small_subset")
        next_title = label("略過 2，再用 1 補到目標", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        marker_skip_two = self.selection_marker(small_tiles[1], choose=False)
        marker_one = self.selection_marker(small_tiles[0], choose=True)
        overshoot = MathTex(r"12+2=14>13", font_size=41, color=CORAL)
        overshoot.move_to([0, -1.82, 0])
        small_result = MathTex(r"8+4+1=13", font_size=52, color=REGION)
        small_result.move_to([0, -2.72, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(partial_sum),
            FadeOut(remainder),
            FadeOut(two_question),
            run_time=0.30,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(overshoot),
            run_time=0.45,
        )
        beat_title = next_title

        self.next_beat("finish_thirteen_subset")
        self.play(Create(marker_skip_two), run_time=0.55)
        self.play(Create(marker_one), run_time=0.55)
        self.play(Write(small_result), run_time=0.75)
        self.wait(0.35)

        # Beat 05 start_target_113: make only the first two large-place decisions.
        self.next_beat("start_target_113")
        next_title = label("回到 113，從最大權重開始", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        target_tiles = self.tile_row(tuple(range(7)), full_x)
        target_label = VGroup(
            label("目標次方", 23, MUTED, "MEDIUM"),
            MathTex("113", font_size=48, color=CORAL),
        ).arrange(RIGHT, buff=0.26).move_to([0, 2.30, 0])
        marker_sixty_four = self.selection_marker(target_tiles[6], choose=True)
        marker_thirty_two = self.selection_marker(target_tiles[5], choose=True)
        first_remainder = MathTex(r"113-64=49", font_size=44, color=POINT)
        first_remainder.move_to([-2.75, -2.25, 0])
        second_remainder = MathTex(r"49-32=17", font_size=44, color=POINT)
        second_remainder.move_to([2.75, -2.25, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(small_tiles),
            FadeOut(small_target),
            FadeOut(marker_eight),
            FadeOut(marker_four),
            FadeOut(marker_skip_two),
            FadeOut(marker_one),
            FadeOut(overshoot),
            FadeOut(small_result),
            run_time=0.38,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(target_tiles),
            FadeIn(target_label),
            run_time=0.62,
        )
        beat_title = next_title

        self.next_beat("choose_largest_target_weights")
        self.play(Create(marker_sixty_four), Write(first_remainder), run_time=0.75)
        self.play(Create(marker_thirty_two), Write(second_remainder), run_time=0.75)
        self.wait(0.25)

        # Beat 06 complete_target_113: settle all remaining switches, but not scalars.
        self.next_beat("complete_target_113")
        next_title = label("剩下 17：選 16，再補 1", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        marker_sixteen = self.selection_marker(target_tiles[4], choose=True)
        skip_markers = VGroup(
            self.selection_marker(target_tiles[3], choose=False),
            self.selection_marker(target_tiles[2], choose=False),
            self.selection_marker(target_tiles[1], choose=False),
        )
        marker_final_one = self.selection_marker(target_tiles[0], choose=True)
        last_remainder = MathTex(r"17-16=1", font_size=41, color=POINT)
        last_remainder.move_to([0, -1.78, 0])
        target_sum = MathTex(
            "64",
            "+",
            "32",
            "+",
            "16",
            "+",
            "1",
            "=",
            "113",
            font_size=50,
            color=REGION,
        )
        target_sum.move_to([0, -2.68, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeIn(next_title),
            FadeOut(first_remainder),
            FadeOut(second_remainder),
            Create(marker_sixteen),
            FadeIn(last_remainder),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(
            LaggedStart(*(Create(marker) for marker in skip_markers), lag_ratio=0.20),
            run_time=0.85,
        )
        self.play(Create(marker_final_one), run_time=0.5)

        self.next_beat("assemble_target_sum")
        self.play(
            TransformFromCopy(VGroup(*target_tiles[6][4][0][1:]), target_sum[0]),
            run_time=0.40,
        )
        self.play(
            Write(target_sum[1]),
            TransformFromCopy(VGroup(*target_tiles[5][4][0][1:]), target_sum[2]),
            run_time=0.40,
        )
        self.play(
            Write(target_sum[3]),
            TransformFromCopy(VGroup(*target_tiles[4][4][0][1:]), target_sum[4]),
            run_time=0.40,
        )

        self.next_beat("finish_target_sum")
        self.play(
            Write(target_sum[5]),
            TransformFromCopy(VGroup(*target_tiles[0][4][0][1:]), target_sum[6]),
            run_time=0.40,
        )
        self.play(
            Write(target_sum[7]),
            Write(target_sum[8]),
            run_time=0.45,
        )
        self.wait(0.25)

        # Beat 07 prove_largest_place: show why all smaller choices cannot replace 64.
        self.next_beat("prove_largest_place")
        next_title = label("較小權重全部加起來，也追不上 64", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        sixty_four_chip = self.weight_chip(64, POINT, size=1.28).move_to([-4.65, 0.45, 0])
        smaller_chips = VGroup(
            *(self.weight_chip(weight, BLUE, size=0.72) for weight in WEIGHTS[:-1])
        ).arrange(RIGHT, buff=0.20).move_to([2.10, 0.83, 0])
        small_bracket_line = Line(
            smaller_chips.get_left() + DOWN * 0.60,
            smaller_chips.get_right() + DOWN * 0.60,
            color=BLUE,
            stroke_width=3,
        )
        small_ticks = VGroup(
            Line(
                small_bracket_line.get_start() + DOWN * 0.10,
                small_bracket_line.get_start() + UP * 0.10,
                color=BLUE,
            ),
            Line(
                small_bracket_line.get_end() + DOWN * 0.10,
                small_bracket_line.get_end() + UP * 0.10,
                color=BLUE,
            ),
        )
        all_smaller_sum = MathTex(
            "1",
            "+",
            "2",
            "+",
            "4",
            "+",
            "8",
            "+",
            "16",
            "+",
            "32",
            "=",
            "63",
            font_size=43,
            color=BLUE,
        ).next_to(small_bracket_line, DOWN, buff=0.24)
        comparison = MathTex(r"63<64", font_size=57, color=CORAL)
        comparison.move_to([0, -1.65, 0])
        forced_note = label(
            "不選 64 時，最大也只有 63",
            26,
            MUTED,
            "MEDIUM",
        ).move_to([0, -2.65, 0])
        proof_visual = VGroup(
            sixty_four_chip,
            smaller_chips,
            small_bracket_line,
            small_ticks,
            all_smaller_sum,
            comparison,
            forced_note,
        )

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(target_tiles),
            FadeOut(target_label),
            FadeOut(marker_sixty_four),
            FadeOut(marker_thirty_two),
            FadeOut(marker_sixteen),
            FadeOut(skip_markers),
            FadeOut(marker_final_one),
            FadeOut(last_remainder),
            FadeOut(target_sum),
            run_time=0.38,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(sixty_four_chip),
            FadeIn(smaller_chips),
            run_time=0.62,
        )
        beat_title = next_title
        self.play(Create(small_bracket_line), Create(small_ticks), run_time=0.55)

        self.next_beat("sum_first_smaller_places")
        self.play(TransformFromCopy(smaller_chips[0][1], all_smaller_sum[0]), run_time=0.28)
        for index in (1, 2):
            self.play(
                Write(all_smaller_sum[2 * index - 1]),
                TransformFromCopy(smaller_chips[index][1], all_smaller_sum[2 * index]),
                run_time=0.28,
            )

        self.next_beat("sum_remaining_smaller_places")
        for index in (3, 4, 5):
            self.play(
                Write(all_smaller_sum[2 * index - 1]),
                TransformFromCopy(smaller_chips[index][1], all_smaller_sum[2 * index]),
                run_time=0.28,
            )
        self.play(Write(all_smaller_sum[11]), Write(all_smaller_sum[12]), run_time=0.38)

        self.next_beat("compare_smaller_sum")
        self.play(Write(comparison), FadeIn(forced_note), run_time=0.7)
        self.wait(0.25)

        # Beat 08 force_binary_digits: repeat the forcing argument down every place.
        self.next_beat("force_binary_digits")
        next_title = label("每一個二進位開關，都被餘數迫使", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        descending_weights = (64, 32, 16, 8, 4, 2, 1)
        forced_bits = (1, 1, 1, 0, 0, 0, 1)
        place_columns = VGroup(
            *(
                self.place_column(weight, bit)
                for weight, bit in zip(descending_weights, forced_bits, strict=True)
            )
        ).arrange(RIGHT, buff=0.55).move_to([0, 1.20, 0])
        place_labels = VGroup(
            label("權重", 18, POINT, "BOLD").move_to([-6.80, 1.55, 0]),
            label("選取", 18, REGION, "BOLD").move_to([-6.80, 0.60, 0]),
        )
        forcing_lines = VGroup(
            MathTex(r"113>63\Rightarrow b_{64}=1,\ r=49", font_size=35, color=INK),
            MathTex(r"49>31\Rightarrow b_{32}=1,\ r=17", font_size=35, color=INK),
            MathTex(r"17>15\Rightarrow b_{16}=1,\ r=1", font_size=35, color=INK),
            MathTex(
                r"r=1\Rightarrow(b_8,b_4,b_2,b_1)=(0,0,0,1)",
                font_size=35,
                color=INK,
            ),
        ).arrange(DOWN, buff=0.20, aligned_edge=LEFT).move_to([0, -1.18, 0])
        for line in forcing_lines:
            line[-1].set_color(REGION)
        binary_result = MathTex(
            "113",
            "=",
            "(",
            "1",
            "1",
            "1",
            "0",
            "0",
            "0",
            "1",
            r")_2",
            font_size=49,
            color=REGION,
        )
        binary_result.move_to([0, -3.05, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(proof_visual),
            run_time=0.35,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(place_labels),
            run_time=0.48,
        )
        beat_title = next_title

        self.next_beat("apply_forcing_digits")
        self.play(
            LaggedStart(*(FadeIn(column, shift=UP * 0.08) for column in place_columns), lag_ratio=0.10),
            run_time=1.05,
        )
        self.play(
            LaggedStart(*(FadeIn(line, shift=RIGHT * 0.08) for line in forcing_lines), lag_ratio=0.18),
            run_time=1.25,
        )
        self.play(
            LaggedStart(
                *(FadeIn(part, shift=UP * 0.04) for part in binary_result),
                lag_ratio=0.08,
            ),
            run_time=0.85,
        )
        self.wait(0.25)

        # Beat 09 collect_multipliers: expose scalar roles only after uniqueness.
        self.next_beat("collect_multipliers")
        next_title = label("路徑唯一後，才拿出四個係數", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        coefficient_tiles = self.tile_row(tuple(range(7)), full_x)
        chosen_markers = VGroup(
            self.selection_marker(coefficient_tiles[0], choose=True),
            self.selection_marker(coefficient_tiles[4], choose=True),
            self.selection_marker(coefficient_tiles[5], choose=True),
            self.selection_marker(coefficient_tiles[6], choose=True),
        )
        omitted_markers = VGroup(
            self.selection_marker(coefficient_tiles[1], choose=False),
            self.selection_marker(coefficient_tiles[2], choose=False),
            self.selection_marker(coefficient_tiles[3], choose=False),
        )
        badge_indices = (0, 4, 5, 6)
        coefficient_badges = VGroup(
            *(
                self.coefficient_badge(SCALARS[index]).move_to(
                    [full_x[index], -1.43, 0]
                )
                for index in badge_indices
            )
        )
        skip_note = label(
            "略過的三欄只貢獻常數 1",
            22,
            MUTED,
            "MEDIUM",
        ).move_to([-2.85, -2.15, 0])
        multiplier_parts = MathTex(
            "1",
            r"\times",
            "5",
            r"\times",
            "6",
            r"\times",
            "7",
            font_size=51,
            color=REGION,
        ).move_to([2.90, -2.25, 0])
        hold_result = label("先保留乘積", 22, CORAL, "BOLD")
        hold_result.next_to(multiplier_parts, DOWN, buff=0.25)

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(place_columns),
            FadeOut(place_labels),
            FadeOut(forcing_lines),
            FadeOut(binary_result),
            run_time=0.38,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(coefficient_tiles),
            FadeIn(chosen_markers),
            FadeIn(omitted_markers),
            run_time=0.62,
        )
        beat_title = next_title

        self.next_beat("collect_selected_scalars")
        self.play(
            LaggedStart(*(GrowFromCenter(badge) for badge in coefficient_badges), lag_ratio=0.18),
            FadeIn(skip_note),
            run_time=0.95,
        )
        self.play(
            TransformFromCopy(coefficient_badges[0][1], multiplier_parts[0]),
            Write(multiplier_parts[1]),
            TransformFromCopy(coefficient_badges[1][1], multiplier_parts[2]),
            Write(multiplier_parts[3]),
            TransformFromCopy(coefficient_badges[2][1], multiplier_parts[4]),
            Write(multiplier_parts[5]),
            TransformFromCopy(coefficient_badges[3][1], multiplier_parts[6]),
            run_time=1.0,
        )
        self.play(FadeIn(hold_result), run_time=0.4)
        self.wait(0.25)

        # Beat 10 reveal_coefficient: combine the unique exponent path and its scalars.
        self.next_beat("reveal_coefficient")
        next_title = label("最後，同時核對次方與純量", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        term_product = MathTex(
            "x",
            r"\cdot",
            r"5x^{16}",
            r"\cdot",
            r"6x^{32}",
            r"\cdot",
            r"7x^{64}",
            font_size=46,
            color=INK,
        ).move_to([0, 1.55, 0])
        separated_product = MathTex(
            r"(1\cdot5\cdot6\cdot7)",
            r"x^{1+16+32+64}",
            font_size=45,
            color=INK,
        ).move_to([0, 0.50, 0])
        separated_product[0].set_color(REGION)
        separated_product[1].set_color(POINT)
        exponent_check = MathTex(r"1+16+32+64=113", font_size=42, color=POINT)
        exponent_check.move_to([0, -0.52, 0])
        scalar_check = MathTex(
            r"1\cdot5\cdot6\cdot7=30\cdot7",
            font_size=42,
            color=REGION,
        ).move_to([0, -1.36, 0])
        final_term = MathTex("210", r"x^{113}", font_size=58, color=INK)
        final_term[0].set_color(REGION)
        final_term[1].set_color(POINT)
        final_term.move_to([0, -2.28, 0])
        answer = VGroup(
            label("所求係數", 25, MUTED, "MEDIUM"),
            MathTex("=210", font_size=48, color=REGION),
        ).arrange(RIGHT, buff=0.25).move_to([0, -3.16, 0])

        self.play(FadeOut(beat_title), run_time=0.22)
        self.play(
            FadeOut(coefficient_tiles),
            FadeOut(chosen_markers),
            FadeOut(omitted_markers),
            FadeOut(coefficient_badges),
            FadeOut(skip_note),
            FadeOut(multiplier_parts),
            FadeOut(hold_result),
            run_time=0.38,
        )
        self.play(
            FadeIn(next_title),
            FadeIn(term_product),
            run_time=0.62,
        )
        beat_title = next_title

        self.next_beat("separate_product_roles")
        self.play(TransformFromCopy(term_product, separated_product), run_time=0.85)
        self.play(FadeIn(exponent_check), run_time=0.55)
        self.play(FadeIn(scalar_check), run_time=0.55)

        self.next_beat("reveal_coefficient_value")
        self.play(FadeIn(final_term), run_time=0.7)
        self.play(FadeIn(answer), Circumscribe(final_term[0], color=REGION), run_time=0.75)
        self.play(Indicate(answer[1], color=REGION), run_time=0.65)
        self.wait(0.60)
