#!/usr/bin/env python3
"""Build historical resolution trend and descriptive escalation signals."""
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

SRC=Path("data/workflows/resolution.json")
OUT=Path("data/workflows/resolution-trends.json")
REPORT=Path("reports/workflows/resolution-trends-latest.md")

def load(p):
    try:return json.loads(p.read_text(encoding="utf-8"))
    except (FileNotFoundError,json.JSONDecodeError,OSError):return None

def parse(v):
    try:return datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception:return None

def main():
    now=datetime.now(timezone.utc)
    src=load(SRC) or {}
    items=src.get("items",[])
    daily={}
    escalations=[]
    for x in items:
        hist=x.get("history",[])
        for e in hist:
            d=(e.get("at") or "")[:10]
            if not d: continue
            row=daily.setdefault(d,{"date":d,"events":0,"opened":0,"resolved":0,"reopened":0,"blocked":0,"validation_pending":0})
            row["events"]+=1
            state=e.get("resolution_state")
            if state=="open": row["opened"]+=1
            elif state=="resolved" and e.get("human_confirmation"): row["resolved"]+=1
            elif state=="reopened": row["reopened"]+=1
            elif state=="blocked": row["blocked"]+=1
            elif state=="validation-pending": row["validation_pending"]+=1
        states=[e.get("resolution_state") for e in hist]
        if "reopened" in states:
            escalations.append({"resolution_id":x.get("id"),"workflow":x.get("workflow"),"stage":x.get("stage"),"type":"reopened","basis":"recorded reopened state"})
        if len(hist)>=3:
            escalations.append({"resolution_id":x.get("id"),"workflow":x.get("workflow"),"stage":x.get("stage"),"type":"repeated-history","event_count":len(hist),"basis":"3+ recorded resolution history events"})
    days=sorted(daily.values(),key=lambda x:x["date"])
    latest=days[-1] if days else None
    prior=days[-2] if len(days)>1 else None
    def delta(k): return latest[k]-prior[k] if latest and prior else None
    trend={"events":delta("events"),"resolved":delta("resolved"),"blocked":delta("blocked"),"reopened":delta("reopened")} if prior else {}
    data={"version":1,"generated_at":now.isoformat(),"status":"healthy" if items else "waiting","summary":{"records":len(items),"days_observed":len(days),"escalation_signals":len(escalations)},"daily":days[-30:],"latest_day":latest,"previous_day":prior,"day_over_day":trend,"escalation_signals":escalations,"coverage":"Trend values use only recorded Resolution Ledger history events; absent days are not treated as zero.","human_validation_required":True,"interpretation":"Trend and escalation signals are descriptive. They do not predict outcomes or establish causality, severity, root cause, or business impact."}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    lines=["# Resolution Trend & Escalation Intelligence","","Historical event trends from the Resolution Ledger.","",f"- Status: {data['status']}",f"- Records: {len(items)}",f"- Days observed: {len(days)}",f"- Escalation signals: {len(escalations)}"]
    if trend: lines += ["", "## Latest day-over-day change"]+[f"- {k}: {v:+d}" for k,v in trend.items() if v is not None]
    lines += ["","## Evidence boundary","Only recorded events are counted. Missing days are not zeros. Reopened or repeated-history records are signals for review, not automatic escalation decisions.",""]
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text("\n".join(lines),encoding="utf-8")
if __name__=="__main__":main()
