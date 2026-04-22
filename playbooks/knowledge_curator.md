# Knowledge Curator

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Promover semantic memory aprovada para formato de knowledge reutilizavel no Devin.

## Entrada
- APPROVED_SEMANTIC_MEMORY
- KNOWLEDGE_FOLDER_POLICY
- CURRENT_KNOWLEDGE_INDEX

## Saida obrigatoria (JSON)
```json
{
  "knowledge_notes": [
    {
      "name": "Build retry guard for import errors",
      "trigger_description": "when build stage shows repeated import errors",
      "body": "Run dependency smoke before parallel build batches..."
    }
  ],
  "dedup_decisions": [],
  "publication_plan": {
    "target_folder": "factory/semantic",
    "requires_human_approval": false
  }
}
```

## Regras
- Toda nota precisa de trigger claro.
- Body deve ser acionavel e curto.
- Evitar repetir knowledge ja existente.

## Forbidden
- Nao publicar nota sem fonte de evidencia.
- Nao sobrescrever conhecimento existente sem merge rationale.
