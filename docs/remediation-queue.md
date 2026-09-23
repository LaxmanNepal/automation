# Remediation Queue

Phase 1.5 converts Failure Intelligence signals into a structured human-review queue.

## Output
- data/workflows/remediation.json
- reports/workflows/remediation-latest.md

## Safety
The queue only prepares review items. It does not change code, retry jobs, merge pull requests, publish content, spend money, trade, or send external messages.

Root causes remain unverified until a human reviews the linked run and job logs.