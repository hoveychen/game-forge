# r/aigamedev practitioner process threads — "What is your process?" and "One shot prompt VS game design phase document"

- https://www.reddit.com/r/aigamedev/comments/1w6j3hg/ (27 upvotes, 26 comments, 2026-09)
- https://www.reddit.com/r/aigamedev/comments/1wcv7ix/ (0 upvotes, 12 comments, 2026-09)
- Evidence strength: WEAK-MODERATE (self-reported workflows, few outcome links), but convergent.

## OP of 1w6j3hg (24-year game dev, business sim, Unity+MCP) — verbatim process
1. setup claude + mcp + unity, environment and repo
2. create a game design document (GDD), then feed that into the LLM side of the AI. Have it poke holes in the design, work with it to flush out any shortcomings.
3. Build a production map timeline, organize the game by groups of tasks (mini-milestones)
4. Have the LLM side write the prompt to send over to the code side (also claude, claude code in my case), to execute on that group of tasks and write a report when it's done. Note: Each mini-milestone(group of tasks) gets it's own session, to keep context length short and on point for that specific milestone.
5. When it finishes, take the report back to the LLM side for review where we discuss what code did, what it didn't do, where it fits on the big picture, any thing i may need to be aware of before playtesting.
6. Playtest the game. Take my own notes and suggestions.
7. Feed my playstest notes back into the LLM, Corraberate with it, and then it prompts the next task it had planned, but also figures out where to add in my suggestions and bug reports from the playest i just did.
8. Repeat this process from step 4.

## Notable replies (verbatim)
- cckynv: "Game Design Document -> turned into playbook for each development phase ... CLAUDE.md - contains hard rules, documentation requirement (CHANGELOG.md) ... PLAYBOOK-STEP-#.md - detailed playbook that the AI follows. Contains requirements, pass/fail criteria, smoke testing steps ... Playtest once it finishes a batch of changes."
- RUSuper: "Make core loop of the game (Which probably changes anyway) ... Make in game editors for editing things like HUD and position of objects by myself instead of endlessly asking Claude to do it for me ... Think about 'Ok this might be too many ideas abort the mission'"
- butchiebags: "Bugs.md which is appended from my own chat commands in the game, so as I playtest I can just /bug and it drops the message with location data etc."
- heavy-minium ("working backward"): "I basically produced a full game wiki that is exhaustive, linked, and with AI generated images. As well as fictional player testimonials about the game - all as if it would already exists. The instructions are to continuously work on the next full vertical - which basically means to fully implement what is described on a page on a defined set of dimensions (controls/rendering/audio/serialization/etc)."
- ZymzAlchemy: "creating a test for each phase and executing the entire batch each time to ensure nothing has been bent in a way that breaks something that has been previously working/corrected. Every phase gets a git commit so rollback is simple."

## 1wcv7ix replies (verbatim)
- OP: "game design document with phases that doesn't allow me to continue adding new features until i test and approve everything is working ... I'm currently stuck with a simple square shapes etc but every core loop works to the letter! Mining, crafting etc"
- Snoo-29395: "Nothing good can come up with one shootting a game. ... create a good GDD. Stick to it ... Define a MVP for a vertical slice you can actually ship as a demo. Split the work into milestones ... subtickets, the smaller the better"
- Square-Yam-3772: "The issue with one prompting is that Ai will now have a working game in-context. You will end up wasting time steering ai away from it"
- Fairway3Games: "even the BEST one-shot game is unlikely to be a reasonable game. ... it's often an amalgamation of very 'thin' features. It seems 'cohesive' only in the sense that the AI made a bunch of decisions and was able to string them together. But once you start trying to convert it to something it wasn't built for, you end up unwinding the string that tied it together."
- ScutFarkush (9 months in): "I have different sessions for graphics, gameplay, ui, progression, sounds, music, code reviews, play testing bots"

Related r/aigamedev 1um2c84 (first-time "Fable" user with full GDD -> vertical slice of level 1): MidSerpent: "Fable really favors big front loaded plans, so starting with a GDD like that is a big part of why you got such a good result."
