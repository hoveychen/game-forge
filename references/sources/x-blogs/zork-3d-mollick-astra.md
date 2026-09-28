# Zork: Underground Empire 3D (Ethan Mollick) — "adapt an existing complete design" prompt + 4 short playtest nudges (full transcript in image)

- **Source URL:** https://x.com/emollick/status/2096047660662722620 (2026-09-05). All prompts are in the screenshot in his self-reply https://x.com/emollick/status/2096051087471943969 (image https://pbs.twimg.com/media/HRaomKnaoAAb6tD.jpg), transcribed below.
- **Model/tool:** GPT-6 Astra in Codex (screenshot shows "Worked for 4h 31s" after the first prompt), with Blender/Unity access and imagegen; evaluator agents
- **Genre:** First-person 3D action-adventure adaptation of Zork I (1977 text adventure), Three.js
- **Result evidence:** Playable at https://zork-underground-empire.netlify.app/ ; open source at https://github.com/emollick/zork-underground-empire (~43 stars); Windows build
- **Quality signal:** ~222k views / 1.8k likes. Mollick: "I did play through 80% of the game, and it does appear to have all 60 rooms fully built out and the puzzles all solveable." A community-spotted inaccuracy (house in a field vs woods) was fixed afterwards.
- **One-shot vs iterative:** 1 main prompt (4.5h autonomous run) + 3 follow-up nudge messages, all from playtesting.
- **Author's own explanation of why it worked:** "it has Zork as its base, which fills in the jagged frontier of the weakest parts of AI (coherent long-run narrative, puzzle design, writing) while using the AI for what it is strongest at."

## Verbatim prompts (transcribed from screenshot)

Prompt 1:
```
turn Zork (which is open source) into a full 3D playable modern action-adventure game. you have blender and unity access if you need it, as well as imagegen capabilities. work back and forth with evaluator agents until it is terrific and aaa level
```
(Worked for 4h 31s)

Prompt 2:
```
use your own design approach, it should look like a modern game
```

Prompt 3:
```
also your really need to make sure any gameplay loops you add are fun and appropriately scaled for challenge
```

Prompt 4:
```
a few things: seperate rooms work great when they have transitions between them (rooms in the house) but make less sense when it is going around the back of the house. you may need to convert those scenes so they operate in one place (walking around the house takes you to the back, etc). whereever possible use the original language from Zork (you can download the game or the transcript). Some of the hints are too broad and easy
```

Prompt 5:
```
on challenges, you want to keep the spirit of Zork, like the falling darkness is great in the basement, but you are missing the iconic grue lines (and visuals?). and there are lots of lines you wrote that are just references to things that haven't happened yet (the songbird mentions a canary, the front path to the house mentions you will unlock it later, etc.)
```

Pattern: the "spec" is an existing, complete, machine-readable design (the open-source Zork source/transcript: 60 rooms, puzzles, text). The human follow-ups are playtest critiques about spatial continuity, source fidelity, hint difficulty, and narrative ordering bugs (foreshadowing things that haven't happened). None of them are implementation instructions.
