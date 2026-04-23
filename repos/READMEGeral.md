# Guia Geral Da Factory Agent-First

## O que e este projeto

Este projeto implementa uma software factory orientada a agentes, desenhada para rodar a pipeline inteira a partir de **uma sessao raiz unica** do Devin.

O objetivo e substituir o runtime Python legado por uma arquitetura em que:
- a sessao raiz coordena o fluxo ponta a ponta;
- os orchestrators de etapa controlam apenas a etapa que lhes pertence;
- os especialistas executam slices pequenas, verificaveis e com contratos claros;
- tracking, memoria, knowledge, skills e estado de resume ficam persistidos em repos internos.

## Qual e o ponto de entrada canonico

O ponto de entrada canonico e:
- `repos/factory-control-plane/prompts/master_pipeline_prompt.md`

Esse arquivo e **bootstrap only**.
Ele nao define a logica da pipeline.

O contrato de execucao canonico da pipeline inteira e:
- `playbooks/packages/shared/pipeline_global_orchestrator.md`

Em outras palavras:
- `master_pipeline_prompt.md` inicia a sessao raiz;
- `pipeline_global_orchestrator` controla a pipeline inteira;
- os orchestrators de etapa executam `P0..P6`;
- os especialistas executam o trabalho local de cada etapa.

## Como a estrutura esta organizada

### Camada canonica de runtime
- `playbooks/packages/`

Aqui ficam os playbooks canonicos realmente usados para definir o comportamento dos agents.
Se houver duvida sobre o comportamento de um agent, essa e a pasta que deve ser tratada como fonte principal.

### Camada de repos internos
- `repos/`

Aqui ficam os repos internos que substituem o antigo runtime Python:

1. `repos/factory-control-plane`
   Prompt de bootstrap, policies, DAG, resume, scheduler, quorum e regras de orquestracao.
2. `repos/factory-contracts`
   Schemas de coordinator, subagents, runtime state, handoffs, promotions e tracking.
3. `repos/factory-params`
   Parametros, perfis, toggles e mapa de repos.
4. `repos/architecture-reference`
   Guardrails, patterns e referencias arquiteturais.
5. `repos/skills-reference`
   Espelho/referencia dos playbooks e skills.
6. `repos/refinement-support`
   Materiais de apoio para intake e briefing.
7. `repos/factory-memory-knowledge`
   Stores de memoria, knowledge, skills e promocoes.
8. `repos/factory-runtime-data`
   Outputs de run, tracking, metrics, state e locks.
9. `repos/project-target-repos`
   Repos reais ou templates tocados pela pipeline.

## O que pode parecer confuso na estrutura

Hoje existem **duas pastas com agents/playbooks**:
- `playbooks/packages`
- `repos/skills-reference/packages`

O desenho correto e:
- `playbooks/packages` = fonte canonica de runtime
- `repos/skills-reference/packages` = espelho/referencia

Entao, se um playbook mudar em `playbooks/packages`, o espelho em `repos/skills-reference/packages` precisa acompanhar.
Se isso nao acontecer, a estrutura realmente fica confusa.

## Fluxo completo da pipeline

### P0 - Intake
Agent principal:
- `pipeline_intake_orchestrator`

Especialistas principais:
- `prompt_normalizer`
- `eval_prompt_normalizer`
- `spec_writer`
- `eval_spec_writer`

Responsabilidade:
- transformar o pedido bruto em input estruturado;
- gerar uma spec inicial forte a partir do prompt;
- avaliar essa spec antes de leva-la ao humano;
- trazer a spec para aprovacao humana em `P0`;
- absorver melhorias pedidas pelo humano e iterar a spec;
- decidir `route_mode`;
- preparar handoff confiavel para `P1` usando `approved_intake_spec`.

### P1 - Brief
Agent principal:
- `pipeline_brief_orchestrator`

Especialistas principais:
- `draft_writer`
- `pm_profile_designer`
- `pm_base`
- `eval_pm`
- `moderator`
- `eval_moderator`

