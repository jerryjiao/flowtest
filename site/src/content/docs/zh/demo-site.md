---
title: 演示站点
description: 仓库内置的被测系统——确定性、离线、零依赖。
---

演示站点是一个单 HTML 文件（`demo/index.html`），带登录门和任务列表——
恰好够一条真实流程施展：增、改名、完成、删。它存在的意义是让新克隆的
仓库几分钟内跑通第一条流程：无构建步骤、无网络依赖、数据确定。

## 伺服它

```bash
python3 -m http.server 4173 -d demo     # 仓库根目录下
# 或：npx serve -l 4173 demo
```

## 演示账号

| 字段 | 值 |
|------|-----|
| 邮箱 | `demo@flowtest.dev` |
| 密码 | `demo-password` |

其他任何组合都会被拒绝并显示可见的"Invalid credentials"提示。会话存在
`sessionStorage`——新浏览器会话默认未登录，流程重跑从头开始。应用页脚的
**重置演示数据**可恢复种子任务列表。

## 流程依赖的约定

- 每个控件都有可访问名，语义定位器（`button 'Sign in'`、
  `textbox 'Email'`、`checkbox 'Buy oat milk'`）无需选择器即可解析。
- 可提取的值以 `data-field` 暴露——摘要行的 `open-count` 与
  `done-count`——`demo-smoke.flow.yaml` 的 `extract` 步骤就读它们。

## 自带示例流程

| 流程 | 旅程 |
|------|------|
| `demo-smoke` | 登录 → 建任务 → 完成 → 提取计数 |

（2026-09-10 实测：PASS，9/9 步，agent-browser 后端宿主节奏 70 秒。）
