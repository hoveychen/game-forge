# icebear0828：Vibe Games Arcade —— Opus 5.5 一句话复刻 LOL / Minecraft / PVZ / 杀戮尖塔

- 来源 URL：https://github.com/icebear0828/vibe-games （2026-09-25 创建，2 次提交）
- 模型/工具：Claude Opus 5.5（具体 agent 宿主未注明；产物均为 React 19 + Vite + Tailwind + vite-singlefile 结构）
- 游戏类型：MOBA 仿真、3D 体素沙盒、塔防、卡牌 Roguelike
- 结果证据：GitHub Pages 在线可玩
  - 总入口 https://icebear0828.github.io/vibe-games/
  - LOL https://icebear0828.github.io/vibe-games/lol/
  - Minecraft https://icebear0828.github.io/vibe-games/minecraft/
  - PVZ https://icebear0828.github.io/vibe-games/pvz/
  - 杀戮尖塔 https://icebear0828.github.io/vibe-games/sts/
  - 源码体量（TS/TSX 字节数，我统计）：LOL ~320KB、Minecraft ~223KB、杀戮尖塔 ~228KB、PVZ ~168KB，均按 engine/ai/render/audio/types 等模块拆分
- 热度：很低（GitHub 2 stars）
- 生成方式：作者声明一次生成（"100% One-Shot Prompted: 核心玩法、状态机、战斗计算与渲染逻辑全部由 Claude Opus 5.5 单轮生成完成"）

## Prompt 原文（README 表格）

| 游戏 | 原始 Prompt |
|---|---|
| 英雄联盟峡谷仿真 | `尽可能利用你的现有能力复刻游戏LOL` |
| 我的世界 3D 沙盒 | `尽可能利用你的现有能力复刻Minecraft` |
| 植物大战僵尸 | `尽可能利用你的现有能力复刻游戏PVZ` |
| 杀戮尖塔肉鸽卡牌 | `尽可能利用你的现有能力复刻杀戮尖塔` |

## 作者对结果的描述（README 原文）

- LOL：英雄联盟召唤师峡谷仿真模拟，包含防御塔仇恨、三路兵线推进、小兵与英雄 AI、A* 寻路和技能系统。
- Minecraft：3D 体素沙盒复刻，包含程序化地形生成（Perlin Noise）、方块破坏/放置、第一人称视角控制与物理碰撞。
- PVZ：包含图鉴（Almanac）、种植网格、阳光经济系统、植物攻击动画与波次僵尸推进。
- 杀戮尖塔：包含地图路线选择、抽牌打牌出牌机制、遗物系统、状态与敌人意图系统。

## 证据强度说明

有可玩链接和完整源码，但热度极低、无第三方评价、无对话记录，"one-shot"为作者自述。价值在于它与 riba2534 案例构成同一 prompt 模式（"尽可能利用你的能力 + 复刻知名游戏"）的第二个独立样本，且覆盖了 2D 策略/卡牌类（非 3D 视觉炫技类）。
