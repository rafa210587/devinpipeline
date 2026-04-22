# Guia End-to-End do Sistema Devin Factory V2

Data: 2026-04-22
Escopo: explicar o sistema de ponta a ponta, o papel de cada arquivo e como operar no dia a dia.

Contrato deste documento:
- este e o documento canonico do estado atual do pacote.
- fluxo oficial atual: 7 etapas operacionais (`P0..P6`), com `P6` opcional por config.

---

## 1) O que e este sistema

Este pacote implementa uma Software Factory orientada a agentes no Devin.
A ideia central e:
- pegar um seed de produto
- refinar em briefing
- quebrar tecnicamente
- construir em paralelo
- validar com gates de qualidade
- documentar

Tudo com orquestracao por sessions no Devin (parent coordinator + child sessions).

Resumo rapido:
- Fluxo oficial atual: P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6 (P6 opcional por config)
- P1 pode ser pulado quando P0 decidir route_mode=pre_briefed
- Governanca: evaluator por etapa + homologacao QA + judge final
- Escala: suporte a run unica e multiplos projetos em paralelo

---

## 2) Visao de arquitetura

## 2.1 Camadas

1. Camada de orquestracao externa (host)
- `devin_pipeline_v2.py`: dispara cada pipeline, faz polling, persiste artefatos.
- `devin_parallel_runner.py`: executa varias pipelines em paralelo (multi-projeto).

2. Camada de orquestracao dentro do Devin
- `playbooks/pipeline_*_orchestrator.md`: coordenadores P0..P6.
- Cada pipeline orchestrator spawna child sessions especialistas.

3. Camada de execucao especializada
- playbooks de workers e evaluators (`builder`, `code_reviewer`, `security`, etc).

4. Camada de contratos
- `schemas.py` + `schemas/*.json`: contratos de structured output.

5. Camada de configuracao e entrada
- `factory_config.json`: configuracao unica da factory.
- `config_loader.py`: loader compartilhado com suporte a `${ENV_VAR}`.
- `.env.example`: placeholders minimos para secrets/IDs.
- `examples/*.json`: seeds e batch de execucao paralela.

## 2.2 Modelo de packages (decisao)

A organizacao oficial de agentes foi definida por **dominio funcional**:
- intake
- product
- technology
- build
- validation
- documentation
- shared

Por que esta forma e melhor que agrupar apenas por P0/P1/P2:
- preserva estabilidade da taxonomia quando o fluxo muda;
- melhora ownership por time (produto/tech/qa/docs);
- evita duplicacao de agentes transversais.

Importante:
- o empacotamento e por dominio;
- a operacao continua por etapa P0..P6.

## 2.3 Out-of-box (como funciona na pratica)

Modo oficial:
- runtime executa playbooks canonicos em `playbooks/*.md`;
- `playbooks/packages/*` e camada de organizacao e governanca;
- IDs dos orchestrators ficam centralizados em `factory_config.json`.

Checklist minimo de primeiro run:
1. `pip install -r requirements.txt`
2. preencher `.env` com `DEVIN_API_KEY`, `DEVIN_ORG_ID`, `PLAYBOOK_*`, `ARR_URL`, `FACTORY_GITHUB_REPO_PATH`
3. executar smoke test:
   - `python devin_pipeline_v2.py intake ./examples/intake_input.example.json`
4. se smoke passar, executar full:
   - `python devin_pipeline_v2.py full ./examples/intake_input.example.json`

---

## 3) Estrutura de arquivos e papel de cada item

## 3.1 Raiz do pacote

- `.env.example`
  - template de placeholders de ambiente consumidos pelo `factory_config.json`.

- `factory_config.json`
  - source of truth unica para endpoints, playbooks, runtime e paralelismo.

- `config_loader.py`
  - carrega `factory_config.json` com merge de defaults + placeholders `${ENV_VAR}`.

- `requirements.txt`
  - dependencia minima local para os scripts Python (`aiohttp`).

