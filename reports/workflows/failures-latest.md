# Failure Intelligence

Generated: 2026-11-15T16:50:58.499034+00:00

Status: **warning**

Repeated failures are grouped by workflow, failed stage, and conclusion. Root causes are not asserted without log evidence.

## 1. Remediation runbooks
- Conclusion: `failure`
- Failed stage: `build`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/43616931049
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## 2. Resolution ledger
- Conclusion: `failure`
- Failed stage: `ledger`
- Occurrences in latest telemetry: **1**
- Evidence: https://github.com/LaxmanNepal/automation/actions/runs/43484238396
- Root cause: **unverified**
- Next action: Inspect the linked run and failed job logs, confirm the failing stage, then make a targeted fix.

## Safety
- No automatic retries or fixes.
- Human review is required before remediation.
