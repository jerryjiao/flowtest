---
title: 流程格式
description: .flow.yaml v1 —— 一段用户旅程一个 YAML 文件。
---

流程（Flow）是描述一段用户旅程的 YAML 测试计划：针对被测系统（SUT）
的有序步骤列表，每步带动作、可选目标、可选期望条件。流程同时为人和
代理而写——一屏读得完，又严格到可以机械校验。

```bash
python3 skills/flowtest/scripts/validate_flow.py path/to/flow.flow.yaml
```

完整契约在仓库
[`skills/flowtest/references/flow-format.md`](https://github.com/jerryjiao/flowtest/blob/main/skills/flowtest/references/flow-format.md)；
本页是导览。

## 一条流程的样子

```yaml
flow: demo-smoke
title: "访客能登录、建任务并完成它"
sut: demo-site
baseUrl: http://localhost:4173
tags: [smoke, demo]
vars:
  DEMO_USER: demo@flowtest.dev

steps:
  - id: submit-signin
    action: click
    target: "button 'Sign in'"
    expect:
      - element: "heading 'Tasks'"
      - not_text: "Invalid credentials"
```

## 步骤

每步有 kebab-case 的 `id`、来自封闭集合的 `action`（`goto`、`click`、
`fill`、`select`、`hover`、`press`、`wait`、`check`、`extract`）、可选
`target`，以及 `expect` 列表——所有条件都满足才算通过。

### 目标是语义定位器

1. 角色加名字：`button 'Sign in'`、`textbox 'Email'`、`heading 'Tasks'`
2. 名字重复时加位置：`button 'Add' (first)`
3. 实在不行用自然语言——宿主代理对着页面快照解析

不写 CSS/XPath：控件没有可访问名是应用的可访问性 bug，值得修，而不是
用选择器绕过去。

### 期望条件

`text`、`not_text`、`url`、`title`、`element`——除非测试数据受控，优先
存在性检查而非精确匹配。`not_text` 是**可见性**断言：隐藏的 DOM 节点
不算数。

### 阶段

`precheck`（前置缺失则快速跳过整条流程）、`setup`（造数据）、`verify`
（被测的旅程——默认）、`conclude`（收尾/清理）。

## 变量

`{{NAME}}` 占位符可出现在任意字符串字段。运行时依次取：环境变量、
`flowtest/.env`（永不提交）、流程内 `vars` 默认值。有未解析的占位符，
浏览器打开前就停。**流程里不写密钥。**

## 状态

步骤终态为 `PASSED`、`HEALED`（有上限的自愈重试后才通过——记录在案，
证据弱于直接通过）、`FAILED`、`SKIPPED`（带原因）。流程级结论由此推导：
`PASS`、`PARTIAL`、`FAIL`。