- `schemas.py`
  - definicoes Python dos schemas de entrada/saida.

- `devin_pipeline_v2.py`
  - runner principal de uma pipeline (full, etapa unica, ou resume).
  - validacao de env por pipeline.
  - enforce de storage corporativo quando configurado.
  - ledger local de sessions (`coordinator_sessions.jsonl` no output).

- `devin_parallel_runner.py`
  - executa varios jobs em paralelo.
  - cada job chama `devin_pipeline_v2.py` com parametros proprios.
  - grava logs separados por job.

- `README.md`
  - operacao rapida (setup e comandos principais).

- `MASTER_GUIDE.md`
  - historico de decisoes e racional de design (nao e contrato operacional atual).

- `GUIA_END_TO_END.md` (este arquivo)
  - explicacao operacional e estrutural ponta a ponta.

- `COORDINATOR_HANDOFF_AND_MEMORY.md`
  - detalhes de handoff entre orchestrators, memoria episodica/semantica e tracking.

- `LLM_HANDOFF_LOG.md`
  - log operacional continuo para troca de contexto entre LLMs durante a implementacao.

## 3.2 Pasta `examples/`

- `intake_input.example.json`
  - exemplo completo para P0 (prompt + repos + constraints).

- `seed_alpha.json`
  - seed exemplo para testar run unica.

- `seed_beta.json`
  - seed exemplo para validar execucao paralela.

- `parallel_jobs.example.json`
  - template de jobs para `devin_parallel_runner.py`.

## 3.3 Pasta `schemas/`

JSON schemas usados pelos orchestrators/workers para structured output.
Agrupamento pratico:

P0 (intake):
- `intake_output_schema.json`
- `prompt_normalizer_schema.json`
- `eval_prompt_normalizer_schema.json`

P1 (produto):
- `briefing_schema.json`
- `critique_schema.json`
- `eval_critique_schema.json`
- `moderator_verdict_schema.json`
- `eval_moderator_schema.json`

P2 (tech):
- `modules_schema.json`
- `eval_modules_schema.json`
- `build_plan_schema.json`
- `eval_build_plan_schema.json`
- `integration_map_schema.json`
- `contract_schema.json`
- `observability_plan_schema.json`
- `eval_observability_plan_schema.json`

P3 (build):
- `builder_output_schema.json`
- `code_review_schema.json`
- `builder_qa_schema.json`
- `devops_infra_builder_schema.json`
- `eval_devops_infra_schema.json`
- `test_builder_schema.json`
- `eval_test_builder_schema.json`
- `quorum_response_schema.json`
- `judge_quorum_schema.json`

P4 (validation):
- `perf_findings_schema.json`
- `resilience_findings_schema.json`
- `pr_validator_schema.json`
- `integration_findings_schema.json`
- `security_findings_schema.json`
- `load_findings_schema.json`
- `chaos_findings_schema.json`
- `architect_final_validation_schema.json`
- `eval_qa_schema.json`
- `qa_consolidator_schema.json`
- `judge_final_schema.json`

P5 (docs):
- `doc_writer_schema.json`
- `eval_docs_schema.json`

P6 (learning):
- `learning_output_schema.json`
- `promotion_manager_schema.json`

Shared memory/knowledge:
- `memory_builder_schema.json`
- `memory_evaluator_schema.json`
- `knowledge_curator_schema.json`

## 3.4 Pasta `playbooks/`

### Orchestrators (controlam pipeline)
- `pipeline_global_orchestrator.md` (opcional, cadeia P0->P6 interna no Devin)
- `pipeline_intake_orchestrator.md` (P0)
- `pipeline_brief_orchestrator.md` (P1)
- `pipeline_tech_orchestrator.md` (P2)
- `pipeline_build_orchestrator.md` (P3)
- `pipeline_validation_orchestrator.md` (P4)
- `pipeline_docs_orchestrator.md` (P5)
- `pipeline_learning_orchestrator.md` (P6)

