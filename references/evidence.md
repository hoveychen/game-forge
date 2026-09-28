# 证据索引

2026-09-28 由五路搜索汇总（X/博客、GitHub、Reddit/HN、中文社区、方法论/评测），原文在 `sources/` 下，每个文件头部有来源 URL、模型、结果证据和热度。多数质量判断来自作者自述，厂商案例（OpenAI、GPT-5 画廊）是精选的，引用时注意这一点。

## 总结论

1. **harness 决定做不做得完，规格决定做出什么。** 反例 Quasar Saz：一只狗在键盘上乱敲出的「规格」，配上很重的测试和截图 harness，照样做完了一个完整的游戏（`github/quasar-saz-dog-designed.md`）。Anthropic 用游戏做的测试里，单 agent 版本「对输入毫无反应」，加上规划者、生成者和一个持怀疑态度、用 Playwright 真去玩的评审之后才变得可玩（`methods/anthropic-harness-design-long-running-apps.md`）。
2. **「一句话出惊艳成品」几乎都是复刻名作。** 原作就是规格（`x-blogs/claude-of-duty-shumer.md`、`zh/riba2534-opus55-oneshot-3d.md`、`github/world-of-claudecraft.md`）。模型不熟悉的参考作品会失败（`x-blogs/FAIL-pitfall-winterspeak.md`）。
3. **「一次成功」多半是营销。** 真实模式是一段种子 prompt，接着数小时到数天的自主循环，再加上人类的试玩反馈。作者自述种子 prompt 只占结果的约 20%（`x-blogs/` 观察 5）。
4. **流传的长 GDD 常常是做完之后反向整理的**，不是原始输入（`zh/pokitx-*`、`zh/thunderfall-*`、`x-blogs/claudepunk-*`）。

## 按失败模式

### 1. 接力很久，前几步仍然走不通，agent 却在打磨细节

| 结论 | 来源 |
|---|---|
| 坏掉的主因是「写了但没接进运行中的游戏」 | `methods/gamexpert-bench.md`、`methods/opengame-debug-skill.md` |
| 编译通过率高，端到端可玩率接近零 | `methods/playcoder-play-at-k.md` |
| 每次开工前先验证核心流程，修好再做新功能 | `methods/anthropic-harness-prompts-verbatim.md` |
| 光在 prompt 里要求不够，要用 hook 强制 | `methods/anthropic-harness-prompts-verbatim.md`、`reddit-hn/quizhp-*` |
| agent 自我接受率 100%，其中 56% 的轮次实际没有进展 | `methods/progress-mirage-self-evaluation-bias.md` |
| 状态注入加关键点检查与人工判断一致率 92%，自由探索只有 59% | `methods/gamegen-verifier-keypoint-state-injection.md` |
| 公开的翻版：第一分钟砍不了木头，agent 在做雪地脚印 | `reddit-hn/shardsofstone-rts-scope-creep.md` |
| 胜利条件没生效：进洞之后什么都没发生 | `reddit-hn/golf-is-golfing-hn-critique.md` |
| 52 条断言全绿，机器人试玩 6 局全部暴毙 | `zh/yupi-isaac-roguelike-loop-engineering.md` |
| 设计文档膨胀成日志，旧决定污染新工作 | `reddit-hn/roguelike-context-pollution-pivots.md` |

### 2. 抓不到好玩的点

| 结论 | 来源 |
|---|---|
| 先做玩具；重主题救不了糟糕的设计 | `methods/gabler-prototype-7-days.md` |
| 用 MDA 八种体验代替「好玩」 | `methods/mda-framework-and-meeplelm.md` |
| 游戏「住在」一个循环里，先做手感 | `x-blogs/kart-royale-ryancampbell.md` |
| 具体的随机种子比「要有创意」有效 | `reddit-hn/quizhp-autonomous-game-factory.md` |
| AI 内容偏浅；AI 试玩者只发现界面问题 | `reddit-hn/ripple-content-game-hn.md` |
| 从约束出发提问，而不是让 AI 发明游戏 | `reddit-hn/matchinko-steam-16days.md` |
| 模糊 prompt 会让模型的默认偏好（视觉或动效）决定游戏是什么 | `reddit-hn/supplementary-quotes.md` |
| 「技术上它几乎都对，错的是游戏本身」 | `reddit-hn/supplementary-quotes.md` |

### 3. 头痛医头，推给老板，改得敷衍

| 结论 | 来源 |
|---|---|
| 补丁叠补丁，局部检查全过，整体是坏的；按规格重做 | `reddit-hn/backpressure-snes-shortcut-system.md` |
| 截图评审发现不了玩法 bug | `x-blogs/kart-royale-ryancampbell.md` |
| 分档评分表让评审循环有了终点 | `x-blogs/kart-royale-ryancampbell.md` |
| 试玩是团队的责任，不是用户的 | `methods/play2code-playtestarena.md`、`methods/openai-codex-*` |
| 玩家擅长发现问题，不擅长给方案 | `methods/rosewater-20-lessons-feedback.md`、`methods/valve-playtesting-*` |
| 裁定钉在测试上；决策文件防止反复争论 | `reddit-hn/connexus-induction-overnight-fleet.md` |
| 加护栏，而不是「下次小心」 | `reddit-hn/matchinko-steam-16days.md` |
| agent 执行数值指令时指出系统性后果 | `reddit-hn/proof-carrying-puzzles-and-pushback.md` |
| 手感是人的工作；游戏内编辑器 | `reddit-hn/alien-pinball-postmortem.md` |

## 值得完整读的样板

| 用途 | 文件 |
|---|---|
| 一页纸 Brief 的格式 | `reddit-hn/worldbuild-bench-pinned-briefs.md` |
| 完整系统沙盒 GDD | `exemplars/open-blue.md` |
| 极简 prompt 加严苛评审循环 | `x-blogs/claude-of-duty-shumer.md` |
| 复刻名作的中文 prompt 范本 | `zh/yupi-isaac-roguelike-loop-engineering.md` |
| 「锁死核心规则、其余放权」的写法 | `zh/ayi1337-astra-oneshot-mosswing.md` |
| 20 节的超长规格 | `x-blogs/dust-corridor-leonlin-20section.md` |
| web 游戏的可测性接口约定 | `github/_harness-openai-develop-web-game-skill.md` |
| 长期多会话项目的踩坑复盘 | `zh/tcm-odyssey-claude-code-pitfalls.md`、`github/archer-wars.md` |

## 尚未解决的分歧

- **标准定多高？** Shumer 派认为不可达的标准是故意的，质量只取决于跑多久；Kart Royale 认为分档评分表才让循环真正有效。本 skill 采用分档，因为老板的痛点是停不下来和空转。
- **规格写多细？** Dust Corridor 规定了整条渲染管线，Shumer 只写了 ThreeJS，结果相当。现有证据倾向于：写清「做什么」和「不许发生什么」，「怎么做」放权。
