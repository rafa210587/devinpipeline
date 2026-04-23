# Factory Memory And Knowledge

Persistent memory, knowledge, skills registry, and promotion records used by the learning stage and future runs.

## Key Stores

- `memory/`: episodic and semantic memory records.
- `knowledge/`: reusable knowledge candidates.
- `skills/skill_registry.json`: canonical factory-owned index of skills that coordinators and subagents may select.
- `skills/skill_events.jsonl`: append-only skill discovery/evaluation/promotion events.
- `promotions/`: promotion decisions for memory, knowledge, and skills.

## Runtime References

All canonical playbooks expose these stores explicitly:

- `FACTORY_MEMORY_ROOT`: `/workspace/repos/factory-memory-knowledge/memory/`
- `FACTORY_KNOWLEDGE_ROOT`: `/workspace/repos/factory-memory-knowledge/knowledge/`
- `FACTORY_SKILL_REGISTRY`: `/workspace/repos/factory-memory-knowledge/skills/skill_registry.json`

Agents may read these stores as contextual support. Promotion and durable writes should be performed only by the learning/promotion agents or by a coordinator with an explicit handoff contract.
