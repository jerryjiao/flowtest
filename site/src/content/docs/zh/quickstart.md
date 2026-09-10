---
title: 快速开始
description: 从全新克隆到一条通过的流程，约两分钟。
---

你需要一个 SKILL.md 约定的宿主（Claude Code、zcode……）、带 PyYAML 的
Python 3、任意静态文件服务器。2026-09-10 实测：冒烟流程 9/9 步通过，
宿主节奏下 70 秒。

## 1. 克隆并伺服演示站点

```bash
git clone https://github.com/jerryjiao/flowtest
cd flowtest
python3 -m http.server 4173 -d demo
```

演示站点是带登录门的单页任务列表——`demo@flowtest.dev` /
`demo-password`——外加列表增删改查。零依赖，完全离线。

## 2. 让代理执行流程

> 运行 `skills/flowtest/examples/demo-smoke.flow.yaml` 这条流程。

引擎技能接手：

1. **校验** —— `scripts/validate_flow.py` 检查流程。
2. **解析** —— `{{占位符}}` 变量依次从环境变量、`flowtest/.env`、流程
   内 `vars` 默认值解析。
3. **执行** —— 代理驱动真实浏览器（宿主有浏览器 MCP 工具优先用之，
   否则退到 `agent-browser` CLI），逐步执行。

## 3. 读报告

运行先落盘，后说话：

- `flowtest/reports/demo-smoke.<时间戳>.result.json` —— 机器可读：结论、
  每步状态、耗时、证据路径。
- `flowtest/reports/demo-smoke.<时间戳>.report.md` —— 人类可读版。
- `flowtest/screenshots/` —— 失败与自愈的证据截图。

```
flow demo-smoke: PASS — 9 steps (9 passed, 0 healed) in 70s
```

## 4. 测你自己的应用

伺服它（或指向已部署的 URL），然后描述旅程：

> 测试用户能用邮箱注册并看到确认页。

代理在 `flowtest/drafts/` 下起草 `.flow.yaml`，**等你确认后**才打开
浏览器。确认过的流程移入 `flowtest/flows/`，重跑不再打扰。

## 排障

- **缺 PyYAML** —— 校验器以退出码 3 说明缺什么（`pip install pyyaml`）。
- **4173 端口被占** —— 换端口伺服，并改流程里的 `baseUrl`。
- **重跑变 PARTIAL？** —— 演示会话存在 `sessionStorage`，会话还活着时
  流程的登录预检会跳过。同一浏览器重跑前，先在演示站点点**重置演示数据**
  并 **Sign out**。全新浏览器会话默认未登录。
