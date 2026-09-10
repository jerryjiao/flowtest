---
title: 描述用户旅程，让代理在真实浏览器里测试它
description: 把"用户能把商品加入购物车并结账"这样的描述变成 .flow.yaml 文件，你的编码代理在真实浏览器里逐步执行，每一步带截图和耗时记录，失败写成笔记供下次运行参考。开源，运行在你已有的代理里。
template: splash
hero:
  tagline: 开源，MIT 协议。你说"用户能把商品加入购物车并结账"，flowtest 把这句话变成 .flow.yaml 文件；你的编码代理在真实浏览器里逐步执行，每一步记录截图和耗时，失败写成笔记，下次运行自动避开。
  image:
    html: |
      <div class="ft-card">
        <div class="ft-card-bar"><i></i><i></i><i></i><span class="ft-card-file">demo-smoke.flow.yaml</span></div>
        <pre><span class="k">flow:</span> <span class="s">demo-smoke</span>
      <span class="k">sut:</span> <span class="s">demo-site</span>
      <span class="k">vars:</span>
        <span class="k">DEMO_USER:</span> <span class="s">demo@flowtest.dev</span>

      <span class="k">steps:</span>
        - <span class="k">id:</span> <span class="s">fill-email</span>
          <span class="k">action:</span> <span class="s">fill</span>
          <span class="k">target:</span> <span class="s">"textbox 'Email'"</span>
          <span class="k">value:</span> <span class="s">"{{DEMO_USER}}"</span>

        - <span class="k">id:</span> <span class="s">submit-signin</span>
          <span class="k">action:</span> <span class="s">click</span>
          <span class="k">target:</span> <span class="s">"button 'Sign in'"</span>
          <span class="k">expect:</span>
            - <span class="k">element:</span> <span class="s">"heading 'Tasks'"</span>
            - <span class="k">not_text:</span> <span class="s">"Invalid credentials"</span>

        - <span class="k">id:</span> <span class="s">complete-task</span>
          <span class="k">action:</span> <span class="s">click</span>
          <span class="k">target:</span> <span class="s">"checkbox 'Buy oat milk'"</span></pre>
      </div>
  actions:
    - text: 跑通第一条流程
      link: /flowtest/zh/quickstart/
      variant: primary
      icon: right-arrow
    - text: GitHub
      link: https://github.com/jerryjiao/flowtest
      variant: secondary
      icon: github
---

