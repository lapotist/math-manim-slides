# Carlo Math Manim Slides

An independent collection of slow, intuitive Traditional Chinese mathematics
lessons built with Manim Community and Manim Slides. Each completed lesson is
linked to the exact solution source from [正哥愛數學](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/).

Question 9 is the reference implementation: it first explores the moving
point, proves upper/lower symmetry, calculates one half, and only then doubles
the area. The same question-first, visual-evidence-first standard applies to
the rest of the collection.

## Current Inventory

<!-- catalog-summary:start -->
The reproducible 2026-07-24 site snapshot records:

- 434 public first-party pages;
- 4,346 unique embedded assets (326 Drive and 4,020 YouTube);
- 2,489 confirmed public, 622 confirmed restricted, and 1,235 unresolved assets; and
- 14 lesson units in the separately supplied ROC 115 pilot collection: 14 `visual_verified`.

Pages, assets, and lesson units are different denominators. Eligibility and production states are tracked separately; placeholders and blocked sources never count as finished lessons.
<!-- catalog-summary:end -->

The site-wide conversion is not complete. The site snapshot and access audit
are complete at the boundary above, while the 2,489 confirmed-public assets
still require problem-level extraction, mathematical review, and an exact
rights decision. The 14-unit ROC 115 pilot is a separately supplied source and
must not be used to imply that every Carlo asset has been converted.

## Lesson Collection

<!-- lesson-table:start -->
| Lesson | Topic | State | Source files |
| --- | --- | --- | --- |
| Part 1, Question 1 | angle bisectors | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q01/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q01/deck.py) / [script](lessons/tcfs_115_math_gifted/q01/presenter.zh-TW.md) |
| Part 1, Question 2 | equal-area rectangles | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q02/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q02/deck.py) / [script](lessons/tcfs_115_math_gifted/q02/presenter.zh-TW.md) |
| Part 1, Question 3 | quadratic functions | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q03/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q03/deck.py) / [script](lessons/tcfs_115_math_gifted/q03/presenter.zh-TW.md) |
| Part 1, Question 4 | sequences and number-line motion | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q04/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q04/deck.py) / [script](lessons/tcfs_115_math_gifted/q04/presenter.zh-TW.md) |
| Part 1, Question 5 | proportional sequences | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q05/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q05/deck.py) / [script](lessons/tcfs_115_math_gifted/q05/presenter.zh-TW.md) |
| Part 1, Question 6 | integer factorization and triangles | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q06/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q06/deck.py) / [script](lessons/tcfs_115_math_gifted/q06/presenter.zh-TW.md) |
| Part 1, Question 7 | radical conjugates | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q07/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q07/deck.py) / [script](lessons/tcfs_115_math_gifted/q07/presenter.zh-TW.md) |
| Part 1, Question 8 | quadratic graph intersections | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q08/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q08/deck.py) / [script](lessons/tcfs_115_math_gifted/q08/presenter.zh-TW.md) |
| Part 1, Question 9 | moving-point locus and area | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q09/lesson.toml) / [scene](question_9_slide.py) / [script](question_9_presenter_script.md) |
| Part 1, Question 10 | inequality bounds | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q10/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q10/deck.py) / [script](lessons/tcfs_115_math_gifted/q10/presenter.zh-TW.md) |
| Part 1, Question 11 | cube plane section | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q11/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q11/deck.py) / [script](lessons/tcfs_115_math_gifted/q11/presenter.zh-TW.md) |
| Part 1, Question 12 | rotation and shortest path | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/q12/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/q12/deck.py) / [script](lessons/tcfs_115_math_gifted/q12/presenter.zh-TW.md) |
| Part 2, Question 1 | symmetric equation systems | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/p2q01/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/p2q01/deck.py) / [script](lessons/tcfs_115_math_gifted/p2q01/presenter.zh-TW.md) |
| Part 2, Question 2 | angle-bisector length identity | `visual_verified` | [metadata](lessons/tcfs_115_math_gifted/p2q02/lesson.toml) / [scene](lessons/tcfs_115_math_gifted/p2q02/deck.py) / [script](lessons/tcfs_115_math_gifted/p2q02/presenter.zh-TW.md) |
<!-- lesson-table:end -->

## Setup And Use

Install [Pixi](https://pixi.sh/), then run:

```bash
pixi install
pixi run prepare-tex
pixi run render-q9
pixi run present-q9
```

`prepare-tex` downloads the resource bundle pinned by Tectonic 0.16.9 during
setup, verifies an actual XDV-to-SVG conversion, and then keeps equation
rendering network-free. It uses an existing `dvisvgm` when available. On
Fedora, if `dvisvgm` is absent, it downloads and extracts the distribution's
`dvisvgm` and AMS outline-font RPMs into ignored `build/` storage without
`sudo`; other systems ask for the native package before continuing. Setup
fails closed if the generated SVG contains missing glyph definitions.

List, render, present, and export cataloged lessons with:

```bash
pixi run lessons list
pixi run lessons render --status visual_verified --jobs 2 --quality l
pixi run lessons present carlo.tcfs_115_math_gifted.q09
pixi run lessons export --status visual_verified --jobs 2
```

Generated videos, Slides manifests, HTML, QA frames, and logs stay in ignored
build directories. Compact source-bound QA attestations under `qa/` make the
verified state checkable from a clean clone without committing media.

Refresh the public source inventory and its flattened registry with:

```bash
pixi run inventory-site
pixi run build-source-catalog
pixi run update-readme
```

## Sources And License

Solution provenance is documented in `SOURCES.md`. The site-owner permission
gate and its privacy boundary are documented in
`docs/provenance/CARLO_PERMISSION.md`.

The exact `LICENSE` file contains CC0-1.0. CC0 applies only to the project-owned
paths explicitly listed in `NOTICE.md`; source material, dependencies, and
unreviewed adapted expression retain their respective status. Source credit is
required by this project's academic-integrity policy even where CC0 would not
legally require attribution.

This project is independent and does not imply endorsement by Carlo, the
schools or contests represented in source material, 3Blue1Brown, Manim, or
Manim Slides.
