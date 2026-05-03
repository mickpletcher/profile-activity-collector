# Project Specification

## Vision
Build a compliant, local-first social activity telemetry system that ingests user-owned account exports and permitted official API data, normalizes events into a shared schema, stores them locally, and provides reliable analytics, reporting, and automation hooks.

The system must remain privacy-first, operator-friendly, modular under src/, and suitable for iterative extension across multiple platforms.

## Current Scope
Current repository scope includes:
- Platform-specific CLI tools for Facebook, X, and LinkedIn activity ingestion and reporting.
- Local SQLite-backed storage for normalized activities, import runs, profile records, and raw source items.
- Archive-first ingestion (JSON, CSV, and JS-wrapper formats where relevant).
- Optional official API import where permissions are valid.
- Local export outputs (JSON, CSV) and markdown summary report generation.

Out of scope for current baseline:
- Cloud-hosted storage or managed SaaS components.
- Multi-user auth, advanced dashboards, and AI workflows.

## Target Architecture
Target architecture is a modular Python application organized by capability:
- src/config and config loading
- src/models and schema normalization contracts
- src/database and persistence abstraction
- src/parsers for source format handling
- src/importers for source-specific ingestion orchestration
- src/analytics for aggregate and pattern computations
- src/reports for markdown, CSV, and JSON outputs
- src/api (future) for local REST endpoints
- src/ai (future) for summarization and semantic features
- src/plugins (future) for platform extensions

Design constraints:
- Feature toggles for all non-baseline components.
- Strict separation between parsing, normalization, storage, and reporting.
- Importers must be idempotent and dedupe-aware.
- Storage abstraction must preserve SQLite support while allowing future Postgres migration.

## Supported Platforms
Current and planned platform coverage:
- Facebook (archive-first, optional Graph API with valid permissions)
- X (archive-first, optional official API with valid permissions)
- LinkedIn (archive-first, optional official API with valid permissions)

Future platform onboarding must use plugin contracts and the shared normalized schema.

## Privacy and Compliance Rules
Mandatory rules:
- Do not bypass authentication, privacy controls, rate limits, bot detection, or access restrictions.
- Do not scrape private data from other users.
- Ingest only user-owned exports and official APIs with valid permissions.
- Keep all processing local by default.
- Store API tokens only in environment variables.
- Redact sensitive fields in logs and error outputs.
- Never commit personal data, exports, local DB files, or secret config files.
- Preserve source provenance in raw_items for auditability.

## Database Strategy
Default database:
- SQLite as primary local persistence engine.

Core schema:
- activities
- imports
- profiles
- raw_items

Database strategy details:
- Maintain normalized activity schema with metadata JSON for extensibility.
- Use deterministic activity identity hashes for dedupe support.
- Add migration-ready abstractions to support future Postgres transition.
- Add indexes for activity_type, created_at, source, and importer tracking fields.
- Preserve invalid and failed records with reason metadata for diagnostics.

## Importer Strategy
Importer principles:
- Archive-first ingestion for all platforms.
- API ingestion is optional and permission-gated.
- Parsers convert source formats into candidate records.
- Normalizers map candidates to unified Activity objects.
- Validation runs at importer boundary before persistence.
- Invalid records are retained with error metadata for review.
- Incremental mode uses import cursors/checksums to avoid reprocessing.

Source handling:
- JSON parser support across platforms.
- CSV parser support for LinkedIn and generic tabular exports.
- JS archive parser support for X archive wrapper formats.

## Reporting Strategy
Reporting modes:
- JSON export for machine-readable outputs.
- CSV export for spreadsheet and BI workflows.
- Markdown report for human-readable summaries.

Reporting expectations:
- Deterministic query ordering and filtering.
- Counts by activity type and engagement summary baseline.
- Recent activity section and import health summaries.
- Extensible report pipeline for dashboard and API exposure.

## Extension Strategy for Future Platforms
Extension model:
- New platforms must implement parser, importer, and mapping contracts.
- Shared normalized schema remains central compatibility layer.
- Feature toggles gate new platform modules.
- Plugin discovery supports built-in and external platform adapters.

Compatibility requirements:
- New platform importers must not break existing schema contracts.
- Cross-platform timeline views must normalize timestamps and sources.
- Platform modules must comply with privacy and API policy rules.

## Non-Goals
The following are explicit non-goals for baseline and near-term implementation:
- Scraping protected or private third-party content.
- Circumventing platform terms, access controls, or anti-abuse systems.
- Requiring cloud processing for core ingestion and analytics.
- Building autonomous posting bots or growth-automation behavior.
- Enabling data resale, surveillance use cases, or unauthorized sharing.
- Shipping multi-tenant SaaS deployment as a baseline requirement.

## Engineering Principles
- Python first
- CLI first
- Local-first processing and storage
- Privacy-first defaults
- SQLite by default with migration path to Postgres
- Modular src/ architecture
- Compliant export/API-only ingestion
- Roadmap compatibility with n8n, AI summarization, dashboards, and local LLM integration
