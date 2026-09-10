---
title: Knowledge base
description: flowtest's memory — an optional KnowFlow workspace of lessons.
---

If failures aren't written down, the same traps get hit again. flowtest
keeps its knowledge layer in a
[KnowFlow](https://github.com/jerryjiao/knowflow) workspace — plain
Markdown, reviewed by humans, searchable locally, no server. The
`flowtest-kb` skill is the thin contract between the engine and KnowFlow.

## Setup

```bash
npm install -g @jerryjiao/knowflow     # Node 18+, Python 3.10+
knowflow init flowtest/kb              # workspace inside the SUT repo
knowflow status                        # confirm state
```

The workspace lives at `flowtest/kb/` in the SUT repository so lessons
version with the code they describe. Commit the wiki; keep the index out of
git.

No `knowflow` CLI? The engine works unchanged — Learn degrades to writing
notes under `flowtest/lessons/`.

## What was measured

On 2026-09-10 ([measurements](https://github.com/jerryjiao/flowtest/blob/main/docs/measurements/2026-09-10-d2.md)):

- Semantic query needs an embedding API key (opt-in, configured in the
  workspace).
- Keyword search over the plain-markdown wiki — what the skill prescribes
  (2–4 short queries, not one long one) — reliably hits the right notes on
  a lessons-sized corpus.

**Verdict: usable, and optional.** The engine never
requires a knowledge base; semantic search is an upgrade, never a
prerequisite.
