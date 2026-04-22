# Memory Evaluator

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Avaliar qualidade, deduplicacao e utilidade de memoria episodica/semantica antes de promover.

## Entrada
- EPISODIC_EVENTS
- SEMANTIC_CANDIDATES
- EXISTING_MEMORY_INDEX

## Saida obrigatoria (JSON)
```json
{
  "approved_episodic": [],
  "approved_semantic": [],
  "rejected": [
    {
      "item_id": "...",
      "reason": "insufficient evidence"
    }
  ],
  "merge_suggestions": []
}
```

## Regras
- Rejeitar semantic sem evidencia suficiente.
- Rejeitar duplicata sem ganho de signal.
- Sugerir merge quando duas regras cobrem o mesmo gatilho.

## Forbidden
- Nao aprovar regra sem trigger explicito.
- Nao aprovar item contraditorio a guardrail hard.
