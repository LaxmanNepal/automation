#!/usr/bin/env python3
"""Build descriptive resolution concentration and aging signals."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SRC=Path("data/workflows/resolution.json")
OUT=Path("data/workflows/resolution-bottlenecks.json")
REPORT=Path("reports/workflows/resolution-bottlenecks-latest.md")

def load(path):
    try: return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError,json.JSONDecodeError,OSError): return None

def dt(v):
    try: return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception: return None

def age_hours(at, now):
    x=dt(at)
    return round(max(0,(now-x).total_seconds())/3600,2) if x else None

def main():
    now=datetime.now(timezone.utc)
    src=load(SRC)
    items=(src or {}).get("items",[])
    if not items:
        data={"version":1,"generated_at":now.isoformat(),"status":"waiting","summary":{"total":0,"unresolved":0,"open":0,"blocked":0,"validation_pending":0,"reopened":0},"aging":{"average_unresolved_hours":None,"oldest_unresolved_hours":None},"workflow_concentration":[],"stage_concentration":[],"state_events":[],"signals":[],"coverage":"Resolution ledger has no generated items yet.","human_validation_required":True,"interpretation":"Concentration signals describe recorded process patterns; they do not establish causality or identify a root cause."}
    else:
        counts=Counter(x.get("resolution_state","open") for x in items)
        unresolved=[x for x in items if x.get("resolution_state") in {"open","blocked","validation-pending","reopened"}]
        ages=[]
        wf=Counter(); st=Counter(); events=Counter()
        for x in unresolved:
            hist=x.get("history",[])
            opened=hist[0].get("at") if hist else None
            a=age_hours(opened,now)
            if a is not None: ages.append(a)
            wf[x.get("workflow") or "unavailable"]+=1
            st[x.get("stage") or "unavailable"]+=1
        for x in items:
            for e in x.get("history",[]):
                key=(x.get("workflow") or "unavailable",x.get("stage") or "unavailable")
                events[key]+=1
        workflow_conc=[{"workflow":k,"unresolved_count":v} for k,v in wf.most_common()]
        stage_conc=[{"stage":k,"unresolved_count":v} for k,v in st.most_common()]
        signals=[]
        for k,v in wf.items():
            if v>=2: signals.append({"type":"workflow-concentration","workflow":k,"count":v,"basis":"2+ unresolved resolution records in the same workflow"})
        for k,v in st.items():
            if v>=2: signals.append({"type":"stage-concentration","stage":k,"count":v,"basis":"2+ unresolved resolution records in the same stage"})
        for k,v in events.items():
            if v>=3: signals.append({"type":"recurring-history","workflow":k[0],"stage":k[1],"event_count":v,"basis":"3+ recorded history events for the same workflow/stage"})
        data={"version":1,"generated_at":now.isoformat(),"status":"healthy","summary":{"total":len(items),"unresolved":len(unresolved),"open":counts.get("open",0),"blocked":counts.get("blocked",0),"validation_pending":counts.get("validation-pending",0),"reopened":counts.get("reopened",0),"resolved":counts.get("resolved",0)},"aging":{"average_unresolved_hours":round(sum(ages)/len(ages),2) if ages else None,"oldest_unresolved_hours":max(ages) if ages else None,"records_with_open_time":len(ages)},"workflow_concentration":workflow_conc,"stage_concentration":stage_conc,"state_events":[{"workflow":k[0],"stage":k[1],"history_events":v} for k,v in events.most_common()],"signals":signals,"coverage":"Signals are calculated from the current Resolution Ledger and its recorded history events.","human_validation_required":True,"interpretation":"These are concentration and aging signals only. Repetition or age does not prove a bottleneck cause, remediation quality, or business impact."}
    OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    s=data["summary"]; a=data["aging"]
    lines=["# Resolution Trend & Bottleneck Intelligence","","Descriptive concentration and aging signals from recorded Resolution Ledger evidence.","",f"- Status: {data['status']}",f"- Total records: {s['total']}",f"- Unresolved: {s['unresolved']}",f"- Open: {s['open']}",f"- Blocked: {s['blocked']}",f"- Validation pending: {s['validation_pending']}",f"- Reopened: {s['reopened']}",f"- Resolved: {s.get('resolved',0)}",f"- Average unresolved age: {a['average_unresolved_hours'] if a['average_unresolved_hours'] is not None else 'not available'} hours",f"- Oldest unresolved age: {a['oldest_unresolved_hours'] if a['oldest_unresolved_hours'] is not None else 'not available'} hours",""]
    lines+=["## Concentration signals"]
    if data["signals"]:
        lines += [f"- {x.get('type')}: {x.get('workflow') or x.get('stage')} — {x.get('count') or x.get('event_count')} ({x.get('basis')})" for x in data["signals"]]
    else: lines.append("- No concentration signal met the descriptive threshold.")
    lines += ["","## Evidence boundary","Aging uses the first recorded history timestamp for unresolved records. Repeated events and concentrations do not prove causality or a root cause. Missing timestamps remain unavailable, not zero.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True); REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__": main()
