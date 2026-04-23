# Config Resolution Policy

This replaces Python config loading behavior.

## Merge order
1. Built-in defaults (`defaults.json`).
2. Profile override (`profiles/<name>.json`).
3. Runtime override payload from master prompt input.

## Environment placeholders
- Allow `${ENV_VAR}` placeholders in any string field.
- Resolve recursively for nested objects and arrays.
- Unset variables resolve to empty string unless field policy says fail-fast.

## Dotenv behavior
- Load `.env` once at startup if present.
- Existing environment variables must not be overwritten by dotenv.

## Validation
- Validate final toggles against `toggles.schema.json`.
- Abort run if required keys are missing.
