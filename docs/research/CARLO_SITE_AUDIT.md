# Carlo Site Scope Audit

Snapshot date: 2026-07-24.

The discovery boundary is the public Google Site root plus every path exposed
by its navigation data. All 434 URLs returned HTTP 200. Page-body link review
found no additional first-party content path outside that boundary.

## Page partition

| Group | Pages |
| --- | ---: |
| Science-class archives | 118 |
| Gifted-class archives | 92 |
| Topical indexes | 129 |
| Competitions | 37 |
| Teacher recruitment | 16 |
| 清大數培 | 7 |
| 國中教育會考 | 4 |
| Curated/resources | 28 |
| Home/about | 3 |
| **Total** | **434** |

Of these, 391 pages contain embedded assets, 22 contain text or links only,
and 21 are empty or navigational shells. Exact page records live in
`catalog/site_taxonomy.json`.

## Asset boundary and access

The pages contain 4,346 unique provider IDs across 7,162 placements: 326 Drive
IDs and 4,020 YouTube IDs. The anonymous access audit found:

| Status | Assets |
| --- | ---: |
| Confirmed public | 2,489 |
| Confirmed restricted | 622 |
| Unresolved YouTube anti-bot challenge | 1,235 |
| **Total** | **4,346** |

Confirmed public consists of 325 Drive downloads and 2,164 playable YouTube
videos. Confirmed restricted consists of 607 member-only videos, 14 private
videos, and one auth-required Drive PDF. An oEmbed title is not proof of video
playability, so anti-bot results remain unresolved. Exact provider records live
in `catalog/source_access_audit.json`.

## Deduplication

There are 2,375 provider IDs on more than one page, representing 2,816 extra
page references. Most are intentional archive-to-topic relationships. The
catalog ingests each provider ID once and retains a many-to-many page/topic
map. No public Drive downloads share an exact SHA-256 digest. Same-title items
remain candidates, not duplicates, unless content evidence confirms identity.

## Eligibility

An embedded asset becomes production input only when access is confirmed
public, an identifiable problem and sufficiently reasoned solution can be
located, and provenance plus rights scope are documented. PDFs can contain
several lesson units; shell pages contain none. Consequently 4,346 is the
audited asset denominator, not a completed-lesson count.

## Problem-level review batches

The first site-derived problem decompositions cover three adjacent TCFSH
gifted-mathematics pages:

| Batch | Problem units | Public worked solutions | Current limitation |
| --- | ---: | ---: | --- |
| ROC 112 | 14 | 14 | Independent lesson mathematics and rendering remain pending |
| ROC 113 | 14 | 14 | Independent lesson mathematics and rendering remain pending by unit |
| ROC 114 | 14 | 4 | Ten solution videos are members-only and remain blocked |
| ROC 104 Chiayi science | 20 | 20 candidate mappings | Worked-content sufficiency and independent mathematics review pending |

ROC 112 and ROC 113 PDFs have blank areas beneath their `解析` headings. They
are problem-statement locators, not evidence of solution reasoning; the exact
public video mapping in each collection supplies that evidence. Paired ROC 113
videos are represented by two problem records pointing to one provider ID.
Provider-level deduplication is therefore preserved while lesson-unit counts
remain explicit.

Independent reconstruction of the ROC 113 proof unit also found a scope
boundary in its final generalization. The reported invariant `mn = 180` follows
the same-ray zigzag family drawn and extended in the public solution. Treating
the two supporting lines as unrestricted signed coordinates admits additional
closure angles, so a finished lesson must name the displayed same-ray
assumption rather than claim the invariant for every possible walk.

The 42 TCFSH records are a problem-level reviewed subset of the 2,489
confirmed-public asset pool. The 20 Chiayi records add an exact one-page and
one-numbered-video mapping, but remain `discovered` until the videos themselves
are inspected for sufficient reasoning. Neither group implies that every
public asset has been decomposed. The next-batch queue must still inspect each
PDF and video rather than deriving eligibility from titles or page co-location.

The separately supplied `數學-115數理資優學科能力評量答案.pdf` is outside this
site snapshot. The public 中一中資優 archive exposed by the crawl ends at ROC
114, so the ROC 115 collection is recorded as user supplied.
