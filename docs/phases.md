# Laxman OS — Phases 1–15

This repository is being developed as a human-in-the-loop operating system.

## 1. Command Center
Dashboard for queue, module health, reports, schedules and safe manual workflow links.

## 2. GitHub Intelligence
Repository inventory, workflow health, stale work, dependency/security signals and actionable findings.

## 3. Action Queue
One prioritized queue combining money, YouTube, GitHub, SEO and website findings.

## 4. Money Opportunity Engine
Research signals that can become traffic, leads, tools, templates or other assets.

## 5. Revenue Asset Factory
Turn validated opportunities into implementation-ready asset specifications and issues.

## 6. YouTube Intelligence
Topic bank + live research + channel-specific opportunity reports.

## 7. Content → Website → Money
Connect videos to searchable pages, tools and monetization metadata without automatic publishing.

## 8. SEO Intelligence
Static-site and content checks with suggested fixes and PR-oriented output.

## 9. Website Intelligence
Availability, freshness, link and metadata checks for configured web properties.

## 10. Analytics
Normalize available metrics into one schema and expose data freshness/coverage.

## 11. AI Command Layer
Generate a concise daily command from evidence already collected by the system.

## 12. Automation Layer
Scheduled jobs, deterministic scripts and safe handoffs between modules.

## 13. Personal Business OS
Goals, projects, routines and business assets in configuration rather than hard-coded logic.

## 14. Mobile/PWA
Responsive dashboard with installable PWA metadata and offline shell.

## 15. Notifications
Create an alert digest and optional notification hooks; sending remains explicitly gated.

## Safety model
Research can be automated. Changes that publish, spend money, trade, send external messages, merge code, or make commercial commitments require human action.


## Phase 1.10 — Resolution Ledger

Preserves remediation-linked history and separates workflow evidence from human-confirmed resolution. States include open, blocked, validation-pending, reopened, and resolved; automation may record evidence but never assigns resolved without human confirmation.


## Phase 1.11 — Human Resolution Control Center

Adds an explicit human decision workflow for resolution records. Decisions are append-only, auditable, and reflected in the Resolution dashboard.

- `confirm-resolved` records explicit human confirmation.
- `reopen` reopens a previously confirmed item.
- `mark-blocked` records a blocked state.
- `mark-investigating` returns an item to open/investigating.
- Dashboard exposes the resolution ID and a link to the manual GitHub Actions control.
- Automation never infers or declares human resolution.


## Phase 1.12 — Resolution SLA & Analytics

Measures recorded resolution lifecycle times and state counts from explicit ledger evidence. Missing timestamps remain unavailable; no causal or business-impact claims are made.


## Phase 1.13 — Resolution Trend & Bottleneck Intelligence

Adds descriptive resolution-state concentration, unresolved aging, workflow/stage concentration, and recurring history-event signals. These signals are observational only and do not establish causal bottlenecks or root causes.
