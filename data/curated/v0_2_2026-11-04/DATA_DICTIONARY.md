# Data dictionary — curated public-source inventory v0.2

The common schema is used in `master_source_inventory.csv` and each platform-specific CSV.

| Column | Definition |
|---|---|
| `record_id` | Stable project lead ID; TikTok `TGT-USER` records distinguish researcher-added user links from earlier web-indexed leads. |
| `platform` | Site or source type; `News video` is a publisher video page, not YouTube or social media. |
| `platform_post_id` | Native platform ID where recoverable; Bluesky uses DID + post rkey. |
| `account_or_channel` | Public creator, official account, publisher, or channel as recorded in prior files. |
| `post_url` | Source-linked original-object URL; no guarantee the item is still publicly accessible. |
| `date_signal` | A supplied original-source timestamp, indexed signal, reported date, or **TikTok ID-derived estimate**. |
| `date_basis` | Strength/meaning of date evidence. The value must not be silently treated as verified publication date. |
| `study_period_provisional` | Phase A, middle/continuity, phase B, outside window, or undetermined. Derived from `date_signal` and thus provisional. |
| `unit_type` | Media or communication category, e.g. creator video, corporate ad, news commentary. May require recoding after content review. |
| `source_description_not_transcript` | Brief discovery synopsis or indexed title, **not** a primary video transcript and not coder-assessed content. |
| `available_original_text_excerpt` | Short exact snippet from a previously accessed original Bluesky post page, capped at 23 words; may not represent the full post. |
| `text_capture_status` | Original text completeness: 14 short posts complete, 14 excerpt-only; other platforms not collected. |
| `evidence_status` | What was actually retrieved/reviewed (source-linked text, indexed metadata, or link only). |
| `source_provenance_url` | Web article or original post that supported the lead; may be secondary reporting. |
| `primary_provenance_record` | Parent collection workbook or inventory. |
| `legacy_record_ids` | Identifiers from older datasets merged into this row to document deduplication. |
| `topic_screen_provisional` | Previous rough relevance/disposition. **Not** a final inclusion decision or coded result. |
| `video_watched` | No for every TikTok and YouTube item in this release. |
| `transcript_checked` | No for every TikTok and YouTube item in this release. |
| `formal_coding_completed` | No for every item in this release. |
| `notes` | Evidence, context, screening caveats, media limitations. |

`corporate_primary_document_leads.csv` is a short list of original corporate-document URLs found in the event timeline, not a new full corporate text corpus. The existing [corporate communications dataset](../../Target_Corporate_Comms_Dataset.xlsx) remains a separate legacy working file.

## Provenance caveats

`post_url` and `platform_post_id` were deduplicated, not all re-fetched in this release. `date_signal` may describe an event date instead of the underlying upload. Direct media playback, transcripts, and complete API responses are unavailable in this release. Any statistical comparison needs a newly defined and implemented sampling/coding step.