# Pipeline Global Orchestrator (Optional)

[SKILL/FILE] SKILL_REGISTRY: /workspace/.agents/skills/
[SKILL/FILE] ARR_REFERENCE_INDEX: /workspace/architecture-reference/INDEX.md
[SKILL/FILE] ARR_GUARDRAILS: /workspace/architecture-reference/guardrails/
[SKILL/FILE] ARR_PATTERNS: /workspace/architecture-reference/patterns/
[SKILL/FILE] ARR_DOMAIN_PROFILE: /workspace/architecture-reference/domains/{domain_slug}.md

## Papel
Orquestrar a cadeia completa P0..P6 dentro de uma sessao Devin quando a operacao optar por coordenacao interna.

## Importante
- Este playbook e opcional.
- O modo oficial continua sendo coordinator externo (`devin_pipeline_v2.py`) + orchestrators por pipeline.

## Fluxo
1. Executar P0 (intake) e decidir rota.
2. Executar P1 (ou pular se pre_briefed).
3. Executar P2 com observability planning.
4. Executar P3 com pilot-then-parallelize.
5. Executar P4 com validacao dinamica por risco.
6. Executar P5 apenas se release aprovado.
7. Executar P6 Learning: context_ledger_updater -> memory_builder -> memory_evaluator -> knowledge_curator -> promotion_manager.

## Quorum e eval
- Em conflito tecnico relevante: abrir quorum (3 papeis) + eval independente.
- Max 2 rounds de debate+eval.

## Saida obrigatoria (JSON)
```json
{
  "status": "completed",
  "pipeline_status": {
    "p0": "completed",
    "p1": "completed",
    "p2": "completed",
    "p3": "completed",
    "p4": "completed",
    "p5": "completed",
    "p6": "completed"
  },
  "release_decision": "approved",
  "tracking_paths": {
    "execution": "execution_tracking.md",
    "dilemmas": "dilemmas_and_solutions.md"
  },
  "memory_paths": {
    "episodic": "memory/episodic_memory.jsonl",
    "semantic": "memory/semantic_memory_candidates.jsonl"
  }
}
```

## Forbidden
- Nao ignorar gate de seguranca critica.
- Nao sobrescrever memoria sem evidencia.
