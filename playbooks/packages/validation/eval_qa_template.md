# Eval QA Template (V2)

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Auditar qualidade do QA executado (nao refazer analise).

## Entrada
- QA_NAME
- QA_OUTPUT
- INPUTS_QA_RECEBEU
- ARR_PATH
- DTP_PLAN (opcional)

## Regra V2 (DTP-aware)
Se houver DTP_PLAN:
- avaliar somente QAs marcados como required/selected
- nao reprovar por QA nao executado quando marcado como not_required

## Validacoes
1. cobertura do escopo esperado
2. especificidade dos findings
3. calibracao de severidade
4. redundancia interna
5. referencias corretas de guardrail
6. razoabilidade contextual

## Output
```json
{
  "qa_name": "string",
  "approved": true,
  "coverage_ok": true,
  "coverage_issues": [],
  "specificity_issues": [],
  "severity_miscalibrations": [],
  "redundancy_flags": [],
  "guardrail_issues": [],
  "false_positives_suspected": [],
  "overall_quality_score": 0,
  "feedback_for_qa": "string"
}
```

