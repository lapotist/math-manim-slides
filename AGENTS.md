# Project Guidance

This workspace produces visual mathematics lessons with Manim Community and
Manim Slides. The intended audience is a Traditional Chinese-speaking student
preparing for selective mathematics assessments. Explanations must be correct,
calm, concrete, and possible to follow at presentation speed.

## Mission And Scope

The project is a public, reproducible collection of lessons derived from
eligible solution material on Carlo's Math site. The canonical production unit
is one identifiable problem and its solution, not one navigation page, PDF, or
exam year.

"All" must be measured from the catalog, never inferred from the files that
happen to exist in the repository. Keep three counts separate:

- a **page** is part of Carlo's first-party information architecture;
- an **asset** is one unique embedded Drive or YouTube provider ID; and
- a **lesson unit** is one identifiable problem together with enough solution
  reasoning to build and verify a deck.

One asset can contain several lesson units, and one asset can appear on several
archive or topic pages. Never equate page count, asset count, and lesson count.
Ingest a provider ID once and retain all of its page/topic relationships.

The frozen 2026-07-24 discovery boundary is the public Google Site root plus
every path in its navigation data: 434 fetched pages, all HTTP 200, with no
additional first-party content path found in page-body links. Those pages
contain 4,346 unique embedded provider IDs: 326 Drive assets and 4,020 YouTube
videos. This is the source-asset denominator, not a claim that 4,346 decks are
complete or even eligible.

The access audit found 2,489 confirmed public assets, 622 confirmed restricted
assets, and 1,235 YouTube assets whose status is unresolved because an
anti-bot challenge prevented anonymous playback verification. `catalog/` is
authoritative for the exact status counts and must retain restricted and
unresolved records as tombstones.

A source item is eligible only when:

- it is publicly reachable from Carlo's site;
- the problem and solution can be identified without guessing;
- the available solution contains enough reasoning to verify a lesson; and
- its permission and provenance can be documented honestly.

Broken, private, member-only, duplicated, answer-only, unresolved-access, or
legally unclear items remain in the catalog with an explicit exclusion or
blocker reason. YouTube oEmbed metadata is not proof that a video is playable.
Never silently omit a record and never represent generated placeholders as
finished lessons.

The user-supplied `數學-115數理資優學科能力評量答案.pdf` is a separate source.
It was not discovered among the 326 Drive assets on the frozen Carlo crawl,
whose 中一中資優 archive currently ends at ROC 114. Catalog it as a supplied,
permission-reviewed input; never claim it was downloaded from the site.

## Timebox And Production Order

The collection has a ten-hour working timebox. Treat it as an engineering
constraint, not permission to weaken mathematical correctness or provenance.
Use the time in this order:

1. Freeze a machine-readable inventory and eligibility rule.
2. Build shared components, metadata validation, and batch commands.
3. Produce lessons in coherent source batches and parallelize independent work.
4. Run static checks continuously and render representative samples early.
5. Reserve the final portion for full catalog reconciliation, documentation,
   licensing, clean-room verification, and publication.

Prefer a reusable mathematical primitive over repeated scene boilerplate, but
do not force unlike arguments into one generic animation. If the timebox and
the catalog disagree, report the exact remaining entries and blockers; never
change the denominator or call a partial collection complete.

## Repository Contract

Use a stable collection layout as the project grows:

- `catalog/`: the source-of-truth inventory and generated indexes;
- `lessons/<source-id>/<problem-id>/`: scene, presenter script, and lesson
  metadata for one problem;
- `src/carlo_manim/`: shared visual language, geometry helpers, and templates;
- `scripts/`: inventory, validation, rendering, exporting, and index tooling;
- `tests/`: metadata, mathematics, manifest, and smoke checks;
- `docs/`: methodology, permission statement, provenance, and publication
  records;
- `build/`: generated videos, slide manifests, HTML, and QA frames; ignored by
  Git unless a deliberately selected artifact is part of a release.

Keep source files and small metadata in Git. Do not commit Pixi environments,
Manim caches, bulk source downloads, temporary frames, or every rendered video.
Select a few representative artifacts for documentation or release assets.

Every lesson-unit catalog entry must have a stable ASCII identifier and, at
minimum:

- title, topic, source collection, school/exam, year, and question number when
  those fields exist;
