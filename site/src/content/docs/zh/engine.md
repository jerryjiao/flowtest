---
title: 引擎循环
description: Plan、Run、Report、Learn 各自的实际行为。
---

`flowtest` 技能就是这个循环。你的代理是运行时，技能是规程。完整规程在
仓库 `skills/flowtest/references/` 下（[plan](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/plan.md)、
[run](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/run.md)、
[report](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/report.md)、
[learn](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/learn.md)）。

## Plan 计划

访谈意图，读 SUT 的页面（或文档），查知识库里的已知坑，然后在
`flowtest/drafts/` 下起草流程。校验、展示计划、**等确认**——新计划绝不
未经确认就执行。确认后的流程放在 `flowtest/flows/`。

## Run 执行

预检（校验 → 解析变量 → 解析 URL），然后步骤循环：快照页面、解析目标、
执行动作、验证 `expect` 条件、记录。关键行为：

- **单步失败不终止运行**——"还剩什么能用"本身就是证据。只有后端崩溃
  或整条流程超时才跳过余下步骤。
- **自愈有上限**——每步至多 2 次重试，按失败类型分类（超时/元素未找到/
  断言失败），策略记录在案。自愈绝不改流程文件；放宽过的断言会明说。
- **执行器中立** —— 代理把流程原语映射到宿主提供的浏览器自动化：宿主
  浏览器 MCP 工具优先，`agent-browser` CLI 兜底（实测依据见
  [ADR-0002](https://github.com/jerryjiao/flowtest/blob/main/docs/adr/0002-executor-priority.md)）。

## Report 报告

result JSON **先于**任何总结落盘。它记录每步状态、耗时、自愈策略、
提取值、证据路径与结论（`PASS` / `PARTIAL` / `FAIL`）。报告步骤把它变成
面向人的 `.report.md`——先结论，再逐步表格，再证据。

## Learn 学习

没有沉淀教训的失败还会再来。Learn 把失败提炼成笔记——什么坑、影响哪些
流程、怎么避开——并经[知识库](/flowtest/zh/kb/)技能入库。没配知识库时，
教训退化为 `flowtest/lessons/` 下的纯 Markdown。
