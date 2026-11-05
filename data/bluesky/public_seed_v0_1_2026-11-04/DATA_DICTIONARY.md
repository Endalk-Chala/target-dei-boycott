# Data dictionary — public Bluesky seed v0.1

The CSV contains **one row per original Bluesky post rkey**. Not every row qualifies for the Target 2025 DEI boycott analytical corpus.

| Field | Meaning |
|---|---|
| Observation ID | Stable inventory identifier, BSKY-001 through BSKY-028 |
| Platform | Bluesky |
| Handle | Public reported account handle; may change |
| DID | AT Protocol account decentralized identifier from source page |
| Post rkey | Stable post record key on that account |
| UTC timestamp | Published timestamp displayed by original source page or recovered in the earlier audit; not necessarily identical to index timestamp |
| Research period | A: initial boycott (Jan 24–Apr 30, 2025); Middle: May 2025–Jan 2026; B: Feb–Mar 2026 |
| Primary post URL | Direct post link |
| Original-source text (≤23-word excerpt) | Exact limited extract, not a paraphrase; **not always the full post** |
| Text capture completeness | Complete short visible body versus excerpt only |
| Original visible word count | Count recorded during original source observation, approximate |
| Actor / voice | Preliminary researcher description, not validated human coding |
| Issue match | Preliminary researcher topic categorization |
| Screening disposition | Proposed decision; remains conditional until independent review |
| Evidence captured from | Earlier web-source review or direct page access |
| Content / ethics note | Reasons to withhold, verify, disambiguate, or classify |
| Embedded media reviewed? | Whether attached media or quote post was opened (typically No) |
| Independent audiovisual content review? | Not completed / not applicable |
| Collection date | Research observation date, **not** a post publication date |

**Interpretation rule:** Do not compute frame prevalence, affect counts or any inferential comparison using these draft classifications. Record the outcome of a human relevance screen and any coder disagreements separately. Do not treat news redistribution as an independent consumer attitude.
