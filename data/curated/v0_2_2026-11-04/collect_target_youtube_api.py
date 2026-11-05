#!/usr/bin/env python3
"""Brand Covenant Broken — read-only public YouTube Data API collector.

Requirements: Python 3.9+ (standard library only), a YouTube Data API v3 key.
Run:
    export YOUTUBE_API_KEY="YOUR_KEY"   # never commit this key
    python collect_target_youtube_api.py --output-dir ./youtube_api_run

The collector records *search retrieval*, not a representative YouTube census.
It collects video metadata. It DOES NOT download or view video content,
download captions, or code sentiment, affect, identity or frames.
"""
import argparse, csv, datetime as dt, json, os, pathlib, sys, time
import urllib.parse, urllib.request, urllib.error

API_ROOT="https://www.googleapis.com/youtube/v3"
STRATA=[
  ("A_initial","2025-01-24","2025-04-30",
   ["Target DEI boycott Minneapolis","Target boycott Target Fast",
    "Target boycott Black owned business","Target boycott opposing opinion",
    "Target boycott corporate advertising","Target boycott community organizers"]),
  ("Middle_continuity","2025-05-01","2026-01-31",
   ["Target boycott continuing","Target boycott supplier businesses",
    "Target boycott Cornell Fiddelke","Target boycott brand trust",
    "Target Fast town hall","Target boycott Minnesota organizers"]),
  ("B_late","2026-02-01","2026-03-31",
   ["Target boycott March 2026","Target Fast ends 2026",
    "Minnesota Target boycott continues","Target boycott accountability",
    "Target DEI boycott organizers 2026","Target boycott Black business 2026"])
]

def api_get(endpoint, params, key):
    p=dict(params);p["key"]=key
    uri=f"{API_ROOT}/{endpoint}?"+urllib.parse.urlencode(p)
    # The URL contains the API key; NEVER log or store request URL.
    req=urllib.request.Request(uri,headers={"User-Agent":"BrandCovenantResearch/0.1"})
    with urllib.request.urlopen(req,timeout=40) as response:
        return json.loads(response.read().decode("utf-8"))

def exclusive_next_day(day):
    return (dt.date.fromisoformat(day)+dt.timedelta(days=1)).isoformat()+"T00:00:00Z"

