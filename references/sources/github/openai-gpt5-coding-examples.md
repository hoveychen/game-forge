# OpenAI gpt-5-coding-examples — vendor-curated one-shot game prompts (GPT-5 / GPT-5.2)

- Repo: https://github.com/openai/gpt-5-coding-examples  (gallery: https://gpt5-coding-examples.vercel.app/ — each demo shows its prompt and runs live)
- Stars: ~1,913 (Sep 2026)
- Tool/model: GPT-5 and GPT-5.2, "generated entirely in a single prompt, without writing any code by hand" (vendor claim; curated/selected, so survivorship bias — these are the winners).
- Genre: small arcade/casual games (asteroids dogfight, endless runner, maze, typing, catcher, tic-tac-toe, trivia, target clicker, color match) among 64 total demos.
- Result evidence: hosted playable builds + screenshots for each, same prompt re-run on 5.2 for comparison (asteroid-game vs asteroid-game-5.2).
- One-shot vs multi-session: strictly one-shot, zero-shot.
- Notable: the prompt template is "Name / Goal / Features / UI" bullet list + hard output constraint (single HTML file, or single next.js page.tsx). The asteroid prompt adds "Be creative with the design... Ensure the gameplay works and is fun." These are the lower bound: tiny scope, one file, one loop.
- Useful as a baseline contrast: small-scope games succeed one-shot with ~5 lines of spec; nothing here is > 1 core loop.

---
## Verbatim prompts (all yaml tagged game or game-like)

### asteroid-game-5.2.yaml
```yaml
id: asteroid-game-5.2
title: Asteroid Game
prompt: |
  Make a 2d space game, in which I can fly a ship, avoid and blow up asteroids, and dogfight with other computer-controlled AI. Be creative with the design of the ships. Ensure the gameplay works and is fun.
  Output code in a single next.js page.tsx file, which can be pasted directly into a next.js app created by create-next-app, alongside any context or instructions needed to run it.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/asteroid-game-5.2.png
tags:
  - game
```

### asteroid-game.yaml
```yaml
id: asteroid-game
title: Asteroid Game
prompt: |
  Make a 2d space game, in which I can fly a ship, avoid and blow up asteroids, and dogfight with other computer-controlled AI. Be creative with the design of the ships. Ensure the gameplay works and is fun.
  Output code in a single next.js page.tsx file, which can be pasted directly into a next.js app created by create-next-app, alongside any context or instructions needed to run it.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/asteroid-game.png
tags:
  - game
```

### color-match-challenge.yaml
```yaml
id: color-match-challenge
title: Color Match Challenge
prompt: |
  Create a single-page app in a single HTML file for a fast-paced “color match” game.
  - Show a word (e.g., “RED”) in a random font color — player must click the correct color button (not the word meaning).
  - Keep score based on correct answers within 30 seconds.
  - Use large typography, color-coded buttons, and smooth button press animations.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/color-match-challenge.png
tags:
  - game
```

### escape-the-maze.yaml
```yaml
id: escape-the-maze
title: Escape the Maze
prompt: |
  Create a single-page app in a single HTML file with following requirements:
  - Name: Escape the Maze
  - Goal: Navigate from start to finish in a randomly generated maze.
  - Features: Arrow key controls, timer, shortest path bonus, replay button.
  - The UI should be clear with visible maze walls and a movable avatar.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/escape-the-maze.png
tags:
  - game

```

### fun-game.yaml
```yaml
id: fun-game
title: Fun Game
prompt: |
  Create a single-page app in a single HTML file with the following requirements:
  - Name: Fun Game
  - Goal: Jump over obstacles to survive as long as possible.
  - Features: Increasing speed, high score tracking, retry button, and funny sounds for actions and events.
  - The UI should be colorful, with parallax scrolling backgrounds.
  - The characters should look cartoonish and be fun to watch.
  - The game should be enjoyable for everyone.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/fun-game.png
tags:
  - game
```

