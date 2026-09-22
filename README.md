# Laxman OS — Automation

A GitHub-based automation hub for Laxman Nepal.

## Mission

Turn recurring work into a measurable loop:

**Research → Prioritize → Execute → Test → Report → Improve**

This repository is the execution layer. ChatGPT can act as the strategy/research layer, while GitHub Actions handles scheduled validation, health checks, and report generation.

## V1 priorities

1. Money opportunities
2. YouTube growth
3. GitHub/project health
4. Website + SEO
5. Analytics
6. Digital assets
7. Finance / NEPSE information tracking

## Safety rules

- No automatic investing or trading.
- No automatic publishing of public content.
- No automatic merge of code changes.
- Scheduled automation may detect, validate, report, and prepare work.
- Human review is required before consequential external actions.

## Repository layout

```
config/       Priorities, channels, and project registry
docs/         Architecture and automation rules
scripts/      Small dependency-free automation scripts
reports/      Generated daily/health reports
data/         Structured automation data
.github/      GitHub Actions workflows
```

## Daily operating loop

- **09:00 Kuwait:** daily command briefing / opportunity review
- **12:00 Kuwait:** GitHub health and fix queue
- **Evening:** analytics + progress review

GitHub Actions times are stored in UTC because GitHub cron schedules are UTC-based. Kuwait is UTC+3, so 09:00 Kuwait is 06:00 UTC and 12:00 Kuwait is 09:00 UTC.

## Setup

The V1 workflows use the built-in GitHub Actions token for this repository. For scanning additional repositories, add a repository secret named `GH_PAT` with the minimum read permissions required for those repositories.

Never commit tokens, API keys, cookies, or other secrets.

## Status

V1 foundation is being built incrementally.