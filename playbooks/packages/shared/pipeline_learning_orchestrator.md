# Pipeline P6 Orchestrator - Learning & Promotion

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Orquestrar consolidacao de contexto, memoria e promocao de conhecimento apos P5.

## Modo
`advanced_mode=manage`.

## Entrada
- TRACKING_EVENTS
- DILEMMAS_AND_SOLUTIONS
- OUTPUTS_P0_P5
- QUORUM_RECORDS
- QA_JUDGE_SUMMARY
- PROMOTION_POLICY

## Execucao
1. Spawn `context_ledger_updater`.
2. Spawn `memory_builder`.
3. Spawn `memory_evaluator`.
4. Spawn `knowledge_curator`.
5. Spawn `promotion_manager`.

Se qualquer evaluator reprovar item critico de promocao:
- nao publica item reprovado
- registrar motivo em `rejections`

## Output obrigatorio
```json
{
  "status": "completed",
  "ledger_patch": {},
  "memory_summary": {
    "episodic_count": 0,
    "semantic_candidates_count": 0,
    "semantic_approved_count": 0
  },
  "knowledge_summary": {
    "notes_generated": 0,
    "notes_published": 0
  },
  "promotion_summary": {
    "project_promotions": 0,
    "global_promotions": 0,
    "rejections": 0
  },
  "artifacts": {
    "learning_report": "memory/LEARNING_REPORT.md"
  }
}
```

## Regras
- nenhuma promocao sem trilha de evidencia
- itens com conflito de guardrail hard sao reprovados
- output sempre explicita o que foi aprovado, rejeitado e por que

## Forbidden
- nao sobrescrever conhecimento existente sem rationale de merge
- nao promover itens nao avaliados
