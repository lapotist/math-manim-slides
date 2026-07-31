"""Manim Slides lesson for ROC 112 TCFS mathematics gifted fill-in Q13."""

from __future__ import annotations

import colorsys
from collections import Counter

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
    Brace,
    Circle,
    Create,
    Dot,
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
    Write,
)
from manim.constants import DOWN, LEFT, RIGHT, UP


TOTAL_MEMBERS = 685
FOUNDERS_MIN = 6
ALLOWED_DIRECT_RECRUITS = (7, 14, 28, 35)
ALLOWED_OUTDEGREES = (0, *ALLOWED_DIRECT_RECRUITS)
SEVEN_PERSON_STEPS = (TOTAL_MEMBERS - FOUNDERS_MIN) // 7
ROOT_CANDIDATES = tuple(
    root_count
    for root_count in range(1, TOTAL_MEMBERS + 1)
    if (TOTAL_MEMBERS - root_count) % 7 == 0
)


def build_six_root_witness() -> tuple[
    tuple[tuple[int, tuple[int, ...]], ...], dict[int, int]
]:
    """Build the temporal 6-root, 97-step witness independently of the scene."""
    existing = set(range(FOUNDERS_MIN))
    used_recruiters: set[int] = set()
    events: list[tuple[int, tuple[int, ...]]] = []
    parent: dict[int, int] = {}
    recruiter = 0
    next_member = FOUNDERS_MIN

    for step in range(SEVEN_PERSON_STEPS):
        if recruiter not in existing:
            raise ValueError("a witness recruiter must already exist")
        if recruiter in used_recruiters:
            raise ValueError("the seven-person witness must use each recruiter once")
        children = tuple(range(next_member, next_member + 7))
        if existing.intersection(children):
            raise ValueError("a witness step must add seven new members")
        if any(child in parent for child in children):
            raise ValueError("a witness child cannot have two recommenders")
        for child in children:
            parent[child] = recruiter
        events.append((recruiter, children))
        used_recruiters.add(recruiter)
        existing.update(children)
        next_member += 7
        if step + 1 < SEVEN_PERSON_STEPS:
            recruiter = children[0]

    if existing != set(range(TOTAL_MEMBERS)):
        raise ValueError("the minimum witness must contain exactly 685 members")
    return tuple(events), parent


MIN_EVENTS, MIN_PARENT = build_six_root_witness()
MIN_OUTDEGREES = Counter(MIN_PARENT.values())
MIN_ROOT_SET = set(range(TOTAL_MEMBERS)).difference(MIN_PARENT)
MIN_ROOT_OF: dict[int, int] = {}
for member in range(TOTAL_MEMBERS):
    if member in MIN_ROOT_SET:
        MIN_ROOT_OF[member] = member
    else:
        MIN_ROOT_OF[member] = MIN_ROOT_OF[MIN_PARENT[member]]


def founder_color(index: int) -> str:
    """Return a deterministic distinct bright color for the all-founder witness."""
    hue = ((index * 257) % TOTAL_MEMBERS) / TOTAL_MEMBERS
    red, green, blue = colorsys.hsv_to_rgb(hue, 0.72, 0.96)
    return f"#{round(red * 255):02X}{round(green * 255):02X}{round(blue * 255):02X}"


ALL_FOUNDER_COLORS = tuple(founder_color(index) for index in range(TOTAL_MEMBERS))

if TOTAL_MEMBERS != 7 * 97 + 6:
    raise ValueError("685 must leave remainder 6 on division by 7")
if any(value % 7 for value in ALLOWED_DIRECT_RECRUITS):
    raise ValueError("every positive allowed outdegree must be divisible by 7")
if ROOT_CANDIDATES[0] != FOUNDERS_MIN or ROOT_CANDIDATES[-1] != TOTAL_MEMBERS:
    raise ValueError("the root candidate endpoints changed")
if len(ROOT_CANDIDATES) != 98:
    raise ValueError("the complete positive root candidate universe changed")
if len(MIN_EVENTS) != SEVEN_PERSON_STEPS or SEVEN_PERSON_STEPS != 97:
    raise ValueError("the minimum witness must use exactly 97 recruitment steps")
if len(MIN_PARENT) != TOTAL_MEMBERS - FOUNDERS_MIN:
    raise ValueError("every nonroot must have exactly one parent")
if MIN_ROOT_SET != set(range(FOUNDERS_MIN)):
    raise ValueError("the minimum witness must have roots 0 through 5")
if set(MIN_OUTDEGREES.values()) != {7} or len(MIN_OUTDEGREES) != 97:
    raise ValueError("exactly 97 witness members must recruit exactly seven")
if any(MIN_OUTDEGREES.get(member, 0) not in ALLOWED_OUTDEGREES for member in range(TOTAL_MEMBERS)):
    raise ValueError("the minimum witness has an illegal direct-recruit total")
if any(parent >= child for child, parent in MIN_PARENT.items()):
    raise ValueError("each witness parent must exist before its child")
if set(MIN_ROOT_OF.values()) != set(range(FOUNDERS_MIN)):
    raise ValueError("the minimum witness must induce exactly six badge colors")
if sum(MIN_OUTDEGREES.values()) != TOTAL_MEMBERS - FOUNDERS_MIN:
    raise ValueError("outdegrees must count every nonroot exactly once")
if len(ALL_FOUNDER_COLORS) != TOTAL_MEMBERS or len(set(ALL_FOUNDER_COLORS)) != TOTAL_MEMBERS:
    raise ValueError("the maximum witness must assign 685 distinct founder colors")


