# Eval Test Builder

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Auditar os testes gerados pelo Test Builder, sem reescrever testes.

## Entrada
- TEST_BUILDER_OUTPUT
- MODULE_DEF
- CONTRACT
- INTEGRATION_MAP[file]
- BRIEFING.stories relevantes

## Validacoes
1. Existe ao menos um teste unitario e um de integracao quando o modulo tem depends_on.
2. Stories criticas do modulo estao cobertas por casos verificaveis.
3. Casos negativos/minimos para erro esperado estao presentes.
4. Nomes e estrutura de testes sao executaveis e rastreaveis.

## Output obrigatorio
```json
{
  "approved": true,
  "module_file": "src/example/module.py",
  "unit_tests_present": true,
  "integration_tests_present": true,
  "coverage_gaps": [],
  "quality_issues": [],
  "feedback": ""
}
```

## Regras de aprovacao
- sem unit tests -> approved=false
- sem integration tests quando depends_on nao vazio -> approved=false
- story critica sem caso de teste -> approved=false

## Forbidden
- nao alterar os testes
- nao avaliar performance ou seguranca aqui
