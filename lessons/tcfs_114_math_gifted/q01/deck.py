"""Manim Slides lesson for TCFS 114 mathematics gifted assessment Q1."""

from __future__ import annotations

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
    Arrow,
    Circumscribe,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    Rectangle,
    ReplacementTransform,
    Square,
    SurroundingRectangle,
    TransformFromCopy,
    VGroup,
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


GRID_SIZE = 12
CELL_SIZE = 0.43
GRID_LEFT = -7.08
GRID_TOP = 2.58


def enumerate_antidiagonals(size: int) -> dict[tuple[int, int], int]:
    """Fill a square by rising anti-diagonals, from lower-left to upper-right."""
    values: dict[tuple[int, int], int] = {}
    current = 1
    for coordinate_sum in range(2, 2 * size + 1):
        first_row = min(size, coordinate_sum - 1)
        last_row = max(1, coordinate_sum - size)
        for row in range(first_row, last_row - 1, -1):
            column = coordinate_sum - row
            values[(row, column)] = current
            current += 1
    return values


GRID_VALUES = enumerate_antidiagonals(GRID_SIZE)
VALUE_COORDS = {value: coordinate for coordinate, value in GRID_VALUES.items()}

if len(GRID_VALUES) != GRID_SIZE**2:
    raise ValueError("anti-diagonal enumeration did not fill the 12x12 grid")
if set(GRID_VALUES.values()) != set(range(1, GRID_SIZE**2 + 1)):
    raise ValueError("anti-diagonal enumeration is not a permutation of 1..144")
for coordinate, expected in {
    (1, 1): 1,
    (1, 4): 10,
    (12, 10): 139,
    (11, 11): 140,
    (10, 12): 141,
    (12, 11): 142,
    (11, 12): 143,
    (12, 12): 144,
    (8, 8): 104,
}.items():
    if GRID_VALUES[coordinate] != expected:
        raise ValueError(f"unexpected value at {coordinate}")


