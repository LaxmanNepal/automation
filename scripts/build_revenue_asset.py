#!/usr/bin/env python3
"""Turn researched money opportunities into implementation-ready asset specs."""
from pathlib import Path
from datetime import datetime, timezone
import json, re

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"data"/"opportunities"/"live_research.json"
OUT=ROOT/"data"/"assets"/"latest.json"
REPORT=ROOT/"reports"/"assets"
REPORT.mkdir(parents=True,exist_ok=True)
OUT.parent.mkdir(parents=True,exist_ok=True)

data=json.loads(SOURCE.read_text(encoding="utf-8")) if SOURCE.exists() else {"opportunities":[]}
items=data.get("opportunities",[])

def slug(s):
    return re.sub(r"[^a-z0-9]+","-",s.lower()).strip("-")[:60]

assets=[]
for x in items:
    title=x.get("asset","").strip() or x.get("problem","").strip()
    if not title: continue
    audience=x.get("audience","General audience")
    assets.append({
        "id":f"asset-{x.get('id','unknown')}",
        "source_opportunity":x.get("id"),
        "asset":title,
        "problem":x.get("problem",""),
        "audience":audience,
        "monetization":x.get("monetization",""),
        "research_signal":x.get("freshness_signal",0),
        "build_effort":"small MVP",
        "suggested_stack":"Existing LaxmanNepal web stack; no paid API required for MVP",
        "mvp": [
            "Landing page explaining the problem and outcome",
            "One core useful feature or resource",
            "Mobile-first responsive UI",
            "SEO metadata and indexable explanatory content",
            "Clear but non-intrusive monetization placement",
            "Analytics event hooks for usage and conversion"
        ],
        "seo": [
            "Create one primary search-intent page",
            "Add supporting FAQ/how-to content",
            "Link from relevant Laxman Nepal properties",
            "Validate current keywords before publishing"
        ],
        "definition_of_done": [
            "Core user task works end-to-end",
            "Mobile and desktop checks pass",
            "Basic accessibility checks pass",
            "SEO title/description/canonical configured",
            "Monetization path is documented",
            "Human review completed"
        ],
        "slug":slug(title),
        "status":"spec-ready",
        "human_validation_required":True
    })

payload={"generated_at":datetime.now(timezone.utc).isoformat(),"count":len(assets),"assets":assets}
OUT.write_text(json.dumps(payload,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
date=datetime.now(timezone.utc).strftime("%Y-%m-%d")
lines=[f"# Laxman OS — Revenue Asset Specs ({date})","",
"| Asset | Source | Audience | Monetization | Signal |",
"|---|---|---|---|---:|"]
for a in sorted(assets,key=lambda z:-z["research_signal"]):
    lines.append(f"| {a['asset']} | {a['source_opportunity']} | {a['audience']} | {a['monetization']} | {a['research_signal']} |")
lines += ["","## Execution gate","These are implementation specifications, not proof of demand or revenue. Validate the opportunity before spending money or launching.","",
"## Next step","Select one validated asset and create an implementation issue/PR manually or through a later human-approved automation layer."]
content="\n".join(lines)+"\n"
(REPORT/f"{date}.md").write_text(content,encoding="utf-8")
(REPORT/"latest.md").write_text(content,encoding="utf-8")
print(content)
