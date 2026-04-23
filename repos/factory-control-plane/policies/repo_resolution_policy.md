# Repo Resolution Policy (Local First With Fallback)

This policy defines how every coordinator/subagent resolves where to read files.

## Resolution algorithm
1. Read local map from `repos/factory-params/params/repos.json`.
2. For each logical repo key, apply:
   - if local path exists, use local path.
   - else if fallback is configured in `repos/factory-params/params/repos_fallback.json`, use fallback.
   - else open blocker and trigger escalation flow.

## Fallback expectations
- Fallback entry can point to:
  - mirror path
  - git URL
  - branch/ref
- Agent must log which source was selected (`local` or `fallback`) in tracking events.

## Safety
- Never silently switch source without recording decision.
- If fallback fetch fails, do not continue blindly; open blocker with evidence.