### Pipe 0 - Intake
- `prompt_normalizer.md`
- `eval_prompt_normalizer.md`

### Pipe A - Produto
- `draft_writer.md`
- `pm_profile_designer.md`
- `pm_base.md`
- `eval_pm.md`
- `moderator.md`
- `eval_moderator.md`

### Pipe B - Quebra tecnica
- `technical_analyst.md`
- `eval_tech_analyst.md`
- `architect.md`
- `eval_architect.md`
- `integration_mapper_llm.md`
- `contract_refiner.md`
- `observability_designer.md`
- `eval_observability_designer.md`

### Pipe C - Execucao
- `builder.md`
- `code_reviewer.md`
- `builder_qa.md`
- `devops_infra_builder.md`
- `eval_devops_infra.md`
- `test_builder.md`
- `eval_test_builder.md`
- `judge_quorum.md`

### Pipe D - Validacao
- `dynamic_test_planner.md` (novo V2)
- `perf_analyst.md`
- `resilience_analyst.md`
- `load_analyst.md`
- `chaos_analyst.md`
- `integration_validator.md`
- `security.md`
- `observability_validator.md`
- `pr_validator.md`
- `eval_qa_template.md`
- `qa_consolidator.md`
- `architect_final_validator.md`
- `judge_final.md`

### Skills e contexto (novo V2)
- `pipeline_global_orchestrator.md` (opcional)
- `skill_builder.md`
- `skill_evaluator.md`
- `context_ledger_updater.md`
- `memory_builder.md`
- `memory_evaluator.md`
- `knowledge_curator.md`
- `promotion_manager.md`

### Pipe E - Documentacao
- `doc_writer.md`
- `eval_docs.md`

### Packages por dominio
- `playbooks/packages/PACKAGES_GUIDE.md`
- `playbooks/packages/<dominio>/...` (copias organizacionais por dominio)
- Runtime usa os arquivos canonicos em `playbooks/*.md`.

---

## 4) Fluxo de ponta a ponta (run unica)

## 4.1 Preparacao

1. Registrar playbooks no Devin
- publicar os playbooks canonicos de `playbooks/*.md` (nao publicar `playbooks/packages/*`).
- coletar os IDs dos 7 orchestrators (P0..P6).

Opcional para organizacao:
- usar `playbooks/packages/PACKAGES_GUIDE.md` para registrar por dominio
  (intake/product/technology/build/validation/documentation/shared).

2. Configurar ambiente
- copiar `.env.example` para `.env` (se usar placeholders `${ENV_VAR}` no config).
- preencher `factory_config.json` (ou manter defaults) e definir IDs/secrets via env.
- no modo corporativo, definir obrigatoriamente:
  - `FACTORY_GITHUB_REPO_PATH` (clone local do repo operacional).

3. Instalar dependencia local
- `pip install -r requirements.txt`

## 4.2 Executar pipeline completa

Comando recomendado (modo corporativo, sem `output_dir` explicito):
```bash
python devin_pipeline_v2.py full ./examples/intake_input.example.json
```

Comando alternativo (com `output_dir` explicito):
```bash
python devin_pipeline_v2.py full ./examples/intake_input.example.json factory_runs/alpha
```

Regra de resolucao de output:
- se `storage.mode=github_repo`, o default vira:
  - `<FACTORY_GITHUB_REPO_PATH>/factory_runs/<slug>/`
- se `storage.enforce_repo_path=true`, escrita fora do repo e bloqueada.

O script executa em ordem:
- P0: intake/prompt optimization
- P1: brief/refinement (quando route_mode=seed_to_brief)
- P2: technical decomposition
- P3: build
- P4: validation/testing
- P5: documentation
- P6: learning/promotion (quando `runtime.learning.enabled=true`)

## 4.3 Artefatos gerados