### falling-object-catcher.yaml
```yaml
id: falling-object-catcher
title: Falling Fruit Catcher
prompt: |
  Create a single-page app in a single HTML file for a falling objects game.
  - Player controls a basket at the bottom (arrow keys or mouse) to catch falling fruits.
  - Score increases with each catch; missing 3 ends the game.
  - Use bright, playful colors, smooth animations, and clear score display.
  - The falling objects should be large enough for kids
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/falling-object-catcher.png
tags:
  - game
```

### trivia-quiz-game.yaml
```yaml
id: trivia-quiz-game
title: Trivia Quiz
prompt: |
  Create a single-page app in a single HTML file that hosts a themed trivia quiz.
  - Inputs: question text, multiple-choice answers, correct answer.
  - Show one question at a time with card-style layout, large readable text, and animated feedback (green check or red X).
  - Include a progress bar at the top and final score display at the end.
  - Create 10 built-in quiz and display them randomly; the quiz must be basic level for US citizens
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/trivia-quiz-game.png
tags:
  - game
```

### typing-rain-5.2.yaml
```yaml
id: typing-rain-5.2
title: Typing Rain
prompt: |
  Create a single-page app in a single HTML file with the following requirements:
  - Name: Typing Rain
  - Goal: Type falling words before they reach the bottom.
  - Features: Increasing difficulty, accuracy tracker, score.
  - The UI should be the city background with animated raindrop words.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/typing-rain-5.2.png
tags:
  - game
```

### tic-tac-toe-game.yaml
```yaml
id: tic-tac-toe-game
title: Tic Tac Toe
prompt: |
  Create a single-page app, in a single HTML file:
  a Tic Tac Toe game that is Roman Empire themed, fully responsive, and modern.

  Requirements:
  - Full-viewport, fluid board (vmin-based) and mobile/desktop responsive layout.
  - Roman theme: marble background, gold accents, SPQR crest, subtle Colosseum vibe.
  - Clean top bar with only three buttons: “New Round”, “Customize”, “Reset Scores”.
  - Put all options in a “Customize” dialog:
    • Theme: Marble Day / Night Legion
    • Glyphs: Standard X/O or Gladius/Laurel
    • Mode: 2-player or vs AI
    • First move: X or O
    • AI discipline: Perfect / Pragmatic / Reckless
  - Game logic:
    • Perfect-play AI via minimax with difficulty handicaps
    • Scoreboard for X, O, and Draws
    • Gold win highlight + non-overlapping victory banner under header
    • Canvas-based confetti on win (no DOM node spraying), respects prefers-reduced-motion
  - Accessibility: ARIA roles for grid/cells, live status updates, keyboard + touch support.
  - Visuals: smooth hover/press states, soft shadows, rounded corners, scalable typography.
  - Constraints: no element overlap or flashing; no external JS frameworks; one HTML file with inline CSS/JS (Google Fonts allowed).
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/tic-tac-toe-game.png
tags:
  - game
```

### target-clicker.yaml
```yaml
id: target-clicker
title: Target Clicker
prompt: |
  Create a single-page app in a single HTML file for a target clicking challenge.
  - Random targets appear briefly around the screen — click them to score.
  - Game runs for 20 seconds; show score and accuracy at the end.
  - Use colorful animated targets and a modern scoreboard overlay. The background should be a light color.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/target-clicker.png
tags:
  - game
```

### typing-rain.yaml
```yaml
id: typing-rain
title: Typing Rain
prompt: |
  Create a single-page app in a single HTML file with the following requirements:
  - Name: Typing Rain
  - Goal: Type falling words before they reach the bottom.
  - Features: Increasing difficulty, accuracy tracker, score.
  - The UI should be the city background with animated raindrop words.
screenshot_url: https://cdn.openai.com/devhub/gpt5prompts/typing-rain.png
tags:
  - game
```
