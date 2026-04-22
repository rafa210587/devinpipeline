"""
schemas.py — JSON Schemas para structured_output das pipelines Devin.

Todos os schemas seguem JSON Schema Draft 7 conforme exigido pela API v3
do Devin (parâmetro structured_output_schema em create_session).
"""

# =======================================================================
# PIPELINE P0 - Intake & Prompt Optimization
# =======================================================================

P0_OUTPUT_SCHEMA = {
    "type": "object",
    "required": [
        "status",
        "route_mode",
        "normalized_prompt",
        "project_context",
        "intake_contract",
    ],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed"]},
        "route_mode": {
            "type": "string",
            "enum": ["seed_to_brief", "pre_briefed"],
        },
        "normalized_prompt": {"type": "string"},
        "normalized_briefing": {"type": "object"},
        "project_context": {
            "type": "object",
            "required": ["slug", "repo_manifest"],
            "properties": {
                "slug": {"type": "string"},
                "domain_slug": {"type": "string"},
                "repo_manifest": {
                    "type": "array",
                    "minItems": 1,
                    "items": {
                        "type": "object",
                        "required": ["name", "url", "branch", "role", "access"],
                        "properties": {
                            "name": {"type": "string"},
                            "url": {"type": "string"},
                            "branch": {"type": "string"},
                            "role": {
                                "type": "string",
                                "enum": ["reference", "target", "support"],
                            },
                            "access": {
                                "type": "string",
                                "enum": ["read_only", "write"],
                            },
                        },
                    },
                },
            },
        },
        "intake_contract": {
            "type": "object",
            "required": ["entry_mode", "next_pipeline", "constraints", "assumptions"],
            "properties": {
                "entry_mode": {
                    "type": "string",
                    "enum": ["seed", "briefing_ready"],
                },
                "next_pipeline": {
                    "type": "string",
                    "enum": ["brief", "tech"],
                },
                "constraints": {"type": "array", "items": {"type": "string"}},
                "assumptions": {"type": "array", "items": {"type": "string"}},
                "open_questions": {"type": "array", "items": {"type": "string"}},
            },
        },
        "evaluator_verdict": {
            "type": "object",
            "properties": {
                "approved": {"type": "boolean"},
                "feedback": {"type": "string"},
            },
        },
        "quorum_record": {
            "type": "object",
            "properties": {
                "question": {"type": "string"},
                "decision": {"type": "string"},
                "rationale": {"type": "string"},
            },
        },
        "reason": {"type": "string"},
    },
}


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE P1 — Brief & Refinement
# ═══════════════════════════════════════════════════════════════════════

STORY_SCHEMA = {
    "type": "object",
    "required": ["id", "title", "context", "behavior", "acceptance"],
    "properties": {
        "id": {"type": "string"},
        "title": {"type": "string"},
        "context": {"type": "string", "minLength": 60},
        "behavior": {"type": "string", "minLength": 60},
        "acceptance": {
            "type": "array",
            "minItems": 3,
            "maxItems": 5,
            "items": {"type": "string"},
        },
    },
}

BRIEFING_SCHEMA = {
    "type": "object",
    "required": ["name", "slug", "profile", "description", "goals",
                 "requirements", "stories"],
    "properties": {
        "name": {"type": "string"},
        "slug": {"type": "string"},
        "profile": {"type": "string"},
        "description": {"type": "string"},
        "goals": {"type": "array", "items": {"type": "string"}, "minItems": 1},
        "users": {"type": "array", "items": {"type": "string"}},
        "requirements": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 1,
        },
        "stories": {
            "type": "array",
            "items": STORY_SCHEMA,
            "minItems": 6,
        },
        "constraints": {"type": "array", "items": {"type": "string"}},
        "domain_rules": {"type": "object"},
        "non_functional": {"type": "object"},
        "open_questions": {"type": "array", "items": {"type": "string"}},
    },
}

