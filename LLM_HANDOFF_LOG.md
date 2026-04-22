# LLM Handoff Log

## 2026-04-21 - Session Start

### Goal
- Evolve the factory to include missing agent roles, stricter eval/evidence flow, and continuous learning promotion.
- Keep docs and commands updated for operational continuity.
- Leave a durable handoff trail for the next LLM if takeover is needed.

### Approved Scope
- Add missing roles: infra/devops builder, test builder, load/chaos validators, architect final validator, promotion manager.
- Add new learning orchestration stage (P6) for memory -> knowledge -> promotion.
- Update orchestrators, schemas, runtime wiring, and operations docs.

### Working Plan
1. Add new playbooks and schemas for missing roles.
2. Update orchestration playbooks and agent matrix.
3. Update runtime (`schemas.py`, `devin_pipeline_v2.py`, config) for P6.
4. Update operational docs (`README.md`, `GUIA_END_TO_END.md`).
5. Keep this log updated with progress and next actions.

### Progress
- Created/updated canonical playbooks for:
  - `devops_infra_builder`, `eval_devops_infra`
  - `test_builder`, `eval_test_builder`
  - `load_analyst`, `chaos_analyst`
  - `architect_final_validator`
  - `promotion_manager`
  - `pipeline_learning_orchestrator`
- Replicated those playbooks into package folders.
- Added new schemas in `schemas/` and wired `schemas.py` with:
  - P3 test evidence requirement
  - P4 architect final validation requirement
  - `P6_OUTPUT_SCHEMA`
- Updated orchestrators:
  - `pipeline_build_orchestrator.md` (infra/test/evals)
  - `pipeline_validation_orchestrator.md` (load/chaos + architect_final_validator)
  - `pipeline_global_orchestrator.md` (P0..P6 with learning chain)
- Runtime wiring in `devin_pipeline_v2.py`:
  - added runtime flags for learning (`LEARNING_ENABLED`, timeout)
  - added `build_p6_prompt(...)`
  - added `run_p6(...)` with tracking/memory/handoff/persist to `p_6_learning.json`
  - `run_full(...)` now executes P6 when `runtime.learning.enabled=true`
  - `run_resume(...)` now supports `--from learn`
  - CLI now accepts `learn` pipeline and `resume --from learn`
  - handoff context now includes summaries for P5 and P6
- Config updates:
  - `config_loader.py` defaults now include `playbooks.learning`, `runtime.learning`, and `max_wait_seconds.learning`
  - `factory_config.json` now includes `playbooks.learning`, `runtime.learning`, and `max_wait_seconds.learning`
  - `.env.example` now includes `PLAYBOOK_LEARNING_ORCHESTRATOR`
- Docs updates:
  - `README.md` updated to include P6/learn commands and handoff log convention
  - `GUIA_END_TO_END.md` updated for P0..P6 flow, new agents, new schemas, learning runtime and troubleshooting

## 2026-04-21 - Current Status (Takeover)

### Completed
- Core feature objective is implemented: P6 exists end-to-end and is connected to full/resume/direct execution.
- Documentation and config were brought to operational parity with the new flow.
- Local validations executed:
  - `factory_config.json` parse OK
  - `config_loader.load_factory_config(...)` confirms `playbooks.learning` and `runtime.learning`
  - Python syntax check via `ast.parse` on key scripts returned `AST_OK`

### Pending Validation
1. Optional smoke checks:
   - `python devin_pipeline_v2.py --help`
   - `python devin_pipeline_v2.py learn <output_dir_existente>`
2. Optional doc polish:
   - review any remaining references to `P0..P5` in long-form docs.

### Notes for Next LLM
- This workspace directory is not a git repository (`git status` fails here), so use direct file inspection for change audit.
- `rg` was unavailable in this environment; fallback used: `Get-ChildItem` + `Select-String`.
- `python -m py_compile` failed here due write lock/permission on `__pycache__`; syntax was validated with `ast.parse` fallback (`AST_OK`).
- `python devin_pipeline_v2.py --help` is blocked until `aiohttp` is installed (`requirements.txt`).

## 2026-04-21 - Presentation Update For Boss (Manus.ai)

### Goal
- Recover prior presentation context and make the Manus prompt safe and current for executive use.

