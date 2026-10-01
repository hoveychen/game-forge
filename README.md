# game-forge

一个 [Claude Code](https://docs.claude.com/en/docs/claude-code) skill：通过和你讨论，把一句话游戏想法写成一份足够具体的设计文档（GDD），然后把这份文档原样交给一个全新会话，**一次做出来**。

*A Claude Code skill that turns a one-line game idea — through a design conversation with you — into a dense, vivid GDD modeled on a known-good exemplar, then hands that GDD verbatim to a fresh agent session to build in one shot.*

## 为什么是这样

这个 skill 的 v2 来自一组对照：

- **一份好 GDD 直接 one-shot 是成立的。** 社区流传的 Open Blue 设计文档（体素田园 + OSRS 式技能），前面加一行技术栈直接交给 Claude，不到两小时就出了一个九个技能、带光影打磨的完整 MVP。
- **流程会杀死产出。** v1 版本走的是另一条路：一句话想法 + 接力开发纪律（打磨禁令、上百条验收合同、评审打分闸门、改设计要审批）。同一个模型跑了一天半，只做出灰盒，里程碑评审还没过。模型读到一份责任状，就只做被允许的最小的事。

所以 v2 只管**把游戏想清楚、写出来**，执行阶段放手。

## 它做什么

1. **拆原话**：参照作品、主题、你点名的每个要求。
2. **考据**：联网查参照作品的具体机制和数字，作为校准锚点。
3. **逼问**：把 GDD 的各个部分当成一棵设计树，按轮提问，每轮把现在就能问的题一次问完、每题带推荐，一直问到每个分支都问过。数值也问，你答「你定」就由它定。
4. **写全文 GDD**：问完才写，这一步不再提问。按 Open Blue 拆出来的 14 个部分写，用设计师推销自己游戏的口吻，写校准锚点、「不要什么」、ASCII 布局和界面、MVP 清单，以及美术怎么用代码造出来。
5. **自检**：13 条清单，找出最薄的一处当场补齐。
6. **开跑**：新建仓库，GDD 作为唯一的 prompt 交给新会话，其余什么都不加。

**它不会没问就定。** 模型自己「推荐」的选项，按定义就是最常见、最平均的那个。一份 GDD 里不平均的东西，只能来自你的品味。v2 只给一张 pitch 卡，用模拟老板测下来，隐藏偏好只召回了一半多；改成按轮逼问后召回到九成以上，代价是每局大约 4 轮、20 来道题。

## 安装

```bash
git clone https://github.com/hoveychen/game-forge ~/.claude/skills/game-forge
```

然后在 Claude Code 里说「我想做一个……的游戏」，skill 就会自动触发。

## 目录

```
SKILL.md                    入口：目标、铁律、流程
references/
  writing.md                GDD 的结构、写法、品类差异、美术路线、自检清单
  exemplars/open-blue.md    标杆原文
```

v1（接力开发纪律版）保留在 git 历史里：`git checkout 8de289c`。

## 注意

- 文档是中文写的，把用户称作「老板」。
- 默认技术栈是 Godot 最新版 + GDScript，你指定别的就照你的。
- 「讨论出来的 GDD 能达到 Open Blue 同等质量」目前只有少量实测，欢迎提 issue 分享结果，尤其是失败的。

## 许可

本仓库的原创内容（SKILL.md、references/writing.md）采用 [MIT](LICENSE) 许可。

`references/exemplars/open-blue.md` 是在社区流传的一份设计文档，原作者不明，收录它只是为了研究和引证。如果你是作者并希望移除，请提 issue。
