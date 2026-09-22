# Workflow Status Monitor

The monitor records recent GitHub Actions runs for the dashboard.

## Output
- `data/workflows/latest.json`

## Execution telemetry
For each configured workflow, the snapshot records:
- latest run status and conclusion
- latest run duration
- failed job/stage when GitHub exposes a failed job
- most recent successful run
- recent run history (up to five runs)
- direct GitHub run/workflow URLs

## Dashboard controls
The Command Center exposes:
- **Run workflow** — opens GitHub's manual workflow page
- **Inspect run** — opens the latest recorded run
- **Retry failed** — opens the failed run for manual review/retry

These are navigation controls only. The dashboard never starts or retries a workflow itself.

## Safety
The monitor is read-only against workflow execution. It does not start, cancel, merge, publish, spend, trade, or message externally. Execution remains a human action.

## Coverage
The snapshot tracks the configured Laxman OS workflows. Missing history is represented as `waiting`, not zero.