- canonical Carlo page URL and exact solution locator or source-asset URL;
- content type, checksum for a downloaded source asset, and duplicate-of ID;
- eligibility decision and reason;
- production state: `discovered`, `blocked`, `planned`, `storyboarded`,
  `math_verified`, `draft_rendered`, `visual_verified`, or `published`;
- scene class, presenter-script path, and build outputs;
- mathematical reviewer state and provenance/license scope.

Generated indexes must come from this metadata. Hand-edited README totals are
not authoritative.

Production states are evidence gates, not estimates of effort:

- `discovered`: source record exists, but no lesson plan is promised;
- `blocked`: a specific access, content, provenance, or rights reason is stored;
- `planned`: eligible unit and exact source locator are known;
- `storyboarded`: metadata, ordered beats, and presenter script agree;
- `math_verified`: the argument and final answer were checked independently;
- `draft_rendered`: scene code rendered through Manim Slides;
- `visual_verified`: manifest, loops, representative frames, and narration were
  reviewed; and
- `published`: the verified lesson is reachable in the public release.

`storyboarded` and `math_verified` records may intentionally have no scene file.
Only `draft_rendered` or later may be treated as renderable. A collection record
and its lesson metadata must report the same production state.

## Collection Architecture

- Metadata organizes and validates lessons; it must never generate the
  pedagogy. Each problem still needs a deliberate, source-verified storyboard.
- Every deck has a globally unique catalog ID, Python scene class, TOML lesson
  metadata file, and Traditional Chinese presenter script.
- Give conceptual beats stable ASCII IDs. Their order and loop flags must agree
  across lesson metadata, source calls, presenter-script headings, and the
  rendered Slides manifest.
- Shared helpers own stable visual semantics, typography, framing, citations,
  and common constructions. Lessons own their mathematical argument.
- Keep a scene's conceptual beats in named methods or small data structures so
  code order reads like the presenter storyboard.
- Parameterize genuinely repeated objects such as number lines, angle markers,
  algebra transformations, coordinate planes, and source footers.
- Do not treat screenshots of solutions, page-by-page PDF playback, or generic
  text fades as completed explanatory lessons.
- A template may establish consistent framing, but every motion and reveal must
  still be justified by that problem's reasoning.
- Keep lesson imports deterministic. Do not fetch network resources during a
  render.
- Display strings may use Traditional Chinese; identifiers, filenames, and
  infrastructure code remain ASCII.
- Promote a helper into the shared package only after a second concrete lesson
  demonstrates the same behavior. Reuse primitives, not finished explanations.

## Parallel Production

- Assign one worker one problem directory at a time. A lesson worker may edit
  that directory and its generated, ignored render outputs, but must not edit
  the shared collection registry, README totals, licensing files, or unrelated
  lessons.
- The integrating worker reviews the rendered contact sheet, independently
  reconciles the lesson state into `collection.toml`, and runs the collection
  validator. This keeps concurrent state updates from overwriting one another.
- A handoff must report the exact render command, segment count, loop result,
  mathematical check, visual inspection performed, and any unresolved caveat.
  A bare claim that a deck is complete is not an evidence gate.
- Production state and rights state are independent. Rendering a lesson may
  advance its production state; it must never advance `pending_cc0_scope` or
  any other permission state without a documented rights decision.
- Coordinate changes to shared helpers before editing them during parallel
  production. Prefer a local lesson primitive until repeated use and integration
  review justify promotion into `src/carlo_manim/`.

## Teaching Order

Use experiential order rather than textbook order:

1. Establish the concrete object with as little text as possible.
2. Vary one meaningful object while keeping the reference geometry fixed.
3. Let the viewer notice a pattern, boundary, symmetry, or invariant.
4. Pause on a question before revealing its answer.
5. Make the observation precise with a visible construction.
6. Test a generic case and the important boundary or extreme cases.
7. Isolate one representative piece while preserving the whole as dim context.
8. Introduce measurements only when the picture has motivated them.
9. Build the algebra from the visible geometry.
10. Return to the complete setup and consolidate the result.

Do not open with a definition, theorem name, finished locus, or final formula.
The viewer should feel that the result could have been discovered from the
diagram.

Review every explanation through four first-party 3Blue1Brown lenses:
motivation, clarity, novelty, and memorability. These are quality questions,
not instructions to imitate another creator's visual style.

- Keep the opening motivation brief and concrete. Give the viewer a specific
  object or puzzle to care about, not a broad promise that the topic is useful.
- Apply motivation at the scale of every beat: a new point, construction,
  variable, or equation must answer a question the viewer already has.
