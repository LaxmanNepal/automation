#!/usr/bin/env python3
"""Collect recent GitHub Actions workflow status for the Laxman OS dashboard."""
import json, os
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

REPO=os.environ.get("GITHUB_REPOSITORY","LaxmanNepal/automation")
TOKEN=os.environ.get("GITHUB_TOKEN")
OUT=Path("data/workflows/latest.json")
WORKFLOWS=[
 ("Money research","money-live-research.yml"),
 ("Revenue assets","revenue-asset-engine.yml"),
 ("Build issue specs","build-issue-generator.yml"),
 ("YouTube opportunities","youtube-opportunity.yml"),
 ("YouTube live research","youtube-live-research.yml"),
 ("GitHub health","github-health.yml"),
 ("Problem detector","problem-detector.yml"),
 ("Action queue","action-queue.yml"),
 ("Unified intelligence","os-intelligence.yml"),
]
def api(url):
    headers={"Accept":"application/vnd.github+json","User-Agent":"laxman-os"}
    if TOKEN: headers["Authorization"]=f"Bearer {TOKEN}"
    req=Request(url,headers=headers)
    with urlopen(req,timeout=20) as r: return json.load(r)
def main():
    generated=datetime.now(timezone.utc).isoformat()
    if not TOKEN:
        data={"version":1,"generated_at":generated,"status":"waiting","workflows":[],"coverage":"GITHUB_TOKEN is required for workflow history.","human_validation_required":True}
    else:
        rows=[]
        for name,file in WORKFLOWS:
            try:
                payload=api(f"https://api.github.com/repos/{REPO}/actions/workflows/{file}/runs?per_page=5")
                runs=payload.get("workflow_runs",[])
                latest=runs[0] if runs else None
                rows.append({"name":name,"workflow":file,"status":"healthy" if latest and latest.get("conclusion")=="success" else ("warning" if latest and latest.get("conclusion") else "waiting"),"latest_run":({"id":latest.get("id"),"status":latest.get("status"),"conclusion":latest.get("conclusion"),"created_at":latest.get("created_at"),"updated_at":latest.get("updated_at"),"html_url":latest.get("html_url")} if latest else None),"recent_runs":[{"id":r.get("id"),"status":r.get("status"),"conclusion":r.get("conclusion"),"updated_at":r.get("updated_at"),"html_url":r.get("html_url")} for r in runs]})
            except Exception as e:
                rows.append({"name":name,"workflow":file,"status":"unavailable","error":type(e).__name__})
        data={"version":1,"generated_at":generated,"status":"healthy" if rows else "waiting","workflows":rows,"coverage":"Recent GitHub Actions runs for configured Laxman OS workflows.","human_validation_required":True}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
if __name__=="__main__": main()