No output do projeto:
- `p_0_intake.json`
- `p_1_brief.json`
- `p_2_tech.json`
- `p_3_build.json`
- `p_4_validation.json`
- `p_5_docs.json`
- `p_6_learning.json` (quando learning habilitado ou pipeline `learn`)
- snapshots timestamped
- `coordinator_sessions.jsonl` (ledger de sessions parent)
- `execution_tracking.md` (status de cada etapa da execucao)
- `dilemmas_and_solutions.md` (registro de dilemas e decisoes)
- `tracking_events.jsonl` (eventos estruturados de tracking)
- `workspace_handoff.json` (handoff de repos/artifacts entre etapas)
- `memory/episodic_memory.jsonl` (memoria episodica)
- `memory/semantic_memory_candidates.jsonl` (candidatos a memoria semantica)
- `memory/MEMORY_LOG.md` (resumo consolidado de memoria)

No repo corporativo (consolidado cross-run):
- `factory_memory/episodic_memory.jsonl`
- `factory_memory/semantic_memory_candidates.jsonl`
- `factory_knowledge/knowledge_candidates.jsonl`
- `factory_skills/skill_events.jsonl` (quando houver skill events)

## 4.4 Gates humanos opcionais

Ative em `factory_config.json`:
- `runtime.human_gates.after_p1=true`
- `runtime.human_gates.after_p2=true`
- `runtime.human_gates.after_p4=true`

Quando gate dispara:
- script salva `GATE_<nome>.json`
- aguarda `APPROVE_<nome>` ou `REJECT_<nome>`

## 4.5 Proxy terminal (mensagens e resposta humana)

- O `devin_pipeline_v2.py` espelha no terminal as mensagens novas da session Devin.
- Se a session entrar em `waiting_for_user` ou `waiting_for_approval`, voce pode responder direto no terminal:
  - digite a mensagem e pressione ENTER
  - a linha e encaminhada ao Devin via `send_message`
- Ajustes em `factory_config.json`:
  - `runtime.terminal_proxy.enabled`
  - `runtime.terminal_proxy.mirror_session_messages`
  - `runtime.terminal_proxy.allow_input_during_wait`
  - `runtime.terminal_proxy.announce_waiting_hint`
  - `runtime.terminal_proxy.prompt_prefix`
  - `runtime.terminal_proxy.max_message_chars`

## 4.6 Como um orchestrator sabe o que o anterior fez

A continuidade acontece por 3 mecanismos combinados:

1. Artefatos de etapa no output
- cada etapa persiste `p_0...p_6` em JSON.
- a etapa seguinte recebe esses artefatos como entrada canonicamente.

2. Handoff automatico no prompt
- o `devin_pipeline_v2.py` injeta bloco `CONTEXT_HANDOFF_AUTOMATICO` no prompt da etapa seguinte.
- esse bloco resume status e fatos principais de P0..Pn ja executados.

3. Memoria operacional
- eventos factuais vao para `memory/episodic_memory.jsonl`.
- heuristicas candidatas vao para `memory/semantic_memory_candidates.jsonl`.
- esse contexto pode ser consumido por agents de memoria/knowledge para evolucao continua.

4. Handoff de workspace
- `workspace_handoff.json` guarda:
  - `repo_manifest`
  - etapa/status mais recente
  - mapa de artefatos por etapa
- esse handoff alimenta o contexto das etapas seguintes.

---

## 5) Fluxo por pipeline (o que entra e sai)

## P0 - Intake & Prompt Optimization

Entrada:
- input bruto (seed ou briefing pronto)
- repo_manifest (reference/target/support)

Processo:
- prompt_normalizer -> eval_prompt_normalizer
- quorum (quando houver duvida relevante)
- route_mode: seed_to_brief ou pre_briefed

Saida chave:
- intake_contract
- normalized_prompt
- project_context
- route_mode

## P1 - Product Brief & Refinement

Entrada:
- seed

Processo:
- draft -> PMs em paralelo -> eval de cada critica -> moderator -> eval moderator

Saida chave:
- briefing refinado
- ready_for_factory