Responsabilidade:
- construir o briefing consolidado de produto;
- definir objetivos, non-goals, riscos, restricoes e criterios de aceite.

### P2 - Tech
Agent principal:
- `pipeline_tech_orchestrator`

Especialistas principais:
- `technical_analyst`
- `eval_tech_analyst`
- `architect`
- `eval_architect`
- `integration_mapper_llm`
- `contract_refiner`
- `observability_designer`
- `eval_observability_designer`

Responsabilidade:
- traduzir briefing em build plan implementavel;
- produzir `module_defs`, `contracts`, `integration_map`, `observability_plan` e esbocos Mermaid funcional/tecnico.

### P3 - Build
Agent principal:
- `pipeline_build_orchestrator`

Especialistas principais:
- `builder`
- `devops_infra_builder`
- `code_reviewer`
- `builder_qa`
- `test_builder`
- `eval_test_builder`
- `eval_devops_infra`
- `judge_quorum`
- `skill_builder`
- `skill_evaluator`

Responsabilidade:
- enumerar tarefas de build;
- controlar DAG de modulos;
- montar `ready_queue`;
- despachar trabalho paralelo so quando for seguro;
- fazer `builder_qa` ser o owner dos testes unitarios do slice;
- usar `test_builder` so para suites complementares quando o risco exigir;
- consolidar artefatos e handoff para `P4`.

### P4 - Validation
Agent principal:
- `pipeline_validation_orchestrator`

Especialistas principais:
- `dynamic_test_planner`
- `security`
- `integration_validator`
- `perf_analyst`
- `load_analyst`
- `resilience_analyst`
- `chaos_analyst`
- `observability_validator`
- `architect_final_validator`
- `pr_validator`
- `eval_qa_template`
- `qa_consolidator`
- `judge_final`

Responsabilidade:
- validar por risco;
- consolidar findings;
- emitir `release_decision`.

### P5 - Docs
Agent principal:
- `pipeline_docs_orchestrator`

Especialistas principais:
- `doc_writer`
- `eval_docs`

Responsabilidade:
- produzir documentacao final aderente ao sistema real entregue;
- garantir fidelidade operacional e navegabilidade.

### P6 - Learning
Agent principal:
- `pipeline_learning_orchestrator`

Especialistas principais:
- `context_ledger_updater`
- `memory_builder`
- `memory_evaluator`
- `knowledge_curator`
- `promotion_manager`

Responsabilidade:
- consolidar memoria, knowledge e skill candidates;
- decidir promocoes;
- persistir aprendizado institucional da run.

## Quem coordena o que

### Coordenador raiz
- `pipeline_global_orchestrator`

Responsavel por:
- stage machine `P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6`
- regras de skip/gate/resume
- despacho dos orchestrators filhos
- consolidacao final da run

### Scheduler interno de build
- `pipeline_build_orchestrator` + `scheduler_policy.md`

Responsavel por:
- DAG de modulos
- `ready_queue`
- paralelismo seguro em `P3`

Importante:
- o scheduler **nao** decide transicao entre etapas
- a transicao entre etapas pertence ao root orchestrator

## Principais funcionalidades do projeto

1. **Uma sessao raiz unica**
   O usuario entra por um bootstrap e a sessao raiz conduz toda a pipeline.

2. **Execucao por stages**
   Cada etapa tem ownership claro e handoff estruturado.

3. **Parallelismo com dependencia**
   `P3` usa DAG de modulos e fila de trabalho segura.

4. **Quorum interno antes de humano**
   Conflitos relevantes devem tentar resolucao interna antes de escalar.

5. **Child sessions com envelopes formais**
   Coordinators e specialists se comunicam por envelopes de `CoordinatorInput`, `SubagentTask`, `SubagentResult` e `CoordinatorOutput`.
   Isso ajuda a manter tasks pequenas, outputs rastreaveis e persistencia consistente.

