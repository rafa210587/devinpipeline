# Factory Control Plane

This repo owns orchestration behavior.

## Main files
- `playbooks/packages/PACKAGES_GUIDE.md`: package taxonomy and canonical agent matrix.
- `playbooks/packages/shared/pipeline_global_orchestrator.md`: canonical root orchestrator for full P0->P6 execution.
- `repos/factory-control-plane/prompts/master_pipeline_prompt.md`: bootstrap-only wrapper used to start the root session.
- `repos/factory-control-plane/policies/orchestration_policy.md`: stage state machine and handoff rules.
- `repos/factory-control-plane/policies/scheduler_policy.md`: dependency-aware parallel dispatch for P3 module work.
- `repos/factory-control-plane/policies/quorum_and_escalation_policy.md`: internal debate and last-resort human escalation.
- `repos/factory-control-plane/policies/skill_selection_policy.md`: governed skill selection for coordinators and subagents.
- `repos/factory-control-plane/workflows/pipeline_dag.json`: stage DAG and required artifacts.
- `repos/factory-control-plane/workflows/resume_map.json`: resume behavior from each stage.

## High-level guide
- `repos/READMEGeral.md`: project-wide explanation, architecture, flow, and usage guide.
- `GUIA_COMPLETO_DO_PROJETO.md`: root-level complete guide with flow, usage, prompt practices, folder mapping, and repo references.

## Entry contract
- Root coordinator model: `Factory Control-Plane Agent`
- Canonical execution contract: `pipeline_global_orchestrator`
- `master_pipeline_prompt.md` is not the source of truth for pipeline logic

## Contract requirement
All coordinator/subagent messages must validate against schemas in `repos/factory-contracts`.

## Shared context references
All canonical playbooks expose AR, memory, knowledge, and skills references:
- AR primary: `/workspace/architecture-reference/`
- AR fallback repo: `repos/architecture-reference`
- Devin skills: `/workspace/.agents/skills/`
- Factory skill registry: `repos/factory-memory-knowledge/skills/skill_registry.json`
- Factory memory/knowledge: `repos/factory-memory-knowledge/memory` and `repos/factory-memory-knowledge/knowledge`

## Repository binding
Use `repos/factory-params/params/repos.json` for paths that exist inside the Devin session workspace. Use `repos_fallback.json` or Devin repo setup for Git URLs and fallback metadata.
