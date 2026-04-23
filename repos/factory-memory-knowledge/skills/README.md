# Factory Skills Registry

This folder is the canonical factory-owned registry for skills.

It does not duplicate playbooks.

## Canonical Files

- `skill_registry.json`: index of skills available to coordinators and subagents.
- `skill_events.jsonl`: append-only events produced during skill discovery, evaluation, and promotion.

## Runtime Rule

Agents should use two sources together:

1. Devin installed skills: `/workspace/.agents/skills/`
2. Factory registry file: `repos/factory-memory-knowledge/skills/skill_registry.json`

The registry tells agents which skills are active, when to use them, where the actual skill lives, and which roles/stages may use it.
