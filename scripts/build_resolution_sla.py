#!/usr/bin/env python3
"""Build resolution SLA metrics from the human-gated resolution history."""
import json
from datetime import datetime, timezone
from pathlib import Path

SRC=Path("data/workflows/resolution.json")
OUT=Path("data/workflows/resolution-sla.json")
REPORT=Path("reports/workflows/resolution-sla-latest.md")

def load(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError,json.JSONDecodeError,OSError): return None

def dt(v):
    try: return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception: return None

def hours(a,b):
    x,y=dt(a),dt(b)
    return round(max(0,(y-x).total_seconds())/3600,2) if x and y else None

def main():
    now=datetime.now(timezone.utc).isoformat()
    src=load(SRC)
    if not src or not src.get("items"):
        data={"version":1,"generated_at":now,"status":"waiting","items":[],"summary":{"open":0,"blocked":0,"validation_pending":0,"resolved":0,"reopened":0,"average_resolution_hours":None},"coverage":"Resolution ledger has no generated items yet.","human_validation_required":True}
    else:
        items=[]; counts={"open":0,"blocked":0,"validation_pending":0,"resolved":0,"reopened":0}; durations=[]
        for x in src.get("items",[]):
            st=x.get("resolution_state","open"); counts[st]=counts.get(st,0)+1
            hist=x.get("history",[])
            opened=hist[0].get("at") if hist else None
            resolved_at=None
            for e in hist:
                if e.get("resolution_state")=="resolved" and e.get("human_confirmation"): resolved_at=e.get("at")
            duration=hours(opened,resolved_at) if resolved_at else None
            if duration is not None: durations.append(duration)
            items.append({"resolution_id":x.get("id"),"workflow":x.get("workflow"),"stage":x.get("stage"),"state":st,"evidence_state":x.get("evidence_state"),"opened_at":opened,"resolved_at":resolved_at,"resolution_hours":duration,"human_confirmed":bool(x.get("human_confirmed")),"history_events":len(hist)})
        avg=round(sum(durations)/len(durations),2) if durations else None
        data={"version":1,"generated_at":now,"status":"healthy","items":items,"summary":{**counts,"average_resolution_hours":avg,"resolved_with_duration":len(durations)},"coverage":"Duration metrics are calculated only from recorded ledger timestamps and explicit human-confirmed resolutions.","human_validation_required":True,"interpretation":"SLA metrics describe recorded process time; they do not establish causality, productivity, or business impact."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    REPORT.parent.mkdir(parents=True,exist_ok=True)
    s=data["summary"]
    lines=["# Resolution SLA & Analytics","","Metrics are derived from recorded Resolution Ledger history.","",f"- Status: {data['status']}",f"- Open: {s.get('open',0)}",f"- Blocked: {s.get('blocked',0)}",f"- Validation pending: {s.get('validation_pending',0)}",f"- Resolved: {s.get('resolved',0)}",f"- Reopened: {s.get('reopened',0)}",f"- Average confirmed resolution time: {s.get('average_resolution_hours') if s.get('average_resolution_hours') is not None else 'not available'} hours","", "## Evidence boundary","Only explicit human-confirmed resolutions contribute to resolution duration. Missing timestamps are not treated as zero.",""]
    REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
