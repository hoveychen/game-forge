# 三分天下 · 百将风云：一句"做款三国志11"起步、五轮口语需求迭代出的网页策略游戏（GPT-6 Astra / Codex）

- 来源 URL：
  - https://github.com/MartinDelophy/awesome-gpt-6-astra/tree/main/works/three-kingdoms
  - 需求原文：works/three-kingdoms/PROMPTS.md；创作记录：works/three-kingdoms/CREATION.md；验证：VALIDATION.md、docs/balance-v2.md
- 创作者：MartinDelophy（awesome-gpt-6-astra 合集维护者，LINUX DO 用户）
- 模型/工具：GPT-6 Astra in Codex（作者确认）；辅助 Codex agents 做规则建议/平衡模拟；独立生图工具生成水墨地形与 3×36 格武将头像图集
- 游戏类型：回合制三国策略（15 城、3 势力、108 武将），React + TypeScript
- 结果证据：在线可玩 https://sanguo-jiangshan.vercel.app ；仓库含源码、回归测试、平衡模拟报告
- 热度：合集 267 stars（单作热度未知）
- 生成方式：多轮迭代（作者明确"not a one-shot result or a benchmark"）

## 需求原文（按顺序，PROMPTS.md "保留中文原文"）

1. > 帮我在桌面做一款三国志11的游戏看看，最好可以在网页上跑的那种
2. > 不用桌面，网页可以打开就好，部署到netlify,不过武将得多一些
3. > 再生成一些武将的头像吧，我觉得这种也很有必要，还有武将太少了，至少得100个，还有数值得平衡一下
4. > 这个处理好之后部署到vercel吧
5. > 完美，遵循仓库规范提交到 https://github.com/MartinDelophy/awesome-gpt-6-astra，注意多语言

头像生图提示词完整保留在 docs/portrait-prompts/{wei,shu,wu}-prompt.txt（每势力一张 6×6 图集）。

## 迭代内容（CREATION.md 原文）

> 初版网页在用户要求下扩展为 108 位武将、每人独立头像；随后调整三方开局资源和道路结构、统兵上限、智略收益、征兵士气、武将休整与 AI 情报公平。
> Finite simulations do not establish equal human-player win rates or guarantee a fixed campaign length.

## 备注

证据中等：可玩、源码和逐条需求都在，但作者就是合集维护者、无第三方评价。价值在于它是"极简起点 + 用户只给数量/方向型反馈（多一些武将、至少 100 个、平衡一下）"的纯口语多轮样本，与 THUNDERFALL 的"长愿望单一次给出"形成对照。美术走外部生图 + CSS 图集，而不是程序绘制——策略类游戏里头像这种"内容资产"是模型代码生成无法替代的部分。
