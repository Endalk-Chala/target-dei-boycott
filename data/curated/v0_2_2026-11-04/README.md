# Brand Covenant Broken — Curated Cross-Platform Source Inventory, v0.2

**Release compiled:** November 4, 2026 (America/Chicago)  
**Researcher:** Endalkachew H. Chala, PhD  
**Working paper status:** **In preparation. Not submitted, accepted, or peer reviewed.**

## Start here

**[master_source_inventory.csv](master_source_inventory.csv)** is the canonical deduplicated index across platforms. Each row is one *distinct linked source object*, **not** a verified relevant observation and **not** a completed coded unit.

| Platform | Distinct objects | What is actually documented |
|---|---:|---|
| TikTok | 37 | Video URLs/IDs; dates estimated from IDs or secondary sources; zero playback/transcript reviews. Includes 36 tracker videos and one additional Target corporate ad lead from the cross-platform audit. |
| Bluesky | 28 | Public original post pages and timestamps; 14 complete very short texts, 14 short excerpts only. No successful bulk API harvest. |
| YouTube | 18 | Video IDs, indexed titles/channel/date signals. Videos and transcripts not independently reviewed; zero YouTube API harvests. |
| Instagram | 7 | Original post/Reel URLs from contemporaneous reporting; content not directly reviewed. |
| Facebook | 2 | Original post/Reel URLs from contemporaneous reporting; content not directly reviewed. |
| News-hosted video | 1 | Original publisher video page; content not independently reviewed. |
| **TOTAL** | **93** | **Zero formally coded observations, no reliability statistics.** |

**Not included as posts:** X/Twitter had no independently recovered post-level records in this dataset. A blank platform is not evidence the campaign was absent there.

## Canonical data files

- [master_source_inventory.csv](master_source_inventory.csv) — 93 deduplicated source-linked objects (one common schema).
- [tiktok_video_leads.csv](tiktok_video_leads.csv) — 37 video-ID leads, including the 8 additional user-submitted links and one official Target promotion. **No original video playback.**
- [bluesky_original_post_seed.csv](bluesky_original_post_seed.csv) — 28 original post pages, with short verbatim excerpts. Seven previously considered provisionally relevant pending independent manual screening; there is no final inclusion sample.
- [youtube_video_metadata_leads.csv](youtube_video_metadata_leads.csv) — 18 unique YouTube video IDs with recorded metadata signals (not official API results).
- [instagram_facebook_and_news_leads.csv](instagram_facebook_and_news_leads.csv) — seven Instagram, two Facebook, one news-hosted video source object.
- [corporate_primary_document_leads.csv](corporate_primary_document_leads.csv) — four source-linked corporate primary-document context leads requiring historical-version verification.
- [campaign_event_timeline.csv](campaign_event_timeline.csv) — 27 contextual event records; many rely on news reporting. **Not 27 independent videos or original posts.**
- [context_sources.csv](context_sources.csv) — ten contextual citations, not ten coded observations.
- [preliminary_codebook_variables.csv](preliminary_codebook_variables.csv) — candidate coding variables, not actual coding results.
- [historical_web_search_log.csv](historical_web_search_log.csv) — older web-search audit; not TikTok-platform searches.
- [manifest.json](manifest.json) — machine-readable counts/status.
- [DATA_DICTIONARY.md](DATA_DICTIONARY.md) — field definitions.
- [COLLECTION_AND_SCREENING.md](COLLECTION_AND_SCREENING.md) — data source audit and strict validity limits.
- [collect_target_youtube_api.py](collect_target_youtube_api.py) — **unexecuted** public YouTube API collection script requiring an API key.

## Prior project resources retained (not overwritten)

- [Corporate communications working XLSX](../../Target_Corporate_Comms_Dataset.xlsx) — pre-existing source spreadsheet; **not independently audited or recoded in this release**.
- [TikTok discovery Batch 03](../../tiktok_discovery/batch03_2026-11-04/) — older 28-lead exploratory archive, retained for provenance. The **37-lead curated list here supersedes the counts from that batch**, but original files remain.
- [Bluesky initial v0.1](../../bluesky/public_seed_v0_1_2026-11-04/) — original seed and previously prepared API script.
- [TikTok systematic search matrix](../../tiktok_discovery/systematic_collection_v1_2026-11-04/) — an unexecuted TikTok on-platform search plan.
- [Codebook DOCX and coding template XLSX](../../../codebook/) — earlier instruments, not a coded dataset.

## Counting and deduplication

Deduplicated by **(platform, native post/video ID)**. Original URLs are retained. Duplicate YouTube records present in both the YouTube inventory and earlier cross-platform collection were merged and their CP record IDs retained in the `legacy_record_ids` column. The 17 prior Bluesky cross-platform references are covered by the 28-row Bluesky collection; they are not counted again. Corporate Instagram and Facebook advertising that may be the same creative are **two platform posts**, not two independent campaign claims. Cross-platform repost identity has not been independently tested.

## Study windows (date signals provisional)

- A: January 24–April 30, 2025 (initial boycott).
- Middle: May 1, 2025–January 31, 2026 (continuity, contextual).
- B: February 1–March 31, 2026 (later boycott).

A TikTok `date_signal` is generally inferred from the numeric video ID; it is **not proof of the publication date**. A YouTube date may reflect the date of an event rather than publication. **Original dates require source-level validation before final temporal analysis.** Outside-period leads remain for provenance, not as automatically eligible observations.

## Ethics and scholarly use

- These data are source-link and limited-excerpt research materials. Public posts may identify private people and concern their expressed views about corporations and public policy. Do not bulk republish full user content without a privacy/ethics assessment and platform-terms review.
- No generalizable claims about platform-level public opinion, framing prevalence or engagement can be made from these convenience-indexed leads.
- Only original content after independent verification, eligibility screening, a defined sampling protocol and proper coding can support manuscript findings.
- The repositories and datasets are not an endorsement of, or opposition to, any boycott. They record available source material for scholarly analysis.

## Accurate description for faculty applications

> *Brand Covenant Broken* (manuscript in preparation) examines how publics and corporate actors contested Target's 2025 DEI commitments, supported by a versioned, open cross-platform source inventory, preliminary codebook, and reproducible public-data collection protocols.

**Do not describe this as a 93-post analyzed sample, an API-collected dataset, or a manuscript submitted to *Public Relations Review*.**

Citation (working data): Chala, E. H. (2026). *Brand Covenant Broken: Curated cross-platform source inventory* (v0.2) [Working research data]. GitHub. https://github.com/Endalk-Chala/target-dei-boycott