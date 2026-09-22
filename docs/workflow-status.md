# Workflow Status Monitor

The monitor records recent GitHub Actions runs for the dashboard.

## Output
- `data/workflows/latest.json`

## Safety
The monitor is read-only against workflow execution. It does not start, cancel, merge, publish, spend, trade, or message externally. Dashboard links may open GitHub's manual workflow controls, but execution remains a human action.

## Coverage
The snapshot tracks the configured Laxman OS workflows and records the latest run plus a small recent history. Missing history is represented as `waiting`, not zero.