### Changes Made
- Updated [MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md](/C:/Users/Rafa/OneDrive/Documentos/Projetos/Agents_Coder/agent-farm/projeto/devin_factory_v2_package/MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md):
  - migrated factual baseline from `P0..P5` to `P0..P6` (with `P6` optional by config)
  - updated counts: `54` total playbooks, `7` stage orchestrators, `1` global optional, `46` specialists
  - updated framing from `6 etapas + 5 pipelines` to `7 etapas + 6 frentes apos intake`
  - updated stage distribution (`P3=11`, `P4=14`, `P6=6`)
  - added missing roles to matrix (`devops_infra_builder`, `test_builder`, `eval_test_builder`, `eval_devops_infra`, `load_analyst`, `chaos_analyst`, `architect_final_validator`, `promotion_manager`, `pipeline_learning_orchestrator`)
  - updated flow and slide narrative to include `P6`
  - fixed reference links to current absolute workspace path
- Updated [RESUMO_EXECUTIVO_SISTEMA_DEVIN.md](/C:/Users/Rafa/OneDrive/Documentos/Projetos/Agents_Coder/agent-farm/projeto/devin_factory_v2_package/RESUMO_EXECUTIVO_SISTEMA_DEVIN.md):
  - refreshed date and aligned with `P0..P6`, current counts, and `p_0...p_6` artifacts.

### Validation
- Ran pattern checks to confirm old baseline terms no longer remain in these two files:
  - no `P0..P5`, `45 agentes`, `5 pipelines centrais` leftovers.

## 2026-04-21 - Presentation Contextualization Addendum

### Request
- Add an executive contextualization chapter for the boss-focused presentation:
  - current state: assisted AI + simple agents
  - target state: fully orchestrated multi-agent pipeline
  - explicit gains from this transition

### Updates Applied
- Updated [MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md](/C:/Users/Rafa/OneDrive/Documentos/Projetos/Agents_Coder/agent-farm/projeto/devin_factory_v2_package/MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md):
  - added mandatory contextualization chapter (AS-IS -> GAP -> TO-BE)
  - reinforced current-maturity framing with non-critical tone toward current team practices
  - added dedicated transition-gains section
  - updated slide narrative to include contextualization at the beginning
  - kept slide plan within 14-16 range (final structure now up to 16 slides)

## 2026-04-21 - Analysis: Devin CLI vs Endpoint + Eval Metrics

### Request
- Validate whether the current factory runtime can use a Devin CLI instead of the HTTP endpoint.
- Read current official Devin docs before proposing any plan.
- Assess how agent evaluation is currently modeled and whether classic metrics like accuracy / precision / recall / F1 already exist.

### Findings
- Current runtime is endpoint-first only:
  - `devin_pipeline_v2.py` imports `aiohttp` and centralizes `API_BASE`, `CREATE_SESSION_ENDPOINT`, `GET_SESSION_ENDPOINT`, `SEND_MESSAGE_ENDPOINT_CANDIDATES`, and `TERMINATE_SESSION_ENDPOINT`.
  - Session lifecycle is implemented through `create_session(...)`, `get_session(...)`, `send_message(...)`, `terminate_session(...)`, and `poll_until_done(...)`.
  - `factory_config.json` only models REST API connectivity under `devin.api_base` and `devin.endpoints.*`.
- No local support was found for:
  - a configurable Devin CLI binary
  - CLI-oriented auth/config
  - MCP transport/runtime path
  - backend abstraction such as `execution_backend=api|cli|mcp`
- Official docs reviewed:
  - API Overview
  - Create Session
  - Advanced Capabilities
  - Devin MCP
  - Enterprise Deployment
  - Devin Review
  - Session Insights
  - Enterprise Session Metrics
- Important doc conclusion:
  - official public docs clearly support `web`, `Slack`, and `API` as session entry points
  - official public docs clearly support `Devin MCP` for programmatic session/playbook/knowledge/schedule management
  - official public docs clearly document a CLI only for `Devin Review` (`npx devin-review ...`)
  - docs do not publicly document a general-purpose Devin session CLI equivalent to the REST session lifecycle used by this package
  - metrics docs mention internal origins `cli`, `vscode_extension`, `devin_spaces`, but those origins are not exposed in the public API response model

