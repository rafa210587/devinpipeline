# Factory Control Plane

This repo owns orchestration behavior.

## Main files
- `playbooks/packages/shared/pipeline_global_orchestrator.md`: canonical root orchestrator for full P0->P6 execution.
- `prompts/master_pipeline_prompt.md`: bootstrap-only wrapper used to start the root session.
- `policies/orchestration_policy.md`: stage state machine and handoff rules.
- `policies/scheduler_policy.md`: dependency-aware parallel dispatch for P3 module work.
- `policies/quorum_and_escalation_policy.md`: internal debate and last-resort human escalation.
- `workflows/pipeline_dag.json`: stage DAG and required artifacts.
- `workflows/resume_map.json`: resume behavior from each stage.

## High-level guide
- `repos/READMEGeral.md`: project-wide explanation, architecture, flow, and usage guide.
- `GUIA_COMPLETO_DO_PROJETO.md`: root-level complete guide with flow, usage, prompt practices, folder mapping, and repo references.

## Entry contract
- Root coordinator model: `Factory Control-Plane Agent`
- Canonical execution contract: `pipeline_global_orchestrator`
- `master_pipeline_prompt.md` is not the source of truth for pipeline logic

## Contract requirement
All coordinator/subagent messages must validate against schemas in `../factory-contracts`.
