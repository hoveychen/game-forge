# Ayi1337：GPT-6 Astra 两次 One Shot——"最短时间"中文一句话 vs 精心写的英文 Remaster 规格（瓜体实验室 / Mosswing）

- 来源 URL：https://github.com/Ayi1337/gpt6-astra-one-shot-games （2026-09-05，54 stars；被 awesome-gpt-6-astra 收录）
- 模型/工具：GPT-6 Astra（Mosswing 标注 Xhigh，用时 21 分钟），产物托管在 chatgpt.site
- 游戏类型：①半流体物理合成（西瓜游戏变体）②移动端 3D 单键飞行（Flappy-like）
- 结果证据：
  - 瓜体实验室 https://melon-game.jack-514.chatgpt.site
  - Mosswing https://mosswing-quiet-flight.jack-514.chatgpt.site/
  - 仓库保留 HTML 产物与源码
- 热度：54 stars
- 生成方式：两次都是一次生成（One Shot）

## Prompt 原文

01 瓜体实验室：
```text
用最短的时间设计一款全新概念（物理性质）的半流体西瓜游戏（html游戏）
```

02 Mosswing（作者说明："上一轮 Prompt 加了时间限定词，这次去掉时间限定"）：
```text
Remaster the classic "tap-to-flap" game — the one where you tap to keep a small creature airborne while gliding through an endless series of gaps — as a 3D game playable in a mobile browser. One index.html, opens and plays instantly, no external assets (CDN libraries are allowed; your call).  Keep the core exactly as everyone remembers it: one-tap control, gravity, gaps that scroll toward you, one hit and you're done, score is gaps passed. Everything else is yours to decide: what the creature is, what the obstacles are, the world, the camera, the feel of the flap, how far to take the visuals. Design an original character and style rather than copying the original's art. I won't answer clarifying questions.  I'm judging a complete, elegant, great-feeling piece of work — not a feature list. Small and finished beats big and rough.
```

## 备注

Mosswing 的 prompt 是本批次里最干净的"one-shot 规格写法"范例：①锁死核心循环（逐条列出不可改的规则）②显式放权其余一切（角色、世界、镜头、手感）③交付形态约束（单文件、即开即玩、无外部资源）④预先声明不回答澄清问题⑤给出评判标准（完整、优雅、手感好；"Small and finished beats big and rough"）。作者自己把"去掉时间限定词"当作一个变量来对照，但没给出两次结果的质量对比文字，只能看成品自行判断——证据中等。