DRAFT_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["briefing"],
    "properties": {"briefing": BRIEFING_SCHEMA},
}

CRITIQUE_SCHEMA = {
    "type": "object",
    "required": ["pm_id", "round", "critique", "critical_issues",
                 "improvements", "questions"],
    "properties": {
        "pm_id": {"type": "string"},
        "pm_label": {"type": "string"},
        "round": {"type": "integer", "minimum": 1},
        "critique": {"type": "string"},
        "critical_issues": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 10,
        },
        "improvements": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 10,
        },
        "questions": {
            "type": "array",
            "items": {"type": "string"},
            "maxItems": 10,
        },
    },
}

EVAL_CRITIQUE_SCHEMA = {
    "type": "object",
    "required": ["pm_id", "approved", "specificity_score"],
    "properties": {
        "pm_id": {"type": "string"},
        "approved": {"type": "boolean"},
        "rejection_reason": {"type": "string"},
        "specificity_score": {"type": "integer", "minimum": 0, "maximum": 10},
        "redundancy_flags": {"type": "array", "items": {"type": "string"}},
        "actionability_score": {"type": "integer", "minimum": 0, "maximum": 10},
        "out_of_scope_questions": {"type": "array", "items": {"type": "string"}},
        "role_violations": {"type": "array", "items": {"type": "string"}},
        "summary": {"type": "string"},
        "feedback_for_pm": {"type": "string"},
    },
}

MODERATOR_VERDICT_SCHEMA = {
    "type": "object",
    "required": ["executive_summary", "critical_issues_consolidated",
                 "ready_for_factory", "refined_briefing"],
    "properties": {
        "executive_summary": {"type": "string"},
        "critical_issues_consolidated": {
            "type": "array",
            "items": {"type": "string"},
        },
        "changes_made": {"type": "array", "items": {"type": "string"}},
        "changes_rejected": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["change", "reason"],
                "properties": {
                    "change": {"type": "string"},
                    "reason": {"type": "string"},
                },
            },
        },
        "ready_for_factory": {"type": "boolean"},
        "refined_briefing": BRIEFING_SCHEMA,
    },
}

EVAL_MODERATOR_SCHEMA = {
    "type": "object",
    "required": ["approved", "decisions_preserved", "completeness_ok"],
    "properties": {
        "approved": {"type": "boolean"},
        "critical_issues_coverage": {"type": "array"},
        "decisions_preserved": {"type": "boolean"},
        "decisions_lost": {"type": "array", "items": {"type": "string"}},
        "story_quality_issues": {"type": "array"},
        "consistency_issues": {"type": "array", "items": {"type": "string"}},
        "moderator_rules_violated": {"type": "array", "items": {"type": "string"}},
        "completeness_ok": {"type": "boolean"},
        "feedback": {"type": "string"},
    },
}

P1_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["status", "briefing", "ready_for_factory"],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed", "degraded"]},
        "briefing": BRIEFING_SCHEMA,
        "debate_rounds": {"type": "array"},
        "evals_summary": {"type": "object"},
        "moderator_output": {"type": "object"},
        "ready_for_factory": {"type": "boolean"},
        "reason": {"type": "string"},
    },
}


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE P2 — Technical Decomposition
# ═══════════════════════════════════════════════════════════════════════

MODULE_SCHEMA = {
    "type": "object",
    "required": ["file", "description", "module_role", "classes",
                 "standalone_functions", "depends_on", "stories_covered"],
    "properties": {
        "file": {"type": "string"},
        "description": {"type": "string"},
        "module_role": {
            "type": "string",
            "enum": ["strategy", "execution", "risk", "io", "scheduling",
                     "utilities", "api", "domain", "model", "infrastructure"],
        },
        "classes": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "description"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        },
        "standalone_functions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "description"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        },
        "depends_on": {"type": "array", "items": {"type": "string"}},
        "stories_covered": {"type": "array", "items": {"type": "string"}},
    },
}

