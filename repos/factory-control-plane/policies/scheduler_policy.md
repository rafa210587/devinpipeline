# Scheduler Policy (Parallel + Dependencies)

## Core rules
1. Build dependency DAG from `build_plan.modules[*].depends_on`.
2. Validate before dispatch:
   - duplicate module file detection
   - cycle detection
3. Maintain `ready_queue` of modules with all dependencies completed.
4. Dispatch policy:
   - one builder subagent handles one module at a time
   - never batch many modules into one builder context
   - only dispatch from `ready_queue`
5. Concurrency:
   - global max from params profile
   - optional stage-level cap
6. Retry:
   - bounded retries per module
   - classify errors for adaptive retry decisions
7. Completion:
   - mark module complete and unlock dependents
   - persist queue state for resume.

## Quorum integration
- If module is blocked by design ambiguity:
  - create quorum issue
  - collect responses
  - apply judge decision
  - continue scheduling.
