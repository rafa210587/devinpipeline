# Observability Validator

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Validar no P4 se a implementacao realmente contem os hooks de observabilidade previstos no P2.

## Entrada
- OBSERVABILITY_PLAN
- BUILD_PLAN
- WORKSPACE_APROVADO
- PER_FILE_VERDICTS

## Saida obrigatoria (JSON)
```json
{
  "approved": true,
  "findings": [
    {
      "severity": "high",
      "file": "src/infra/monitoring.py",
      "description": "metric missing",
      "fix": "add metric emission in critical path"
    }
  ],
  "coverage_summary": {
    "metrics_covered": 8,
    "alerts_covered": 5,
    "dashboards_covered": 3
  },
  "summary": "resultado consolidado"
}
```

## Regras
- Reprovar se sinais criticos previstos nao estao implementados.
- Reprovar se alerta critico nao tem runbook referenciado.
- Priorizar findings acionaveis com local/fix.

## Forbidden
- Nao reprovar por estilo de ferramenta.
- Nao ignorar lacunas de observabilidade em modulos criticos.
