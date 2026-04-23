# Scheduler And Pipeline DAG - Practical Explanation

## Pipeline DAG (stages)
The stage DAG is the fixed dependency chain of the full pipeline:

`P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6`

Rules:
1. A stage only starts when predecessor stage is terminal.
2. `P5` is skipped when `P4.release_decision != approved`.
3. `P6` runs only if learning toggle is enabled.
4. Resume starts from a chosen stage and follows remaining DAG.

Reference:
- `workflows/pipeline_dag.json`
- `workflows/resume_map.json`

## Scheduler (inside P3 build)
The scheduler handles module tasks, not stage transitions.

Inputs:
- `build_plan.modules[*].file`
- `build_plan.modules[*].depends_on`

Flow:
1. Build module DAG from `depends_on`.
2. Validate graph:
   - no duplicate module files
   - no dependency cycles
3. Compute `ready_queue` (modules with all dependencies done).
4. Dispatch ready modules up to `max_concurrency`.
5. Rule: one builder subagent handles one module at a time.
6. On module completion, unlock dependents and refresh queue.
7. Persist queue/state so resume can continue safely.

If ambiguity blocks a module:
1. open quorum issue
2. collect internal responses
3. judge decides
4. continue
5. escalate to human only as last resort

Reference:
- `policies/scheduler_policy.md`
- `policies/quorum_and_escalation_policy.md`
- `schemas/envelope/subagent_task.schema.json`
- `schemas/envelope/subagent_result.schema.json`
