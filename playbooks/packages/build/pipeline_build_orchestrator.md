# Pipeline P3 Orchestrator - Build (V2)

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Orquestrar implementacao com estrategia pilot-then-parallelize, usando
roteamento de complexidade para suportar tasks simples e complexas.

## Modo
`advanced_mode=manage`.


## Politica global de decisao (obrigatoria)
- Em qualquer duvida real de definicao, abra quorum.
- Quorum minimo: 3 agentes com papeis diferentes (owner da etapa + builder lead + qa lead).
- Todo quorum deve gerar `quorum_record` com pergunta, opcoes, decisao, racional e escopo de impacto.
- Todo debate tecnico exige eval por agente independente (que nao participou do debate).
- Se eval reprovar, repetir debate com feedback do eval (max 2 rounds).
- Se houver duvida sem quorum+eval, a etapa e invalida.

## Entradas
- TASKS.md
- build_plan
- integration_map
- contracts
- briefing
- project_memory (opcional)

## Execucao

### Passo 0 - Complexity Router (novo)
Para cada modulo, calcular `complexity_score` (0-10):
- +2 altera contrato publico
- +2 auth/dinheiro/dado sensivel/operacao critica
- +2 depende de >=3 modulos
- +1 concorrencia/async
- +1 historico de falha similar
- +1 incerteza de requisito
- +1 migracao/compatibilidade

Roteamento:
- 0-3: caminho simples
- 4-7: caminho padrao
- 8-10: caminho complexo

### Passo 0.5 - Debate tecnico + eval independente (condicional)
Se houver duvida real em roteamento de complexidade, fronteira de modulo ou estrategia de implementacao:
1. Abra debate tecnico com architect + builder lead + qa lead.
2. Registre `quorum_record`.
3. Execute eval independente (preferencialmente `eval_qa_template` ou `code_reviewer`) sobre a decisao debatida.
4. Se eval reprovar, refaca o debate (max 2 rounds).
5. Se continuar reprovado apos 2 rounds, ABORTE P3: reason="quorum_eval_failed".

### Passo 1 - Pilot build (role-aware)
Escolher modulo piloto com menor dependencia e risco controlado.
Roteamento por tipo:
- se module_role=`infrastructure`: spawn `devops_infra_builder`
- caso contrario: spawn `builder`

### Passo 2 - Validacao do piloto
Loop ate aprovar ou abortar:
1. deterministic checks (compile, ast, placeholders, exports, smoke)
2. `code_reviewer`
3. `builder_qa`
4. `test_builder`
5. `eval_test_builder`
6. se for modulo de infra: `eval_devops_infra`

Se `builder.status=blocked` ou `devops_infra_builder.status=blocked`, abrir quorum:
- `architect` modo quorum
- se houver divergencia, `judge_quorum`

### Passo 3 - Parallel build
Apenas apos piloto aprovado.
Executar batches topologicos:
- simples: 1 builder por modulo
- padrao: 2-4 builders simultaneos
- complexo: debate tecnico curto antes + 4-8 builders max

Cada modulo repete o mesmo gate:
- deterministic checks -> code_reviewer -> builder_qa -> test_builder -> eval_test_builder
- modulos de infra tambem passam por eval_devops_infra

### Passo 4 - Skill candidate hook (novo)
Ao aprovar cada modulo, aceitar `skill_candidate` opcional do builder.
Se houver:
1. spawn `skill_builder`
2. spawn `skill_evaluator`
3. registrar evento em ledger (publish|pilot|reject)

### Passo 5 - Output final
Retornar structured_output com:
- status
- per_file_verdicts
- failed_files
- pilot_file
- quorums_logged
- tier_stats
- error_type_histogram
- test_evidence_summary
- skill_events (opcional)

## Regras
- Nunca paralelizar antes do piloto.
- Nunca pular deterministic checks antes de reviewer.
- Nunca concluir modulo sem test_builder + eval_test_builder.
- Nunca concluir modulo de infra sem eval_devops_infra.
- Nunca ignorar decisao de quorum.
- Nunca concluir sem reportar arquivos falhos.

## Failure modes
- piloto falha apos limite de tentativas -> abort pipeline
- builder travado > 45 min -> encerrar sessao e marcar modulo failed
- circular dependency confirmada -> abort