- Keep one concrete example front and center. Let the audience play with one or
  two cases and notice one relevant pattern at a time before stating a rule.
- Delay equations until the corresponding visual relationship can already be
  pictured. Algebra should name and compress an idea, not introduce it cold.
- Design the consolidation beat around an earned realization: the final result
  should resolve the opening question and make the route memorable.
- Develop an original voice, pacing, composition, and color system. Reuse
  explanatory principles, never channel-specific artwork or mannerisms.

## Motion And Proof

- Every movement must answer the same question as the narration at that moment.
- Choose motion states deliberately: generic, canonical, boundary/extreme, and
  mirrored states. Undirected roaming is not evidence.
- Freeze all variables except the one currently under study.
- Keep dependent geometry attached with updaters during exploration.
- Do not leave a permanent trace for an arbitrary exploratory path; it could be
  mistaken for the mathematical locus. A short dissipating trace is acceptable
  only when clearly useful.
- Preserve object identity through transforms. Prefer transforming a copy of a
  visible shape or label when deriving a new representation.
- Establish symmetry with an explicit constraint-preserving map, not by saying
  that two shapes look alike. Show one arbitrary object and its reflected copy,
  show why the defining data are unchanged, and only then generalize.
- A visual argument must remain mathematically exact. Animation may motivate a
  claim, but must not conceal a missing boundary case or unjustified equality.
- Repetition must add evidence: for example, generic case, extreme case,
  reflected case, then a final replay. Do not repeat motion decoratively.

## Attention And Visual Language

- Keep reference geometry neutral and the current variable visually dominant.
- Give each mathematical role a stable semantic color across the whole lesson.
  A color used for a region or length in the diagram must carry into its formula
  term.
- Use opacity to focus attention while retaining useful context. Prefer dimming
  inactive construction lines to repeatedly clearing and rebuilding the scene.
- Keep the camera stable for a 2D diagram unless a zoom reveals a relationship
  that is genuinely too small to see.
- Avoid decorative motion, dense headers, and simultaneous unrelated changes.
- A slide boundary must land on a settled, readable composition that can remain
  on screen while the presenter speaks.

## Equations

- Every equation must be visually earned. Reveal the geometric length, angle,
  sector, triangle, or area before showing the corresponding symbol.
- Build long expressions one contribution at a time instead of writing a
  completed derivation in one animation.
- Prefer `TransformFromCopy` or an equivalent continuity-preserving transform
  from diagram labels and shapes into formula terms.
- Stop dynamic geometry before asking the audience to read algebra.
- State a local or half-result before generalizing to the whole.

## Manim Slides Workflow

- Presentation scenes subclass `manim_slides.Slide`, not `manim.Scene`.
- Use `self.next_slide()` only after a conceptual beat has resolved.
- Options on `next_slide(...)` configure the following animation segment.
  Therefore place `self.next_slide(loop=True)` immediately before a looping
  animation.
- A loop must return to its starting visual state without a visible jump.
- Do not add unnecessary `next_slide()` calls at the beginning or end; Manim
  Slides supplies those boundaries.
- Use the Pixi environment so rendering and presenting share the same Manim and
  plugin installation.
- Run `pixi run prepare-tex` once after installation. It populates Tectonic's
  pinned resource cache and proves that XDV-to-SVG conversion works before
  writing `build/tex/.ready`; the Manim wrapper then enforces cached-only
  equation compilation so renders never fetch network resources.
- Prefer an existing system `dvisvgm`. On Fedora, `prepare-tex` may download and
  extract the distribution converter and AMS outline-font RPMs into ignored
  `build/` storage without `sudo`. Do not commit those packages or broaden
  `LD_LIBRARY_PATH` globally. Other operating systems must install their native
  `dvisvgm` package explicitly.
- Do not accept a zero-exit converter probe by itself. `prepare-tex` must parse
  the warm-up SVG and reject missing glyph definitions; a file can exist yet
  still render every equation blank. After changing the TeX toolchain version,
  invalidate prior TeX/partial-render caches or render once with caching
  disabled before visual QA.
- Give every render its own `--media_dir build/media/<lesson-id>`, especially
  when jobs run concurrently. Manim cleans intermediate TeX files after a
  conversion; sharing `media/Tex` lets one process delete another process's XDV
  between compilation and `dvisvgm`. The batch runner must preserve this
  isolation rather than relying on render timing.

Suggested commands:

