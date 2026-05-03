# Project Constitution

This constitution is the standing source of truth for AI-assisted planning and implementation in `profile-activity-collector`. Feature specs and implementation plans must preserve these principles unless the project specification is explicitly updated.

## Mission

Build a compliant, local-first social activity telemetry system that ingests user-owned account exports and permitted official API data, normalizes events into a shared schema, stores them locally, and provides reliable analytics, reporting, and automation hooks.

## Non-Negotiable Principles

### Privacy-first and local-first

- Process and store data locally by default.
- Do not introduce cloud processing as a baseline requirement.
- Do not commit personal data, platform exports, local database files, `.env` files, tokens, or generated reports containing personal data.
- Redact sensitive values in logs, errors, reports, and test output.

### Compliance-safe ingestion

- Ingest only user-owned exports and official APIs with valid permissions.
- Do not bypass authentication, privacy controls, access restrictions, rate limits, bot detection, or platform protections.
- Do not scrape private data from other users.
- Do not build autonomous posting, growth automation, surveillance, resale, or unauthorized sharing features.

### Shared core first

- Put shared schema, persistence, validation, querying, analytics, reporting, configuration, and reusable CLI behavior in `profile_activity_core`.
- Keep platform-specific directories focused on parsers, importers, API clients, source-specific mapping rules, and thin CLI adapters.
- Prefer compatibility shims over duplicating shared logic in each platform app.

### CLI-first baseline

- The CLI remains the default operating surface.
- Dashboards, APIs, scheduled jobs, n8n workflows, and AI features must be opt-in layers over the local data store.
- New user-facing workflows should be scriptable and testable without a browser.

### SQLite-compatible persistence

- SQLite is the default local database.
- Schema changes must remain migration-friendly and should not close the door on a future Postgres adapter.
- Importers must be idempotent and dedupe-aware.
- Preserve source provenance in `raw_items` for auditability.

### Testable, fixture-driven changes

- Parser and importer changes should include fixture coverage for representative archive shapes.
- Shared core changes should include top-level tests.
- Platform behavior should remain covered by `scripts/run_tests.py`.
- Tests must not require real platform credentials or personal data.

## Spec Workflow Rules

Use a feature spec for medium-to-large work, especially:

- Incremental import support
- CLI filtering, pagination, and output modes
- Layered config and feature toggles
- Local API or dashboard work
- Plugin architecture
- AI summarization, semantic search, or recommendation features

Feature specs are optional for:

- Small parser fixture additions
- One-off bug fixes
- Minor docs edits
- Narrow refactors inside one file

Each feature spec should include:

- Problem statement
- Goals and non-goals
- User stories or workflows
- Functional requirements
- Data/schema impact
- Privacy and compliance considerations
- Implementation plan
- Test plan
- Acceptance criteria

## Definition of Done

A feature is done when:

- Acceptance criteria in its feature spec are satisfied.
- Relevant shared and platform tests pass.
- New behavior is documented where users or future agents need it.
- Privacy, compliance, and local-first constraints remain intact.
- Existing platform CLIs remain compatible unless a breaking change is explicitly approved.
