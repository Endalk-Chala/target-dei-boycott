# Brand Covenant Broken — Bluesky public-source research snapshot v0.1
**Released:** 2026-11-04 · **Research status:** In progress · **Principal investigator:** Endalkachew H. Chala, PhD

This is an **open, versioned research discovery/verification seed**, not a completed analytical dataset or a journal publication.

## What is in this release?

- **28 unique original Bluesky post links and post identifiers** (27 previously recovered; one additional source page checked on Nov 4).
- Source-derived UTC timestamps, author handles and public DIDs, short excerpts (maximum 23 words), provenance, and preliminary research screening decisions.
- **14 very short post bodies fully represented; 14 excerpt-only records.** The full text of excerpt-only posts is *not* in this CSV and must be checked at the original link or retrieved through the public API.
- **7** records provisionally flagged for inclusion pending further topic and context screening.
- **0** formally coded observations and **0** observations collected through a successful live API request in this run.
- **2** entries from Feb–Mar 2026: these do not constitute a usable consumer comparison sample; one concerns a separate ICE-related campaign.

The files are **not** an exhaustive search or a representative sample. Public search-engine discovery is selective and can overrepresent prominent accounts, news sharing, and indexable material.

## Files
- [bluesky_posts_seed.csv](bluesky_posts_seed.csv) — source-linked individual post leads and preliminary decisions.
- [collect_target_bluesky_public_api.py](collect_target_bluesky_public_api.py) — read-only API retrieval script for a network-connected computer.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — field definitions and screening codes.
- [COLLECTION_PROTOCOL.md](COLLECTION_PROTOCOL.md) — study periods, proposed queries, methodological controls and ethical safeguards.

## Run the public API collector
From this directory on a machine with network access:
```bash
python -m pip install requests
python collect_target_bluesky_public_api.py --seed bluesky_posts_seed.csv --output bluesky_api_raw_private.csv --max-per-query 300
```
The script is **prepared but was not run successfully in this research environment**. Bluesky public search behavior, pagination, limits, and access rules may change; inspect its log before drawing conclusions. Do not publish unreviewed full post bodies automatically.

## Related project data
- [TikTok source leads, Batch 03](../../tiktok_discovery/batch03_2026-11-04/) — 28 exact-ID discovery leads, *not* watched or coded video observations.
- [Systematic TikTok search protocol](../../tiktok_discovery/systematic_collection_v1_2026-11-04/) — search plan, *not* an executed TikTok platform harvest.
- [Research profile](../../../..//paper/WORKING_PAPER_PROFILE_2026-11-04.md) — theory and ongoing study status.

## How to describe the release in applications
**Accurate:** "Developing an openly documented cross-platform case study of Target's 2025 DEI rollback and consumer boycott, with versioned public-source data inventories, source-level provenance and a reproducible Bluesky API collector."

**Not accurate:** "300 TikTok posts analyzed," "API-collected cross-platform sample," "intercoder reliability completed," or "paper accepted/submitted to Public Relations Review."

## Research ethics
Ordinary users expressed politically sensitive viewpoints. This public seed minimizes quotation to short excerpts and links, and does not redistribute media. Follow institutional IRB/data governance guidance, platform terms, and scholarly anonymization practices before publishing full transcripts or individual-level coding.

**Cite the current working snapshot:** Chala, E. H. (2026). *Brand Covenant Broken: Bluesky public-source research snapshot, v0.1* [Working research data]. GitHub. https://github.com/Endalk-Chala/target-dei-boycott
