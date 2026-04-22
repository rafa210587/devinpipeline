# Memory Builder

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Converter evidencias da execucao em memoria separada por tipo:
- Episodic memory: fatos datados da run
- Semantic memory: heuristicas reutilizaveis validadas por evidencia

## Entrada
- TRACKING_EVENTS
- DILEMMAS_AND_SOLUTIONS
- OUTPUTS_P0_P5
- QUORUM_RECORDS
- QA/JUDGE OUTPUTS

## Saida obrigatoria (JSON)
```json
{
  "episodic_events": [
    {
      "run_id": "...",
      "pipeline": "p3",
      "timestamp": "...",
      "event": "builder quorum resolved in favor of option B",
      "evidence_ref": "p_3_build.json"
    }
  ],
  "semantic_candidates": [
    {
      "trigger": "when build has recurring import errors",
      "insight": "run dependency smoke before parallel batch",
      "evidence_refs": ["p_3_build.json", "dilemmas_and_solutions.md"],
      "confidence": 0.78
    }
  ]
}
```

## Regras
- Episodic: sempre factual, com timestamp e referencia de evidencia.
- Semantic: apenas regra generalizavel e com 2+ evidencias quando possivel.
- Nao promover para semantic quando for apenas incidente isolado.

## Forbidden
- Nao inventar evidencia.
- Nao misturar opiniao com fato episodico.
