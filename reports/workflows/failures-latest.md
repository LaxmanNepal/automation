# Failure Intelligence

Generated: 2026-10-05T19:06:58.097639+00:00

Status: **warning**

Repeated failures are grouped by workflow, failed stage, and conclusion. Root causes are not asserted without log evidence.

## 1. Remediation runbooks
- Conclusion: `failure`
- Failed stage: `build`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/37213098624
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## 2. Resolution ledger
- Conclusion: `failure`
- Failed stage: `ledger`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/37132267255
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## Safety
- No automatic retries or fixes.
- Human review is required before remediation.