MODULES_SCHEMA = {
    "type": "object",
    "required": ["modules", "total_modules", "coverage_report"],
    "properties": {
        "modules": {
            "type": "array",
            "items": MODULE_SCHEMA,
            "minItems": 1,
        },
        "total_modules": {"type": "integer"},
        "coverage_report": {
            "type": "object",
            "required": ["stories_total", "stories_covered_ids",
                         "stories_uncovered"],
            "properties": {
                "stories_total": {"type": "integer"},
                "stories_covered_ids": {"type": "array", "items": {"type": "string"}},
                "stories_uncovered": {"type": "array", "items": {"type": "string"}},
            },
        },
        "shared_infrastructure": {"type": "array"},
        "notes": {"type": "string"},
    },
}

EVAL_MODULES_SCHEMA = {
    "type": "object",
    "required": ["approved"],
    "properties": {
        "approved": {"type": "boolean"},
        "coverage_gaps": {"type": "array"},
        "overlap_issues": {"type": "array"},
        "granularity_issues": {"type": "array", "items": {"type": "string"}},
        "catchall_modules": {"type": "array"},
        "explicit_separation_violated": {"type": "array"},
        "role_inconsistencies": {"type": "array"},
        "dependency_issues": {"type": "array"},
        "role_distribution_issue": {"type": ["string", "null"]},
        "feedback": {"type": "string"},
    },
}

BUILD_PLAN_MODULE_SCHEMA = {
    "type": "object",
    "required": ["file", "description", "classes", "standalone_functions",
                 "depends_on"],
    "properties": {
        "file": {"type": "string"},
        "description": {"type": "string"},
        "module_role": {"type": "string"},
        "classes": {"type": "array"},
        "standalone_functions": {"type": "array"},
        "depends_on": {"type": "array", "items": {"type": "string"}},
        "stories_covered": {"type": "array", "items": {"type": "string"}},
        "build_order_hint": {"type": "integer"},
        "design_decisions": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["decision", "rationale"],
                "properties": {
                    "decision": {"type": "string"},
                    "rationale": {"type": "string"},
                },
            },
        },
    },
}

BUILD_PLAN_SCHEMA = {
    "type": "object",
    "required": ["spec_md", "build_plan"],
    "properties": {
        "spec_md": {"type": "string"},
        "build_plan": {
            "type": "object",
            "required": ["modules", "build_order"],
            "properties": {
                "project_name": {"type": "string"},
                "modules": {
                    "type": "array",
                    "items": BUILD_PLAN_MODULE_SCHEMA,
                    "minItems": 1,
                },
                "design_decisions": {"type": "array"},
                "build_order": {"type": "array", "items": {"type": "string"}},
            },
        },
    },
}

EVAL_BUILD_PLAN_SCHEMA = {
    "type": "object",
    "required": ["approved", "mapping_1_to_1"],
    "properties": {
        "approved": {"type": "boolean"},
        "mapping_1_to_1": {"type": "boolean"},
        "mapping_issues": {"type": "array"},
        "attribute_preservation_issues": {"type": "array"},
        "design_decision_issues": {"type": "array"},
        "build_order_issues": {"type": "array"},
        "spec_coherence_issues": {"type": "array"},
        "domain_rules_missing": {"type": "array", "items": {"type": "string"}},
        "feedback": {"type": "string"},
    },
}

INTEGRATION_MAP_SCHEMA = {
    "type": "object",
    "required": ["files"],
    "properties": {
        "files": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "properties": {
                    "exports": {"type": "array", "items": {"type": "string"}},
                    "imports_from": {"type": "array", "items": {"type": "string"}},
                    "inferred_dependencies": {"type": "array", "items": {"type": "string"}},
                    "required_by": {"type": "array", "items": {"type": "string"}},
                    "smoke_targets": {"type": "array", "items": {"type": "string"}},
                    "notes": {"type": "string"},
                },
            },
        },
        "global_notes": {"type": "array", "items": {"type": "string"}},
    },
}