6. **Debates por etapa**
   P1, P2, P3, P4 e P6 devem abrir rodadas internas de debate quando houver ambiguidade material antes de quorum ou escalacao humana.

7. **Resume**
   A run pode continuar de uma etapa intermediaria com base no state persistido.

8. **Tracking e auditoria**
   Estado, dilemas, eventos, outputs e handoffs ficam persistidos.

9. **Memoria, knowledge e skills**
   O aprendizado da run vira ativo reutilizavel no ciclo obrigatorio `P6`.

10. **Resumo e aprovacao humana por etapa**
   Toda etapa terminal fecha com resumo estruturado, artefatos principais, blockers e proposta de proximo passo.
   O root orchestrator deve aguardar aprovacao humana explicita antes de avancar.

## Arquivos mais importantes para entender o sistema

- `factory_config.json`
- `repos/factory-control-plane/prompts/master_pipeline_prompt.md`
- `playbooks/packages/shared/pipeline_global_orchestrator.md`
- `playbooks/packages/build/pipeline_build_orchestrator.md`
- `repos/factory-control-plane/docs/SCHEDULER_AND_DAG.md`
- `repos/factory-control-plane/workflows/pipeline_dag.json`
- `repos/factory-control-plane/workflows/resume_map.json`
- `repos/factory-params/params/repos.json`
- `repos/factory-params/params/repos_fallback.json`

## Como usar o projeto

### 1) Ajustar configuracao
Revise:
- `factory_config.json`
- `repos/factory-params/params/repos.json`
- `repos/factory-params/params/repos_fallback.json`

Defina:
- repos locais canonicos
- fallbacks, se existirem
- concurrency, timeouts e regras de review humano obrigatorio

### 2) Garantir que os playbooks canonicos estejam corretos
A pasta canonica e:
- `playbooks/packages`

Se voce alterar essa pasta, sincronize o espelho:
- `repos/skills-reference/packages`

### 3) Iniciar uma sessao raiz do Devin
Use o bootstrap:
- `repos/factory-control-plane/prompts/master_pipeline_prompt.md`

Essa sessao deve:
- carregar `factory_config.json`
- resolver `agent_runtime.root_orchestrator`
- delegar a execucao ao `pipeline_global_orchestrator`

### 4) Acompanhar a execucao
Os outputs de runtime ficam principalmente em:
- `repos/factory-runtime-data`

Arquivos importantes:
- `tracking/execution_tracking.md`
- `tracking/dilemmas_and_solutions.md`
- `tracking/tracking_events.jsonl`
- `state/runtime_state.json`
- `state/workspace_handoff.json`

### 5) Consumir os resultados
Os resultados principais da run devem incluir:
- status por etapa
- resumo terminal de cada etapa para revisao humana
- indice de artefatos
- blockers e decisoes
- release decision
- promocoes de memoria/knowledge/skills produzidas em `P6`

## Regras operacionais importantes

1. O bootstrap **nao** e a fonte de verdade da pipeline.
   O contrato canonico da pipeline e o `pipeline_global_orchestrator`.

2. `P6` e uma etapa real e obrigatoria.
   Ela sempre fecha a run com consolidacao de memoria, knowledge, skills e promocoes.

3. O root orchestrator manda na stage machine.
   Os orchestrators de etapa mandam apenas dentro da propria etapa.

4. Toda etapa precisa fechar com resumo e revisao humana antes da aprovacao da proxima.

5. O espelho em `repos/skills-reference` nao deve divergir da fonte canonica sem motivo.

## Estado atual do desenho

Hoje o desenho central esta assim:
- `master_pipeline_prompt.md` = bootstrap fino
- `pipeline_global_orchestrator` = contrato canonico de execucao
- `pipeline_build_orchestrator` = contrato canonico do scheduler de `P3`
- demais stage orchestrators = coordenadores especificos de etapa

Esse e o desenho correto para o modelo agent-first que discutimos.
