# Prepublication Audit: 2026-07-25

Status: passed for the committed source candidate; GitHub remote publication
remains pending.

## Candidate

- Commit: `d14cd2a7cc2c46f1494a2fe3cc13b5d1f044c8ce`
- Tree: `edcc95a14bf571d04f5ae2c4728f7bb32a61aafc`
- Isolation: `git archive HEAD` extracted into a new ignored directory, with no
  working-tree media or environment copied into it
- Platform: Linux x86_64, Fedora 44 kernel series
- Pixi: 0.73.0
- Python: 3.13.14
- Manim Community: 0.20.1
- Manim Slides: 5.6.0
- Tectonic: 0.16.9

## Static Gate

The isolated tree was installed with `pixi install --frozen`. These commands
all exited successfully:

```text
pixi run test                  55 tests passed
pixi run validate-catalog      76 problems; 46 lessons; registries consistent
pixi run check-sources         source index current for 46 lessons
pixi run lessons list          46 renderable visual_verified lessons
pixi run prepare-tex           cached TeX-to-SVG probe passed
```

The catalog state at this candidate is 46 `visual_verified`, 20 `discovered`,
10 `blocked`, and 0 `published`. The audit does not promote any unfinished
record.

## Representative Render Gate

The clean tree rendered `carlo.tcfs_115_math_gifted.q09` at low render quality
through the checked batch command, then ran its mechanical slide QA:

```text
pixi run lessons render carlo.tcfs_115_math_gifted.q09 --quality l
pixi run qa-slides carlo.tcfs_115_math_gifted.q09
```

Result: 16 nonblank 1920x1080 segments, a generated Manim Slides manifest, no
QA errors, and two loop endpoints within the configured difference threshold.
The contact sheet and full-resolution settled frames for reflection symmetry,
the upper-half result, and reflect-then-double were visually inspected and had
no clipping, overlap, blank output, or ordering regression.

- Manifest SHA-256:
  `4de8493728fbff67bbe40b387d5c3aded1325bf0de2a002b933a27f76b4d2692`
- Contact-sheet SHA-256:
  `37e033e0b0acae50bb6257c4626f10ace6eb77a06d4710020827c3e3cab4bd2b`

The generated manifest, videos, TeX cache, and frames remain ignored audit
outputs and are not part of the public source commit.

## Remaining Publication Gates

The maintainer approved rewriting all 20 commits to the authenticated GitHub
account's ID-based no-reply address. Author and committer dates, messages, and
trees were preserved. A verified complete bundle of the pre-rewrite history is
stored under ignored `build/backups/` storage; the temporary old-history Git
reference was removed, so only the rewritten `main` is reachable.

1. Authenticate the pinned GitHub CLI through the maintainer's browser.
2. Create the public remote, push `main`, verify its visible contents and
   default branch, then share the URL with the Carlo site owner.

The identity checkpoint is resolved. Continue with the authentication and
post-push verification steps in `docs/PUBLISHING.md`.
