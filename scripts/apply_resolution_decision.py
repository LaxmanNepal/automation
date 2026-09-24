#!/usr/bin/env python3
"""Apply an explicit human decision to the resolution ledger.

This script is only intended to run from the manually-triggered Resolution Control
workflow. It validates the target resolution, appends an audit record, and updates
the current ledger. It never infers a human decision.
"""
import argparse, json
from datetime import datetime, timezone
from pathlib import Path

BASE = Path("data/workflows")
RESOLUTION = BASE / "resolution.json"
DECISIONS = BASE / "resolution-decisions.json"

ALLOWED = {
    "confirm-resolved": ("resolved", True),
    "reopen": ("reopened", False),
    "mark-blocked": ("blocked", False),
    "mark-investigating": ("open", False),
}

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--resolution-id", required=True)
    ap.add_argument("--decision", choices=sorted(ALLOWED), required=True)
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    ledger = load(RESOLUTION, {})
    items = ledger.get("items", [])
    item = next((x for x in items if x.get("id") == args.resolution_id), None)
    if item is None:
        raise SystemExit(f"Unknown resolution id: {args.resolution_id}")

    now = datetime.now(timezone.utc).isoformat()
    resolution_state, confirmed = ALLOWED[args.decision]
    decision = {
        "at": now,
        "resolution_id": args.resolution_id,
        "decision": args.decision,
        "resolution_state": resolution_state,
        "human_confirmed": confirmed,
        "note": args.note.strip(),
    }

    store = load(DECISIONS, {"version": 1, "decisions": []})
    store.setdefault("decisions", []).append(decision)
    store["generated_at"] = now
    store["status"] = "healthy"
    store["human_validation_required"] = True
    DECISIONS.parent.mkdir(parents=True, exist_ok=True)
    DECISIONS.write_text(json.dumps(store, indent=2) + "\n", encoding="utf-8")

    history = list(item.get("history", []))
    history.append({
        "at": now,
        "evidence_state": item.get("evidence_state", "waiting"),
        "resolution_state": resolution_state,
        "signature": f"human-decision|{args.decision}|{now}",
        "evidence_run_id": item.get("evidence_run_id"),
        "evidence_url": item.get("evidence_url"),
        "human_confirmation": confirmed,
        "human_decision": args.decision,
        "note": args.note.strip(),
    })
    item.update({
        "resolution_state": resolution_state,
        "human_confirmed": confirmed,
        "human_decision": args.decision,
        "human_decision_at": now,
        "human_decision_note": args.note.strip(),
        "history": history,
    })
    ledger["generated_at"] = now
    ledger["status"] = "healthy" if resolution_state == "resolved" else ("warning" if resolution_state == "blocked" else "waiting")
    ledger["human_validation_required"] = True
    ledger["resolution_boundary"] = "Automation never declares a real-world issue resolved. Human confirmation is required."
    RESOLUTION.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {args.decision} to {args.resolution_id}")

if __name__ == "__main__":
    main()
