#!/usr/bin/env python3
"""Collect current public-interest signals for monetizable problem ideas."""
from pathlib import Path
from datetime import datetime, timezone
import json, urllib.parse, urllib.request
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"opportunities"/"research_bank.yml"
OUT=ROOT/"data"/"opportunities"/"live_research.json"
REPORT=ROOT/"reports"/"opportunities"
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

# Parse the fixed query-list syntax: ["a", "b", "c"].
for x in items:
    qraw=x.get("queries","")
    queries=[q.strip().strip('"') for q in qraw.strip("[]").split(",") if q.strip()]
    signals=[]
    for q in queries:
        url="https://news.google.com/rss/search?"+urllib.parse.urlencode({"q":q,"hl":"en-US","gl":"US","ceid":"US:en"})
        try:
            req=urllib.request.Request(url,headers={"User-Agent":"LaxmanOS/1.0"})
            root=ET.fromstring(urllib.request.urlopen(req,timeout=15).read())
            titles=[n.text or "" for n in root.findall(".//item/title")][:10]
            signals.append({"query":q,"ok":True,"result_count":len(titles),"titles":titles[:5]})
        except Exception as e:
            signals.append({"query":q,"ok":False,"result_count":0,"error":str(e)})
    x["freshness_signal"]=sum(min(s["result_count"],10) for s in signals)
    x["signals"]=signals
    x["validation"]="Validate actual search demand, competition, audience fit, acquisition path, and monetization before building."

payload={"generated_at":datetime.now(timezone.utc).isoformat(),"count":len(items),"opportunities":items}
OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
ranked=sorted(items,key=lambda x:(-x["freshness_signal"],x["id"]))
lines=[f"# Laxman OS — Money Live Research ({date})","",
"| Signal | Problem | Asset | Monetization |",
"|---:|---|---|---|"]
for x in ranked:
    lines.append(f"| {x['freshness_signal']} | {x.get('problem','')} | {x.get('asset','')} | {x.get('monetization','')} |")
lines += ["","## Interpretation","The signal is based on current public news-search activity and is only a research-prioritization aid. It does not prove demand, profitability, or revenue potential.","",
"## Validation gate","Before spending money or building, validate the problem with current search results, competitors, target users, distribution, and a realistic monetization path."]
content="\n".join(lines)+"\n"
(REPORT/f"{date}-money-live.md").write_text(content,encoding="utf-8")
(REPORT/"money-live-latest.md").write_text(content,encoding="utf-8")
print(content)
