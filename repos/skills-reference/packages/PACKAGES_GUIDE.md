# Agent Packages Guide

## Decisao de organizacao

Modelo adotado: **packages por dominio funcional** (intake, product, technology, build, validation, documentation, shared)
com **fluxo operacional por etapa** (P0..P6).

Resumo da decisao:
- Melhor para operacao: ownership por area (Produto, Tecnologia, Validacao, Docs).
- Melhor para evolucao: evita quebrar taxonomia quando a pipeline ganha/ajusta etapas.
- Melhor para governanca: reduz sobreposicao de agentes multi-etapa.

## Por que nao pacote por P0/P1/P2 apenas

Pacote somente por etapa funciona no curto prazo, mas piora manutencao:
- Se uma etapa muda, move ou subdivide, a estrutura de pastas quebra junto.
- Agentes transversais (`judge_quorum`, `context_ledger_updater`) tendem a duplicacao.
- Ownership por time fica opaco (Validacao e Docs ficam acoplados a numero de etapa).

Conclusao:
- Use **dominio como taxonomia principal**.
- Use **P0..P6 como indice operacional** (execucao e observabilidade).

## Estrutura de packages

- `playbooks/packages/intake/`
- `playbooks/packages/product/`
- `playbooks/packages/technology/`
- `playbooks/packages/build/`
- `playbooks/packages/validation/`
- `playbooks/packages/documentation/`
- `playbooks/packages/shared/`

## Coordinator inicial central

No modo agent-first, a sessao inicial central e:
- `Factory Control-Plane Agent`

O contrato canonico de execucao dessa sessao e:
- `pipeline_global_orchestrator`

O arquivo `master_pipeline_prompt.md` continua existindo, mas **apenas como bootstrap tecnico**.
Ele nao deve mais ser tratado como a fonte da verdade da pipeline.
O usuario nao deveria precisar colar esse prompt operacionalmente a cada run.

Responsabilidade do coordinator central:
- abrir a sessao raiz
- definir e controlar a rota `P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6`
- aplicar `resume`, `skip`, gates obrigatorios de revisao humana e execucao mandataria de `P6`
- disparar orchestrators de etapa e especialistas
- controlar dependencias, quorum, escalacao e handoffs
- consolidar artefatos e expor resultado de cada etapa ao usuario com resumo antes da aprovacao da proxima

## Matriz de agentes (fonte oficial)

| Agent | Package | Etapa principal | Papel |
|---|---|---|---|
| pipeline_intake_orchestrator | intake | P0 | Orquestra prompt cru -> normalizacao -> spec -> aprovacao humana -> handoff |
| prompt_normalizer | intake | P0 | Normaliza prompt inicial, anexos e hints para geracao de spec |
| eval_prompt_normalizer | intake | P0 | Avalia se a normalizacao esta pronta para sustentar a spec |
| spec_writer | intake | P0 | Gera a spec inicial de intake com apoio de AR, refinement e skills aderentes |
| eval_spec_writer | intake | P0 | Audita a spec antes da revisao humana e do handoff para P1 |
| pipeline_brief_orchestrator | product | P1 | Orquestra refinamento de briefing |
| draft_writer | product | P1 | Produz draft inicial de briefing |
| pm_profile_designer | product | P1 | Define composicao de PMs especialistas |
| pm_base | product | P1 | Critica especializada de produto |
| eval_pm | product | P1 | Filtra qualidade de critica dos PMs |
| moderator | product | P1 | Consolida criticas aprovadas em briefing final |
| eval_moderator | product | P1 | Valida briefing refinado pelo moderator |
| pipeline_tech_orchestrator | technology | P2 | Orquestra backlog tecnico, contratos, integracao e diagramas Mermaid |
| technical_analyst | technology | P2 | Quebra backlog tecnico em slices pequenas e produz Mermaid funcional |
| eval_tech_analyst | technology | P2 | Valida granularidade, rastreabilidade e Mermaid funcional |
| architect | technology | P2/P3(quorum) | Define build_plan, decisoes tecnicas e Mermaid tecnico |
| eval_architect | technology | P2 | Valida fidelity 1:1 modules/build_plan |
| integration_mapper_llm | technology | P2 | Explicita mapa de integracao e dependencias coerentes com os diagramas |
| contract_refiner | technology | P2 | Refina contratos por modulo com referencias de schema |
| observability_designer | technology | P2 | Define plano de observabilidade (metricas/logs/traces/dash/alertas) |
| eval_observability_designer | technology | P2 | Valida qualidade e cobertura do plano de observabilidade |
| pipeline_build_orchestrator | build | P3 | Orquestra execucao pilot+parallel |
| builder | build | P3 | Implementa modulo |
| devops_infra_builder | build | P3 | Implementa modulo de infraestrutura/IaC |
| code_reviewer | build | P3 | Avalia conformidade tecnica do codigo |
| builder_qa | build | P3 | Construi testes unitarios do slice e matriz minima de rastreabilidade |
| test_builder | build | P3 | Construi testes complementares de integracao/contrato quando o risco exigir |
| eval_test_builder | build | P3 | Audita se a camada de testes esta aderente ao contrato, risco e ownership esperado |
| eval_devops_infra | build | P3 | Audita fidelidade/seguranca/idempotencia de IaC |
| judge_quorum | build | P3/P4 | Desempata conflitos tecnicos vinculantes |
| skill_builder | build | P3 | Materializa skill candidate |
| skill_evaluator | build | P3 | Audita skill candidate |
| pipeline_validation_orchestrator | validation | P4 | Orquestra validacao dinamica por risco |
| dynamic_test_planner | validation | P4 | Decide quais validadores acionar |
| perf_analyst | validation | P4 | Avalia performance |
| resilience_analyst | validation | P4 | Avalia resiliencia/falhas externas |
| integration_validator | validation | P4 | Valida contratos de integracao |
| security | validation | P4 | Avalia seguranca |
| load_analyst | validation | P4 | Avalia riscos de carga/volume/concurrency |
| chaos_analyst | validation | P4 | Avalia readiness para falhas abruptas/degradacao |
| observability_validator | validation | P4 | Valida cobertura de observabilidade no codigo entregue |
| architect_final_validator | validation | P4 | Valida aderencia final da implementacao ao desenho arquitetural |
| pr_validator | validation | P4 | Concilia perf x resilience |
| eval_qa_template | validation | P4 | Audita qualidade do QA executado |
| qa_consolidator | validation | P4 | Homologa resultados dos QAs |
| judge_final | validation | P4 | Decisao final GO/NO-GO |
| pipeline_docs_orchestrator | documentation | P5 | Orquestra documentacao final |
| doc_writer | documentation | P5 | Gera docs finais baseadas no codigo |
| eval_docs | documentation | P5 | Valida fidelidade e qualidade de docs |
| pipeline_global_orchestrator | shared | P0..P6 | Coordenador raiz canonico da cadeia completa, gates, resume, contexto e consolidado final |
| context_ledger_updater | shared | P0..P6 | Atualiza ledger de contexto/memoria ao longo da run e na consolidacao final |
| memory_builder | shared | P0..P6/P6 | Separa memoria episodica e semantic a partir de evidencias da run |
| memory_evaluator | shared | P0..P6/P6 | Deduplica e valida memoria antes de promover |
| knowledge_curator | shared | P0..P6/P6 | Converte semantic memory aprovada em knowledge reutilizavel |
| promotion_manager | shared | P6 | Decide promocao project/global para memoria/knowledge/skills |
| pipeline_learning_orchestrator | shared | P6 | Executa obrigatoriamente a etapa final de learning, promotions e consolidacao institucional |

