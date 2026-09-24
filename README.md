# Laxman OS — Automation

A GitHub-based personal automation and command system for Laxman Nepal.

## Mission

Turn recurring work into a measurable loop:

**Research → Evidence → Prioritize → Prepare → Human Review → Execute → Measure → Improve**

ChatGPT can provide strategy/research while GitHub Actions provides deterministic scheduled collection, validation, health checks and reports.

## Phase map

| Phase | System | State |
|---|---|---|
| 1 | Command Center | Active |
| 2 | GitHub Intelligence | Active |
| 3 | Action Queue | Active |
| 4 | Money Opportunity Engine | Active |
| 5 | Revenue Asset Factory | Active |
| 6 | YouTube Intelligence | Active |
| 7 | Content → Website → Money | Foundation |
| 8 | SEO Intelligence | Active |
| 9 | Website Intelligence | Active |
| 10 | Analytics | Foundation |
| 11 | AI Command Layer | Foundation |
| 12 | Automation Layer | Active |
| 13 | Personal Business OS | Foundation |
| 14 | Mobile / PWA | Active |
| 15 | Notifications | Digest foundation |

Detailed scope: docs/phases.md and docs/module-contract.md.

## Dashboard

index.html is the Laxman OS command center. It reads generated JSON/Markdown artifacts and provides overview, actions, module health, phase map and report links.

For GitHub Pages deployment, the dashboard workflow deploys changes pushed to `main` when GitHub Pages is configured for GitHub Actions.

## Daily operating loop — Kuwait time

- 09:00 command briefing
- 10:00 money research
- 10:30 revenue asset engine
- 10:45 build issue generator
- 11:00 YouTube opportunities
- 11:30 YouTube live research
- 12:00 GitHub health
- 12:30 problem detector
- 13:00 action queue
- 13:30 unified intelligence

GitHub cron schedules are UTC-based.

## Safety

- No automatic investing or trading.
- No automatic public publishing.
- No automatic merge.
- No automatic external messages.
- No automatic spending or commercial commitments.
- Automation can detect, research, prepare and report.
- Human review is required before consequential external actions.

## Data rule

Missing data is not treated as zero. Outputs distinguish waiting, healthy, warning, stale, unavailable and error states where applicable.

## Repository layout

- config/ — priorities, channels, projects, websites and business goals
- data/ — machine-readable module outputs
- docs/ — architecture, phase and module contracts
- scripts/ — dependency-light deterministic automation
- reports/ — human-readable outputs
- .github/workflows/ — scheduled automation
- index.html — dashboard
- manifest.webmanifest / sw.js — PWA foundation

Never commit tokens, API keys, cookies or other secrets.


Phase 1.13 Resolution Trend & Bottleneck Intelligence active
