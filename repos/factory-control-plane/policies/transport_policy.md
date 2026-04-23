# Transport Policy

## Modes
- `http`: use REST session APIs.
- `mcp`: use tool gateway or jsonrpc payload mode.

## Required checks
- Validate transport credentials before run.
- Validate endpoint/tool names by mode.
- Fail early on invalid mode.

## Message interaction fallback
- If primary message endpoint fails with method/route mismatch,
  retry with configured fallback candidate list.