```bash
pixi run manim-slides render --quality h --media_dir build/media/question_9 question_9_slide.py Question9Slide
pixi run manim-slides present Question9Slide
pixi run manim-slides convert --to html --one-file --offline Question9Slide question_9_slides.html
```

Use `--quality h`, not the combined `-qh` flag: the Slides wrapper can interpret
the `h` as its own help option. Collection-wide commands should be Pixi tasks
and accept catalog IDs or deterministic batches. A failed lesson must make the
batch command nonzero and produce a machine-readable failure report.

```bash
pixi run validate-catalog
pixi run lessons list
pixi run lessons render carlo.tcfs_115_math_gifted.q09 --quality l
pixi run lessons export --status visual_verified
```

## Presenter Script Contract

- Every deck must have a presenter script in Traditional Chinese beside the
  scene source.
- Number script beats one-to-one with the rendered slide segments.
- Mark presenter actions explicitly, including `[NEXT]`, `[LOOP]`, and
  `[PAUSE]` cues.
- Narrate only what is currently visible. Do not name a theorem, construction,
  or formula before it appears.
- Use short, speakable sentences and leave real silence after a question.
- Put reasoning and transitions in the script; keep on-screen wording brief.
- Do not narrate a conclusion before the visual operation that justifies it has
  visibly settled.

## Reference Implementation: Question 9

For the moving-point locus in `question_9_slide.py`, preserve this order:

1. Show only the fixed segment `AB = 4`.
2. Introduce the same point `P` that will remain throughout the lesson.
3. Move `P` through deliberate valid configurations with `AP`, `BP`, and the
   angle updating; do not show the locus yet.
4. Ask where `P` can move, then reveal the locus outline.
5. Reflect one arbitrary upper point to a lower point and show that the angle
   constraint is unchanged. Only then state upper/lower symmetry.
6. Dim the lower half and calculate only the upper half.
7. Reveal the `90 degree` boundary and its semicircle construction.
8. Reveal the `30 degree` boundary, center, radii, and equilateral triangle.
9. Build the upper-area expression from the visible sector, triangle, and
   semicircle, one term at a time.
10. Hold the upper result, reflect its region downward, and only then multiply
    by two.
11. End by reconnecting the final area to the original moving point.

For this lesson specifically, never say "multiply by two" until the reflected
half has visibly landed.

## Verification

- Run a Python compile/import check before rendering.
- Render through the `manim-slides` wrapper and confirm that the slide manifest
  is generated.
- Inspect representative frames from every conceptual segment, including the
  loop, symmetry proof, half-area derivation, and final reflection.
- Run `pixi run qa-slides <lesson-id>` for mechanical segment, resolution,
  nonblank-frame, and loop-endpoint checks. Treat it as a rejection gate, not a
  substitute for visual inspection.
- Inspect the complete contact sheet at presentation scale, then open every
  dense algebra, table, or multi-label frame at full 1920x1080 resolution.
  Endpoint thumbnails can hide collisions that remain obvious to an audience.
- Sample intermediate frames for transformations whose source and target move
  across the diagram. Settled-frame QA cannot detect a label crossing another
  object halfway through an otherwise correct animation.
- When a semantic label changes, transform or remove the old label before the
  replacement appears. Never leave two versions occupying the same geometry;
  this commonly creates a visually plausible but unreadable composite string.
- Check 1920x1080 framing for clipped text, overlapping labels, blank frames,
  illegible contrast, and unexpected layout shifts.
- Confirm the presenter script has exactly the same ordered beats as the deck.
- Verify the final formula independently from the animation code.
- After all human checks pass, run `pixi run freeze-qa --human-reviewed
  <lesson-id>`. Commit the compact `qa/` attestation, not the generated video,
  contact sheet, or Slides manifest. Any later scene, script, or storyboard edit
  invalidates its recorded hash and requires a new render and review.

Collection-wide verification has three gates:

1. Static gate for every entry: schema, URLs, path uniqueness, Python compile,
   scene import, script/segment count, attribution, and expected final result.
2. Render gate for every completed entry: Slides manifest, nonblank first and
   last frames, valid dimensions, playable media, and clean loop endpoints.
3. Human gate: mathematical argument, Traditional Chinese narration, visual
   legibility, and agreement with the cited source solution.

Automated checks may reject a lesson but may not declare its mathematics
correct. A catalog item reaches `verified` only after its result has been
checked independently of the animation implementation.

