# Upgrade Prompts

Each section contains a copy-and-paste ready prompt for GitHub Copilot. Prompts are aligned to future-upgrades.md and assume Python, CLI-first, local-first, privacy-first implementation constraints.

## Tier 1 Prompts

### Prompt 1: Data Validation and Schema Enforcement
Goal: Implement strict validation for normalized activities before database persistence.
Context: Existing importers normalize events but validation is limited. Add schema validation at importer boundaries.
Files to inspect first: src/models.py, src/importers/, src/database.py, tests/test_models.py, tests/test_importer.py
Files to create or modify: src/validators/activity_validator.py, src/importers/*, src/main.py, tests/
Technical requirements:
- Enforce required fields and allowed activity_type enums.
- Add strict mode option that fails on first invalid record.
- Persist invalid records to raw_items with validation_error metadata.
Testing requirements:
- Add valid and invalid fixture cases for each platform importer.
- Add strict and non-strict mode tests.
Acceptance criteria:
- Invalid activities are never inserted into activities table.
- Validation errors are traceable with source file metadata.

### Prompt 2: Improved CLI UX (Flags, Filtering, Pagination)
Goal: Add advanced filtering and pagination to list and export commands.
Context: CLI commands exist but filtering and paging are basic.
Files to inspect first: src/main.py, src/database.py, tests/
Files to create or modify: src/cli/options.py, src/main.py, src/database.py, tests/
Technical requirements:
- Add filter flags for source, type, date range, and text contains.
- Add pagination options offset, limit, page.
- Add output format option table/json/csv for list command.
Testing requirements:
- Add tests for each filter and pagination path.
- Add negative tests for invalid flag combinations.
Acceptance criteria:
- list-activity supports deterministic paging and filter results.

### Prompt 3: Incremental Import Support
Goal: Implement incremental import mode for archive and API pipelines.
Context: Current importers process all files/items each run.
Files to inspect first: src/importers/, src/database.py, src/main.py
Files to create or modify: src/importers/*, src/database.py, src/main.py, tests/test_importer.py
Technical requirements:
- Track importer state using checksum/cursor metadata.
- Add incremental and full-refresh command flags.
- Skip previously imported unchanged records.
Testing requirements:
- Add repeated-run tests showing unchanged files are skipped.
- Add full-refresh tests showing complete reprocessing.
Acceptance criteria:
- Incremental mode reduces processed count on reruns without missing new events.

### Prompt 4: Logging and Error Handling Improvements
Goal: Standardize structured logging and importer error handling.
Context: Logging exists but lacks unified format and exception strategy.
Files to inspect first: src/config.py, src/importers/, src/main.py
Files to create or modify: src/logging_setup.py, src/errors.py, src/importers/*, tests/
Technical requirements:
- Add structured logger initialization with redaction.
- Define custom exceptions for parse/import/api failures.
- Persist summarized failure reasons in imports table.
Testing requirements:
- Add tests that verify sensitive field redaction.
- Add tests for error persistence and retry boundaries.
Acceptance criteria:
- Import failures are diagnosable without leaking secrets.

### Prompt 5: Config System (.env + config.yaml)
Goal: Add layered configuration with explicit precedence and feature toggles.
Context: Project currently relies mostly on environment variables.
Files to inspect first: src/config.py, src/main.py, .env.example
Files to create or modify: src/config_loader.py, src/config.py, src/main.py, README.md, tests/
Technical requirements:
- Support yaml config loading with precedence CLI over env over yaml.
- Add feature toggles namespace for optional modules.
- Validate config at startup and fail with clear messages.
Testing requirements:
- Add precedence tests and missing-key tests.
- Add tests for toggle default behavior.
Acceptance criteria:
- Config values resolve predictably across all sources.

### Prompt 6: Unit and Integration Test Coverage Expansion
Goal: Expand automated test coverage for core CLI and import workflows.
Context: Baseline tests exist but do not cover full end-to-end command paths.
Files to inspect first: tests/, src/main.py, src/importers/, src/reports/
Files to create or modify: tests/fixtures/, tests/integration/, test config files
Technical requirements:
- Add fixture-driven archive scenarios for all supported platforms.
- Add CLI integration tests for init-db, import, export, report.
- Add parser edge-case and malformed-input tests.
Testing requirements:
- Enforce minimum coverage threshold.
- Ensure tests run in isolated temp directories.
Acceptance criteria:
- CI-ready test suite reliably catches parser/importer regressions.

### Prompt 7: Data Deduplication Logic
Goal: Add deterministic dedupe logic and duplicate audit metadata.
Context: Event identity is hash-based but dedupe policies are not fully explicit.
Files to inspect first: src/models.py, src/database.py, src/importers/
Files to create or modify: src/dedupe.py, src/importers/*, src/database.py, tests/
Technical requirements:
- Define canonical dedupe key strategy by source, type, actor, timestamp, and content fingerprint.
- Support soft dedupe and hard dedupe modes.
- Record duplicate_of and dedupe_reason metadata.
Testing requirements:
- Add tests for duplicate and near-duplicate scenarios.
- Add cross-platform duplicate behavior tests.
Acceptance criteria:
- Duplicate records are consistently handled and auditable.

### Prompt 8: Basic Local Dashboard
Goal: Build a minimal local dashboard for activity and importer status.
Context: Reporting is currently CLI and markdown only.
Files to inspect first: src/database.py, src/analytics/, src/reports/
Files to create or modify: src/web/app.py, src/web/templates/, src/main.py, tests/
Technical requirements:
- Add local read-only web routes for recent activity and counts.
- Reuse existing analytics/database abstractions.
- Gate web module behind feature toggle.
Testing requirements:
- Add route tests and smoke test for startup.
- Add permission boundary tests for read-only mode.
Acceptance criteria:
- Local dashboard runs and displays current dataset safely.

## Tier 2 Prompts

### Prompt 9: n8n Integration
Goal: Integrate local n8n workflows for import, export, and report automation.
Context: Commands are manual; workflows are not yet orchestrated.
Files to inspect first: src/main.py, src/importers/, src/reports/
Files to create or modify: automation/n8n/, src/api/ or src/cli hooks, README.md
Technical requirements:
- Provide workflow templates for recurring ingestion.
- Add idempotency key handling for reruns.
- Keep all workflow execution local-first.
Testing requirements:
- Validate one end-to-end workflow run locally.
- Verify duplicate workflow execution does not duplicate data.
Acceptance criteria:
- n8n can run repeatable ingestion and reporting jobs safely.

### Prompt 10: Scheduled Imports
Goal: Add scheduler support for unattended imports with lock protection.
Context: Imports run manually only.
Files to inspect first: src/importers/, src/database.py
Files to create or modify: scripts/schedule_*, src/scheduler.py, README.md, tests/
Technical requirements:
- Add cron and platform scheduler examples.
- Implement lock file and stale-lock recovery.
- Emit structured run summary per schedule cycle.
Testing requirements:
- Test lock behavior and stale lock cleanup.
- Test scheduled runner idempotent behavior.
Acceptance criteria:
- Scheduled runs execute reliably without overlap.

### Prompt 11: Cross-Platform Unified Timeline
Goal: Create a single timeline query and report view across all platforms.
Context: Platform loggers are currently separate projects and outputs.
Files to inspect first: src/models.py, src/database.py, src/reports/
Files to create or modify: src/timeline.py, src/database.py, src/reports/*, tests/
Technical requirements:
- Add canonical timeline schema with platform field.
- Normalize timestamps and merge ordering.
- Add conflict handling for cross-source duplicates.
Testing requirements:
- Add multi-platform fixture tests.
- Verify stable ordering and dedupe behavior.
Acceptance criteria:
- Unified timeline output is available via CLI and export.

### Prompt 12: Tagging and Categorization Engine
Goal: Add user tags and rule-based event categorization.
Context: Events are normalized but semantic grouping is limited.
Files to inspect first: src/database.py, src/main.py, src/analytics/
Files to create or modify: src/rules/, src/tagging.py, src/database.py, src/main.py, tests/
Technical requirements:
- Create tags and activity_tags tables.
- Implement keyword/metadata rule matching.
- Add tag management commands.
Testing requirements:
- Add tests for rule matches and manual tag operations.
- Add export/report tests with tags.
Acceptance criteria:
- Tagged analytics and filtered outputs are available.

### Prompt 13: Advanced Filtering and Querying
Goal: Implement composable query language for activity retrieval.
Context: Current filtering is flag-based and limited.
Files to inspect first: src/database.py, src/main.py
Files to create or modify: src/query/engine.py, src/query/parser.py, src/database.py, src/main.py, tests/
Technical requirements:
- Build safe parameterized query translation.
- Add saved query persistence.
- Add explain mode for query diagnostics.
Testing requirements:
- Add parser and SQL generation tests.
- Add injection-safety tests.
Acceptance criteria:
- Complex queries run safely and reproducibly.

### Prompt 14: REST API Layer
Goal: Expose local API endpoints for activity, import status, and reports.
Context: Existing tool is CLI only.
Files to inspect first: src/database.py, src/analytics/, src/reports/
Files to create or modify: src/api/app.py, src/api/routes/, src/api/schemas.py, tests/
Technical requirements:
- Add versioned routes and local auth token support.
- Reuse existing business logic modules.
- Add optional local rate limiting.
Testing requirements:
- Add API contract tests and auth tests.
- Add route tests for filters and pagination.
Acceptance criteria:
- Local API serves core capabilities without duplicating logic.

### Prompt 15: Plugin System for New Platforms
Goal: Introduce plugin architecture for adding new social platforms.
Context: Platform support currently requires direct code changes.
Files to inspect first: src/importers/, src/parsers/, src/models.py
Files to create or modify: src/plugins/interfaces.py, src/plugins/loader.py, src/plugins/registry.py, tests/
Technical requirements:
- Define parser/importer/mapper plugin contracts.
- Implement discovery and validation.
- Isolate plugin failures from core runtime.
Testing requirements:
- Add plugin loading tests with valid and invalid plugins.
- Add compatibility tests for schema mapping.
Acceptance criteria:
- New platform can be added via plugin without core rewrites.

### Prompt 16: Export Connectors
Goal: Add connector-ready export adapters for BI and spreadsheet tools.
Context: Exports currently target generic CSV and JSON.
Files to inspect first: src/reports/csv_export.py, src/reports/json_export.py
Files to create or modify: src/connectors/, src/reports/, src/main.py, tests/
Technical requirements:
- Add profile-based export schemas.
- Add optional XLSX output support.
- Preserve stable column naming conventions.
Testing requirements:
- Add golden-file tests for connector outputs.
- Add schema stability regression tests.
Acceptance criteria:
- Connectors produce consistent outputs for downstream tools.

## Tier 3 Prompts

### Prompt 17: AI-Powered Activity Summarization
Goal: Generate periodic AI summaries of activity trends and anomalies.
Context: Reports are deterministic but not insight-focused.
Files to inspect first: src/reports/markdown_report.py, src/analytics/
Files to create or modify: src/ai/summarization/, src/reports/, src/main.py, tests/
Technical requirements:
- Add prompt templates and retrieval-based context building.
- Keep provider interface pluggable and local-first.
- Add source citation metadata in summaries.
Testing requirements:
- Add deterministic mock-provider tests.
- Add redaction tests for summary inputs.
Acceptance criteria:
- AI summaries run locally and are traceable to source events.

### Prompt 18: Behavioral Pattern Detection
Goal: Detect engagement and cadence anomalies over time.
Context: Existing analytics are mostly aggregate counts.
Files to inspect first: src/analytics/activity_summary.py, src/database.py
Files to create or modify: src/analytics/patterns.py, src/reports/, src/database.py, tests/
Technical requirements:
- Compute rolling windows and change-point metrics.
- Persist anomaly flags and confidence scores.
- Add configurable thresholds.
Testing requirements:
- Add time-series fixture tests.
- Validate anomaly precision against known synthetic datasets.
Acceptance criteria:
- Pattern detections are reproducible and configurable.

### Prompt 19: Recommendation Engine
Goal: Recommend optimal posting windows and engagement actions.
Context: Historical activity exists but no guidance layer is present.
Files to inspect first: src/analytics/, src/reports/
Files to create or modify: src/ai/recommendations/, src/main.py, src/reports/, tests/
Technical requirements:
- Build local ranking model from historical outcomes.
- Include confidence and explanation output fields.
- Expose recommendations via CLI and report sections.
Testing requirements:
- Add model training and inference tests.
- Add stability tests across repeated runs.
Acceptance criteria:
- Recommendations are generated with explainable scoring.

### Prompt 20: Vector Database Integration
Goal: Add semantic search over activity content.
Context: Search currently relies on keyword filtering.
Files to inspect first: src/models.py, src/database.py, src/main.py
Files to create or modify: src/ai/embeddings/, src/search/, src/main.py, tests/
Technical requirements:
- Generate and store embeddings linked to activity IDs.
- Implement semantic and hybrid search commands.
- Keep local embedding pipeline as default.
Testing requirements:
- Add semantic retrieval tests using controlled fixtures.
- Add fallback tests when vector backend is unavailable.
Acceptance criteria:
- Semantic search returns relevant ranked results locally.

### Prompt 21: Real-Time Ingestion Pipeline
Goal: Move from batch-only to queue-based near real-time ingestion.
Context: Ingestion runs currently as synchronous CLI jobs.
Files to inspect first: src/importers/, src/database.py
Files to create or modify: src/ingestion/queue.py, src/ingestion/worker.py, src/importers/, tests/
Technical requirements:
- Add queue abstraction with retry-safe checkpoints.
- Make processors idempotent and restart-safe.
- Keep batch ingestion mode fully supported.
Testing requirements:
- Add worker retry and crash-recovery tests.
- Add idempotency tests for duplicate messages.
Acceptance criteria:
- Real-time pipeline processes events reliably without duplication.

### Prompt 22: Multi-User Support with Role Separation
Goal: Add local multi-user scopes and role-based access controls.
Context: Current model is single-user local operation.
Files to inspect first: src/database.py, src/api/ if present, src/web/ if present
Files to create or modify: src/auth/, src/database.py, src/api/, src/web/, tests/
Technical requirements:
- Add users, roles, permissions, and workspace scoping.
- Enforce access boundaries in API and dashboard layers.
- Add audit trail for privileged actions.
Testing requirements:
- Add authorization matrix tests.
- Add cross-workspace isolation tests.
Acceptance criteria:
- Data and actions are properly isolated by user role and workspace.

### Prompt 23: Advanced Analytics Dashboard
Goal: Build deeper visual analytics dashboard with platform comparisons.
Context: Basic dashboard roadmap exists but advanced visuals are pending.
Files to inspect first: src/web/, src/analytics/, src/reports/
Files to create or modify: src/web/, src/api/, src/analytics/, static assets, tests/
Technical requirements:
- Add trend, cohort, and cross-platform comparison views.
- Cache heavy aggregate queries.
- Keep dashboard read-only by default.
Testing requirements:
- Add endpoint and rendering smoke tests.
- Add aggregate query performance baseline tests.
Acceptance criteria:
- Dashboard provides stable, useful analytics with acceptable local performance.

### Prompt 24: Local LLM Integration
Goal: Integrate local LLM providers for private analysis workflows.
Context: AI roadmap requires local model support and provider abstraction.
Files to inspect first: src/config.py, src/ai/ if present
Files to create or modify: src/ai/providers/, src/ai/runtime.py, src/main.py, tests/
Technical requirements:
- Create provider adapter interface.
- Support local endpoint configuration and offline operation.
- Enforce prompt/input redaction safeguards.
Testing requirements:
- Add adapter tests with mocked local endpoints.
- Add fallback and timeout behavior tests.
Acceptance criteria:
- Local LLM workflows execute without cloud dependency by default.

### Prompt 25: Alerting System
Goal: Implement rule-driven alerting via webhook and email channels.
Context: Analytics currently require manual review.
Files to inspect first: src/analytics/, src/main.py, src/reports/
Files to create or modify: src/alerts/rules.py, src/alerts/channels.py, src/alerts/engine.py, tests/
Technical requirements:
- Support threshold, anomaly, and policy-based alert rules.
- Implement dedupe keys and suppression windows.
- Add local-safe delivery adapters.
Testing requirements:
- Add rule evaluation tests.
- Add channel delivery tests with mock endpoints.
Acceptance criteria:
- Alerts trigger accurately and avoid duplicate noise.
