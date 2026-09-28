---
source: 社区流传（老板提供），原始出处未知
model: Claude Opus 5.5
genre: 体素生活模拟 / 沙盒 / OSRS 式技能成长
outcome: 老板评价「非常惊艳」
notes: 结尾残留「Yes — that split makes sense」，推测是与 AI 多轮对话后整理出的设计文档
---

Rather than relying on a engine like unreal or godot, I want you to program an engine from scratch to build the below concept game, currently referred to as Open Blue. 
This concept works especially well if the MVP is **small geographically but systemically dense**. I would build one compact voxel valley, three purchasable properties, and only the first **5 levels** of the initial skills. The goal is to prove that simply *living on the land* is satisfying before adding dozens of skills, towns, relationships, seasons, livestock, etc.
## Core premise
You begin in a corporate office.
Your character is exhausted, staring at a computer while emails and notifications keep appearing. After a very short playable introduction, you decide:
> **“I’m done.”**
You resign, liquidate your savings/investments, and leave the city with approximately **$205,000**.
A rural real-estate agent shows you three properties.
Every property costs exactly **$200,000**.
This is important because the choice isn't:
**cheap property vs expensive property**
It's:
**What kind of life do I want to build?**
You are left with only about **$5,000 cash**, basic clothes, and whatever starter tools come with the land.
---
# The three starting properties
### 🌾 1. Meadowbrook Farm
**Best for Farming**
Large open property consisting mostly of grassland.
**Advantages**
- Largest tillable area
- Rich soil
- Small existing vegetable patch
- Several berry bushes
- Flat terrain makes construction easier
- Small abandoned barn
**Disadvantages**
- Very few mature trees
- No natural fishing water
- Stone/ore resources are limited
- Hunting animals don't visit frequently
Approximate layout:
```text
┌──────────────────────────────────┐
│     Trees                        │
│      ♣ ♣                         │
│                                  │
│        FARMHOUSE                 │
│           ▣                      │
│                                  │
│   █████████████████████████      │
│   █   OPEN FARMLAND       █      │
│   █████████████████████████      │
│                                  │
│                     OLD BARN     │
│                        ▣         │
└──────────────────────────────────┘
```
This property makes early Farming extremely convenient, but you'll eventually want to travel for timber, fish and ore.
---
# 🌲 2. Pine Hollow
**Best for Woodcutting / Hunting**
A cabin surrounded by dense woodland.
**Advantages**
- Huge number of trees
- Trees regenerate faster
- More wildlife spawns
- Naturally occurring mushrooms/berries
- Early access to better Woodcutting resources
**Disadvantages**
- Very little farmland
- Uneven terrain
- No large fishing source
- Clearing farmland requires cutting trees and removing stumps
```text
┌──────────────────────────────────┐
│ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣       │
│ ♣ ♣ ♣ ♣    DEER    ♣ ♣ ♣       │
│ ♣ ♣ ♣             ♣ ♣ ♣ ♣      │
│ ♣ ♣      CABIN       ♣ ♣ ♣      │
│ ♣ ♣        ▣         ♣ ♣ ♣      │
│ ♣ ♣                  ♣ ♣ ♣      │
│ ♣ ♣   small clearing ♣ ♣ ♣      │
│ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣ ♣       │
└──────────────────────────────────┘
```
This becomes the classic **woodsman/hunter homestead**.
---
# 🎣 3. Willowbend
**Best for Fishing / balanced survival**
A smaller property where a river widens into a little pond.
**Advantages**
- Fishing directly from your property
- River provides water
- Moderate tree population
- Wildlife frequently approaches the water
- Some clay/stone deposits near the riverbank
- Beautiful property
**Disadvantages**
- Water takes up usable land
- Farming area is smaller
- Occasional flooding could eventually become a mechanic
- Less dense timber than Pine Hollow
```text
┌──────────────────────────────────┐
│ ♣      ♣                   ♣     │
│                                  │
│       HOUSE                      │
│         ▣                        │
│                                  │
│ █████ FARM █████                 │
│                                  │
│ ~~~~~~~~~~~~~~~~                 │
│ ~     POND      ~~~~~~~~         │
│ ~~~~~~~~~~~~~~~~~~~~~~~~         │
│          RIVER →                 │
└──────────────────────────────────┘
```
I would intentionally make **none of them objectively better**.
---
# The world
The player's property is only their home base.
Around it is a larger voxel world:
```text
                  MOUNTAINS
                     ▲
                     │
          FOREST ── TOWN ── MINE
             │       │
             │       │
        PLAYER LAND  │
             │       │
             └── RIVER ── LAKE
```
For the MVP, the map doesn't need to be enormous.
Something like:
**512×512 voxel tiles**
would already feel substantial with isometric rendering.
Eventually this could grow into procedural regions.
---
# Visual direction
I would target something between:
**Minecraft × OSRS × Stardew Valley × Tiny Glade**
but with your own voxel identity.
Not cubes representing everything.
Instead:
- voxel terrain
- voxel trees
- voxel buildings
- stylized voxel characters
- detailed lighting
- soft shadows
- ambient wildlife
- wind moving foliage
- water reflections
- smoke from chimneys
Characters might be around:
```text
6–8 voxels wide
18–24 voxels tall
```
which gives enough resolution for clothing, tools and equipment.
---
# Camera
The camera should **not be permanently locked** to one traditional isometric angle.
Default:
```text
Pitch: ~35°
Yaw:   ~45°
```
But the player can rotate around the environment.
### Controls
**WASD**
Move character.
**Middle mouse drag**
Rotate camera.
**Mouse wheel**
Zoom.
**Shift + wheel**
Adjust camera height.
**Q / E**
Rotate camera 45°.
Possible zoom range:
```text
Close
│
├── Character view
├── Property view
├── Farm overview
│
└── Regional overview
```
At the farthest zoom, trees/buildings could partially simplify into lower-detail voxel models.
---
# OSRS-style skills
I would absolutely use the classic concept:
> **Do activity → gain XP → activity gets better → unlock new things.**
No arbitrary talent points.
Your character becomes good at something because they actually **do it**.
Initial skills:
| Skill | MVP |
|---|---:|
| Farming | 1–5 |
| Hunting | 1–5 |
| Woodcutting | 1–5 |
| Fishing | 1–5 |
| Firemaking | 1–5 |
| Cooking | 1–5 |
| Fletching | 1–5 |
| Mining | 1–5 |
| Smithing | 1–5 |
Long-term cap could eventually be **99 or 120**.
For the prototype, though, Level 5 is plenty.
---
# Woodcutting 1–5
### Level 1
Cut fallen branches.
```text
Fallen Branch
Woodcutting 1
+5 XP
```
### Level 2
Cut saplings.
### Level 3
Cut young pine trees.
### Level 4
Cut mature pine.
### Level 5
Cut oak.
Higher skill gradually affects:
- chop speed
- stamina use
- log yield
- rare material chance
Example:
```text
Pine Tree
Level 1 player:
Not skilled enough
Level 3:
7 swings
Level 5:
5 swings
```
---
# Firemaking
Logs have actual utility.
### Level 1
Small campfire.
Requires:
```text
3 Branches
1 Tinder
```
### Level 2
Basic log fire.
### Level 3
Improved campfire.
### Level 4
Firepit.
### Level 5
Long-burning hearth fire.
Fire has physical characteristics:
```text
Fuel
Heat
Burn Time
Light Radius
Cooking Slots
```
A tiny branch fire may last two minutes.
A proper hardwood fire could last much longer.
---
# Fishing
Fishing shouldn't just be:
> click water → wait → fish
You'll visibly cast into voxel water.
Fish move underneath.
### Levels 1–5
**1 — Minnow**
**2 — Bluegill**
**3 — Perch**
**4 — Trout**
**5 — Bass**
Different water locations produce different fish.
Eventually:
- rivers
- ponds
- lakes
- ocean
- streams
- caves
can each have ecosystems.
---
# Farming
Farming should be more physical than Stardew's instant tile interactions.
You actually prepare land.
```text
Grass
 ↓ Hoe
Soil
 ↓ Seed
Planted Soil
 ↓ Water
Wet Soil
 ↓ Time
Crop
```
### Levels
**1**
Potatoes
**2**
Carrots
**3**
Onions
**4**
Cabbage
**5**
Wheat
Higher Farming improves:
```text
Yield
Growth reliability
Seed recovery
Crop quality
Disease resistance
```
---
# Mining
Early mining can occur at exposed rock deposits.
### Level 1
Stone
### Level 2
Clay / Flint
### Level 3
Copper
### Level 4
Tin
### Level 5
Small iron deposits
Eventually mines become much deeper.
You could literally uncover underground voxel layers.
---
# Smithing
Mining feeds directly into Smithing.
```text
Copper Ore
    ↓
Furnace
    ↓
Copper Bar
    ↓
Anvil
    ↓
Copper Axe
```
Early recipes:
**Level 1**
Nails
**Level 2**
Copper knife
**Level 3**
Copper axe
**Level 4**
Copper pickaxe
**Level 5**
Copper hoe
That creates an important progression loop.
Your character initially buys crappy tools.
Eventually:
> **You make your own tools.**
---
# Fletching
This becomes surprisingly useful immediately.
Level 1:
```text
Stick
```
Level 2:
```text
Wooden Shaft
```
Level 3:
```text
Arrow Shaft
```
Level 4:
```text
Flint Arrow
```
Level 5:
```text
Basic Hunting Bow
```
This naturally connects:
```text
Woodcutting
     ↓
 Fletching
     ↓
 Hunting
     ↓
 Cooking
```
---
# Hunting
I wouldn't turn this into traditional action-game hunting yet.
For the MVP:
### Animals
- rabbit
- squirrel
- deer
Early Hunting might involve:
**Level 1**
Tracking footprints.
**Level 2**
Basic snare.
**Level 3**
Rabbit hunting.
**Level 4**
Improved traps.
**Level 5**
Bow hunting.
Animals should actually exist in the world rather than spawning as resource nodes.
A rabbit might:
```text
Eat
↓
Wander
↓
Notice player
↓
Flee
↓
Hide
↓
Return later
```
---
# Cooking
Cooking ties everything together.
Raw ingredients have quality.
Example:
```text
Raw Trout
Freshness: 91%
Quality: Normal
Weight: 1.4 lb
```
Cooking methods matter.
```text
Raw Fish
   │
   ├── Campfire
   ├── Pan
   ├── Oven
   └── Smoker
```
Early recipes:
**1**
Roasted potato
**2**
Cooked fish
**3**
Vegetable stew
**4**
Grilled rabbit
**5**
Fish and vegetable soup
---
# The first major gameplay loop
The player buys their property.
Their first morning might look like:
```text
Wake up
   ↓
Walk outside
   ↓
Cut branches
   ↓
Woodcutting XP
   ↓
Build campfire
   ↓
Firemaking XP
   ↓
Catch fish
   ↓
Fishing XP
   ↓
Cook fish
   ↓
Cooking XP
   ↓
Sell extra fish
   ↓
Buy seeds
   ↓
Plant crops
   ↓
Farming XP
```
Nothing forces them into this sequence.
That's the important part.
Someone may immediately decide:
> Screw farming. I'm becoming a lumberjack.
And spend three days cutting trees.
---
# Money
Starting money:
```text
Savings                  $205,000
Property                -$200,000
---------------------------------
Remaining                   $5,000
```
That creates an interesting psychological shift.
The character technically had a lot of money.
Now they are **land rich and cash poor**.
Early expenses might include:
```text
Seeds                 $4
Basic fishing rod    $35
Iron axe             $60
Food                  $8
Backpack             $75
Chicken              $40
```
Eventually the economy could become considerably deeper.
---
# Property ownership
Your property boundary should actually matter.
Inside your land you can:
- cut trees
- dig
- farm
- construct
- terraform
- place objects
- build fences
- make roads
- create ponds
- build structures
Outside it, land belongs to:
- town
- wilderness
- other farms
- government
- NPCs
That eventually creates opportunities for purchasing neighboring parcels.
You might start with:
```text
8 acres
```
and eventually own:
```text
8
↓
16
↓
30
↓
65
↓
120 acres
```
---
# The interface
I would keep the UI extremely clean.
Top-left:
```text
06:42
Spring 3
Year 1
$4,872
```
Bottom:
```text
[1] Axe
[2] Pickaxe
[3] Hoe
[4] Fishing Rod
[5] Seeds
```
When XP is earned:
```text
Woodcutting
+12 XP
```
Then:
```text
┌────────────────────────────┐
│ WOODCUTTING LEVEL 3        │
│                            │
│ You can now cut Pine Trees │
└────────────────────────────┘
```
Very OSRS-inspired without copying its UI.
---
# Skills panel
Something like:
```text
CHARACTER
Farming        3    184 XP
Hunting        1     14 XP
Woodcutting    4    322 XP
Fishing        3    207 XP
Firemaking     2     89 XP
Cooking        3    215 XP
Fletching      1     31 XP
Mining         2     76 XP
Smithing       1     22 XP
```
Clicking a skill shows its unlock ladder.
```text
WOODCUTTING
✓ Lv 1 Branches
✓ Lv 2 Saplings
✓ Lv 3 Pine
○ Lv 4 Mature Pine
○ Lv 5 Oak
🔒 Lv 6 ???
```
Even though Levels **6–99 aren't implemented yet**, they can visually exist as locked future progression.
That makes the MVP feel like the beginning of a much larger game.
---
# MVP boundary
This is where I'd stop the **first playable build**:
### World
- one small town
- three property layouts
- forest
- pond
- river
- mine entrance
- basic roads
### Character
- walking
- running
- stamina
- inventory
- tool use
- camera control
### Skills
Levels **1–5** for the nine initial skills.
### Animals
- rabbit
- squirrel
- deer
- several fish
### Crops
- potato
- carrot
- onion
- cabbage
- wheat
### Resources
- branches
- pine
- oak
- stone
- flint
- copper
- tin
- iron
### Crafting
Approximately **25–40 recipes**.
### Structures
- campfire
- firepit
- chest
- basic crafting bench
- furnace
- anvil
- small fence
### Economy
One general store where goods can be bought and sold.
That is enough to answer the most important question:
> **Is living in this little voxel world fun?**
If that answer is yes, then expanding from **Level 5 → 20 → 50 → 99** becomes content production rather than redesigning the entire game.
And this has enormous room to grow later into construction, livestock, carpentry, relationships, NPC occupations, weather, seasons, property expansion, business ownership, exploration, archaeology, combat and an actual player-driven rural economy.
---
Yes — that split makes sense.
For a voxel game, I’d separate assets into two pipelines:
World objects → reconstructed 3D
trees
rocks
crops
furniture
buildings
animals
resource nodes
anything the player can walk around These should have real volume, because the camera will expose them from multiple angles.
Held/equipped items → depth-mapped sprite extrusion
axe
hoe
pickaxe
sword
shovel
fishing rod
food
crafting materials These benefit from keeping the recognizable pixel-art silhouette while getting enough thickness and contour to feel like a physical object.
I would probably avoid pure flat extrusion except for deliberately thin objects such as signs, paper, cards, posters, leaves, cloth panels, or UI-adjacent props.
For your game specifically, a good asset rule could be:
2D source art
    ↓
Classify asset
 
WORLD / ENVIRONMENT
    ↓
Semantic reconstruction
    ↓
True voxel volume
    ↓
Optimized mesh
 
HELD / INVENTORY ITEM
    ↓
Depth estimation
    ↓
Pixel silhouette preserved
    ↓
1–4 voxel variable thickness
    ↓
Optimized mesh
That also gives you a very efficient art workflow. You could draw essentially everything as 16×16, 24×24, or 32×32 pixel art first, then let the importer generate the appropriate 3D representation based on an asset type.
For example:
iron_axe.png
type = TOOL
depth = AUTO
edge_depth = 1
handle_depth = 2
head_depth = 4
would become something closer to:
            █████
          ████████
        █████████
             ██
             ██
            ██
            ██
           ██
but in 3D the iron axe head could be 3–4 voxels thick, while the wooden handle might only be 1–2 voxels thick.
A tree could instead say:
oak_tree.png
type = WORLD_OBJECT
 
brown → trunk
green → foliage
and your system generates an actual trunk volume and irregular canopy.
That would give the game a consistent pixel-art visual language without making the world look like a collection of cardboard sprites.
