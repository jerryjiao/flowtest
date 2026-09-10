---
type: entity
title: demo-smoke flow
created: 2026-09-10
created_from: raw/web/2026-09-10-1704-text.md
status: reviewed
---

# demo-smoke flow

## 基本信息

- **类型**: 项目构件（shipped example flow）
- **别名/英文名**: demo-smoke
- **所属领域**: browser end-to-end testing
- **关键数据**: 9 steps; shipped at
  `skills/flowtest/examples/demo-smoke.flow.yaml`

## 核心要点

- Journey: sign in as the seeded demo user, create one task ("Buy oat
  milk"), complete it, confirm the list item, extract the summary counters
  (EXTRACTED)
- First measured run (2026-09-10): PASS, 9/9 steps passed, 0 healed — 70 s
  host-paced wall clock via the agent-browser CLI backend; all semantic
  locators resolved on first snapshot (EXTRACTED)

## 关联内容

- 来源: [[sources/flowtest-demo-site-notes]], [[sources/demo-smoke-not-text-lesson]]

## 时间线

| 日期 | 事件 | 来源 |
|------|------|------|
| 2026-09-10 | First measured end-to-end run: PASS 9/9 | [[sources/flowtest-demo-site-notes]] |
