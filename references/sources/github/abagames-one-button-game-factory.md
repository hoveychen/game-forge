# Claude One-Button Game Creation — Kenta Cho (ABA Games) agentic factory for batches of crisp-game-lib one-button arcade games

- Repo: https://github.com/abagames/claude-one-button-game-creation  (gallery GAMES.md; playable at https://abagames.github.io/claude-one-button-game-creation/?<game>) ; skills in https://github.com/abagames/agentic-gamedev-skills
- Stars: 53. 200 commits, 2024-03-11 → 2026-07-27 (evolved from Claude chat + knowledge files in 2024 → Cursor → agent workflow w/ skills in 2026; old versions in archive/).
- Author credibility: abagames = Kenta Cho, prolific and celebrated one-button/minimalist arcade designer (crisp-game-lib author). His taste is encoded in the design guides.
- Tool/model: Claude (originally chat w/ project knowledge), later Claude Code/Codex-style coding agents following AGENTS.md.
- Genre: tiny one-button arcade games (dozens published with GIF screenshots).
- Result evidence: 60+ published playable games with animated screenshots. Published builds under docs/ are human-curated ("may be changed only by explicit human instruction"), so this is generate-many-then-curate.
- One-shot vs multi-session: one fresh context per game; batch of 10; random 3-tag seed per game from data/tags.csv.
- Notable process practices:
  - Idea generation by constrained randomness: `random_tag_selector.js -n 3` → agent designs around 3 tags. Removes "vague idea" problem by forcing concrete, novel constraint combos.
  - Normative one-game procedure in workflows/game-generation.md, executed 10× in fresh contexts; each context "does not read or rank the rest of the batch" (avoids convergence/self-comparison).
  - Real-browser smoke test for every game (Playwright Chromium) + scripts/check_batch.js verifies count, required deliverables, runtime.
  - Human curation gate for publishing; agent must not delete/replace/move existing games without direction.
  - Archive contains earlier design knowledge: one-button-game-design-guide.md, implementation guide, game-testing-prompt.md, sample games as few-shot references.

---
## Verbatim: AGENTS.md
# claude-one-button-game-creation

An automatic one-button game generation project using crisp-game-lib. Agents
use random tags as inspiration to design and implement a varied batch of ten
browser-playable games.

The standard workflow ends when ten runnable games are presented. Ranking,
selection, human review, Polish, retrospective, publication, and play-log
mechanical evaluation are separate activities and require an explicit user
request.

---

## Working Directory

Run all commands from the project root (the directory containing this file).

- Generation workflow: `./workflows/game-generation.md`
- Scripts: `./scripts/`
- Static tag inputs: `./data/`
- Generated games: `./tmp/games/`

On a fresh clone, run:

```bash
npm ci
npm run skills:install
npm run playwright:install
npm test
```

`skills:install` copies only the skills required by this project from
[`abagames/agentic-gamedev-skills`](https://github.com/abagames/agentic-gamedev-skills)
into the ignored local `.agents/skills/` directory. It replaces only those
three skill directories and preserves other content under `.agents/`. To
refresh intentionally, run the command again; set `AGENT_SKILLS_REF` to the
desired upstream commit. The generation workflow has no durable-state
initialization requirement.

---

## Standard Flow: Generate and Present Ten Games

1. Confirm `tmp/games/` is absent or empty. If it contains anything, stop and
   ask the user what to do. Do not delete, overwrite, move, or archive existing
   output without explicit user direction.
2. Run `workflows/game-generation.md` once per game with a fresh generation
   context and fresh tag seed.
3. Repeat until `tmp/games/` contains exactly ten new games.
4. Smoke-test every game's `index.html` in a real browser. Repair runtime
   failures and re-run the failed smoke test.
5. Present the ten games as an unranked list and stop.

Each game must be generated independently. A game-generation context may read
the generation workflow, the relevant skills, its own tags, and its own output,
but must not compare against other games in the batch or attempt to select a
winner.

Use this command once per game to obtain tags:

```bash
node scripts/random_tag_selector.js -n 3 -f text
```

Validate the completed batch and smoke-test every game with:

```bash
npm run batch:check
```

The command must exit successfully. It enforces exactly ten game directories,
the three required files in each directory, and a passing real-browser smoke
test for every `index.html`.

Smoke testing is part of generation completion because the presented games
must run. Comparative measurement, defect panels, ranking, winner ledgers, and
Polish are not part of this flow.

**Publication is always separate and human-authorized.** Never copy, move, or
sync a generated game into `docs/` unless the user explicitly requests that
publication action.

---

## Documents

| File | Purpose |
| :--- | :--- |
| `README.md` | Operational entry point for generating and presenting a batch |
| `workflows/game-generation.md` | Normative procedure for creating one game |
| `data/tags.csv` | Static tag seed catalog |
| `scripts/install_agent_skills.sh` | Install the three required upstream skills into local `.agents/skills/` |
| `scripts/check_batch.js` | Enforce the ten-game deliverable contract and run every browser smoke test |
| `archive/retired-batch-selection/` | Non-normative former selection and Polish workflow |
| `archive/retired-play-log-evaluation/` | Non-normative former play-log mechanical evaluation workflow |

Archived material is historical context only. It must not be treated as a
continuation step after generating a batch.

---

## Deliverables

```text
tmp/games/<slug>/
├── index.html
├── main.js
└── README.md
```

The complete batch deliverable is ten directories in `tmp/games/`, plus a
successful browser smoke test for each game. `tmp/` is working output and does
not authorize publication.


---
## Verbatim: workflows/game-generation.md
# Game Generation Workflow (One Game)

How to create ONE one-button game: Phase 1 (tag selection) → Phase 2
(design) → Phase 3 (implementation). Run it once per game; a batch is just
this workflow repeated ten times with fresh tag seeds (see `AGENTS.md` for the
batch procedure).

This workflow has no comparative, ranking, or selection gates. It optimizes
for variance (diverse, novel games), but each game must still satisfy the
lightweight design checks below and pass the real-browser smoke test.

---

## Phase 1: Tag Selection

```bash
node scripts/random_tag_selector.js -n 3 -f text
```

| Option         | Description                    | Default      |
| :------------- | :----------------------------- | :----------- |
| `-n, --count`  | Number of tags to select       | 3            |
| `-s, --seed`   | Random seed (for reproduction) | Current time |
| `-f, --format` | text/json/markdown             | markdown     |

**Important**: Tags are "seeds for inspiration," not "design specifications." Use contradicting tags as creative tension.

---

## Phase 2: Game Design

**Reference**: `.agents/skills/designing-mini-games/` — the canonical source
for mini-game design craft. Bind its general input-scheme support to this
project's fixed brief: `button_types = 1`; one binary input expressed only
through press, hold, and release; no second key, chord, swipe, or auxiliary
input. **Use it with the generation profile below**: the project secures
diversity by generating ten independent games without comparative gates, so
verification machinery that would narrow the design space stays out of
generation.

Generation profile (what to use at generation time):

- USE: the skill's Phase-1 ideation steps 1–4 (free association → record the
  first association and forbid it → deviation exploration → core experience →
  construct mechanics with the already-fixed `button_types = 1` scheme), the
  reference guide's four core principles (§2), contradiction-as-tension table
  (§7), and abstract-question prompts (§6).
