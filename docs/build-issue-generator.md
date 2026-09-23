# Build Issue Generator

Turns revenue-asset specifications into implementation-ready GitHub issue specs.

## Schedule
- 10:45 Kuwait daily (45 7 * * * UTC)
- Manual workflow dispatch is available.

## Pipeline
`money research -> revenue asset -> build issue specification -> human-approved implementation`

## Outputs
- `data/assets/issue_specs.json`
- `reports/assets/YYYY-MM-DD-issues.md`
- `reports/assets/issues-latest.md`

Each issue includes the objective, problem, audience, asset, monetization, MVP checklist, SEO requirements, analytics events, acceptance criteria, research signal, and a safety gate.

## Creating real issues
Scheduled runs only generate specs. Manual dispatch with `create_issues=true` creates GitHub issues. Creation is deduplicated with a stable `laxman-os-asset-id` marker.

## Safety
No merging, deployment, publishing, spending, or commercial commitment occurs automatically. Human approval remains required.
