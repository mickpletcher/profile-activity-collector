# Development Tasks

This file converts future-upgrades.md into execution-ready engineering tasks.

## Tier 1: Foundation Enhancements

### Task T1-01: Data Validation and Schema Enforcement
- Objective: Enforce strict normalized event validation before persistence.
- Files likely affected: src/models.py, src/importers/*, src/validators/, src/database.py, tests/test_models.py, tests/test_importer.py
- Acceptance criteria:
  - Validation layer rejects malformed activities and unsupported activity_type values.
  - Importers persist invalid records with validation_error metadata.
  - Strict mode can fail fast from CLI.
- Estimated complexity: Medium
- Suggested implementation order: 1

### Task T1-02: Improved CLI UX (Flags, Filtering, Pagination)
- Objective: Add robust filter, paging, and output mode options to list and export workflows.
- Files likely affected: src/main.py, src/cli/options.py, src/database.py, tests/
- Acceptance criteria:
  - list-activity supports source/type/date/text filters.
  - Pagination works with deterministic ordering.
  - Output format selection works consistently.
- Estimated complexity: Low
- Suggested implementation order: 2

### Task T1-03: Incremental Import Support
- Objective: Import only new/changed records for archive and API sources.
- Files likely affected: src/importers/*, src/database.py, src/models.py, tests/test_importer.py
- Acceptance criteria:
  - Importers skip unchanged files/items in incremental mode.
  - Full-refresh mode still available.
  - imports table stores incremental state metadata.
- Estimated complexity: Medium
- Suggested implementation order: 3

### Task T1-04: Logging and Error Handling Improvements
- Objective: Implement structured logs, redaction-safe diagnostics, and standard exception hierarchy.
- Files likely affected: src/logging_setup.py, src/errors.py, src/importers/*, src/config.py, tests/
- Acceptance criteria:
  - All importers emit structured log entries.
  - Sensitive values are redacted in logs and exceptions.
  - Import failure reasons are persisted in imports.error.
- Estimated complexity: Medium
- Suggested implementation order: 4

### Task T1-05: Layered Config System (.env + config.yaml)
- Objective: Add config.yaml support with deterministic precedence and feature toggles.
- Files likely affected: src/config.py, src/config_loader.py, src/main.py, .env.example, README.md, tests/
- Acceptance criteria:
  - Effective config precedence is CLI over env over yaml defaults.
  - Feature toggles available and validated at startup.
  - Non-sensitive effective config can be printed.
- Estimated complexity: Low
- Suggested implementation order: 5

### Task T1-06: Unit and Integration Test Coverage Expansion
- Objective: Raise confidence with fixture-driven integration tests and coverage thresholds.
- Files likely affected: tests/, pytest config files, CI config
- Acceptance criteria:
  - CLI integration tests cover init/import/export/report paths.
  - Parser edge-case tests for malformed input are added.
  - Coverage gate is enforced in test pipeline.
- Estimated complexity: Medium
- Suggested implementation order: 6

### Task T1-07: Data Deduplication Logic
- Objective: Add deterministic dedupe policies and dedupe audit metadata.
- Files likely affected: src/models.py, src/database.py, src/importers/*, tests/
- Acceptance criteria:
  - Duplicate events are detected with canonical hash strategy.
  - Soft and hard dedupe modes are supported.
  - Duplicate linkage metadata is persisted.
- Estimated complexity: Medium
- Suggested implementation order: 7

### Task T1-08: Basic Local Dashboard
- Objective: Provide a read-only local UI for counts, imports, and recent activity.
- Files likely affected: src/web/, src/database.py, src/analytics/*, src/main.py, tests/
- Acceptance criteria:
  - Local server runs without cloud dependencies.
  - Dashboard shows import status and activity summaries.
  - Feature toggle can disable web module.
- Estimated complexity: Medium
- Suggested implementation order: 8

## Tier 2: Advanced Capabilities

### Task T2-01: n8n Integration for Workflow Automation
- Objective: Enable ingestion/export/report execution from local n8n workflows.
- Files likely affected: automation/n8n/, src/api/ or src/cli hooks, README.md
- Acceptance criteria:
  - At least one workflow template runs full ingest to report flow.
  - Workflow execution is idempotent and logs run outcome.
  - Local-only operation is documented.
- Estimated complexity: Medium
- Suggested implementation order: 1

### Task T2-02: Scheduled Imports
- Objective: Support scheduled import runs with lock protection and run summaries.
- Files likely affected: scripts/, src/importers/*, src/database.py, README.md
- Acceptance criteria:
  - Scheduled jobs can run without overlapping execution.
  - Stale lock recovery is implemented.
  - Import run summary output is generated after each run.
- Estimated complexity: Medium
- Suggested implementation order: 2

### Task T2-03: Cross-Platform Unified Activity Timeline
- Objective: Merge platform events into a single timeline view.
- Files likely affected: src/models.py, src/database.py, src/analytics/*, src/reports/*
- Acceptance criteria:
  - Unified query returns events from all enabled platforms.
  - Timestamps are normalized consistently.
  - Cross-source duplicate handling is defined and tested.
- Estimated complexity: Medium
- Suggested implementation order: 3

### Task T2-04: Tagging and Categorization Engine
- Objective: Add user-defined tags and rule-driven categorization.
- Files likely affected: src/rules/, src/database.py, src/main.py, src/reports/*, tests/
- Acceptance criteria:
  - Tags can be created and applied via CLI.
  - Rule-based classification runs on demand.
  - Tagged exports and summaries are available.
- Estimated complexity: Medium
- Suggested implementation order: 4

### Task T2-05: Advanced Filtering and Querying
- Objective: Implement composable filtering and saved queries.
- Files likely affected: src/query/, src/database.py, src/main.py, tests/
- Acceptance criteria:
  - Query expressions map to parameterized SQL safely.
  - Saved queries can be created and executed.
  - Explain mode available for diagnostics.
- Estimated complexity: Medium
- Suggested implementation order: 5

### Task T2-06: Local REST API Layer
- Objective: Expose local endpoints for activity, imports, and reporting.
- Files likely affected: src/api/, src/database.py, src/analytics/*, tests/
- Acceptance criteria:
  - Versioned API routes are documented and tested.
  - Local auth token support is available.
  - API reuses existing service/database abstractions.
- Estimated complexity: Medium
- Suggested implementation order: 6

### Task T2-07: Plugin System for New Platforms
- Objective: Create platform plugin contracts and discovery mechanism.
- Files likely affected: src/plugins/, src/importers/, src/parsers/, tests/
- Acceptance criteria:
  - Plugins can be discovered and validated at runtime.
  - Plugin contract includes parser/importer/mapper requirements.
  - Failure isolation prevents plugin errors from crashing core.
- Estimated complexity: High
- Suggested implementation order: 7

### Task T2-08: Export Connectors
- Objective: Add standardized connector exports for BI and spreadsheet tools.
- Files likely affected: src/connectors/, src/reports/*, src/main.py, tests/
- Acceptance criteria:
  - Export profiles are configurable.
  - Connector outputs are schema-stable.
  - At least one XLSX output path is supported.
- Estimated complexity: Medium
- Suggested implementation order: 8

## Tier 3: Intelligence and Scale

### Task T3-01: AI-Powered Activity Summarization
- Objective: Generate periodic summaries from local activity data.
- Files likely affected: src/ai/summarization/, src/reports/, src/main.py, tests/
- Acceptance criteria:
  - Summaries run fully local when local model is configured.
  - Prompt templates are configurable.
  - Outputs include source traceability.
- Estimated complexity: High
- Suggested implementation order: 1

### Task T3-02: Behavioral Pattern Detection
- Objective: Detect cadence and engagement anomalies over time windows.
- Files likely affected: src/analytics/patterns.py, src/database.py, src/reports/*, tests/
- Acceptance criteria:
  - Rolling-window metrics and anomaly flags are computed.
  - Threshold configuration is available.
  - Pattern outputs are queryable and exportable.
- Estimated complexity: High
- Suggested implementation order: 2

### Task T3-03: Recommendation Engine
- Objective: Recommend posting windows and engagement optimizations.
- Files likely affected: src/ai/recommendations/, src/analytics/*, src/reports/*, tests/
- Acceptance criteria:
  - Recommendations include confidence and rationale fields.
  - Model can be retrained with local data.
  - Recommendations accessible via CLI and report output.
- Estimated complexity: High
- Suggested implementation order: 3

### Task T3-04: Vector Database Integration
- Objective: Support semantic search over activity text and metadata.
- Files likely affected: src/ai/embeddings/, src/search/, src/database.py, src/main.py, tests/
- Acceptance criteria:
  - Embeddings generated and linked to activity IDs.
  - Semantic search returns ranked local results.
  - Hybrid search mode supports keyword plus semantic ranking.
- Estimated complexity: High
- Suggested implementation order: 4

### Task T3-05: Real-Time Ingestion Pipeline
- Objective: Introduce queue-based near real-time ingestion workflows.
- Files likely affected: src/ingestion/, src/importers/, src/database.py, tests/
- Acceptance criteria:
  - Queue workers process ingestion tasks idempotently.
  - Retry and checkpoint strategies are implemented.
  - Batch mode remains supported for offline workflows.
- Estimated complexity: High
- Suggested implementation order: 5

### Task T3-06: Multi-User Support with Role Separation
- Objective: Add local multi-user scopes and role-based access controls.
- Files likely affected: src/auth/, src/database.py, src/api/, src/web/, tests/
- Acceptance criteria:
  - User/workspace data segregation is enforced.
  - Role checks protect API and dashboard routes.
  - Audit logging captures privileged actions.
- Estimated complexity: High
- Suggested implementation order: 6

### Task T3-07: Advanced Analytics Dashboard
- Objective: Build richer visual analytics and comparative views.
- Files likely affected: src/web/, src/api/, src/analytics/, static assets, tests/
- Acceptance criteria:
  - Dashboard displays trends, cohorts, and platform comparisons.
  - Cached aggregate queries reduce load.
  - Read-only mode is default and configurable.
- Estimated complexity: High
- Suggested implementation order: 7

### Task T3-08: Local LLM Integration
- Objective: Integrate local model providers for private AI workflows.
- Files likely affected: src/ai/providers/, src/ai/, src/config.py, tests/
- Acceptance criteria:
  - Local provider adapter supports configurable endpoints.
  - Prompt and output redaction safeguards are enforced.
  - Offline mode is explicitly supported.
- Estimated complexity: High
- Suggested implementation order: 8

### Task T3-09: Alerting System
- Objective: Trigger alert notifications based on rules and thresholds.
- Files likely affected: src/alerts/, src/analytics/, src/api/, src/main.py, tests/
- Acceptance criteria:
  - Rule engine supports threshold, anomaly, and policy triggers.
  - Notification adapters support webhook and email.
  - Alert dedupe and suppression windows are implemented.
- Estimated complexity: High
- Suggested implementation order: 9