CONTRACT_SCHEMA = {
    "type": "object",
    "required": ["file", "module_summary"],
    "properties": {
        "file": {"type": "string"},
        "module_summary": {"type": "string"},
        "definition_order": {"type": "array", "maxItems": 6, "items": {"type": "string"}},
        "required_globals": {"type": "array", "maxItems": 4, "items": {"type": "string"}},
        "required_helpers": {"type": "array", "maxItems": 5, "items": {"type": "string"}},
        "small_classes": {"type": "array", "maxItems": 4, "items": {"type": "string"}},
        "allowed_external_imports": {"type": "array", "maxItems": 5, "items": {"type": "string"}},
        "integration_points": {"type": "array", "maxItems": 4, "items": {"type": "string"}},
        "build_notes": {"type": "array", "maxItems": 6, "items": {"type": "string"}},
        "test_focus": {"type": "array", "maxItems": 5, "items": {"type": "string"}},
    },
}

P2_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["status", "tasks_md", "build_plan", "integration_map",
                 "contracts", "observability_plan"],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed"]},
        "tasks_md": {"type": "string"},
        "build_plan": {"type": "object"},
        "integration_map": {"type": "object"},
        "contracts": {"type": "object"},
        "observability_plan": {
            "type": "object",
            "properties": {
                "metrics": {"type": "array", "items": {"type": "string"}},
                "logs": {"type": "array", "items": {"type": "string"}},
                "traces": {"type": "array", "items": {"type": "string"}},
                "dashboards": {"type": "array", "items": {"type": "string"}},
                "alerts": {"type": "array", "items": {"type": "string"}},
                "runbooks": {"type": "array", "items": {"type": "string"}},
                "slo_sli": {"type": "array", "items": {"type": "string"}},
            },
        },
        "modules": {"type": "object"},
        "tech_analyst_eval": {"type": "object"},
        "architect_eval": {"type": "object"},
        "reason": {"type": "string"},
    },
}


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE P3 — Build
# ═══════════════════════════════════════════════════════════════════════

BUILDER_OUTPUT_SCHEMA = {
    "oneOf": [
        {
            "type": "object",
            "required": ["status", "module_file", "content"],
            "properties": {
                "status": {"type": "string", "enum": ["done"]},
                "module_file": {"type": "string"},
                "content": {"type": "string"},
                "notes": {"type": "string"},
                "correction_notes": {"type": "string"},
                "self_check": {"type": "object"},
                "stories_addressed": {"type": "array"},
            },
        },
        {
            "type": "object",
            "required": ["status", "question", "context", "my_position"],
            "properties": {
                "status": {"type": "string", "enum": ["blocked"]},
                "task_id": {"type": "string"},
                "question": {"type": "string"},
                "context": {"type": "string"},
                "my_position": {"type": "string"},
                "why_blocking": {"type": "string"},
            },
        },
    ],
}

CODE_REVIEW_SCHEMA = {
    "type": "object",
    "required": ["approved", "file"],
    "properties": {
        "approved": {"type": "boolean"},
        "file": {"type": "string"},
        "module_def_coverage": {"type": "array"},
        "contract_compliance": {"type": "object"},
        "integration_compliance": {"type": "object"},
        "quorum_decisions_followed": {"type": "array"},
        "architectural_issues": {"type": "array"},
        "story_coverage_signal": {"type": "object"},
        "feedback": {"type": "string"},
    },
}

BUILDER_QA_SCHEMA = {
    "type": "object",
    "required": ["approved", "file", "overall_status"],
    "properties": {
        "approved": {"type": "boolean"},
        "file": {"type": "string"},
        "stories_coverage": {"type": "array"},
        "overall_status": {
            "type": "string",
            "enum": ["complete", "partial", "missing"],
        },
        "overall_summary": {"type": "string"},
        "feedback": {"type": "string"},
    },
}