### Recommendation
- Do not treat a generic "Devin CLI backend" as an officially documented production control plane yet.
- If corporate constraints make direct REST integration difficult, the safest officially documented alternative is to add an optional `MCP` backend before or alongside any experimental CLI adapter.
- If a CLI adapter is still desired, design it as an experimental pluggable backend with strict capability checks and telemetry, not as the default path.

### Eval Status
- The project already has strong qualitative/operational eval gates:
  - independent evaluator agents are required in key debates and QA reviews
  - `eval_pm` uses `specificity_score` and `actionability_score`
  - QA evals use `overall_quality_score` and `false_positives_suspected`
  - architect final validation uses `architecture_alignment_score`
  - final judge uses a global `score` plus `scores_by_dimension`
- However, no classical classification metrics were found locally:
  - `accuracy`: 0 matches
  - `precision`: 0 matches
  - `recall`: 0 matches
  - `f1`: 0 matches
- Conclusion:
  - current eval is governance-focused and rubric-based
  - it is not yet benchmarked as a statistical evaluation framework with labeled ground truth and confusion-matrix metrics

### Next-Step Plan Candidate
- If approved later, the implementation plan should be:
  1. Introduce backend abstraction (`api`, `mcp`, optional `cli_experimental`).
  2. Keep current API backend as baseline/fallback.
  3. Add MCP backend first for officially supported alternative transport and gather semantics.
  4. Add experimental CLI adapter only behind config/feature flag, after deciding which CLI is trusted and how its outputs map to factory contracts.
  5. Add eval telemetry layer with ground-truth datasets and per-agent/per-playbook metrics (`precision`, `recall`, `F1`, false-positive rate, false-negative rate, calibration).

## 2026-04-22 - Implemented: Eval Metrics + Transport Toggle HTTP/MCP

### Request
- Add eval metrics persistence to the project/repo for later analysis.
- Add runtime config toggle to switch transport between current HTTP mode and MCP mode.
- Validate implementation.

### Changes Implemented

#### 1) Config model expanded
- Updated `config_loader.py` defaults:
  - `runtime.transport.mode` (`http|mcp`)
  - `runtime.transport.mcp.*` (base_url, endpoint, auth_token, tools aliases, payload_mode, timeout)
  - `runtime.eval_metrics.*` (enabled, deterministic mode, report files, history jsonl, ground-truth file, shared promotion flag)
  - `storage.shared_metrics_root`
- Updated `factory_config.json`:
  - added `runtime.transport` and `runtime.eval_metrics`
  - added `storage.shared_metrics_root`
- Updated `.env.example`:
  - `DEVIN_MCP_BASE_URL`
  - `DEVIN_MCP_TOOL_CALL_ENDPOINT`
  - `DEVIN_MCP_AUTH_TOKEN`
- Updated `README.md` with:
  - transport toggle docs (`http` vs `mcp`)
  - eval metrics artifacts and shared replication behavior

#### 2) Runtime transport backend toggle
- `devin_pipeline_v2.py` now reads:
  - `TRANSPORT_MODE`
  - MCP config bundle
- Added MCP tool-call implementation:
  - `_mcp_call_tool(...)`
  - `create_session_mcp(...)`
  - `get_session_mcp(...)`
  - `send_message_mcp(...)`
  - `terminate_session_mcp(...)`
- Added transport wrappers:
  - `create_session_transport(...)`
  - `get_session_transport(...)`
  - `send_message_transport(...)`
  - `terminate_session_transport(...)`
- Pipeline stages (`P0..P6`) now use `create_session_transport(...)` instead of fixed HTTP create call.
- Polling now uses transport wrappers (`get_session_transport` / `terminate_session_transport`) so `http|mcp` works across lifecycle.
- Session ledger now records `transport_mode`.
- `validate_config(...)` now validates required fields based on selected transport mode.

#### 3) Deterministic eval metrics pipeline
- Added deterministic metrics/report generation in `devin_pipeline_v2.py`:
  - quality score extraction from stage artifacts
  - stage completion rate and release decision summary
  - optional binary classification metrics (`accuracy`, `precision`, `recall`, `f1`) from `eval_ground_truth.json`
  - output artifacts:
    - `eval_metrics.json`
    - `eval_metrics_report.md`
    - `eval_metrics_history.jsonl`
  - optional shared promotion:
    - `factory_metrics/eval_metrics_history.jsonl`
    - `factory_metrics/latest/<slug>.json`
