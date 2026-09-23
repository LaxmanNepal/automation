#!/usr/bin/env python3
"""Build evidence-based verification records for remediation items."""
import json
from datetime import datetime, timezone
from pathlib import Path

WORKFLOWS = Path("data/workflows/latest.json")
FAILURES = Path("data/workflows/failures.json")
REMEDIATION = Path("data/workflows/remediation.json")
OUT = Path("data/workflows/change-verification.json")
REPORT = Path("reports/workflows/change-verification-latest.md")

def load(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return None

def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

def workflow_rows(data):
    return {r.get("workflow"): r for r in (data or {}).get("workflows", []) if r.get("workflow")}

def find_failure(item, failures):
    rid = item.get("remediation_id") or ""
    fp = rid[4:] if rid.startswith("rem-") else ""
    return next((f for f in failures if f.get("fingerprint") == fp), None)

def verify(failure, row):
    latest = row.get("latest_run") if row else None
    recent = row.get("recent_runs", []) if row else []
    if not row or not latest:
        return {"verification_state":"waiting","verification_basis":"Workflow telemetry or latest run is unavailable.","verification_run_id":None,"verification_conclusion":None,"verification_run_url":None}

    previous_ids = set(failure.get("run_ids", []) if failure else [])
    failure_times = [parse_dt(r.get("updated_at") or r.get("created_at")) for r in recent if r.get("id") in previous_ids]
    failure_times = [x for x in failure_times if x]
    failure_time = max(failure_times) if failure_times else None

    later = []
    for run in recent:
        if run.get("id") in previous_ids:
            continue
        run_time = parse_dt(run.get("updated_at") or run.get("created_at"))
        if failure_time and run_time and run_time <= failure_time:
            continue
        later.append(run)
    later.sort(key=lambda r: parse_dt(r.get("updated_at") or r.get("created_at")) or datetime.min.replace(tzinfo=timezone.utc), reverse=True)

    if not later:
        return {"verification_state":"waiting","verification_basis":"No later workflow run is recorded in the available recent telemetry.","verification_run_id":None,"verification_conclusion":None,"verification_run_url":None}

    candidate = later[0]
    conclusion = candidate.get("conclusion")
    if conclusion == "success":
        state = "verified-by-later-success"
        basis = "A later successful run of the same workflow is recorded after the failure evidence."
    else:
        state = "still-failing"
        basis = "A later run of the same workflow is recorded, but its conclusion is not successful."
    return {"verification_state":state,"verification_basis":basis,"verification_run_id":candidate.get("id"),"verification_conclusion":conclusion,"verification_run_url":candidate.get("html_url")}

def main():
    generated = datetime.now(timezone.utc).isoformat()
    telemetry, failures_data, remediation_data = load(WORKFLOWS), load(FAILURES), load(REMEDIATION)
    if telemetry is None:
        data = {"version":1,"generated_at":generated,"status":"waiting","items":[],"coverage":"Workflow telemetry is unavailable; change verification cannot be established.","human_validation_required":True}
    else:
        rows = workflow_rows(telemetry)
        items = []
        for item in (remediation_data or {}).get("items", []):
            failure = find_failure(item, (failures_data or {}).get("failures", []))
            result = verify(failure, rows.get(item.get("workflow")))
            previous_ids = failure.get("run_ids", []) if failure else []
            items.append({
                "id":"verify-" + str(item.get("id","unknown")),
                "remediation_id":item.get("id"),
                "workflow":item.get("workflow"),
                "stage":item.get("stage"),
                "priority":item.get("priority"),
                "previous_failure_run_ids":previous_ids,
                "previous_failure_run_id":previous_ids[-1] if previous_ids else None,
                **result,
                "causal_claim":"unverified",
                "human_validation_required":True
            })
        states = {x["verification_state"] for x in items}
        status = "warning" if "still-failing" in states else ("healthy" if items and states <= {"verified-by-later-success"} else "waiting")
        data = {"version":1,"generated_at":generated,"status":status,"items":items,"coverage":"Compares remediation-linked failure runs with later runs of the same workflow in available recent telemetry.","human_validation_required":True}

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Change Verification","","This ledger checks whether a remediation-linked workflow has a later execution outcome in the available telemetry.","","## Interpretation","- verified-by-later-success: a later successful run of the same workflow is recorded.","- still-failing: a later run exists but is not successful.","- waiting: there is not enough later telemetry to verify the outcome.","","A later success is execution evidence only. The ledger does not claim that a particular code change caused the result; causality remains unverified.","","## Safety","No automatic retry, code modification, merge, publish, spend, trade, or external message is performed. Human review is required.",""]
    for item in data.get("items", []):
        lines += [f"### {item.get('workflow','Workflow')}",f"- Remediation: {item.get('remediation_id')}",f"- Verification state: **{item.get('verification_state')}**",f"- Previous failure run: {item.get('previous_failure_run_id')}",f"- Verification run: {item.get('verification_run_id')}",f"- Conclusion: {item.get('verification_conclusion')}",f"- Basis: {item.get('verification_basis')}",f"- Causality: {item.get('causal_claim')}",""]
    REPORT.write_text("\n".join(lines), encoding="utf-8")

if __name__ == "__main__":
    main()
