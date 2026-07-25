# Project Guidance

This workspace produces visual mathematics lessons with Manim Community and
Manim Slides. The intended audience is a Traditional Chinese-speaking student
preparing for selective mathematics assessments. Explanations must be correct,
calm, concrete, and possible to follow at presentation speed.

Treat this as a teacher-led worked-example genre for that specific audience,
not a learner diary, research-news summary, or general-interest spectacle.
Before storyboarding, record the prerequisite knowledge and the likely first
misconception. Let those facts determine vocabulary, pause length, and how much
intermediate structure remains visible; do not inherit pacing from a creator in
a different explanatory genre merely because its animation style is appealing.

## Mission And Scope

The project is a public, reproducible, multi-source collection of visual
mathematics lessons. Each source cohort must have its own provenance,
permission, and rights record. The canonical production unit is one
identifiable problem and its solution, not one navigation page, PDF, video,
creator, or exam year.

"All" must name a source boundary and be measured from the catalog, never
inferred from the files that happen to exist in the repository. For a
site-derived cohort, keep three counts separate:

- a **page** is part of that source's first-party information architecture;
- an **asset** is one unique embedded Drive or YouTube provider ID; and
- a **lesson unit** is one identifiable problem together with enough solution
  reasoning to build and verify a deck.

One asset can contain several lesson units, and one asset can appear on several
archive or topic pages. Never equate page count, asset count, and lesson count.
Ingest a provider ID once and retain all of its page/topic relationships.

### Current Carlo Source Cohort

The frozen 2026-07-24 Carlo discovery boundary is the public Google Site root
plus every path in its navigation data: 434 fetched pages, all HTTP 200, with
no additional first-party content path found in page-body links. Those pages
contain 4,346 unique embedded provider IDs: 326 Drive assets and 4,020 YouTube
videos. This is that cohort's source-asset denominator, not a claim that 4,346
decks are complete or even eligible, and not a denominator for future cohorts.

The access audit found 2,489 confirmed public assets, 622 confirmed restricted
assets, and 1,235 YouTube assets whose status is unresolved because an
anti-bot challenge prevented anonymous playback verification. `catalog/` is
authoritative for the exact status counts and must retain restricted and
unresolved records as tombstones.

A source item is eligible only when:

- its provenance and access path are documented and publicly verifiable, or a
  supplied-source record explains the controlled review boundary;
- the problem and solution can be identified without guessing;
- the available solution contains enough reasoning to verify a lesson; and
- its permission and provenance can be documented honestly.

Broken, private, member-only, duplicated, answer-only, unresolved-access, or
legally unclear items remain in their source cohort with an explicit exclusion
or blocker reason. YouTube oEmbed metadata is not proof that a video is
playable. Never silently omit a record and never represent generated
placeholders as finished lessons.

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

## Source Research Gate

Research is part of lesson production, not a preliminary task that can be
skipped once a render starts. Before storyboarding a problem:

- open the canonical source record and record the exact problem asset,
  solution asset, page or timestamp range, provider IDs, access status, and
  checksum;
- reconstruct the argument independently from the problem statement, including
  domain restrictions, endpoints, degenerate cases, and the requested answer;
- separate restrictions stated by the problem from conventions suggested only
  by its picture, such as same-ray placement, point order, positive lengths,
  orientation, or convexity. Try at least one exact counterexample outside the
  pictured configuration before turning a construction-specific observation
  into a universal claim;
- compare that reconstruction with the source solution and record any omission,
  ambiguity, or correction in neutral language before adapting it;
- identify the one motivating question, the concrete example the viewer can
  manipulate, the boundary case that tests the idea, and the final realization
  the lesson should earn; and
- confirm what the reported permission actually covers. Keep source expression,
  downloaded media, trademarks, and third-party embeds outside the project
  licenses unless an exact rights record brings them into scope.

Put the source reconstruction and teaching rationale in `storyboard.md`; put
the independently checkable mathematical claim in `lesson.toml`. A public
video title, thumbnail, answer key, or plausible final answer is not enough
evidence to begin a finished deck. When the public source does not expose the
reasoning, keep the item `blocked` rather than reverse-engineering a solution
and attributing it to a source creator.

