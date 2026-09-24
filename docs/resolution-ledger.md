# Resolution Ledger

Phase 1.10 preserves remediation history while keeping workflow evidence separate from human-confirmed resolution.

## States
- open: no later verification evidence is available.
- blocked: a later workflow run exists but is not successful.
- validation-pending: later workflow success is recorded, but human confirmation is still required.
- reopened: reserved for a human-confirmed issue that later becomes active again.
- resolved: reserved for explicit human confirmation; automation never assigns it.

## Evidence boundary
A later successful workflow run is execution evidence only. It does not prove that a particular code change caused the result or that the broader problem is solved.

## History
Each item keeps timestamped evidence/resolution transitions and linked workflow evidence. Existing history is retained when the scheduled job refreshes the ledger.

## Safety
No automatic retry, code modification, merge, publishing, spending, trading, external messaging, or automatic resolution is performed. Human review is required.