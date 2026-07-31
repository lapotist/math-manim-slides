#!/usr/bin/env python3
"""Report presentation segments that contain too many animation phases."""

from __future__ import annotations

import argparse
import ast
import sys
import tomllib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MAX_PLAY_CALLS_PER_SEGMENT = 4


def _self_call_name(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
        return None
    owner = node.func.value
    if not isinstance(owner, ast.Name) or owner.id != "self":
        return None
    return node.func.attr


def _integer_constant(node: ast.AST) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if (
        isinstance(node, ast.UnaryOp)
        and isinstance(node.op, ast.USub)
        and isinstance(node.operand, ast.Constant)
        and isinstance(node.operand.value, int)
    ):
        return -node.operand.value
    return None


def _iteration_count(node: ast.AST) -> int | None:
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return len(node.elts)
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
        if node.func.id == "range" and not node.keywords:
            values = [_integer_constant(argument) for argument in node.args]
            if all(value is not None for value in values) and 1 <= len(values) <= 3:
                return len(range(*values))  # type: ignore[arg-type]
        if node.func.id == "enumerate" and node.args:
            return _iteration_count(node.args[0])
        if node.func.id == "zip" and node.args:
            counts = [_iteration_count(argument) for argument in node.args]
            if all(count is not None for count in counts):
                return min(counts)  # type: ignore[arg-type]
    return None


def _block_events(statements: list[ast.stmt]) -> list[tuple[int, int, str]]:
    events: list[tuple[int, int, str]] = []
    for statement in statements:
        if isinstance(statement, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        if isinstance(statement, (ast.For, ast.AsyncFor)):
            body = _block_events(statement.body)
            repetitions = _iteration_count(statement.iter)
            if repetitions is None and any(
                name in {"begin_beat", "next_beat", "next_slide", "play"}
                for _, _, name in body
            ):
                raise ValueError(
                    f"cannot determine animation-loop length at line {statement.lineno}"
                )
            repetitions = repetitions if repetitions is not None else 1
            if repetitions > 1 and any(
                name in {"begin_beat", "next_beat", "next_slide"}
                for _, _, name in body
            ):
                raise ValueError("presentation boundary appears inside a repeated loop")
            events.extend(body * repetitions)
            events.extend(_block_events(statement.orelse))
            continue
        if isinstance(statement, ast.If):
            branches = [_block_events(statement.body), _block_events(statement.orelse)]
            events.extend(max(branches, key=lambda branch: sum(item[2] == "play" for item in branch)))
            continue
        if isinstance(statement, (ast.With, ast.AsyncWith, ast.While)):
            events.extend(_block_events(statement.body))
            events.extend(_block_events(statement.orelse) if isinstance(statement, ast.While) else [])
            continue
        if isinstance(statement, ast.Try):
            branches = [_block_events(statement.body)] + [
                _block_events(handler.body) for handler in statement.handlers
            ]
            events.extend(max(branches, key=lambda branch: sum(item[2] == "play" for item in branch)))
            events.extend(_block_events(statement.orelse))
            events.extend(_block_events(statement.finalbody))
            continue
        if isinstance(statement, ast.Match):
            branches = [_block_events(case.body) for case in statement.cases]
            if branches:
                events.extend(
                    max(branches, key=lambda branch: sum(item[2] == "play" for item in branch))
                )
            continue
        events.extend(
            sorted(
                (
                    (node.lineno, node.col_offset, name)
                    for node in ast.walk(statement)
                    if (name := _self_call_name(node))
                    in {"begin_beat", "next_beat", "next_slide", "play"}
                ),
                key=lambda item: (item[0], item[1]),
            )
        )
    return events


def segment_play_counts(source: str) -> list[int]:
    """Count top-level scene ``play`` calls between presentation boundaries."""
    tree = ast.parse(source)
    construct = next(
        (
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name == "construct"
        ),
        None,
    )
    if construct is None:
        return []

    calls = _block_events(construct.body)
    uses_named_beats = any(name in {"begin_beat", "next_beat"} for _, _, name in calls)

    if uses_named_beats:
        counts: list[int] = []
        for _, _, name in calls:
            if name in {"begin_beat", "next_beat"}:
                counts.append(0)
            elif name == "play":
                if not counts:
                    raise ValueError("play() appears before begin_beat()")
                counts[-1] += 1
        return counts

    counts = [0]
    for _, _, name in calls:
        if name == "next_slide":
            counts.append(0)
        elif name == "play":
            counts[-1] += 1
    return counts if any(counts) else []


def lesson_density_errors(
    scene_path: Path,
    beat_ids: list[str],
    *,
    maximum: int = MAX_PLAY_CALLS_PER_SEGMENT,
) -> list[str]:
    counts = segment_play_counts(scene_path.read_text(encoding="utf-8"))
    if len(counts) != len(beat_ids):
        return [
            f"segment count {len(counts)} differs from metadata beat count "
            f"{len(beat_ids)}"
        ]
    return [
        f"beat {beat_id} has {count} play phases; maximum is {maximum}"
        for beat_id, count in zip(beat_ids, counts, strict=True)
        if count > maximum
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-plays",
        type=int,
        default=MAX_PLAY_CALLS_PER_SEGMENT,
        help="Maximum self.play() calls allowed in one navigable segment.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_plays < 1:
        print("ERROR: --max-plays must be positive", file=sys.stderr)
        return 2

    failures = 0
    checked = 0
    for metadata_path in sorted(ROOT.glob("lessons/*/*/lesson.toml")):
        with metadata_path.open("rb") as handle:
            lesson = tomllib.load(handle)
        scene_path = ROOT / lesson.get("scene_file", "")
        if not scene_path.is_file():
            continue
        checked += 1
        beat_ids = [beat["id"] for beat in lesson.get("beats", [])]
        try:
            errors = lesson_density_errors(
                scene_path,
                beat_ids,
                maximum=args.max_plays,
            )
        except (SyntaxError, ValueError) as error:
            errors = [str(error)]
        for error in errors:
            failures += 1
            print(f"ERROR: {lesson['id']}: {error}", file=sys.stderr)

    if failures:
        print(f"Slide density failed: {failures} issue(s) across {checked} scenes.")
        return 1
    print(
        f"Slide density passed: {checked} scenes, at most "
        f"{args.max_plays} play phases per segment."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