Observacao sobre cobertura FinOps:
- Performance e carga estao cobertas no pacote `validation` (`perf_analyst`, `load_analyst`, `resilience_analyst`, `pr_validator`).
- Ainda nao existe agente FinOps dedicado canonico para custo/eficiencia de execucao.
- Tratar FinOps como gap planejado de evolucao (custo por run, custo por etapa, alertas de eficiencia).

## Indice rapido por etapa

- P0: `pipeline_intake_orchestrator`, `prompt_normalizer`, `eval_prompt_normalizer`, `spec_writer`, `eval_spec_writer`
- P1: `pipeline_brief_orchestrator`, `draft_writer`, `pm_profile_designer`, `pm_base`, `eval_pm`, `moderator`, `eval_moderator`
- P2: `pipeline_tech_orchestrator`, `technical_analyst`, `eval_tech_analyst`, `architect`, `eval_architect`, `integration_mapper_llm`, `contract_refiner`, `observability_designer`, `eval_observability_designer`
- P3: `pipeline_build_orchestrator`, `builder`, `devops_infra_builder`, `code_reviewer`, `builder_qa`, `test_builder`, `eval_test_builder`, `eval_devops_infra`, `judge_quorum`, `skill_builder`, `skill_evaluator`
- P4: `pipeline_validation_orchestrator`, `dynamic_test_planner`, `perf_analyst`, `resilience_analyst`, `integration_validator`, `security`, `load_analyst`, `chaos_analyst`, `observability_validator`, `architect_final_validator`, `pr_validator`, `eval_qa_template`, `qa_consolidator`, `judge_final`
- P5: `pipeline_docs_orchestrator`, `doc_writer`, `eval_docs`
- P6: `pipeline_learning_orchestrator`, `context_ledger_updater`, `memory_builder`, `memory_evaluator`, `knowledge_curator`, `promotion_manager`
- Transversal: `pipeline_global_orchestrator`

## Regras de funcionamento out-of-box

1. Runtime usa playbooks canonicos em `playbooks/*.md`.
2. `playbooks/packages/*` e camada organizacional para registro e governanca.
3. IDs em `factory_config.json` devem apontar para orchestrators canonicos (`playbooks.intake/brief/tech/build/validate/docs/learning`).
4. O **contrato canonico de entrada** da pipeline inteira deve ser `agent_runtime.root_orchestrator`.
5. `master_pipeline_prompt.md` deve existir apenas como bootstrap tecnico, nao como fonte de verdade da pipeline.
6. Antes do primeiro run, valide:
   - repos e referencias resolvidos em `repos/factory-params/params/repos.json`
   - fallbacks definidos em `repos/factory-params/params/repos_fallback.json` quando necessario
   - `root_orchestrator` apontando para `playbooks/packages/shared/pipeline_global_orchestrator.md`
   - gates humanos configurados para revisar `P0..P6` antes de cada transicao
7. Tracking e memoria saem automaticos no output:
   - `execution_tracking.md`, `dilemmas_and_solutions.md`, `tracking_events.jsonl`
   - `memory/episodic_memory.jsonl` e `memory/semantic_memory_candidates.jsonl`
8. `P6` nao deve ser desabilitada:
   - a etapa final sempre consolida memoria, knowledge, skills e promocoes da run