## P2 - Technical Decomposition

Entrada:
- briefing P1

Processo:
- technical_analyst -> eval -> architect -> eval -> integration map -> contracts

Saida chave:
- tasks_md
- build_plan
- integration_map
- contracts
- observability_plan

## P3 - Build

Entrada:
- outputs P2

Processo:
- complexity routing
- pilot build
- parallel build por batches
- deterministic checks + code review + builder QA
- quorum quando bloqueio real
- captura de skill candidates

Saida chave:
- per_file_verdicts
- failed_files
- quorums_logged
- estatisticas de erro/tentativa

## P4 - Validation

Entrada:
- outputs P3 + briefing/build context

Processo:
- Dynamic Test Planner (decide validacoes por risco)
- validadores selecionados em paralelo
- eval de QAs executados
- QA Consolidator (homologacao)
- Judge Final (GO/NO-GO)

Saida chave:
- findings consolidados
- qa_consolidator
- judge_verdict
- release_decision

## P5 - Documentation

Entrada:
- release homologada

Processo:
- doc_writer -> eval_docs

Saida chave:
- docs e status final de pipeline

## P6 - Learning & Promotion

Entrada:
- contexto consolidado de P0..P5 + memoria da run

Processo:
- context_ledger_updater -> memory_builder -> memory_evaluator -> knowledge_curator -> promotion_manager

Saida chave:
- ledger_patch
- memory_summary
- knowledge_summary
- promotion_summary (project/global/rejections)

---

## 5.1 Politica de quorum e eval independente (obrigatoria)

Regra global:
- Sempre que houver duvida relevante de definicao ou conflito entre agentes, abrir quorum.
- Quorum minimo: 3 agentes de papeis diferentes.
- Toda decisao de quorum gera `quorum_record`.
- Todo debate tecnico deve ser auditado por eval independente (agente que nao participou do debate).
- Limite: 2 rounds de debate+eval. Se continuar reprovado, abortar etapa com `reason="quorum_eval_failed"`.

Quando abrir quorum:
- requisito ambiguo com impacto tecnico
- tradeoff sem consenso (custo, risco, prazo, arquitetura)
- conflito de findings entre validadores
- bloqueio recorrente do builder/reviewer/qa

## 5.2 Cadeia de papeis sem redundancia

P0 (Intake):
- Executor: prompt_normalizer
- Evaluator: eval_prompt_normalizer
- Decisao/quorum: pipeline_intake_orchestrator + quorum ad hoc
- Nao faz: refinamento profundo de produto nem decomposicao tecnica

P1 (Brief/Refinamento):
- Executor: draft_writer, PMs
- Evaluator: eval_pm, eval_moderator
- Decisao/quorum: moderator + quorum ad hoc
- Nao faz: implementacao de codigo

P2 (Quebra tecnica):
- Executor: technical_analyst, architect, contract_refiner, observability_designer
- Evaluator: eval_tech_analyst, eval_architect
- Evaluator adicional: eval_observability_designer
- Decisao/quorum: architect + builder lead + qa lead
- Nao faz: coding da solucao final

P3 (Execucao):
- Executor: builder
- Evaluator: code_reviewer, builder_qa
- Decisao/quorum: architect/judge_quorum (quando conflito)
- Nao faz: homologacao final de release

P4 (Validacao):
- Executor: validadores (perf/resilience/security/integration/observability)
- Evaluator: eval_qa_template
- Homologacao: qa_consolidator
- Decisao final: judge_final
- Nao faz: reimplementar codigo

P5 (Documentacao):
- Executor: doc_writer
- Evaluator: eval_docs
- Nao faz: redefinicao de arquitetura/codigo

P6 (Learning):
- Executor: context_ledger_updater, memory_builder, knowledge_curator, promotion_manager
- Evaluator: memory_evaluator
- Decisao/quorum: promotion_manager aplica criterios de promote/reject
- Nao faz: alterar codigo de produto diretamente

