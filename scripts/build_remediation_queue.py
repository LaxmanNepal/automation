#!/usr/bin/env python3
"""Turn failure signals into human-review remediation items."""
import json
from pathlib import Path
from datetime import datetime, timezone
FAILURES=Path("data/workflows/failures.json")
OUT=Path("data/workflows/remediation.json")
REPORT=Path("reports/workflows/remediation-latest.md")
def main():
    now=datetime.now(timezone.utc).isoformat()
    if not FAILURES.exists():
        data={"version":1,"generated_at":now,"status":"waiting","items":[],"coverage":"Failure intelligence has not produced telemetry yet.","human_validation_required":True}
    else:
        src=json.loads(FAILURES.read_text(encoding="utf-8")); items=[]
        for f in src.get("failures",[]):
            items.append({"id":"rem-"+str(f.get("fingerprint","unknown")).replace("/","-"),"workflow":f.get("name"),"stage":f.get("failed_stage") or "unavailable","conclusion":f.get("conclusion"),"occurrences":f.get("occurrences",0),"priority":"high" if f.get("occurrences",0)>=2 else "normal","status":"needs-review","evidence_url":f.get("latest_run_url"),"next_action":"Review run/job logs, confirm root cause, then create a targeted fix.","root_cause_status":"unverified","human_validation_required":True})
        data={"version":1,"generated_at":now,"status":"warning" if items else "healthy","items":items,"item_count":len(items),"coverage":"Derived only from failure-intelligence evidence.","human_validation_required":True}
    OUT.parent.mkdir(parents=True,exist_ok=True); REPORT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    lines=["# Remediation Queue","","Human-review queue derived from failure evidence.","","Generated: "+data["generated_at"],"Status: **"+data["status"]+"**",""]
    if not data["items"]: lines.append("No remediation items are currently generated.")
    for i,x in enumerate(data["items"],1):
        lines += [f"## {i}. {x['workflow']}",f"- Priority: **{x['priority']}**",f"- Stage: {x['stage']}",f"- Status: {x['status']}",f"- Evidence: {x.get('evidence_url') or 'unavailable'}","- Root cause: **unverified**",f"- Next action: {x['next_action']}",""]
    lines += ["## Safety","- This queue does not modify code or run retries.","- Human review is required before any remediation."]
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
if __name__=="__main__": main()