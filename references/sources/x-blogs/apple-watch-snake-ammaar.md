# Heart-rate Snake for Apple Watch (Ammaar Reshi) — short bulleted mechanic spec + 4 debug turns (full transcript public)

- **Source URL:** https://x.com/ammaar/status/1894131337583288636 (2025-02-24); full conversation https://claude.ai/share/ac45287c-3d56-4a7d-a438-bbe8c5e3ce06
- **Model/tool:** Claude 3.7 Sonnet (claude.ai chat, copy-paste into Xcode, no agent)
- **Genre:** Snake variant (watchOS, SwiftUI + HealthKit); the twist is that snake speed is driven by heart rate
- **Result evidence:** Demo video on the watch in the tweet, plus the full chat transcript with code
- **Quality signal:** ~232k views / 1.4k likes. Featured in Alex Albert's 3.7 launch highlights.
- **One-shot vs iterative:** "In just 5 prompts." Turn 1 is the spec. Turn 2 pastes 5 compile errors (HKQuery API misuse). Turn 3: "jumpy... dropping frames, and when I swipe it totally freezes". Turn 4: "still playing SUPER slowly, there's definitely some major bug". Turn 5 is the human diagnosing the root cause: "maybe the way youre reading the heartbeat and controlling speed of the game is making it appear like its 1-2 FPS but you need to update it with periodic heartbeat checks... rather than waiting for updates". The model then decoupled the render loop from the HealthKit callbacks.

## Verbatim prompt (turn 1)

```
Write all of the code for a snake game for the Apple Watch which:
* Uses your heartbeat to determine the speed of the snake, we'll need to use HealthKit for this (and tell me how to set it up)
* You swipe on the screen to move the snake up, down, left, right
* The walls don't kill you, you just appear from the other side, so the only way to die is to run into your snake, just like the Nokia version
* Use graphics like the Nokia version, that camo green look those screens had

Write all of the code and outline each file so I can copy and paste this and run it
```

## Follow-up turns (verbatim)

2. `I get these 5 errors` + pasted Xcode errors (`Value of type 'HKQuery' has no member 'updateHandler'`, ...)
3. `Hmm so the game appears properly and everything but is jumpy with the snake rather than smooth motion and it feels like its dropping frames, and when I swipe it totally freezes the game rather than changing the direction of the snake smoothly`
4. `The game is still playing SUPER slowly, there's definitely some major bug`
5. `the game is still frozen on start, maybe the way youre reading the heartbeat and controlling speed of the game is making it appear like its 1-2 FPS but you need to update it with periodic heartbeat checks or something rather than waiting for updates to update the speed?`

Lesson: the spec gave every mechanic rule clearly (wraparound, the only death condition, input, art reference) but said nothing about the *timing architecture* (game tick vs. sensor update rate). That gap is exactly where the build broke, and the model didn't fix it until the human named the cause.