<section class="ft-lead">
  <p class="ft-lead-strip">
    <span>流程是一个 YAML 文件</span>
    <span>运行在你已有的编码代理里</span>
    <span>不装守护进程</span>
  </p>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>它测的是单元测试看不到的那一层</h2>
    <p>改版改掉了按钮的名字，结账流程悄悄断掉——这类问题单元测试和 CI 发现不了</p>
  </div>
  <div class="ft-duo">
    <div class="ft-pain">
      <p>单元测试检查一个个函数，集成测试检查一个个接口。而<em>用户能不能走完整段旅程</em>——注册、加购物车、结账——这一层，大多数项目没有任何测试在看守。</p>
      <p>flowtest 补上这一层：你用一句话描述旅程，代理把它变成可以反复执行的浏览器测试。</p>
    </div>
    <figure class="ft-shot">
      <img src="/flowtest/demo.gif" alt="演示：代理驱动浏览器完成登录、建任务、完成任务并读取计数" />
      <figcaption>实拍：demo-smoke 流程——登录 → 建任务 → 完成 → 读取计数。9 步全部通过，用时 70 秒。</figcaption>
    </figure>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>一个循环，四个动作</h2>
    <p>代理每次运行流程都走同一条路径</p>
  </div>
  <div class="ft-feats">
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="19" r="2"/><circle cx="18" cy="3" r="2"/><path d="M8 19h6a4 4 0 0 0 0-8h-4a4 4 0 0 1 0-8h6"/></svg></div><b>Plan 计划</b><span>你用自然语言描述旅程，代理把它写成 <code>.flow.yaml</code>：步骤、目标、期望条件。新文件先给你确认，确认后才执行。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg></div><b>Run 执行</b><span>代理在真实浏览器里逐步执行。目标用语义定位器写（按钮 <code>'Sign in'</code>），不写 CSS 选择器。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1"/><path d="M9 12h6M9 16h4"/></svg></div><b>Report 报告</b><span>每一步记录 PASSED / HEALED / FAILED / SKIPPED，附截图和耗时。结果先写成 JSON 文件，再生成给人读的报告。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></div><b>Learn 学习</b><span>失败写成笔记：什么坑、影响哪些流程、怎么避开。下一次计划自动读取这些笔记。</span></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>三步跑通第一条流程</h2>
    <p>全程在你已有的编码代理里完成，不安装新东西</p>
  </div>
  <div class="ft-steps">
    <div class="ft-step"><span class="n">1</span><b>伺服演示站</b><span>仓库自带一个零依赖的演示站点，一条命令启动。</span><code>python3 -m http.server 4173 -d demo</code></div>
    <div class="ft-step"><span class="n">2</span><b>让代理执行</b><span>对代理说出要运行的流程文件，引擎接手：先校验，再解析变量，然后打开浏览器。</span><code>运行 demo-smoke.flow.yaml</code></div>
    <div class="ft-step"><span class="n">3</span><b>读报告</b><span>结论、每步状态、截图、耗时，全部落在 flowtest/reports/ 目录。</span><code>flowtest/reports/*.result.json</code></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>代理只做执行，决定权在你</h2>
    <p>三条边界写在引擎规程里，代理不能越过</p>
  </div>
  <div class="ft-bounds">
    <ul>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>新计划要先经你确认，代理才会打开浏览器。确认过的流程重跑不再询问。</span></li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>凭据不写进流程文件：运行时从环境变量或 .env 占位符读取。</span></li>
      <li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg><span>每个动作对应真实的浏览器操作，代理不会发明替代动作。</span></li>
    </ul>
    <p class="ft-quote">flowtest 以代理技能的形式发布。你已有的编码代理（Claude Code、zcode，或任何支持 SKILL.md 约定的宿主）就是运行时——没有独立的测试框架，也没有守护进程。</p>
  </div>
</section>

<section class="ft-section">
  <div class="ft-section-head">
    <h2>六个设计决定</h2>
    <p>每一条都对应文档里的完整说明</p>
  </div>
  <div class="ft-grid">
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div><b>流程是 YAML 文件</b><span>一个文件一屏读完，能机器校验。放进版本库，参加 code review。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg></div><b>语义定位器</b><span>目标写角色和名字，不写选择器。控件没有可访问名时会被报出来——那是应用的可访问性问题。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 2v6"/><path d="M15 2v6"/><path d="M6 8h12v3a6 6 0 0 1-12 0z"/><path d="M12 17v5"/></svg></div><b>执行器不绑定</b><span>宿主有浏览器 MCP 工具就用它，没有就用 agent-browser 命令行。同一份流程，换宿主照跑。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg></div><b>证据随报告落盘</b><span>失败和自愈的步骤自动截图。结果 JSON 先写盘，再输出摘要。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 11.5 11 13.5 15 9.5"/></svg></div><b>自愈有上限</b><span>每步最多重试 2 次，重试策略记录在报告里。放宽过的断言会标注清楚：HEALED 弱于 PASSED。</span></div>
    <div class="ft-feat"><div class="ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div><b>知识库可选</b><span>不配置知识库也能用全部功能。Learn 退化为 flowtest/lessons/ 下的 Markdown 笔记。</span></div>
  </div>
</section>

<section class="ft-section">
  <div class="ft-cta">
    <h2>从第一条旅程开始</h2>
    <p>克隆仓库、启动演示站、运行 demo-smoke——两分钟内看到 PASS。</p>
    <a class="cta" href="/flowtest/zh/quickstart/">开始 →</a>
  </div>
</section>
