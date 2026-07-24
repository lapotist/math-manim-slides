# Sources And Provenance

This ledger records provenance; it is not a license grant. Exact lesson-level
rows will be generated from catalog metadata as the collection grows.

| ID | Creator/source | Role and use | Affected paths | Rights status |
| --- | --- | --- | --- | --- |
| `carlo-site` | [正哥愛數學](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/) | Public source inventory and mathematical-solution provenance; URLs and factual metadata only in the catalog | `catalog/site_pages.json`, `catalog/site_taxonomy.json`, `catalog/source_assets.json`, `catalog/source_access_audit.json`, `catalog/audit_summary.json` | Site-owner permission reported by the user; exact CC0 authority and third-party boundaries require the release gate |
| `chiayi-104-science` | [104 嘉中科學班 page](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E5%98%89%E4%B8%AD%E7%A7%91%E5%AD%B8%E7%8F%AD/104%E5%98%89%E4%B8%AD), public Drive PDF `1ePTUjWYnFX91XMFZlouPxcOpqf6J1qef`, and the 20 uniquely numbered public videos mapped in collection metadata | One problem per PDF page and one candidate solution video per fill-in question; worked-content sufficiency review is still pending | `lessons/chiayi_104_science/` | Site-owner permission reported by the user; source and future lesson expression remain outside the CC0 allowlist pending exact scope confirmation |
| `tcfs-112-gifted-math` | [112 中一中資優班 page](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/112%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87), public Drive PDF `1wZiSE5cZZI9Fr_YJovGP_H3aWoFXxc_H`, and the 14 public videos mapped in the collection metadata | Problem statements for 13 fill-ins and one four-part proof unit; the PDF solution areas are blank, so the videos are the worked-solution sources | `lessons/tcfs_112_math_gifted/` | Site-owner permission reported by the user; lesson expression remains excluded from the CC0 allowlist pending exact scope confirmation |
| `tcfs-113-gifted-math` | [113 中一中資優班 page](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/113%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87), public Drive PDF `1QQhuf8PqZMVyCdF9s9LHR8Q3y8RmAk3M`, and public videos `FSGAuRvRFU0`, `W-NGUVPlcOc`, `Hypdc2fqjfM`, `xRrA7_xEStU`, `X6Cabjm94eY`, `FxSdkChC9Z8`, `zUVNQX92b64`, `rw7Z1rw7gYA` | Problem statements and worked reasoning for 13 fill-ins and one three-part proof unit; paired videos are decomposed by exact problem records | `lessons/tcfs_113_math_gifted/` | Site-owner permission reported by the user; lesson expression remains excluded from the CC0 allowlist pending exact scope confirmation |
| `tcfs-114-gifted-math` | [114 中一中資優班 page](https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87%E5%84%AA%E7%8F%AD/114%E4%B8%AD%E4%B8%80%E4%B8%AD%E8%B3%87), public Drive PDF `17g2ffD4VJK5Xl5qVitUH9kbNDIDxwd1J`, and public videos `oRepfpw90Fg`, `CeH9yZ8pnc0`, `MUhQmAz9OvE`, `Eq_1v5YG5bs` | Problem statements and solution reasoning for fill-in questions 1, 2, 3, and 13; the ten member-only solution videos are cataloged as blocked and are not lesson inputs | `lessons/tcfs_114_math_gifted/` | Site-owner permission reported by the user; lesson expression remains excluded from the CC0 allowlist pending exact scope confirmation |
| `tcfs-115-gifted-math` | `數學-115數理資優學科能力評量答案.pdf` | Separately supplied mathematical source for the 14-unit ROC 115 TCFSH collection; it was not discovered among the site's 326 embedded Drive assets | `lessons/tcfs_115_math_gifted/`, `question_9_slide.py`, `question_9_presenter_script.md` | Adaptation permission reported by the user; excluded from the CC0 allowlist pending exact scope confirmation |
| `3b1b-research` | [3Blue1Brown exposition](https://www.3blue1brown.com/about/), linked official lessons, and [What makes a great math explanation?](https://www.youtube.com/watch?v=cDofhN-RJqg) | Pedagogy research only; no code, artwork, narration, or rendered media incorporated | `AGENTS.md`, `docs/research/PEDAGOGY.md` | Reference only, not incorporated |
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
