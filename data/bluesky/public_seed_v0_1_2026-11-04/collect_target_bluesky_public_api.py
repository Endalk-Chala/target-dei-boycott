#!/usr/bin/env python3
"""Read-only Bluesky public API collector for the Target DEI boycott project.

Run locally (where https://api.bsky.app is accessible):
    python -m pip install requests
    python collect_target_bluesky_public_api.py \
        --seed bluesky_posts_seed.csv \
        --output target_bluesky_api_collection.csv

Does NOT run in the ChatGPT execution environment when outbound requests are blocked.
Unscreened results are only a discovery frame; original text and engagements
must be ethically reviewed before coding. Preserve raw CSV privately.
"""
from __future__ import annotations
import argparse
import csv
from datetime import datetime, timezone, timedelta
import json
import pathlib
import sys
import time
from urllib.parse import quote
import requests

BASE = "https://api.bsky.app/xrpc"
FALLBACK = "https://public.api.bsky.app/xrpc"
QUERIES = ["Target boycott", "Target DEI", "#BoycottTarget", '"Target Fast"',
           '"Target" "DEI"', '"Target" "belonging"']
WINDOWS = [
    ("A_2025_01_24_02_28", "2025-01-24T00:00:00Z", "2025-03-01T00:00:00Z"),
    ("A_2025_03", "2025-03-01T00:00:00Z", "2025-04-01T00:00:00Z"),
    ("A_2025_04", "2025-04-01T00:00:00Z", "2025-05-01T00:00:00Z"),
    ("M_2025_05_06", "2025-05-01T00:00:00Z", "2025-07-01T00:00:00Z"),
    ("M_2025_07_09", "2025-07-01T00:00:00Z", "2025-10-01T00:00:00Z"),
    ("M_2025_10_12", "2025-10-01T00:00:00Z", "2026-01-01T00:00:00Z"),
    ("M_2026_01", "2026-01-01T00:00:00Z", "2026-02-01T00:00:00Z"),
    ("B_2026_02", "2026-02-01T00:00:00Z", "2026-03-01T00:00:00Z"),
    ("B_2026_03", "2026-03-01T00:00:00Z", "2026-04-01T00:00:00Z"),
]
COLS = ["uri", "cid", "post_url", "handle", "did", "post_rkey", "created_at",
        "indexed_at", "text", "lang", "like_count", "repost_count", "reply_count",
        "quote_count", "retrieved_utc", "search_queries", "search_windows", "status"]


def get_json(session, base, endpoint, params, max_retries=2):
    url = base + "/" + endpoint
    for attempt in range(max_retries + 1):
        try:
            r = session.get(url, params=params, timeout=25)
            if r.status_code in (401, 403):
                raise RuntimeError(f"Public API denied {r.status_code} on {url}. Use authorized access; do not bypass restrictions.")
            if r.status_code == 429:
                pause = min(int(r.headers.get("Retry-After", "20")), 120)
                if attempt < max_retries:
                    time.sleep(pause)
                    continue
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            if attempt == max_retries:
                raise
            time.sleep(3 * (attempt + 1))


