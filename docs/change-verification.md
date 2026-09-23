# Change Verification

Phase 1.8 connects human remediation records to later workflow executions.

## Verification states

- \`verified-by-later-success\`: a later successful run of the same workflow is recorded.
- \`still-failing\`: a later run exists but is not successful.
- \`waiting\`: available telemetry does not contain a later run that can verify the outcome.

## Evidence boundary

The module links a remediation item to its recorded failure run IDs and compares those with later runs from the same workflow. A later success is execution evidence, not proof that a particular code change caused the success. Causality remains unverified.

Because the workflow-status module retains only recent telemetry, an old failure may remain \`waiting\` when its later verification run is outside the retained window.

## Safety

This module only reads telemetry and writes a ledger/report. It does not retry workflows, modify code, merge pull requests, publish content, spend money, trade, or send external messages. Human validation is required.
