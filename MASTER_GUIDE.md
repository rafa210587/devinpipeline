# Devin Factory V2 - Hybrid Master Spec (Best of Both)

Data: 2026-04-16
Status: aprovado para desenho alvo
Objetivo: unificar o melhor dos playbooks do Claude com a governanca da V1, mantendo 5 pipes, paralelismo real, debate entre agentes, skills dinamicas e validacao precisa sem redundancia.

---

## 1) Decisao executiva

Avaliacao final dos playbooks:
- Melhor para execucao operacional: pacote Claude (orchestrators + workers + evals).
- Melhor para governanca e estrategia de produto: V1 (5 pipes oficiais, QA Homologator, memoria x guardrails, API/MCP primario e CLI em piloto).
- Melhor V2: hibrido. Basear execucao nos playbooks Claude, com ajustes estruturais obrigatorios da V1.

Veredito objetivo:
- Claude venceu em profundidade operacional, fallbacks e disciplina de runtime.
- V1 venceu em desenho de sistema, separacao de responsabilidades e direcao de longo prazo.
- V2 deve manter ~75% da malha operacional do Claude e ~90% da governanca da V1.

---

## 2) Analise profunda dos playbooks (quem ficou melhor e por que)

Criterios usados (0-10):
- clareza de papel
- qualidade de entrada/saida
- capacidade de paralelismo
- tratamento de falhas e retries
- disciplina de debate/quorum
- calibracao de avaliacao
- risco de redundancia
- aderencia ao fluxo real da Agent Farm
- capacidade de escalar simples vs complexo
- extensibilidade para skills/memory

### 2.1 Score consolidado por bloco

| Bloco | Claude | V1 Templates | Melhor |
|---|---:|---:|---|
| Orchestrators P1-P5 | 9.2 | 6.1 | Claude |
| Workers de execucao (P2/P3) | 8.9 | 6.4 | Claude |
| Validators/evals/homologacao | 8.7 | 7.4 | Claude |
| Governanca de pipeline (5 pipes, gates, papel QA final) | 7.6 | 9.1 | V1 |
| Estrategia skills + memory + guardrails | 6.5 | 9.0 | V1 |
| Estrategia CLI subagents vs API/MCP | 6.2 | 8.8 | V1 |

### 2.2 Diagnostico por pipe

Pipe A (Brief/Refinamento):
- Claude melhor no mecanismo de debate real (draft -> PMs paralelos -> eval por critica -> moderator -> eval moderator).
- V1 melhor ao explicitar gate formal de readiness e alinhamento com suas 5 pipes.
- V2: manter motor Claude de debate, com contratos V1 de artefato e gate.

Pipe B (Quebra tecnica):
- Claude muito forte no controle de fidelity gap (mapping 1:1 modules -> build_plan) com eval dedicado.
- V1 melhor na semantica de ownership e simplificacao de outputs para backlog tecnico.
- V2: manter fluxo Claude, adicionar classificacao de complexidade por task para roteamento de build.

Pipe C (Execucao/build):
- Claude excelente em pilot-then-parallelize, deterministic checks, quorum e loop guards.
- V1 melhor na visao de papel executor/evaluator com menos sobrecarga semantica.
- V2: manter esqueleto Claude, com dispatch dinamico por complexidade e limite adaptativo de builders.

Pipe D (Validacao/testing):
- Claude forte em malha de validadores + QA Consolidator + Judge Final.
- Ponto fraco Claude: tende a executar validacoes amplas sempre, com risco de redundancia e custo.
- V1 trouxe direcao correta de homologacao e avaliacao sem Telegram.
- V2: manter Consolidator/Judge, adicionar Risk-Based Dynamic Test Planner para decidir quando rodar perf/load/security/resilience/chaos.

Pipe E (Docs):
- Claude melhor em fidelidade ao codigo e anti-alucinacao com eval_docs.
- V1 melhor em alinhar docs ao gate de release homologado.
- V2: manter quase integral do Claude.

### 2.3 Diagnostico por capacidade pedida por voce

Separacao por etapas:
- V1 melhor no desenho macro.
- Claude melhor no micro-fluxo de execucao.
- V2: combinar os dois (obrigatorio).