QUORUM_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["mode", "position", "reasoning", "agrees_with_builder"],
    "properties": {
        "mode": {"type": "string", "enum": ["quorum_response"]},
        "position": {"type": "string"},
        "reasoning": {"type": "string"},
        "guardrail_reference": {"type": "string"},
        "agrees_with_builder": {"type": "boolean"},
        "alternative_proposed": {"type": ["string", "null"]},
    },
}

JUDGE_QUORUM_SCHEMA = {
    "type": "object",
    "required": ["quorum_id", "decision", "reasoning", "decided_in_favor_of",
                 "binding"],
    "properties": {
        "quorum_id": {"type": "string"},
        "decision": {"type": "string"},
        "reasoning": {"type": "string"},
        "decided_in_favor_of": {
            "type": "string",
            "enum": ["builder", "architect", "neutral"],
        },
        "guardrail_reference": {"type": "string"},
        "task_criterion_supported": {"type": "string"},
        "applies_to": {"type": "array", "items": {"type": "string"}},
        "alternative_considered_and_rejected": {"type": "object"},
        "binding": {"type": "boolean"},
    },
}

P3_OUTPUT_SCHEMA = {
    "type": "object",
    "required": [
        "status",
        "per_file_verdicts",
        "failed_files",
        "test_evidence_summary",
    ],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed"]},
        "per_file_verdicts": {"type": "array"},
        "failed_files": {"type": "array", "items": {"type": "string"}},
        "pilot_file": {"type": "string"},
        "quorums_logged": {"type": "array"},
        "tier_stats": {"type": "object"},
        "error_type_histogram": {"type": "object"},
        "test_evidence_summary": {"type": "object"},
        "reason": {"type": "string"},
    },
}


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE P4 — Validation
# ═══════════════════════════════════════════════════════════════════════

FINDING_SCHEMA = {
    "type": "object",
    "required": ["finding_id", "severity", "category", "file", "location",
                 "description", "fix"],
    "properties": {
        "finding_id": {"type": "string"},
        "severity": {
            "type": "string",
            "enum": ["critical", "high", "medium", "low"],
        },
        "category": {"type": "string"},
        "file": {"type": "string"},
        "location": {"type": "string"},
        "description": {"type": "string"},
        "fix": {"type": "string"},
        "guardrail_reference": {"type": "string"},
        "estimated_impact": {"type": "string"},
    },
}

PERF_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "findings"],
    "properties": {
        "approved": {"type": "boolean"},
        "files_analyzed": {"type": "integer"},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "summary": {"type": "string"},
    },
}

RESILIENCE_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "findings"],
    "properties": {
        "approved": {"type": "boolean"},
        "files_analyzed": {"type": "integer"},
        "external_dependencies_identified": {"type": "array"},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "summary": {"type": "string"},
        "positive_observations": {"type": "array"},
    },
}

PR_VALIDATOR_SCHEMA = {
    "type": "object",
    "required": ["approved", "performance_approved", "resilience_approved"],
    "properties": {
        "approved": {"type": "boolean"},
        "performance_approved": {"type": "boolean"},
        "resilience_approved": {"type": "boolean"},
        "conflicts_detected": {"type": "array"},
        "consolidated_high_findings": {"type": "array"},
        "overall_feedback": {"type": "string"},
    },
}

INTEGRATION_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "pairs_checked", "smoke_results"],
    "properties": {
        "approved": {"type": "boolean"},
        "pairs_checked": {"type": "array"},
        "inconsistencies": {"type": "array"},
        "circular_dependencies": {"type": "array"},
        "undeclared_dependencies": {"type": "array"},
        "workspace_vs_plan": {"type": "object"},
        "smoke_results": {"type": "array"},
        "summary": {"type": "string"},
    },
}

SECURITY_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "scope_reviewed", "findings"],
    "properties": {
        "approved": {"type": "boolean"},
        "scope_reviewed": {"type": "array", "items": {"type": "string"}},
        "dependency_scan": {"type": "object"},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "summary": {"type": "string"},
    },
}

