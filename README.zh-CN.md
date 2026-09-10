# flowtest

> 给编码 agent 用的自然语言浏览器测试：你描述用户旅程，agent 把它变成 `.flow.yaml` 测试计划，在真实浏览器里执行、出报告、并从失败中学习。

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/jerryjiao/flowtest)](https://github.com/jerryjiao/flowtest/releases)

**文档与演示：[jerryjiao.github.io/flowtest](https://jerryjiao.github.io/flowtest/)** ·
[English README](README.md)

<p align="center">
  <img src="docs/assets/architecture.svg" alt="flowtest 架构：在宿主（你的编码 agent）内部，引擎 skill 运行 Plan → Run → Report → Learn 循环，写出 .flow.yaml、.result.json 与 report.md 工件；flowtest-kb 知识库把经验教训回馈给 Plan；Run 驱动真实浏览器访问被测系统。" width="760">
</p>
<p align="center"><em>引擎循环运行在你的编码 agent 内部；知识库把经验教训回馈进每一次 Plan。</em></p>

## 为什么选 flowtest

你当然可以直接让 agent 拿 Playwright "测一下注册流程"。flowtest 的不同在于三点：

- **计划是工件，不是聊天记录。** 旅程变成一份可读、可改、可评审、可进版本库的 `.flow.yaml`。agent 负责起草，你看过了才执行。
- **不引入新运行时。** flowtest 以两个 agent skill 的形态装进你已有的宿主——Claude Code、zcode 或任何 SKILL.md 约定的 agent。写应用的同一个 agent 就能测应用。没有守护进程，没有锁定。
- **失败会沉淀成记忆。** 每次失败的运行都被提炼进本地知识库，下一次 Plan 会查询它——循环越用越准，且全部发生在你的机器上。

## 快速开始（实测：约 2 分钟跑通第一条流程）

需要一个 SKILL.md 约定的宿主（Claude Code、zcode……）、带 PyYAML 的
Python 3、任意静态文件服务器：

```bash
git clone https://github.com/jerryjiao/flowtest && cd flowtest
python3 -m http.server 4173 -d demo        # 伺服演示站点
```

然后对你的 agent 说：**“运行 `skills/flowtest/examples/demo-smoke.flow.yaml`
这条流程。”** 引擎 skill 接管：校验 → 解析变量 → 驱动真实浏览器 → 在
`flowtest/reports/` 下写出 result JSON 与报告。

在同一个浏览器里重跑？先在演示站点点**重置演示数据**和 **Sign out**——
会话还活着时，流程的登录预检会跳过，跑出来是 PARTIAL 而不是 PASS。

想测自己的应用？描述旅程——"测试用户能用邮箱注册并看到确认页"——agent
会起草流程，**经你确认后**才执行。

## 工作原理

引擎 skill 在宿主内部运行一个四阶段循环，每个阶段都会写出一个你可以
检查的文件：

| 阶段 | 发生什么 | 工件 |
|---|---|---|
| **Plan（计划）** | 大白话意图变成结构化、可评审的测试计划 | `*.flow.yaml` |
| **Run（执行）** | agent 驱动真实浏览器逐步执行，带截图 | `*.result.json` |
| **Report（报告）** | 结果渲染成人和 agent 都能读的报告 | `*.report.md` |
| **Learn（学习）** | 失败提炼成经验；下一次 Plan 会查询它们 | KB 笔记 |

第四个阶段是差异所在：经验进入 `flowtest-kb`——一个本地的
[KnowFlow](https://github.com/jerryjiao/knowflow) 工作区——并回流进之后的
每一次 Plan（即上图中青色箭头）。

深度文档（中文站）：[引擎循环](https://jerryjiao.github.io/flowtest/zh/engine/) ·
[流程格式](https://jerryjiao.github.io/flowtest/zh/flow-format/) ·
[知识库](https://jerryjiao.github.io/flowtest/zh/kb/) ·
[演示站点](https://jerryjiao.github.io/flowtest/zh/demo-site/)

## 流程格式

一条流程就是纯 YAML——步骤、语义化目标、期望。摘自内置示例
（[完整文件](skills/flowtest/examples/demo-smoke.flow.yaml)）：

```yaml
flow: demo-smoke
title: "Visitor can sign in, create a task, and complete it on the demo site"
sut: demo-site
baseUrl: http://localhost:4173
vars:
  DEMO_USER: demo@flowtest.dev
  DEMO_PASSWORD: demo-password

steps:
  - id: fill-email
    action: fill
    target: "textbox 'Email'"
    value: "{{DEMO_USER}}"

  - id: submit-signin
    action: click
    target: "button 'Sign in'"
    expect:
      - element: "heading 'Tasks'"
      - not_text: "Invalid credentials"

  - id: grab-summary
    action: extract
    value: [open-count, done-count]
```

目标写的是角色名而不是 CSS 选择器——宿主在活页面上解析它们，这让流程
保持可读、可自愈。[格式参考](https://jerryjiao.github.io/flowtest/zh/flow-format/)
覆盖了全部动作、期望与阶段。

## 怎么读报告

每次运行写一份机器可读的 result（`*.result.json`），并从中生成人类可读的
报告（`*.report.md`）。下面是内置演示运行的真实节选：

```json
{
  "flow": "demo-smoke",
  "backend": "agent-browser",
  "verdict": "PASS",
  "counts": { "passed": 9, "healed": 0, "failed": 0, "skipped": 0, "total": 9 },
  "steps": [
    {
      "id": "submit-signin",
      "action": "click",
      "target": "button 'Sign in'",
      "status": "PASSED",
      "durationMs": 9000,
      "screenshot": null
    }
  ]
}
```

每个步骤落进四种状态之一——`PASSED`、`HEALED`（目标变了但运行自行恢复）、
`FAILED`、`SKIPPED`——流程级判定为 `PASS`、`PARTIAL` 或 `FAIL`。失败带
错误信息与截图路径，Learn 阶段凭证据提炼，而不是凭感觉。

## 安装

**Claude Code / zcode（插件）：** 把本仓库加为 marketplace 再安装——两个
skill（`flowtest`、`flowtest-kb`）自动发现：

```bash
claude plugin marketplace add jerryjiao/flowtest
claude plugin install flowtest@flowtest
```

zcode 里：设置 → 插件管理 → Discover → **+** → `jerryjiao/flowtest` →
**Get**。（安装已实测：`claude plugin install` 报告 *Skills (2): flowtest,
flowtest-kb*；zcode 读取同一份 `.claude-plugin/` 清单。）

**任意 SKILL.md 宿主：** 直接拷贝 [`skills/`](skills/) 目录——每个 skill
自包含。

## 项目结构

```
skills/flowtest/       引擎：Plan → Run → Report → Learn（含 .flow.yaml 格式与校验器）
skills/flowtest-kb/    记忆：本地 KnowFlow 知识库（经验教训 + 产品笔记）
demo/                  演示站点：零依赖的被测系统，示例流程的目标
flowtest/              活的工作区：示例运行产物 + 种子知识库
site/                  官网（Astro + Starlight），部署在 GitHub Pages
tests/                 flow 格式校验器测试 + 仓库结构与遗留绑定扫描门禁
```

## 贡献与许可

[MIT](LICENSE)。欢迎 issue 与 PR——先看
[CONTRIBUTING.md](CONTRIBUTING.md) 了解流程与词汇。