class CarloTcfs114MathQ01(CarloSlide):
    """Discover the anti-diagonal invariant, then locate 104 by counting."""

    lesson_id = "carlo.tcfs_114_math_gifted.q01"

    @staticmethod
    def cell_center(row: int, column: int):
        return (
            RIGHT * (GRID_LEFT + (column - 0.5) * CELL_SIZE)
            + UP * (GRID_TOP - (row - 0.5) * CELL_SIZE)
        )

    @classmethod
    def diagonal_coordinates(cls, coordinate_sum: int) -> list[tuple[int, int]]:
        first_row = min(GRID_SIZE, coordinate_sum - 1)
        last_row = max(1, coordinate_sum - GRID_SIZE)
        return [
            (row, coordinate_sum - row)
            for row in range(first_row, last_row - 1, -1)
        ]

    @classmethod
    def diagonal_cells(
        cls,
        coordinate_sum: int,
        color: str,
        opacity: float,
    ) -> VGroup:
        cells = VGroup()
        for row, column in cls.diagonal_coordinates(coordinate_sum):
            cell = Square(
                side_length=CELL_SIZE * 0.91,
                stroke_width=0,
                fill_color=color,
                fill_opacity=opacity,
            ).move_to(cls.cell_center(row, column))
            cell.set_z_index(-2)
            cells.add(cell)
        return cells

    @classmethod
    def diagonal_arrow(cls, coordinate_sum: int, color: str) -> Arrow:
        coordinates = cls.diagonal_coordinates(coordinate_sum)
        return Arrow(
            cls.cell_center(*coordinates[0]),
            cls.cell_center(*coordinates[-1]),
            buff=0.12,
            color=color,
            stroke_width=3,
            tip_length=0.14,
        ).set_z_index(3)

    @classmethod
    def grid_art(cls) -> tuple[VGroup, VGroup, VGroup, list, list]:
        grid_right = GRID_LEFT + GRID_SIZE * CELL_SIZE
        grid_bottom = GRID_TOP - GRID_SIZE * CELL_SIZE
        lines = VGroup()
        for index in range(GRID_SIZE + 1):
            y = GRID_TOP - index * CELL_SIZE
            outer = index in {0, GRID_SIZE}
            lines.add(
                Line(
                    RIGHT * GRID_LEFT + UP * y,
                    RIGHT * grid_right + UP * y,
                    color=MUTED if outer else HAIRLINE,
                    stroke_width=2.8 if outer else 1.35,
                )
            )
            x = GRID_LEFT + index * CELL_SIZE
            lines.add(
                Line(
                    RIGHT * x + UP * GRID_TOP,
                    RIGHT * x + UP * grid_bottom,
                    color=MUTED if outer else HAIRLINE,
                    stroke_width=2.8 if outer else 1.35,
                )
            )

        column_ticks = []
        row_ticks = []
        for index in range(1, GRID_SIZE + 1):
            column_tick = label(str(index), 13, MUTED, "MEDIUM")
            column_tick.move_to(
                RIGHT * (GRID_LEFT + (index - 0.5) * CELL_SIZE)
                + UP * (GRID_TOP + 0.17)
            )
            column_ticks.append(column_tick)

            row_tick = label(str(index), 13, MUTED, "MEDIUM")
            row_tick.move_to(
                RIGHT * (GRID_LEFT - 0.18)
                + UP * (GRID_TOP - (index - 0.5) * CELL_SIZE)
            )
            row_ticks.append(row_tick)

        ticks = VGroup(*column_ticks, *row_ticks)
        axis_titles = VGroup(
            label("列 m ↓", 20, CORAL, "BOLD").move_to(
                [GRID_LEFT + 0.63, GRID_TOP + 0.49, 0]
            ),
            label("行 n →", 20, BLUE, "BOLD").move_to(
                [grid_right - 0.63, GRID_TOP + 0.49, 0]
            ),
        )
        return lines, ticks, axis_titles, row_ticks, column_ticks

    @classmethod
    def number_art(cls) -> dict[int, object]:
        result = {}
        for coordinate, value in GRID_VALUES.items():
            size = 17 if value < 10 else 14 if value < 100 else 12
            number = label(str(value), size, INK, "MEDIUM")
            number.move_to(cls.cell_center(*coordinate)).set_z_index(5)
            result[value] = number
        return result

    def construct(self) -> None:
        heading = label("第 1 題｜數字沿著哪條路走？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 1 頁｜影片 oRepfpw90Fg",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        grid_lines, grid_ticks, axis_titles, row_ticks, column_ticks = self.grid_art()
        numbers = self.number_art()

        # Beat 01 grid_seed: establish the square and only its first entry.
        self.begin_beat("grid_seed")
        beat_title = label("先從左上角的 1 出發", 31, INK, "BOLD")
        beat_title.move_to([3.15, 2.28, 0])
        grid_facts = VGroup(
            MathTex(r"12\times12", font_size=50, color=BLUE),
            label("一共 144 格", 28, INK, "BOLD"),
            label("數字會依序放入 1 到 144", 25, MUTED, "MEDIUM"),
        ).arrange(DOWN, buff=0.34).move_to([3.15, 0.38, 0])

        self.add(heading, source)
        self.play(Create(grid_lines), run_time=1.25)
        self.play(FadeIn(grid_ticks), FadeIn(axis_titles), run_time=0.75)
        self.play(GrowFromCenter(numbers[1]), FadeIn(beat_title), run_time=0.65)
        self.play(FadeIn(grid_facts), run_time=0.7)

        # Beat 02 follow_numbers: let one marker make the actual first moves.
        self.next_beat("follow_numbers")
        next_title = label("跟著 2 到 10 走一次", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        marker = Square(
            side_length=CELL_SIZE * 0.82,
            color=POINT,
            stroke_width=4,
            fill_color=POINT,
            fill_opacity=0.14,
        ).move_to(self.cell_center(1, 1)).set_z_index(3)
        walk_prompt = label("每走幾步，方向就重新開始", 27, POINT, "BOLD")
        walk_prompt.move_to([3.15, -1.70, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(grid_facts),
            FadeIn(marker),
            run_time=0.7,
        )
        beat_title = next_title
        for value in range(2, 11):
            self.play(
                marker.animate.move_to(self.cell_center(*VALUE_COORDS[value])),
                FadeIn(numbers[value], shift=UP * 0.04),
                run_time=0.38,
            )
        self.play(FadeIn(walk_prompt), run_time=0.45)

        # Beat 03 notice_diagonals: group the same numbers without a formula yet.
        self.next_beat("notice_diagonals")
        next_title = label("把數字看成一條一條斜線", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        early_diagonals = {
            total: self.diagonal_cells(total, REGION, 0.15)
            for total in range(2, 6)
        }
        early_arrows = {
            total: self.diagonal_arrow(total, REGION)
            for total in range(3, 6)
        }
        grouped_values = MathTex(
            "1",
            r"\;|\;",
            "2,3",
            r"\;|\;",
            "4,5,6",
            r"\;|\;",
            "7,8,9,10",
            font_size=37,
            color=INK,
        ).move_to([3.15, 0.55, 0])
        grouped_values[0].set_color(POINT)
        grouped_values[2].set_color(REGION)
        grouped_values[4].set_color(REGION)
        grouped_values[6].set_color(REGION)
        diagonal_note = label("每一組都由左下走向右上", 27, REGION, "BOLD")
        diagonal_note.move_to([3.15, -0.45, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(walk_prompt),
            FadeOut(marker),
            run_time=0.6,
        )
        beat_title = next_title
        for index, total in enumerate(range(2, 6)):
            source_numbers = VGroup(
                *(numbers[GRID_VALUES[coordinate]] for coordinate in self.diagonal_coordinates(total))
            )
            animations = [FadeIn(early_diagonals[total])]
            if total in early_arrows:
                animations.append(Create(early_arrows[total]))
            animations.append(TransformFromCopy(source_numbers, grouped_values[2 * index]))
            self.play(*animations, run_time=0.7)
        self.play(
            Write(VGroup(grouped_values[1], grouped_values[3], grouped_values[5])),
            FadeIn(diagonal_note),
            run_time=0.65,
        )

        # Beat 04 one_diagonal: earn m+n by inspecting one concrete group.
        self.next_beat("one_diagonal")
        next_title = label("只盯住 4、5、6 這一條", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        focus_diagonal = self.diagonal_cells(4, POINT, 0.31)
        dim_numbers = VGroup(*(numbers[value] for value in (1, 2, 3, 7, 8, 9, 10)))
        coordinate_row = MathTex(
            r"(3,1)",
            r"\quad(2,2)",
            r"\quad(1,3)",
            font_size=39,
            color=REGION,
        ).move_to([3.15, 0.95, 0])
        sum_row = MathTex(
            "3+1",
            "=",
            "2+2",
            "=",
            "1+3",
            "=",
            "4",
            font_size=40,
            color=INK,
        ).move_to([3.15, -0.05, 0])
        sum_row[6].set_color(POINT)
        invariant = MathTex(r"m+n=4", font_size=48, color=POINT)
        invariant.move_to([3.15, -1.20, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(VGroup(*early_diagonals.values(), *early_arrows.values())),
            FadeOut(grouped_values),
            FadeOut(diagonal_note),
            FadeIn(focus_diagonal),
            dim_numbers.animate.set_opacity(0.22),
            run_time=0.85,
        )
        beat_title = next_title
        self.play(FadeIn(coordinate_row), run_time=0.55)
        self.play(Write(sum_row), run_time=0.8)
        self.play(TransformFromCopy(sum_row, invariant), run_time=0.7)

        # Beat 05 grow_then_shrink: make the square boundary change the counts.
        self.next_beat("grow_then_shrink")
        next_title = label("斜線先變長，碰到邊界後再變短", 29, INK, "BOLD")
        next_title.move_to(beat_title)
        boundary_diagonals = {
            13: self.diagonal_cells(13, BLUE, 0.17),
            14: self.diagonal_cells(14, REGION, 0.17),
            15: self.diagonal_cells(15, CORAL, 0.17),
            16: self.diagonal_cells(16, POINT, 0.17),
        }

        lengths = list(range(1, 13)) + list(range(11, 0, -1))
        bar_width = 0.22
        bar_gap = 0.055
        bar_start = 0.04
        bar_base = -0.88
        bar_scale = 0.175
        bars = VGroup()
        bar_colors = []
        for index, length in enumerate(lengths):
            if index < 12:
                color = BLUE
            elif index == 12:
                color = REGION
            elif index == 13:
                color = CORAL
            elif index == 14:
                color = POINT
            else:
                color = PURPLE
            bar_colors.append(color)
            height = length * bar_scale
            bar = Rectangle(
                width=bar_width,
                height=height,
                stroke_width=0,
                fill_color=color,
                fill_opacity=0.82,
            )
            bar.move_to(
                [bar_start + index * (bar_width + bar_gap), bar_base + height / 2, 0]
            )
            bars.add(bar)
        profile_base = Line(
            [bar_start - 0.14, bar_base, 0],
            [bar_start + 22 * (bar_width + bar_gap) + bar_width + 0.14, bar_base, 0],
            color=HAIRLINE,
            stroke_width=2,
        )
        selected_bar_labels = VGroup()
        for index in (0, 11, 12, 13, 14, 22):
            text = label(str(lengths[index]), 12, bar_colors[index], "BOLD")
            text.next_to(bars[index], UP, buff=0.05)
            selected_bar_labels.add(text)
        profile_note = label("每根短棒＝一條斜線的格數", 23, MUTED, "MEDIUM")
        profile_note.move_to([3.15, -1.58, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(focus_diagonal),
            FadeOut(coordinate_row),
            FadeOut(sum_row),
            FadeOut(invariant),
            dim_numbers.animate.set_opacity(0.72),
            Create(profile_base),
            run_time=0.75,
        )
        beat_title = next_title
        self.play(
            FadeIn(boundary_diagonals[13]),
            LaggedStart(
                *(GrowFromEdge(bars[index], DOWN) for index in range(12)),
                lag_ratio=0.055,
            ),
            run_time=1.55,
        )
        self.play(
            FadeIn(boundary_diagonals[14]),
            FadeIn(boundary_diagonals[15]),
            FadeIn(boundary_diagonals[16]),
            LaggedStart(
                *(GrowFromEdge(bars[index], DOWN) for index in range(12, 23)),
                lag_ratio=0.055,
            ),
            run_time=1.45,
        )
        self.play(FadeIn(selected_bar_labels), FadeIn(profile_note), run_time=0.55)

        # Beat 06 count_to_78: count the growing half before touching later bands.
        self.next_beat("count_to_78")
        next_title = label("先只算前 12 條斜線", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        first_half = VGroup(
            *(
                Square(
                    side_length=CELL_SIZE * 0.91,
                    stroke_width=0,
                    fill_color=BLUE,
                    fill_opacity=0.055,
                ).move_to(self.cell_center(row, column)).set_z_index(-3)
                for (row, column) in GRID_VALUES
                if row + column <= 13
            )
        )
        count_formula = MathTex(
            "1",
            "+",
            "2",
            "+",
            r"\cdots",
            "+",
            "12",
            "=",
            "78",
            font_size=43,
            color=INK,
        ).move_to([3.15, -2.05, 0])
        count_formula[0].set_color(BLUE)
        count_formula[2].set_color(BLUE)
        count_formula[6].set_color(BLUE)
        count_formula[8].set_color(POINT)
        count_note = label("第 12 條斜線的最後一格就是 78", 24, POINT, "BOLD")
        count_note.move_to([3.15, -2.72, 0])
        numbers[78].set_color(POINT)

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeIn(first_half),
            VGroup(*bars[:12]).animate.set_opacity(0.95),
            VGroup(*bars[12:]).animate.set_opacity(0.16),
            boundary_diagonals[14].animate.set_fill(opacity=0.045),
            boundary_diagonals[15].animate.set_fill(opacity=0.045),
            boundary_diagonals[16].animate.set_fill(opacity=0.045),
            FadeOut(profile_note),
            run_time=0.85,
        )
        beat_title = next_title
        self.play(
            Indicate(bars[0], color=BLUE, scale_factor=1.08),
            Indicate(bars[1], color=BLUE, scale_factor=1.08),
            Indicate(bars[11], color=BLUE, scale_factor=1.08),
            run_time=0.55,
        )
        self.play(Write(count_formula), run_time=0.85)
        self.play(FadeIn(numbers[78]), FadeIn(count_note), run_time=0.6)
        self.play(Indicate(numbers[78], color=POINT), run_time=0.55)

        # Beat 07 step_to_99: consume two complete shrinking diagonals.
        self.next_beat("step_to_99")
        next_title = label("再走完整的 11 格、10 格", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        note_14 = VGroup(
            MathTex(r"m+n=14", font_size=34, color=INK),
            label("共有 11 格", 24, REGION, "BOLD"),
        ).arrange(RIGHT, buff=0.24)
        note_14.move_to([3.15, 1.15, 0])
        note_15 = VGroup(
            MathTex(r"m+n=15", font_size=34, color=INK),
            label("共有 10 格", 24, CORAL, "BOLD"),
        ).arrange(RIGHT, buff=0.24)
        note_15.move_to([3.15, 0.40, 0])
        stage_one = MathTex("78", "+", "11", "=", "89", font_size=45, color=INK)
        stage_one[2].set_color(REGION)
        stage_one[4].set_color(POINT)
        stage_one.move_to([3.15, -0.78, 0])
        stage_two = MathTex(
            "78", "+", "11", "+", "10", "=", "99", font_size=45, color=INK
        )
        stage_two[2].set_color(REGION)
        stage_two[4].set_color(CORAL)
        stage_two[6].set_color(POINT)
        stage_two.move_to([3.15, -0.78, 0])
        ninety_nine_note = label("兩條都走完，現在停在 99", 26, POINT, "BOLD")
        ninety_nine_note.move_to([3.15, -1.60, 0])
        for value in (79, 89):
            numbers[value].set_color(REGION)
        for value in (90, 99):
            numbers[value].set_color(CORAL if value == 90 else POINT)

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(VGroup(*bars, profile_base, selected_bar_labels)),
            FadeOut(count_formula),
            FadeOut(count_note),
            FadeOut(first_half),
            boundary_diagonals[13].animate.set_fill(opacity=0.05),
            boundary_diagonals[14].animate.set_fill(opacity=0.25),
            run_time=0.9,
        )
        beat_title = next_title
        self.play(
            FadeIn(note_14),
            FadeIn(numbers[79]),
            FadeIn(numbers[89]),
            Write(stage_one),
            run_time=0.85,
        )
        self.play(
            boundary_diagonals[15].animate.set_fill(opacity=0.25),
            FadeIn(note_15),
            FadeIn(numbers[90]),
            FadeIn(numbers[99]),
            ReplacementTransform(stage_one, stage_two),
            run_time=0.9,
        )
        self.play(FadeIn(ninety_nine_note), Indicate(numbers[99], color=POINT), run_time=0.65)

        # Beat 08 find_the_band: locate the offset without revealing its cell.
        self.next_beat("find_the_band")
        next_title = label("104 比 99 多走幾格？", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        offset = MathTex("104", "-", "99", "=", "5", font_size=50, color=INK)
        offset[0].set_color(POINT)
        offset[2].set_color(CORAL)
        offset[4].set_color(POINT)
        offset.move_to([3.15, 0.65, 0])
        next_band = MathTex(r"m+n=16", font_size=45, color=POINT)
        next_band.move_to([3.15, -0.30, 0])
        fifth_cell = label("所以要找這條斜線的第 5 格", 27, POINT, "BOLD")
        fifth_cell.move_to([3.15, -1.12, 0])
        start_card = MathTex(r"(12,4)", r"\longrightarrow", "100", font_size=37, color=INK)
        start_card[0].set_color(REGION)
        start_card.move_to([3.15, -1.90, 0])
        numbers[100].set_color(REGION)
        marker.move_to(self.cell_center(12, 4))

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(note_14),
            FadeOut(note_15),
            FadeOut(stage_two),
            FadeOut(ninety_nine_note),
            boundary_diagonals[14].animate.set_fill(opacity=0.06),
            boundary_diagonals[15].animate.set_fill(opacity=0.06),
            boundary_diagonals[16].animate.set_fill(opacity=0.28),
            run_time=0.85,
        )
        beat_title = next_title
        self.play(Write(offset), run_time=0.7)
        self.play(FadeIn(next_band), FadeIn(fifth_cell), run_time=0.6)
        self.play(FadeIn(marker), FadeIn(numbers[100]), FadeIn(start_card), run_time=0.7)

        # Beat 09 walk_five_cells: count exact cells and reveal the answer only at five.
        self.next_beat("walk_five_cells")
        next_title = label("同一條斜線上，一上一右", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        walk_rule = MathTex(
            r"(m,n)", r"\longrightarrow", r"(m-1,n+1)", font_size=37, color=INK
        )
        walk_rule[2].set_color(REGION)
        walk_rule.move_to([3.15, 1.55, 0])
        walk_coordinates = [(12 - step, 4 + step) for step in range(5)]
        walk_values = [GRID_VALUES[coordinate] for coordinate in walk_coordinates]
        if walk_values != [100, 101, 102, 103, 104]:
            raise ValueError("the five-cell walk does not land on 104")
        walk_rows = VGroup()
        for index, ((row, column), value) in enumerate(
            zip(walk_coordinates, walk_values, strict=True)
        ):
            row_art = MathTex(
                rf"({row},{column})",
                r"\longrightarrow",
                str(value),
                font_size=32,
                color=POINT if value == 104 else INK,
            )
            row_art.move_to([3.15, 0.78 - index * 0.62, 0])
            walk_rows.add(row_art)
        numbers[101].set_color(REGION)
        numbers[102].set_color(REGION)
        numbers[103].set_color(REGION)
        numbers[104].set_color(POINT)

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(offset),
            FadeOut(next_band),
            FadeOut(fifth_cell),
            FadeIn(walk_rule),
            ReplacementTransform(start_card, walk_rows[0]),
            run_time=0.8,
        )
        beat_title = next_title
        for index in range(1, 5):
            coordinate = walk_coordinates[index]
            value = walk_values[index]
            self.play(
                marker.animate.move_to(self.cell_center(*coordinate)),
                FadeIn(numbers[value]),
                FadeIn(walk_rows[index], shift=UP * 0.05),
                run_time=0.62,
            )
        self.play(
            Circumscribe(VGroup(marker, numbers[104]), color=POINT),
            Indicate(walk_rows[4], color=POINT),
            run_time=0.8,
        )

        # Beat 10 return_and_check: restore all 144 entries and verify both counts.
        self.next_beat("return_and_check")
        next_title = label("回到整張表，再檢查一次", 31, INK, "BOLD")
        next_title.move_to(beat_title)
        visible_values = {
            *range(1, 11),
            78,
            79,
            89,
            90,
            99,
            100,
            101,
            102,
            103,
            104,
        }
        existing_numbers = VGroup(
            *(numbers[value] for value in sorted(visible_values) if value != 104)
        )
        missing_numbers = [
            numbers[value]
            for value in range(1, GRID_SIZE**2 + 1)
            if value not in visible_values
        ]
        for number in missing_numbers:
            number.set_opacity(0.34)

        target_row, target_column = VALUE_COORDS[104]
        target_center = self.cell_center(target_row, target_column)
        horizontal_guide = DashedLine(
            [GRID_LEFT - 0.02, target_center[1], 0],
            target_center,
            color=POINT,
            stroke_width=3,
            dash_length=0.08,
        ).set_z_index(2)
        vertical_guide = DashedLine(
            [target_center[0], GRID_TOP + 0.02, 0],
            target_center,
            color=POINT,
            stroke_width=3,
            dash_length=0.08,
        ).set_z_index(2)
        invariant_check = MathTex("8+8", "=", "16", font_size=45, color=INK)
        invariant_check[0].set_color(POINT)
        invariant_check.move_to([3.15, 0.95, 0])
        count_check = MathTex("99", "+", "5", "=", "104", font_size=45, color=INK)
        count_check[0].set_color(CORAL)
        count_check[2].set_color(POINT)
        count_check[4].set_color(POINT)
        count_check.move_to([3.15, -0.05, 0])
        final_answer = MathTex(r"(m,n)=(8,8)", font_size=54, color=POINT)
        final_answer.move_to([3.15, -1.35, 0])
        answer_box = SurroundingRectangle(
            final_answer,
            color=POINT,
            buff=0.22,
            stroke_width=3,
        )
        final_note = label("座標和鎖定斜線，第 5 格鎖定位置", 24, MUTED, "MEDIUM")
        final_note.move_to([3.15, -2.18, 0])

        self.play(
            ReplacementTransform(beat_title, next_title),
            FadeOut(walk_rule),
            FadeOut(walk_rows),
            FadeOut(VGroup(*boundary_diagonals.values())),
            existing_numbers.animate.set_opacity(0.34),
            run_time=0.85,
        )
        beat_title = next_title
        self.play(
            LaggedStart(
                *(FadeIn(number, shift=UP * 0.025) for number in missing_numbers),
                lag_ratio=0.003,
            ),
            run_time=1.6,
        )
        self.play(
            Create(horizontal_guide),
            Create(vertical_guide),
            row_ticks[7].animate.set_color(POINT).scale(1.25),
            column_ticks[7].animate.set_color(POINT).scale(1.25),
            numbers[104].animate.set_opacity(1).set_color(POINT),
            marker.animate.set_fill(opacity=0.22),
            run_time=0.8,
        )
        self.play(
            TransformFromCopy(VGroup(row_ticks[7], column_ticks[7]), invariant_check[0]),
            Write(VGroup(invariant_check[1], invariant_check[2])),
            run_time=0.75,
        )
        self.play(Write(count_check), run_time=0.75)
        self.play(Write(final_answer), Create(answer_box), FadeIn(final_note), run_time=0.9)
        self.play(
            Circumscribe(VGroup(marker, numbers[104]), color=POINT),
            Indicate(final_answer, color=POINT),
            run_time=0.8,
        )
