# Human Resolution Control

Phase 1.11 adds an explicit, audit-preserving human control surface for the Resolution Ledger.

## How it works

1. Open the **Resolution** tab in the Laxman OS dashboard.
2. Copy the displayed resolution ID.
3. Open the **Resolution Control** workflow in GitHub Actions.
4. Enter the resolution ID, choose one decision, and optionally add a note.
5. Review the workflow result and refresh the dashboard.

## Decisions

- `confirm-resolved`: explicitly marks the item resolved and records human confirmation.
- `reopen`: reopens a previously resolved item.
- `mark-blocked`: records that the issue is blocked pending further work.
- `mark-investigating`: returns the item to an open/investigating state.

## Audit trail

Decisions are append-only in `data/workflows/resolution-decisions.json`. The resolution item also receives a timestamped history event containing the decision and optional note.

## Safety boundary

The control workflow does not retry jobs, modify application code, merge pull requests, publish content, spend money, trade assets, or send external messages. A human must explicitly start the workflow and choose the decision.

A successful workflow run is still execution evidence; only `confirm-resolved` records an explicit human confirmation.
