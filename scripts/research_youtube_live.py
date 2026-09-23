#!/usr/bin/env python3
"""Collect free, reproducible freshness signals for the YouTube topic bank.

Uses public Google News RSS queries by default. If YOUTUBE_API_KEY is configured,
YouTube Data API search results are also collected. No credentials are required
for the default mode.
"""
from pathlib import Path
from datetime import datetime, timezone
import json, os, re, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"youtube"/"topic_bank.yml"
OUT=ROOT/"data"/"youtube"/"live_research.json"
REPORT=ROOT/"reports"/"youtube"
REPORT.mkdir(parents=True,exist_ok=True)

items=[]; current=None
for raw in SOURCE.read_text(encoding="utf-8").splitlines():
    line=raw.strip()
    if line.startswith("- id:"):
        if current: items.append(current)
        current={"id":line.split(":",1)[1].strip().strip('"')}
    elif current and ":" in line:
        k,v=line.split(":",1); current[k.strip()]=v.strip().strip('"')
if current: items.append(current)

def rss_signal(topic):
    q=urllib.parse.quote(topic)
    url=f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"
    req=urllib.request.Request(url,headers={"User-Agent":"LaxmanOS/1.0"})
    try:
        data=urllib.request.urlopen(req,timeout=15).read()
        root=ET.fromstring(data)
        titles=[x.text or "" for x in root.findall(".//item/title")][:10]
        return {"ok":True,"result_count":len(titles),"recent_titles":titles[:5]}
    except Exception as e:
        return {"ok":False,"result_count":0,"error":str(e)}

def youtube_api_signal(topic):
    key=os.environ.get("YOUTUBE_API_KEY")
    if not key: return {"enabled":False}
    params=urllib.parse.urlencode({"part":"snippet","q":topic,"type":"video","maxResults":10,"order":"date","key":key})
    url="https://www.googleapis.com/youtube/v3/search?"+params
    try:
        data=json.loads(urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"LaxmanOS/1.0"}),timeout=15).read())
        return {"enabled":True,"ok":True,"result_count":len(data.get("items",[])),
                "titles":[x.get("snippet",{}).get("title","") for x in data.get("items",[])[:5]]}
    except Exception as e:
        return {"enabled":True,"ok":False,"error":str(e)}

results=[]
for x in items:
    news=rss_signal(x.get("topic",""))
    yt=youtube_api_signal(x.get("topic",""))
    # Signal score is deliberately not a prediction of views or revenue.
    signal=min(news.get("result_count",0),10)
    if yt.get("ok"): signal+=min(yt.get("result_count",0),10)
    x={**x,"freshness_signal":signal,"google_news":news,"youtube_search":yt,
       "validation":"Search demand, competition, audience fit, and monetization still require review."}
    results.append(x)

payload={"generated_at":datetime.now(timezone.utc).isoformat(),
         "source":"Google News RSS; optional YouTube Data API",
         "count":len(results),"topics":results}
OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
lines=[f"# Laxman OS — Live YouTube Research ({date})","",
"| Channel | Topic | Freshness signal | News results | API mode |",
"|---|---|---:|---:|---|"]
for x in results:
    y=x.get("youtube_search",{})
    lines.append(f"| {x.get('channel','')} | {x.get('topic','')} | {x.get('freshness_signal',0)} | {x.get('google_news',{}).get('result_count',0)} | {'enabled' if y.get('enabled') else 'free RSS'} |")
lines += ["","## Interpretation","The signal measures current searchable/news activity, not expected views, rankings, or revenue. Higher signal means 'research this topic first,' not 'this topic will perform better.'","",
"## Validation gate","Before publishing, manually verify current YouTube results, competition, search intent, audience fit, accuracy, and monetization."] 
content="\n".join(lines)+"\n"
(REPORT/f"{date}-live.md").write_text(content,encoding="utf-8")
(REPORT/"live-latest.md").write_text(content,encoding="utf-8")
print(content)
