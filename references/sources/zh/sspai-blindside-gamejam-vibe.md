# 少数派：《茫室 Blindside》——两人 Game Jam 100% Vibe Coding 复盘

- 来源 URL：https://sspai.com/post/110972 （《AI 工作流实践：100% Vibe Coding 完成 Game Jam 游戏开发》，少数派 Matrix 精选）
- 游戏：https://blasin.itch.io/blindside ；机核 https://www.gcores.com/games/179928
- 模型/工具：Cursor（主力 Agent，含 Continual Learning 记忆插件、Debug Mode）、Codex（补充）、Claude（分析）；Unity + Unity MCP；ElevenLabs 生成全部音乐音效；Notion 写剧本；LDtk 关卡
- 游戏类型：俯视角射击（核心机制：敌人在光中无敌，只能在阴影里预判击杀），Unity，出 iOS/Android/WebGL
- 团队：2 人（Blasin 程序 / Frank 美术关卡）
- 结果证据：itch.io 与机核可玩；作者给出代码统计（约 31,000 行，去年同类 Jam 约 4,000 行）、约 1,000 次提交（去年约 400）、投入约 100 小时
- 热度：少数派 Matrix 精选（文章赞助/支持数约 69，具体点赞数未取到）
- 生成方式：多轮、多会话（整个 Jam 周期）

## 流程要点（原文引用）

资产/配置"模糊转译"：
> 这是一种模糊转译，而 Agent 相当擅长这类工作
（美术随手命名的文件如 `Reload GUI 指示物开启.png` → Agent 统一重命名、整理目录、替换场景引用、更新配置；Notion 剧本 → Agent 抽取转成游戏配置）

Git：
> Agent 像是一种可以用自然语言交互的 Git 客户端
（原子提交、自然语言解决场景冲突、git bisect 定位渲染回归、git worktree 并行修 WebGL）

指代问题（给复杂层级做 deeplink）：
> 当你要指定其中一个敌人的武器时就很难描述
（自制工具栏导出 GlobalObjectId，精确指向实体）

闭环：
> 避免的办法就是把它扔进可以自我验证的闭环之中
（Unity MCP 的 `compile_and_fix` skill：Asset Refresh → 编译 → 查 console → Play 模式冒烟，循环到干净）
> 拒绝盲猜（Debug Mode：列假设、埋日志、要求复现再修）
> Agent 让做实验的门槛大大降低（脚步声、juice 细节这类低优先级功能变得可做）

## 失败/教训（原文引用）

> Mechanics 只是起点
> 前期工程推进有多顺利，后半程发现体验拼不起来时，就有多沮丧
> 光有机制并不足以定义一款完整的游戏
（作者用 MDA 框架解释：Agent 能搞定 Mechanics，搞不定 Dynamics/Aesthetics；美术接入太晚，系统与美学意图后期对不上）
> 抽卡，而不是稳定生产（ElevenLabs 生成音频）
> AI 改变的是生产效率，而非游戏质量本身
> 游戏最后是否成立，仍然要回到体验、审美、测试和人的判断

## 备注

没有单个"大 prompt"，价值在于一个真实上线的双人项目中 agent 用在哪里最值（转译、配置、git、自验证编译循环），以及"机制推进顺利 ≠ 游戏成立"这个后期才暴露的失败模式。WebFetch 摘要转述，引文为原文中文句子。