- USE LIGHTWEIGHT: the skill's Phase-2 steps 5–7. Identify the state and
  tradeoff (or explain why geometry alone creates choices), explain why idle,
  hold-only, and mashing lose to skilled play, and define the in-world scoring
  cause and what scales with difficulty.
- DO NOT REQUIRE at generation time: formal invariant proofs, state tables,
  seed prechecks, extended checklists, or separate hardening documents. These
  steer concepts toward easily-provable archetypes and reduce batch variance.
- Output format: keep this file's 6-section README below (it is the
  stable game deliverable), not the skill's Appendix A.

### Design Procedure

1. **Free Association**: Verbalize images that come to mind from tags
2. **Deviation Exploration**: Consider the "opposite," "negation," or "extreme" of tags
3. **Core Experience Decision**: Define the "momentary sensation" you want to give the player in one phrase
4. **Mechanics Construction**: Design one-button operation that realizes the core experience
5. **Lightweight Specification**: Record the state/tradeoff, monotonous-input
   weaknesses, in-world scoring cause, and difficulty scaling
6. **Consistency Verification**: Confirm with checklist below

### Design Checklist

- [ ] Does it complete with one button?
- [ ] Is the game over condition single and visually obvious?
- [ ] Does the design explain why idle play is suboptimal?
- [ ] Does it explain why hold-only play is suboptimal?
- [ ] Does it explain why repeated mashing is suboptimal?
- [ ] Is scoring caused by an in-world event rather than the input itself?
- [ ] Is the state/tradeoff defined, or is a geometry-only decision space justified?
- [ ] Does the design state what scales with difficulty and why?
- [ ] Are there moments of feeling "I've never seen this before"?
- [ ] Is this NOT a clone or minor variation of a widely-known existing game?

### Output Format

Write the following to `tmp/games/<slug>/README.md`:

```markdown
# <GAME_NAME> (<slug>)

**Tags**: #tag1, #tag2, #tag3

## 1. Core Mechanics

<Input → behavior → end condition.

State/tradeoff, or why geometry alone creates meaningful choices.

In-world scoring cause and difficulty scaling.

Why idle, hold-only, and mashing are weaker than skilled play.>

## 2. Object Specifications

<Each object's shape, behavior, collision handling>

## 3. Design Guide Analysis

<Evaluation against four core design principles (Simplicity and Intuitiveness, Visual Feedback and Game Over, Skill-Based Scoring and Risk/Reward, Novel Mechanics)>

## 4. Relationship with Tags

<Idea development from tags>

## 5. Basis for Novelty

<Elements beyond existing patterns>

## 6. Similarity Check

<List any known games with similar mechanics. Explain key differences that make this design distinct.>
```

---

## Phase 3: Implementation

**Reference**: `.agents/skills/developing-with-crisp-game-lib/` — read
`SKILL.md` (setup, implementation flow, mandatory rules, patterns) and its
`references/api.md` (complete API) / `references/examples.md` (working
loops). This skill is the canonical source for crisp-game-lib knowledge.

### Constraints

- **Lines**: About 150 lines
- **Dependencies**: crisp-game-lib only
- **Structure**: Include `title`, `description`, `characters`, `options`, `update()`

### Difficulty Settings

Use `difficulty` variable (auto-increasing) for difficulty increase:

```javascript
let count = 3 * sqrt(difficulty); // Gradually increases
let speed = 1.0 + difficulty; // Gradually accelerates
```

Make the increase perceptible within a short arcade session while keeping the
first interactions readable; cap rates before visual or control legibility
collapses.

### Output Location

Place the following in `tmp/games/<slug>/`:

- `index.html` - HTML template
- `main.js` - Game code

### HTML Template

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>GAME_NAME</title>
    <meta
      name="viewport"
      content="width=device-width, height=device-height, user-scalable=no, initial-scale=1, maximum-scale=1"
    />
    <script src="https://unpkg.com/algo-chip@1.0.2/packages/core/dist/algo-chip.umd.js"></script>
    <script src="https://unpkg.com/algo-chip@1.0.2/packages/util/dist/algo-chip-util.umd.js"></script>
    <script src="https://unpkg.com/crisp-game-lib@1.5.0/docs/bundle.js"></script>
    <script src="./main.js"></script>
    <script>
      window.addEventListener("load", onLoad);
    </script>
  </head>
  <body style="background: #ddd"></body>
</html>
```

### Implementation Template

```javascript
title = "GAME_NAME";

description = `
[Hold] Action
`;

characters = [];

options = {
  isPlayingBgm: true,
  isReplayEnabled: true,
  audioSeed: 0,
};

let player;
let obstacles;

function update() {
  if (!ticks) {
    player = { pos: vec(50, 80) };
    obstacles = [];
  }

  // Input handling
  if (input.isJustPressed) {
    // On button press
  }
  if (input.isPressed) {
    // While button held
  }

  // ★Important: Drawing order for collision detection
  // Draw detection targets "first" (cannot detect objects drawn later)

  // 1. Draw player first
  color("cyan");
  box(player.pos, 6);

  // 2. Draw obstacles later and detect collision with player (cyan)
  color("red");
  obstacles.forEach((obs) => {
    if (box(obs.pos, 8).isColliding.rect.cyan) {
      end(); // Collision with player
    }
  });
}
```

### Implementation Notes

#### Collision Detection Drawing Order (Important)

In crisp-game-lib, **collision detection only works with objects drawn earlier**.

```javascript
// ❌ Doesn't work: player (cyan) doesn't exist yet when drawing obstacles
obstacles.forEach(o => box(o.pos, 8));  // red
box(player.pos, 6);                      // cyan (later)

