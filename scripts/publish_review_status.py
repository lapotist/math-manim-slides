#!/usr/bin/env python3
"""Publish sanitized local review progress for the public lesson library."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

try:
    from scripts.build_lessons import load_lessons, select_lessons
    from scripts.review_site import (
        BUILT_PUBLIC_STATUS_PATH,
        PUBLIC_STATUS_PATH,
        REVIEW_ROOT,
        ReviewSiteError,
        load_reviewable_lesson,
        write_public_status_feed,
    )
except ModuleNotFoundError:  # Direct execution puts scripts/ on sys.path.
    from build_lessons import load_lessons, select_lessons  # type: ignore[no-redef]
    from review_site import (  # type: ignore[no-redef]
        BUILT_PUBLIC_STATUS_PATH,
        PUBLIC_STATUS_PATH,
        REVIEW_ROOT,
        ReviewSiteError,
        load_reviewable_lesson,
        write_public_status_feed,
    )


def publish(
    lessons: list[dict],
    *,
    review_root: Path = REVIEW_ROOT,
    destinations: tuple[Path, ...] = (PUBLIC_STATUS_PATH, BUILT_PUBLIC_STATUS_PATH),
) -> dict:
    asset_map = {}
    records = []
    errors = []
    for lesson in lessons:
        try:
            records.append(load_reviewable_lesson(lesson, asset_map))
        except ReviewSiteError as error:
            errors.append(str(error))
    if errors:
        raise ReviewSiteError("\n".join(errors))
    if not records:
        raise ReviewSiteError("no lesson has current source-bound QA")
    return write_public_status_feed(records, review_root, destinations)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ids", nargs="*")
    parser.add_argument(
        "--status",
        default="draft_rendered,visual_verified,published",
        help="Select one production state or a comma-separated set of states.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        selected = select_lessons(load_lessons(), args.ids, args.status)
        feed = publish(selected)
    except (OSError, ReviewSiteError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    print(
        f"Review status ready: {PUBLIC_STATUS_PATH.relative_to(PUBLIC_STATUS_PATH.parents[1])} "
        f"({len(feed['lessons'])} lessons)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
