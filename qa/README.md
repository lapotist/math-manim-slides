# QA Evidence

This directory stores compact release evidence for lessons marked
`visual_verified` or `published`. Videos, contact sheets, and Manim Slides
manifests remain generated files under ignored directories.

Each JSON attestation is produced from a clean `qa-slides` report only after a
human has inspected the settled-frame contact sheet, the fixed-cadence
transition sweep, every dense frame at full resolution, and relevant
transition frames. It binds that review to SHA-256 hashes of the
lesson metadata, scene, presenter script, storyboard, Slides manifest, every
rendered segment, and the pinned Pixi toolchain. Later source or render changes
therefore invalidate the evidence during catalog validation. Ignored render
files remain reproducible locally; their recorded hashes preserve the exact
reviewed-artifact identity in a clean clone.

Regenerate evidence only after rerendering and repeating human review:

```bash
pixi run freeze-qa --human-reviewed carlo.tcfs_115_math_gifted.q09
```

The loopback verifier (`pixi run review-slides`) stores in-progress decisions
under ignored `build/reviews/`. Those source-bound receipts help complete the
human pass but are not attestations. `freeze-qa` now requires a current receipt
whose every segment and lesson criterion passes; the command still creates the
formal attestation only after the lesson metadata has advanced to a verified
production state.

The verifier also writes sanitized progress to `qa/review-status.json` for the
public player. That generated feed contains only status, counts, timestamps,
and a stable evidence digest. It never contains reviewer notes and never turns
`review_complete` into formal `verified` status.

Project-authored review prose in these attestations is CC BY 4.0 under
`NOTICE.md`. Hashes, paths, dimensions, and other facts are evidence rather
than a license claim over the lesson sources or bundled dependencies.
