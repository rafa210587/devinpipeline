# Dynamic Test Planner (DTP)

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Decidir quais validacoes do Pipe D devem ser executadas para cada modulo/lote,
com base em risco real e evitando redundancia.

## Entrada
- BRIEFING
- BUILD_PLAN
- INTEGRATION_MAP
- PER_FILE_VERDICTS (P3)
- PROJECT_MEMORY (opcional)
- CHANGED_MODULES

## Saida obrigatoria (JSON)
```json
{
  "validation_plan": {
    "always": ["integration_light", "qa_consolidator", "judge_final"],
    "by_module": [
      {
        "file": "src/execution/broker.py",
        "risk_score": 9,
        "run": ["security", "resilience", "performance", "load", "chaos", "observability"]
      }
    ]
  },
  "global_reasons": [
    "module has external I/O + money flow + SLA"
  ],
  "dedup_rules": [
    "do not run perf/load on pure utility modules"
  ]
}
```

## Regras
- Integration leve sempre ativa em modulos com depends_on.
- Security ativa se houver input externo, auth, segredo, dados sensiveis ou acao critica.
- Resilience ativa se houver dependencia externa, timeout/retry/fallback, operacao remota.
- Performance ativa se houver SLA/latencia/throughput ou hot path.
- Load ativa quando houver meta de volume/concurrencia/burst.
- Chaos ativa so quando risco operacional alto e sistema critico.
- Observability ativa quando modulo eh critico, tem I/O externo ou SLO declarado.

## Forbidden
- Nao acionar suite completa por padrao sem justificativa.
- Nao deixar modulo critico sem validacao de seguranca.
- Nao repetir validacao equivalente sem novo sinal.
