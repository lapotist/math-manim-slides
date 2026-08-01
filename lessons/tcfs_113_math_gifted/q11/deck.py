"""Manim Slides lesson for ROC 113 TCFS mathematics gifted fill-in Q11."""

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
    RoundedRectangle,
    Succession,
    SurroundingRectangle,
    Transform,
    VGroup,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


WIDTH_BLOCKS = (
    (1, 1, 3, 3, 3),
    (2, 4, 9, 12, 15),
    (3, 10, 31, 66, 81),
    (4, 32, 99, 272, 353),
    (5, 100, 316, 1085, 1438),
)


def square_digit_stream(minimum_length: int) -> str:
    """Return the direct square stream through the requested length."""
    chunks: list[str] = []
    length = 0
    integer = 1
    while length < minimum_length:
        chunk = str(integer * integer)
        chunks.append(chunk)
        length += len(chunk)
        integer += 1
    return "".join(chunks)


def locate_within_block(
    position: int,
    previous_cumulative: int,
    width: int,
    first_root: int,
) -> tuple[int, int, int, int]:
    """Return offset, completed squares, 1-indexed digit, and root."""
    offset = position - previous_cumulative
    completed, zero_based_digit = divmod(offset - 1, width)
    return offset, completed, zero_based_digit + 1, first_root + completed


STREAM = square_digit_stream(2024)
LOCATION_113 = locate_within_block(113, 81, 4, 32)
LOCATION_2024 = locate_within_block(2024, 1438, 6, 317)

if WIDTH_BLOCKS != (
    (1, 1, 3, 3, 3),
    (2, 4, 9, 12, 15),
    (3, 10, 31, 66, 81),
    (4, 32, 99, 272, 353),
    (5, 100, 316, 1085, 1438),
):
    raise ValueError("unexpected square-width blocks")
if LOCATION_113 != (32, 7, 4, 39) or LOCATION_2024 != (586, 97, 4, 414):
    raise ValueError("unexpected target locations")
if (STREAM[112], STREAM[2023]) != ("1", "3"):
    raise ValueError("direct digit stream disagrees with target answer")
if not (
    STREAM[80] == str(31**2)[-1]
    and STREAM[81] == str(32**2)[0]
    and STREAM[1437] == str(316**2)[-1]
    and STREAM[1438] == str(317**2)[0]
):
    raise ValueError("digit-width boundary check failed")


