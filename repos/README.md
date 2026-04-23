# Repos Layout For Agent-Only Factory

This folder holds the agent-first replacement for the old Python runtime.

## Repositories

1. `factory-control-plane`
   Single entry prompt, orchestration policy, scheduler policy, quorum and escalation.
2. `factory-contracts`
   Versioned schemas for coordinator/subagent communication and runtime state.
3. `factory-params`
   Runtime toggles, execution profiles, and repo pointers.
4. `architecture-reference`
   Guardrails, patterns, and domain references used by stage agents.
5. `skills-reference`
   Skill packages and selection policy.
6. `refinement-support`
   Intake and briefing support artifacts for initial prompt quality.
7. `factory-memory-knowledge`
   Episodic/semantic memory, knowledge candidates, and promotion logs.
8. `factory-runtime-data`
   Run outputs, tracking, metrics, state checkpoints, and locks.
9. `project-target-repos`
   Actual project code repos (or templates) touched by build/validation/docs.

## Goal

Run the full pipeline from one single prompt while preserving all core capabilities from the old Python orchestrators.
