# Money Opportunity Engine

The Opportunity Engine turns structured opportunity ideas into a ranked shortlist using impact, effort, and evidence strength.

## Important limitation

This v1 does not pretend that a score is market truth. Search demand, competition, pricing, and monetization must be validated before execution.

## Workflow

1. Add an opportunity to `data/opportunities/queue.yml`.
2. Run the engine.
3. Review `data/opportunities/latest.json` or `reports/opportunities/latest.md`.
4. Validate the highest-value candidates with current market/search evidence.
5. Move only validated work into the Action Queue.

The engine never spends money, publishes content, or launches a product automatically.
