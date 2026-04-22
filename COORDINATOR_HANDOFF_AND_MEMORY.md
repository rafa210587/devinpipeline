# Coordinator Handoff, Memory and Tracking

Data: 2026-04-16

## 1) Coordinator geral e orchestrators de pipeline

Este sistema usa dois niveis de coordenacao:

1. Coordinator geral (control plane externo)
- Script: `devin_pipeline_v2.py`
- Responsabilidades:
  - executar a cadeia P0..P5
  - garantir handoff entre etapas
  - persistir artefatos e tracking
  - manter continuidade entre execucoes (inclusive resume)

2. Orchestrator de cada pipeline (dentro do Devin)
- Playbooks `pipeline_*_orchestrator.md`
- Responsabilidades:
  - spawnar child sessions especialistas
  - conduzir debate tecnico/quorum quando necessario
  - aplicar eval independente por etapa
  - retornar structured_output no schema

## 2) Como o contexto passa de um orchestrator para outro

A continuidade entre etapas e automatica e acontece por 3 mecanismos:

1. Artefatos canonicos por etapa
- `p_0_intake.json` ... `p_5_docs.json`
- Cada etapa seguinte usa o output anterior como entrada de verdade.

2. Handoff no prompt
- O coordinator externo injeta `CONTEXT_HANDOFF_AUTOMATICO` no prompt das etapas P1..P5.
- Esse bloco resume status e fatos principais ja produzidos nas etapas anteriores.

2.1 Handoff de workspace versionado
- O coordinator persiste `workspace_handoff.json` por run.
- Esse arquivo registra:
  - repo_manifest (repos target/reference/support)
  - etapa/status mais recente
  - artefatos por etapa (`p_0..p_5`)
- O bloco `CONTEXT_HANDOFF_AUTOMATICO` tambem incorpora esse arquivo.

3. Ledger de sessions
- `coordinator_sessions.jsonl` registra session_id, pipeline, playbook e timestamp.
- Facilita auditoria e continuidade operacional.

## 3) Memoria separada: episodic vs semantic

## 3.1 Episodic Memory

Definicao:
- fatos datados da execucao (o que aconteceu em uma run especifica).

Arquivo:
- `memory/episodic_memory.jsonl`

Exemplos:
- quorum aberto no P3 para desempate arquitetural
- release bloqueada no P4 por finding critico
- etapa pulada por route_mode pre_briefed

## 3.2 Semantic Memory

Definicao:
- regras/heuristicas reutilizaveis extraidas de evidencias recorrentes.

Arquivo:
- `memory/semantic_memory_candidates.jsonl`

Exemplos:
- "quando erro de import repetir no build, executar smoke de dependencia antes de paralelizar"
- "blocker critico de seguranca sempre bloqueia release"

## 3.3 Pipeline de promocao de memoria

1. `memory_builder`
- extrai episodic e semantic candidates de tracking + outputs + dilemas.

2. `memory_evaluator`
- deduplica, valida evidencia, remove ruido.

3. `knowledge_curator`
- converte semantic memory aprovada para knowledge operacional no Devin.

## 4) Tracking da execucao e dilemas

Arquivos gerados automaticamente por run:
- `execution_tracking.md`: timeline por etapa (start/end/status/artifact)
- `dilemmas_and_solutions.md`: dilemas, decisoes e racional
- `tracking_events.jsonl`: eventos estruturados para auditoria/analytics

Com isso, cada execucao fica rastreavel por:
- status de cada etapa
- decisoes tecnicas tomadas
- evidencias que alimentam memoria e knowledge

## 5) Observabilidade, resiliencia e monitoramento na quebra tecnica

A etapa P2 agora incorpora explicitamente:
- `observability_designer`
- `eval_observability_designer`

Resultado:
- `observability_plan` obrigatorio no output P2
  (metricas, logs, traces, dashboards, alertas, runbooks, SLO/SLI)

A etapa P4 pode acionar:
- `observability_validator`

Objetivo:
- validar que o que foi desenhado em P2 realmente foi implementado e esta operacionalmente pronto.

## 6) Persistencia corporativa em repo GitHub (padrao recomendado)

No modo corporativo (`storage.mode=github_repo`), a persistencia ocorre em clone local de repo Git:
- `factory_runs/<slug>/...`
- `factory_memory/*.jsonl`
- `factory_knowledge/*.jsonl`
- `factory_skills/*.jsonl`

`storage.enforce_repo_path=true` impede escrita fora desse repo.

Sugestao de estrutura:
- `runs/<run_id>/execution_tracking.md`
- `runs/<run_id>/dilemmas_and_solutions.md`
- `runs/<run_id>/memory/*.jsonl`
- `index/latest_runs.md`

Opcionalmente, habilite `git_sync` para `add/commit/push` automatico.
