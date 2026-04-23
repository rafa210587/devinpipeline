# Orchestration Policy

## Stage state machine
- Allowed states: `pending`, `running`, `completed`, `failed`, `skipped`, `blocked`.
- Transition rule: a stage can start only if all predecessor stages are terminal and policy allows continuation.

## Stage contracts
- P0 produces a review-ready spec and the root promotes it to `approved_intake_spec` only after human approval.
- P0 output always feeds P1.
- If route mode is `pre_briefed`, P1 runs in a reduced validation/consolidation mode instead of rediscovering the product brief from scratch.
- P5 is skipped if P4 release decision is not `approved`.
- P6 is mandatory and must always run as the final learning stage, even if P5 was skipped.

## Handoff
- Every stage writes:
  - canonical artifact
  - timestamp snapshot
  - handoff summary for next stage
  - stage closure summary for human review
- Handoff must pass schema validation before next stage starts.

## Timeouts and retries
- Use per-stage timeout from params profile.
- On transient failures: retry with bounded attempts.
- On deterministic contract failure: fail fast and emit blocker.

## Resume
- Persist stage state and task state continuously.
- Resume must reload known artifacts and continue from chosen stage only.

## Human gates
- Human gate is mandatory after every terminal stage.
- The root orchestrator must present a concise stage summary, key artifacts, blockers and next-step proposal before any transition.
- The next stage only starts after explicit human approval of the prior stage outcome.