Treat filenames and page headings such as `解析` as labels, not content
evidence. Inspect the actual solution region: a PDF with blank worked areas can
locate the problem but cannot verify an argument. Conversely, one public video
may solve several identifiable problems. In that case create one lesson record
and one exact timestamp or chapter locator per problem while retaining a
single provider-asset record for the shared video.

Pin shared-video boundaries by inspecting frames on both sides of each problem
change. A coarse contact sheet is useful for discovery, but it is not an exact
locator: record the last settled source frame for one problem and the first
settled frame for the next, and describe any transition ambiguity instead of
inventing false precision. Store the reconciled locator in both collection and
lesson metadata.

Make the independent check genuinely independent of the source presentation
and scene code. Prefer exhaustive enumeration for finite cases, exact rational
coordinates for geometry, substitution for claimed roots, or symbolic bounds
that cover the full domain. A second copy of the same handwritten derivation is
not an independent check. Write the check before animation work when practical;
if it fails, stop the storyboard until the discrepancy is resolved.

When symmetry or periodicity reduces a moving configuration to a smaller
parameter interval, make the reduction itself part of the proof. Name the
motion that preserves the requested quantity, show how every original
parameter maps into the retained interval, and audit both endpoints. At an
endpoint, coincident support lines, merged vertices, or a lower-sided polygon
may make a generic interior formula degenerate; verify that case directly or
by a justified continuous limit instead of hiding it behind a symmetric
picture.

For a finite search, define the complete candidate universe before filtering
it. At each gate, say whether the condition is necessary, sufficient, or both,
and retain enough rejected context to show that every branch was accounted for.
Passing a congruence, inequality, or terminal-digit test does not prove a
candidate works; independently test every survivor against the original
conditions. Likewise, never accept the last visible card merely because the
others were crossed out. The final beat must substitute the survivor back into
the concrete object and recheck all requested properties.

For a minimum or maximum, separate the bound from attainment. A congruence,
counting inequality, or relaxation can rule values out without showing that
the surviving endpoint is legal. After deriving the bound, construct an exact
witness and replay every original constraint, including order-of-arrival,
distinctness, interiority, and conditional rules that may be vacuous at an
extreme. Give the witness its own visual beat; do not hide existence inside the
line that derives the bound.

When a source conclusion is correct only for the displayed construction family,
keep the result but narrow it honestly. Add a `solution_scope_note` to collection
metadata, state the extra assumption in the storyboard and presenter script,
and make that assumption visible before the conclusion. Do not silently promote
a same-ray, same-side, ordered, or positive-length result to an unrestricted
theorem.

## Repository Contract

Use a stable collection layout as the project grows:

- `catalog/`: the source-of-truth inventory and generated indexes;
- `lessons/<source-id>/<problem-id>/`: scene, presenter script, and lesson
  metadata for one problem;
- `src/math_manim/`: neutral public API for shared visual language, geometry
  helpers, and templates;
- `src/carlo_manim/`: QA-bound compatibility implementation for existing
  verified Carlo-source decks;
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
- canonical source page URL and exact solution locator or source-asset URL;
- content type, checksum for a downloaded source asset, and duplicate-of ID;
- an explicit Boolean eligibility decision and, when false outside a blocked
  state, the review reason;
- production state: `discovered`, `blocked`, `planned`, `storyboarded`,
  `math_verified`, `draft_rendered`, `visual_verified`, or `published`;
- scene class, presenter-script path, and build outputs;
- mathematical reviewer state and provenance/license scope.

For a Carlo-site-derived lesson, `source_asset_id`, `source_asset_sha256`,
`solution_asset_id`, and `solution_url` must reconcile against
`catalog/source_assets.json`: the solution must be confirmed public, both
assets must name the canonical source page, and the downloaded PDF checksum
must match. Its collection must also pin `source_page_sha256` to the frozen
record in `catalog/site_pages.json`. A working URL by itself is not sufficient
provenance.

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