LOAD_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "files_analyzed", "findings", "summary"],
    "properties": {
        "approved": {"type": "boolean"},
        "files_analyzed": {"type": "integer"},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "summary": {"type": "string"},
    },
}

CHAOS_FINDINGS_SCHEMA = {
    "type": "object",
    "required": ["approved", "files_analyzed", "findings", "summary"],
    "properties": {
        "approved": {"type": "boolean"},
        "files_analyzed": {"type": "integer"},
        "findings": {"type": "array", "items": FINDING_SCHEMA},
        "summary": {"type": "string"},
        "experiment_suggestions": {"type": "array", "items": {"type": "string"}},
    },
}

ARCHITECT_FINAL_VALIDATION_SCHEMA = {
    "type": "object",
    "required": ["approved", "architecture_alignment_score"],
    "properties": {
        "approved": {"type": "boolean"},
        "architecture_alignment_score": {"type": "integer", "minimum": 0, "maximum": 10},
        "critical_mismatches": {"type": "array"},
        "non_critical_mismatches": {"type": "array"},
        "quorum_adherence_issues": {"type": "array"},
        "residual_architecture_risks": {"type": "array", "items": {"type": "string"}},
        "feedback": {"type": "string"},
    },
}

EVAL_QA_SCHEMA = {
    "type": "object",
    "required": ["qa_name", "approved", "overall_quality_score"],
    "properties": {
        "qa_name": {"type": "string"},
        "approved": {"type": "boolean"},
        "coverage_ok": {"type": "boolean"},
        "coverage_issues": {"type": "array"},
        "specificity_issues": {"type": "array"},
        "severity_miscalibrations": {"type": "array"},
        "redundancy_flags": {"type": "array"},
        "guardrail_issues": {"type": "array"},
        "false_positives_suspected": {"type": "array"},
        "overall_quality_score": {"type": "integer", "minimum": 0, "maximum": 10},
        "feedback_for_qa": {"type": "string"},
    },
}

QA_CONSOLIDATOR_SCHEMA = {
    "type": "object",
    "required": ["approved", "overall_assessment"],
    "properties": {
        "approved": {"type": "boolean"},
        "overall_assessment": {
            "type": "string",
            "enum": ["all_covered", "gaps_present", "critical_gaps"],
        },
        "story_coverage_gaps": {"type": "array"},
        "module_coverage_gaps": {"type": "array"},
        "contradictions": {"type": "array"},
        "quorum_coverage_gaps": {"type": "array"},
        "systemic_gaps": {"type": "array"},
        "qa_trust_flags": {"type": "array"},
        "critical_gaps_summary": {"type": "array", "items": {"type": "string"}},
        "recommendations_for_judge": {"type": "array", "items": {"type": "string"}},
    },
}

JUDGE_FINAL_SCHEMA = {
    "type": "object",
    "required": ["approved", "score", "scores_by_dimension", "reasoning"],
    "properties": {
        "approved": {"type": "boolean"},
        "score": {"type": "number", "minimum": 0, "maximum": 10},
        "scores_by_dimension": {
            "type": "object",
            "required": ["task_completeness", "architectural_coherence",
                         "test_adequacy", "operational_readiness",
                         "security_posture", "executability"],
            "properties": {
                "task_completeness": {"type": "integer", "minimum": 0, "maximum": 10},
                "architectural_coherence": {"type": "integer", "minimum": 0, "maximum": 10},
                "test_adequacy": {"type": "integer", "minimum": 0, "maximum": 10},
                "operational_readiness": {"type": "integer", "minimum": 0, "maximum": 10},
                "security_posture": {"type": "integer", "minimum": 0, "maximum": 10},
                "executability": {"type": "integer", "minimum": 0, "maximum": 10},
            },
        },
        "release_blockers": {"type": "array"},
        "residual_risks": {"type": "array", "items": {"type": "string"}},
        "reasoning": {"type": "string"},
        "qa_consolidator_respected": {"type": "boolean"},
        "summary": {"type": "string"},
    },
}