MIN_ROOT_COLORS = (BLUE, PURPLE, REGION, CORAL, POINT, "#E8A4C9")


class CarloTcfs112MathQ13(CarloSlide):
    """Count badge colors by counting roots, then attain both extrema."""

    lesson_id = "carlo.tcfs_112_math_gifted.q13"

    @staticmethod
    def title_change(old, new) -> Succession:
        return Succession(FadeOut(old), FadeIn(new))

    @staticmethod
    def stage_title(text: str, size: int = 30):
        title = label(text, size, INK, "BOLD")
        title.move_to([0, 3.18, 0])
        return title

    @staticmethod
    def member(color: str, radius: float = 0.20, *, founder: bool = False) -> VGroup:
        shell = Circle(
            radius=radius,
            color=color,
            stroke_width=2.7,
            fill_color=color,
            fill_opacity=0.18,
        )
        badge = Dot(radius=max(radius * 0.25, 0.035), color=color)
        parts = VGroup(shell, badge)
        if founder:
            halo = Circle(
                radius=radius + 0.075,
                color=POINT,
                stroke_width=2.5,
                fill_opacity=0,
            )
            parts.add(halo)
        return parts

    @classmethod
    def seven_row(
        cls,
        color: str,
        *,
        radius: float = 0.12,
        buff: float = 0.18,
    ) -> VGroup:
        return VGroup(*(cls.member(color, radius) for _ in range(7))).arrange(
            RIGHT, buff=buff
        )

    @classmethod
    def star_tree(
        cls,
        root_position: tuple[float, float, float],
        child_y: float,
        color: str,
        *,
        span: float = 2.8,
        root_radius: float = 0.25,
        child_radius: float = 0.13,
    ) -> VGroup:
        root = cls.member(color, root_radius, founder=True).move_to(root_position)
        child_xs = [
            root_position[0] - span / 2 + index * span / 6 for index in range(7)
        ]
        children = VGroup(
            *(
                cls.member(color, child_radius).move_to([x, child_y, 0])
                for x in child_xs
            )
        )
        edges = VGroup(
            *(
                Line(
                    root.get_center(),
                    child.get_center(),
                    buff=root_radius * 0.72,
                    color=color,
                    stroke_width=2.3,
                ).set_z_index(0)
                for child in children
            )
        )
        root.set_z_index(2)
        children.set_z_index(2)
        return VGroup(edges, root, children)

    @staticmethod
    def bundle_option(total: int, groups: int) -> VGroup:
        frame = RoundedRectangle(
            width=2.70,
            height=2.68,
            corner_radius=0.06,
            color=REGION,
            stroke_width=2.2,
            fill_color=REGION,
            fill_opacity=0.055,
        )
        total_tex = MathTex(str(total), font_size=40, color=INK)
        total_tex.move_to(frame.get_top() + DOWN * 0.39)
        rows = VGroup()
        for _ in range(groups):
            row = VGroup(*(Dot(radius=0.048, color=REGION) for _ in range(7)))
            row.arrange(RIGHT, buff=0.105)
            rows.add(row)
        rows.arrange(DOWN, buff=0.105)
        rows.move_to(frame.get_center() + UP * 0.03)
        factor = MathTex(
            rf"{groups}\cdot7", font_size=27, color=REGION
        ).move_to(frame.get_bottom() + UP * 0.35)
        return VGroup(frame, total_tex, rows, factor)

    @staticmethod
    def timeline_step(before: int, after: int, color: str) -> VGroup:
        left_value = MathTex(str(before), font_size=34, color=INK)
        right_value = MathTex(str(after), font_size=34, color=color)
        arrow = Arrow(
            LEFT * 0.62,
            RIGHT * 0.62,
            buff=0,
            color=REGION,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )
        plus = MathTex("+7", font_size=23, color=REGION).next_to(
            arrow, UP, buff=0.04
        )
        row = VGroup(left_value, VGroup(arrow, plus), right_value).arrange(
            RIGHT, buff=0.20
        )
        return row

    @staticmethod
    def all_founder_grid() -> VGroup:
        columns = 37
        x_start = -5.82
        x_step = 0.323
        y_start = 2.34
        y_step = 0.225
        dots = VGroup()
        for index, color in enumerate(ALL_FOUNDER_COLORS):
            row, column = divmod(index, columns)
            dots.add(
                Dot(
                    [x_start + column * x_step, y_start - row * y_step, 0],
                    radius=0.047,
                    color=color,
                )
            )
        return dots

    def construct(self) -> None:
        heading = label("第 13 題｜認證顏色藏在哪裡？", 27, MUTED, "BOLD")
        heading.to_corner(UP + LEFT, buff=0.36)
        source = label(
            "解題來源：正哥愛數學｜PDF 第 13 頁｜影片 nEbzWC6QD7g 00:00-02:55.00",
            15,
            MUTED,
            "MEDIUM",
        )
        source.to_corner(DOWN + RIGHT, buff=0.22)

        # Beat 01 grow_first_seven_children: grow one exact direct-recruit bundle.
        self.begin_beat("grow_first_seven_children")
        stage_title = self.stage_title("一位創社社員，先推薦恰好 7 個人")
        root = self.member(BLUE, 0.32, founder=True).move_to([-3.75, 1.45, 0])
        children_one = self.seven_row(BLUE, radius=0.16, buff=0.24)
        children_one.move_to([-3.75, -0.15, 0])
        edges_one = VGroup(
            *(
                Line(
                    root.get_center(),
                    child.get_center(),
                    buff=0.27,
                    color=BLUE,
                    stroke_width=2.8,
                ).set_z_index(0)
                for child in children_one
            )
        )
        tree_one = VGroup(edges_one, root, children_one)
        root_caption = label("創社社員", 24, POINT, "BOLD").next_to(
            root, UP, buff=0.18
        )
        child_brace = Brace(children_one, DOWN, color=REGION, buff=0.16)
        child_count = label("直接推薦 7 人", 24, REGION, "BOLD").next_to(
            child_brace, DOWN, buff=0.12
        )
        direct_note = label(
            "只數直接相連的人，不把後代算進來", 26, MUTED, "MEDIUM"
        )
        direct_note.move_to([3.25, 0.32, 0])
        allowed_note = label("曾推薦者：7、14、28 或 35 人", 27, INK, "BOLD")
        allowed_note.move_to([3.25, -0.45, 0])
        seven_focus = SurroundingRectangle(
            allowed_note,
            color=REGION,
            stroke_width=2.2,
            buff=0.15,
            corner_radius=0.05,
        )

        self.add(heading, source)
        self.play(FadeIn(stage_title), run_time=0.48)
        self.play(GrowFromCenter(root), FadeIn(root_caption), run_time=0.58)
        self.play(
            LaggedStart(*(Create(edge) for edge in edges_one), lag_ratio=0.08),
            run_time=0.86,
        )
        self.play(
            LaggedStart(
                *(GrowFromCenter(child) for child in children_one), lag_ratio=0.10
            ),
            run_time=1.02,
        )

        # Beat 02 grow_seven_branch: continue at a settled semantic boundary.
        self.next_beat("grow_seven_branch")
        self.play(
            Create(child_brace),
            FadeIn(child_count),
            FadeIn(direct_note),
            FadeIn(allowed_note),
            run_time=0.68,
        )
        self.play(Create(seven_focus), run_time=0.40)
        self.wait(0.42)

        # Beat 03 grow_second_generation: retain one child and pass blue downward.
        self.next_beat("grow_second_generation")
        next_title = self.stage_title("同一種認證顏色，沿推薦邊傳到下一層")
        active_child = children_one[3]
        active_ring = Circle(
            radius=0.25, color=REGION, stroke_width=3.0, fill_opacity=0
        ).move_to(active_child)
        children_two = self.seven_row(BLUE, radius=0.135, buff=0.20)
        children_two.move_to([-3.75, -1.67, 0])
        edges_two = VGroup(
            *(
                Line(
                    active_child.get_center(),
                    child.get_center(),
                    buff=0.22,
                    color=BLUE,
                    stroke_width=2.5,
                ).set_z_index(0)
                for child in children_two
            )
        )
        sender = self.member(BLUE, 0.24).move_to([2.25, 0.45, 0])
        receiver = self.member(BLUE, 0.24).move_to([4.65, 0.45, 0])
        pass_arrow = Arrow(
            sender.get_right(),
            receiver.get_left(),
            buff=0.12,
            color=BLUE,
            stroke_width=3.0,
            max_tip_length_to_length_ratio=0.18,
        )
        sender_text = label("推薦人", 22, MUTED, "MEDIUM").next_to(
            sender, DOWN, buff=0.16
        )
        receiver_text = label("新社員", 22, MUTED, "MEDIUM").next_to(
            receiver, DOWN, buff=0.16
        )
        inheritance = label("推薦人與新社員同色", 28, BLUE, "BOLD")
        inheritance.move_to([3.45, -0.65, 0])
        branch_note = label("整個分支都保留根的顏色", 27, INK, "BOLD")
        branch_note.move_to([3.45, -1.47, 0])
        pass_demo = VGroup(
            sender,
            receiver,
            pass_arrow,
            sender_text,
            receiver_text,
            inheritance,
            branch_note,
        )
        second_generation = VGroup(edges_two, children_two, active_ring, pass_demo)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(direct_note),
            FadeOut(allowed_note),
            FadeOut(seven_focus),
            run_time=0.58,
        )
        stage_title = next_title
        self.play(Create(active_ring), Indicate(active_child, color=REGION), run_time=0.58)
        self.play(
            LaggedStart(*(Create(edge) for edge in edges_two), lag_ratio=0.07),
            run_time=0.78,
        )
        self.play(
            LaggedStart(
                *(GrowFromCenter(child) for child in children_two), lag_ratio=0.08
            ),
            run_time=0.92,
        )

        # Beat 04 pass_color_forward: continue at a settled semantic boundary.
        self.next_beat("pass_color_forward")
        self.play(FadeIn(sender), FadeIn(sender_text), run_time=0.36)
        self.play(Create(pass_arrow), FadeIn(receiver), FadeIn(receiver_text), run_time=0.52)
        self.play(FadeIn(inheritance), FadeIn(branch_note), run_time=0.54)
        self.wait(0.42)

        # Beat 05 compare_two_colored_trees: compare two exact rooted stars.
        self.next_beat("compare_two_colored_trees")
        next_title = self.stage_title("新顏色只從另一位創社社員開始")
        compact_blue = self.star_tree((-3.60, 1.25, 0), -0.20, BLUE, span=3.1)
        purple_tree = self.star_tree((3.60, 1.25, 0), -0.20, PURPLE, span=3.1)
        blue_root_tag = label("根 1", 23, POINT, "BOLD").next_to(
            compact_blue[1], UP, buff=0.17
        )
        purple_root_tag = label("根 2", 23, POINT, "BOLD").next_to(
            purple_tree[1], UP, buff=0.17
        )
        blue_tree_tag = label("樹內都是藍色", 24, BLUE, "BOLD")
        blue_tree_tag.move_to([-3.60, -1.15, 0])
        purple_tree_tag = label("樹內都是紫色", 24, PURPLE, "BOLD")
        purple_tree_tag.move_to([3.60, -1.15, 0])
        root_equivalence = label(
            "顏色種數 ＝ 創社社員人數 ＝ 根數", 33, INK, "BOLD",
            t2c={"顏色種數": REGION, "根數": POINT},
        )
        root_equivalence.move_to([0, -2.35, 0])
        root_symbol = MathTex("r", font_size=45, color=POINT).next_to(
            root_equivalence, DOWN, buff=0.15
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(root_caption),
            FadeOut(child_brace),
            FadeOut(child_count),
            FadeOut(second_generation),
            Transform(tree_one, compact_blue),
            run_time=0.82,
        )
        stage_title = next_title
        self.play(FadeIn(blue_root_tag), FadeIn(blue_tree_tag), run_time=0.42)
        self.play(Create(purple_tree[0]), GrowFromCenter(purple_tree[1]), run_time=0.68)
        self.play(
            LaggedStart(
                *(GrowFromCenter(child) for child in purple_tree[2]), lag_ratio=0.08
            ),
            FadeIn(purple_root_tag),
            run_time=0.90,
        )

        # Beat 06 equate_colors_and_roots: continue at a settled semantic boundary.
        self.next_beat("equate_colors_and_roots")
        self.play(FadeIn(purple_tree_tag), run_time=0.34)
        self.play(FadeIn(root_equivalence), Write(root_symbol), run_time=0.66)
        self.wait(0.46)

        # Beat 07 count_unique_incoming_edges: count unique parents before writing a sum.
        self.next_beat("count_unique_incoming_edges")
        next_title = self.stage_title("把 685 人拆成根與非根，再數所有推薦邊")
        mini_blue = self.star_tree((-5.05, 1.05, 0), -0.20, BLUE, span=2.1, root_radius=0.20, child_radius=0.095)
        mini_purple = self.star_tree((-2.35, 1.05, 0), -0.20, PURPLE, span=2.1, root_radius=0.20, child_radius=0.095)
        unique_edge_note = label("每位非根社員恰有一條入邊", 24, REGION, "BOLD")
        unique_edge_note.move_to([-3.70, -1.20, 0])

        root_icon = self.member(POINT, 0.24, founder=True)
        root_count = MathTex("r", font_size=42, color=POINT)
        root_text = label("位根", 25, POINT, "BOLD")
        root_part = VGroup(root_icon, root_count, root_text).arrange(RIGHT, buff=0.20)

        nonroot_icons = VGroup(
            self.member(BLUE, 0.16),
            self.member(PURPLE, 0.16),
            self.member(REGION, 0.16),
        ).arrange(RIGHT, buff=0.10)
        nonroot_count = MathTex("685-r", font_size=42, color=REGION)
        nonroot_text = label("位非根", 25, REGION, "BOLD")
        nonroot_part = VGroup(nonroot_icons, nonroot_count, nonroot_text).arrange(
            RIGHT, buff=0.20
        )
        split_group = VGroup(root_part, nonroot_part).arrange(DOWN, buff=0.58)
        split_group.move_to([3.25, 0.58, 0])
        split_total = MathTex("685", font_size=48, color=INK).next_to(
            split_group, UP, buff=0.42
        )
        split_group.add(split_total)

        degree_relation = MathTex(
            "685-r", "=", r"\sum_v d(v)", font_size=45, color=INK
        )
        degree_relation[0].set_color(REGION)
        degree_relation.move_to([2.75, -1.35, 0])
        degree_note = label("右邊：每個人的直接推薦總數", 23, MUTED, "MEDIUM")
        degree_note.next_to(degree_relation, DOWN, buff=0.20)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(blue_root_tag),
            FadeOut(purple_root_tag),
            FadeOut(blue_tree_tag),
            FadeOut(purple_tree_tag),
            FadeOut(root_equivalence),
            FadeOut(root_symbol),
            Transform(tree_one, mini_blue),
            Transform(purple_tree, mini_purple),
            run_time=0.82,
        )
        stage_title = next_title
        all_edges = [*tree_one[0], *purple_tree[0]]
        self.play(
            LaggedStart(
                *(Indicate(edge, color=REGION, scale_factor=1.03) for edge in all_edges),
                lag_ratio=0.045,
            ),
            FadeIn(unique_edge_note),
            run_time=1.18,
        )
        self.play(FadeIn(root_part), FadeIn(split_total), run_time=0.45)

        # Beat 08 count_each_nonroot: continue at a settled semantic boundary.
        self.next_beat("count_each_nonroot")
        self.play(FadeIn(nonroot_part), run_time=0.48)
        self.play(Write(degree_relation), FadeIn(degree_note), run_time=0.68)
        self.wait(0.44)

        # Beat 09 compress_recruitment_bundles: display every allowed multiple.
        self.next_beat("compress_recruitment_bundles")
        next_title = self.stage_title("四種推薦人數，都由完整的七人列組成")
        bundle_options = VGroup(
            self.bundle_option(7, 1),
            self.bundle_option(14, 2),
            self.bundle_option(28, 4),
            self.bundle_option(35, 5),
        ).arrange(RIGHT, buff=0.30)
        bundle_options.move_to([0, 0.38, 0])
        allowed_formula = MathTex(
            "d(v)",
            r"\in",
            r"\{0,7,14,28,35\}",
            "=",
            "7",
            r"\{0,1,2,4,5\}",
            font_size=36,
            color=INK,
        )
        allowed_formula[0].set_color(BLUE)
        allowed_formula[4].set_color(REGION)
        allowed_formula[5].set_color(REGION)
        allowed_formula.move_to([0, -2.00, 0])
        zero_note = label("沒有推薦過的人，直接推薦數是 0", 24, MUTED, "MEDIUM")
        zero_note.next_to(allowed_formula, DOWN, buff=0.20)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(tree_one),
            FadeOut(purple_tree),
            FadeOut(unique_edge_note),
            FadeOut(split_group),
            FadeOut(degree_relation),
            FadeOut(degree_note),
            run_time=0.72,
        )
        stage_title = next_title
        self.play(
            LaggedStart(
                *(FadeIn(option, shift=UP * 0.10) for option in bundle_options),
                lag_ratio=0.18,
            ),
            run_time=1.12,
        )
        self.play(Write(allowed_formula), FadeIn(zero_note), run_time=0.72)
        self.wait(0.44)

        # Beat 10 write_recruitment_multiple: derive the complete congruence candidate list.
        self.next_beat("write_recruitment_multiple")
        next_title = self.stage_title("所有非根社員的總數，必須是 7 的倍數")
        bundle_target = bundle_options.copy().scale(0.47)
        bundle_target.arrange(RIGHT, buff=0.22).move_to([0, 2.04, 0])
        multiple_note = label("每一份都含完整七人列", 23, REGION, "BOLD")
        multiple_note.move_to([0, 1.18, 0])
        count_equation = MathTex(
            "685", "-", "r", "=", "7K", font_size=47, color=INK
        )
        count_equation[2].set_color(POINT)
        count_equation[4].set_color(REGION)
        count_equation.move_to([0, 0.55, 0])
        division = MathTex(
            "685", "=", "7", r"\cdot", "97", "+", "6",
            font_size=40,
            color=INK,
        )
        division[2].set_color(REGION)
        division[6].set_color(CORAL)
        division.move_to([0, -0.28, 0])
        congruence = MathTex(
            "r", r"\equiv", "6", r"\pmod 7", font_size=45, color=INK
        )
        congruence[0].set_color(POINT)
        congruence[2].set_color(CORAL)
        congruence.move_to([0, -1.12, 0])
        candidates_label = label("正整數候選", 23, MUTED, "MEDIUM")
        candidates = MathTex(
            "6", ",", "13", ",", "20", ",", r"\ldots", ",", "685",
            font_size=38,
            color=INK,
        )
        candidates[0].set_color(CORAL)
        candidates[-1].set_color(POINT)
        candidate_group = VGroup(candidates_label, candidates).arrange(
            DOWN, buff=0.12
        )
        candidate_group.move_to([0, -2.20, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(allowed_formula),
            FadeOut(zero_note),
            Transform(bundle_options, bundle_target),
            run_time=0.72,
        )
        stage_title = next_title
        self.play(FadeIn(multiple_note), Write(count_equation), run_time=0.62)

        # Beat 11 earn_mod_seven: continue at a settled semantic boundary.
        self.next_beat("earn_mod_seven")
        self.play(Write(division), run_time=0.58)
        self.play(Write(congruence), run_time=0.58)
        self.play(FadeIn(candidate_group), run_time=0.62)
        self.wait(0.50)

        # Beat 12 pause_before_feasibility: hold six as a question, not an answer.
        self.next_beat("pause_before_feasibility")
        next_title = self.stage_title("先停住：餘數只給必要條件")
        six_question = MathTex("r", "=", "6", "?", font_size=76, color=INK)
        six_question[0].set_color(POINT)
        six_question[2].set_color(CORAL)
        six_question[3].set_color(CORAL)
        six_question.move_to([0, 0.48, 0])
        necessity = label("1 到 5 不可能，但 6 還沒有被造出來", 30, CORAL, "BOLD")
        necessity.move_to([0, -0.72, 0])
        timing_question = label(
            "能否從 6 位根出發，依時間順序加入 97 組七人？",
            28,
            INK,
            "BOLD",
        )
        timing_question.move_to([0, -1.58, 0])
        caution = label("必要條件 ≠ 可行構造", 24, MUTED, "MEDIUM")
        caution.move_to([0, -2.24, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(bundle_options),
            FadeOut(multiple_note),
            FadeOut(count_equation),
            FadeOut(division),
            FadeOut(congruence),
            FadeOut(candidate_group),
            run_time=0.66,
        )
        stage_title = next_title
        self.play(FadeIn(six_question), run_time=0.55)
        self.play(FadeIn(necessity), run_time=0.48)
        self.play(FadeIn(timing_question), FadeIn(caution), run_time=0.60)
        self.wait(0.86)

        # Beat 13 plant_six_founders: establish the exact initial witness state.
        self.next_beat("plant_six_founders")
        next_title = self.stage_title("先放 6 位創社社員，六種顏色各有一個根")
        founders = VGroup(
            *(
                self.member(color, 0.34, founder=True)
                for color in MIN_ROOT_COLORS
            )
        ).arrange(RIGHT, buff=0.82)
        founders.move_to([0, 0.38, 0])
        founder_label = label("六位都在一開始加入", 28, INK, "BOLD")
        founder_label.move_to([0, 1.58, 0])
        total_text = label("社員", 25, MUTED, "MEDIUM")
        total_value = MathTex("6", font_size=43, color=INK)
        color_text = label("顏色", 25, MUTED, "MEDIUM")
        color_value = MathTex("6", font_size=43, color=POINT)
        count_divider = Line(DOWN * 0.32, UP * 0.32, color=HAIRLINE, stroke_width=2)
        initial_counts = VGroup(
            total_text, total_value, count_divider, color_text, color_value
        ).arrange(RIGHT, buff=0.26)
        initial_counts.move_to([0, -1.10, 0])
        first_active = Circle(
            radius=0.49, color=REGION, stroke_width=3.2, fill_opacity=0
        ).move_to(founders[0])
        first_note = label("第一位先接下推薦任務", 26, REGION, "BOLD")
        first_note.move_to([0, -2.02, 0])
        founder_group = VGroup(founders, founder_label, initial_counts, first_active, first_note)

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(six_question),
            FadeOut(necessity),
            FadeOut(timing_question),
            FadeOut(caution),
            run_time=0.62,
        )
        stage_title = next_title
        self.play(FadeIn(founder_label), run_time=0.38)
        self.play(
            LaggedStart(
                *(GrowFromCenter(founder) for founder in founders), lag_ratio=0.15
            ),
            run_time=1.02,
        )

        # Beat 14 activate_first_founder: continue at a settled semantic boundary.
        self.next_beat("activate_first_founder")
        self.play(FadeIn(initial_counts), run_time=0.50)
        self.play(Create(first_active), FadeIn(first_note), run_time=0.55)
        self.wait(0.44)

        # Beat 15 show_first_recruitment_step: show two temporal steps, then compress.
        self.next_beat("show_first_recruitment_step")
        next_title = self.stage_title("每次由一位既有新人接力，恰好再加入 7 人", 29)
        founders_target = founders.copy().scale(0.62).move_to([-3.60, 2.10, 0])
        active_target = Circle(
            radius=0.34, color=REGION, stroke_width=3.0, fill_opacity=0
        ).move_to(founders_target[0])
        first_children = self.seven_row(BLUE, radius=0.115, buff=0.19)
        first_children.move_to([-4.10, 0.98, 0])
        first_edges = VGroup(
            *(
                Line(
                    founders_target[0].get_center(),
                    child.get_center(),
                    buff=0.18,
                    color=BLUE,
                    stroke_width=2.2,
                )
                for child in first_children
            )
        )
        chosen_child = first_children[3]
        chosen_ring = Circle(
            radius=0.19, color=REGION, stroke_width=2.6, fill_opacity=0
        ).move_to(chosen_child)
        second_children = self.seven_row(BLUE, radius=0.105, buff=0.18)
        second_children.move_to([-4.10, -0.18, 0])
        second_edges = VGroup(
            *(
                Line(
                    chosen_child.get_center(),
                    child.get_center(),
                    buff=0.17,
                    color=BLUE,
                    stroke_width=2.0,
                )
                for child in second_children
            )
        )
        step_one_tag = label("第 1 步", 21, REGION, "BOLD").move_to([-6.08, 1.02, 0])
        step_two_tag = label("第 2 步", 21, REGION, "BOLD").move_to([-6.08, -0.18, 0])
        relay_note = label(
            "下一位推薦人來自剛加入、尚未推薦的七人",
            23,
            MUTED,
            "MEDIUM",
        )
        relay_note.move_to([-4.10, -1.03, 0])

        timeline_one = self.timeline_step(6, 13, BLUE).move_to([3.55, 1.35, 0])
        timeline_two = self.timeline_step(13, 20, BLUE).move_to([3.55, 0.30, 0])
        timeline_dots = MathTex(r"\vdots", font_size=37, color=MUTED).move_to(
            [3.55, -0.52, 0]
        )
        timeline_final = self.timeline_step(678, 685, POINT).move_to(
            [3.55, -1.34, 0]
        )
        final_step_tag = label("第 97 步", 21, REGION, "BOLD").next_to(
            timeline_final, RIGHT, buff=0.18
        )
        witness_equation = MathTex(
            "6", "+", "97", r"\cdot", "7", "=", "685",
            font_size=48,
            color=INK,
        )
        witness_equation[0].set_color(POINT)
        witness_equation[2].set_color(REGION)
        witness_equation[4].set_color(REGION)
        witness_equation[6].set_color(POINT)
        witness_equation.move_to([0, -2.30, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(founder_label),
            FadeOut(initial_counts),
            FadeOut(first_note),
            run_time=0.50,
        )
        stage_title = next_title
        self.play(
            Transform(founders, founders_target),
            Transform(first_active, active_target),
            run_time=0.58,
        )
        self.play(
            Create(first_edges),
            LaggedStart(
                *(GrowFromCenter(child) for child in first_children), lag_ratio=0.07
            ),
            FadeIn(step_one_tag),
            run_time=0.92,
        )
        self.play(FadeIn(timeline_one), Create(chosen_ring), run_time=0.52)

        # Beat 16 show_second_recruitment_step: continue at a settled semantic boundary.
        self.next_beat("show_second_recruitment_step")
        self.play(
            Create(second_edges),
            LaggedStart(
                *(GrowFromCenter(child) for child in second_children), lag_ratio=0.07
            ),
            FadeIn(step_two_tag),
            run_time=0.90,
        )
        self.play(FadeIn(timeline_two), FadeIn(relay_note), run_time=0.50)
        self.play(FadeIn(timeline_dots), run_time=0.34)

        # Beat 17 repeat_ninety_seven_steps: continue at a settled semantic boundary.
        self.next_beat("repeat_ninety_seven_steps")
        self.play(FadeIn(timeline_final), FadeIn(final_step_tag), run_time=0.60)
        self.play(Write(witness_equation), run_time=0.72)
        self.wait(0.52)

        witness_visual = VGroup(
            founders,
            first_active,
            first_children,
            first_edges,
            second_children,
            second_edges,
            chosen_ring,
            step_one_tag,
            step_two_tag,
            relay_note,
            timeline_one,
            timeline_two,
            timeline_dots,
            timeline_final,
            final_step_tag,
            witness_equation,
        )

        # Beat 18 compare_necessary_and_feasible: combine necessity with the explicit witness.
        self.next_beat("compare_necessary_and_feasible")
        next_title = self.stage_title("不能少於 6，而且六根森林確實做得到")
        divider = Line([0, -0.90, 0], [0, 2.05, 0], color=HAIRLINE, stroke_width=2.0)
        necessary_title = label("必要下界", 27, CORAL, "BOLD")
        necessary_equation = MathTex(
            "r", r"\equiv", "6", r"\pmod 7", font_size=42, color=INK
        )
        necessary_equation[0].set_color(POINT)
        necessary_equation[2].set_color(CORAL)
        necessary_result = MathTex("r", r"\ge", "6", font_size=46, color=INK)
        necessary_result[0].set_color(POINT)
        necessary_result[2].set_color(CORAL)
        necessary_group = VGroup(
            necessary_title, necessary_equation, necessary_result
        ).arrange(DOWN, buff=0.42)
        necessary_group.move_to([-3.65, 0.58, 0])

        feasible_title = label("可行構造", 27, REGION, "BOLD")
        feasible_equation = MathTex(
            "6", "+", "97", r"\cdot", "7", "=", "685",
            font_size=40,
            color=INK,
        )
        feasible_equation[0].set_color(POINT)
        feasible_equation[2].set_color(REGION)
        feasible_check = label("六個根｜每位推薦者恰推 7 人", 25, REGION, "BOLD")
        feasible_group = VGroup(
            feasible_title, feasible_equation, feasible_check
        ).arrange(DOWN, buff=0.42)
        feasible_group.move_to([3.65, 0.58, 0])
        left_arrow = Arrow(
            [-2.65, -0.83, 0],
            [-0.78, -1.58, 0],
            buff=0.08,
            color=CORAL,
            stroke_width=3,
        )
        right_arrow = Arrow(
            [2.65, -0.83, 0],
            [0.78, -1.58, 0],
            buff=0.08,
            color=REGION,
            stroke_width=3,
        )
        p_result = MathTex("p", "=", "6", font_size=62, color=INK)
        p_result[0].set_color(POINT)
        p_result[2].set_color(POINT)
        p_result.move_to([0, -2.10, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(witness_visual),
            FadeIn(divider),
            run_time=0.68,
        )
        stage_title = next_title
        self.play(FadeIn(necessary_group), run_time=0.58)
        self.play(FadeIn(feasible_group), run_time=0.58)

        # Beat 19 certify_minimum: continue at a settled semantic boundary.
        self.next_beat("certify_minimum")
        self.play(Create(left_arrow), Create(right_arrow), run_time=0.50)
        self.play(Write(p_result), run_time=0.66)
        self.wait(0.48)

        minimum_certificate = VGroup(
            divider,
            necessary_group,
            feasible_group,
            left_arrow,
            right_arrow,
            p_result,
        )

        # Beat 20 count_possible_root_colors: establish the separate upper bound.
        self.next_beat("count_possible_root_colors")
        next_title = self.stage_title("最大值另問：每種顏色都要占用一位根")
        sample_colors = tuple(ALL_FOUNDER_COLORS[index] for index in range(0, 603, 75))
        sample_roots = VGroup(
            *(self.member(color, 0.27, founder=True) for color in sample_colors)
        ).arrange(RIGHT, buff=0.55)
        sample_roots.move_to([0, 0.95, 0])
        colors_caption = label("不同顏色，各有一位創社社員", 27, INK, "BOLD")
        colors_caption.move_to([0, 1.88, 0])
        root_brace = Brace(sample_roots, DOWN, color=POINT, buff=0.18)
        root_symbol_bound = MathTex("r", font_size=40, color=POINT).next_to(
            root_brace, DOWN, buff=0.12
        )
        subset_note = label("創社社員也包含在全體 685 人之內", 27, MUTED, "MEDIUM")
        subset_note.move_to([0, -0.78, 0])
        root_bound = MathTex("r", r"\le", "685", font_size=49, color=INK)
        root_bound[0].set_color(POINT)
        root_bound[2].set_color(INK)
        root_bound.move_to([0, -1.52, 0])
        q_bound = MathTex("q", r"\le", "685", font_size=53, color=INK)
        q_bound[0].set_color(PURPLE)
        q_bound.move_to([0, -2.33, 0])
        upper_bound_group = VGroup(
            sample_roots,
            colors_caption,
            root_brace,
            root_symbol_bound,
            subset_note,
            root_bound,
            q_bound,
        )

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(minimum_certificate),
            run_time=0.64,
        )
        stage_title = next_title
        self.play(FadeIn(colors_caption), run_time=0.36)
        self.play(
            LaggedStart(
                *(GrowFromCenter(root_node) for root_node in sample_roots),
                lag_ratio=0.10,
            ),
            run_time=0.88,
        )
        self.play(Create(root_brace), Write(root_symbol_bound), run_time=0.48)

        # Beat 21 bound_color_count: continue at a settled semantic boundary.
        self.next_beat("bound_color_count")
        self.play(FadeIn(subset_note), Write(root_bound), run_time=0.58)
        self.play(Write(q_bound), run_time=0.54)
        self.wait(0.46)

        # Beat 22 show_all_founders: render all 685 distinct roots and no edges.
        self.next_beat("show_all_founders")
        next_title = self.stage_title("讓 685 人全都是創社社員：沒有任何推薦邊")
        all_founders = self.all_founder_grid()
        all_founder_caption = label("685 位，全部在一開始加入", 27, INK, "BOLD")
        all_founder_caption.move_to([0, -2.02, 0])
        edge_label = label("推薦邊", 24, MUTED, "MEDIUM")
        edge_value = MathTex("0", font_size=38, color=REGION)
        edge_zero = VGroup(edge_label, edge_value).arrange(RIGHT, buff=0.18)
        edge_zero.move_to([-3.65, -2.62, 0])
        vacuous_note = label("沒有人曾推薦；條件沒有違反者", 25, REGION, "BOLD")
        vacuous_note.move_to([1.72, -2.62, 0])
        q_result = MathTex("q", "=", "685", font_size=55, color=INK)
        q_result[0].set_color(PURPLE)
        q_result[2].set_color(POINT)
        q_result.move_to([0, -3.24, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(upper_bound_group),
            run_time=0.64,
        )
        stage_title = next_title
        self.play(FadeIn(all_founders, shift=UP * 0.08), run_time=1.10)
        self.play(FadeIn(all_founder_caption), run_time=0.44)

        # Beat 23 realize_all_founders: continue at a settled semantic boundary.
        self.next_beat("realize_all_founders")
        self.play(FadeIn(edge_zero), FadeIn(vacuous_note), run_time=0.56)
        self.play(Write(q_result), run_time=0.62)
        self.wait(0.52)

        maximum_witness = VGroup(
            all_founders,
            all_founder_caption,
            edge_zero,
            vacuous_note,
            q_result,
        )

        # Beat 24 place_minimum_and_maximum_witnesses: settle both witnesses before the pair.
        self.next_beat("place_minimum_and_maximum_witnesses")
        next_title = self.stage_title("兩個極端都完成構造，最後才合成數對")
        final_divider = Line([0, -1.18, 0], [0, 2.18, 0], color=HAIRLINE, stroke_width=2)

        final_min_roots = VGroup(
            *(
                self.member(color, 0.17, founder=True)
                for color in MIN_ROOT_COLORS
            )
        ).arrange(RIGHT, buff=0.24)
        final_min_roots.move_to([-3.75, 1.48, 0])
        mini_seven = VGroup(*(Dot(radius=0.055, color=BLUE) for _ in range(7)))
        mini_seven.arrange(RIGHT, buff=0.10).move_to([-3.75, 0.68, 0])
        mini_edges = VGroup(
            *(
                Line(
                    final_min_roots[0].get_center(),
                    dot.get_center(),
                    buff=0.16,
                    color=BLUE,
                    stroke_width=1.8,
                )
                for dot in mini_seven
            )
        )
        min_repeat = label("同一規則接力 97 步", 22, REGION, "BOLD")
        min_repeat.move_to([-3.75, 0.06, 0])
        min_formula = MathTex(
            "6", "+", "97", r"\cdot", "7", "=", "685",
            font_size=34,
            color=INK,
        ).move_to([-3.75, -0.52, 0])
        final_p = MathTex("p", "=", "6", font_size=48, color=INK)
        final_p[0].set_color(POINT)
        final_p[2].set_color(POINT)
        final_p.move_to([-3.75, -1.12, 0])
        min_summary = VGroup(
            final_min_roots,
            mini_edges,
            mini_seven,
            min_repeat,
            min_formula,
            final_p,
        )

        max_summary_dots = VGroup()
        for index in range(60):
            row, column = divmod(index, 10)
            max_summary_dots.add(
                Dot(
                    [2.65 + column * 0.25, 1.85 - row * 0.25, 0],
                    radius=0.045,
                    color=ALL_FOUNDER_COLORS[index * 11],
                )
            )
        max_caption = label("685 個根｜0 條推薦邊", 25, REGION, "BOLD")
        max_caption.move_to([3.78, 0.02, 0])
        final_q = MathTex("q", "=", "685", font_size=48, color=INK)
        final_q[0].set_color(PURPLE)
        final_q[2].set_color(POINT)
        final_q.move_to([3.78, -1.12, 0])
        max_summary = VGroup(max_summary_dots, max_caption, final_q)

        final_pair = MathTex(
            "(p,q)", "=", "(6,685)", font_size=58, color=INK
        )
        final_pair[0].set_color(MUTED)
        final_pair[2].set_color(POINT)
        final_pair.move_to([0, -2.15, 0])
        pair_frame = SurroundingRectangle(
            final_pair,
            color=POINT,
            stroke_width=2.7,
            buff=0.20,
            corner_radius=0.06,
        )
        realization = label(
            "七的倍數控制非根；創社社員決定顏色",
            25,
            INK,
            "BOLD",
            t2c={"七的倍數": REGION, "創社社員": POINT},
        )
        realization.move_to([0, -3.05, 0])

        self.play(
            self.title_change(stage_title, next_title),
            FadeOut(maximum_witness),
            FadeIn(final_divider),
            run_time=0.66,
        )
        self.play(
            FadeIn(final_min_roots),
            Create(mini_edges),
            FadeIn(mini_seven),
            run_time=0.66,
        )
        self.play(FadeIn(min_repeat), Write(min_formula), Write(final_p), run_time=0.65)
        self.play(FadeIn(max_summary_dots), FadeIn(max_caption), run_time=0.62)

        # Beat 25 reveal_extreme_pair: continue at a settled semantic boundary.
        self.next_beat("reveal_extreme_pair")
        self.play(Write(final_q), run_time=0.48)
        self.play(Write(final_pair), Create(pair_frame), run_time=0.72)
        self.play(FadeIn(realization), run_time=0.52)
        self.wait(0.72)