class CarloTcfs113MathQ11(CarloSlide):
    """Locate two digits using cumulative square-width blocks."""

    lesson_id = "carlo.tcfs_113_math_gifted.q11"

    @staticmethod
    def replace_title(scene: "CarloTcfs113MathQ11", old, new) -> None:
        scene.play(FadeOut(old), run_time=0.25)
        scene.play(FadeIn(new), run_time=0.30)

    @staticmethod
    def digit_cell(
        digit: str,
        *,
        color: str = INK,
        width: float = 0.78,
        height: float = 0.94,
        font_size: float = 39,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.06,
            color=HAIRLINE,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.97,
        )
        value = MathTex(digit, font_size=font_size, color=color).move_to(frame)
        frame.set_z_index(2)
        value.set_z_index(3)
        return VGroup(frame, value)

    @classmethod
    def square_chunk(cls, root: int) -> VGroup:
        digits = VGroup(*(cls.digit_cell(digit) for digit in str(root * root)))
        digits.arrange(RIGHT, buff=0.035)
        caption = MathTex(f"{root}^2", font_size=24, color=MUTED).next_to(
            digits, UP, buff=0.15
        )
        return VGroup(digits, caption)

    @staticmethod
    def cursor_for(cell: VGroup, color: str) -> Arrow:
        return Arrow(
            cell.get_bottom() + DOWN * 0.73,
            cell.get_bottom() + DOWN * 0.06,
            buff=0,
            color=color,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.28,
        )

    @staticmethod
    def width_block(
        width: int,
        first_root: int,
        last_root: int,
        contribution: int,
        cumulative: int,
        color: str,
        *,
        card_width: float = 3.72,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=card_width,
            height=2.12,
            corner_radius=0.08,
            color=color,
            stroke_width=2.6,
            fill_color=BG,
            fill_opacity=0.97,
        )
        title = label(f"{width} 位平方數", 21, color, "BOLD")
        roots = MathTex(
            f"{first_root}^2",
            r"\ldots",
            f"{last_root}^2",
            font_size=27,
            color=INK,
        )
        count = last_root - first_root + 1
        addition = MathTex(
            str(count),
            r"\cdot",
            str(width),
            "=",
            str(contribution),
            font_size=27,
            color=INK,
        )
        cumulative_tex = MathTex(
            r"\Sigma",
            "=",
            str(cumulative),
            font_size=29,
            color=color,
        )
        content = VGroup(title, roots, addition, cumulative_tex).arrange(DOWN, buff=0.13)
        content.move_to(frame)
        return VGroup(frame, content)

    @staticmethod
    def summary_card(title_text: str, tex: str, color: str, *, width: float = 3.4) -> VGroup:
        frame = RoundedRectangle(
            width=width,
            height=1.50,
            corner_radius=0.08,
            color=color,
            stroke_width=2.4,
            fill_color=BG,
            fill_opacity=0.97,
        )
        title = label(title_text, 20, color, "BOLD")
        value = MathTex(tex, font_size=31, color=INK)
        content = VGroup(title, value).arrange(DOWN, buff=0.20).move_to(frame)
        return VGroup(frame, content)

    @staticmethod
    def boundary_card(
        position: int,
        square_tex: str,
        caption_text: str,
        color: str,
    ) -> VGroup:
        frame = RoundedRectangle(
            width=4.45,
            height=1.50,
            corner_radius=0.08,
            color=color,
            stroke_width=2.2,
            fill_color=BG,
            fill_opacity=0.97,
        )
        position_tex = MathTex("k", "=", str(position), font_size=27, color=color)
        square = MathTex(square_tex, font_size=31, color=INK)
        caption = label(caption_text, 18, MUTED, "MEDIUM")
        content = VGroup(position_tex, square, caption).arrange(DOWN, buff=0.10).move_to(frame)
        return VGroup(frame, content)

    @staticmethod
    def square_slot(root: int, color: str = MUTED) -> VGroup:
        frame = RoundedRectangle(
            width=1.42,
            height=0.88,
            corner_radius=0.06,
            color=color,
            stroke_width=2,
            fill_color=BG,
            fill_opacity=0.97,
        )
        value = MathTex(f"{root}^2", font_size=27, color=color).move_to(frame)
        return VGroup(frame, value)

    def construct(self) -> None:
        heading = label("第 11 題｜平方數接成的數字帶", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 11 頁｜影片 FxSdkChC9Z8",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01: establish one short tape and the 1-indexed cursor.
        self.begin_beat("move_cursor_on_tape")
        beat_title = label("游標從第 1 位開始走", 35, INK, "BOLD")
        beat_title.move_to([0, 2.88, 0])
        chunks = VGroup(*(self.square_chunk(root) for root in range(1, 7)))
        chunks.arrange(RIGHT, buff=0.24).move_to([0, 0.38, 0])
        all_cells = [cell for chunk in chunks for cell in chunk[0]]
        cursor = self.cursor_for(all_cells[0], POINT)
        index_label = MathTex("k", "=", "1", font_size=32, color=POINT)
        index_label.next_to(cursor, DOWN, buff=0.08)
        one_indexed = label("全域位置從 1 開始", 24, POINT, "BOLD")
        one_indexed.move_to([0, -2.02, 0])
        example = MathTex("d_5", "=", "6", font_size=43, color=INK)
        example[0].set_color(POINT)
        example[2].set_color(REGION)
        example.move_to([4.82, -1.45, 0])

        self.add(heading, source)
        self.play(FadeIn(beat_title), run_time=0.45)
        self.play(LaggedStart(*(FadeIn(chunk) for chunk in chunks), lag_ratio=0.12), run_time=1.2)
        self.play(GrowFromCenter(cursor), FadeIn(index_label), FadeIn(one_indexed), run_time=0.65)

        self.next_beat("read_short_tape_example")
        target_cursor = self.cursor_for(all_cells[4], POINT)
        target_index = MathTex("k", "=", "5", font_size=32, color=POINT)
        target_index.next_to(target_cursor, DOWN, buff=0.08)
        self.play(
            Transform(cursor, target_cursor),
            Succession(FadeOut(index_label), FadeIn(target_index)),
            all_cells[0][0].animate.set_fill(BG, opacity=0.97),
            all_cells[4][0].animate.set_fill(POINT, opacity=0.22),
            run_time=1.15,
        )
        index_label = target_index
        self.play(FadeIn(example), run_time=0.65)
        self.wait(0.4)

        # Beat 02: group only the first three widths and earn cumulative 81.
        self.next_beat("build_boundary_81")
        next_title = label("同位數的平方，先收成三個區塊", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        block_colors = (BLUE, REGION, PURPLE)
        width_cards = VGroup(
            *(
                self.width_block(*block, color)
                for block, color in zip(WIDTH_BLOCKS[:3], block_colors, strict=True)
            )
        )
        width_cards.arrange(RIGHT, buff=0.34).move_to([0, 0.36, 0])
        cumulative_line = MathTex(
            "3",
            r"\longrightarrow",
            "15",
            r"\longrightarrow",
            "81",
            font_size=39,
            color=MUTED,
        ).move_to([0, -1.45, 0])
        cumulative_line[0].set_color(BLUE)
        cumulative_line[2].set_color(REGION)
        cumulative_line[4].set_color(PURPLE)
        boundary_note = label("前三段在第 81 位結束", 24, PURPLE, "BOLD")
        boundary_note.move_to([0, -2.12, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(chunks), FadeOut(cursor), FadeOut(index_label), FadeOut(one_indexed), FadeOut(example), run_time=0.6)
        self.play(LaggedStart(*(FadeIn(card) for card in width_cards), lag_ratio=0.20), run_time=1.1)
        self.play(FadeIn(cumulative_line), FadeIn(boundary_note), run_time=0.75)
        self.wait(0.4)

        # Beat 03: add the four-digit block and test the 81/82 boundary.
        self.next_beat("place_position_113")
        next_title = label("第 113 位進入四位數平方區塊", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        prefix_81 = self.summary_card("前三段累計", r"\Sigma=81", PURPLE, width=4.15)
        prefix_81.move_to([-2.65, 1.20, 0])
        block_4 = self.width_block(*WIDTH_BLOCKS[3], POINT, card_width=4.75)
        block_4.scale(0.82).move_to([2.55, 1.20, 0])
        target_range = MathTex("81", "<", "113", r"\le", "353", font_size=43, color=INK)
        target_range[0].set_color(PURPLE)
        target_range[2].set_color(POINT)
        target_range[4].set_color(POINT)
        target_range.move_to([0, -0.08, 0])
        boundary_81 = self.boundary_card(81, r"31^2=96\boxed{1}", "三位數區塊最後一位", PURPLE)
        boundary_82 = self.boundary_card(82, r"32^2=\boxed{1}024", "四位數區塊第一位", POINT)
        boundary_pair_81 = VGroup(boundary_81, boundary_82).arrange(RIGHT, buff=0.55)
        boundary_pair_81.move_to([0, -1.42, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(cumulative_line),
            FadeOut(boundary_note),
            FadeOut(width_cards),
            run_time=0.45,
        )
        self.play(FadeIn(prefix_81), FadeIn(block_4), run_time=0.65)
        self.play(FadeIn(target_range), run_time=0.6)
        self.play(LaggedStart(FadeIn(boundary_81), FadeIn(boundary_82), lag_ratio=0.22), run_time=0.9)
        self.wait(0.4)

        # Beat 04: resolve offset 32 as seven complete squares plus digit four.
        self.next_beat("resolve_113_square")
        next_title = label("32 位 = 七個完整平方，再走四格", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        offset_113 = MathTex("113", "-", "81", "=", "32", font_size=43, color=INK)
        offset_113[0].set_color(POINT)
        offset_113[2].set_color(PURPLE)
        offset_113[4].set_color(POINT)
        offset_113.move_to([0, 1.82, 0])
        decomposition_113 = MathTex("32", "=", "7", r"\cdot", "4", "+", "4", font_size=43, color=INK)
        decomposition_113[0].set_color(POINT)
        decomposition_113[2].set_color(BLUE)
        decomposition_113[6].set_color(POINT)
        decomposition_113.move_to([0, 1.08, 0])
        square_slots_113 = VGroup(*(self.square_slot(root) for root in range(32, 40)))
        square_slots_113.arrange(RIGHT, buff=0.12).move_to([0, -0.20, 0])
        slot_numbers = VGroup(
            *(
                MathTex(str(index), font_size=20, color=MUTED).next_to(slot, DOWN, buff=0.10)
                for index, slot in enumerate(square_slots_113, start=1)
            )
        )
        root_39 = MathTex("n", "=", "32", "+", "7", "=", "39", font_size=41, color=INK)
        root_39[2].set_color(POINT)
        root_39[4].set_color(BLUE)
        root_39[6].set_color(POINT)
        root_39.move_to([0, -1.70, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(prefix_81), FadeOut(block_4), FadeOut(target_range), FadeOut(boundary_pair_81), run_time=0.6)
        self.play(FadeIn(offset_113), FadeIn(decomposition_113), run_time=0.75)
        self.play(LaggedStart(*(FadeIn(slot) for slot in square_slots_113), lag_ratio=0.08), FadeIn(slot_numbers), run_time=1.0)

        self.next_beat("identify_square_39")
        target_slot_frame = SurroundingRectangle(square_slots_113[-1], color=POINT, buff=0.08, stroke_width=4)
        self.play(square_slots_113[:-1].animate.set_opacity(0.28), Create(target_slot_frame), run_time=0.65)
        self.play(FadeIn(root_39), run_time=0.65)
        self.wait(0.4)

        # Beat 05: expand 39^2 and read its fourth digit.
        self.next_beat("read_digit_a")
        next_title = label("展開 39 的平方，游標停在第 4 格", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        square_39 = MathTex("39^2", "=", "1521", font_size=48, color=INK)
        square_39[0].set_color(POINT)
        square_39.move_to([0, 1.42, 0])
        digits_39 = VGroup(*(self.digit_cell(digit, width=1.20, height=1.15, font_size=48) for digit in "1521"))
        digits_39.arrange(RIGHT, buff=0.08).move_to([0, 0.03, 0])
        internal_39 = VGroup(
            *(
                MathTex(str(index), font_size=24, color=MUTED).next_to(cell, DOWN, buff=0.12)
                for index, cell in enumerate(digits_39, start=1)
            )
        )
        cursor_113 = self.cursor_for(digits_39[-1], POINT)
        cursor_113_label = MathTex("k_{inside}", "=", "4", font_size=29, color=POINT)
        cursor_113_label.next_to(cursor_113, DOWN, buff=0.08)
        a_badge = MathTex("a", "=", "1", font_size=51, color=INK)
        a_badge[0].set_color(POINT)
        a_badge[2].set_color(POINT)
        a_badge.move_to([4.72, -1.30, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(offset_113),
            FadeOut(decomposition_113),
            FadeOut(square_slots_113),
            FadeOut(slot_numbers),
            FadeOut(target_slot_frame),
            FadeOut(root_39),
            run_time=0.50,
        )
        self.play(FadeIn(square_39), run_time=0.55)
        self.play(LaggedStart(*(FadeIn(cell) for cell in digits_39), lag_ratio=0.12), FadeIn(internal_39), run_time=0.9)

        self.next_beat("select_fourth_digit_a")
        self.play(GrowFromCenter(cursor_113), FadeIn(cursor_113_label), run_time=0.55)
        self.play(
            digits_39[-1][0].animate.set_fill(POINT, opacity=0.22),
            FadeIn(a_badge),
            run_time=0.7,
        )
        self.wait(0.4)

        # Beat 06: extend the cumulative tape only through the six-digit entrance.
        self.next_beat("extend_boundary_1438")
        next_title = label("再加五位數區塊，累計到 1438", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        milestone_81 = self.summary_card("一到三位數", r"\Sigma=81", PURPLE, width=2.85)
        milestone_353 = self.summary_card("四位數", r"+272\;\Rightarrow\;353", POINT, width=3.15)
        milestone_1438 = self.summary_card("五位數", r"+1085\;\Rightarrow\;1438", CORAL, width=3.55)
        milestone_6 = self.summary_card("六位數從這裡開始", r"317^2=100489", REGION, width=3.35)
        milestones = VGroup(milestone_81, milestone_353, milestone_1438, milestone_6)
        milestones.arrange(RIGHT, buff=0.25).move_to([0, 0.30, 0])
        five_count = MathTex("316-100+1", "=", "217", font_size=39, color=INK)
        five_digits = MathTex("217", r"\cdot", "5", "=", "1085", font_size=39, color=INK)
        five_count[2].set_color(CORAL)
        five_digits[0].set_color(CORAL)
        five_digits[4].set_color(CORAL)
        five_math = VGroup(five_count, five_digits).arrange(RIGHT, buff=0.85)
        five_math.move_to([0, -1.18, 0])
        after_boundary = MathTex("1438", "<", "2024", font_size=43, color=INK)
        after_boundary[0].set_color(CORAL)
        after_boundary[2].set_color(REGION)
        after_boundary.move_to([0, -2.00, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        a_corner = a_badge.copy().scale(0.72).move_to([5.72, 1.86, 0])
        self.play(
            FadeOut(square_39),
            FadeOut(digits_39),
            FadeOut(internal_39),
            FadeOut(cursor_113),
            FadeOut(cursor_113_label),
            Transform(a_badge, a_corner),
            run_time=0.65,
        )
        self.play(LaggedStart(*(FadeIn(card) for card in milestones), lag_ratio=0.13), run_time=1.0)
        self.play(FadeIn(five_math), FadeIn(after_boundary), run_time=0.75)
        self.wait(0.4)

        # Beat 07: test the 1438/1439 boundary before subtracting.
        self.next_beat("place_position_2024")
        next_title = label("第 1439 位才是六位數區塊的第一格", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        boundary_1438 = self.boundary_card(1438, r"316^2=9985\boxed{6}", "五位數區塊最後一位", CORAL)
        boundary_1439 = self.boundary_card(1439, r"317^2=\boxed{1}00489", "六位數區塊第一位", REGION)
        boundary_pair_1438 = VGroup(boundary_1438, boundary_1439).arrange(RIGHT, buff=0.55)
        boundary_pair_1438.move_to([0, 0.58, 0])
        offset_2024 = MathTex("2024", "-", "1438", "=", "586", font_size=47, color=INK)
        offset_2024[0].set_color(REGION)
        offset_2024[2].set_color(CORAL)
        offset_2024[4].set_color(REGION)
        offset_2024.move_to([0, -1.22, 0])
        boundary_note_1438 = label("新區塊的第一格，區塊內位置就是 1", 23, POINT, "BOLD")
        boundary_note_1438.move_to([0, -2.05, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(milestones), FadeOut(five_math), FadeOut(after_boundary), run_time=0.6)
        self.play(LaggedStart(FadeIn(boundary_1438), FadeIn(boundary_1439), lag_ratio=0.22), run_time=0.9)
        self.play(FadeIn(offset_2024), FadeIn(boundary_note_1438), run_time=0.7)
        self.wait(0.4)

        # Beat 08: resolve offset 586 into 97 complete squares and digit four.
        self.next_beat("resolve_2024_square")
        next_title = label("586 位 = 九十七個完整平方，再走四格", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        decomposition_2024 = MathTex("586", "=", "97", r"\cdot", "6", "+", "4", font_size=47, color=INK)
        decomposition_2024[0].set_color(REGION)
        decomposition_2024[2].set_color(BLUE)
        decomposition_2024[6].set_color(REGION)
        decomposition_2024.move_to([0, 1.60, 0])
        start_slot = self.square_slot(317, REGION)
        end_complete_slot = self.square_slot(413, BLUE)
        target_414_slot = self.square_slot(414, REGION)
        ellipsis = MathTex(r"\cdots", font_size=43, color=MUTED)
        complete_group = VGroup(start_slot, ellipsis, end_complete_slot).arrange(RIGHT, buff=0.40)
        complete_frame = SurroundingRectangle(complete_group, color=BLUE, buff=0.22, stroke_width=3)
        complete_caption = label("前 97 個完整六位數平方", 22, BLUE, "BOLD")
        complete_caption.next_to(complete_frame, DOWN, buff=0.18)
        next_arrow = MathTex(r"\longrightarrow", font_size=43, color=POINT)
        local_tape_2024 = VGroup(complete_group, next_arrow, target_414_slot).arrange(RIGHT, buff=0.55)
        local_tape_2024.move_to([0, 0.18, 0])
        complete_frame.move_to(complete_group)
        complete_caption.next_to(complete_frame, DOWN, buff=0.18)
        target_414_frame = SurroundingRectangle(target_414_slot, color=REGION, buff=0.10, stroke_width=4)
        root_414 = MathTex("n", "=", "317", "+", "97", "=", "414", font_size=43, color=INK)
        root_414[2].set_color(REGION)
        root_414[4].set_color(BLUE)
        root_414[6].set_color(REGION)
        root_414.move_to([0, -1.72, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(FadeOut(boundary_pair_1438), FadeOut(offset_2024), FadeOut(boundary_note_1438), run_time=0.6)
        self.play(FadeIn(decomposition_2024), run_time=0.65)
        self.play(FadeIn(local_tape_2024), Create(complete_frame), FadeIn(complete_caption), run_time=0.85)
        self.play(Create(target_414_frame), FadeIn(root_414), run_time=0.7)
        self.wait(0.4)

        # Beat 09: expand 414^2 and hold both results without the ordered pair.
        self.next_beat("read_digit_b_preanswer")
        next_title = label("兩個目標都停在平方內的第 4 格", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        square_414 = MathTex("414^2", "=", "171396", font_size=48, color=INK)
        square_414[0].set_color(REGION)
        square_414.move_to([0, 1.52, 0])
        digits_414 = VGroup(*(self.digit_cell(digit, width=1.04, height=1.08, font_size=45) for digit in "171396"))
        digits_414.arrange(RIGHT, buff=0.07).move_to([0, 0.23, 0])
        internal_414 = VGroup(
            *(
                MathTex(str(index), font_size=22, color=MUTED).next_to(cell, DOWN, buff=0.11)
                for index, cell in enumerate(digits_414, start=1)
            )
        )
        cursor_2024 = self.cursor_for(digits_414[3], REGION)
        cursor_2024_label = MathTex("k_{inside}", "=", "4", font_size=28, color=REGION)
        cursor_2024_label.next_to(cursor_2024, DOWN, buff=0.08)
        b_badge = MathTex("b", "=", "3", font_size=51, color=INK)
        b_badge[0].set_color(REGION)
        b_badge[2].set_color(REGION)
        b_badge.move_to([4.85, -1.42, 0])
        index_checks = VGroup(
            MathTex("32", "=", "7", r"\cdot", "4", "+", "4", font_size=31, color=POINT),
            MathTex("586", "=", "97", r"\cdot", "6", "+", "4", font_size=31, color=REGION),
        ).arrange(DOWN, buff=0.25).move_to([-4.75, -1.55, 0])
        preanswer_note = label("兩次都從 1 開始：完整平方之後讀第 4 格", 22, POINT, "BOLD")
        preanswer_note.move_to([0, -2.40, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(decomposition_2024),
            FadeOut(local_tape_2024),
            FadeOut(complete_frame),
            FadeOut(complete_caption),
            FadeOut(target_414_frame),
            FadeOut(root_414),
            FadeIn(square_414),
            run_time=0.7,
        )
        self.play(LaggedStart(*(FadeIn(cell) for cell in digits_414), lag_ratio=0.10), FadeIn(internal_414), run_time=0.9)
        self.play(GrowFromCenter(cursor_2024), FadeIn(cursor_2024_label), run_time=0.55)
        self.play(
            digits_414[3][0].animate.set_fill(REGION, opacity=0.22),
            FadeIn(b_badge),
            FadeIn(index_checks),
            FadeIn(preanswer_note),
            run_time=0.8,
        )
        self.wait(0.5)

        # Beat 10: only now assemble the two checked digits into the ordered pair.
        self.next_beat("assemble_ordered_pair")
        next_title = label("最後才依題目順序組成數對", 35, INK, "BOLD")
        next_title.move_to(beat_title)
        ordered_pair = MathTex(
            "(a,b)",
            "=",
            "(",
            "1",
            ",",
            "3",
            ")",
            font_size=58,
            color=INK,
        ).move_to([0, -0.05, 0])
        ordered_pair[0].set_color(PURPLE)
        ordered_pair[3].set_color(POINT)
        ordered_pair[5].set_color(REGION)
        final_frame = SurroundingRectangle(ordered_pair, color=POINT, buff=0.24, stroke_width=4)
        boundary_reminder = VGroup(
            MathTex("81", "|", "82", font_size=31, color=PURPLE),
            MathTex("1438", "|", "1439", font_size=31, color=CORAL),
        ).arrange(RIGHT, buff=1.0)
        reminder_label = label("舊區塊末位｜新區塊首位", 21, MUTED, "MEDIUM")
        reminder = VGroup(boundary_reminder, reminder_label).arrange(DOWN, buff=0.24)
        reminder.move_to([0, -1.72, 0])

        self.replace_title(self, beat_title, next_title)
        beat_title = next_title
        self.play(
            FadeOut(square_414),
            FadeOut(digits_414),
            FadeOut(internal_414),
            FadeOut(cursor_2024),
            FadeOut(cursor_2024_label),
            FadeOut(index_checks),
            FadeOut(preanswer_note),
            a_badge.animate.move_to([-4.72, 0.02, 0]).scale(1.15),
            b_badge.animate.move_to([4.72, 0.02, 0]),
            run_time=0.75,
        )
        self.play(FadeIn(VGroup(ordered_pair[0], ordered_pair[1], ordered_pair[2], ordered_pair[4], ordered_pair[6])), run_time=0.55)

        self.next_beat("reveal_ordered_pair_digits")
        self.play(
            FadeIn(ordered_pair[3]),
            FadeIn(ordered_pair[5]),
            run_time=0.7,
        )
        self.play(Create(final_frame), FadeIn(reminder), run_time=0.65)
        self.play(Circumscribe(ordered_pair, color=REGION), run_time=0.6)
        self.wait(0.5)