def write_csv(path, rows, columns):
    with open(path,"w",newline="",encoding="utf-8") as file:
        writer=csv.DictWriter(file,fieldnames=columns,extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output-dir",default="youtube_api_run")
    ap.add_argument("--max-pages",type=int,default=1,help="Search result pages per query (max 50 per page)")
    ap.add_argument("--sleep",type=float,default=0.25)
    ap.add_argument("--key-env",default="YOUTUBE_API_KEY")
    args=ap.parse_args()
    key=os.environ.get(args.key_env,"").strip()
    if not key:
        sys.exit("Missing YouTube API key. Set YOUTUBE_API_KEY in your environment; do not commit it to GitHub.")
    if args.max_pages<1 or args.max_pages>10:
        sys.exit("--max-pages must be 1–10.")
    out=pathlib.Path(args.output_dir);out.mkdir(parents=True,exist_ok=True)
    run_ts=dt.datetime.now(dt.timezone.utc).isoformat()
    lead_rows=[];search_log=[];raw_search=[]
    for group,start,end,terms in STRATA:
        for q in terms:
            page_token=None
            for page in range(1,args.max_pages+1):
                p={"part":"snippet","type":"video","q":q,"maxResults":50,
                   "publishedAfter":f"{start}T00:00:00Z",
                   "publishedBefore":exclusive_next_day(end),
                   "order":"date","regionCode":"US"}
                if page_token:p["pageToken"]=page_token
                log={"run_utc":run_ts,"stratum":group,"start":start,"end":end,
                     "query":q,"page":page,"sort":"date","status":"ok","count":0,"error":""}
                try:
                    result=api_get("search",p,key)
                    log["count"]=len(result.get("items",[]))
                    raw_search.append({"query":q,"stratum":group,"page":page,"data":result})
                    for rank,item in enumerate(result.get("items",[]),1):
                        vid=item.get("id",{}).get("videoId")
                        if not vid:continue
                        sn=item.get("snippet",{})
                        lead_rows.append({
                          "video_id":vid,"video_url":"https://www.youtube.com/watch?v="+vid,
                          "search_stratum":group,"search_query":q,"search_page":page,
                          "search_rank":rank,"published_at_search":sn.get("publishedAt",""),
                          "title_search":sn.get("title",""),"channel_search":sn.get("channelTitle",""),
                          "collection_utc":run_ts})
                    page_token=result.get("nextPageToken")
                except (urllib.error.URLError,urllib.error.HTTPError,ValueError) as e:
                    log["status"]="error"
                    log["error"]=str(e)[:300]
                    search_log.append(log)
                    print(f"ERROR [{group}] {q}: {e}",file=sys.stderr)
                    break
                search_log.append(log)
                if not page_token:break
                time.sleep(args.sleep)
    # Deduplicate by actual YouTube ID, but preserve *all* query appearance rows.
    ids=sorted({row["video_id"] for row in lead_rows})
    detailed={}
    for start_idx in range(0,len(ids),50):
        chunk=ids[start_idx:start_idx+50]
        try:
            result=api_get("videos",{"part":"snippet,contentDetails,statistics,status",
                                     "id":",".join(chunk)},key)
            for v in result.get("items",[]):
                sn=v.get("snippet",{});st=v.get("statistics",{});dur=v.get("contentDetails",{})
                detailed[v["id"]]={
                    "video_id":v["id"],"video_url":"https://www.youtube.com/watch?v="+v["id"],
                    "published_at":sn.get("publishedAt",""),
                    "title":sn.get("title",""),"description":sn.get("description",""),
                    "channel_id":sn.get("channelId",""),"channel":sn.get("channelTitle",""),
                    "duration_iso8601":dur.get("duration",""),"caption_flag":dur.get("caption",""),
                    "view_count_at_collection":st.get("viewCount",""),
                    "like_count_at_collection":st.get("likeCount",""),
                    "comment_count_at_collection":st.get("commentCount",""),
                    "collection_utc":run_ts,
                    "content_watched":"No","topic_screen":"Not screened",
                    "code_complete":"No"}
        except Exception as e:
            print("Metadata API error:",str(e)[:300],file=sys.stderr)
        time.sleep(args.sleep)
    lead_cols=["video_id","video_url","search_stratum","search_query","search_page",
               "search_rank","published_at_search","title_search","channel_search","collection_utc"]
    video_cols=["video_id","video_url","published_at","title","description","channel_id","channel",
                "duration_iso8601","caption_flag","view_count_at_collection","like_count_at_collection",
                "comment_count_at_collection","collection_utc","content_watched","topic_screen","code_complete"]
    log_cols=["run_utc","stratum","start","end","query","page","sort","status","count","error"]
    write_csv(out/"search_occurrences.csv",lead_rows,lead_cols)
    write_csv(out/"unique_video_metadata.csv",list(detailed.values()),video_cols)
    write_csv(out/"search_log.csv",search_log,log_cols)
    # Raw results may contain names, descriptions and personal data. Keep out of public repo pending review.
    with open(out/"raw_search_private.json","w",encoding="utf-8") as f:
        json.dump(raw_search,f,ensure_ascii=False)
    with open(out/"RUN_STATUS.txt","w",encoding="utf-8") as f:
        f.write(f"Run: {run_ts}\nSearch tasks: {len(search_log)}\n"
                f"Video IDs found: {len(ids)}\nOfficial detailed records: {len(detailed)}\n"
                "Zero videos reviewed or formally coded by this program.\n"
                "Do not treat search hits as a representative sample.\n")
    print(f"Done: {len(ids)} distinct IDs; {len(detailed)} metadata records. See {out.resolve()}")

if __name__=="__main__":
    main()