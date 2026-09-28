# Valve's Approach to Playtesting: The Application of Empiricism (GDC 2009)

- URL (slides PDF): https://cdn.akamai.steamstatic.com/apps/valve/2009/GDC2009_ValvesApproachToPlaytesting.pdf ; GDC Vault: https://www.gdcvault.com/play/1566/Valve-s-Approach-to-Playtesting
- Author/org: Mike Ambinder, PhD (Experimental Psychologist), Valve
- Date: GDC 2009
- Why it matters: the canonical industry statement that designs are hypotheses and playtests are experiments; the playtest goal is FUN (not bugs/balance); trust what players DO over what they SAY. Gives the frame for turning feedback into root-cause design changes rather than surface tweaks.

## Verbatim slide text
Valve's Game Design Process:
- "Goal is a fun game"
- "Game designs are hypotheses"
- "Playtests are experiments"
- "Evaluate designs off playtest results"
- "Repeat"

Playtesting Goal:
- "Fun" / "Not bug testing" / "Not game balancing" / "DEFINITELY not focus testing"

Valve's Philosophy:
- "We want to make informed decisions" / "Get data early, get data often" / "Iterate constantly"
- "We don't know what's best (players do)"
- "Create a feedback loop between design and playtest"

Direct Observation:
- "Watch people play the game" / "Observe their gameplay/behavior" / "Simulate at-home experience" / "Have a design goal"
- "+ Importance of what people do—not what they say"
- "– Presence of observers can bias results" / "– Salient event can slant interpretation" / "– Behavior requires interpretation"

Verbal reports (think-aloud): "People describe their actions as they play" / "Unprompted and uncorrected"; "+ Effective for 'why' questions"; "– Inaccurate and biased"

Q&A: "+ Answer specific design questions" / "+ Determine specific player intent" / "– Group biases (anchoring, social pressure, saliency, etc.)" / "– People don't know why they do what they do" / "– Potential for biased questions"

Benefits of traditional methods: "+ Nothing beats direct gameplay observation" / "+ Determine major gameplay, navigation, and content issues" / "+ Get an idea of player thoughts/mental models"

Stat collection: "Record of gameplay behaviors" / "Deaths, level times, friendly fire, …" (heatmap of death concentrations, TF2 Dustbowl); "– Averages hide extreme examples" / "– Can see 'illusory' patterns"

Design experiments: "Hypothesis testing" / "Compare two or more conditions" / "Collect data" / "Verify hypothesis"; "– Right questions aren't always clear"

Surveys (example, verbatim): "How challenging were the following enemies (1 = very easy; 7 = very hard)?" ... "Please rank order your preference for the following weapons from 1 (most liked) to 12 (least liked)"; "+ Forced choice helpful for revealing preference"; "– Difficulty in converting ratings to meaningful decisions"

Summary: "Do your QA early" / "Understand pros/cons of existing methods" / "Correctly frame design questions"

## Mapping to agent loops
- Each playtest round should state a hypothesis ("players will understand X / will want to do Y again") and a measurable observation, then a design change targeting the hypothesis -- not a list of cosmetic tweaks.
- Instrument the game: log deaths, time-to-first-success, quit points, retries -> agents can reason over telemetry rather than prose opinions.
