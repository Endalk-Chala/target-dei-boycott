# Collection, limitations and next validation steps

## How this v0.2 release was built

Inputs available on November 4, 2026:
1. TikTok verification-intake v3 (36 original exact-ID leads, including 8 links supplied directly by the researcher).
2. TikTok Batch03 28-video lead log (secondary-source synopsis and provenance for older video IDs).
3. Public Bluesky source-data seed v0.1 (28 original URLs with 23-word maximum excerpts).
4. YouTube Batch01 inventory (18 video IDs and indexed metadata or earlier leads).
5. Cross-platform Batch01 (36 records; 17 Bluesky references, eight YouTube items, seven Instagram posts, two Facebook posts, one Target TikTok, and one news video).
6. Contextual event timeline, corporate-source links, source bibliography, codebook variables and web search log.

We used native platform IDs to remove **within-platform** duplicate entries. We did **not** treat identical creative placed on different platforms as one post; platform-level objects and engagement need independent inspection.

## Actual verification thresholds

| Level | Meaning | Current coverage |
|---|---|---|
| D0 — Source discovery | A stable-looking original URL/ID discovered from index, reporting, or user. | All 93 inventory objects. |
| D1 — Original text accessed | Original public text displayed; some longer records preserved only as excerpts. | 28 Bluesky original pages, with mixed full/excerpt completeness. |
| D2 — Original audiovisual content reviewed | Full original video watched or transcript verified, upload date checked. | **0 TikTok and YouTube videos.** |
| D3 — Analytic eligibility confirmed | Source meets predefined sampling/inclusion rules after independent content review. | **0 final inclusion decisions**; seven preliminary Bluesky recommendations are not final. |
| D4 — Formal content coding and reliability | Final codebook, actual coded observations and reliability audit. | **0 completed.** |

TikTok's numerical IDs embed an approximate creation-time signal, but this is **not confirmed upload time**; it must not be used as the final date for inferential longitudinal comparisons. YouTube records contain indexed video dates and some event dates; they are not direct API export rows. No official Bluesky or YouTube API harvest ran in this snapshot.

## Risks and methodological guardrails

- Search-engine discovery is biased toward indexable, often popular English-language items. It is not a random or exhaustive platform sample.
- Original posts and news reports about posts are separate evidence types. Public commentary on an official Target advertisement is a different analytic unit from the advertisement itself.
- Different campaign coalitions are related but not identical; distinguish initial Minnesota organizers and the Target Fast initiative.
- The 2025 DEI rollback boycott, 2023 Pride-related Target controversy and 2026 ICE-related boycotts must be screened separately, except when an original post clearly bridges topics.
- Record failed accesses, deletions, non-English language, edits, comments vs video, source date mismatches, and duplicate mirror links.
- Ordinary users' public social-media political/brand views can be sensitive. Consult relevant institutional guidance, follow platform terms, and avoid unnecessary disclosure of identifying details in analysis outputs.

## Practical next steps

1. Review the canonical CSV, verify original links, and save exact screenshots/captions/transcripts only in an appropriate access-controlled working store.
2. Run the open Bluesky public API script on a connected machine and preserve API JSON + run logs. Label the newly obtained result as API data **only after successful execution**.
3. Run the YouTube API collector with an API key; verify exact `publishedAt` against prior indexed/event dates.
4. Verify TikTok videos manually and mark missing, unrelated, relevant, or contested. Don't silently substitute source-media descriptions for video content.
5. Fix sampling and study windows before final eligibility screening; pilot and refine the codebook; then conduct formal coding with a reliability check.
6. Use the dated GitHub commit as a frozen citation for academic job materials; revise the research status only when milestones are actually completed.