# ADR-0001: KnowFlow as the knowledge substrate

- **Status**: Accepted (2026-09-10)
- **Context**: The Plan step works better when the agent can retrieve product knowledge — docs for the System Under Test, plus notes from past failed runs. The legacy implementation carried a self-built Python vector pipeline (custom embedding-format store, single-vendor embedding API, and a privately-hosted server component).

## Options considered

1. **Port the self-built RAG** — keeps vendor bindings and a server dependency; duplicates maintenance of capability that already exists in the author's ecosystem.
2. **Integrate KnowFlow** — a local, MIT-licensed Markdown knowledge workspace (`ingest` / semantic search / graph / review gate) that any coding agent can drive.
3. **No knowledge layer in v0.1** — simplest, but forfeits the Learn step that differentiates the engine.

## Decision

Option 2. The KB ships as a **thin skill** that teaches the host agent to use KnowFlow (`knowflow init` a KB workspace, `ingest` docs and failure notes, query during Plan). The self-built vector pipeline is not ported; the external server is retired entirely.

## Consequences

- The plugin loses its Python vector code and all server-side dependencies — skills plus scripts only.
- KnowFlow becomes a user-facing (optional) dependency; users without an embedding API key get the engine without the Learn step.
- The two projects cross-link and share an audience; if KnowFlow's recall proves weak for planning at D2, KB degrades to optional rather than blocking the release.