## 5.3 Matriz completa de agentes (descricao + etapa)

| Agent | Etapa | Papel resumido |
|---|---|---|
| pipeline_intake_orchestrator | P0 | Orquestra intake e define rota inicial |
| prompt_normalizer | P0 | Normaliza prompt e repo_manifest |
| eval_prompt_normalizer | P0 | Avalia qualidade do intake |
| pipeline_brief_orchestrator | P1 | Orquestra refinamento de briefing |
| draft_writer | P1 | Gera draft inicial |
| pm_profile_designer | P1 | Define squad de PMs |
| pm_base | P1 | Critica especializada |
| eval_pm | P1 | Valida qualidade da critica |
| moderator | P1 | Consolida briefing final |
| eval_moderator | P1 | Audita briefing final |
| pipeline_tech_orchestrator | P2 | Orquestra quebra tecnica |
| technical_analyst | P2 | Decompoe modulos |
| eval_tech_analyst | P2 | Audita decomposicao |
| architect | P2/P3 quorum | Define plano tecnico |
| eval_architect | P2 | Audita fidelity 1:1 |
| integration_mapper_llm | P2 | Refina mapa de integracao |
| contract_refiner | P2 | Define contrato por modulo |
| observability_designer | P2 | Define plano de observabilidade operacional |
| eval_observability_designer | P2 | Audita cobertura/qualidade do plano de observabilidade |
| pipeline_build_orchestrator | P3 | Orquestra build paralelo |
| builder | P3 | Implementa modulo |
| devops_infra_builder | P3 | Implementa IaC e automacoes de infra |
| eval_devops_infra | P3 | Valida seguranca e consistencia de infraestrutura |
| test_builder | P3 | Implementa testes unitarios/integracao/e2e |
| eval_test_builder | P3 | Audita qualidade e cobertura dos testes construidos |
| code_reviewer | P3 | Revisa conformidade tecnica |
| builder_qa | P3 | Valida cobertura de escopo |
| judge_quorum | P3/P4 | Desempata conflito tecnico |
| skill_builder | P3 | Construi skill candidate |
| skill_evaluator | P3 | Audita skill candidate |
| pipeline_validation_orchestrator | P4 | Orquestra validacao por risco |
| dynamic_test_planner | P4 | Decide quais testes rodam |
| perf_analyst | P4 | Avalia performance |
| resilience_analyst | P4 | Avalia resiliencia |
| load_analyst | P4 | Valida comportamento sob carga |
| chaos_analyst | P4 | Valida falhas controladas e recuperacao |
| integration_validator | P4 | Valida fronteiras de integracao |
| security | P4 | Audita seguranca |
| observability_validator | P4 | Valida se telemetria/dash/alertas foram implementados |
| pr_validator | P4 | Concilia perf x resilience |
| eval_qa_template | P4 | Audita qualidade do QA executado |
| qa_consolidator | P4 | Homologa resultado cross-QA |
| architect_final_validator | P4 | Valida aderencia da execucao ao desenho arquitetural |
| judge_final | P4 | Decide GO/NO-GO |
| pipeline_docs_orchestrator | P5 | Orquestra documentacao final |
| doc_writer | P5 | Gera docs baseadas em codigo |
| eval_docs | P5 | Audita fidelidade das docs |
| pipeline_learning_orchestrator | P6 | Orquestra cadeia de aprendizado e promocao |
| pipeline_global_orchestrator | P0..P6 | Orquestracao interna opcional da cadeia completa |
| context_ledger_updater | P0..P6 | Mantem memoria/ledger da run |
| memory_builder | P0..P6 | Gera memoria episodica e semantic candidates |
| memory_evaluator | P0..P6 | Deduplica e valida memoria |
| knowledge_curator | P0..P6 | Promove memoria semantica aprovada para knowledge |
| promotion_manager | P6 | Decide promote project/global ou rejeicao de candidatos |

Matriz oficial com packages por dominio: `playbooks/packages/PACKAGES_GUIDE.md`.

