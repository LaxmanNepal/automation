#!/usr/bin/env python3
"""Normalize an optional local analytics export."""
import json,pathlib
from datetime import datetime,timezone
ROOT=pathlib.Path(__file__).resolve().parents[1];src=ROOT/"data/analytics/input.json"
now=datetime.now(timezone.utc).isoformat()
if not src.exists():
    payload={"version":1,"generated_at":now,"status":"waiting","sources":[],"metrics":{},"coverage":"No analytics export supplied.","human_validation_required":True}
else:
    raw=json.loads(src.read_text())
    payload={"version":1,"generated_at":now,"status":"healthy","sources":raw.get("sources",[]),"metrics":raw.get("metrics",{}),"coverage":raw.get("coverage","Local export"),"human_validation_required":True}
(ROOT/"data/analytics/latest.json").write_text(json.dumps(payload,indent=2)+"\n")
