# Sources And Provenance

This ledger records provenance; it is not a license grant. Exact lesson-level
rows will be generated from catalog metadata as the collection grows.

| ID | Creator/source | Role and use | Affected paths | Rights status |
| --- | --- | --- | --- | --- |
| `carlo-site` | [正哥愛數學](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/) | Public source inventory and mathematical-solution provenance; URLs and factual metadata only in the catalog | `catalog/site_pages.json`, `catalog/site_taxonomy.json`, `catalog/source_assets.json`, `catalog/source_access_audit.json`, `catalog/audit_summary.json` | Site-owner permission reported by the user; exact CC0 authority and third-party boundaries require the release gate |
| `tcfs-115-gifted-math` | `數學-115數理資優學科能力評量答案.pdf` | Separately supplied mathematical source for the 14-unit ROC 115 TCFSH collection; it was not discovered among the site's 326 embedded Drive assets | `lessons/tcfs_115_math_gifted/`, `question_9_slide.py`, `question_9_presenter_script.md` | Adaptation permission reported by the user; excluded from the CC0 allowlist pending exact scope confirmation |
| `3b1b-research` | [3Blue1Brown exposition](https://www.3blue1brown.com/about/) and linked official lessons | Pedagogy research only; no code, artwork, narration, or rendered media incorporated | `AGENTS.md` | Reference only, not incorporated |
| `manim` | [Manim Community](https://github.com/ManimCommunity/manim) | Runtime dependency | `pixi.toml`, `pixi.lock` | MIT; package contents not relicensed |
| `manim-slides` | [Manim Slides](https://github.com/jeertmans/manim-slides) | Runtime dependency | `pixi.toml`, `pixi.lock` | MIT; package contents not relicensed |
| `noto-sans-cjk` | [Noto CJK](https://github.com/notofonts/noto-cjk) | Named system font at render time; no font binary currently bundled | `question_9_slide.py` | OFL-1.1 if redistributed; not currently incorporated |

For each completed lesson, record the canonical Carlo page, exact file or
video locator, creator/rightsholder, access date, use, modified paths,
modifications, permission reference, and whether the material is included in
or excluded from the CC0 scope.

The 2026-07-24 crawl found the public 中一中資優 archive through ROC 114. The
ROC 115 PDF above therefore uses the archive page only as creator context; the
repository must not describe it as a site download.
