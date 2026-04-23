# Orchestration Policy

## Stage state machine
- Allowed states: `pending`, `running`, `completed`, `failed`, `skipped`, `blocked`.
- Transition rule: a stage can start only if all predecessor stages are terminal and policy allows continuation.

## Stage contracts
- P0 output feeds P1 unless route mode is `pre_briefed`.
- If `pre_briefed`, generate synthetic P1 result and continue to P2.
- P5 is skipped if P4 release decision is not `approved`.
- P6 is optional by toggle.

## Handoff
- Every stage writes:
  - canonical artifact
  - timestamp snapshot
  - handoff summary for next stage
- Handoff must pass schema validation before next stage starts.

## Timeouts and retries
- Use per-stage timeout from params profile.
- On transient failures: retry with bounded attempts.
- On deterministic contract failure: fail fast and emit blocker.

## Resume
- Persist stage state and task state continuously.
- Resume must reload known artifacts and continue from chosen stage only.

## Human gates
- Human gate is optional and policy-driven.
- Gate check points: after P1, after P2, after P4.
