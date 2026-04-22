# Context Ledger Updater

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Atualizar ledger de contexto da run com decisoes de debate, quoruns,
skills candidatas/publicadas e fatos importantes para continuidade entre sessoes.

## Entrada
- RUN_ID
- PIPE
- NEW_DECISIONS
- NEW_DEBATES
- NEW_SKILL_EVENTS
- NEW_RISK_NOTES

## Saida obrigatoria (JSON)
```json
{
  "ledger_patch": {
    "decisions_locked": [],
    "debates": [],
    "skills": {
      "candidates": [],
      "published": [],
      "rejected": []
    },
    "risk_notes": [],
    "memory_writeback": []
  },
  "consistency_checks": {
    "conflicts_found": [],
    "requires_manual_review": false
  }
}
```

## Regras
- Cada decisao lock deve ter origem e timestamp.
- Mudanca de decisao lock exige referencia ao debate que aprovou.
- Evento de skill deve registrar status e motivo.

## Forbidden
- Nao sobrescrever decisao lock sem justificativa rastreavel.
- Nao registrar informacao sem fonte do artefato.
