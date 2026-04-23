# Promotion Policy (Memory, Knowledge, Skill)

This policy ensures P6 promotion behavior is explicit and auditable.

## Promotion scopes
1. Project scope
- applies only to current project context.
2. Global scope
- reusable across projects after stronger evidence.

## Promotion types
1. Memory promotion
- semantic candidates accepted into stable memory notes.
2. Knowledge promotion
- validated insights written as knowledge candidates.
3. Skill promotion
- repeated successful patterns converted into skill events.

## Evidence gate
A promotion must include:
- source stage(s)
- rationale
- confidence
- observed impact or expected impact

## Decision flow
1. P6 consolidates candidates.
2. Promotion manager proposes promotions.
3. Evaluator checks policy compliance.
4. Decision is written to `promotions/promotion_decisions.jsonl`.

## Minimum event fields
- ts_utc
- run_id
- promotion_type (`memory|knowledge|skill`)
- scope (`project|global`)
- decision (`approved|rejected`)
- rationale
- confidence
