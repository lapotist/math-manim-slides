# Carlo Math Manim Slides

An independent collection of slow, intuitive Traditional Chinese mathematics
lessons built with Manim Community and Manim Slides. Each completed lesson is
linked to the exact solution source from [正哥愛數學](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/).

The current golden lesson explains Question 9 from the 115 academic-year
Taichung First Senior High School mathematics gifted-placement assessment. It
first explores the moving point, proves the upper/lower symmetry, calculates
one half, and only then doubles the area.

## Current Inventory

<!-- catalog-summary:start -->
The reproducible 2026-07-24 site snapshot records:

- 434 public first-party pages;
- 4,346 unique embedded assets (326 Drive and 4,020 YouTube);
- 2,489 confirmed public, 622 confirmed restricted, and 1,235 unresolved assets; and
- 14 lesson units in the separately supplied ROC 115 pilot collection: 4 `math_verified`, 9 `storyboarded`, 1 `visual_verified`.

Pages, assets, and lesson units are different denominators. Eligibility and production states are tracked separately; placeholders and blocked sources never count as finished lessons.
<!-- catalog-summary:end -->

## Setup And Use

Install [Pixi](https://pixi.sh/), then run:

```bash
pixi install
pixi run render-q9
pixi run present-q9
```

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
