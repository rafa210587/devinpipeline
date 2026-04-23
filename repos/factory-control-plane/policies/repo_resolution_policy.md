# Repo Resolution Policy (Local First With Fallback)

This policy defines how every coordinator/subagent resolves where to read files.

## Resolution algorithm
1. Read local map from `repos/factory-params/params/repos.json`.
2. For each logical repo key, apply:
   - if local path exists, use local path.
   - else if fallback is configured in `repos/factory-params/params/repos_fallback.json`, use fallback.
   - else open blocker and trigger escalation flow.

## Important distinction
- `repos.json` is the active workspace map. Values must resolve to paths the Devin session can actually read or edit.
- Do not put a Git URL in `repos.json` and assume the agent can read it as a filesystem.
- Git URLs belong in `repos_fallback.json` or in Devin repo setup/API metadata.
- A remote Git URL is only usable after Devin has permission to access it and the repo is cloned or otherwise mounted in the session workspace.

## Devin binding requirements
Before relying on a repo alias:
1. Grant Devin access to the Git repository in Devin integrations/permissions.
2. Configure the repo in Devin environment setup so sessions boot with the needed repos available.
3. Index the repo when code search, Ask Devin, DeepWiki, or skill discovery from connected repos is expected.
4. If sessions are created programmatically, include the relevant Devin repo identifiers in the session `repos` payload when required by the API/runtime path.
5. Keep `repos.json` aligned with the path visible from inside the session, such as `/workspace/<repo>`, `~/repos/<repo>`, or a factory-local path under `/workspace/repos/...`.

## Fallback expectations
- Fallback entry can point to:
  - mirror path
  - git URL
  - branch/ref
- Agent must log which source was selected (`local` or `fallback`) in tracking events.

## Safety
- Never silently switch source without recording decision.
- If fallback fetch fails, do not continue blindly; open blocker with evidence.
