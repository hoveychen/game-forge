# 药灵山谷（中医学习 2D 像素游戏）：小白用 Claude Code 做游戏的多轮踩坑复盘

- 来源 URL：
  - 复盘文章：https://www.cnblogs.com/gogoSandy/p/19948386 （博客园「风雨中的小七」，《和AI一起搞事情#4. 小白用claude code做游戏究竟能踩多少坑》）
  - 仓库：https://github.com/DSXiangLi/tcm_odyssey （2026-04-06 创建，持续推到 2026-06-09）
- 模型/工具：Claude Code（配 superpowers 技能：brainstorming / writing-plans / systematic-debugging）；Gemini / nanobanana pro 生图；Claude 多模态做地图校验；Hermes-Agent 做 AI NPC
- 游戏类型：2D 像素风 RPG + 经营/教育（种植、诊断、煎药、炮制小游戏，AI NPC 对话），Phaser 3 + TypeScript + Vite
- 结果证据：仓库 assets/ 下有各玩法录屏（clinic_area.mp4、煎药.mp4、辩证.mp4、npc对话.mp4、背包.mp4 等）；CLAUDE.md 进度表显示 Phase 1–2.5 多数完成（"NPC Agent系统 S1-S13, 861测试"、"背包 E2E测试42/42通过"），但种植等仍在开发中，作者承认仍有"人在房檐上走"的 bug
- 热度：低（GitHub 2 stars；博客园文章热度未知）
- 生成方式：多轮、多会话迭代（两个多月，数十份 plans/specs，二十多份 experience 复盘文档）

## 关键教训（复盘文章原文引用）

需求阶段：
> 需求没有被完全澄清，所以AI在所有不完整的需求中，自己YY了一部分

作者一开始跳过了 brainstorming，后来改为先用 `/brainstorming` 把需求澄清完再写码。作者称大部分时间花在 UI/设计文档上，需求落定后编码本身只花了约 2 小时。

测试阶段（"假绿"问题）：
> 模型全面测试通过后，一打开网页——崩溃了、黑屏了
> 因为上下文焦虑带来的"测试失败模型选择跳过"

地图/美术：
> 网格划分得粗了——一个格子里啥都有 / 网格划分得细了——多模态模型根本看不见里面写的数字

行走动画一致性"灾难"：
> 不是没有左边人物侧脸…要么就所有人都迈左脚 / 人往前走，脑袋在后面的

有效的解法：用生图模型生成黑白二值"可行走遮罩"（"无敌的 nanobanana pro，几乎完美地完成了任务"）；动画用"换角色不换姿势参考"保证一致性；调试改用 `/systematic-debugging`（根因→模式分析→假设验证→实现）。

## 仓库内的经验文档（原文摘录）

`docs/superpowers/experience/2026-04-29-e2e-testing-core-lessons.md`：
> **问题**: CSS未导入导致UI空白，但测试报告100%通过。
> **根本原因**: `toBeVisible()` 只检查元素在DOM中存在，不验证实际渲染尺寸和样式。
> **问题**: 测试直接跳转场景，绕过了真实游戏流程，隐藏了入口触发问题。
> **一句话总结**：测试通过了≠用户能用了。必须验证尺寸、样式、真实路径。

`docs/superpowers/experience/2026-05-29-walkable-config-consistency-issue.md`：
> 用户反馈："是的行走域还是不对，当前几乎多数区域都能行走"
> 遮罩层定义: 919个可行走瓦片（22.3%占比）；实际配置: 1837个可行走瓦片（44.5%占比）
> 问题: tests目录有完整分析结果，但src/data没有正确复制使用。
> 临时修复心态：问题: 路径不连通…方案: 手动添加路径矩形区域 ❌ 正确: 重新分析遮罩层或调整遮罩层本身 ✓
> 没有明确文档说明"可行走配置的唯一数据源是什么"

## 项目的多会话骨架（CLAUDE.md 原文）

> 文档职责划分（渐进式加载）：PROGRESS.md 进行中任务 / STATE.md 已完成任务 / CLAUDE.md 快速索引 / docs/superpowers/experience/ 经验教训
> 每个设计文档和规划文档写完之后必须使用subagent模式调用 design-doc-reviewer 技能对文档进行独立审核
> 目标+标准驱动执行：定义成功标准。循环直到验证通过。"修复 bug"：编写一个能复现该 bug 的测试，然后使其通过

## 备注

这是本批次最完整的"长周期、非 one-shot"中文复盘：有对话外的持久化文档体系（CLAUDE.md/PROGRESS/STATE/experience），也有大量失败证据。核心失败模式：(1) 需求不澄清→模型自行脑补；(2) 测试只断言 DOM 存在→"测试全绿但黑屏"；(3) 同一数据（可行走区域）多处维护，模型"临时修复"破坏单一数据源；(4) 美术资产（地图、行走帧）一致性远比代码难。
