# Remediation Runbooks

Deterministic review checklists generated from remediation evidence.

Generated: 2026-11-01T16:53:19.933472+00:00

## 1. Resolution ledger
- Stage: ledger
- Priority: normal
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/41095438078
- Root cause: **unverified**
- Checklist:
  1. Open the linked workflow run.
  2. Inspect the failed job and relevant step logs.
  3. Confirm whether the failure is reproducible or transient.
  4. Identify the smallest evidence-backed corrective change.
  5. Review the proposed change before editing code.
  6. Run the relevant validation workflow after the change.

## 2. Unified intelligence
- Stage: intelligence
- Priority: normal
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/41216712380
- Root cause: **unverified**
- Checklist:
  1. Open the linked workflow run.
  2. Inspect the failed job and relevant step logs.
  3. Confirm whether the failure is reproducible or transient.
  4. Identify the smallest evidence-backed corrective change.
  5. Review the proposed change before editing code.
  6. Run the relevant validation workflow after the change.

## Safety
Runbooks provide review guidance only. They do not edit code, retry runs, merge PRs, publish, spend, trade, or message externally.
