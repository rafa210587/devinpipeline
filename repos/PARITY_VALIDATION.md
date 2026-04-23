# Parity Validation - Python Features Replaced By Agent Repos

Validation scope: legacy capabilities that were previously implemented by Python helpers and are now represented in the agent-first control plane under `repos/`.

Validation method: check each capability is represented by prompt/policy/schema/state file in `repos/` (no runtime dependency on Python files).

## A. Config and Params

- [x] Default config baseline -> `repos/factory-params/params/defaults.json`
- [x] Profile overrides -> `repos/factory-params/params/profiles/*.json`
- [x] Toggle contract validation -> `repos/factory-params/params/toggles.schema.json`
- [x] Config merge order policy -> `repos/factory-params/params/config_resolution_policy.md`
- [x] Env placeholder resolution policy -> `repos/factory-params/params/config_resolution_policy.md`
- [x] Dotenv one-time load policy -> `repos/factory-params/params/config_resolution_policy.md`
- [x] Repo path registry -> `repos/factory-params/params/repos.json`
- [x] Repo fallback registry -> `repos/factory-params/params/repos_fallback.json`
- [x] Local-first repo resolution policy -> `repos/factory-control-plane/policies/repo_resolution_policy.md`
- [x] Transport mode toggle -> `repos/factory-params/params/defaults.json`
- [x] Timeouts per stage -> `repos/factory-params/params/defaults.json`
- [x] Human gate toggles -> `repos/factory-params/params/defaults.json`

## B. Session, Transport, and Polling

- [x] Single-entry full execution prompt -> `repos/factory-control-plane/prompts/master_pipeline_prompt.md`
- [x] HTTP/MCP transport policy -> `repos/factory-control-plane/policies/transport_policy.md`
- [x] Fallback message endpoint policy -> `repos/factory-control-plane/policies/transport_policy.md`
- [x] Waiting state handling policy -> `repos/factory-control-plane/policies/orchestration_policy.md`
- [x] Waiting timeout policy -> `repos/factory-params/params/defaults.json`
- [x] Terminal message mirroring policy -> `repos/factory-control-plane/policies/terminal_proxy_policy.md`
- [x] Human input during waiting policy -> `repos/factory-control-plane/policies/terminal_proxy_policy.md`
- [x] Message truncation policy -> `repos/factory-control-plane/policies/terminal_proxy_policy.md`
- [x] Deduped message stream policy -> `repos/factory-control-plane/policies/terminal_proxy_policy.md`
- [x] Non-interactive terminal fallback -> `repos/factory-control-plane/policies/terminal_proxy_policy.md`

## C. Stage Orchestration (P0..P6)

- [x] Stage DAG P0->P6 -> `repos/factory-control-plane/workflows/pipeline_dag.json`
- [x] P0 route mode handling policy -> `repos/factory-control-plane/policies/orchestration_policy.md`
- [x] Pre-briefed synthetic P1 behavior -> `repos/factory-control-plane/policies/orchestration_policy.md`
- [x] P5 skip when release blocked -> `repos/factory-control-plane/workflows/pipeline_dag.json`
- [x] P6 mandatory final learning stage -> `repos/factory-control-plane/workflows/pipeline_dag.json`
- [x] Stage handoff required before next stage -> `repos/factory-control-plane/policies/orchestration_policy.md`
- [x] Stage output contracts represented -> `repos/factory-contracts/schemas/pipeline/stage_contracts.schema.json`
- [x] Coordinator input envelope -> `repos/factory-contracts/schemas/envelope/coordinator_input.schema.json`
- [x] Coordinator repo fallback support (`repo_fallbacks_file`/`repo_fallbacks`) -> `repos/factory-contracts/schemas/envelope/coordinator_input.schema.json`
- [x] Coordinator output envelope -> `repos/factory-contracts/schemas/envelope/coordinator_output.schema.json`
- [x] Stage status model -> `repos/factory-control-plane/policies/orchestration_policy.md`

## D. Parallelism and Dependencies

- [x] Dependency DAG enforcement -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] Duplicate module detection rule -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] Circular dependency detection rule -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] Ready queue dispatch -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] 1 builder = 1 module dispatch rule -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] Concurrency cap from profile -> `repos/factory-params/params/*.json`
- [x] Retry bounded policy -> `repos/factory-control-plane/policies/scheduler_policy.md`
- [x] Task contract for subagents -> `repos/factory-contracts/schemas/envelope/subagent_task.schema.json`
- [x] Task result contract for subagents -> `repos/factory-contracts/schemas/envelope/subagent_result.schema.json`
- [x] Parallel batch manifest contract -> `repos/factory-control-plane/workflows/parallel_jobs_manifest.schema.json`
- [x] Parallel batch example -> `repos/factory-control-plane/examples/parallel_jobs.example.json`

