# profile-activity-collector

AI-powered social activity ingestion and telemetry pipeline for tracking and analyzing profile interactions.

## Repository Shape

This repo contains platform-specific CLIs for Facebook, X, and LinkedIn, plus a shared `profile_activity_core` package for common models, SQLite persistence, validation, analytics, and report/export helpers.

## Spec-Driven Workflow

Medium-to-large features should start from a lightweight feature spec in `.github/specs/`. The standing project guardrails live in `.specify/memory/constitution.md`.

Use specs for shared core changes, importer state, CLI behavior changes, local API/dashboard work, plugin architecture, and AI or automation features. Small fixture additions, narrow bug fixes, and minor docs edits can stay spec-free.

The first seed spec is `.github/specs/improved-cli-ux/spec.md`.

## Development

Create a virtual environment and install the shared package with development dependencies:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e ".[dev]"
```

Run the shared core tests:

```bash
python -m pytest -q
```

Run every platform test suite in isolated subprocesses:

```bash
python scripts/run_tests.py
```

Each platform CLI still works from its own directory, for example:

```bash
cd x-activity-logger
python -m src.main init-db
```
