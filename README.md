# Devin Factory V2 - Agent-First

Este projeto foi migrado para arquitetura agent-first com prompt unico de execucao.

## Ponto de entrada
- `repos/factory-control-plane/prompts/master_pipeline_prompt.md`
- Coordinator inicial central: `Factory Control-Plane Agent`, que opera a sessao raiz e materializa a coordenacao via `pipeline_global_orchestrator`

## Documentacao principal
- `repos/factory-control-plane/docs/DOCUMENTATION_INDEX.md`
- `repos/factory-control-plane/docs/SCHEDULER_AND_DAG.md`
- `repos/PARITY_VALIDATION.md`

## Estrutura de repos internos
- `repos/factory-control-plane`
- `repos/factory-contracts`
- `repos/factory-params`
- `repos/architecture-reference`
- `repos/skills-reference`
- `repos/refinement-support`
- `repos/factory-memory-knowledge`
- `repos/factory-runtime-data`
- `repos/project-target-repos`

## Observacao
O projeto agora assume operacao agent-first. A governanca, os contratos e o runtime canonico vivem em `repos/`.
