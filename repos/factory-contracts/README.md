# Factory Contracts

Versioned schemas for communication and runtime persistence.

## Scope
- Coordinator input/output envelopes.
- Subagent task/result contracts.
- Quorum and escalation contracts.
- Runtime state, handoff, and tracking event schemas.

## Rule
No coordinator may start the next stage before validating the previous stage output against contracts.