P4_OUTPUT_SCHEMA = {
    "type": "object",
    "required": [
        "status",
        "qa_consolidator",
        "architect_final_validator",
        "judge_verdict",
        "release_decision",
        "release_blockers_summary",
    ],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed"]},
        "findings": {"type": "object"},
        "evals": {"type": "object"},
        "qa_consolidator": QA_CONSOLIDATOR_SCHEMA,
        "architect_final_validator": ARCHITECT_FINAL_VALIDATION_SCHEMA,
        "judge_verdict": JUDGE_FINAL_SCHEMA,
        "quorums_p4": {"type": "array"},
        "release_decision": {
            "type": "string",
            "enum": ["approved", "blocked"],
        },
        "release_blockers_summary": {"type": "array"},
    },
}


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE P5 — Documentation
# ═══════════════════════════════════════════════════════════════════════

DOC_WRITER_SCHEMA = {
    "type": "object",
    "required": ["files"],
    "properties": {
        "files": {
            "type": "object",
            "required": ["README", "ARCHITECTURE"],
            "properties": {
                "README": {"type": "string"},
                "ARCHITECTURE": {"type": "string"},
                "RUNBOOK": {"type": "string"},
            },
        },
        "generated_sections": {"type": "object"},
        "notes": {"type": "string"},
        "items_skipped": {"type": "array"},
    },
}

EVAL_DOCS_SCHEMA = {
    "type": "object",
    "required": ["approved", "overall_quality_score"],
    "properties": {
        "approved": {"type": "boolean"},
        "false_claims": {"type": "array"},
        "missing_sections": {"type": "array"},
        "sensitive_info_exposed": {"type": "array"},
        "language_issues": {"type": "array"},
        "private_api_exposed": {"type": "array"},
        "overall_quality_score": {"type": "integer", "minimum": 0, "maximum": 10},
        "feedback_for_doc_writer": {"type": "string"},
    },
}

P5_OUTPUT_SCHEMA = {
    "type": "object",
    "required": ["status"],
    "properties": {
        "status": {
            "type": "string",
            "enum": ["completed", "skipped", "failed"],
        },
        "docs_generated": {"type": "array", "items": {"type": "string"}},
        "doc_paths": {"type": "object"},
        "eval_docs_passed": {"type": "boolean"},
        "pipeline_complete": {"type": "boolean"},
        "reason": {"type": "string"},
        "note": {"type": "string"},
    },
}


# =======================================================================
# PIPELINE P6 - Learning & Promotion
# =======================================================================

P6_OUTPUT_SCHEMA = {
    "type": "object",
    "required": [
        "status",
        "ledger_patch",
        "memory_summary",
        "knowledge_summary",
        "promotion_summary",
        "artifacts",
    ],
    "properties": {
        "status": {"type": "string", "enum": ["completed", "failed"]},
        "ledger_patch": {"type": "object"},
        "memory_summary": {
            "type": "object",
            "required": ["episodic_count", "semantic_candidates_count", "semantic_approved_count"],
            "properties": {
                "episodic_count": {"type": "integer"},
                "semantic_candidates_count": {"type": "integer"},
                "semantic_approved_count": {"type": "integer"},
            },
        },
        "knowledge_summary": {
            "type": "object",
            "required": ["notes_generated", "notes_published"],
            "properties": {
                "notes_generated": {"type": "integer"},
                "notes_published": {"type": "integer"},
            },
        },
        "promotion_summary": {
            "type": "object",
            "required": ["project_promotions", "global_promotions", "rejections"],
            "properties": {
                "project_promotions": {"type": "integer"},
                "global_promotions": {"type": "integer"},
                "rejections": {"type": "integer"},
            },
        },
        "artifacts": {"type": "object"},
        "reason": {"type": "string"},
    },
}
