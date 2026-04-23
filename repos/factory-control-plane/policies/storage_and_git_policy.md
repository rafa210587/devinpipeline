# Storage And Git Policy

## Path safety
- Runtime writes must stay inside allowed repo roots.
- Reject output paths outside configured storage root when enforcement is enabled.

## Artifact persistence
- Write canonical stage artifact and timestamp snapshot.
- Keep handoff and tracking files append-only where possible.

## Git sync
- Optional policy-driven git sync:
  - add changed run artifacts
  - optional commit
  - optional push
- Ignore "nothing to commit" as non-failure.
