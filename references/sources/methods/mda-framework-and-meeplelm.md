# MDA framework (Hunicke, LeBlanc, Zubek 2004) + MeepleLM virtual playtester (2026)

## A. MDA: A Formal Approach to Game Design and Game Research
- URL: https://users.cs.northwestern.edu/~hunicke/MDA.pdf (AAAI: https://aaai.org/papers/ws04-04-001-mda-a-formal-approach-to-game-design-and-game-research/)
- Authors: Robin Hunicke, Marc LeBlanc, Robert Zubek; AAAI Workshop on Challenges in Game AI, 2004 (taught at GDC Game Design and Tuning Workshop 2001-2004)
- Why it matters: gives agents a vocabulary to replace "make it fun" with a named target aesthetic and a causal path (aesthetic <- dynamic <- mechanic). This is how you turn "it's boring" feedback into a mechanic-level root cause instead of adding content.

Verbatim:
- "thinking about the player encourages experience-driven (as opposed to feature-driven) design."
- "Mechanics describes the particular components of the game, at the level of data representation and algorithms. Dynamics describes the run-time behavior of the mechanics acting on player inputs and each others' outputs over time. Aesthetics describes the desirable emotional responses evoked in the player, when she interacts with the game system."
- "the content of a game is its behavior – not the media that streams out of it towards the player."
- "From the designer's perspective, the mechanics give rise to dynamic system behavior, which in turn leads to particular aesthetic experiences. From the player's perspective, aesthetics set the tone, which is born out in observable dynamics and eventually, operable mechanics."
- "In describing the aesthetics of a game, we want to move away from words like "fun" and "gameplay" towards a more directed vocabulary."
- Taxonomy: "1. Sensation Game as sense-pleasure 2. Fantasy Game as make-believe 3. Narrative Game as drama 4. Challenge Game as obstacle course 5. Fellowship Game as social framework 6. Discovery Game as uncharted territory 7. Expression Game as self-discovery 8. Submission Game as pastime"
- Examples: "The Sims: Discovery, Fantasy, Expression, Narrative."
- "If the player doesn't see a clear winning condition, or feels like they can't possibly win, the game is suddenly a lot less interesting."
- "Expression comes from dynamics that encourage individual users to leave their mark: systems for purchasing, building or earning game items, for designing, constructing and changing levels or worlds, and for creating personalized, unique characters. Dramatic tension comes from dynamics that encourage a rising tension, a release, and a denouement."
- Worked root-cause example (Monopoly): runaway-leader feedback loop -> "As the gap widens, only a few (and sometimes only one) of the players is really invested. Dramatic tension and agency are lost." Fix proposed at the MECHANIC level (subsidies/taxes, time pressure), then "play testing and tuning."
- "our dynamic models help us pinpoint where problems may be coming from."

## B. MeepleLM: A Virtual Playtester Simulating Diverse Subjective Experiences
- URL: https://arxiv.org/abs/2601.07251 (html v5 2026-04-12); ACL 2026 per papernotes
- Authors: Zizhen Li, Chuanhao Li, Yibin Wang, Yukang Feng, Jianwen Sun, Jiaxin Ai, Fanrui Zhang, Mingzhu Sun, Yifei Huang, Kaipeng Zhang
- Why it matters: evidence that off-the-shelf LLMs are poor "fun" judges -- positivity and central-tendency bias -- and that MDA-structured reasoning + explicit player personas improves alignment with real player opinion.

Findings:
- General LLMs: central tendency bias ("play it safe", GPT-5.1 Wasserstein 0.950 vs MeepleLM 0.221); positivity bias / "mode collapse" to safe high scores (7-9) missing legitimate negative feedback; generic homogeneous voice; no persona differentiation.
- Personas: System Purist (mechanical elegance, depth), Efficiency Essentialist (streamlined, minimal downtime), Social Lubricator (party/group), Narrative Architect (thematic immersion/story), Thrill Seeker (high-risk volatility).
- MDA-Reasoning chain (verbatim step questions): Mechanics "What specific content does the review explicitly mention?"; Dynamics "What Interaction or System Dynamic occurred during play?"; Aesthetics "What was the final Aesthetic Experience or emotional feeling?"
- Ablation: removing MDA reasoning, persona conditioning, or rulebook context each significantly degrades performance.
- Opinion recovery 69.77% vs GPT-5.1 63.44%; 70% user preference.

## C. Dan Cook skill atoms (secondary -- original lostgarden pages returned 403)
- https://lostgarden.com/2007/07/19/the-chemistry-of-game-design/ ; https://lostgarden.com/2012/04/30/loops-and-arcs/
- Skill atom = Action -> Simulation -> Feedback -> Modeling (player updates mental model). Secondary-quoted claim: "With skill chains, you can always hook up logging software and observe where atoms light up and where they burn out." Loops = mechanics exercised repeatedly; arcs = content consumed once (narrative). NOT verified verbatim against original.
