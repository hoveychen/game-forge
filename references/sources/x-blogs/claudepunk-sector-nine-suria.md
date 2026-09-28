# Claudepunk 2077 / "Sector Nine" (Yogi Suria, @suriadesign) — property-based feature brief with process clause

- **Source URL:** https://github.com/kalaanakonda/Claudepunk2077 (PROMPT.md, "The brief this project was built from"). Owner is Yogi Suria (GitHub twitter_username: suriadesign). I did not locate the original X post; secondary coverage is 36kr (https://eu.36kr.com/en/p/3916419636555394) and explainx's "Top 10 Opus 5 game prompts".
- **Model/tool:** Claude Opus 5 (per coverage), parallel specialised agents + critic passes
- **Genre:** First-person cyberpunk exploration / immersive sim-lite (free roam, environmental storytelling, one mission chain)
- **Result evidence:** Repo only (3 stars), no deployed link. README documents what shipped: Kessel Row, Drip Alley, and Vantage Stack complete; 3 areas are **stubs**; the elevator isn't wired. It includes measured perf (median 2.6 ms, p95 6.1 ms on a 200-frame path) and a list of perf fixes.
- **Quality signal:** Weak public signal (low stars; the tweet wasn't found). Media coverage cites it as a copy of the "Challenge Loop" pattern. The README is honest about gaps.
- **One-shot vs iterative:** 14 commits over about 13 hours (2026-07-26). **Caveat:** PROMPT.md reads as a consolidated spec written or edited after the build. It says "Do not reference... any... previously supplied prompt". The README describes "retrofitting daylight onto a night-first scene", which suggests day/night and weather were added mid-project and then folded back into the brief. Treat it as "final spec", not "literal seed prompt".
- **Notable spec traits:** A standing IP-originality constraint that "outranks everything"; real-world references are to be read as *properties* (proportion, mood), not things to copy; many **testable anti-failure rules** ("Pedestrians must never visibly disappear... do not simply widen a despawn radius", "Sky traffic must bunch", "Dark areas must stay readable, not black", "Rain must interact visually with surfaces rather than being a screen-space overlay"); "Evaluate whether real rigged human models are viable... justify with numbers"; performance as a design requirement ("Measure it; do not assume it"); and a process clause (parallel disciplines, independent critical review, capture rendered views).

## Verbatim prompt (PROMPT.md)

# The Prompt

The brief this project was built from.

What was actually delivered, what was cut, and what is still missing is recorded in
[README.md](README.md). This document is the specification.

---

## Standing constraint

> Keep the setting, architecture, characters, signage, corporations, technologies,
> terminology, visual identity, and lore **completely original**. Do not reference,
> imitate, name, or present the project as being derived from any existing game, film,
> franchise, studio, or previously supplied prompt.

This outranks everything else in this document. Where a requirement below names a
real-world reference point, treat it as a description of a *property* — a proportion, a
mood, a genre of sound — never as a thing to reproduce.

---

## The game

Build an original **first-person cyberpunk exploration game in Three.js**, focused on
immersive free-roaming, environmental discovery, atmosphere, and systemic interaction.

It must feel like a **self-contained place**, not a tech demo. A continuous world with no
linear level design — the player should be able to pick a direction and find that
somebody thought about what is down there.

---

## Movement and traversal

Walk, sprint, crouch, jump, climb, mantle. Stairs, ladders, uneven terrain, and a real
response to falling. Acceleration and inertia rather than instant velocity. Restrained
procedural camera — footsteps, landing, sprint, breathing — **without excessive shake**.
Per-surface footstep sounds.

---

## The district

Narrow neon alleys, large streets, rooftops, elevated pedestrian bridges, industrial
machinery, maintenance tunnels, underground, apartment corridors, storefronts, food
stalls, abandoned interiors, ventilation, drainage channels, construction zones, hidden
rooftop spaces, distant megastructures, holographic advertising, cables, and inhabited
clutter.

Avoid repetitive procedural-looking placement. **Every area needs a recognisable
identity** — you should be able to say where you are from one screenshot.

The city must not stop existing at the edge of the playable street. Build out the ground
**behind the main frontages** — service yards, back lots, the rear of the blocks — so the
district has a back as well as a front.

### Vertical scale

Include **extremely tall, extremely slender towers** — a proportion target, not a design
reference: height-to-width ratios far beyond ordinary architecture. Keep the designs
original.

The distant skyline needs **real parallax and depth**, resolving into layers as the
player moves, rather than reading as a painted backdrop.

---

## Atmosphere

Volumetric fog, localised mist, rain, wet surfaces, puddles, reflected signage, steam
vents, drifting particles, haze, wind, flickering electronics, sparks, animated ads,
moving shadows, light shafts, smoke.

**Rain must interact visually with surfaces rather than being a screen-space overlay.**

---

## Lighting

Physically believable but cinematic. Neon, screens, lamps and vehicles must *meaningfully
illuminate nearby surfaces*. Strong contrast between warm interiors and cold streets.

- **Dark areas must stay readable, not black.**
- **Bloom must represent glare, not wash out the image.** Glare should spread widely
  rather than sit as a tight halo around each source.

---

## Materials

Layered surface variation: decals, stains, grime, leaks, scratches, repair marks,
graffiti, labels, stickers, wear. **No large perfectly clean surfaces.**

---

## Signage

The density of commercial signage is what makes a district feel inhabited and sold-to.
The build needs **a great deal of text, logos and billboards** — layered up every
elevation, on brackets over the street, on the roofs — not a handful of hero signs.

---

## Time of day and weather

A full **day/night cycle** with both a day scene and a night scene, switchable directly
and runnable as a loop.

**Weather styles** as a separate axis from the clock: rain, drizzle, cloudy, a clear
sunny day, storm. Rain must also be independently switchable off, so "clear sky" and "not
currently raining" stay distinguishable.

---

## Ambient life

Pedestrians with non-repeating behaviour, vendors, workers, security and delivery drones,
street traffic, and sky traffic.

**Crowd density must be high enough that the street reads as busy** at street level, not
merely populated.

**Sky traffic must bunch.** Evenly spaced vehicles read as a dotted line; real traffic
arrives in clumps with gaps between them.

**Pedestrians must never visibly disappear.** Nobody may blink out inside the player's
view. Agents that want to leave should be routed into the quieter parts of the district —
the back alleys and service ground — and the population should be maintained on the main
street by **circulating agents through the other areas**. Build a system for this; do not
simply widen a despawn radius.

Evaluate whether **real rigged human models** are viable for the crowd, and justify the
answer with numbers before committing either way.

---

## Audio

Layered positional audio zones.

**Music**, on its own channel and switchable: an orchestral/classical option and a techno
option.

**Crowd sound** — subtle street ambience. People moving, background babble, footfall.
It should sit under the scene, not on top of it, and should follow how many people are
genuinely nearby.

---

## Interaction and storytelling

Doors, switches, elevators, vending, terminals, shutters, physics props, machinery.

Environmental narrative and collectibles, discovered by looking, **without waypoint
markers**.

### Mission

One simple objective chain. The player is an **enforcement officer**: reach an office and
watch people on a bank of CCTV monitors.

---

## Interface

- A **settings menu** — a proper panel, not controls stuck to the corner of the HUD.
  Everything adjustable lives there.
- A **HUD minimap, bottom-left**, cyberpunk and retro in style.
- A **pixelated mode** — a deliberate low-resolution look, not merely a smaller
  framebuffer.
- **Depth of field**, subtle, softening the far buildings and distant geometry.

---

## Performance

Performance is a **core design requirement**, not a cleanup pass: instancing, batching,
texture atlases, LOD, culling, pooled particles, selective dynamic lighting.

The target is a steady frame rate on ordinary hardware with the full district, weather,
signage and crowd live. Measure it; do not assume it.

---

## Process

Break the work into independent disciplines and use parallel specialised agents where
available. Every discipline gets an **independent critical review pass where the reviewer
actively searches for problems**. Repeat: implement → inspect → criticise → revise.
Regularly capture representative rendered views and judge the actual image.

---

## Reading order for the result

| Document | What it covers |
|---|---|
| [GUIDE.md](GUIDE.md) | How to run it, every control, and what is worth doing |
| [README.md](README.md) | Architecture, area status, measured performance, known gaps |
| [KIT.md](KIT.md) | The contract every content module is written against |
