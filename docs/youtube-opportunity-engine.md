# YouTube Opportunity Engine

The engine maintains a small, version-controlled topic bank for Laxman Nepal's Nepali and English channels.

## Schedule

- 11:00 Kuwait daily (`0 8 * * *` UTC)
- Can also be run manually from GitHub Actions.

## Output

- `data/youtube/latest.json`
- `reports/youtube/YYYY-MM-DD.md`
- `reports/youtube/latest.md`

## What it does

1. Reads the maintained topic bank.
2. Scores topics using viewer-intent and freshness signals.
3. Separates Nepali and English opportunities.
4. Produces a production-oriented shortlist.

## Important limitation

This V1 does **not** access live YouTube/Google Trends search volume. A topic marked `verify-current` must be checked for current demand, competition, freshness, and monetization before recording.

## Human gate

The engine does not publish videos, buy ads, or make channel changes automatically. Final topic selection and publishing remain human decisions.