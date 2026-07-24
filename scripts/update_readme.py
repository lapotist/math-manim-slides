#!/usr/bin/env python3
"""Regenerate the README inventory block from catalog metadata."""

from __future__ import annotations

import json
import re
import tomllib
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
START = "<!-- catalog-summary:start -->"
END = "<!-- catalog-summary:end -->"
LESSONS_START = "<!-- lesson-table:start -->"
LESSONS_END = "<!-- lesson-table:end -->"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collection_counts() -> tuple[int, Counter[str]]:
    total = 0
    states: Counter[str] = Counter()
    for path in sorted(ROOT.glob("lessons/*/collection.toml")):
        with path.open("rb") as handle:
            collection = tomllib.load(handle)
        for problem in collection["problems"]:
            total += 1
            states[problem["production_state"]] += 1
    return total, states


def render_summary() -> str:
    audit = load_json(ROOT / "catalog" / "audit_summary.json")
    total_lessons, states = collection_counts()
    state_text = ", ".join(
        f"{count} `{state}`" for state, count in sorted(states.items())
    )
    return "\n".join(
        (
            START,
            "The reproducible 2026-07-24 site snapshot records:",
            "",
            f"- {audit['scope']['pages']:,} public first-party pages;",
            (
                f"- {audit['unique_assets']['total']:,} unique embedded assets "
                f"({audit['unique_assets']['google_drive']:,} Drive and "
                f"{audit['unique_assets']['youtube']:,} YouTube);"
            ),
            (
                f"- {audit['access']['confirmed_public']:,} confirmed public, "
                f"{audit['access']['confirmed_restricted']:,} confirmed "
                f"restricted, and "
                f"{audit['access']['unresolved_bot_challenge']:,} unresolved "
                "assets; and"
            ),
            (
                f"- {total_lessons} lesson units in the separately supplied "
                f"ROC 115 pilot collection: {state_text}."
            ),
            "",
            (
                "Pages, assets, and lesson units are different denominators. "
                "Eligibility and production states are tracked separately; "
                "placeholders and blocked sources never count as finished "
                "lessons."
            ),
            END,
        )
    )


def render_lesson_table() -> str:
    metadata_by_id: dict[str, tuple[dict[str, Any], Path]] = {}
    for path in sorted(ROOT.glob("lessons/*/*/lesson.toml")):
        with path.open("rb") as handle:
            metadata = tomllib.load(handle)
        metadata_by_id[metadata["id"]] = (metadata, path.relative_to(ROOT))

    rows = [
        LESSONS_START,
        "| Lesson | Topic | State | Source files |",
        "| --- | --- | --- | --- |",
    ]
    for collection_path in sorted(ROOT.glob("lessons/*/collection.toml")):
        with collection_path.open("rb") as handle:
            collection = tomllib.load(handle)
        for problem in collection["problems"]:
            metadata, metadata_path = metadata_by_id[problem["id"]]
            scene_path = ROOT / metadata["scene_file"]
            links = [f"[metadata]({metadata_path.as_posix()})"]
            if scene_path.is_file():
                links.append(f"[scene]({metadata['scene_file']})")
            links.append(f"[script]({metadata['presenter_script']})")
            rows.append(
                "| "
                f"{problem['label']} | {problem['topic']} | "
                f"`{problem['production_state']}` | {' / '.join(links)} |"
            )
    rows.append(LESSONS_END)
    return "\n".join(rows)


def main() -> int:
    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8")
    pattern = re.compile(
        rf"{re.escape(START)}.*?{re.escape(END)}",
        re.DOTALL,
    )
    if not pattern.search(readme):
        raise ValueError("README inventory markers are missing")
    updated = pattern.sub(render_summary(), readme)
    lesson_pattern = re.compile(
        rf"{re.escape(LESSONS_START)}.*?{re.escape(LESSONS_END)}",
        re.DOTALL,
    )
    if not lesson_pattern.search(updated):
        raise ValueError("README lesson-table markers are missing")
    updated = lesson_pattern.sub(render_lesson_table(), updated)
    readme_path.write_text(updated, encoding="utf-8")
    print("Updated README catalog summary.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