## E. Quorum and Human Escalation

- [x] Internal quorum-first policy -> `repos/factory-control-plane/policies/quorum_and_escalation_policy.md`
- [x] Quorum issue contract -> `repos/factory-contracts/schemas/envelope/quorum_issue.schema.json`
- [x] Judge decision + confidence contract -> `repos/factory-contracts/schemas/envelope/quorum_issue.schema.json`
- [x] Human escalation last resort policy -> `repos/factory-control-plane/policies/quorum_and_escalation_policy.md`
- [x] Escalation payload contract -> `repos/factory-contracts/schemas/envelope/escalation_request.schema.json`
- [x] Human gate checkpoints after every stage with explicit approval -> `repos/factory-control-plane/policies/orchestration_policy.md`

## F. Persistence, Tracking, Memory, Metrics

- [x] Canonical + snapshot artifact rule -> `repos/factory-control-plane/policies/storage_and_git_policy.md`
- [x] Runtime data root -> `repos/factory-runtime-data/README.md`
- [x] Execution tracking markdown -> `repos/factory-runtime-data/tracking/execution_tracking.md`
- [x] Session ledger file -> `repos/factory-runtime-data/tracking/coordinator_sessions.jsonl`
- [x] Tracking events file -> `repos/factory-runtime-data/tracking/tracking_events.jsonl`
- [x] Dilemmas log file -> `repos/factory-runtime-data/tracking/dilemmas_and_solutions.md`
- [x] Workspace handoff file -> `repos/factory-runtime-data/state/workspace_handoff.json`
- [x] Runtime state checkpoint file -> `repos/factory-runtime-data/state/runtime_state.json`
- [x] Locks directory for concurrency control -> `repos/factory-runtime-data/state/locks/.gitkeep`
- [x] Episodic memory file -> `repos/factory-memory-knowledge/memory/episodic_memory.jsonl`
- [x] Semantic memory file -> `repos/factory-memory-knowledge/memory/semantic_memory_candidates.jsonl`
- [x] Memory summary log -> `repos/factory-memory-knowledge/memory/MEMORY_LOG.md`
- [x] Knowledge candidate file -> `repos/factory-memory-knowledge/knowledge/knowledge_candidates.jsonl`
- [x] Skill events file -> `repos/factory-memory-knowledge/skills/skill_events.jsonl`
- [x] Promotion decisions file -> `repos/factory-memory-knowledge/promotions/promotion_decisions.jsonl`
- [x] Promotion policy (memory/knowledge/skill) -> `repos/factory-control-plane/policies/promotion_policy.md`
- [x] Promotion event contract -> `repos/factory-contracts/schemas/state/promotion_event.schema.json`
- [x] Eval metrics history file -> `repos/factory-runtime-data/metrics/eval_metrics_history.jsonl`
- [x] Eval metrics payload contract -> `repos/factory-contracts/schemas/state/eval_metrics_payload.schema.json`
- [x] Memory record contract -> `repos/factory-contracts/schemas/state/memory_record.schema.json`

## G. Resume, Safety, and Git Sync

- [x] Resume rules by stage -> `repos/factory-control-plane/workflows/resume_map.json`
- [x] Resume-required artifact list -> `repos/factory-control-plane/workflows/resume_map.json`
- [x] Path safety policy -> `repos/factory-control-plane/policies/storage_and_git_policy.md`
- [x] Optional git sync policy -> `repos/factory-control-plane/policies/storage_and_git_policy.md`
- [x] Optional commit/push toggles -> `repos/factory-params/params/defaults.json`
- [x] Single prompt full-pipeline command mode -> `repos/factory-control-plane/prompts/master_pipeline_prompt.md`

## H. Migration Traceability

- [x] Legacy playbooks copied for continuity -> `repos/skills-reference/packages/`
- [x] Legacy JSON schemas copied for migration reference -> `repos/factory-contracts/schemas/deprecated_python_contracts/`

## I. Documentation

- [x] Scheduler and DAG explainer -> `repos/factory-control-plane/docs/SCHEDULER_AND_DAG.md`
- [x] Documentation index -> `repos/factory-control-plane/docs/DOCUMENTATION_INDEX.md`

## Result

All core legacy capabilities are represented in agent-first artifacts under `repos/`.

Note: this validation confirms design-level implementation (prompt/policy/schema/data layout). Runtime execution tests are still required for operational proof.
