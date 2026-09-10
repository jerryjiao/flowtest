# Rebirth consensus — 2026-09-10

flowtest is a fresh start: an internal LLM-driven browser-testing solution (April 2026, single author) reborn as an open, host-agnostic plugin. This document records the consensus that shapes v0.1. The legacy repo stays private and is never republished; this repo starts from a clean snapshot with zero shared git history.

## Decisions

| # | Topic | Decision |
|---|-------|----------|
| 1 | Purpose | Portfolio piece **and** a seriously-maintained community project (issues answered, releases shipped) |
| 2 | Form | Claude Code plugin (installs into Claude Code / zcode via plugin install); any SKILL.md host can consume `skills/` directly. No standalone CLI — the host agent is the runtime |
| 3 | Scope | Ship the **Engine** (Plan → Run → Report → Learn) and a thin **KB** skill. The legacy issue-tracker sync skill is dropped |
| 4 | Knowledge layer | KnowFlow as substrate instead of ported self-built RAG — see [ADR-0001](../adr/0001-knowflow-as-knowledge-substrate.md) |
| 5 | Name | `flowtest` — echoes the `.flow.yaml` artifact and the KnowFlow family. Verified free under the author's namespace; similar-named projects exist in adjacent niches (API-test IDE, netflow probes), accepted as non-blocking |
| 6 | License / docs | MIT; bilingual README (EN primary, zh-CN mirror) |
| 7 | Demo target | In-repo offline Demo Site (forms, multi-step flows, list CRUD) — deterministic, no external services, first flow runs within ~10 minutes of cloning |
| 8 | Browser executor | Decided by measurement at D1: keep the legacy `agent-browser` path vs switch to Playwright — whichever gets a newcomer from zero to first passing flow faster |

## Non-goals for v0.1

- No issue-tracker integration, no cloud service, no daemon.
- No multi-project orchestration — one SUT at a time.
- No self-hosted server component of any kind (the legacy external memory server is retired, not ported).

## Plan

- **D0** — name check, scaffold (this repo), consensus + ADR-0001 + glossary, fresh history. ✅
- **D1** — port the Engine skill; scrub all legacy bindings (IPs, vendor lock-ins, client-specific material); rewrite KB as a KnowFlow-contract skill.
- **D2** — Demo Site; measure the end-to-end quickstart (Plan → Run → Report); measure KnowFlow recall quality for planning, downgrade to optional if weak.
- **D3** — plugin install verified in zcode; CI (structure tests + secret scan gate); publish v0.1.

## Release gates (hard, pre-publish)

1. Security scan clean (Mimosa high-severity gate or equivalent).
2. Repo-wide grep for credentials, hardcoded IPs, and legacy-client identifiers: **zero hits**.
3. Fresh orphan history confirmed — no objects shared with any legacy repo.