// ✅ Correct: Draw detection targets first
box(player.pos, 6);                      // cyan (first)
obstacles.forEach(o => {
  if (box(o.pos, 8).isColliding.rect.cyan) { ... }  // red
});
```

#### Browser API Compatibility (Important)

Use only the API documented in
`.agents/skills/developing-with-crisp-game-lib/references/api.md`. Do not infer
API availability from JavaScript or similarly named game libraries. The
completed game must pass the real-browser smoke test from `AGENTS.md`.

---

## Deliverables

```
tmp/games/<slug>/
├── index.html    # HTML template
├── main.js       # Game code
└── README.md     # Game description
```

---

## Tag Categories

| Category      | Description            | Examples                                |
| :------------ | :--------------------- | :-------------------------------------- |
| `player`      | Player characteristics | `player-rotate`, `player-multiple`      |
| `on_pressed`  | On button press        | `on_pressed-jump`, `on_pressed-turn`    |
| `on_holding`  | While button held      | `on_holding-move`, `on_holding-charge`  |
| `on_released` | On button release      | `on_released-throw`                     |
| `on_got_item` | On item acquisition    | `on_got_item-power_up`                  |
| `field`       | Field characteristics  | `field-auto_scroll`, `field-1D`         |
| `rule`        | Game rules             | `rule-physics`, `rule-combo_multiplier` |
| `weapon`      | Weapons/Attacks        | `weapon-explosion`, `weapon-reflect`    |
| `obstacle`    | Obstacles              | `obstacle-chase`, `obstacle-penalty`    |


---
## Verbatim: archive/for_chat/cc_knowledge/one-button-game-design-guide.md (2024-25 era design guide)
# One-Button Game Design Workflow Guide (Human-LLM Collaborative Version)

This guide provides a systematic 5-phase workflow for designing games that are fun, understandable, and innovative through strategic human-LLM collaboration.

**IMPORTANT: The themes, verbs, methods, mechanics, types, genres, etc. mentioned in this guide should be treated as examples only. Feel free to think broadly and creatively beyond the content presented in this guide.**

**Diversity Encouragement: Explore diverse physical concepts like light, magnetism, growth, and other intuitive phenomena. The goal is to create varied, innovative experiences that players can immediately understand and enjoy.**

## 🤝 Human-LLM Collaboration Protocol

**Strategic Collaboration:**

- **LLM Strengths**: Systematic processing, template completion, constraint checking, pattern recognition
- **Human Strengths**: Intuitive validation, experience judgment, ambiguity resolution, creative feedback
- **Collaboration Triggers**: Uncertainty detection, constraint violations, complexity issues, final validation

**Session Time**: 35-50 minutes | LLM autonomous: ~70% | Human validation: ~30%

**Essential Human Checkpoints:**

1. **Phase 0**: Theme concreteness and appeal validation
2. **Phase 1**: Simple solution logic validation
3. **Phase 2**: Experience walkthrough approval
4. **Phase 3**: Implementation readiness confirmation

**Collaboration Execution:**

```markdown
🤖 LLM AUTO-EXECUTE: Template completion, constraint checking, systematic processing
🤝 HUMAN CHECKPOINT: Problem clarity, solution logic, complexity assessment, final validation
🚫 FORBIDDEN: Starting with "interesting mechanics" before problem definition
✅ REQUIRED: Problem → Solution → Innovation → Experience → Implementation flow
```

## Workflow Overview

**Complete each phase in order. Each phase validates and refines previous phases.**

| Phase | Purpose                             | Input                                   | Output                           | Completion Check                                              |
| ----- | ----------------------------------- | --------------------------------------- | -------------------------------- | ------------------------------------------------------------- |
| 0     | Concrete Theme Inspiration (Human-Validated) | Theme categories                        | Selected concrete theme     | ✅ Concrete theme selected + Human validation obtained + Clear constraints identified |
| 1     | Simple Problem-Solution Design | Problem categories + Theme | Clear problem-solution pairs | ✅ Problem defined + Simple verb + Logic validated |
| 2     | Player Experience Integration       | Simple, clear mechanics              | Engaging, understandable game    | ✅ Conceptual walkthrough + User feedback                     |
| 3     | Final Validation & Documentation    | Complete experience                     | Implementation-ready spec        | ✅ All warning signs checked + Spec complete                  |

---

## Phase 0: Theme Inspiration (Automated)

**Phase Input:** Theme categories (provided below)
**Phase Output:** Selected concrete, relatable theme to guide creative thinking
**Completion Criteria:** ✅ Concrete professional/historical theme selected ✅ Human validation obtained ✅ Theme provides clear constraints and universal appeal

### ⚠️ Phase 0 Execution Protocol

**EXECUTION ORDER:**

```markdown
🤖 LLM AUTO: Theme category selection → Theme generation → 3-stage validation → Best theme selection
🤝 HUMAN: Theme appeal confirmation → Alternative preference → Final approval
⚠️ IMPORTANT: Theme serves as INSPIRATION only, not as design constraint
⚠️ CRITICAL: Problem-solution logic always takes priority over theme adherence
⚠️ NEW: Concrete professions/scenarios preferred over abstract concepts
```

### 0.1 Theme Category Selection

**LLM automatically generates 3-5 themes from across all categories below, prioritizing concrete and relatable experiences:**

```markdown
🏛️ **Historical Professions & Roles**
Examples: Lighthouse keeper, Telegraph operator, Blacksmith, Town crier, Mail carrier, Night watchman
Effect: Concrete professional experiences with clear responsibilities, time-period constraints, and job-specific limitations

🌍 **Specific Places & Facilities**
Examples: Library operations, Museum security, Observatory work, Dam control room, Radio station, Fire tower
Effect: Real-world locations with specific operational constraints, environmental factors, and facility-based responsibilities

📚 **Historical Events & Scenarios**
Examples: Apollo moon landing, Medieval castle siege, Early telephone switching, 1960s computer operation, Ship navigation pre-GPS
Effect: Time-period constraints, technological limitations, urgency, and historical context create natural game constraints

🔧 **Everyday Tools & Machines**
Examples: Analog watch repair, Manual printing press, Record player adjustment, Old-style camera operation, Hand-crank drill
Effect: Tactile understanding, precision requirements, familiar mechanical interactions with clear operational constraints

🎪 **Cultural Events & Performances**
Examples: Circus preparation, Orchestra tuning, Theater lighting, Festival coordination, Art gallery setup, Wedding planning
Effect: Performance pressure, timing requirements, coordination challenges, and perfectionism constraints

⚡ **Everyday Natural Phenomena**
Examples: Surface tension effects, Plant growth cycles, Ice melting patterns, Sand flow dynamics, Steam condensation, Water pressure
Effect: Daily-life physics experiences, intuitive understanding, natural timing constraints

🎮 **Classic Game Reinterpretation**
Examples: Pac-Man maze navigation, Billiards angle calculation, Chess strategic thinking, Arcade timing challenges
Effect: Provides familiar interaction patterns to reinterpret with one-button constraint

🔬 **Professional Domain Basics**
Examples: Medical equipment calibration, Laboratory sample preparation, Engineering measurement, Cooking temperature control
Effect: Suggests systematic processes, specialized knowledge applications, and precision requirements
```

### 0.2 Theme Generation and Selection

```markdown
LLM AUTOMATED PROCESS:

1. **Theme Generation**: Create 3-5 specific themes from across ALL categories above
2. **3-Stage Selection Process**:

   **Stage 1: Concreteness Check**
   ✅ Represents a concrete profession, place, or historical scenario
   ✅ Universally recognizable and relatable (avoid cultural specificity)
   ✅ Can be visualized and understood by anyone

   **Stage 2: Appeal Assessment**
   ✅ Engaging enough to make people curious ("I'd like to try that")
   ✅ Unexplored in game themes (fresh without being obscure)
   ✅ Can be explained compellingly in one sentence

   **Stage 3: Constraint Clarity**
   ✅ Has domain-specific constraints and responsibilities
   ✅ Natural limitations that align with one-button gameplay
   ✅ Clear cause-and-effect relationships

3. **Final Selection**: Pick ONE theme that passes all three stages as creative inspiration
```

### 0.2.1 Human Validation Checkpoint

```markdown
🤝 HUMAN VALIDATION REQUEST:
"I've selected [THEME] as the creative inspiration. Quick validation:

- Is this concrete and relatable enough?
- Does it sound engaging to you?
- Can you immediately imagine the constraints this profession/scenario would have?
- Would you prefer a different theme from these alternatives: [list other candidates]?"

