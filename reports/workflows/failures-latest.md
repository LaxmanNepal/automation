# Failure Intelligence

Generated: 2026-11-12T17:57:30.110450+00:00

Status: **warning**

Repeated failures are grouped by workflow, failed stage, and conclusion. Root causes are not asserted without log evidence.

## 1. Remediation runbooks
- Conclusion: `failure`
- Failed stage: `build`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/43073455921
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## 2. Resolution ledger
- Conclusion: `failure`
- Failed stage: `ledger`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/42877990452
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## Safety
- No automatic retries or fixes.
- Human review is required before remediation.
