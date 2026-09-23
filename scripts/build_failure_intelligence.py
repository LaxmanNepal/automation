#!/usr/bin/env python3
"""Build deterministic failure intelligence from recent GitHub Actions telemetry."""
import json, os, re
from pathlib import Path
from urllib.request import Request, urlopen
from datetime import datetime, timezone

REPO = os.environ.get("GITHUB_REPOSITORY", "LaxmanNepal/automation")
TOKEN = os.environ.get("GITHUB_TOKEN")
INPUT = Path("data/workflows/latest.json")
OUT = Path("data/workflows/failures.json")
REPORT = Path("reports/workflows/failures-latest.md")

def api(url):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "laxman-os"}
    if TOKEN: headers["Authorization"] = f"Bearer {TOKEN}"
    req = Request(url, headers=headers)
    with urlopen(req, timeout=20) as r: return json.load(r)

def normalize_stage(value):
    return re.sub(r"\\s+", " ", str(value or "unknown-stage").strip().lower())

def main():
    generated = datetime.now(timezone.utc).isoformat()
    if not INPUT.exists():
        data = {"version":1,"generated_at":generated,"status":"waiting","failures":[],"coverage":"Workflow telemetry has not been generated yet.","human_validation_required":True}
    else:
        snapshot = json.loads(INPUT.read_text(encoding="utf-8"))
        groups = {}
        for w in snapshot.get("workflows", []):
            run = w.get("latest_run") or {}
            conclusion = run.get("conclusion")
            if conclusion not in ("failure","timed_out","cancelled","action_required"): continue
            stage = normalize_stage(run.get("failed_stage"))
            fingerprint = f"{w.get('workflow','unknown')}::{stage}::{conclusion}"
            g = groups.setdefault(fingerprint, {"fingerprint":fingerprint,"workflow":w.get("workflow"),"name":w.get("name"),"failed_stage":run.get("failed_stage"),"conclusion":conclusion,"occurrences":0,"run_ids":[],"latest_run_url":run.get("html_url"),"evidence":[]})
            g["occurrences"] += 1
            if run.get("id"): g["run_ids"].append(run["id"])
            g["evidence"].append({"run_id":run.get("id"),"updated_at":run.get("updated_at"),"url":run.get("html_url"),"stage":run.get("failed_stage"),"conclusion":conclusion})
        failures = sorted(groups.values(), key=lambda x:(-x["occurrences"], x["name"] or ""))
        for f in failures:
            f["suggested_action"] = "Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix."
            f["root_cause_status"] = "unverified"
        data = {"version":1,"generated_at":generated,"status":"warning" if failures else "healthy","failures":failures,"failure_count":len(failures),"coverage":"Latest failed/timed-out/cancelled/action-required workflow runs from the workflow monitor.","human_validation_required":True}
    OUT.parent.mkdir(parents=True, exist_ok=True); REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    lines = ["# Failure Intelligence","","Generated: " + str(data.get("generated_at")),"","Status: **" + str(data.get("status","waiting")) + "**","","Repeated failures are grouped by workflow, failed stage, and conclusion. Root causes are not asserted without log evidence.",""]
    if not data.get("failures"): lines.append("No verified failure groups are currently recorded.")
    for i,f in enumerate(data.get("failures",[]),1):
        lines += [f"## {i}. {f.get('name','Workflow')}",f"- Conclusion: `{f.get('conclusion')}`",f"- Failed stage: `{f.get('failed_stage') or 'unavailable'}`",f"- Occurrences in latest telemetry: **{f.get('occurrences',0)}**",f"- Evidence: {f.get('latest_run_url') or 'unavailable'}",f"- Root cause: **unverified**",f"- Next action: {f.get('suggested_action')}",""]
    lines += ["## Safety","- No automatic retries or fixes.","- Human review is required before remediation."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

if __name__ == "__main__": main()