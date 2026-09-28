# Jumping Ball Runner (OpenAI GPT-5 launch page) — vendor demo, short bulleted single-file spec

- **Source URL:** https://openai.com/index/introducing-gpt-5/ ("Here are some examples of what GPT-5 has created with just one prompt")
- **Model/tool:** GPT-5 (ChatGPT/API, single response, no agent loop), Aug 2025
- **Genre:** Endless runner (one-button jump), single HTML file
- **Result evidence:** Embedded playable demo on the launch page
- **Quality signal:** Vendor-selected showcase, so it is cherry-picked by design and there is no independent assessment. Useful as an example of what a vendor considers a "good one-shot prompt" for a chat model.
- **One-shot vs iterative:** One-shot

## Verbatim prompt

```
Create a single-page app in a single HTML file with the following requirements:
- Name: Jumping Ball Runner
- Goal: Jump over obstacles to survive as long as possible.
- Features: Increasing speed, high score tracking, retry button, and funny sounds for actions and events.
- The UI should be colorful, with parallax scrolling backgrounds.
- The characters should look cartoonish and be fun to watch.
- The game should be enjoyable for everyone.
```

Traits: it names the game and a one-sentence goal (the core loop), gives a short list of feature nouns covering difficulty ramp, meta (high score), restart, and juice (sounds), and adds tone/art adjectives. The scope is tiny and fixed by the delivery constraint (single HTML file).
