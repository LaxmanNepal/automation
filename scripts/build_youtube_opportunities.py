#!/usr/bin/env python3
"""Build a deterministic YouTube topic shortlist from a maintained topic bank."""
from pathlib import Path
from datetime import datetime, timezone
import json

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"youtube"/"topic_bank.yml"
OUT=ROOT/"data"/"youtube"/"latest.json"
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

def score(x):
    intent=x.get("intent","").lower()
    freshness=x.get("freshness","").lower()
    s=0
    s += {"how-to":5,"problem-solving":5,"comparison":4}.get(intent,2)
    s += 2 if "ai" in x.get("topic","").lower() or "ai" in x.get("themes","").lower() else 0
    s += 1 if freshness=="verify-current" else 0
    return s

for x in items:
    x["score"]=score(x)
    x["research_status"]="Needs current search/competition validation"
items.sort(key=lambda x:(x.get("channel",""),-x["score"],x["id"]))

payload={"generated_at":datetime.now(timezone.utc).isoformat(),"count":len(items),"topics":items}
OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
lines=[f"# Laxman OS — YouTube Opportunities ({date})","",
"| Score | Channel | Topic | Intent | Format | Freshness |",
"|---:|---|---|---|---|---|"]
for x in items:
    lines.append(f"| {x['score']} | {x.get('channel','')} | {x.get('topic','')} | {x.get('intent','')} | {x.get('format','')} | {x.get('freshness','')} |")
lines += ["","## Validation gate","This engine organizes candidates; it does not claim live search volume, competition, trends, or revenue. Validate those before recording.","","## Production rule","Prefer topics with clear viewer intent, a concrete problem, and a useful outcome. Keep the final publish decision human-reviewed."]
content="\n".join(lines)+"\n"
(REPORT/f"{date}.md").write_text(content,encoding="utf-8")
(REPORT/"latest.md").write_text(content,encoding="utf-8")
print(content)