Executar tarefas simples e complexas:
- Claude cobre bem complexas, mas nao define estrategia explicita de simplificacao.
- V1 sugere modularizacao, sem algoritmo de roteamento.
- V2: criar Complexity Router no Coordinator.

Quebra e distribuicao para builders em paralelo:
- Claude ja entrega mecanismo robusto em P3.
- V1 precisa de detalhe operacional.
- V2: base Claude + limites dinamicos por risco/custo.

Agentes discutirem entre si:
- Claude cobre debate forte em P1 e quorum em P3/P4.
- Falta protocolo de debate transversal para qualquer etapa.
- V2: criar Debate Protocol transversal (proposal/challenge/synthesis/decision).

Agentes construirem skills:
- Claude nao cobre.
- V1 cobre estrategia, mas nao fluxo operacional completo.
- V2: Skill Creation Loop (propose -> build -> eval -> publish -> memory).

Consultar skills + guardrails da arquitetura de 102k:
- Claude depende de ARR, mas sem taxonomia de skills.
- V1 define modularizacao e precedencia.
- V2: skill registry por dominio/pipe/risco + retrieval orientado por tarefa.

Validacao precisa sem redundancia:
- Claude e forte em rigor, mas com tendencia a sobrevalidar.
- V1 e forte em principio, mas sem mecanismo tecnico.
- V2: Dynamic Test Planner com gatilhos de risco e deduplicacao de evidencias.

Coordinator mantendo contexto entre sessoes:
- Claude usa bem estado operacional, mas precisa reforco em memoria estrategica e skills evolutivas.
- V1 define melhor precedencia memoria x guardrails.
- V2: state unico canonicamente versionado por run.

---

## 3) O que entra na V2 (keep/change/drop)

### 3.1 Keep (Claude)
- pipeline_brief_orchestrator: manter motor de debate em rounds + eval de critica.
- pipeline_tech_orchestrator: manter enforce 1:1 modules/build_plan + eval_architect.
- pipeline_build_orchestrator: manter pilot-then-parallelize + deterministic checks + quorum.
- pipeline_validation_orchestrator: manter fanout de validadores + QA Consolidator + Judge Final.
- pipeline_docs_orchestrator: manter fluxo doc_writer -> eval_docs.
- worker/eval specs detalhadas de P2/P3/P4/P5 (com ajustes abaixo).

### 3.2 Keep (V1)
- 5 pipes oficiais como contrato de governanca.
- separacao executor/evaluator e papel explicito de QA Homologator.
- precedencia de memoria: objective > guardrail hard > contratos locked > heuristicas.
- estrategia de plataforma: API/MCP primario, CLI subagents como piloto controlado.

### 3.3 Change (obrigatorio na V2)
- adicionar Complexity Router antes de Pipe C.
- adicionar Debate Protocol transversal para Pipe B/C/D (nao so P1 e quorum).
- adicionar Skill Creation Loop com aprovacao por Skill Evaluator.
- adicionar Dynamic Test Planner para evitar validacao redundante.
- transformar P4 em validacao por risco e contexto (nao sempre full fanout).
- adicionar Session Context Ledger para manter contexto entre parent/children.

### 3.4 Drop
- qualquer dependencia de Telegram.
- qualquer validacao duplicada sem ganho de sinal.
- qualquer regra fixa de teste que ignore risco real do modulo.

### 3.5 Quadro playbook-a-playbook (veredito final)

