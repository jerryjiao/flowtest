// sync-changelog.mjs — 把仓库根 CHANGELOG.md 同步成 Starlight 的 changelog 页
// （site 内为生成物，勿手编；ai-study-kit sync-docs.mjs 的单文件简化版）。
// CHANGELOG.md 用英文维护（与 GitHub Releases 一致）；zh 页同内容、仅标题本地化，
// 避免每次发版双倍翻译。运行：site 的 prebuild 自动跑。
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const siteRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const src = resolve(siteRoot, '../CHANGELOG.md');
const outBase = resolve(siteRoot, 'src/content/docs');

const text = readFileSync(src, 'utf8');
// 抽首个 H1 之后的正文，H1 换成 frontmatter title，避免与页面头重复。
const body = text.replace(/^#\s+.*\n/, '').trim();

const TITLES = { en: 'Changelog', zh: '更新日志' };
for (const [locale, title] of Object.entries(TITLES)) {
  const dir = resolve(outBase, locale);
  mkdirSync(dir, { recursive: true });
  const page = `---\ntitle: ${title}\ndescription: flowtest 的版本更新记录。\n---\n\n${body}\n`;
  writeFileSync(resolve(dir, 'changelog.md'), page);
  console.log(`changelog -> src/content/docs/${locale}/changelog.md`);
}
