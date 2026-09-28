# game-forge

一个 [Claude Code](https://docs.claude.com/en/docs/claude-code) skill：和 AI agent 一起，把一个游戏想法变成**能闭环、有乐趣、能被多个会话接力做完**的项目。

*A Claude Code skill for planning and building video games with AI agents — turning a rough idea into a design doc, and keeping long multi-session builds playable, on-scope, and fun. Rules are backed by ~90 real-world case studies (in Chinese, with English sources).*

## 为什么需要它

直接把一个游戏想法丢给 agent，常见的结果是下面三种失败：

1. **接力几十棒，游戏前 3 步就走不下去，agent 却在打磨无关细节。**
2. **做出来的游戏抓不到好玩的点**，尤其是依赖内容和创意的游戏。
3. **头痛医头**：让你「去找人试玩」，拿到反馈后又敷衍地改。

从约 90 个社区案例和工程文章里能总结出两条规律：

- **harness（验证与纪律）决定游戏能不能做完，规格只决定做出来的是什么。**
- **复刻名作是 AI 做游戏的捷径，原创才是难点。** 原作本身就是一份完整的规格；原创游戏的规划，就是把这份不存在的规格补出来。

## 它做什么

分两个阶段：

**规划阶段**。agent 负责出具体的草稿，你负责提供品味、做取舍。这个阶段会产出一份设计文档，并把开发纪律直接装进游戏仓库：

| 文件 | 作用 |
|---|---|
| `GAME.md` | 唯一的设计依据：你的原话、一页纸 Brief、乐趣假设、系统卡、资源流表、不变式、MVP 边界、主线通关路径、里程碑、设计决策日志 |
| `RELAY.md` | 接力纪律：开工三步、红灯规则、完成的定义、打磨禁令、「重做，不打补丁」、独立评审、反馈协议、借口对照表 |
| `HANDOFF.md` / `BUGLOG.md` / `PLAYTEST.md` | 交接记录（第一行永远是主线通关状态）、缺陷根因日志、给你的试玩问题队列 |
| 主线通关脚本 + 关键点检查 | 用真实输入驱动的自动玩家，外加通过状态注入逐个检查系统 |
| `.game-forge/check-relay.py` | Claude Code hook：本会话改了代码，就必须重跑主线、写好交接，否则不让收工 |

**接力开发阶段**。之后每一个会话都要先跑主线通关：主线是红的，就只许修主线；每一棒只做一件事；里程碑由一个看不到代码、需要自己动手去玩的独立评审 agent 来验收。

## 安装

```bash
git clone https://github.com/hoveychen/game-forge ~/.claude/skills/game-forge
```

然后在 Claude Code 里说「我想做一个游戏……」，或者「帮我救一下这个玩不通的游戏项目」，skill 就会自动触发。

## 目录

```
SKILL.md                      入口：三种失败、七条铁律、阶段判断
references/
  planning.md                 规划流程 A0–A8 + 抢救模式
  genre-lenses.md             品类透镜（乐趣时间尺度、可自验程度、证据等级）
  evidence.md                 每条规则背后的案例索引
  open-blue-anatomy.md        一份高质量 GDD 的拆解
  exemplars/  sources/        案例原文摘录（约 90 份）
templates/
  GAME.md  RELAY.md  CLAUDE-snippet.md
  hooks/check-relay.py
```

## 注意

- 文档是中文写的，把用户称作「老板」。
- 证据有局限：多数案例的质量判断来自作者自述，厂商展示的案例是精选过的。`genre-lenses.md` 里每个品类都标了证据等级，JRPG 目前没有案例支撑，只是推理。
- 这些规则还没有经过系统的对照实测。欢迎提 issue 分享你的使用结果，尤其是失败的案例。

## 许可

本仓库的原创内容（SKILL.md、references 中的分析文档、templates）采用 [MIT](LICENSE) 许可。

`references/sources/` 和 `references/exemplars/` 里是第三方内容的摘录，版权属于原作者，收录它们只是为了研究和引证，每个文件都注明了来源链接。其中 `exemplars/open-blue.md` 是在社区流传的一份设计文档，原作者不明。如果你是某份内容的作者并希望移除，请提 issue。
