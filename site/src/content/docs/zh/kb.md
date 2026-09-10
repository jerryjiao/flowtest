---
title: 知识库
description: flowtest 的记忆——可选的 KnowFlow 知识库。
---

Learn 是乘数：没有沉淀教训的失败还会再来。flowtest 的知识层放在
[KnowFlow](https://github.com/jerryjiao/knowflow) 工作区——纯 Markdown、
人审、本地检索、无服务器。`flowtest-kb` 技能是引擎与 KnowFlow 之间的
薄契约。

## 安装

```bash
npm install -g @jerryjiao/knowflow     # Node 18+、Python 3.10+
knowflow init flowtest/kb              # SUT 仓库内的工作区
knowflow status                        # 确认状态
```

工作区位于 SUT 仓库的 `flowtest/kb/`，让教训与它描述的代码一起版本化。
wiki 入库，索引不入库。

没有 `knowflow` CLI？引擎照常工作——Learn 退化为在 `flowtest/lessons/`
下写笔记。

## 实测结论

2026-09-10 实测（[度量记录](https://github.com/jerryjiao/flowtest/blob/main/docs/measurements/2026-09-10-d2.md)）：

- 语义检索需要 embedding API key（可选，在工作区配置）。
- 对纯 Markdown wiki 的关键词检索——即技能规定的用法（2–4 条短查询，
  而非一条长查询）——在教训规模的语料上稳定命中。

**结论：可用，但不是魔法——知识库保持可选。** 引擎永远不强制要求知识库；
语义检索是增强项，不是前置条件。
