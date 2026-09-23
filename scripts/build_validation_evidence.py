#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone
SRC=Path("data/workflows/latest.json"); OUT=Path("data/workflows/validation.json"); REPORT=Path("reports/workflows/validation-latest.md")
def main():
    now=datetime.now(timezone.utc).isoformat()
    if not SRC.exists(): data={"version":1,"generated_at":now,"status":"waiting","records":[],"coverage":"Workflow telemetry unavailable.","human_validation_required":True}
    else:
        src=json.loads(SRC.read_text(encoding="utf-8")); rows=[]
        for w in src.get("workflows",[]):
            latest=w.get("latest_run") or {}; conclusion=latest.get("conclusion")
            rows.append({"workflow":w.get("name"),"workflow_file":w.get("workflow"),"latest_run_id":latest.get("id"),"latest_conclusion":conclusion,"latest_status":latest.get("status"),"latest_run_url":latest.get("html_url"),"validation_state":"validated" if conclusion=="success" else ("needs-validation" if conclusion else "waiting"),"validation_basis":"latest recorded workflow conclusion","human_validation_required":True})
        data={"version":1,"generated_at":now,"status":"healthy","records":rows,"record_count":len(rows),"coverage":"Validation state reflects recorded workflow telemetry only.","human_validation_required":True}
    OUT.parent.mkdir(parents=True,exist_ok=True); REPORT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    lines=["# Validation Evidence","","Generated: "+data["generated_at"],"","Validation is evidence-based and does not execute or modify workflows.",""]
    if not data["records"]: lines.append("No workflow telemetry available.")
    for r in data["records"]: lines += ["## "+str(r["workflow"]),"- State: **"+str(r["validation_state"])+"**","- Latest conclusion: `"+str(r["latest_conclusion"] or "unavailable")+"`","- Run: "+str(r["latest_run_url"] or "unavailable"),"- Basis: "+r["validation_basis"],""]
    lines += ["## Safety","A successful workflow run is evidence that the recorded workflow completed successfully; it is not proof that a broader product or business problem is solved. Human review remains required."]
    REPORT.write_text("\n".join(lines)+"\n",encoding="utf-8")
if __name__=="__main__": main()