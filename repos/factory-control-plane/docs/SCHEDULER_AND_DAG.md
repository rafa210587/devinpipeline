# Scheduler And Pipeline DAG - Practical Explanation

## Ownership correto da orquestracao
Existem dois niveis distintos de coordenacao:

1. **Stage orchestration (P0..P6)**  
   Ownership: `pipeline_global_orchestrator`

2. **Module scheduling inside P3 build**  
   Ownership: `pipeline_build_orchestrator` + scheduler policy

O scheduler **nao** decide transicao entre etapas.
Ele so decide ordem segura de execucao de modulos dentro do build.

## Pipeline DAG (stages)
O stage DAG canonico da pipeline inteira e:

`P0 -> P1 -> P2 -> P3 -> P4 -> P5 -> P6`

Regras:
1. Uma etapa so inicia quando a predecessora estiver terminal.
2. Toda etapa terminal gera um `stage_closure_summary` para revisao humana.
3. A proxima etapa so pode iniciar apos aprovacao humana explicita da etapa anterior.
4. `P5` so roda quando `P4.release_decision == approved`; caso contrario, `P5` vira `skipped_release_not_approved`.
5. `P6` e obrigatoria como etapa final de learning e roda apos `P5` concluir ou ser validamente pulada.
6. `resume` inicia do stage escolhido e segue o restante do DAG.
7. O dono dessas transicoes e o `pipeline_global_orchestrator`.

Referencias:
- `workflows/pipeline_dag.json`
- `workflows/resume_map.json`
- `playbooks/packages/shared/pipeline_global_orchestrator.md`

## Bootstrap vs contrato de execucao
- `master_pipeline_prompt.md` serve apenas para bootstrap da sessao raiz.
- O contrato canonico de execucao e o `pipeline_global_orchestrator`.
- O usuario nao deveria precisar colar o master prompt para a pipeline funcionar.
- O root orchestrator e quem apresenta o resumo de cada etapa e coleta a aprovacao antes do proximo stage.

## Scheduler (inside P3 build)
O scheduler lida com tarefas de modulo, nao com stages.

Inputs:
- `build_plan.modules[*].file`
- `build_plan.modules[*].depends_on`

Flow:
1. Montar module DAG a partir de `depends_on`.
2. Validar o grafo:
   - sem arquivos duplicados
   - sem ciclos de dependencia
3. Calcular `ready_queue` (modulos com todas as dependencias concluidas).
4. Despachar modulos prontos ate `max_concurrency`.
5. Regra: um builder subagente trata um modulo por vez.
6. Ao concluir um modulo, liberar dependentes e recalcular a fila.
7. Persistir queue/state para permitir `resume` seguro.

Se uma ambiguidade bloquear um modulo:
1. abrir quorum issue
2. coletar respostas internas
3. o judge decide
4. continuar
5. escalar para humano apenas como ultimo recurso

Referencias:
- `policies/scheduler_policy.md`
- `policies/quorum_and_escalation_policy.md`
- `schemas/envelope/subagent_task.schema.json`
- `schemas/envelope/subagent_result.schema.json`
