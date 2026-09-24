#!/usr/bin/env python3
"""Build a human-gated resolution ledger from workflow evidence."""
import json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("data/workflows")
REMEDIATION = BASE / "remediation.json"
VERIFICATION = BASE / "change-verification.json"
PREVIOUS = BASE / "resolution.json"
OUT = BASE / "resolution.json"
REPORT = Path("reports/workflows/resolution-latest.md")\nDECISIONS = BASE / "resolution-decisions.json"

def load(path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default

def evidence_state(item, verification):
    row = next((x for x in (verification or {}).get("items", []) if x.get("remediation_id") == item.get("id")), None)
    if not row: return "waiting", None
    state = row.get("verification_state")
    if state == "verified-by-later-success": return "verified", row
    if state == "still-failing": return "still-failing", row
    return "waiting", row

def latest_decisions():\n    data = load(DECISIONS, {}) or {}\n    latest = {}\n    for decision in data.get("decisions", []):\n        rid = decision.get("resolution_id")\n        if rid:\n            latest[rid] = decision\n    return latest\n\ndef derive_resolution(evidence, previous, decision):\n    if decision:\n        return decision.get("resolution_state") or previous or "open"
    if evidence == "verified":
        return "validation-pending" if previous not in {"resolved", "reopened"} else previous
    if evidence == "still-failing": return "blocked"
    return "open" if previous not in {"resolved", "reopened"} else previous

def main():
    now = datetime.now(timezone.utc).isoformat()
    remediation, verification = load(REMEDIATION), load(VERIFICATION)
    old = load(PREVIOUS, {}) or {}
    old_items = {x.get("id"): x for x in old.get("items", [])}\n    decisions = latest_decisions()
    if remediation is None or verification is None:
        data={"version":1,"generated_at":now,"status":"waiting","items":[],"coverage":"Remediation or change-verification evidence is unavailable.","human_validation_required":True}
    else:
        items=[]
        for rem in remediation.get("items", []):
            item_id="resolution-"+str(rem.get("id","unknown"))
            previous=old_items.get(item_id,{})
            evidence,vrow=evidence_state(rem,verification)
            decision=decisions.get(item_id)\n            resolution=derive_resolution(evidence,previous.get("resolution_state"),decision)
            history=list(previous.get("history",[]))
            signature=evidence+"|"+resolution+"|"+str((vrow or {}).get("verification_run_id"))+"|"+str((decision or {}).get("at"))
            if not history or history[-1].get("signature") != signature:
                history.append({"at":now,"evidence_state":evidence,"resolution_state":resolution,"signature":signature,"evidence_run_id":(vrow or {}).get("verification_run_id"),"evidence_url":(vrow or {}).get("verification_run_url"),"human_confirmation":bool((decision or {}).get("human_confirmed", False)),"human_decision":(decision or {}).get("decision"),"human_decision_at":(decision or {}).get("at"),"note":(decision or {}).get("note","")})
            items.append({"id":item_id,"remediation_id":rem.get("id"),"workflow":rem.get("workflow"),"stage":rem.get("stage"),"priority":rem.get("priority"),"evidence_state":evidence,"resolution_state":resolution,"human_confirmation_required":True,"human_confirmed":bool((decision or {}).get("human_confirmed", False)),"human_decision":(decision or {}).get("decision"),"human_decision_at":(decision or {}).get("at"),"human_decision_note":(decision or {}).get("note",""),"causal_claim":"unverified","evidence_run_id":(vrow or {}).get("verification_run_id"),"evidence_url":(vrow or {}).get("verification_run_url"),"history":history})
        states={x["resolution_state"] for x in items}
        data={"version":1,"generated_at":now,"status":"warning" if "blocked" in states else ("healthy" if items else "waiting"),"items":items,"coverage":"Persistent remediation state built from retained verification evidence.","human_validation_required":True,"resolution_boundary":"Automation never declares a real-world issue resolved. Human confirmation is required.","decision_source":"data/workflows/resolution-decisions.json"}
    OUT.parent.mkdir(parents=True,exist_ok=True)
    OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    lines=["# Resolution Ledger","","This ledger preserves remediation history and separates workflow evidence from human-confirmed resolution.","","## Resolution states","- open: no later verification evidence is available.","- blocked: a later workflow run exists but is not successful.","- validation-pending: later workflow success is recorded, but human confirmation is still required.","- reopened: reserved for a human-confirmed issue that later becomes active again.","- resolved: reserved for explicit human confirmation; automation does not assign it.","","## Evidence boundary","A later successful workflow run is execution evidence only. It does not prove causality or that the broader problem is solved.","","## Safety","No automatic retry, code change, merge, publish, spend, trade, external messaging, or automatic resolution is performed. Human review remains required.",""]
    for item in data.get("items",[]):
        lines += ["## "+str(item.get("workflow","Workflow")),"- Remediation: "+str(item.get("remediation_id")),"- Evidence state: "+str(item.get("evidence_state")),"- Resolution state: "+str(item.get("resolution_state")),"- Human confirmed: "+str(item.get("human_confirmed")),"- Human decision: "+str(item.get("human_decision") or "none"),"- Decision note: "+str(item.get("human_decision_note") or "none"),"- Evidence run: "+str(item.get("evidence_run_id")),""]
    REPORT.write_text("\n".join(lines),encoding="utf-8")

if __name__=="__main__": main()
