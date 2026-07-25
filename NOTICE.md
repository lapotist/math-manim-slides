# Split License Scope And Exclusions

This repository uses a path-based split license. The licenses apply only to
material controlled by this project's contributors; they do not relicense
third-party source material named, linked, or described in the repository.

Repository revisions through commit `56b0cf6` used a CC0 notice for a limited
set of project-authored paths. Nothing in this migration attempts to withdraw
any rights that were effectively granted for those earlier revisions. The
separate MIT and CC BY 4.0 grants below govern the current revision and later
contributions unless a later notice says otherwise.

The project is now named *Math Manim Slides*. Earlier revisions and existing
render metadata may identify it as *Carlo Math Manim Slides*; both names refer
to the same contributor project, not to Carlo or any source owner as licensor.

## MIT Software

The MIT License in `LICENSE` applies to the project-authored software and
software-support files in these paths:

- `src/math_manim/`
- `src/carlo_manim/` (QA-bound compatibility API)
- `scripts/`
- `tests/`
- `tools/`
- `lessons/**/deck.py`
- `.gitignore`
- `pyproject.toml`
- `pixi.toml`

The Manim scene files are executable software under MIT. A render produced by
those files is educational media covered by the content license below to the
extent the render contains only project-controlled material.

## CC BY 4.0 Content

The Creative Commons Attribution 4.0 International license in
`LICENSE-CONTENT` applies to the project-authored educational expression,
documentation, selection and arrangement, and original visual composition in:

- `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, `NOTICE.md`, `SOURCES.md`,
  and `THIRD_PARTY.md`;
- `lessons/`, except `deck.py` files covered by MIT above;
- `docs/`, including project-created render previews;
- `catalog/` and `qa/`, to the extent their prose, review notes, or selection
  and arrangement are protected;
- project-authored teaching media generated under `build/media/`,
  `slides/files/`, or `media/`, when it contains no excluded input; and
- the project-authored lesson media and scoped attribution section in
  `dist/**/*.html`; bundled dependency code remains excluded below.

When an output is copied to another release path, distribute `NOTICE.md` and
the relevant `SOURCES.md` entry with it. Standalone HTML exports carry their
own generated attribution/source appendix and embedded dependency notices. Raw
MP4 segments and Slides manifests are build inputs, not self-attributing
standalone release artifacts; package them with `NOTICE.md` and the relevant
`SOURCES.md` entry if they are distributed separately. No artifact-level notice
converts bundled third-party material into CC BY content.

In mixed metadata and evidence files, factual identifiers, URLs, hashes,
mathematical facts, third-party titles, and third-party material remain outside
the CC BY grant. The license applies only to the contributors' protectable
contributions.

When sharing CC BY material, retain this attribution in a reasonable form:

> Math Manim Slides contributors, *Math Manim Slides*, licensed
> under CC BY 4.0. Retain the lesson-specific solution provenance in
> `SOURCES.md` and indicate whether you made changes.

Also retain a link to <https://creativecommons.org/licenses/by/4.0/> and, where
practicable, the repository or release URL from which the material was
obtained. Lesson source credit identifies research provenance; it does not
identify Carlo or a school as the CC BY licensor of this project's content.

## Not Relicensed

Neither project license covers rights the contributors do not control,
including:

- source PDFs, PowerPoint files, scans, question sheets, answer sheets,
  downloaded website assets, source video, source audio, or source frames;
- third-party wording, diagrams, photographs, artwork, fonts, logos,
  trademarks, names, and publisher or school branding;
- Carlo, 3Blue1Brown, school, contest, or other third-party material merely
  cited, linked, cataloged, or used for research;
- dependency code, package contents, `pixi.lock` dependency metadata, and
  files carrying their own license or notice; and
- Reveal.js or other dependency assets bundled into an exported HTML file.

`LICENSES/` contains verbatim upstream notices for dependencies embedded by
the standalone exporter. Those notices retain their upstream status and are
not grants by this project's contributors.

Those materials retain their original status and terms. `SOURCES.md` records
research provenance, while `THIRD_PARTY.md` records known runtime-license
boundaries. Public availability is not treated as permission to redistribute
or relicense a source.

The project is independent and is not endorsed by Carlo, 3Blue1Brown, Manim,
Manim Slides, any school, publisher, or contest organizer.
