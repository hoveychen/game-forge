---
name: game-forge
description: Use when the user wants to plan or build a video game with an AI agent — turning a rough game idea into a design doc, starting a new game project, or continuing / rescuing a multi-session game build that is unplayable, stuck polishing details, or not fun.
---

# Game Forge

把一个游戏想法变成「能闭环、有乐趣、能被接力做完」的项目。分两个阶段：**规划**（和老板一起产出设计文档，并把开发纪律装进项目仓库）和**接力开发**（每一棒按仓库里的纪律干活）。

两条来自真实案例的总结论（详见 `references/evidence.md`）：

- **harness 决定做不做得完，规格决定做出什么。** 验证和纪律缺位时，再好的规格也会烂尾。
- **复刻名作是捷径，原创是难点。** 原创游戏的规划，就是补上那份不存在的「原作规格」。

## 这个 skill 要防的三种失败（都是真实发生过的）

1. **接力 30–40 棒，游戏前 3 步就走不下去，agent 却一直在打磨无关细节。** 根因：没人从头玩过这个游戏；每一棒只看得到局部，挑最容易「完成」的事做。
2. **游戏抓不到好玩的点，尤其是内容驱动的游戏。** 根因：没有明确的乐趣假设；内容被当成写完系统后的填充物，填进去的是最平均的内容。
3. **头痛医头、推给老板「去找人试玩」，拿到反馈又敷衍地改。** 根因：agent 没有自我验证手段；把反馈当 bug 单而不是体验诊断；写代码的人在评审自己。

下面每一条规则都对应其中至少一种失败。**违反规则的字面就是违反规则的精神**，不接受「这次情况特殊」。

## 铁律

1. **主线通关脚本红了，什么别的都不许做。** 主线必须用真实输入跑通。先修到绿。
2. **行走骨架先于一切打磨。** 灰盒把整条主线跑通之前，不碰美术、特效、音效、设置菜单、非必要重构。
3. **每一棒只做一件事，并写明它让游戏离乐趣假设或主线通关更近了什么。** 写不出来就不做。
4. **反馈先诊断再动手。** 走反馈协议（见 `templates/RELAY.md`），不许直接改第一个想到的表面方案。
5. **写代码的不评审自己。** 里程碑验收由一个全新上下文、没有写权限、自己动手玩的评审 agent 做。
6. **自己能验证的，不许推给老板。** 推给老板的必须是具体、可回答的品味问题，附截图或参数。
7. **纪律用 hook 强制，不只写在文字里。** 验证必须是阻断式的。

## 先判断现在处于哪一步

```
项目仓库里有 GAME.md？
├── 有 → 接力开发阶段：读仓库里的 RELAY.md，按「开工三步」执行
└── 没有
    ├── 已有代码但玩不通/不好玩 → 抢救模式（references/planning.md 末尾）
    └── 只有想法 → 规划阶段（references/planning.md）
```

## 规划阶段产出什么

规划不是「写一份文档」，而是把北极星和纪律**装进项目仓库**，让之后每一棒都绕不开：

| 文件 | 作用 | 模板 |
|---|---|---|
| `GAME.md` | 唯一设计依据：老板原话、一页纸 Brief、乐趣假设、系统、资源流、不变式、MVP 边界、主线通关路径、里程碑、设计决策日志 | `templates/GAME.md` |
| `RELAY.md` | 接力纪律：开工三步、红灯规则、完成的定义、选活、打磨禁令、重做不打补丁、独立评审、反馈协议、停机条件、借口对照表 | `templates/RELAY.md` |
| `HANDOFF.md` | 每棒交接记录，第一行永远是主线通关状态 | RELAY.md 内有格式 |
| `BUGLOG.md` / `PLAYTEST.md` | 缺陷根因日志 / 待老板试玩的具体问题队列 | RELAY.md 内有格式 |
| `GAME_GUIDE.md` | 玩家指南，评审 agent 靠它来玩 | planning.md A7 |
| `ART_DIRECTION.md` + `docs/visual/` | 美术圣经与参考图 | planning.md A7 |
| 主线通关脚本 + 关键点检查 | 真实输入驱动的自动玩家；状态注入的系统检查 | planning.md A6 |
| `.game-forge/check-relay.py` | SessionStart + Stop hook，强制收工前重跑主线、写交接 | `templates/hooks/check-relay.py` |
| `CLAUDE.md` 片段 | 让任何进入仓库的 agent 先读 RELAY.md | `templates/CLAUDE-snippet.md` |

## 参考资料

- `references/planning.md` — 规划阶段的完整流程（A0–A8）与抢救模式。**规划阶段必读。**
- `references/genre-lenses.md` — 不同品类的乐趣时间尺度、MVP 问题、可自验程度，带证据等级。
- `references/evidence.md` — 所有规则背后的案例索引，以及值得完整读的样板。
- `references/open-blue-anatomy.md` — 一份高质量游戏设计文档的拆解。
- `references/exemplars/`、`references/sources/` — 案例原文（约 90 份）。
