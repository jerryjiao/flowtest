# flowtest

> 给编码 agent 用的自然语言浏览器测试：你描述用户旅程，agent 把它变成 `.flow.yaml` 测试计划，在真实浏览器里执行、出报告、并从失败中学习。

```
skills/flowtest/       引擎：Plan → Run → Report → Learn（含 .flow.yaml 格式与校验器）
skills/flowtest-kb/    记忆：本地 KnowFlow 知识库（经验教训 + 产品笔记）
demo/                  演示站点：零依赖的被测系统，示例流程的目标
flowtest/              活的工作区：示例运行产物 + 种子知识库
site/                  官网（Astro + Starlight），部署在 GitHub Pages
tests/                 flow 格式校验器测试 + 仓库结构与遗留绑定扫描门禁
```

**文档与演示：[jerryjiao.github.io/flowtest](https://jerryjiao.github.io/flowtest/)** ·
[English README](README.md)

## 快速开始（实测：约 2 分钟跑通第一条流程）

需要一个 SKILL.md 约定的宿主（Claude Code、zcode……）、带 PyYAML 的
Python 3、任意静态文件服务器：

```bash
git clone https://github.com/jerryjiao/flowtest && cd flowtest
python3 -m http.server 4173 -d demo        # 伺服演示站点
```

然后对你的 agent 说：**"运行 `skills/flowtest/examples/demo-smoke.flow.yaml`
这条流程。"** 引擎 skill 接管：校验 → 解析变量 → 驱动真实浏览器 → 在
`flowtest/reports/` 下写出 result JSON 与报告。

想测自己的应用？描述旅程——"测试用户能用邮箱注册并看到确认页"——agent
会起草流程，**经你确认后**才执行。

## 它做什么

- **Plan（计划）**——把一句大白话意图（"用户能把商品加进购物车并完成结算"）变成可读、可改、可进版本库的 `.flow.yaml` 结构化测试计划。
- **Run（执行）**——你的编码 agent 在真实浏览器里逐步执行流程，带截图。
- **Report（报告）**——每条流程一份结构化的通过/失败报告，人和 agent 都能读。
- **Learn（学习）**——失败用例沉淀进本地知识库，让后续规划更准。由 [KnowFlow](https://github.com/jerryjiao/knowflow) 驱动，全部在你的机器上。

## 为什么是 skill 而不是框架

flowtest 以 agent skill 形态发布，不是测试框架。你现有的编码 agent（Claude Code、zcode 及所有遵循 SKILL.md 约定的宿主）就是运行时——不引入新锁定、不要守护进程，写应用的同一个 agent 就能测应用。

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

## 许可

[MIT](LICENSE)
