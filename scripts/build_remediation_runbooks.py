#!/usr/bin/env python3
"""Generate deterministic human-review runbooks from remediation items."""
import json
from pathlib import Path
from datetime import datetime, timezone
SRC=Path("data/workflows/remediation.json")
OUT=Path("data/workflows/runbooks.json")
REPORT=Path("reports/workflows/runbooks-latest.md")
def main():
    now=datetime.now(timezone.utc).isoformat()
    if not SRC.exists():
        data={"version":1,"generated_at":now,"status":"waiting","runbooks":[],"human_validation_required":True}
    else:
        src=json.loads(SRC.read_text(encoding="utf-8")); rows=[]
        for x in src.get("items",[]):
            rows.append({
                "id":"runbook-"+str(x.get("id","unknown")),
                "remediation_id":x.get("id"),
                "workflow":x.get("workflow"),
                "stage":x.get("stage"),
                "priority":x.get("priority"),
                "status":"ready-for-review",
                "steps":[
                    "Open the linked workflow run.",
                    "Inspect the failed job and relevant step logs.",
                    "Confirm whether the failure is reproducible or transient.",
                    "Identify the smallest evidence-backed corrective change.",
                    "Review the proposed change before editing code.",
                    "Run the relevant validation workflow after the change."
                ],
                "evidence_url":x.get("evidence_url"),
                "root_cause_status":"unverified",
                "human_validation_required":True
            })
        data={"version":1,"generated_at":now,"status":"warning" if rows else "healthy","runbooks":rows,"runbook_count":len(rows),"human_validation_required":True}
    OUT.parent.mkdir(parents=True,exist_ok=True); REPORT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    lines=["# Remediation Runbooks","","Deterministic review checklists generated from remediation evidence.","",f"Generated: {data['generated_at']}",""]
    if not data["runbooks"]: lines.append("No runbooks currently require review.")
    for i,r in enumerate(data["runbooks"],1):
        lines += [f"## {i}. {r['workflow']}",f"- Stage: {r['stage']}",f"- Priority: {r['priority']}",f"- Evidence: {r.get('evidence_url') or 'unavailable'}","- Root cause: **unverified**","- Checklist:"]
        lines += [f"  {n}. {s}" for n,s in enumerate(r["steps"],1)]
        lines.append("")
    lines += ["## Safety","Runbooks provide review guidance only. They do not edit code, retry runs, merge PRs, publish, spend, trade, or message externally."]
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
if __name__=="__main__": main()
