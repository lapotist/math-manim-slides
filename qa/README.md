# QA Evidence

This directory stores compact release evidence for lessons marked
`visual_verified` or `published`. Videos, contact sheets, and Manim Slides
manifests remain generated files under ignored directories.

Each JSON attestation is produced from a clean `qa-slides` report only after a
human has inspected the contact sheet, every dense frame at full resolution,
and relevant transition frames. It binds that review to SHA-256 hashes of the
lesson metadata, scene, presenter script, storyboard, Slides manifest, every
rendered segment, and the pinned Pixi toolchain. Later source or render changes
therefore invalidate the evidence during catalog validation. Ignored render
files remain reproducible locally; their recorded hashes preserve the exact
reviewed-artifact identity in a clean clone.

Regenerate evidence only after rerendering and repeating human review:

```bash
pixi run freeze-qa --human-reviewed carlo.tcfs_115_math_gifted.q09
```
