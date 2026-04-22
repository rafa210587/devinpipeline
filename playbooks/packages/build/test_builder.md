# Test Builder

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Construir testes unitarios e de integracao para UM modulo aprovado em build.

## Entrada
- MODULE_DEF
- CONTRACT
- CODE_REVIEW_OUTPUT
- BUILDER_QA_OUTPUT
- INTEGRATION_MAP[file]
- BRIEFING.stories relevantes

## Procedure
1. Gerar testes unitarios focados em comportamentos do modulo.
2. Gerar testes de integracao para fronteiras declaradas em integration_map.
3. Evitar testes acoplados a detalhe interno instavel.
4. Em retry, corrigir apenas gaps apontados pelo eval.

## Output obrigatorio
```json
{
  "approved_to_merge": true,
  "module_file": "src/example/module.py",
  "test_files": [
    {
      "path": "tests/unit/test_module.py",
      "content": "...",
      "test_type": "unit"
    },
    {
      "path": "tests/integration/test_module_integration.py",
      "content": "...",
      "test_type": "integration"
    }
  ],
  "coverage_targets": {
    "stories_targeted": ["story_01"],
    "contracts_targeted": ["definition_order", "exports"]
  },
  "notes": ""
}
```

## Forbidden
- nao alterar codigo de producao
- nao inventar cenarios fora das stories/contrato sem marcar como extra
