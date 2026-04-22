> Documento canonico do estado atual: `GUIA_END_TO_END.md` (operacao + arquitetura em runtime)

# Devin Factory V2 Package

Data: 2026-04-22

Este README e intencionalmente curto: setup rapido, comandos e links para os documentos certos.

Este pacote entrega:
- pipeline completa `P0 -> P6` (com `P6` opcional via `runtime.learning.enabled`)
- orquestracao externa (`devin_pipeline_v2.py`)
- runner paralelo (`devin_parallel_runner.py`)
- configuracao unica (`factory_config.json`)
- playbooks canonicos + packages por dominio
- auditoria de aderencia a docs oficiais do Devin

## Estrutura

```text
devin_factory_v2_package/
  README.md
  GUIA_END_TO_END.md
  COORDINATOR_HANDOFF_AND_MEMORY.md
  MASTER_GUIDE.md
  DEVIN_DOCS_CONFORMANCE_AUDIT.md
  factory_config.json
  config_loader.py
  .env.example
  schemas.py
  devin_pipeline_v2.py
  devin_parallel_runner.py
  examples/
    intake_input.example.json
    seed_alpha.json
    seed_beta.json
    parallel_jobs.example.json
  playbooks/
    *.md                      # canonicos
    packages/
      PACKAGES_GUIDE.md       # organizacao por dominio + matriz de agentes
      intake/
      product/
      technology/
      build/
      validation/
      documentation/
      shared/
  schemas/
    *.json
```

## 1) Configuracao unica

Edite `factory_config.json`:
- `devin.*`
- `playbooks.*` (inclui `playbooks.intake` e `playbooks.learning`)
- `arr.*`
- `runtime.*` (inclui `runtime.p0`, `runtime.learning`, `runtime.transport`, `runtime.eval_metrics`, `session_defaults` e `max_wait_seconds.*`)
- `storage.*` (repo corporativo GitHub como raiz de persistencia, incluindo `shared_metrics_root`)
- `git_sync.*` (opcional: add/commit/push automatico)
- `parallel_runner.*`
- `references.*`

Placeholders `${ENV_VAR}` sao suportados.

## 2) Variaveis de ambiente minimas

Use `.env.example` para secrets/IDs usados nos placeholders do config.
Obrigatorio no modo corporativo:
- `FACTORY_GITHUB_REPO_PATH` -> caminho local da clone do repo GitHub operacional.

## 3) Rodar pipelines

### P0 (intake somente)
```bash
python devin_pipeline_v2.py intake ./examples/intake_input.example.json
```

### Full (P0->P6 quando learning estiver habilitado)
```bash
python devin_pipeline_v2.py full ./examples/intake_input.example.json
```

### Etapas individuais
```bash
python devin_pipeline_v2.py brief ./examples/intake_input.example.json factory_runs/alpha
python devin_pipeline_v2.py tech factory_runs/alpha
python devin_pipeline_v2.py build factory_runs/alpha
python devin_pipeline_v2.py validate factory_runs/alpha
python devin_pipeline_v2.py docs factory_runs/alpha
python devin_pipeline_v2.py learn factory_runs/alpha
```

### Resume
```bash
python devin_pipeline_v2.py resume factory_runs/alpha --from build
python devin_pipeline_v2.py resume factory_runs/alpha --from learn
```

## 4) Execucao paralela

```bash
python devin_parallel_runner.py --batch ./examples/parallel_jobs.example.json
```

Defaults de concorrencia/script/logs sao lidos de `factory_config.json`.

## 4.1) Alternar transporte HTTP x MCP

- `runtime.transport.mode=http` usa o fluxo REST atual (`devin.api_base` + `devin.endpoints.*`).
- `runtime.transport.mode=mcp` usa chamadas MCP via `runtime.transport.mcp.*`.
- Campos principais no modo MCP:
  - `runtime.transport.mcp.base_url`
  - `runtime.transport.mcp.tool_call_endpoint`
  - `runtime.transport.mcp.auth_token`
  - `runtime.transport.mcp.tools.*` (aliases para create/get/send/terminate)

## 4.2) Proxy de mensagens no terminal

- O orquestrador agora espelha no terminal as mensagens que chegarem da session Devin.
- Em estado `waiting_for_user` / `waiting_for_approval`, voce pode digitar no terminal e pressionar ENTER para encaminhar a mensagem para o Devin.
- Config em `factory_config.json`:
  - `runtime.terminal_proxy.enabled`
  - `runtime.terminal_proxy.mirror_session_messages`
  - `runtime.terminal_proxy.allow_input_during_wait`
  - `runtime.terminal_proxy.announce_waiting_hint`
  - `runtime.terminal_proxy.prompt_prefix`
  - `runtime.terminal_proxy.max_message_chars`

