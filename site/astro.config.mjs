import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// Sidebar labels are translated per locale via `translations`; the `← Website`
// link points at the English landing, which auto-redirects zh browsers to /zh/.
const withZh = (en, zh) => ({ label: en, translations: { zh, 'zh-CN': zh } });

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
      sidebar: [
        { ...withZh('← Website', '← 官网'), link: '/flowtest/' },
        { ...withZh('Introduction', '简介'), slug: 'intro' },
        { ...withZh('Quickstart', '快速开始'), slug: 'quickstart' },
        { ...withZh('The flow format', '流程格式'), slug: 'flow-format' },
        { ...withZh('The engine loop', '引擎循环'), slug: 'engine' },
        { ...withZh('Demo site', '演示站点'), slug: 'demo-site' },
        { ...withZh('Knowledge base', '知识库'), slug: 'kb' },
        {
          ...withZh('GitHub', 'GitHub'),
          link: 'https://github.com/jerryjiao/flowtest',
        },
      ],
      customCss: ['./src/styles/starlight-tweaks.css'],
    }),
  ],
});