| Playbook | Base escolhida | Veredito V2 | Motivo principal |
|---|---|---|---|
| pipeline_brief_orchestrator | Claude | Keep + tune | Melhor debate multi-PM com eval por critica; ajustar contratos da V1 |
| draft_writer | Claude | Keep | Bom draft inicial com schema disciplinado |
| pm_profile_designer | Claude | Keep | Bom dimensionamento de squad por lacuna real |
| pm_base | Claude | Keep + tune | Excelente para debate, mas limitar ruido e padronizar criticas por risco |
| eval_pm | Claude | Keep | Gate anti-ruido muito bom |
| moderator | Claude | Keep | Boa sintese de critica aprovada |
| eval_moderator | Claude | Keep | Fecha ciclo de qualidade do Pipe A |
| pipeline_tech_orchestrator | Claude | Keep + tune | Fluxo tecnico robusto; ajustar integracao com complexity router |
| technical_analyst | Claude | Keep | Decomposicao clara e orientada a stories |
| eval_tech_analyst | Claude | Keep | Evita decomposicao fraca e catch-all |
| architect | Claude | Keep + tune | Forte no 1:1; incluir politica de skills candidatas por modulo |
| eval_architect | Claude | Keep | Melhor controle contra fidelity gap |
| integration_mapper_llm | Claude | Keep + tune | Util para enriquecer contratos; ativacao deve ser condicional por risco |
| contract_refiner | Claude | Keep | Bom contrato cirurgico por modulo |
| pipeline_build_orchestrator | Claude | Keep + tune | Melhor estrategia operacional; adicionar roteamento simples/complexo |
| builder | Claude | Keep + tune | Forte em escopo e quorum; adicionar hook para proposta de skills |
| code_reviewer | Claude | Keep | Regras objetivas e acionaveis |
| builder_qa | Claude | Keep | Excelente cobertura de acceptance por story |
| judge_quorum | Claude | Keep | Boa decisao vinculante com rastreabilidade |
| pipeline_validation_orchestrator | Claude | Keep + tune | Estrutura forte; tornar ativacao de testes dinamica por risco |
| perf_analyst | Claude | Keep + tune | Bom criterio de severidade; ativar so quando risco/volume pedir |
| resilience_analyst | Claude | Keep + tune | Forte; ativar por dependencia externa e criticidade |
| integration_validator | Claude | Keep | Essencial para executabilidade |
| security | Claude | Keep | Essencial e com override correto |
| pr_validator | Claude | Keep | Resolve conflito perf x resilience sem misturar papeis |
| eval_qa_template | Claude | Keep + tune | Bom para auditoria de QA; deduplicar com Dynamic Test Planner |
| qa_consolidator | Claude | Keep | Melhor elemento de homologacao cross-QA |
| judge_final | Claude | Keep + tune | Bom gate terminal; usar sinal do DTP para evitar overblocking |
| pipeline_docs_orchestrator | Claude | Keep | Simples e funcional |
| doc_writer | Claude | Keep | Forte anti-alucinacao |
| eval_docs | Claude | Keep | Excelente para fidelidade documental |
| Product/Tech/QA/Doc templates V1 | V1 | Keep as policy layer | Servem como camada de governanca e padrao de saida |
| QAHomologator (V1) | V1 | Merge into qa_consolidator role | Funcao permanece obrigatoria, sem duplicar agente |
| QuorumArchitect/QuorumJudge (V1) | V1 + Claude | Merge with architect + judge_quorum | Evita redundancia de papeis |

---

## 4) Arquitetura V2 do Coordinator (orquestrador real)

## 4.1 Responsabilidades
- planejar e despachar por pipe.
- selecionar estrategia simples vs complexa por task.
- abrir debates entre agentes quando houver incerteza relevante.
- controlar fanout paralelo de builders com limites adaptativos.
- acionar validacao dinamica baseada em risco.
- aprovar ou bloquear promocao de skills candidatas.
- consolidar memoria de run para proximas sessoes.

## 4.2 Estado canonico (coordinator_state.json)

```json
{
  "run_id": "string",
  "project_slug": "string",
  "parent_session_id": "string",
  "child_sessions": [
    {
      "session_id": "string",
      "pipe": "A|B|C|D|E",
      "role": "executor|evaluator|homologator|debater|skill_builder",
      "status": "running|blocked|done|failed"
    }
  ],
  "artifacts": {
    "pipe_a": {},
    "pipe_b": {},
    "pipe_c": {},
    "pipe_d": {},
    "pipe_e": {}
  },
  "debates": [
    {
      "debate_id": "string",
      "topic": "string",
      "options": ["string"],
      "decision": "string",
      "rationale": "string",
      "applies_to": ["task_id"]
    }
  ],
  "skills": {
    "candidates": [],
    "published": [],
    "rejected": []
  },
  "memory_updates": {
    "locked_decisions": [],
    "anti_patterns": [],
    "similar_failures": [],
    "heuristics": []
  },
  "gates": {
    "pipe_a": "approved|blocked|retry",
    "pipe_b": "approved|blocked|retry",
    "pipe_c": "approved|blocked|retry",
    "pipe_d": "approved|blocked|retry",
    "pipe_e": "approved|blocked|retry"
  }
}
```

---