Every problem record must carry `eligible = true` or `eligible = false`;
absence never means "not reviewed." Rendered states require `eligible = true`.
Use `eligible = false` plus `eligibility_reason` while public worked-content or
mathematical review is still pending, and use the explicit `blocked` state plus
`blocker_reason` when a named gate cannot currently be satisfied.

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
- Promote a helper into `math_manim` only after a second concrete lesson
  demonstrates the same behavior. Reuse primitives, not finished explanations.

## Parallel Production

- Assign one worker one problem directory at a time. A lesson worker may edit
  that directory and its generated, ignored render outputs, but must not edit
  the shared collection registry, README totals, licensing files, or unrelated
  lessons.
- The integrating worker reviews the rendered contact sheet, independently
  reconciles the lesson state into `collection.toml`, and runs the collection
  validator. This keeps concurrent state updates from overwriting one another.
- When several problem records share one solution asset, anchor every
  collection edit on the stable problem `id`, not the repeated provider ID or
  URL. Re-open the exact edited block before freezing QA; a syntactically valid
  patch can otherwise promote the neighboring problem and attach the wrong
  timestamp without producing a TOML error.
- A handoff must report the exact render command, segment count, loop result,
  mathematical check, visual inspection performed, and any unresolved caveat.
  A bare claim that a deck is complete is not an evidence gate.
- Lesson workers stop at `draft_rendered`. Only the integrating worker may set
  `visual_verified`, after independently opening the render, reconciling the
  collection state, and freezing a human-reviewed QA attestation.
- Production state and rights state are independent. Rendering a lesson may
  advance its production state; it must never advance `release_rights_state`
  or any source-permission state without a documented rights decision.
- Coordinate changes to shared helpers before editing them during parallel
  production. Prefer a local lesson primitive until repeated use and integration
  review justify promotion into `src/math_manim/`.
- Existing verified decks keep `carlo_manim` and `CarloSlide` until every
  affected deck is rerendered and visually reviewed. New decks use
  `math_manim` and `MathSlide`. The locked `carlo-math-slides` distribution
  identifier remains only because `pixi.toml` and `pixi.lock` are bound into
  every current QA attestation; changing it requires the same complete review.

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
- For a growing-pattern problem, build the first few cases from the same local
  rule, isolate exactly what one new step adds or hides, and only then write a
  recurrence or closed form. Check that form against an exact construction for
  the boundary case and several later cases; a plausible continuation of a
  small diagram is not proof. Audit perimeter, area, count, and overlap as
  separate quantities because the same added piece can change each one by a
  different amount.
- Delay equations until the corresponding visual relationship can already be
  pictured. Algebra should name and compress an idea, not introduce it cold.
- Plan a two-way translation between the concrete/spatial view and the symbolic
  or numerical view. After an equation compresses the picture, return its terms
  to the visible objects and use the original setup to check the result. A
  one-way replacement of a diagram by algebra is not visual explanation.
- Design the consolidation beat around an earned realization: the final result
  should resolve the opening question and make the route memorable.
- Preserve uncertainty long enough for the audience to reason. Do not place the
  final answer in an opening title, prefill it in the first diagram, or reveal
  it during a transition. Keep a settled pre-answer frame, then make the answer
  reveal its own deliberate event.
- Develop an original voice, pacing, composition, and color system. Reuse
  explanatory principles, never channel-specific artwork or mannerisms.

## Motion And Proof

- Every movement must answer the same question as the narration at that moment.
- Give every planned movement a one-sentence purpose in the storyboard. If the
  purpose cannot be named, remove the movement; moving text or equations merely
  to keep the screen active competes with the presenter rather than teaching.
- Choose motion states deliberately: generic, canonical, boundary/extreme, and
  mirrored states. Undirected roaming is not evidence.
- Freeze all variables except the one currently under study.
- Keep dependent geometry attached with updaters during exploration.
- Do not leave a permanent trace for an arbitrary exploratory path; it could be
  mistaken for the mathematical locus. A short dissipating trace is acceptable
  only when clearly useful.
- Preserve object identity through transforms. Prefer transforming a copy of a
  visible shape or label when deriving a new representation.
