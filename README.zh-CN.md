# flowtest

> 给编码 agent 用的自然语言浏览器测试：你描述用户旅程，agent 把它变成 `.flow.yaml` 测试计划，在真实浏览器里执行、出报告、并从失败中学习。

**状态：早期骨架。** 引擎、demo 站和安装方式随 v0.1 落地——见[计划文档](docs/plans/2026-09-10-rebirth-consensus.md)（英文）。

## 它做什么

- **Plan（计划）**——把一句大白话意图（"用户能把商品加进购物车并完成结算"）变成可读、可改、可进版本库的 `.flow.yaml` 结构化测试计划。
- **Run（执行）**——你的编码 agent 在真实浏览器里逐步执行流程，带截图。
- **Report（报告）**——每条流程一份结构化的通过/失败报告，人和 agent 都能读。
- **Learn（学习）**——失败用例沉淀进本地知识库，让后续规划更准。由 [KnowFlow](https://github.com/jerryjiao/knowflow) 驱动，全部在你的机器上。

## 为什么是 skill 而不是框架

flowtest 以 agent skill 形态发布，不是测试框架。你现有的编码 agent（Claude Code、zcode 及所有遵循 SKILL.md 约定的宿主）就是运行时——不引入新锁定、不要守护进程，写应用的同一个 agent 就能测应用。

## 安装

随 v0.1 提供（Claude Code / zcode 插件安装；其他 SKILL.md 宿主可直接拷 `skills/` 目录）。

## 许可

[MIT](LICENSE)
