# Pixel Darts: From Pub to Glory — vibe-coded Steam game over 8 months (~1000 h), honest breakdown

- Reddit: https://www.reddit.com/r/vibecoding/comments/1u9g7ym/ (r/vibecoding, 474 upvotes, 122 comments, 2026-06)
- Steam: https://store.steampowered.com/app/4712560/Pixel_Darts_From_Pub_to_Glory/ (demo live; full release ~1 month after post)
- Model/tool: Claude Opus 4.5 -> 4.8 as "frontend dev", GPT 5.1/5.2 -> 5.5 as "backend dev"; Phaser 3; ElevenLabs SFX, Suno music; Nano Banana Pro / GPT Image 2 art reworked by hand in Aseprite; ~500 EUR AI cost
- Genre: 90s-arcade-style darts game with career/story mode
- Outcome: SUCCESS (shipped Steam demo; commenters found it fun/polished). Author (non-coder, literature M.A.) explicitly says he "still couldn't just completely 'prompt' my way to a game".
- Session style: MULTI-SESSION, 8 months, ~4h/day

## Key lessons (verbatim)
Prototype != game:
> "The first attempts with Opus as frontend dev and GPT 5.1/5.2 as backend dev went well, and the basic gameplay mechanic came together relatively quickly. These are the kind of prototypes that then often get shown on Twitter/Reddit et al. and get hailed as the death knell of the gamedev industry. But going from a prototype like that to a real game is a very long road."

The fun problem was a design problem, solved by a human-chosen genre frame, not by code:
> "the question came up fairly quickly: how can the game be fun when the mechanic is so simple? ... if you replicate the throwing motion with the mouse, then a player probably figures out fairly quickly how to throw in order to always hit high scores (and the game gets boring fast). At that point there was no real genre or direction set for the game yet. There was a board and an arrow sprite ..."
> "In conversations with a friend I came to the idea that the genre of 90s arcade games would be a good fit ... he also pointed me to Super Punch-Out!! Since then I actually set a certain focus for the game: I wanted to translate the '90s arcade feeling' onto the sport of darts."
> Design pillars derived: "simple gameplay mechanic with direct player feedback on whether the short action was successful ... 1-on-1 gameplay: building rivalries, focus on the 'individuality' of the characters ... high score mechanic"

Juice > mechanic:
> "Over the following months (especially January through April) I worked a lot on giving the game more 'JUICE'. ... More important than the pure gameplay mechanic became the feedback through visual flashes/shakes and SFX."

Content by the human:
> "A career mode had to happen, and in the meantime I wrote the story, dialogues etc. for it. ... This part was written entirely by me"
> "one-shot prompts ('game prototypes') and the like are also completely soulless. I hope that over the last 8 months I was able to give my game some 'soul' ... through writing all of the content components myself (NPCs, dialogues, story, and so on)"

What kept it from collapsing — a mandatory design/state matrix every agent reads first:
> "**The thing that kept the project from collapsing: strict prompt engineering.** In the process there are an incredible number of small decisions and adjustments which, partly due to the nature of vibe coding, lead to bugs popping up again in other places. I set up a documentation requirement for every smaller adjustment early on – a matrix covering gameplay mechanics, design decisions, and backend state – which every agent has to read before touching the code. It kept the bigger bugs in check. Toward the end, token usage climbed significantly; I tried to offset that by networking sub-agents together. The bugs still appeared"

Project selection criteria (up front):
> "I myself have a connection to the gameplay mechanic or to the game / the gameplay mechanic has to be simple! / the engine should be something as well documented as possible (LLM-friendly) and 'simple'"

Top commenter (Some-Ice-4455): "The AI can generate a lot, but the actual project still lives or dies on structure, testing, taste, rollback discipline, and knowing when something is broken. ... Once a project gets past toy size, the problem is less 'can AI write code?' and more 'can you keep the AI from forgetting the architecture and breaking something that already worked?'"
