# 冥骨魂殿 / Bone Halls：把"设计"当成可验收的工程交付——AI 技能特效流水线 + 三模型盲评

- 来源 URL：https://hk.v2ex.com/t/1228361 （V2EX《用 Claude Design / GPT-5.6-sol / Kimi K3 给我的游戏做技能特效，附三份可玩的 standalone》）
- 相关：skill 仓库 https://github.com/joeeeeey/open-design-skill ；游戏 https://bonehalls.com （网页内测，计划上 Steam）
- 模型/工具：Claude Design（生产基准）；Open Design × GPT-5.6-sol、Open Design × Kimi K3（挑战者）；Playwright 录像 + GPT-5.6-sol 当盲评裁判；Phaser 4.1
- 游戏类型：哥特埃及题材类吸血鬼幸存者 Roguelike（H5）
- 结果证据：三份可交互 standalone
  - Claude Design 基准（已上线）https://artifact.cafe/a/54b9lvjsge
  - GPT-5.6-sol 版（盲评 91）https://artifact.cafe/a/2pcxiumquv
  - Kimi K3 版（盲评 82）https://artifact.cafe/a/q5mo9j3mm2
  - 游戏本体可网页试玩
- 热度：低（抓取时 0 回复）
- 生成方式：多轮流水线（每个技能：handoff 包 → 一轮生成 standalone → 自动验收 gate + 盲评 → 移植进 Phaser 并做保真门）

## 流程原文（作者）

> 核心思路：把「设计」当成一份可验收的工程交付(pipeline with skills)，而不是一句 prompt 。
>
> Handoff 包生成 skill：每个设计需求打成一个自包含 zip —— 真实游戏截图、机制数值表、视觉正交规则（新技能不和老技能相似）、性能预算等。这个 zip 会扔给 claude design 作为需求，并且定义交付标准。
> 生成：设计系统返回一个自包含的交互式 standalone HTML —— 不是一张图，是能玩的可调参数的网页，还要暴露一个脚本化 API 方便我自动验收让 AI 接入。
> 独立验收：用 Playwright 录像截图，跑一套硬性 gate 后丢给另一个模型盲评打分。
> 移植：过审的 standalone 走 takeover 流程进 Phaser —— 深读它的源码（ painter / 时间轴 / 锚点），±5% 保真门，真机 ADB 录像验证。

## 这次实验的"规格"（技能描述原文）

> 做的技能是「巫毒魂瓶」：瓶子在敌人之间弹跳，每跳眩晕 + 咒印，5 秒诅咒窗口内伤害叠加，期满一次性结算爆发（灵感来自 DOTA 巫医的麻痹药剂 + 诅咒）。
> 同一份生产 handoff zip 一字不改，喂给本地的 pipeline （ Open Design + 前沿模型），一轮生成能不能摸到这个生产基准的水位？
> 两个挑战者之间做严格盲评：等时驱动录像、抽等时关键帧、匿名乱序，GPT-5.6-sol （ high reasoning ）按 100 分表当裁判。

结果：
> GPT-5.6-sol 91 分，Kimi K3 82 分 —— 两份都摸到了「可以进 owner 审阅」的水位，这在 1 个月前是不敢想的。

## 备注

不是"整个游戏一次生成"，而是把游戏拆成可独立验收的资产单元（一个技能 = 一个 standalone），每个单元带：参照截图、数值表、与既有内容的差异约束、性能预算、脚本化验收接口。handoff 包内容本身未公开（作者说正在泛化成模板），所以只有结构、没有全文。