- If one algebraic symbol names a length, angle, or region in two diagrams,
  make the rendered objects genuinely equal in scene coordinates and carry the
  first into the second with `TransformFromCopy` or an explicit equality cue.
  Never draw unequal objects with the same label and ask narration to repair
  the contradiction. Keep their semantic color unchanged through every later
  formula and diagram.
- Establish symmetry with an explicit constraint-preserving map, not by saying
  that two shapes look alike. Show one arbitrary object and its reflected copy,
  show why the defining data are unchanged, and only then generalize.
- A visual argument must remain mathematically exact. Animation may motivate a
  claim, but must not conceal a missing boundary case or unjustified equality.
- Distinguish a point's drawn position from its permitted domain. If signed
  coordinates, directed lengths, opposite rays, or alternate orientations are
  mathematically possible, either test them or state the construction rule that
  excludes them before asserting uniqueness, minimality, or closure.
- Repetition must add evidence: for example, generic case, extreme case,
  reflected case, then a final replay. Do not repeat motion decoratively.

## Attention And Visual Language

- Keep reference geometry neutral and the current variable visually dominant.
- Give each mathematical role a stable semantic color across the whole lesson.
  A color used for a region or length in the diagram must carry into its formula
  term.
- Use opacity to focus attention while retaining useful context. Prefer dimming
  inactive construction lines to repeatedly clearing and rebuilding the scene.