Cobertura de performance e custo (estado atual):
- Performance: coberta no P4 por `dynamic_test_planner` + `perf_analyst` + `load_analyst` + `resilience_analyst` + conciliacao `pr_validator`.
- Custo/FinOps: ainda sem agente dedicado canonico no baseline atual.
- Implicacao: custo e eficiencia de execucao sao monitorados operacionalmente, mas sem um papel FinOps especializado na cadeia.
- Recomendacao: incluir agente FinOps para custo por run, custo por etapa/pipeline e alertas de eficiencia.

## 5.4 Runtime corporativo (config decisiva)

Campos-chave no `factory_config.json`:
- `runtime.waiting_status_details`
  - lista de `status_detail` tratados como espera operacional (ex.: `waiting_for_user`, `waiting_for_approval`).
- `runtime.waiting_detail_timeout_seconds`
  - timeout dedicado para estados de espera.
- `runtime.session_defaults`
  - `repos`, `knowledge_ids`, `secret_ids`, `bypass_approval`.
  - `use_repo_manifest_as_repos` (recomendado manter `false` ate validar formato 100% compativel com API).
- `runtime.transport`
  - `runtime.transport.mode=http|mcp` define transporte de sessao (`create/get/send/terminate`).
  - em `mcp`, configurar `runtime.transport.mcp.base_url`, `tool_call_endpoint`,
    `auth_token` e `tools.*` conforme gateway MCP.
- `runtime.terminal_proxy`
  - habilita espelhamento de mensagens da session no terminal.
  - durante `waiting_for_user`/`waiting_for_approval`, permite responder no proprio terminal.
  - parametros: `enabled`, `mirror_session_messages`, `allow_input_during_wait`,
    `announce_waiting_hint`, `prompt_prefix`, `max_message_chars`.
- `runtime.learning`
  - `enabled` liga/desliga o P6 no fluxo `full` e no `resume` automatico apos docs.
  - `max_wait_seconds` controla timeout da etapa de learning.
- `storage`
  - `mode=github_repo`, `github_repo_path`, `runs_root`, `shared_memory_root`, `shared_knowledge_root`, `shared_skills_root`, `enforce_repo_path`.
- `git_sync`
  - `enabled`, `auto_commit`, `auto_push`, `branch`, `commit_message_template`.

Comportamento importante:
- P4 e P5 exigem `status=completed` para sucesso da etapa.
- `release_decision` continua gate de entrada de P5.
- P6 exige `status=completed` e artifacts minimos (`ledger_patch`, `memory_summary`, `knowledge_summary`, `promotion_summary`).

## 6) Execucao em paralelo (multi-projeto)

Use `devin_parallel_runner.py` com batch JSON.

Exemplo:
```bash
python devin_parallel_runner.py --batch ./examples/parallel_jobs.example.json --max-concurrency 2
```

Como funciona:
- cada job roda um subprocess chamando `devin_pipeline_v2.py`
- logs por job vao para o path configurado em `parallel_runner.logs_dir`
- resumo final mostra exit code de cada job
- default atual: `factory_runs/_parallel_logs`

Quando usar:
- multiprojetos independentes
- carga de operacao continua

---

## 7) Novidades V2 e por que existem

1. Complexity Router (P3)
- separa caminho simples/padrao/complexo por modulo.
- evita tratar tudo como "complexo" e perder eficiencia.

2. Dynamic Test Planner (P4)
- ativa validacao por risco real.
- reduz redundancia e custo de verificacao.

3. Skill loop dinamico
- builder/architect podem sugerir skill candidate.
- `skill_builder` estrutura.
- `skill_evaluator` aprova/reprova.
- resultado vira ativo reutilizavel de operacao.

4. Session ledger
- rastreia sessions parent por etapa no output.
- melhora auditabilidade e troubleshooting.

5. Memoria dual-layer (episodic + semantic)
- separa fatos da execucao (episodic) de heuristicas reutilizaveis (semantic).
- reduz ruido e melhora evolucao autonoma de knowledge.

