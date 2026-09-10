---
title: 简介
description: flowtest 是什么、给谁用、循环长什么样。
---

flowtest 是**面向编码代理的自然语言浏览器测试**。你描述一段用户旅程；
代理把它变成 `.flow.yaml` 计划，在真实浏览器里执行，每一步带截图和
耗时地报告通过/失败，并把失败记成笔记。

它以**代理技能（agent skills）**的形式发布，不是一个测试框架。你已有
的编码代理（Claude Code、zcode，或任何遵循 SKILL.md 约定的宿主）就是
运行时——不需要安装新的服务，也没有守护进程。

## 循环

- **Plan 计划** —— "用户能把商品加入购物车并结账"这样的描述变成结构
  化、可读、可版本化的 `.flow.yaml`。执行前必须经你确认。
- **Run 执行** —— 代理用语义定位器（`button 'Sign in'`、`textbox 'Email'`）
  逐步驱动真实浏览器——不写 CSS 选择器，页面改版后不需要跟着改。
- **Report 报告** —— 每步落盘为 `PASSED` / `HEALED` / `FAILED` /
  `SKIPPED`，带截图与耗时；结果先写盘，再生成摘要。
- **Learn 学习** —— 失败被提炼成知识库笔记（可选，
  [KnowFlow](https://github.com/jerryjiao/knowflow)），下次计划自动避开
  已知的坑。

## 它不是什么

- 不是一个测试框架——没有 runner 进程，没有配置矩阵，没有"迁移"一说。
- 不是云服务——一切都在你的机器、你的代理里运行。
- 不做多项目编排——一次只测一个被测系统（SUT）。

## 仓库地图

| 路径 | 是什么 |
|------|--------|
| `skills/flowtest/` | 引擎技能：Plan → Run → Report → Learn、流程格式、校验器 |
| `skills/flowtest-kb/` | 记忆技能：本地 KnowFlow 知识库 |
| `demo/` | 零依赖演示站点——默认 SUT |
| `flowtest/` | 活的工作区：示例运行产物 + 种子知识库 |
| `tests/` | 流程校验器测试 + 仓库结构与清洁门禁 |

下一步：[快速开始](/flowtest/zh/quickstart/)——约两分钟跑通第一条流程。
