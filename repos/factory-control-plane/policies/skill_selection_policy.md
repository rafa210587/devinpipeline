# Skill Selection Policy

Coordinators and subagents must select skills from the factory skill registry and the Devin installed skill root.

## Canonical Sources

1. Devin skill root: `/workspace/.agents/skills/`
2. Factory registry file: `repos/factory-memory-knowledge/skills/skill_registry.json`

## Selection Rules

1. Use the minimum skill set required for the task.
2. Select only skills whose `status` is `active`, unless the coordinator explicitly approves a draft skill.
3. Match skills by `trigger_conditions`, `allowed_stages`, `allowed_roles`, and tags.
4. Prefer repo-local or project-scoped skills for repo-specific procedures.
5. Prefer global/domain skills for reusable workflow, validation, and governance behavior.
6. If two skills conflict, trigger internal debate/quorum before human escalation.
7. Record selected skills in `SubagentTask.selected_skill_refs`.
8. Record new or changed skill candidates in `skill_events.jsonl` and route promotion decisions through P6.

## Do Not

- Do not use this registry as a playbook mirror.
- Do not load draft, disabled, or deprecated skills silently.
- Do not invent a skill path that is not present in the registry or Devin skill root.
- Do not promote a skill without evidence and `promotion_manager` decision.