def iso_utc(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError:
        return None


def post_row(p):
    uri = p.get("uri", "")
    author = p.get("author") or {}
    record = p.get("record") or {}
    rkey = uri.rsplit("/", 1)[-1]
    handle = author.get("handle") or ""
    return {
        "uri": uri, "cid": p.get("cid", ""),
        "post_url": f"https://bsky.app/profile/{handle}/post/{rkey}" if handle and rkey else "",
        "handle": handle, "did": author.get("did") or "", "post_rkey": rkey,
        "created_at": record.get("createdAt") or "", "indexed_at": p.get("indexedAt") or "",
        "text": record.get("text") or "", "lang": ",".join(record.get("langs") or []),
        "like_count": p.get("likeCount"), "repost_count": p.get("repostCount"),
        "reply_count": p.get("replyCount"), "quote_count": p.get("quoteCount"),
        "retrieved_utc": datetime.now(timezone.utc).isoformat(), "search_queries": "",
        "search_windows": "", "status": "UNSCREENED_API_ORIGINAL",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--seed", help="Optional CSV file with DID and Post rkey columns to retrieve known posts")
    ap.add_argument("--output", default="target_bluesky_api_collection.csv")
    ap.add_argument("--max-per-query", type=int, default=300)
    ap.add_argument("--delay", type=float, default=1.7)
    args = ap.parse_args()
    if args.max_per_query < 1 or args.max_per_query > 1000 or args.delay < 1:
        ap.error("Use 1 <= max-per-query <= 1000 and delay >= 1 second")
    session = requests.Session()
    session.headers["User-Agent"] = "AcademicReadOnlyTargetDEIBoycottResearch/1.0"
    results = {}
    log = []
    # Recover exact originals for known seeds via getPosts, in batches of <=25.
    if args.seed:
        with open(args.seed, newline="", encoding="utf-8-sig") as f:
            seed = list(csv.DictReader(f))
        at_uris = [f"at://{r['DID']}/app.bsky.feed.post/{r['Post rkey']}" for r in seed if r.get('DID') and r.get('Post rkey')]
        for i in range(0, len(at_uris), 25):
            params=[("uris",u) for u in at_uris[i:i+25]]
            try:
                block=get_json(session, FALLBACK, "app.bsky.feed.getPosts", params)
                for p in block.get("posts", []):
                    row=post_row(p)
                    results[row["uri"]] = row
                log.append({"task":"seed", "count":len(block.get("posts", []))})
            except Exception as e:
                log.append({"task":"seed", "error":str(e)})
            time.sleep(args.delay)
    for label, since, until in WINDOWS:
        floor=iso_utc(since)
        for query in QUERIES:
            end=until
            collected=0
            failed=""
            for page in range(1, 15):
                if collected >= args.max_per_query:
                    break
                params={"q":query, "sort":"latest", "limit":min(100,args.max_per_query-collected),
                        "since":since, "until":end}
                try:
                    obj=get_json(session, BASE, "app.bsky.feed.searchPosts", params)
                    found=obj.get("posts", [])
                except Exception as e:
                    failed=str(e)
                    break
                if not found:
                    break
                timestamps=[]
                for p in found:
                    row=post_row(p)
                    dt=iso_utc(row["created_at"] or row["indexed_at"])
                    if dt and (dt < floor or dt >= iso_utc(until)):
                        continue
                    u=row["uri"]
                    if not u:
                        continue
                    if u not in results:
                        results[u]=row
                    if query not in results[u]["search_queries"].split(" | "):
                        results[u]["search_queries"]=(results[u]["search_queries"] + " | " + query).strip(" | ")
                    if label not in results[u]["search_windows"].split(" | "):
                        results[u]["search_windows"]=(results[u]["search_windows"] + " | " + label).strip(" | ")
                    if dt:
                        timestamps.append(dt)
                collected += len(found)
                if not timestamps:
                    break
                oldest=min(timestamps)
                next_end=(oldest-timedelta(milliseconds=1)).isoformat().replace("+00:00", "Z")
                if next_end >= end or oldest <= floor:
                    break
                end=next_end
                time.sleep(args.delay)
            log.append({"task":f"{label}:{query}", "records_seen":collected, "error":failed})
            print(f"{label} {query}: {collected} returned; {len(results)} unique overall",file=sys.stderr)
            time.sleep(args.delay)
    target=pathlib.Path(args.output)
    target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("w",newline="",encoding="utf-8-sig") as f:
        wr=csv.DictWriter(f,fieldnames=COLS)
        wr.writeheader()
        wr.writerows(results.values())
    with target.with_suffix(".search_log.json").open("w",encoding="utf-8") as f:
        json.dump(log,f,indent=2)
    print(f"Saved {len(results)} unique UNCLASSIFIED original Bluesky posts to {target}")
    print("Do not publish identifiable content or infer representativeness without ethical review and screening.")

if __name__=="__main__":
    main()