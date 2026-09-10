# ADR-0003: The website runs the ai-study-kit recipe — Starlight splash + plain-fact copy

- **Status**: Accepted
- **Date**: 2026-09-10

## Context

The first website shipped a hand-rolled landing page (`Landing.astro`, 359
lines + 621 lines of `landing.css`) living next to a stock-Starlight docs
site. Two visual systems, double the maintenance, and the landing's "flat,
no gradients" house rule produced a page judged below the bar of
[ai-study-kit's site](https://jerryjiao.github.io/ai-study-kit/) — a sibling
project on the identical stack (Astro + Starlight + GitHub Pages, same
indigo accent).

A grill session on 2026-09-10 settled both complaints — "样式不好看" and
"文案也要好好改改" — into a redesign consensus.

## Decision

Adopt the ai-study-kit website recipe wholesale, with flowtest-specific
content:

1. **One skin**: the homepage is a Starlight `splash` page
   (`content/docs/{en,zh}/index.md`), not a custom component. The hand-rolled
   landing and its stylesheet are deleted. All shared chrome — glass header,
   3px indigo→cyan gradient top line, card system — is ported into
   `src/styles/custom.css` under an `.ft-*` namespace (their `.ask-*`).
   The old "flat, no gradients" rule is retired with it.
2. **Hero shows the artifact, not a mock**: the right column is a code card
   excerpting the real `demo-smoke.flow.yaml`. (An HTML/CSS product mock was
   explicitly rejected for flowtest.)
3. **Sidebar as a journey**: 开始/Get started → 参考/Reference → 资源/Resources
   → 更新日志/Changelog, whose sidebar label carries the plugin version read
   from `.claude-plugin/plugin.json` at build time — zero-maintenance on
   release.
4. **Changelog single-sourced**: a root `CHANGELOG.md` is the file of record;
   `scripts/sync-changelog.mjs` (prebuild) generates the site pages from it.
5. **Plain-fact copy, site-wide**: homepage and all twelve doc pages
   (en/zh) rewritten to the ai-study-kit copy bar — concrete factual
   sentences ("a flow is a YAML file"), no wisecracks, no jargon the
   audience hasn't been given, and no repo-internal citations (the
   "measured — see ADR-0002" pointer left the website; ADRs live in the
   repo). Numbers survive: 9 steps, 70 s, two minutes.
6. **Chinese is the copy master**: zh text is finalized first, en mirrors it.

Deviations from ai-study-kit, on purpose: English stays the default locale
(`/en/` + `/zh/`, not zh-root) to preserve published URLs; no header
"Docs / Live demo" pills (flowtest has no in-site demo); no language
auto-redirect script in the Starlight header — the bare root path redirects
via `src/pages/index.astro`.

## Consequences

- One visual system and one copy voice across landing and docs; the site is
  markdown all the way down except the root redirect.
- Future site work should extend the `.ft-*` components in `custom.css`
  rather than reintroducing per-page CSS.
- Two sibling projects now share a website recipe; changes to it should be
  considered port-able in both directions.
