# Changelog

All notable changes to flowtest are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/). The site changelog page is
generated from this file at build time — edit here, not in `site/`.

## [0.1.0] — 2026-09-10

Initial release.

### Added

- Engine skill (`skills/flowtest/`): the Plan → Run → Report → Learn loop —
  natural-language journeys become validated `.flow.yaml` plans, executed in
  a real browser via semantic locators, with per-step evidence (screenshots,
  timings, `result.json`) and bounded self-healing (max 2 retries per step).
- Memory skill (`skills/flowtest-kb/`): optional KnowFlow knowledge base for
  lessons learned from failures; degrades to plain Markdown notes without it.
- Flow format v1 with a standalone validator (`validate_flow.py`) and a
  closed action set (`goto`, `click`, `fill`, `select`, `hover`, `press`,
  `wait`, `check`, `extract`).
- Zero-dependency demo site (`demo/`) — sign-in gate plus a task list — and
  the `demo-smoke` example flow (9 steps, verified passing in 70 s).
- zcode plugin packaging (`.claude-plugin/`) and this documentation site.
