# Feature Specs

This directory contains lightweight feature specs for Copilot/Codex-assisted development. Specs are used for medium-to-large work where requirements, privacy constraints, schema impact, and tests need to be explicit before implementation.

## When To Create A Spec

Create a spec for:

- New shared core capabilities
- Importer state or schema changes
- CLI behavior changes across platforms
- Local API/dashboard work
- Plugin architecture
- AI, semantic search, recommendation, or automation features

Skip a spec for:

- Small fixture additions
- Simple bug fixes
- Minor documentation edits
- Mechanical refactors with no behavior change

## Workflow

1. Copy [template.md](template.md) into a new feature folder.
2. Fill in the problem, goals, requirements, implementation plan, test plan, and acceptance criteria.
3. Implement only against the accepted spec.
4. Update the spec if implementation discoveries change the intended behavior.
5. Keep the project constitution in [.specify/memory/constitution.md](../../.specify/memory/constitution.md) as the top-level guardrail.

## Current Seed Specs

- [Improved CLI UX](improved-cli-ux/spec.md)
