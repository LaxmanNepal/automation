# Money Live Research

This engine adds a current-interest signal to a small, version-controlled bank of monetizable problem ideas.

## Schedule

- 10:00 Kuwait daily (`0 7 * * *` UTC)
- Manual workflow dispatch is also available.

## Method

The default implementation uses public Google News RSS searches for multiple queries attached to each opportunity.

For each opportunity it records:
- current result counts
- recent result titles
- a freshness signal
- proposed asset
- possible monetization path

## Outputs

- data/opportunities/live_research.json
- reports/opportunities/YYYY-MM-DD-money-live.md
- reports/opportunities/money-live-latest.md

## Interpretation

A higher signal means an idea deserves earlier research. It does **not** mean the idea is profitable, has guaranteed traffic, or will generate a specific amount of money.

## Human validation

Before building or spending money, validate:
1. real user problem
2. current search demand
3. existing competitors
4. acquisition/distribution path
5. realistic monetization
6. build and maintenance cost

The engine does not spend money, launch products, or make financial decisions automatically.