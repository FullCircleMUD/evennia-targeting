# Progress

Running log of milestones with links to evidence. Reverse chronological — newest first.

## 2026-05-20 — repository scaffolded

LIBRARY_STANDARDS scaffold in place: `pyproject.toml`, `runtests.py`, `tests/test_settings.py` + `tests/urls.py`, `src/evennia_targeting/__init__.py` (version 0.0.1), `apps.py`, placeholder `predicates.py` + `helpers.py` modules, smoke tests, `CLAUDE.md`, `README.md`, `docs/INDEX.md`, `docs/progress.md`, `docs/documentation-structure.md`, `docs/architecture.md`, `docs/archive/`.

Tests use Django's test runner via `runtests.py` (standard LIBRARY_STANDARDS pattern — the library will depend on Evennia at runtime once code lands).

**No library code yet.** Predicates and helpers are placeholder modules; the smoke test only verifies the package imports under the runner. Per CLAUDE.md principle 4, primitives are added only when a real consumer needs them — the first consumer being a port of FCM's `utils/targeting/` package, decoupled from FCM-specific imports (FCMCharacter, Condition enum, mixin types, combat handler, group membership). Extraction substrate and open questions captured in [architecture.md](architecture.md).
