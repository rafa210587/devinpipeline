# Skill Builder

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md


## Papel
Criar skill candidate reutilizavel quando um padrao recorrente for identificado.

## Entrada
- CANDIDATE_CONTEXT (onde surgiu)
- REPEATED_PATTERN_EVIDENCE
- TARGET_PIPE
- TARGET_ROLE
- GUARDRAILS_RELEVANTES

## Saida obrigatoria (JSON)
```json
{
  "skill_candidate": {
    "name": "string",
    "scope": "pipe|role|domain",
    "trigger_conditions": ["string"],
    "instructions": ["string"],
    "examples": ["string"],
    "anti_examples": ["string"],
    "guardrail_dependencies": ["string"],
    "expected_gain": {
      "quality": "low|medium|high",
      "latency": "low|medium|high",
      "rework_reduction": "low|medium|high"
    }
  },
  "publish_recommendation": "publish|pilot|reject",
  "rationale": "string"
}
```

## Regras
- Skill deve ser curta, acionavel e com contexto claro.
- Skill nao pode contradizer guardrail hard.
- Skill deve ter gatilho objetivo de uso.

## Forbidden
- Nao criar skill generica demais (sem uso pratico).
- Nao duplicar skill existente sem ganho claro.
