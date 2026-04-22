# Corporate Hardening Explicito (As-Is -> Fix -> Why)

Data: 2026-04-17  
Escopo: deixar `devin_factory_v2_package` pronto para uso corporativo com Devin, com persistencia em repositorio GitHub (clone local).

## 1) Storage corporativo em repo GitHub

Como estava:
- O runtime escrevia em `./output/<slug>/` por padrao.
- Nao havia bloqueio para impedir escrita fora de um repositorio corporativo.

Problema:
- Em ambiente corporativo, rastreabilidade e governanca exigem que artefatos/memoria/knowledge fiquem em repo versionado.

Como foi resolvido:
- Adicionado bloco `storage` em `factory_config.json` e `config_loader.py`.
- Novo modo `storage.mode=github_repo` com `storage.github_repo_path`.
- Escrita default agora resolve para `<repo>/factory_runs/<slug>/`.
- `storage.enforce_repo_path=true` bloqueia escrita fora do repo configurado.

Por que:
- Garante trilha auditavel, backup natural (git) e operacao padronizada em uma unica clone local.

## 2) Sync git opcional automatizado

Como estava:
- O pacote nao executava sync git automatizado.

Problema:
- Equipes podem esquecer `git add/commit/push`, perdendo a consistencia operacional esperada.

Como foi resolvido:
- Adicionado bloco `git_sync` (enabled/auto_commit/auto_push/branch/template).
- Runtime chama `git add` automatico do `output_dir`; commit/push opcionais por config.

Por que:
- Permite evoluir de operacao manual para semiautomatica sem mudar o codigo.

## 3) Handoff de workspace entre etapas

Como estava:
- Handoff era majoritariamente textual via `CONTEXT_HANDOFF_AUTOMATICO`.

Problema:
- Risco de perda de contexto de repositorio/branch entre sessoes.

Como foi resolvido:
- Novo artefato `workspace_handoff.json`.
- Atualizado a cada etapa com:
  - `repo_manifest`
  - `last_pipeline`, `last_status`
  - mapa de artefatos por etapa
- `CONTEXT_HANDOFF_AUTOMATICO` agora incorpora esse handoff.

Por que:
- Reduz ambiguidade e melhora continuidade real entre sessions managed.

## 4) Sessao Devin com defaults corporativos (repos/knowledge/secrets)

Como estava:
- `create_session` usava apenas campos basicos.

Problema:
- Menor controle corporativo para conectar repos/knowledge/secrets e aprovacoes.

Como foi resolvido:
- `create_session` agora suporta: `repos`, `knowledge_ids`, `secret_ids`, `bypass_approval`.
- Novo `runtime.session_defaults` + `stage_overrides` por etapa (`p0..p5`).
- `repo_manifest` de entrada/handoff pode ser injetado em `repos` via flag
  `runtime.session_defaults.use_repo_manifest_as_repos`.

Por que:
- Facilita padronizar politicas corporativas sem hardcode no codigo.

## 5) Polling robusto para estados de espera

Como estava:
- Polling concluia em terminal status ou `running+finished` com output presente.

Problema:
- Sessao podia ficar em `waiting_for_user`/`waiting_for_approval` ate timeout global.

Como foi resolvido:
- Adicionado `runtime.waiting_status_details` e `runtime.waiting_detail_timeout_seconds`.
- Polling agora monitora explicitamente estados de espera e encerra com erro claro ao exceder limite.
- Logs incluem `status_detail`.

Por que:
- Evita deadlocks silenciosos e melhora previsibilidade da automacao.

## 6) Gates P4/P5 mais rigidos

Como estava:
- P4 validava campos, mas podia passar com `status=failed` se campos existissem.
- P5 nao barrava explicitamente `status=failed`.

Problema:
- Risco de continuar pipeline com etapa falha.

Como foi resolvido:
- P4 agora exige `status=completed` para seguir.
- P5 agora exige `status=completed` (quando executado) e falha explicitamente caso contrario.

Por que:
- Garante integridade de release e evita falso positivo de pipeline concluida.

## 7) Memoria/knowledge/skills no repo corporativo

Como estava:
- Memoria era gerada apenas dentro da pasta da run.

Problema:
- Dificulta visao consolidada multi-run para memoria organizacional.

Como foi resolvido:
- Mantida memoria por run.
- Adicionado espelhamento consolidado no repo corporativo:
  - `factory_memory/episodic_memory.jsonl`
  - `factory_memory/semantic_memory_candidates.jsonl`
  - `factory_knowledge/knowledge_candidates.jsonl`
  - `factory_skills/skill_events.jsonl` (quando houver `skill_events` no output)

Por que:
- Permite evolucao continua da base de conhecimento com rastreabilidade unica.

## 8) Ajuste de contrato P0

Como estava:
- Prompt de P0 pedia `observability_plan`.

Problema:
- Divergencia com schema de P0 (responsabilidade real de observabilidade esta em P2).

Como foi resolvido:
- Removida exigencia de `observability_plan` do prompt de P0.

Por que:
- Mantem coesao entre prompt, schema e papel de cada etapa.

## 9) O que ainda e decisao operacional (nao hardcoded)

- Ligar ou nao `git_sync.auto_commit/auto_push`.
- Quais `knowledge_ids`/`secret_ids` usar por etapa.
- Politica de `bypass_approval` por ambiente.
- Modo de consumo de ARR/skills por playbook.

## 10) Checklist rapido de ativacao corporativa

1. Configurar `.env` com `FACTORY_GITHUB_REPO_PATH`, `DEVIN_*`, `PLAYBOOK_*`, `ARR_URL`.
2. Confirmar que `FACTORY_GITHUB_REPO_PATH` aponta para clone git valida.
3. Definir `storage.mode=github_repo` e `storage.enforce_repo_path=true`.
4. Rodar smoke:
   - `python devin_pipeline_v2.py intake ./examples/intake_input.example.json`
5. Verificar arquivos no repo:
   - `factory_runs/<slug>/...`
   - `factory_memory/...`, `factory_knowledge/...`, `factory_skills/...`.