- Added trigger integration in CLI flow:
  - after `full`
  - after `resume`
  - after individual stage commands (`intake`, `brief`, `tech`, `build`, `validate`, `docs`, `learn`)

### Validation Performed
- Syntax/config:
  - `AST_OK: devin_pipeline_v2.py`
  - `AST_OK: config_loader.py`
  - `JSON_OK: factory_config.json`
  - `load_factory_config(...)` confirms:
    - `TRANSPORT_MODE=http`
    - `EVAL_ENABLED=True`
    - `SHARED_METRICS_ROOT=factory_metrics`
- Runtime help:
  - `python devin_pipeline_v2.py --help` working after installing deps.
- Deterministic eval metrics:
  - Executed `maybe_generate_eval_metrics(...)` on synthetic artifacts.
  - Confirmed creation of:
    - `eval_metrics.json`
    - `eval_metrics_report.md`
    - `eval_metrics_history.jsonl`
  - Confirmed `accuracy/precision/recall/f1=0.5` with synthetic `eval_ground_truth.json` sample.
- Transport toggle:
  - Generated temporary config with `runtime.transport.mode=mcp`.
  - Executed `intake`; runtime entered MCP path and failed at MCP host resolution (`mcp.invalid`) as expected.
  - This verifies toggle routing is active and not falling back silently to HTTP.

### Notes / Caveats
- MCP execution depends on reachable MCP endpoint and compatible tool-call contract (`tool_gateway` or JSON-RPC style response).
- Full end-to-end MCP run against real Devin MCP server still depends on corporate network/access setup.

## Update 2026-04-22 (Follow-up validation)

- Revalidated runtime and config loading after feature delivery:
  - `python devin_pipeline_v2.py --help` OK
  - `load_factory_config('factory_config.json')` returns:
    - `runtime.transport.mode = http`
    - `runtime.eval_metrics.enabled = true`
    - `storage.shared_metrics_root = factory_metrics`
- Confirmed code references for:
  - transport switch (`http|mcp`)
  - deterministic eval metrics generation and persistence
  - docs and env examples updated.
- Restored tracked temporary validation files (`_tmp_eval_metrics/*`, `_tmp_factory_config_mcp.json`) to avoid accidental deletions in git history.
- Workspace still has untracked `__pycache__/*.pyc` files locked by filesystem/OneDrive; these do not impact runtime.

## Update 2026-04-22 (Presentation prompt refinement)

- Reviewed `MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md` for redundancy and structure clarity.
- Added mandatory redundancy-control instructions so final deck consolidates repeated themes instead of duplicating slides.
- Added a new mandatory section for agent grouping by profile (in addition to stage grouping):
  - Engenharia
  - Qualidade
  - DevOps e Operacoes
  - Seguranca
  - Refiner
  - Governanca e Orquestracao
  - Memoria e Conhecimento
  - FinOps (explicitly marked as current gap / roadmap)
- Updated suggested 16-slide narrative to include a dedicated profile-grouping slide and kept total slide count within requested range.
- Updated “Peca especial” checklist to explicitly require profile grouping slide.

## Update 2026-04-22 (Performance vs Cost/FinOps coverage clarification)

- Confirmed performance evaluation is already implemented and documented in P4 (dynamic test planner + perf/load/resilience validators + pr_validator).
- Confirmed no dedicated canonical FinOps agent exists in baseline.
- Updated docs to make this explicit and avoid ambiguity:
  - README: added explicit note that FinOps/cost analysis is a known gap and recommendation.
  - GUIA_END_TO_END: added section "Cobertura de performance e custo (estado atual)".
  - PACKAGES_GUIDE: added FinOps coverage note under agent matrix.
- Presentation prompt already marks FinOps as gap; kept alignment with docs.

## Update 2026-04-22 (Presentation refinement: performance vs cost)

- Updated `MANUS_PRESENTATION_PROMPT_DEVIN_FACTORY.md` to explicitly separate:
  - what is already operational (performance/risk-based validation in P4)
  - what is still roadmap (dedicated FinOps/cost agent)
- Added required guidance to avoid overclaiming FinOps maturity.
- Added KPI suggestions for performance and execution cost (p95/p99, cost per run, cost per stage, runs above budget).
- Updated narrative slides to include executive scorecard and explicit risk/gap messaging for FinOps.
- Added mandatory special slide: "performance e custo: estado atual vs gap FinOps".
