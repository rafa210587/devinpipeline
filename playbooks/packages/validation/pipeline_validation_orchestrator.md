# Pipeline P4 Orchestrator - Validation (V2)

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Executar validacao dinamica por risco, com homologacao cross-QA e decisao final.

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
- briefing
- build_plan
- integration_map
- per_file_verdicts (P3)
- quorums_logged (P3)
- workspace aprovado

## Execucao

### Passo 0.5 - Debate tecnico + eval independente (condicional)
Se houver conflito relevante entre findings de validadores (ex.: perf x resilience, coverage x risco):
1. Abra debate tecnico com qa_consolidator + validador A + validador B.
2. Registre `quorum_record`.
3. Execute eval independente (agente que nao participou do debate) para auditar a decisao.
4. Se eval reprovar, refaca o debate (max 2 rounds).
5. Se continuar reprovado apos 2 rounds, ABORTE P4: reason="quorum_eval_failed".

### Passo 1 - Preparar contexto consolidado
Gerar bundle do workspace e lista de arquivos para validacao.

### Passo 2 - Dynamic Test Planner (novo)
Spawn `dynamic_test_planner` para decidir validadores por modulo/lote.

Baseline minimo:
- integration (leve) quando ha depends_on
- qa_consolidator
- judge_final

Validadores condicionais por risco:
- security
- resilience
- performance
- load
- chaos
- observability_validator

### Passo 3 - Executar validadores selecionados
Executar em paralelo apenas os validadores marcados pelo DTP.
Mapeamento esperado quando selecionado:
- `load` -> `load_analyst`
- `chaos` -> `chaos_analyst`

### Passo 4 - Eval de cada QA executado
Para cada QA acionado, spawn variante de `eval_qa_template`.
Regra: nao reprovar por QA nao executado quando DTP marcou `not_required`.

### Passo 5 - QA Consolidator (homologacao)
Spawn `qa_consolidator` com:
- resultados de P3
- resultados dos QAs executados
- status dos evals
- quoruns
- plano DTP

### Passo 6 - Architect Final Validator
Spawn `architect_final_validator` para validar aderencia final ao desenho tecnico.

### Passo 7 - Judge Final
Spawn `judge_final` com prioridade para QA Consolidator.
Judge tambem deve considerar resultado do architect_final_validator.
Judge deve respeitar obrigatoriedades do DTP e overrides absolutos:
- security critical bloqueia
- smoke/circular bloqueia

### Passo 8 - Output final
Retornar:
- findings (somente validadores executados)
- evals correspondentes
- qa_consolidator
- architect_final_validator
- judge_verdict
- release_decision
- release_blockers_summary
- dtp_plan_summary
- observability_coverage_summary (quando observability_validator executar)

## Regras
- Nunca executar fanout full por padrao sem justificativa.
- Nunca pular QA Consolidator.
- Nunca pular architect_final_validator.
- Nunca aprovar release com security critical aberto.
- Nunca aprovar com circular dependency ou smoke failed.