HUMAN RESPONSE OPTIONS:
✅ "Good choice, proceed" → Continue to Phase 1
🔄 "Try [alternative] instead" → Use human suggestion
❌ "All seem abstract/boring" → Generate new set with different approach
```

### 0.3 Theme Application Guidelines

```markdown
ENHANCED THEME USAGE PROTOCOL:

✅ **CORRECT Usage**:

- Use theme to inspire problem category selection based on profession-specific challenges
- Let theme suggest natural environmental constraints (workplace limitations, tool restrictions, time pressure)
- Allow theme to guide visual and conceptual metaphors rooted in real-world experience
- Reference theme when choosing specific verbs and mechanics that reflect actual job duties
- Leverage universal recognition of the profession/scenario for immediate player understanding

❌ **INCORRECT Usage**:

- Force all mechanics to literally recreate every aspect of the profession
- Abandon good problem-solution logic for theme authenticity
- Add complexity just to include more profession-specific details
- Use theme as excuse for violating one-button constraint
- Choose themes that require cultural knowledge to understand

🎯 **ENHANCED THEME INTEGRATION PRINCIPLE**:
"Concrete themes inspire relatable problems, universal constraints enable accessible solutions"

💡 **NEW THEME QUALITY CHECK**:
"Can someone immediately picture this job/scenario and understand why it would be challenging?"
```

**⏭️ Proceed to Phase 1 with selected theme as creative reference**

---

## Phase 1: Simple Problem-Solution Design

**Phase Input:** Problem categories + Selected theme (from Phase 0)
**Phase Output:** Clear problem-solution pairs with simple, understandable mechanics
**Completion Criteria:** ✅ Problem category selected, ✅ Problem template completed, ✅ Simple verb applied, ✅ Solution logic validated, ✅ Goal achievement path clear

### ⚠️ Phase 1 Execution Protocol

**EXECUTION ORDER:**

```markdown
🤖 LLM AUTO: Theme-informed problem category selection → Template completion
🤝 HUMAN: Problem validation → Solution logic confirmation
🤖 LLM AUTO: Verb application → Control design → Goal setting
```

### 1.1 Problem Definition (Steps A-B)

#### Step A: Theme-Informed Problem Category Selection

**Reference selected theme and select ONE problem category that resonates:**

```markdown
PROBLEM CATEGORIES:
□ **Movement/Navigation**: Cannot reach location due to obstacle/constraint
□ **Resource/Collection**: Must collect/use resource but constraint prevents efficiency
□ **Timing/Coordination**: Must coordinate action with moving element but limitation makes synchronization difficult
□ **Information/Visibility**: Cannot perceive critical information due to obstruction
□ **State/Balance**: Must maintain beneficial state while avoiding harmful state
□ **Physics/Forces**: Must overcome/manipulate physical force but natural law prevents direct control
□ **Pattern/Signal**: Must recognize/create/transmit pattern but interference obscures communication
```

#### Step B: Problem Template Completion

```markdown
SELECTED THEME: [Theme from Phase 0]
SELECTED CATEGORY: [Category from Step A]

