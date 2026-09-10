---
type: entity
title: flowtest demo site
created: 2026-09-10
created_from: raw/web/2026-09-10-1703-text.md
status: reviewed
---

# flowtest demo site

## 基本信息

- **类型**: 产品（in-repo demo System Under Test）
- **别名/英文名**: demo site, Demo Site
- **所属领域**: browser end-to-end testing
- **关键数据**: single HTML file (`demo/index.html`), zero dependencies,
  served on port 4173; seeded account demo@flowtest.dev / demo-password

## 核心要点

- A single-page task list with a sign-in gate and full list CRUD (create,
  rename inline, complete, delete) plus open/done counters exposed as
  `data-field` spans (EXTRACTED)
- Every control carries an accessible name, so flow-format semantic locators
  resolve without CSS selectors; this is the demo doing double duty as an
  accessibility reference (INFERRED: the example flows target only
  role/name locators and pass)

## 关联内容

- 来源: [[sources/flowtest-demo-site-notes]], [[sources/demo-smoke-not-text-lesson]]

## 注意事项与矛盾

- The "Invalid credentials" alert node exists in the DOM at all times
  (hidden) — see [[sources/demo-smoke-not-text-lesson]] before writing
  absence assertions against this site.
