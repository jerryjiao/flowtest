# KnowFlow 合成契约

你是合成 agent（ZCode、Codex CLI、Claude Code、OpenCode 中的任意一个）。本契约是你的完整工作规程：把 `raw/` 素材合成为 wiki 页面。同一份契约，四种 agent 的执行结果必须一致。

三条硬禁令，任何步骤不得违反：

1. **绝不运行不带 `--dry-run` 的 `knowflow fix`**——破坏性修复，会毁掉待审稿（见第 5 节）。
2. **绝不创建、修改或命名 `wiki/index.md`、`wiki/log.md`、`wiki/tag/`**——归工具所有。
3. **绝不改写 `status: reviewed` 页面的实质内容**——审阅权在人。

页面形状以 [templates/](../../templates/) 四张模板为权威本体；必填/可选剖分、验收线与裁定详见 [data-model.md](../reference/data-model.md)，本契约与两者冲突时以模板为准。

约定：默认布局 `raw/` 为素材目录、`wiki/` 为 wiki 根（`.knowflowrc` 可改，以配置值为准）；所有路径为 POSIX 相对路径。

## 1. 发现待合成素材

待合成 = `raw/**/*.md` 全集 − 四个页型目录（`wiki/sources` `wiki/entities` `wiki/concepts` `wiki/comparisons`）所有页面 frontmatter 中出现过的 `created_from` 值。派生差集，零状态文件，无登记表。

等价 shell（POSIX 可移植，在项目根执行；`$t` 为任意可写临时目录，用后清理）：

```sh
find raw -type f -name '*.md' -print 2>/dev/null | sed 's|^\./||' | LC_ALL=C sort > "$t/raw"
find wiki/sources wiki/entities wiki/concepts wiki/comparisons -type f -name '*.md' \
  -exec grep -h '^created_from:' {} + 2>/dev/null \
  | sed -e 's/^created_from:[[:space:]]*//' -e "s/^[\"']//" -e "s/[\"']\$//" \
        -e 's|^\./||' | LC_ALL=C sort -u > "$t/done"
comm -23 "$t/raw" "$t/done"
```

注：上式假定默认布局（`raw/` 与 `wiki/` 在项目根）；自定义 `.knowflowrc` 布局以 `knowflow compose --list` 为准。

说明：grep 模式 `^created_from:` 匹配 frontmatter 内该键；两侧路径统一剥 `./` 前缀后再比较，比较前均为 POSIX 相对路径。

本机 knowflow 较新时可直接运行 `knowflow compose --list`，输出语义与上式一致；旧版本无此命令时用上述 shell。

性质（理解即可，无需处理）：

- 删除某张已合成页 → 其 raw 自动回到待合成清单（自愈）。
- 同一 URL 采集两次 → 两张 source 页是设计内行为；内容级去重属 roadmap，不在本契约。
- 手动建页与 agent 建页一视同仁：页面 frontmatter 有 `created_from` 即算「已合成」。

## 2. 合成单元与范围

1. 一个待合成 raw 文件 → 一张 `status: pending` 的 source 页，直接落在最终目录 `wiki/sources/`。
2. 同时为该 source 页「提取的实体」中尚不存在的实体各建一张最小 entity 页：必填章节齐全，确实未知的字段写「无」，不得为凑内容编造。已存在的实体页不重建、不改写，source 页直接链接。
3. concept / comparison 页仅在人显式点名时合成（如「给 X 建概念页」），不随 raw 数量自动膨胀。
4. 允许一个会话批量合成 N 个 raw；每张页独立待审、独立翻转，互不阻塞。
5. 各页型章节剖分、必填/可选与验收线以 templates/ 与 data-model.md 为准。注意裁定：必填章节「关联内容」仅适用于 entity / concept / comparison——source 页的对外链接职责由「提取的实体」「提取的概念」两章节承担。

## 3. 命名与链接

文件命名：

