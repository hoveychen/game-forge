# Der Koloss (Rishi, @0xRishi) — "fork my existing game and bring the visuals to AAA" overhaul prompt (Opus 5), lineage to Modern Claudefare and Astral War

- **Source URL:** https://x.com/0xRishi/status/2081230708593590378 (2026-07-26, ~140k views). The prompt is verbatim in the author's self-reply in the thread.
- **Model/tool:** Claude Code, Opus 5 High mode; ElevenLabs for SFX/voice. The original v1 was built the previous weekend with Kimi K3 (https://x.com/0xRishi/status/2080024077662847030)
- **Genre:** CoD-Zombies-style wave shooter (pack-a-punch, perk machines, mystery box, teleporters, doors), Three.js
- **Result evidence:** Playable at https://www.derkoloss.com/ (solo/multiplayer); codebase released (linked in thread); 28-min multiplayer gameplay video
- **Quality signal:** The author: "the first-shot output nailed the visual overhaul and movement, but as with most large single-shot overhauls, it still had a lot of rough edges"; "it did NOT do a good job overhauling the soldier models". Rest of the session went to "iterating to iron out the kinks".
- **One-shot vs iterative:** One overhaul prompt (dictated via WisprFlow) with screenshots of Shumer's video attached, then iterative polish in the same session.
- **Lineage (useful for "start from an existing codebase" pattern):** Der Koloss -> Modern Claudefare (https://x.com/0xRishi/status/2084322235788226653, Opus 5 High, "a few days", 84.1k LOC, 4 remade maps, Meshy for 8 rigged soldiers because "LLMs... struggle with creating humans/creatures & animating them properly", 430+ ElevenLabs audio files) -> Astral War (https://x.com/0xRishi/status/2096079660605997264, GPT-6 Astra, "built in a day"; key addition: a "MASSIVE library of image refs" of every gun/map generated with GPT Image 2 as "a clear visual reference & bar for Astra to hillclimb against via... Gauntlet Loop", see http://astralwar.io/refs). Those two later posts don't include verbatim prompts.

## Verbatim prompt ("spoken/transcribed with @WisprFlow hence the conversational format")

```
I want you to fork this zombie project directory, and I want us to make the environment, the map, and the gameplay look AAA, just like this tweet (screenshots attached for visual reference): https://x.com/mattshumer_/status/2081054356405731740?s=46

Right now, the game you'll see is very blocky and not realistic... I want it to look like Battlefield 6 or the latest Call of Duty, with motion blur, amazing shadows, lighting, microanimations, and all the other bells/whistles that differentiate a vibe-coded game from a studio-level game.

I want the map and gameplay and logic to effectively stay the same, but the visuals and movement need a huge update.

Let's not edit this directory directly. I just want you to fork it and then redo everything graphics-wise:
* visual theme
* movement
* all the models
* etc

If you need new sound effects, you can do it with ElevenLabs, and you can even do new music with ElevenLabs or text-to-speech, anything. You can also use the ElevenLabs library of sound effects we already have as well. Whatever's best.

For the 3D modeling of the zombies, the gun, that map, the lighting, everything, the motion blur, the movement systems, how smooth it is, how your camera shakes when you run, all that stuff: that's gotta get to that level of quality of latest Battlefield/COD.

Work until you are done. Test using browser if you need. And just have many recursive loops until its fully up to AAA standards.
```
(note: attached screenshots of Matt's video for visual reference)

Traits: the gameplay design is frozen ("map and gameplay and logic... stay the same") and only presentation is in scope. Visual targets are named references plus attached screenshots, and there's a concrete list of polish features (motion blur, shadows, micro-animations, camera shake when running).