## 5) Pipeline V2 (5 pipes oficiais)

## Pipe A - Brief/Refinamento Produto

Objetivo:
- transformar seed em briefing executavel.

Nucleo operacional V2:
- draft_writer (executor)
- PMs paralelos (debate)
- eval_pm por critica
- moderator
- eval_moderator

Gate A:
- briefing coerente
- stories validas
- ready_for_factory true

## Pipe B - Quebra Tecnica

Objetivo:
- decompor briefing em backlog tecnico com contracts e dependencias.

Nucleo operacional V2:
- technical_analyst
- eval_tech_analyst
- architect
- eval_architect
- integration_mapper (+ llm refiner opcional)
- contract_refiner por modulo

Gate B:
- mapping 1:1 modules/build_plan
- task_graph valido
- contracts completos

## Pipe C - Execucao/Desenvolvimento

Objetivo:
- implementar codigo com paralelismo seguro.

Nucleo operacional V2:
- Complexity Router
- pilot builder
- builders paralelos por batch topologico
- code_reviewer
- builder_qa
- quorum architect/judge quando bloqueio real

Gate C:
- modulo aprovado por reviewer + builder_qa
- checks deterministas pass
- falhas abaixo de limite

## Pipe D - Validacao/Testing Dinamica

Objetivo:
- validar release com cobertura precisa e custo controlado.

Nucleo operacional V2:
- Dynamic Test Planner (novo)
- validadores acionados por risco: perf, load, security, resilience, integration, chaos
- eval de cada validador acionado
- qa_consolidator (homologacao)
- judge_final (decisao go/no-go)

Gate D:
- sem blocker critico
- sem contradicao nao resolvida
- homologacao aprovada

## Pipe E - Documentacao

Objetivo:
- documentacao real do sistema aprovado.

Nucleo operacional V2:
- doc_writer
- eval_docs

Gate E:
- docs fieis ao codigo
- sem exposicao sensivel

---

## 6) Simple vs Complex Task Dispatch (novo)

Complexity Score (0-10) por task/modulo:
- +2 se depende de >=3 modulos
- +2 se altera contrato publico
- +2 se mexe em auth, dinheiro, dados sensiveis ou operacao critica
- +1 se ha incerteza de requisito
- +1 se historico de falha semelhante na memoria
- +1 se precisa migracao/compatibilidade
- +1 se envolve concorrencia/assincronia

Roteamento:
- score 0-3: fluxo simples
- score 4-7: fluxo padrao
- score 8-10: fluxo complexo com debate tecnico previo

Fluxo simples:
- 1 builder + 1 reviewer + 1 QA funcional minimo.

Fluxo padrao:
- pilot + 2-4 builders paralelos + reviewer/qa por modulo.

Fluxo complexo:
- debate tecnico curto antes do build
- pilot reforcado
- 4-8 builders max
- validacao expandida orientada por risco

---

## 7) Debate Protocol transversal (novo)

Quando abrir debate:
- incerteza com impacto em arquitetura, custo ou risco.
- conflito entre recomendacoes de agentes.
- duvida nao resolvida por guardrail explicito.

Formato do debate:
- fase 1: proposal (Agente A)
- fase 2: challenge (Agente B)
- fase 3: synthesis (Moderator tecnico)
- fase 4: decision (Coordinator ou Judge Quorum)

Saida obrigatoria do debate:
- opcoes consideradas
- tradeoffs
- decisao final vinculante
- escopo onde a decisao se aplica

Regra anti-ruido:
- max 2 rounds por debate.
- sem nova informacao, encerra com decisao do architect/judge.

---

## 8) Skills dinamicas criadas pelos agentes (novo)

## 8.1 Skill Creation Loop

Trigger para propor skill:
- padrao repetido em >=3 tasks no mesmo run ou em runs diferentes.
- ganho esperado de qualidade/tempo com instrucoes reutilizaveis.

Fluxo:
- skill_candidate_proposer (pode ser Builder/Architect/QA) sugere.
- skill_builder gera rascunho da skill.
- skill_evaluator audita clareza, seguranca e reuso.
- coordinator decide publish/reject.
- skill publicada entra no skill_registry do projeto.

## 8.2 Guardrails para skills dinamicas
- skill nunca sobrepoe guardrail hard.
- skill deve declarar pipe alvo, contexto, limites e exemplos.
- skill sem evidencia de ganho nao e promovida.

