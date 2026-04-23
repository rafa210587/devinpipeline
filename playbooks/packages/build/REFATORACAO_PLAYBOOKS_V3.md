# REFATORACAO PLAYBOOKS V3

## O que foi ajustado
- restaurado o bloco opcional `skill_candidate` em todos os playbooks revisados;
- adicionada em todos a secao `Referencias de arquitetura aplicaveis`;
- aumentado o grau de especializacao por papel;
- reduzido o uso de output generico quando o papel pede estrutura mais precisa;
- endurecidos criterios de bloqueio, self-check e prioridade entre fontes.

## Arquivos revisados
- builder.md
- test_builder.md
- code_reviewer.md
- builder_qa.md
- devops_infra_builder.md
- eval_devops_infra.md
- eval_test_builder.md
- judge_quorum.md
- pipeline_build_orchestrator.md
- skill_builder.md
- skill_evaluator.md

## Observacao
A remocao do bloco `skill_candidate` nao foi uma boa decisao para o seu modelo.
No seu desenho, ele funciona como hook transversal para capturar padroes reutilizaveis e alimentar learning/maturidade da factory.
O correto e manter o bloco como opcional, mas com gatilho mais estrito de uso.
