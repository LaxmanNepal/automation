#!/usr/bin/env python3
"""Build descriptive current resolution workload and review-capacity signals."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SRC=Path("data/workflows/resolution.json")
OUT=Path("data/workflows/resolution-capacity.json")
REPORT=Path("reports/workflows/resolution-capacity-latest.md")
UNRESOLVED={"open","blocked","validation-pending","reopened"}
BUCKETS=[("under_24h",0,24),("24_to_72h",24,72),("3_to_7d",72,168),("7_to_14d",168,336),("14d_plus",336,None)]

def load(p):
    try: return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError,json.JSONDecodeError,OSError): return None
def parse(v):
    try: return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception: return None
def age_hours(v,now):
    x=parse(v)
    return round(max(0,(now-x).total_seconds())/3600,2) if x else None
def band(n):
    if n is None: return "unavailable"
    if n <= 2: return "low"
    if n <= 5: return "medium"
    return "high"

def main():
    now=datetime.now(timezone.utc); src=load(SRC); items=(src or {}).get("items",[])
    unresolved=[x for x in items if x.get("resolution_state") in UNRESOLVED]
    ages=[]; wf=Counter(); st=Counter(); buckets={k:0 for k,_,_ in BUCKETS}; missing=0
    for x in unresolved:
        wf[x.get("workflow") or "unavailable"]+=1; st[x.get("stage") or "unavailable"]+=1
        hist=x.get("history",[]); opened=hist[0].get("at") if hist else None; a=age_hours(opened,now)
        if a is None: missing+=1; continue
        ages.append(a)
        for key,lo,hi in BUCKETS:
            if a >= lo and (hi is None or a < hi): buckets[key]+=1; break
    if not items:
        data={"version":1,"generated_at":now.isoformat(),"status":"waiting",
              "summary":{"total_records":0,"unresolved":0,"open":0,"blocked":0,"validation_pending":0,"reopened":0,"human_confirmation_pending":0},
              "review_load":{"band":"unavailable","current_unresolved":0,"basis":"No Resolution Ledger records are available."},
              "aging":{"buckets":{k:None for k,_,_ in BUCKETS},"records_with_age":0,"records_missing_age":0},
              "workflow_workload":[],"stage_workload":[],"coverage":"Waiting for Resolution Ledger records.",
              "human_validation_required":True,
              "interpretation":"Current review-load signals are descriptive only; they do not forecast outcomes or staffing requirements."}
    else:
        counts=Counter(x.get("resolution_state","open") for x in items)
        data={"version":1,"generated_at":now.isoformat(),"status":"healthy",
              "summary":{"total_records":len(items),"unresolved":len(unresolved),"open":counts.get("open",0),
                         "blocked":counts.get("blocked",0),"validation_pending":counts.get("validation-pending",0),
                         "reopened":counts.get("reopened",0),"resolved":counts.get("resolved",0),
                         "human_confirmation_pending":sum(1 for x in unresolved if x.get("human_confirmed") is not True)},
              "review_load":{"band":band(len(unresolved)),"current_unresolved":len(unresolved),
                             "basis":"Descriptive band based only on current unresolved record count: low 0–2, medium 3–5, high 6+."},
              "aging":{"buckets":buckets,"records_with_age":len(ages),"records_missing_age":missing,
                       "average_unresolved_hours":round(sum(ages)/len(ages),2) if ages else None,
                       "oldest_unresolved_hours":max(ages) if ages else None},
              "workflow_workload":[{"workflow":k,"unresolved_count":v} for k,v in wf.most_common()],
              "stage_workload":[{"stage":k,"unresolved_count":v} for k,v in st.most_common()],
              "coverage":"Current unresolved Resolution Ledger records and their recorded history timestamps.",
              "human_validation_required":True,
              "interpretation":"Review-load and aging indicators describe currently recorded work only. They do not forecast resolution, staffing needs, productivity, severity, causality, or business impact."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    s=data["summary"]; a=data["aging"]; rl=data["review_load"]
    lines=["# Resolution Capacity & Review Load","","Descriptive current workload and aging signals from the Resolution Ledger.","",
           f"- Status: {data['status']}",f"- Total records: {s['total_records']}",f"- Unresolved: {s['unresolved']}",
           f"- Open: {s['open']}",f"- Blocked: {s['blocked']}",f"- Validation pending: {s['validation_pending']}",
           f"- Reopened: {s['reopened']}",f"- Human confirmation pending: {s['human_confirmation_pending']}",
           f"- Review-load band: {rl['band']}",f"- Review-load basis: {rl['basis']}","","## Aging buckets"]
    lines += [f"- {k}: {v if v is not None else 'not available'}" for k,v in a["buckets"].items()]
    lines += ["","## Evidence boundary","Aging uses the first recorded history timestamp for unresolved records. Missing timestamps are unavailable, not zero.",
              "Review-load bands are descriptive thresholds over the current unresolved count; they are not staffing or outcome forecasts.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