## 5) Outbox behavior

- Packages oficiais por dominio: `intake`, `product`, `technology`, `build`, `validation`, `documentation`, `shared`.
- Fluxo operacional continua por etapa: `P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6`.
- Runtime usa os playbooks canonicos em `playbooks/*.md`.
- `playbooks/packages/*` e organizacao por dominio para registro/gestao.
- `pipeline_global_orchestrator.md` existe como opcao interna no Devin (modo recomendado continua coordinator externo).
- P0 decide rota automaticamente:
  - `seed_to_brief` -> passa por P1
  - `pre_briefed` -> pula P1 e entra em P2 com briefing normalizado
- Handoff entre orchestrators e automatico via artefatos `p_0..p_6` + bloco `CONTEXT_HANDOFF_AUTOMATICO` no prompt.
- Handoff de workspace agora e persistido em `workspace_handoff.json` (repo_manifest + artefatos + status).
- Tracking automatico por run: `execution_tracking.md`, `dilemmas_and_solutions.md`, `tracking_events.jsonl`.
- Eval metrics deterministicas por run:
  - `eval_metrics.json`
  - `eval_metrics_report.md`
  - `eval_metrics_history.jsonl`
- Metricas de `accuracy/precision/recall/f1` sao calculadas quando `eval_ground_truth.json` existir na run.
- Cobertura de validacao de performance existe em `P4` (ex.: `perf_analyst`, `load_analyst`, `resilience_analyst`, conciliacao via `pr_validator`).
- Analise de custo/FinOps dedicada ainda nao existe como agente canonico no baseline atual.
  - Status atual: lacuna conhecida.
  - Recomendacao: adicionar agente FinOps para custo/eficiencia por run e por pipeline.
- Handoff entre LLMs: `LLM_HANDOFF_LOG.md` (status atual, progresso, proximos passos).
- Memoria separada: `memory/episodic_memory.jsonl` (fatos) e `memory/semantic_memory_candidates.jsonl` (heuristicas).
- Em modo corporativo, memoria/knowledge/skills tambem sao espelhados em:
  - `factory_memory/*.jsonl`
  - `factory_knowledge/*.jsonl`
  - `factory_skills/*.jsonl`
  - `factory_metrics/*.jsonl` (+ `factory_metrics/latest/*.json` quando habilitado)

Persistencia no repo corporativo:
- Se `storage.mode=github_repo`, o `output_dir` default e `<FACTORY_GITHUB_REPO_PATH>/factory_runs/<slug>/`.
- Se `storage.enforce_repo_path=true`, o runtime bloqueia qualquer escrita fora do repo configurado.
- Se `git_sync.enabled=true`, o runtime executa `git add` automatico no output da run.
- Se `git_sync.auto_commit=true`, faz commit.
- Se `git_sync.auto_push=true`, faz push para `git_sync.branch`.

Session payload corporativo:
- `runtime.session_defaults.repos`: lista no formato esperado pela API do Devin.
- `runtime.session_defaults.use_repo_manifest_as_repos`: se `true`, usa o `repo_manifest` do contrato como `repos` em `create_session`.
- Recomendacao: manter `false` ate validar que o formato do `repo_manifest` e 100% compatível com a API.

Checklist rapido:
- `pip install -r requirements.txt`
- preencher `.env` (`DEVIN_API_KEY`, `DEVIN_ORG_ID`, `PLAYBOOK_*`, `ARR_URL`, `FACTORY_GITHUB_REPO_PATH`)
- rodar smoke: `python devin_pipeline_v2.py intake ./examples/intake_input.example.json`

## 6) Onde ver papel de cada agente

- Matriz completa por agente/etapa/pacote:
  - `playbooks/packages/PACKAGES_GUIDE.md`
- Explicacao operacional ponta a ponta:
  - `GUIA_END_TO_END.md`

## 7) Hierarquia da Documentacao

- Estado atual (fonte canonica): `GUIA_END_TO_END.md`
- Operacao rapida: `README.md` (este arquivo)
- Historico de decisoes e racional antigo: `MASTER_GUIDE.md`
- Handoff/memoria/tracking: `COORDINATOR_HANDOFF_AND_MEMORY.md`
- Conformance Devin docs: `DEVIN_DOCS_CONFORMANCE_AUDIT.md`
- Endurecimento corporativo e racional das correcoes: `CORPORATE_HARDENING_EXPLICITO.md`