- 目录 = 页型目录；文件名 = 标题（entity 页为实体本名）的 slug：ASCII 字母转小写、CJK 字符原样保留、空格转 `-`、不加日期前缀（日期在 frontmatter `created`）、写入前做 NFC Unicode 规范化。
- 目标路径已存在时追加消歧后缀，绝不静默覆盖既有文件。

wikilink（生成页强制）：

- 目标为 wiki 根相对路径，不带 `.md`，不带 `|别名` 管道，禁裸名。`[[entities/karpathy]]` 合法；`[[karpathy]]`、`[[entities/karpathy.md]]`、`[[karpathy|Andrej]]` 非法。
- 显示变体写进散文文本，不进链接语法。
- 链接目标必须真实存在（本批创建的页算存在）。尚无页面的概念：在「提取的概念」中写概念名散文加本篇角色说明，不加 wikilink；待人工点名合成该概念页后再由人工决定补链。
- `wiki/index.md`、`wiki/log.md`、`wiki/tag/` 归工具所有，你不创建也不命名；`topics/`、`overview` 不在解剖内，不生成。

## 4. 状态与审核

1. 生成页直接落最终目录，frontmatter `status: pending`。无 staging 区、无转正 move、无「待审」文件名后缀。
2. 审核动作 = 人把 pending 一词改成 reviewed。不设工具闸；建议审核者翻转前先看一眼最近一次 `knowflow health` 输出。
3. 驳回 = 删除该文件。残留反链随后由 health 暴露为坏链——这是诚实信号，不做掩蔽处理。
4. 无 `status` 键的存量页按已审（reviewed）处理；手写页可直接落 `status: reviewed`。

## 5. 验证循环

写完本批所有页后立即执行，阻塞到绿：

```sh
knowflow health
```

- 三查（坏链、最小体积、孤儿页）全绿才算交付。坏链与最小体积检查对 pending 页全量生效；孤儿页判定豁免 pending——待审稿没被链接是常态，**不要为消孤儿乱建链接**，审核后自然消。
- 红项只修你自己本批创建的 pending 页（改内容、补 `created_from`、修链接），改完重跑直到全绿。
- 若红项来自你未创建的存量页（reviewed / 无 status / 工具页）：不动手修改（硬禁令 3），如实向委托人报告存量问题后交付本批——你的交付边界是本批页面合规，不是全库返绿。
- 参考工具：`knowflow fix --dry-run`。只读其输出、自己动手改页；该模式不落盘。
- 铁律重申：**绝不运行不带 `--dry-run` 的 `knowflow fix`**。不带该旗标的修复会创建垃圾占位页、删除未填槽位行，直接毁掉待审稿。
- `knowflow tags`、`knowflow graph`、`knowflow index` 不进合成循环——它们是人审核后的构建动作。

## 6. 交付前自检清单

逐条自检，全部通过才交付：

- (a) 文件位于与其 frontmatter `type` 匹配的页型目录。
- (b) 正文有 H1，且 H1 文本与 frontmatter `title` 一致。
- (c) frontmatter 可解析，`type` / `title` / `created` / `created_from` / `status` 齐全；source 页强烈建议附 `source_url`。
- (d) 必填章节齐全、标题与模板逐字一致（中文标题精确匹配）、顺序一致；必填章节无内容写「无」，可选且无关章节整节省略。
- (e) 无 `{{...}}` 占位符，无模板 HTML 注释等写作指引残留。
- (f) source / entity 页每条核心要点行尾恰好一个 `(EXTRACTED)` 或 `(INFERRED)`；concept / comparison 页不带任何标注。
- (g) 验收线：source 核心要点 3–8 条；entity 2–4 条；concept 的「不同来源的视角对比」表 ≥2 行且引用 ≥2 张不同 source 页；comparison 七个维度行全部填写、对比对象 2–3 个。
- (h) `knowflow health` 三查绿（pending 页按孤儿豁免语义评估）。
