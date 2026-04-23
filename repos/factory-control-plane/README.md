# Factory Control Plane

This repo owns orchestration behavior.

## Main files
- `prompts/master_pipeline_prompt.md`: one prompt to run full P0->P6.
- Root coordinator model: `Factory Control-Plane Agent` starts the root session and delegates stage work through `pipeline_global_orchestrator`.
- `policies/orchestration_policy.md`: stage state machine and handoff rules.
- `policies/scheduler_policy.md`: dependency-aware parallel dispatch.
- `policies/quorum_and_escalation_policy.md`: internal debate and last-resort human escalation.
- `workflows/pipeline_dag.json`: stage DAG and required artifacts.
- `workflows/resume_map.json`: resume behavior from each stage.

## Contract requirement
All coordinator/subagent messages must validate against schemas in `../factory-contracts`.
