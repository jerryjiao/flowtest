import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import { readFileSync } from 'node:fs';

// Sidebar labels are translated per locale via `translations`. The old
// `← Website` sidebar link is gone: the splash homepage IS the docs home.
// zh browsers hitting the English homepage auto-redirect via pages script.
const withZh = (en, zh) => ({ label: en, translations: { zh, 'zh-CN': zh } });

// Plugin version from the repo manifest — the changelog sidebar label
// picks it up automatically on every release (ai-study-kit recipe).
const VERSION = JSON.parse(
  readFileSync(new URL('../.claude-plugin/plugin.json', import.meta.url), 'utf8'),
).version;

export default defineConfig({
  site: 'https://jerryjiao.github.io',
  base: '/flowtest/',
  integrations: [
    starlight({
      title: 'flowtest',
      description:
        'Natural-language browser testing for coding agents: describe the journey, your agent turns it into a .flow.yaml plan, runs it in a real browser, reports, and learns from failures.',
      logo: { src: './src/assets/logo.svg', alt: 'flowtest logo' },
      favicon: '/favicon.svg',
      defaultLocale: 'en',
      locales: {
        en: { label: 'English', lang: 'en' },
        zh: { label: '简体中文', lang: 'zh-CN' },
      },
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/jerryjiao/flowtest' }],
      sidebar: [
        {
          ...withZh('Get started', '开始'),
          items: [
            { ...withZh('Introduction', '简介'), slug: 'intro' },
            { ...withZh('Quickstart', '快速开始'), slug: 'quickstart' },
          ],
        },
        {
          ...withZh('Reference', '参考'),
          items: [
            { ...withZh('The flow format', '流程格式'), slug: 'flow-format' },
            { ...withZh('The engine loop', '引擎循环'), slug: 'engine' },
          ],
        },
        {
          ...withZh('Resources', '资源'),
          items: [
            { ...withZh('Demo site', '演示站点'), slug: 'demo-site' },
            { ...withZh('Knowledge base', '知识库'), slug: 'kb' },
          ],
        },
        {
          label: `Changelog · v${VERSION}`,
          translations: { zh: `更新日志 · v${VERSION}`, 'zh-CN': `更新日志 · v${VERSION}` },
          slug: 'changelog',
        },
      ],
      customCss: ['./src/styles/custom.css'],
      head: [
        {
          tag: 'meta',
          attrs: { property: 'og:image', content: 'https://jerryjiao.github.io/flowtest/og.png' },
        },
        { tag: 'meta', attrs: { property: 'og:type', content: 'website' } },
        { tag: 'meta', attrs: { name: 'twitter:card', content: 'summary_large_image' } },
      ],
    }),
  ],
});
