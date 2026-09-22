# Laxman OS Module Contract

Every module should expose:
- input data under data/
- generated machine-readable output as JSON
- a human-readable report under reports/
- generated_at timestamp
- source/scope metadata
- explicit freshness/coverage status
- human_validation_required when a decision is involved

A module must not silently treat missing data as zero. Missing, stale and unavailable are distinct states.

## Standard status values
- healthy
- warning
- stale
- unavailable
- error
- waiting

## Evidence rule
Recommendations are generated from recorded evidence. They are not guarantees of traffic, revenue, rankings, subscribers or business results.
