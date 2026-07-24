# Catalog

This directory is the source of truth for collection scope.

`site_pages.json` inventories public navigation pages and embedded source
assets discovered from Carlo's Math site. A page or embedded file is not
automatically an eligible lesson. Problem-level lesson records must separately
identify the exact problem, solution, provenance, permission scope, and
production state.

`audit_summary.json` records the frozen 2026-07-24 access and taxonomy audit.
It distinguishes confirmed public, confirmed restricted, and unresolved
anti-bot-challenge assets. `source_assets.json` retains each unique provider ID
once, together with all source pages where it occurs.

`source_access_audit.json` stores the corresponding status for every provider
ID. It is deliberately snapshot-based: access can change, and a future audit
must record a new date rather than silently rewriting historical evidence.

`site_taxonomy.json` preserves the reviewed section, audience, exam, topic,
content status, and asset counts for all 434 pages. Landing and shell pages
remain taxonomy records; they are not lesson units.

The supplied ROC 115 TCFSH assessment PDF used by the reference lesson is not
one of the embedded assets in this site snapshot. Its lesson metadata and
provenance record must describe it as a separately supplied source.

Regenerate the site inventory with:

```bash
pixi run inventory-site
```

Never edit generated counts in documentation by hand. Generate them from the
catalog and preserve blocked or excluded entries with explicit reasons.
