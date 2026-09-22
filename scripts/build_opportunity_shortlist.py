#!/usr/bin/env python3
"""Build a ranked money-opportunity shortlist from structured evidence."""
from pathlib import Path
from datetime import datetime, timezone
import json, re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"opportunities"/"queue.yml"
OUT=ROOT/"data"/"opportunities"/"latest.json"
REPORT=ROOT/"reports"/"opportunities"
REPORT.mkdir(parents=True,exist_ok=True)

# Deliberately lightweight YAML parsing for this fixed schema; no third-party packages.
items=[]; current=None
for raw in SOURCE.read_text(encoding="utf-8").splitlines():
    line=raw.strip()
    if line.startswith("- id:"):
        if current: items.append(current)
        current={"id":line.split(":",1)[1].strip().strip('"')}
    elif current and ":" in line:
        k,v=line.split(":",1); v=v.strip().strip('"')
        current[k.strip()]=v
if current: items.append(current)

def num(x,default=0):
    try:return float(x)
    except:return default

ranked=[]
for x in items:
    if x.get("status") in {"done","rejected"}: continue
    impact=num(x.get("impact")); effort=max(num(x.get("effort"),1),1)
    evidence=0
    ev=x.get("evidence","").lower()
    for word,pts in [("search",3),("demand",3),("revenue",3),("current",2),("manual",0)]:
        if word in ev: evidence+=pts
    score=round((impact*4)+(evidence*2)+(10/effort),1)
    ranked.append({**x,"score":score,"evidence_strength":evidence})
ranked.sort(key=lambda x:-x["score"])

payload={"generated_at":datetime.now(timezone.utc).isoformat(),"count":len(ranked),"opportunities":ranked}
OUT.write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
lines=[f"# Laxman OS — Opportunity Shortlist ({date})","",
"| Score | Category | Opportunity | Evidence | Next action |","|---:|---|---|---|---|"]
for x in ranked:
    lines.append(f"| {x['score']} | {x.get('category','')} | {x.get('title','')} | {x.get('evidence','')} | {x.get('next_action','')} |")
lines += ["","## Human validation gate","Scores are queueing aids only. Before building or spending money, validate demand, competition, monetization, and feasibility."]
content="\n".join(lines)+"\n"
(REPORT/f"{date}.md").write_text(content,encoding="utf-8")
(REPORT/"latest.md").write_text(content,encoding="utf-8")
print(content)
