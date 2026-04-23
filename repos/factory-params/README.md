# Factory Params

Central place for execution toggles and profiles.

- `params/defaults.json`: baseline runtime behavior.
- `params/profiles/*.json`: profile-specific overrides.
- `params/toggles.schema.json`: toggle contract.
- `params/repos.json`: canonical repository path mapping for paths available inside the Devin workspace.
- `params/repos_fallback.json`: fallback mirror path or Git URL metadata when the primary path is unavailable.

## Repo Path Rule

`repos.json` should point to readable/editable workspace paths, not raw Git endpoints.

Use Git URLs in `repos_fallback.json` or Devin repo setup metadata. The agent can only read and edit a repository after Devin has access and the repository is cloned/mounted in the session environment.
