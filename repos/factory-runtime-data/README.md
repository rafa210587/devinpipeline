# Factory Runtime Data

Runtime persistence for runs, tracking, metrics, context ledgers, and resumable state.

## Expected Areas

- `factory_runs/`: run snapshots and legacy-compatible run folders.
- `tracking/`: execution tracking, dilemmas and JSONL events.
- `state/`: runtime state, workspace handoff and locks.
- `metrics/`: eval metrics and latest metric snapshots.
- `context/`: compact context ledgers used to preserve continuity between small child-session tasks.
