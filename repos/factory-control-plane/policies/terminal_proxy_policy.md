# Terminal Proxy Policy

## Goals
- Mirror session messages to operator terminal.
- Allow optional operator input while stage waits for user/approval.

## Rules
- Enable only if terminal proxy toggle is true.
- Keep message deduplication using stable signatures.
- Truncate very long messages by configured max chars.
- Ignore operator `/skip` input command.
- Disable interactive input when terminal is non-interactive.
