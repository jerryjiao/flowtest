# AGENTS.md

## Synthesis workflow（KnowFlow）

- 合成 `raw/` 素材前，按 `docs/agents/synthesize.md` 契约执行（发现待合成、页面解剖、命名与链接、验证循环）。
- 生成页 frontmatter 带 `status: pending` 待人审；人工审阅通过后翻转为 `status: reviewed`。
- 每批合成后运行 `knowflow health` 验证，迭代到全绿。
- 绝不运行不带 `--dry-run` 的 `knowflow fix`。
