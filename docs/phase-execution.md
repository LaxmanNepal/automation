# Phase Execution Plan

Each phase has four gates: **Build → Verify → Human Review → Activate**.

| Phase | Build target | Verification | Activation gate |
|---|---|---|---|
| 1 | Command Center | Dashboard loads without live data | Human reviews UI |
| 2 | GitHub Intelligence | Inventory/health outputs valid JSON | Human reviews findings |
| 3 | Action Queue | Priority queue generated | Human selects actions |
| 4 | Money Engine | Research signals recorded | Human validates opportunity |
| 5 | Revenue Assets | Asset spec + issue generated | Human approves build |
| 6 | YouTube Intelligence | Topic/live reports generated | Human validates topic |
| 7 | Content → Money | Mapping rules + asset links | Human approves publishing |
| 8 | SEO | Static checks + report | Human reviews fixes |
| 9 | Website | Health checks + findings | Human reviews remediation |
| 10 | Analytics | Normalized schema + freshness | Human connects/approves source |
| 11 | AI Command | Evidence-based command | Human chooses execution |
| 12 | Automation | Scheduled workflows | Human reviews workflow permissions |
| 13 | Business OS | Goals/projects/assets model | Human maintains priorities |
| 14 | PWA | Manifest + offline shell | Human installs/tests |
| 15 | Notifications | Alert digest | Human explicitly enables delivery |

## Definition of complete

A phase is not considered production-complete merely because files exist. It must produce its documented output, handle missing data explicitly, and preserve the human approval gate.

## Global safety gates

Never automate:
- financial transactions or trading
- spending or purchases
- public publishing
- external messaging
- pull-request merging
- destructive repository changes
- commercial commitments

Automation may research, detect, summarize, validate, prepare files/issues, and report results.