If a source answer conflicts with its own derivation, preserve the original
locator and discrepancy in metadata, recompute the result independently, and
test the corrected value by substitution or exhaustive checking where
possible. Present the correction neutrally and never silently rewrite the
source record.

## Provenance, Permission, And Licensing

- License the project's original code, original lesson text, and original
  project artwork with `CC0-1.0` in the root `LICENSE` file.
- Treat CC0 as applying only to an explicit path allowlist in `NOTICE.md`, not
  as a blanket claim over the repository.
- Before incorporating an input, classify it as project-original,
  Carlo-authorized, compatible third-party, reference-only, or excluded.
- Keep `SOURCES.md` or an equivalent generated source index with one canonical
  Carlo URL and solution locator per lesson. Repeat the concise source credit in
  lesson metadata and the presenter script.
- Keep a public permission statement that names the grantor, grantee/project,
  material scope, allowed adaptation/publication, CC0 relicensing scope, and
  date. State only facts supported by the permission; do not publish private
  messages, email addresses, signatures, or other personal correspondence.
- Permission from the site owner does not automatically establish ownership of
  third-party exam statements, logos, fonts, photographs, linked documents, or
  3Blue1Brown material. Link to those inputs and document their separate status
  unless the permission scope explicitly covers redistribution and relicensing.
- General permission to use or adapt material is not automatically authority to
  make an irrevocable CC0 dedication. Before release, verify that the written
  grant directly applies CC0 or expressly authorizes the required relicensing
  for the exact source and output paths. Unclear scope fails closed.
- Do not copy web wording, diagrams, scans, images, code, audio, video, fonts,
  or logos merely because a source is cited. Independently express mathematical
  facts unless the recorded permission explicitly covers the adaptation.
- Do not copy 3Blue1Brown code, artwork, narration, or rendered assets into the
  CC0 project. Learn from its explanatory patterns and implement original
  scenes.
- CC0 does not require attribution, but this project requires source credit as
  a provenance and academic-integrity rule.
- Add an explicit exception notice for any non-CC0 input retained in the
  repository. Never place a blanket CC0 claim over third-party material.
- Generated HTML and video are CC0 only when every bundled input is covered or
  separately compatible and correctly marked.
- Never change `LICENSE`, `NOTICE.md`, `SOURCES.md`, the public permission note,
  covered paths, or release-license claims without a fresh rights audit.
- Never imply endorsement by Carlo, 3Blue1Brown, Manim, Manim Slides, a school,
  a publisher, or a contest organizer.

## GitHub Publication

- Initialize Git only after `.gitignore`, `LICENSE`, provenance documents, and
  the first validated catalog are present.
- Scan staged paths for secrets, private permission correspondence, local
  absolute paths, oversized binaries, and generated caches before every public
  push.
- Use small, reviewable commits that separate inventory, infrastructure,
  lessons, and generated documentation.
- The public README must state scope, exact catalog totals by status, build and
  presentation commands, source-credit policy, permission basis, and known
  blockers. Totals must be generated from the catalog.
- Before publication, clone or archive from the committed tree into a clean
  temporary directory, install with the lock file, run static validation, and
  render at least one representative lesson from each template family.
- Publication is complete only when the public GitHub URL is reachable, the
  default branch contains the intended license and provenance files, and the
  documented commands work from the committed tree.

## Research Basis

The guidance above adapts teaching principles and animation grammar from these
sources without copying their artwork, narration, or scene implementation:

- Carlo's Traditional Chinese mathematics resource and its concept-first,
  animated worked-example organization:
  https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/
- 3Blue1Brown's official exposition advice:
  https://www.3blue1brown.com/about/
- The concrete-to-general circle-area lesson:
  https://www.3blue1brown.com/lessons/essence-of-calculus/
- The fixed-points/variable-point problem-solving lesson:
  https://www.3blue1brown.com/lessons/hardest-problem/
- The whole-to-one-piece-to-whole sphere-area lesson:
  https://www.3blue1brown.com/lessons/sphere-area/
- Diagnostic motion followed by local geometric proof:
  https://www.3blue1brown.com/lessons/derivatives-trig-functions/
- An explicit invariant used to justify a visual equivalence:
  https://www.3blue1brown.com/lessons/dandelin-spheres/
- Deliberate exploration and invariant discovery:
  https://www.3blue1brown.com/lessons/windmills/
- Manim Slides official documentation:
  https://manim-slides.eertmans.be/latest/
