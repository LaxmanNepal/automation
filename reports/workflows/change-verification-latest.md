# Change Verification

This ledger checks whether a remediation-linked workflow has a later execution outcome in the available telemetry.

## Interpretation
- verified-by-later-success: a later successful run of the same workflow is recorded.
- still-failing: a later run exists but is not successful.
- waiting: there is not enough later telemetry to verify the outcome.

A later success is execution evidence only. The ledger does not claim that a particular code change caused the result; causality remains unverified.

## Safety
No automatic retry, code modification, merge, publish, spend, trade, or external message is performed. Human review is required.
