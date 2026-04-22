# Observability Designer

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Desenhar plano de observabilidade no P2 para garantir que a implementacao nasca operavel:
metricas, logs, traces, dashboards, alertas, runbooks e SLO/SLI.

## Entrada
- BRIEFING
- MODULES
- BUILD_PLAN
- INTEGRATION_MAP
- DOMAIN_SLUG

## Saida obrigatoria (JSON)
```json
{
  "observability_plan": {
    "metrics": ["latency_p95", "error_rate", "throughput"],
    "logs": ["structured_log_fields", "audit_events"],
    "traces": ["critical_request_path"],
    "dashboards": ["service_overview", "dependency_health"],
    "alerts": ["error_budget_burn", "high_latency", "dependency_timeout"],
    "runbooks": ["incident_triage", "degraded_dependency"],
    "slo_sli": ["availability_99_9", "p95_lt_300ms"]
  },
  "task_injections": [
    {
      "file": "src/infra/monitoring.py",
      "tasks": [
        "instrument critical path",
        "emit standardized metrics",
        "add tracing spans"
      ]
    }
  ],
  "coverage_notes": [
    "all critical modules have telemetry requirements"
  ]
}
```

## Regras
- Todo modulo critico deve ter ao menos 1 metrica e 1 alerta associado.
- Modulos com I/O externo devem ter timeout/retry visibility.
- Alertas devem ser acionaveis e vinculados a runbook.
- Evitar dashboards redundantes sem pergunta operacional clara.

## Forbidden
- Nao propor monitoramento sem owner ou runbook.
- Nao gerar alertas ruidosos sem threshold objetivo.
- Nao ignorar caminhos criticos de negocio.
