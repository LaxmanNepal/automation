# Validation Evidence

Phase 1.7 records whether monitored workflows have a recent successful execution.

## Interpretation
`validated` means the latest recorded workflow conclusion is `success`. `needs-validation` means the latest run is not successful. `waiting` means no conclusion is available.

This is workflow evidence, not proof that a wider application or business objective is complete.

## Safety
The module only reads telemetry and writes a report. It does not execute, retry, modify, merge, publish, spend, trade, or message externally.
