from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

DEFAULT_CONFIG_BASENAME = "factory_config.json"
ENV_CONFIG_PATH = "DEVIN_FACTORY_CONFIG_PATH"
_ENV_VAR_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)\}")

DEFAULT_CONFIG: dict[str, Any] = {
    "devin": {
        "api_base": "https://api.devin.ai",
        "org_id": "",
        "api_key": "",
        "endpoints": {
            "create_session": "/v3/organizations/{org_id}/sessions",
            "get_session": "/v3/organizations/{org_id}/sessions/{session_id}",
            "send_message_candidates": [
                "/v3/organizations/{org_id}/sessions/{session_id}/messages",
            ],
            "terminate_session": "/v3/organizations/{org_id}/sessions/{session_id}",
        },
        "terminate_http_method": "DELETE",
        "terminate_archive": False,
        "terminal_statuses": ["exit", "error", "suspended"],
    },
    "playbooks": {
        "intake": "",
        "brief": "",
        "tech": "",
        "build": "",
        "validate": "",
        "docs": "",
        "learning": "",
    },
    "arr": {
        "url": "",
        "branch": "main",
    },
    "runtime": {
        "poll_interval_seconds": 15,
        "gate_wait_seconds": 1800,
        "waiting_status_details": ["waiting_for_user", "waiting_for_approval"],
        "waiting_detail_timeout_seconds": 1800,
        "session_defaults": {
            "repos": [],
            "knowledge_ids": [],
            "secret_ids": [],
            "bypass_approval": False,
            "use_repo_manifest_as_repos": False,
        },
        "max_wait_seconds": {
            "intake": 1800,
            "brief": 7200,
            "tech": 5400,
            "build": 14400,
            "validate": 7200,
            "docs": 3600,
            "learning": 3600,
        },
        "p0": {
            "enabled": True,
            "default_route_mode": "seed_to_brief",
            "allow_pre_briefed": True,
        },
        "learning": {
            "enabled": False,
            "max_wait_seconds": 3600,
        },
        "tracking": {
            "enabled": True,
            "execution_md": "execution_tracking.md",
            "dilemmas_md": "dilemmas_and_solutions.md",
            "sessions_jsonl": "coordinator_sessions.jsonl",
            "events_jsonl": "tracking_events.jsonl",
        },
        "memory": {
            "enabled": True,
            "episodic_jsonl": "memory/episodic_memory.jsonl",
            "semantic_jsonl": "memory/semantic_memory_candidates.jsonl",
            "summary_md": "memory/MEMORY_LOG.md",
        },
        "human_gates": {
            "after_p1": False,
            "after_p2": False,
            "after_p4": False,
        },
        "transport": {
            "mode": "http",
            "mcp": {
                "base_url": "",
                "tool_call_endpoint": "/tools/call",
                "auth_token": "",
                "payload_mode": "tool_gateway",
                "timeout_seconds": 60,
                "tools": {
                    "create_session": "devin_session_create",
                    "get_session": "devin_session_get",
                    "send_message": "devin_session_interact",
                    "terminate_session": "devin_session_terminate",
                },
            },
        },
        "eval_metrics": {
            "enabled": True,
            "report_mode": "deterministic",
            "json_file": "eval_metrics.json",
            "markdown_file": "eval_metrics_report.md",
            "history_jsonl": "eval_metrics_history.jsonl",
            "ground_truth_file": "eval_ground_truth.json",
            "promote_to_shared": True,
        },
    },
    "storage": {
        "mode": "local",
        "github_repo_path": "",
        "runs_root": "factory_runs",
        "shared_memory_root": "factory_memory",
        "shared_knowledge_root": "factory_knowledge",
        "shared_skills_root": "factory_skills",
        "shared_metrics_root": "factory_metrics",
        "enforce_repo_path": False,
    },
    "git_sync": {
        "enabled": False,
        "auto_commit": False,
        "auto_push": False,
        "branch": "main",
        "commit_message_template": "devin factory run {pipeline} at {ts_utc}",
    },
    "parallel_runner": {
        "default_max_concurrency": 2,
        "pipeline_script": "devin_pipeline_v2.py",
        "logs_dir": "factory_runs/_parallel_logs",
    },
    "references": {
        "skill_registry": "[SKILL/FILE] /workspace/.agents/skills/",
        "arr_reference_index": "[SKILL/FILE] /workspace/architecture-reference/INDEX.md",
        "arr_guardrails": "[SKILL/FILE] /workspace/architecture-reference/guardrails/",
        "arr_patterns": "[SKILL/FILE] /workspace/architecture-reference/patterns/",
        "arr_domain_profiles": "[SKILL/FILE] /workspace/architecture-reference/domains/{domain_slug}.md",
    },
}


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    out = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = _deep_merge(out[key], value)
            continue
        out[key] = value
    return out


def _resolve_env_placeholders(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _resolve_env_placeholders(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_resolve_env_placeholders(v) for v in value]
    if isinstance(value, str):
        return _ENV_VAR_PATTERN.sub(lambda m: os.getenv(m.group(1), ""), value)
    return value


def _default_config_path() -> Path:
    env_path = os.getenv(ENV_CONFIG_PATH)
    if env_path:
        return Path(env_path).expanduser().resolve()
    return (Path(__file__).resolve().parent / DEFAULT_CONFIG_BASENAME)


def load_factory_config(config_path: str | Path | None = None) -> dict[str, Any]:
    chosen_path = (
        Path(config_path).expanduser().resolve()
        if config_path is not None
        else _default_config_path()
    )
    if not chosen_path.exists():
        raise FileNotFoundError(
            f"Arquivo de configuracao nao encontrado: {chosen_path}"
        )

    loaded = json.loads(chosen_path.read_text(encoding="utf-8"))
    merged = _deep_merge(DEFAULT_CONFIG, loaded)
    return _resolve_env_placeholders(merged)
