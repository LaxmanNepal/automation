# YouTube Live Research

This layer adds current freshness signals to the maintained YouTube topic bank.

## Free default

The workflow queries Google News RSS for each topic. It requires no API key.

## Optional YouTube API

Set a repository secret named `YOUTUBE_API_KEY` to collect recent YouTube search results through the official YouTube Data API.

The key is optional and is never written into repository files.

## Schedule

- 11:30 Kuwait daily
- Manual workflow dispatch is also available.

## Outputs

- `data/youtube/live_research.json`
- `reports/youtube/YYYY-MM-DD-live.md`
- `reports/youtube/live-latest.md`

## Meaning of the signal

The freshness signal is a research-prioritization indicator based on returned current results. It is **not** a forecast of views, subscribers, rankings, or revenue.

## Human validation

Before publishing, verify the actual YouTube search results, competition, audience fit, factual accuracy, and monetization. The workflow does not publish automatically.