## 8.3 Relacao com ARR 102k chars

Quando voce quebrar a arquitetura de referencia, transformar em:
- skills/guardrails-hard
- skills/patterns-recommended
- skills/checklists-by-pipe
- skills/domain-specific
- skills/testing-strategies

Recuperacao de skill no runtime:
- por pipe
- por domain_slug
- por module_role
- por nivel de risco

---

## 9) Validacao precisa sem redundancia (novo)

## 9.1 Principio
- sempre validar o suficiente para risco real.
- nunca repetir validacao equivalente sem novo sinal.

## 9.2 Dynamic Test Planner (DTP)

Decide quais validadores ativar por modulo/lote:
- Performance: quando ha SLA/latencia/throughput, loops de hot path, concorrencia.
- Load: quando ha meta de volume, fila, burst, multicliente.
- Security: quando ha input externo, auth, segredo, dados sensiveis, acao critica.
- Resilience: quando ha dependencia externa, timeout, retry, circuito, fallback.
- Chaos: quando sistema e servico critico e risco operacional alto.
- Integration: sempre que existe depends_on/contratos entre modulos.

Baseline minimo sempre ativo:
- deterministic checks
- code_reviewer
- builder_qa
- integration_validator leve

## 9.3 Deduplicacao de avaliacao
- evaluator audita qualidade do validador, nao repete analise completa.
- consolidator cruza resultados, nao reanalisa codigo.
- judge decide release, nao reexecuta validacao.

## 9.4 Homologacao QA
- QA Consolidator continua obrigatorio.
- Judge Final continua terminal.
- Security critical continua override bloqueante.

---

## 10) Modelo de memoria e contexto entre sessoes

Precedencia obrigatoria:
1. objetivo da run e contrato do usuario
2. guardrails hard (ARR/skills)
3. decisoes locked de arquitetura da run
4. memoria empirica (heuristicas, falhas, anti-patterns)

Persistencias apos cada pipe:
- decisoes fechadas
- riscos residuais
- padroes de falha
- skills candidatas/aprovadas
- evidencias de validacao

Regra:
- memoria nunca revoga guardrail hard.
- mudanca de decisao locked exige debate formal + registro.

---

## 11) API/MCP x CLI subagents (eficiencia real)

Diretriz V2:
- Producao: API v3 + managed child sessions + structured outputs + MCP.
- CLI subagents: piloto controlado para produtividade de operacao assistida.

Quando CLI e eficiente:
- exploracao rapida
- depuracao de fluxo
- operador humano no loop em tempo real

Quando API/MCP e superior:
- repetibilidade
- telemetria
- controle de retries/gates
- auditoria de sessao e custo

Metricas obrigatorias no piloto CLI:
- lead time por pipe
- taxa de sucesso sem intervenção
- custo por run
- retrabalho por falha de contexto

Se CLI ficar >= API/MCP em confiabilidade por 3 ciclos, promover de piloto para trilha oficial secundaria.

---

## 12) Backlog de implementacao V2 (priorizado)

P0:
- consolidar playbooks hibridos (keep/change/drop acima)
- adicionar Complexity Router no coordinator
- adicionar Dynamic Test Planner
- adicionar Debate Protocol transversal
- adicionar Skill Creation Loop

P1:
- implementar skill_registry local e politica de promocao
- integrar Session Context Ledger completo
- adicionar metricas de custo/latencia por tipo de task

P2:
- expandir testes de carga e caos orientados por risco
- ajustar limites adaptativos de paralelismo por historico
- preparar trilha CLI com medicao automatica

---

## 13) Conclusao

A base mais forte para V2 e:
- usar playbooks Claude como motor operacional de execucao e validacao.
- aplicar governanca V1 para separar pipes, controlar qualidade sem redundancia e sustentar evolucao por skills/memory.

Com isso, a V2 atende exatamente o que voce pediu:
- etapas separadas e claras
- tasks simples/complexas roteadas corretamente
- builders em paralelo com controle
- debate entre agentes para decisoes melhores
- criacao e uso de skills durante a execucao
- consulta estruturada a guardrails/skills da arquitetura de referencia
- validacao dinamica e precisa
- coordinator mantendo contexto entre sessoes do inicio ao fim