---

## 8) Onde alterar cada comportamento

"Quero mudar logica da pipeline":
- editar `playbooks/pipeline_*_orchestrator.md`

"Quero mudar criterio tecnico de um papel":
- editar playbook do papel (`builder.md`, `security.md`, etc)

"Quero mudar contrato de saida":
- editar `schemas.py`
- regenerar/ajustar `schemas/*.json`

"Quero mudar comando/fluxo de execucao":
- `devin_pipeline_v2.py`

"Quero manter continuidade entre LLMs":
- atualizar `LLM_HANDOFF_LOG.md` a cada bloco relevante (progresso, decisoes e proximos passos).

"Quero mudar paralelismo multi-projeto":
- `devin_parallel_runner.py`
- `examples/parallel_jobs.example.json`

"Quero ajustar setup de ambiente":
- `factory_config.json`
- `config_loader.py`
- `.env.example` (somente placeholders/env secrets)
- `requirements.txt`

---

## 9) Operacao recomendada (playbook de time)

1. Rodar 1 projeto piloto (`full`) e validar qualidade de artefatos.
2. Rodar 2 projetos em paralelo e medir estabilidade/custo.
3. Ajustar timeouts e max concurrency.
4. Ativar gates humanos em P1/P2/P4 para projetos criticos.
5. Revisar skill candidates aprovadas a cada ciclo.

---

## 10) Troubleshooting rapido

Erro: "ERRO: instale aiohttp"
- instalar dependencias: `pip install -r requirements.txt`

Erro de playbook id ausente
- conferir `playbooks.*` no `factory_config.json` e placeholders `PLAYBOOK_*` no ambiente

Pipeline travando em gate
- verificar se arquivo `APPROVE_*` ou `REJECT_*` foi criado corretamente

Resume falhando
- garantir que artefatos anteriores existem no output:
  - `--from tech` precisa de `p_1`
  - `--from build` precisa de `p_1` e `p_2`
  - `--from validate` precisa de `p_1`, `p_2`, `p_3`
  - `--from docs` precisa de `p_1`, `p_2`, `p_3`, `p_4`
  - `--from learn` usa contexto disponivel e prioriza `p_2`, `p_4`, `p_5`

Erro: `storage.github_repo_path` ausente/invalido
- conferir `.env` e `FACTORY_GITHUB_REPO_PATH`
- garantir que a pasta existe e contem `.git`

Erro de escrita fora do repo corporativo
- ocorre quando `storage.enforce_repo_path=true` e `output_dir` aponta fora do repo
- usar caminho relativo a `<FACTORY_GITHUB_REPO_PATH>` ou omitir `output_dir`

Session em `waiting_for_user`/`waiting_for_approval` ate timeout
- ajustar `runtime.waiting_detail_timeout_seconds` conforme politica da empresa
- revisar necessidade de `bypass_approval` em `runtime.session_defaults` (quando permitido)

--- 

## 11) Definicao curta do sistema

Se voce precisar explicar este pacote em 30 segundos:

"E uma factory de software com orquestracao por agentes no Devin.
Tem 7 etapas operacionais (P0..P6, com P6 opcional por configuracao),
incluindo intake, produto, tecnica, build, validacao, docs e learning,
com workers especializados, avaliacao por etapa, homologacao QA,
judge final de release e suporte a execucao paralela entre projetos."

---

## 12) Leitura complementar

- `README.md` (operacao rapida)
- `COORDINATOR_HANDOFF_AND_MEMORY.md` (handoff/memoria detalhados)
- `MASTER_GUIDE.md` (historico de decisoes e racional antigo)
- `CORPORATE_HARDENING_EXPLICITO.md` (as-is -> problema -> solucao -> por que)
- `DEVIN_DOCS_CONFORMANCE_AUDIT.md` (aderencia a docs oficiais do Devin)

---

Fim.