Player wants to: [Specific goal - consider theme context]
Current obstacle: [What prevents this goal - may be theme-inspired]
Environmental constraint: [Why normal methods don't work - can reflect theme]

🤝 HUMAN CHECKPOINT:
"Does this problem make sense as an interesting game challenge?
Does the theme enhance understanding without adding complexity?"
```

### 1.2 Simple Solution Design (Steps C-D)

**KEY PRINCIPLE: Maintain 3-second rule clarity above all else**

#### Step C: Simple and Effective Verb Selection

**STREAMLINED PROCESS: Clear mechanics with light innovation**

```markdown
STAGE 1: BASELINE VERB IDENTIFICATION
- Identify obvious/expected verb for the defined problem
- REVERSE CHECK: "Will this basic verb solve [obstacle] to achieve [goal]?"

BASELINE VERB CANDIDATES:
- Basic: Push, pull, rotate, stop, launch, release, activate, charge, aim, time
- Simple variations: Hold to charge, tap to release, time the action

STAGE 2: LIGHT IMPROVEMENT (3-SECOND RULE MAINTAINED)
- Keep the basic verb but add ONE simple twist that enhances engagement
- Examples:
  - "Push" → "Push with timing" (timing adds strategy)
  - "Launch" → "Charge and launch" (charging adds preparation)
  - "Release" → "Release at peak moment" (timing adds skill)

**Guidelines for Light Innovation:**
- ✅ Must be instantly understandable (3-second rule)
- ✅ Should solve the core problem more effectively
- ✅ Can add ONE strategic element (timing, charging, rhythm)
- ❌ No complex physics or multi-step processes
- ❌ No abstract concepts requiring explanation

STAGE 3: ONE-BUTTON COMPATIBILITY CHECK
- Verify selected verb works with press/hold/release only
- Ensure no hidden directional or positional input needed
- Confirm 3-second rule compliance
```

#### Step D: Simple Problem-Solution Logic Validation

```markdown
SIMPLE VALIDATION REQUIREMENTS:
□ Does the verb directly address the defined problem?
□ Is the connection clear: Problem → Simple Solution → Goal Achievement?
□ Can new player understand WHY this solution works within 3 seconds?
□ Does the solution respect the environmental constraint?
□ Is the mechanic immediately understandable and engaging?

🤝 HUMAN CHECKPOINT:
"Does this simple problem-solution logic make sense and feel fun?"

- Problem: [specific obstacle]
- Simple Solution: [clear verb with light innovation]
- Logic: [why this solution works]
- 3-Second Test: [can new player understand instantly?]
```

### 1.3 Control Design (Step E)

#### Step E: Input-to-Output Mapping

```markdown
DEFINE EXACTLY:
Press (Tap): [Specific immediate action]
Hold (1-3 seconds): [Specific continuous action or parameter change]
Release (after hold): [Specific action execution or state change]

CONSTRAINT VALIDATION:
□ Can this be achieved with ONLY press/hold/release?
□ No position selection, directional input, or multiple inputs required?
□ Player can achieve goal using only these inputs?

🤝 HUMAN SIMULATION:
"Try to 'play' this for 30 seconds using only press/hold/release.
Does anything feel impossible or require hidden inputs?"
```

### 1.4 Goal and Risk Setting (Step F)

```markdown
GOAL DEFINITION:

- Goal = Solution to the defined player problem
- Success = Problem resolved through designed mechanics
- Clear visual/spatial relationship between problem and goal

RISK DESIGN:

- Risks emerge from attempts to solve the core problem
- Failure = Problem becomes worse or new problems emerge
- Recovery = Learning better problem-solving strategies
```

**⏭️ Proceed to Phase 2 only after Phase 1 completion criteria are met**

---

## Phase 2: Player Experience Integration

**Phase Input:** Simple, clear mechanics from Phase 1
**Phase Output:** Engaging, understandable complete game experience
**Completion Criteria:** ✅ Conceptual walkthrough completed, ✅ User feedback obtained, ✅ Experience validated

### 2.1 Conceptual Walkthrough (Replaces Impossible Simulation)

**Critical Replacement:** Since numerical simulation is impossible without parameters, use logical validation instead

#### Conceptual Walkthrough Process

**Instead of "30-second simulation," perform logical walkthrough:**

```markdown
WALKTHROUGH REQUIREMENTS:
□ Describe player's logical action sequence using only "press", "hold", "release"
□ Verify each action logically connects to next game state
□ Confirm goal achievement is logically possible
□ Check that no "impossible" actions are required

EXAMPLE WALKTHROUGH:
Start: Player faces the defined problem (cannot reach high platform)
Action 1: Player presses → applies solution mechanic (gravity change)
Result 1: Game state changes (gravity direction shifts)
Action 2: Player holds → modifies solution parameter (gravity strength)
Result 2: Effect scales appropriately (stronger gravity pull)
Action 3: Player releases → executes solution (gravity applied)
Result 3: Problem resolves (player reaches platform)
End: Goal achieved through logical problem-solution chain

VALIDATION CHECK:
□ Every action uses only press/hold/release? ✅
□ Goal logically achievable? ✅
□ No directional input required? ✅
□ No position selection required? ✅
□ Problem-solution logic maintained? ✅
```

#### Impossible Action Detection

```markdown
RED FLAGS - If any appear, return to Phase 1:
□ "Player aims" → How? One button cannot aim
□ "Player chooses location" → How? One button cannot select positions  
□ "Player decides between options" → How? One button cannot make binary choices
□ Walkthrough requires information not available to player
□ Solution mechanics don't actually solve the defined problem

If ANY red flag appears, the design is fundamentally flawed.
```

### 2.2 User Feedback Integration (FLEXIBLE APPROACH)

**Multiple validation options based on available resources:**

#### Option A: Actual User Testing (Preferred)

**Ask users (colleagues, friends) these specific questions:**

```markdown
Understanding Test:

1. "I'll describe a game concept. Tell me what you think the player does."
   [Describe your problem-solution concept in 2-3 sentences]

2. "What do you think happens when the player presses the button?"
   [Listen for understanding of your core mechanic]

3. "What do you think the goal is, and how would you achieve it?"
   [Verify problem-solution logic is clear]

4. "Does this sound fun to you? Why or why not?"
   [Check engagement level]

Pass Criteria:
□ User understands the problem the player faces
□ User understands how button press helps solve it
□ User sees logical connection between action and goal
□ User expresses interest or curiosity
```

#### Option B: Human Proxy Testing (Alternative)

```markdown
🤝 HUMAN PROXY VALIDATION REQUEST:
"I'll describe the game concept. Please respond as if you're hearing it for the first time:
[Concept description]

What do you think the player does?
What happens when they press the button?
What's the goal and how would you achieve it?
Does this sound fun? Why or why not?"

EVALUATION CRITERIA:
□ Human understands concept immediately
□ Human can explain mechanics back correctly
□ Human sees clear connection between action and goal
□ Human expresses genuine interest or asks follow-up questions
```

#### Option C: LLM Simulation with Human Oversight (Fallback)

```markdown
🤖 LLM SIMULATED RESPONSES:
[LLM generates typical user responses based on concept clarity]

🤝 HUMAN VALIDATION REQUEST:
"I'll simulate typical user responses. Please confirm if these seem realistic:
[Simulated responses]
Do these responses indicate good understanding and engagement?"

HUMAN EVALUATION:
✅ "Responses seem realistic and positive" → Proceed
🔄 "Some responses seem unrealistic" → Refine concept
❌ "Responses indicate confusion" → Return to Phase 2
```

#### Response-Based Refinement

```markdown
Common User Responses → Refinements Needed:

"I don't understand what I'm supposed to do" → Problem definition unclear
"How do I control where things go?" → Hidden directional input detected  
"That sounds complicated" → 3-second rule violation
"Why can't I just [normal solution]?" → Problem constraints unclear
"That sounds boring" → Innovation or engagement insufficient

If users don't understand within 3 explanation sentences, redesign needed.
```

**⏭️ Proceed to Phase 3 only after Phase 2 completion criteria are met**

---

## Phase 3: Final Validation & Documentation

**Phase Input:** Complete experience from Phase 2
**Phase Output:** Implementation-ready specification with all warning signs addressed
**Completion Criteria:** ✅ All warning signs checked, ✅ Final walkthrough validated, ✅ Implementation specification complete

### 3.1 Distributed Warning Signs Check (COLLABORATIVE)

**Instead of single overwhelming check, warnings distributed throughout phases:**

#### Phase 1 Auto-Checks (LLM Handles Automatically)

```markdown
🤖 LLM AUTOMATED REJECTION CRITERIA:
One-Button Constraint Basics:
□ Description includes "player chooses", "player aims", "player selects"  
□ Requires position selection beyond press/hold/release timing
□ Multiple control schemes or input modes needed

Problem Definition Completeness:
□ Abstract expressions ("use," "utilize") cannot be concretized
□ Forces/actions needed for goal achievement don't exist in described system
□ Phenomena violating physics laws occur without basis

If ANY detected → Automatic return to appropriate phase
```

#### Phase 1 Human-Assisted Checks

```markdown
🤝 HUMAN EVALUATION REQUEST:
"Please check these potential issues with the design:

Simplicity Check:

- Can you understand the core mechanic within 3 seconds?
- Does the solution feel natural and intuitive?
- Is the theme helping or hindering understanding?

Engagement Check:

- Does this feel fun or just repetitive?
- Is there room for skill improvement?
- Would you want to play this more than once?

Please flag any concerns before we proceed."

HUMAN RESPONSE OPTIONS:
✅ "No issues detected" → Proceed
🔄 "Some concerns" → Human provides specific guidance
❌ "Major problems" → Return to appropriate phase
```

#### Phase 2 Collaborative Checks

```markdown
🤖 LLM AUTO-CHECK + 🤝 HUMAN VALIDATION:

LLM Automated Assessment:
□ Can player clear by ignoring one mechanic entirely?
□ Game reduces to simple parameter optimization (hold time, etc.)?
□ Only one strategy exists for success?

Human Final Experience Review:
"Based on the walkthrough, do you see:

- Multiple ways to approach the challenge?
- Opportunities for players to improve through understanding?
- Clear 'Aha!' moments or surprising behaviors?

Any red flags about gameplay depth?"
```

#### Phase 3 Human Final Review

```markdown
🤝 HUMAN FINAL VALIDATION:
"Please review this complete design for any obvious problems:
[Provide concise summary]

Focus on:

- Does this sound implementable and fun?
- Any references to existing games in core mechanics?
- Innovation seems genuine rather than surface-level?
- Overall coherence and implementation readiness?

Final approval to proceed with implementation?"

HUMAN RESPONSE OPTIONS:  
✅ "Approved for implementation" → Create specification
🔄 "Minor issues" → Address specific concerns
❌ "Major problems" → Return to appropriate phase with guidance
```

### 3.2 Final Walkthrough Validation (AUTOMATED + HUMAN CONFIRMATION)

**LLM Automated Final Check + Human Confirmation:**

```markdown
🤖 LLM AUTOMATED VALIDATION:
□ Problem → Solution → Goal logic chain is unbroken
□ No automatically detectable warning signs present
□ 3-second rule maintained after all innovations
□ Conceptual walkthrough completes without impossible actions

🤝 HUMAN CONFIRMATION REQUEST:
"Final walkthrough validation:

- Problem → Solution → Goal logic: [summary]
- User feedback results: [summary]
- Key innovations: [summary]
- Control system: [summary]

Does this complete design feel coherent and implementable?"

HUMAN FINAL APPROVAL:
✅ "Ready for implementation" → Proceed to specification
🔄 "Needs minor adjustments" → Address specific issues
❌ "Fundamental issues" → Return to appropriate phase

If any element fails, return to appropriate phase for fixes.
```

### 3.3 Implementation Specification Template

**Create implementation-ready specification:**

```markdown
# Game Title: [Name]

## Problem-Solution Foundation

- Player Problem: [Specific challenge player faces]
- Core Solution: [How one-button mechanic solves this problem]
- Goal Achievement Logic: [Clear path from problem → solution → goal]

## Core Mechanics

- Button Press: [Immediate action and visual feedback]
- Button Hold: [Parameter modification and visual indication]
- Button Release: [Action execution and world response]
- Control Target: [Elements directly affected by player]
- Effect Range: [Clear boundaries of player influence]

## Game Loop

- Start State: [Player faces the defined problem]
- Player Action: [How they apply the solution]
- World Response: [How environment changes]
- Success Condition: [Problem resolved, goal achieved]
- Failure Condition: [Problem worsened or new problems created]

## Visual Communication

- Problem Indication: [How player recognizes the challenge]
- Solution Availability: [How player knows when/where to act]
- Action Feedback: [Immediate response to button press/hold/release]
- Progress Indicators: [How player tracks goal achievement]
- Failure Warning: [Early indication of potential failure]

## Innovation Elements

- Light Innovation: [Simple twist that enhances the basic mechanic]
- Physical Concept: [Real-world phenomenon inspiring mechanics]
- Engagement Factor: [What makes this more interesting than the obvious solution]

## User Validation Results

- Understanding Test Results: [User comprehension feedback]
- Engagement Assessment: [User interest and curiosity levels]
- Refinements Made: [Changes based on user feedback]
```

This specification provides everything needed for the implementation guide phase.

## Chapter 6: Converting to Implementation Format

### 6.1 Staged Conversion Process

To preserve all critical design information while converting to the implementation guide format, follow this three-stage process:

#### Stage 1: Information Preservation and Analysis

**Step 1.1: Extract Implementation Categories**

```markdown
# Analyze Environment and Movement Patterns

- Environment Type: [Select from: Central fixed point/Defined path/Open space/Scrolling/Lane/Dynamic surface]
- Movement Pattern: [Select from: Static/Auto/Controlled trajectory/Gravity propulsion/Path following/Point-to-point/Physics floating/State dependent]

# Determine Mechanics Integration

- Count total mechanics used in design
- Assess interaction patterns between mechanics
- Evaluate control complexity and predictability
```

**Step 1.2: Preserve Visual Communication Details**

```markdown
# Create Visual Design Preservation Notes

- UI/UX Elements: [Compile all Problem Indication + Solution Availability + Progress Indicators]
- Feedback Systems: [Preserve detailed Action Feedback specifications]
- Warning Systems: [Maintain Failure Warning specifications]
- Input Response Chain: [Document Button Press → Hold → Release sequence with visual responses]
```

**Step 1.3: Document Validation Context**

```markdown
# User Testing Context for Implementation

- Validated Understanding Elements: [From Understanding Test Results]
- Proven Engagement Factors: [From Engagement Assessment]
- Applied Refinements: [From Refinements Made]
- Design Decision Rationale: [Link specific choices to user feedback]
```

#### Stage 2: Format Transformation

**Step 2.1: Core Mechanics Conversion**

```markdown
## Core Mechanics

- Button action: [Synthesize from Button Press + Button Hold + Button Release actions]
- World response: [Combine Control Target + Effect Range + World Response descriptions]
- Input pattern: [Map to Press/Hold/Release or Press/Hold or Press only]
- Environment type: [From Stage 1.1 analysis]
- Movement pattern: [From Stage 1.1 analysis]
```

**Step 2.2: Game Loop Transformation**

```markdown
## Game Loop

- Objective: [Extract from Success Condition + Goal Achievement Logic]
- Action: [Simplify from Player Action + detailed button mechanics]
- Obstacle: [Derive from Failure Condition + Problem definition]
- Reward: [Extract success elements from Success Condition]
```

**Step 2.3: Failure Conditions Mapping**

```markdown
## Failure Conditions (Clear Game Over)

- Primary failure condition: [Primary element from Failure Condition]
- Visual feedback: [Combine Failure Warning + relevant Action Feedback]
- Avoidable failure: [Assess from Problem-Solution Foundation + control specifications]
```

#### Stage 3: Implementation Integration

**Step 3.1: Innovation Elements Synthesis**

```markdown
## Innovative Elements

[Direct copy from Innovation Elements section, preserving:

- Light Innovation details
- Physical Concept inspirations
- Engagement Factor specifications]
```

**Step 3.2: Mechanics Integration Assessment**

```markdown
## Mechanics Integration

- Number of mechanics used: [Count from Stage 1.1 analysis]
- Mechanics compatibility: [Assess interaction patterns from preserved details]
- Control evaluation: [Evaluate from Button mechanics + Visual Communication preserved data]
```

**Step 3.3: Implementation Priority Planning**

```markdown
## Implementation Priority

- Phase 1: [Core mechanics from Button action + World response + primary Objective]
- Phase 2: [Enhanced feedback from preserved Visual Communication details]
- Phase 3: [Optimization based on User Validation Results context]
```

### 6.2 Information Preservation Strategy

**Critical Elements to Maintain Throughout Conversion:**

1. **Three-Layer Button Mechanics**: Preserve Press/Hold/Release sequence details in implementation notes
2. **Visual Communication System**: Create detailed UI specification document alongside standard format
3. **User Validation Context**: Maintain testing results as implementation decision rationale
4. **Problem-Solution Logic**: Embed core reasoning into Objective and Action descriptions

**Conversion Quality Check:**

- ✅ All Visual Communication elements have implementation equivalents
- ✅ Button Press/Hold/Release details are preserved in expanded specifications
- ✅ User validation insights inform implementation priority decisions
- ✅ Innovation elements maintain light innovation and physical concept details
- ✅ Problem-Solution Foundation logic is traceable in final format

This staged approach ensures no critical design information is lost while producing the standardized format required for implementation.

---

## 🎯 Collaborative Workflow Summary

**Optimized Human-LLM Partnership for One-Button Game Design**

### Time and Effort Optimization

- **Total Session Time**: 35-50 minutes (optimized 4-phase workflow)
- **Human Involvement**: ~30% of total time (strategic validation points)
- **LLM Autonomous Work**: ~70% of total time (systematic processing)

### Key Success Factors

1. **Concrete Theme Selection**: Human validates theme appeal and concreteness from the start
2. **Simple Creative Problem-Solving**: Light innovation applied while maintaining 3-second rule clarity
3. **Early Innovation Validation**: Human confirms creative logic makes sense and feels engaging
4. **Experience Validation**: Human confirms player understanding before final specification  
5. **Implementation Readiness**: Human ensures coherent, implementable design

### Expected Outcomes

- **Higher Success Rate**: Early validation prevents late-stage redesigns
- **Clearer Designs**: Human intuition catches ambiguity LLM might miss
- **Better Innovation**: Human judgment prevents innovation for its own sake
- **Implementable Results**: Human validation ensures practical feasibility

This collaborative approach leverages both LLM systematic processing and human intuitive judgment for optimal game design outcomes.


---
## Verbatim: archive/for_chat/cursor_knowledge/game-testing-prompt.md
# One-Button Game Testing Framework for Node.js

## Purpose

This framework provides a structured approach to systematically test and compare multiple game concepts using Node.js before implementing the selected concept in a chosen game library (e.g., crisp-game-lib). By implementing minimal prototype versions of different game concepts in Node.js, you can gather empirical evidence to select the most promising ideas before full implementation.

## Framework Overview

The testing system implemented in `cursor_knowledge/game-testing-framework.js` consists of several core components that enable concept testing in the Node.js environment:

1. **GameSimulator**: Runs game simulations with various input patterns in Node.js. It mimics key `crisp-game-lib` drawing and collision APIs.
2. **InputPatternGenerator**: Creates different button press sequences to test game behavior.
3. **GameAnalyzer**: Evaluates game performance based on key metrics.

This testing approach lets you focus on core mechanics and gameplay evaluation before adding visual implementations.

## Testing Process Instructions

### Loading the Framework

1. Create a new game concept file in the `tmp/concepts/` directory.
2. Follow the format defined by the test framework.
3. This file will be loaded by the testing framework when you run the test command.

### Game Concept Implementation

Your game concept must include at least the following exported functions:

1.  **`init(params, simulator)`**: A function that initializes the game state. It receives simulation parameters (`params`) and the `simulator` instance itself. If your concept uses character sprites (`char()`), call `simulator.loadCharacters(yourCharacterArray)` within this function.
2.  **`update(input, simulator)`**: A function that updates the game state based on the current `input` object and allows interaction with the `simulator` (e.g., for collision detection via drawing functions).
3.  **`getScore()`**: A function that returns the current score as a number.
4.  **`isGameOver()`**: A function that returns a boolean indicating if the game has ended.

Additionally, you can optionally include:

5.  **`generateExpertInput(gameState, currentTick)`**: A function that returns `true` if the button should be pressed on the given `currentTick`, based on the provided `gameState`. This allows for game-specific expert player simulation. If not provided, a generic expert pattern will be used. This function can use the `simulator`'s drawing/collision methods to make decisions.
6.  Helper functions specific to your game mechanics.
7.  Constants for game parameters.

Implement your game prototype following these guidelines:

- Use simple variables and objects to track game state (position, velocity, score, etc.).
- Define clear game over conditions in `isGameOver()`.
- Implement a meaningful scoring system in `getScore()`.
- Keep the logic minimal while preserving the core experience.
- **Collision Detection (Using Simulator's Drawing Functions):**
  - The framework's `GameSimulator` provides collision detection methods that closely mimic `crisp-game-lib`. **Use these methods for all collision checks.**
  - **Set Color:** Before drawing/checking collisions for an object, set its "color" using `simulator.color('colorName')`. Valid color names include `red`, `blue`, `green`, `yellow`, `purple`, `cyan`, `black`, `white`, `transparent`, and their `light_` variants.
  - **Drawing & Collision Check:** Call methods like `simulator.rect(x, y, w, h)`, `simulator.box(x, y, w, h)`, `simulator.line(x1, y1, x2, y2, thickness)`, `simulator.bar(...)`, `simulator.arc(...)`, `simulator.text("string", x, y)`, or `simulator.char('a', x, y)` to **both** simulate drawing the shape _and_ check for collisions against previously drawn shapes in the same frame.
  - **Get Collision Result:** These drawing functions return a `Collision` object. The result contains information about what the shape collided with.
  - **Check Result:** The returned `Collision` object has an `isColliding` property. Check for collisions like this:
    - `collision.isColliding.rect.blue`: Collided with a blue rect/box.
    - `collision.isColliding.text['!']`: Collided with the text character '!'.
    - `collision.isColliding.char.b`: Collided with character 'b'.
    - Check against any color used with `simulator.color()`.
  - **Transparent:** Use `simulator.color('transparent')` before a drawing call to check for collisions without adding the object to the collision history for subsequent checks (useful for detection zones).
  - **Do Not Use:** Standalone collision functions (like `collideRects`, `collideBoxes`) are **not available** in the simulator. All collision detection **must** be done via the drawing functions (`rect`, `box`, `line`, etc.).
- **Exposing State for Expert Input:** If implementing `generateExpertInput`, ensure your `update` function makes the necessary internal game state accessible for the generator. Assign it to `simulator.conceptState` (e.g., `simulator.conceptState = { playerPos: this.player.pos, enemies: this.enemyPool.items };`). Accessing `global.simulator` is discouraged; use the passed `simulator` instance.

### Running Evaluations

To evaluate a game concept:

1. Run the test framework using Node.js, providing the paths to your concept files:

   ```bash
   node ./cursor_knowledge/game-testing-framework.js ./tmp/concepts/concept1.js ./tmp/concepts/concept2.js ...
   ```

2. The framework will:
   - Run multiple simulations with different input patterns (Beginner, Expert, Monotonous).
   - Analyze game performance across key metrics using the `GameAnalyzer`.
   - Generate a comprehensive evaluation report comparing the concepts.

### Comparing Multiple Concepts

To compare different game concepts:

1. Implement each concept as a separate file in the `tmp/concepts/` directory.
2. Run the test framework with all concept files listed as arguments.
3. The framework automatically runs tests on all provided concepts and generates a comparison table at the end.
4. Use the comparison data and individual reports to make an informed decision on which concept to fully implement.

## Metrics and Evaluation

The framework evaluates games based on four key metrics:

1. **Skill Gap**: The difference in performance (score or duration) between "expert" and "beginner" input patterns.

   - Higher values indicate the game rewards skill and learning.
   - Low skill gaps may suggest randomness or limited depth.

2. **Game Duration**: Average survival time, especially for the expert pattern.

   - Evaluates if the game provides an appropriate play session length.
   - Too short suggests high initial difficulty or abrupt endings.

3. **Difficulty Progression**: Implicitly measured by comparing beginner/expert duration and skill gap.

   - A good gap and reasonable expert duration suggest a curve exists.
   - Poor results might indicate a flat, overly steep, or inconsistent curve.

4. **Monotonous Input Resistance**: How well the game prevents simple, repetitive inputs (no input, hold, spam) from achieving high scores or survival times.
   - Tests if the game requires varied or thoughtful interaction.
   - Low resistance indicates potential exploits or lack of engaging mechanics.

## Rating Methodology

The framework uses a comprehensive rating system:

- Each metric is scored on a scale of 0-3 points.
- The total score ranges from 0-12 points.
- Games are given one of five ratings based on the total score:
  - EXCELLENT (10-12 points)
  - GOOD (7-9 points)
  - AVERAGE (4-6 points)
  - BELOW AVERAGE (1-3 points)
  - POOR (0 points)
- Ratings help provide a quick assessment of overall concept quality.

## Testing Patterns

The framework uses these input patterns to evaluate games:

1.  **Expert Patterns**: Sophisticated input sequences mimicking skilled play.

    - **If `generateExpertInput` is provided:** The framework calls this function repeatedly, passing the current `gameState` (including `simulator.conceptState`) and `currentTick`. The function should return `true` (press) or `false` (release) for that tick. It can use `simulator` methods (like `box()`, `rect()`) to analyze the game state via collision checks.
    - **If not provided:** A generic fallback pattern is used.
    - Helps determine the **Skill Gap** and **Game Duration** potential.

2.  **Beginner Patterns**: Simple, inconsistent inputs simulating new players.

    - Used with Expert Patterns to calculate the **Skill Gap**.

3.  **Monotonous Patterns**: Simple, repetitive inputs (No Input, Hold Only, Spam Press).
    - Used to determine **Monotonous Input Resistance**.

## Implementation Guidelines

When implementing your game concept:

1.  **State Representation**:

    - Use simple data structures (variables, objects, classes) within your concept file.
    - **For Expert Input Simulation**: Expose necessary state via `simulator.conceptState` in your `update` function.

2.  **Input Handling & Game Logic**:
    - **`update(input, simulator)`**: The core game loop function.
      - Receives `input` object: `{ pressed, justPressed, justReleased, heldTime }`.
      - Receives `simulator` instance. Use `simulator.color()`, `simulator.box()`, `simulator.rect()`, `simulator.line()`, etc., for drawing and collision checks. Check the returned collision object.
      - Update your game state variables based on input and game rules.
    - **`generateExpertInput(gameState, currentTick)` (Optional)**:
      - Receives `gameState` object: `{ ticks, input, conceptState }`. Access your exposed state via `gameState.conceptState`.
      - Receives `currentTick`.
      - **Crucially, this function can call `simulator.color()`, `simulator.box()`, etc., to perform collision checks _within the expert logic_ to determine the best action.** This allows the expert AI to "see" the game world like the player does. Remember that `simulator` is available globally (`global.simulator`) within this function's context during generation, or preferably passed if the framework evolves.
      - Return `true` to press the button, `false` to release.

## Example Concept Implementation

Here's a simplified example demonstrating the required functions, optional expert input, and the **correct way to use drawing functions for collision detection**:

```javascript
// --- Sample game: Minimal Jumper ---

// Game state (scoped within the module)
let playerY, playerVy, obstacleX, score, gameTicks, isDone;

// Constants
const GRAVITY = 0.1;
const JUMP_STRENGTH = 2;
const GROUND = 90;
const PLAYER_SIZE = 6;
const OBSTACLE_SIZE = 8;
const OBSTACLE_SPEED = 1;
const PLAYER_X = 30; // Player fixed X position

// --- Required Functions ---

function init(params, simulator) {
  playerY = 50;
  playerVy = 0;
  obstacleX = 150; // Start obstacle off-screen
  score = 0;
  gameTicks = 0;
  isDone = false;
  console.log("Minimal Jumper Initialized");
  // simulator.loadCharacters(...) // If needed
}

function update(input, simulator) {
  if (isDone) return;

  gameTicks++;

  // === Player Logic ===
  playerVy += GRAVITY;
  playerY += playerVy;

  // Ground check
  if (playerY >= GROUND) {
    playerY = GROUND;
    playerVy = 0;
  }

  // Jump on press (only if on ground)
  if (input.justPressed && playerY >= GROUND - 1) {
    playerVy = -JUMP_STRENGTH;
  }

  // === Obstacle Logic ===
  obstacleX -= OBSTACLE_SPEED;
  if (obstacleX < -OBSTACLE_SIZE) {
    obstacleX = 150; // Reset position
    score++;
  }

  // === Collision Detection & Drawing Simulation ===
  // **IMPORTANT:** Call drawing functions to check collisions.
  // Order matters: Check player against things drawn *before* it.

  // 1. Simulate drawing the obstacle (and add its hitbox)
  simulator.color("red"); // Obstacle is red
  // Use box() for center-based coordinates. Store result (optional here).
  simulator.box(
    obstacleX,
    GROUND - OBSTACLE_SIZE / 2, // Position obstacle on the ground
    OBSTACLE_SIZE,
    OBSTACLE_SIZE
  );

  // 2. Simulate drawing the player and check collision *against existing hitboxes* (the obstacle)
  simulator.color("blue"); // Player is blue
  const playerCollision = simulator.box(
    PLAYER_X,
    playerY,
    PLAYER_SIZE,
    PLAYER_SIZE
  );

  // 3. Check the player's collision result
  if (playerCollision.isColliding.rect.red) {
    // Did the blue player box hit the red obstacle box?
    isDone = true; // Game over on collision
    console.log(`Game Over! Final Score: ${score}`);
  }

  // --- Expose State for Expert Input ---
  // Make current state available for generateExpertInput
  simulator.conceptState = {
    playerY: playerY,
    playerVy: playerVy,
    obstacleX: obstacleX,
    groundY: GROUND,
    playerX: PLAYER_X,
  };
}

function getScore() {
  return score;
}

function isGameOver() {
  return isDone;
}

// --- Optional Expert Input ---
function generateExpertInput(gameState, currentTick) {
  const state = gameState.conceptState;

  // Basic Expert Logic: Jump if obstacle is close and player is on the ground
  const jumpThreshold = 40; // How close the obstacle needs to be

  if (
    state.playerY >= state.groundY - 1 && // Player is on the ground
    state.obstacleX > state.playerX && // Obstacle is to the right
    state.obstacleX < state.playerX + jumpThreshold // Obstacle is close enough
  ) {
    // Check if jumping *now* would likely clear the obstacle.
    // (This is a simplified check; real logic might be more complex)
    // We could even use simulator.box() here to predict future positions,
    // but let's keep it simple for the example.
    return true; // Press button to jump
  }

  return false; // Don't press button
}

// Export the functions
module.exports = {
  init,
  update,
  getScore,
  isGameOver,
  generateExpertInput, // Export the expert function if defined
};
```

## Interpreting Test Results

The test framework will provide detailed results for each metric:

1. **Skill Gap Analysis**:

   - A breakdown of scores achieved by expert vs. beginner patterns
   - Specific areas where skilled play made the biggest difference
   - Suggestions for enhancing or balancing skill requirements

2. **Duration Assessment**:

   - Distribution of game duration across multiple simulations
   - Factors influencing premature game overs
   - Recommendations for adjusting difficulty to achieve target duration

3. **Progression Evaluation**:

   - Analysis of how challenge increases over time
   - Identification of difficulty spikes or plateaus
   - Guidance on creating smoother progression curves

4. **Input Diversity Requirements**:
   - Effectiveness of different input strategies
   - Identification of dominant strategies or exploits
   - Suggestions for mechanics that encourage varied inputs

## Recommendations

Based on the test results, consider:

1. **Adjusting Parameters**: Fine-tune game constants to address specific issues
2. **Mechanic Modifications**: Revise core mechanics that aren't performing well
3. **Feature Additions**: Add complementary features to enhance strengths or address weaknesses
4. **Concept Pivots**: For low-scoring concepts, consider more substantial redesigns or alternative approaches
