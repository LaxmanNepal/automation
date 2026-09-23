# Failure Intelligence Center

Failure Intelligence groups recent unsuccessful GitHub Actions runs by workflow, failed stage, and conclusion.

## Output
- `data/workflows/failures.json`
- `reports/workflows/failures-latest.md`

## Interpretation
A grouped failure is an evidence signal, not a proven root cause. The system does not infer causes from a failure name alone. Linked runs and job logs must be reviewed before remediation.

## Schedule
Runs daily at 10:00 UTC (13:00 Kuwait) and can also be started manually from GitHub Actions.

## Safety
No automatic retries, fixes, merges, publishing, spending, trading, or external messaging. Human review is required before remediation.
