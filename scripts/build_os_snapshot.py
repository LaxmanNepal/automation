#!/usr/bin/env python3
"""Build a deterministic cross-module Laxman OS snapshot."""
import json, pathlib
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parents[1]
def load(rel):
    try: return json.loads((ROOT/rel).read_text(encoding="utf-8"))
    except Exception: return {}
def count(o, keys):
    for k in keys:
        if isinstance(o.get(k), list): return len(o[k])
    return 0
assets=load("data/assets/latest.json")
yt=load("data/youtube/latest.json")
problems=load("data/problems/latest.json")
github=load("data/github/health.json")
seo=load("data/seo/latest.json")
website=load("data/website/latest.json")
analytics=load("data/analytics/latest.json")
business=load("data/business/latest.json")
modules={
 "money":{"status":"healthy" if assets else "waiting","count":count(assets,["assets","opportunities"])},
 "youtube":{"status":"healthy" if yt else "waiting","count":count(yt,["opportunities","topics"])},
 "github":{"status":"healthy" if github else "waiting","count":count(github,["repositories"])},
 "problems":{"status":"warning" if count(problems,["findings","problems"]) else "healthy","count":count(problems,["findings","problems"])},
 "seo":{"status":seo.get("status","waiting"),"count":count(seo,["findings"])},
 "website":{"status":website.get("status","waiting"),"count":count(website,["findings","sites"])},
 "analytics":{"status":analytics.get("status","waiting"),"count":len(analytics.get("metrics",{}))},
 "business":{"status":business.get("status","waiting"),"count":len(business.get("goals",[]))+len(business.get("projects",[]))}
}
actions=[]
for m in ("problems","money","youtube","seo","website"):
    if modules[m]["count"] or m in ("seo","website"):
        actions.append({"priority":"high" if m in ("problems","money","youtube") else "medium","category":m,"action":"Review "+m+" findings and select a human-approved next step","evidence":modules[m]["count"]})
now=datetime.now(timezone.utc).isoformat()
payload={"version":1,"generated_at":now,"modules":modules,"actions":actions,"human_validation_required":True}
out=ROOT/"data/os"; out.mkdir(parents=True,exist_ok=True)
(out/"latest.json").write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
rep=ROOT/"reports/os"; rep.mkdir(parents=True,exist_ok=True)
(rep/"latest.md").write_text("# Laxman OS Snapshot\n\nGenerated: "+now+"\n\n## Modules\n"+"\n".join(f"- **{k}**: {v['status']} ({v['count']})" for k,v in modules.items())+"\n\n## Command\n"+"\n".join(f"{i}. **{a['priority'].upper()}** {a['action']} — evidence: {a['evidence']}" for i,a in enumerate(actions,1))+"\n")
print("Built",out/"latest.json")