- Dimming does not make spatial overlap acceptable. Before a final
  consolidation, either transform the existing cards, labels, or shapes into
  their final arrangement, or remove obsolete containers completely. Never
  stack a new answer group over a dimmed predecessor and leave duplicate values
  or intersecting outlines in the settled frame.
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
- Keep mathematical notation in `MathTex` and Traditional Chinese prose in the
  project `label()`/Manim `Text` layer. The pinned math fonts do not cover CJK;
  putting Chinese inside `\text{...}` can produce missing glyphs or fail only
  when a small TeX font size is requested. For a mixed sentence, arrange a CJK
  label and one or more symbolic `MathTex` objects as a group, then smoke-render
  the smallest formula size used by the scene.
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
pixi run manim-slides render --quality h --media_dir build/media/question_9 lessons/tcfs_115_math_gifted/q09/deck.py Question9Slide
pixi run manim-slides present Question9Slide
pixi run lessons export carlo.tcfs_115_math_gifted.q09
```

`--offline` describes the generated deck, not the conversion process. The
Manim Slides converter downloads Reveal.js assets from its configured CDN, so
run export with network access and then verify that the resulting one-file HTML
opens with networking disabled. Do not report a sandbox DNS failure as a
converter defect. Use the checked batch exporter rather than calling `convert`
directly: it pins the audited Reveal.js version, appends a legal appendix with
exact lesson provenance, and embeds the required third-party notices. The
generated appendix is deliberately outside the presenter-script
beat count but remains a normal navigable section so mobile scroll mode does
not omit it.

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

For the moving-point locus in
`lessons/tcfs_115_math_gifted/q09/deck.py`, preserve this order:

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
- In addition to endpoints, generate a fixed-cadence sweep of the complete
  movie (one frame per second is a useful default) and inspect the resulting
  dense sheet. Then sample more tightly around any transform that crosses a
  label, changes semantic text, or converges several moving objects.
- Sample intermediate frames for transformations whose source and target move
  across the diagram. Settled-frame QA cannot detect a label crossing another
  object halfway through an otherwise correct animation.
- When a semantic label changes, transform or remove the old label before the
  replacement appears. Never leave two versions occupying the same geometry;
  this commonly creates a visually plausible but unreadable composite string.
- Treat simultaneous `FadeOut`/`Write` or unrelated text transforms at one
  location as high-risk transitions. Sequence the old object fully out before
  the new one appears unless a tight multi-frame sweep proves there is no
  overprint, hybrid glyph, or momentary ambiguity; endpoint checks are not
  evidence for this case.
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

- Use the path-based split in `NOTICE.md`: project software is MIT under
  `LICENSE`; project-authored educational content and project-controlled
  renders are CC BY 4.0 under `LICENSE-CONTENT`.
- Treat both licenses as applying only to the exact project-controlled paths
  and contributions identified in `NOTICE.md`, never as blanket claims over
  the repository.
- Before incorporating an input, classify it as project-original,
  source-authorized, compatible third-party, reference-only, or excluded.
- Keep `SOURCES.md` or an equivalent generated source index with one canonical
  source URL and solution locator per lesson. Repeat the concise source credit
  in lesson metadata and the presenter script.
- Keep a public permission statement that names the role of the grantor, the
  grantee/project, material scope, allowed adaptation/publication, permitted
  licensing model, and date. State only facts supported by the permission; do
  not publish private messages, email addresses, signatures, or other personal
  correspondence.
- Permission from a site or channel owner does not automatically establish
  ownership of third-party exam statements, logos, fonts, photographs, linked
  documents, or 3Blue1Brown material. Link to those inputs and document their
  separate status unless the permission scope explicitly covers redistribution
  and relicensing.
- General permission to use or adapt material does not relicense the source.
  Apply CC BY 4.0 only to the project's own expression or to an adaptation the
  recorded permission actually authorizes. Unclear third-party scope fails
  closed and remains excluded.
- Do not copy web wording, diagrams, scans, images, code, audio, video, fonts,
  or logos merely because a source is cited. Independently express mathematical
  facts unless the recorded permission explicitly covers the adaptation.
- Do not copy 3Blue1Brown code, artwork, narration, or rendered assets into the
  project. Learn from its explanatory patterns and implement original scenes.
- Treat `3b1b/videos` as a research reference only: its scene repository is
  licensed CC BY-NC-SA 4.0, targets 3b1b's ManimGL workflow rather than Manim
  Community, and includes version-specific code. Do not port snippets or infer
  content-license compatibility from the MIT license of the Manim engine
  itself.
- CC BY attribution names this project and its contributors. Lesson-level
  source credit separately records whose solution was researched; never
  confuse source credit with the identity of the CC BY licensor.
- Add an explicit exception notice for every third-party input retained in the
  repository. Never place an MIT or CC BY claim over third-party material.
- Generated HTML and video may be described as CC BY only when every embedded
  input is project-controlled or separately compatible and correctly marked.
  Exported HTML must preserve bundled dependency notices.
- Treat raw MP4 segments and Slides manifests as internal build inputs unless a
  release package also carries `NOTICE.md` and the lesson's `SOURCES.md` entry.
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
- Before the first public push, inspect every reachable commit's author and
  committer identity. Confirm that each email address is intentionally public,
  or obtain explicit maintainer approval before rewriting history to a verified
  no-reply identity. Never expose a personal email merely because tracked file
  contents passed a secret scan.
- Treat any lesson whose `release_rights_state` is not `cleared` as a release
  blocker for promotion to `published`. A mixed-scope public repository must
  preserve the exact license map and exclusions in `NOTICE.md`.
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
- After publication, share the public repository URL with the Carlo site owner
  as requested in the recorded 2026-07-24 permission exchange. This is a
  maintainer follow-up, not a downstream CC BY condition.
- Follow `docs/PUBLISHING.md` for the preflight, identity decision, clean-tree
  audit, repository creation, and post-push verification. Stop at its identity
  checkpoint until the maintainer has chosen whether existing commit email
  addresses may be public or has approved rewriting them to the account's
  verified GitHub no-reply address.

## Research Basis

The guidance above adapts teaching principles and animation grammar from these
sources without copying their artwork, narration, or scene implementation:

- Carlo's Traditional Chinese mathematics resource and its concept-first,
  animated worked-example organization:
  https://sites.google.com/chjs.ntpc.edu.tw/carlovemath/
- 3Blue1Brown's official exposition advice:
  https://www.3blue1brown.com/about/
- A concrete geometric view translated back and forth with coordinates:
  https://www.3blue1brown.com/lessons/vectors/
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
- The checkpoint-oriented ManimGL production workflow, used only as workflow
  research rather than Community Edition code:
  https://www.3blue1brown.com/lessons/manim-demo/
- The separate license and compatibility boundary of 3Blue1Brown's scene code:
  https://github.com/3b1b/videos
- Manim Slides official documentation:
  https://manim-slides.eertmans.be/latest/
