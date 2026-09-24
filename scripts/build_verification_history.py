#!/usr/bin/env python3
import json
from datetime import datetime, timezone
from pathlib import Path
B=Path('data/workflows')
def load(n):
    try:return json.loads((B/n).read_text())
    except (FileNotFoundError,json.JSONDecodeError,OSError):return None
def main():
    now=datetime.now(timezone.utc).isoformat(); v=load('change-verification.json'); t=load('latest.json')
    if v is None:data={'version':1,'generated_at':now,'status':'waiting','timelines':[],'coverage':'Change verification data unavailable.','human_validation_required':True}
    else:
        timelines=[]
        for i in v.get('items',[]):
            row=next((x for x in (t or {}).get('workflows',[]) if x.get('workflow')==i.get('workflow')),None); prev=set(i.get('previous_failure_run_ids',[])); events=[]
            for r in (row or {}).get('recent_runs',[]):
                rid=r.get('id'); role='failure-evidence' if rid in prev else ('verification-evidence' if rid==i.get('verification_run_id') else 'observed-run'); events.append({'run_id':rid,'role':role,'conclusion':r.get('conclusion'),'created_at':r.get('created_at'),'updated_at':r.get('updated_at'),'url':r.get('html_url')})
            state={'verified-by-later-success':'verified','still-failing':'still-failing'}.get(i.get('verification_state'),'waiting'); timelines.append({'id':'timeline-'+str(i.get('remediation_id','unknown')),'remediation_id':i.get('remediation_id'),'workflow':i.get('workflow'),'stage':i.get('stage'),'state':state,'events':events,'causal_claim':'unverified','human_validation_required':True})
        states={x['state'] for x in timelines}; data={'version':1,'generated_at':now,'status':'warning' if 'still-failing' in states else ('healthy' if timelines and states=={'verified'} else 'waiting'),'timelines':timelines,'coverage':'Chronological failure and later-run evidence from retained telemetry.','human_validation_required':True}
    (B/'verification-history.json').write_text(json.dumps(data,indent=2)+'\n'); p=Path('reports/workflows/verification-history-latest.md'); p.parent.mkdir(parents=True,exist_ok=True); p.write_text('# Verification History\n\nChronological remediation-linked workflow evidence. A later success is execution evidence only; causality remains unverified.\n\nNo automatic retry, code change, merge, publish, spend, trade, or external messaging.\n')
if __name__=='__main__':main()
