# Design/production practice: prototype vs vertical slice, walking skeleton, interesting decisions

Lower-authority / secondary than the other files; kept because they define the vocabulary for "core loop first".

## Rami Ismail -- Prototypes & Vertical Slice (Levelling The Playing Field)
- URL: https://ltpf.ramiismail.com/prototypes-and-vertical-slice/ ; Rami Ismail (Vlambeer co-founder), 2022-09-26
- Prototypes exist "to answer the question marks in your idea. They're usually small, scrappy, and messy"
- Vertical slice is "a _production_ prototype" that proves "you _can_ create that game"; it builds "some _one of each thing_...at a fidelity that approaches or convincingly simulates the shipping quality"
- Prototypes answer whether you SHOULD make the game; vertical slices prove you CAN.

## Alistair Cockburn -- Walking Skeleton (via secondary sources; definition widely quoted)
- Definition: "a tiny implementation of the system that performs a small end-to-end function. It need not use the final architecture, but it should link together the main architectural components."
- Game translation (inference): title -> start -> one input changes state -> feedback -> win/lose -> restart, all wired, before any breadth.

## Sid Meier -- "Interesting Decisions" (GDC 2012)
- GDC Vault: https://gdcvault.com/play/1015756/Interesting ; report: https://www.escapistmagazine.com/gdc-2012-sid-meier-sees-interesting-decisions-even-in-rhythm-games/ (2012-03-07); Game Developer report https://www.gamedeveloper.com/design/gdc-2012-sid-meier-on-how-to-see-games-as-sets-of-interesting-decisions (403 to fetcher; quotes via search snippet)
- "A game is a series of interesting decisions."
- "It's easier to look at it as what is not an interesting decision" -- if a player always chooses the first of three options it is not interesting; nor is a random selection.
- Decision types: customization, trade-offs, long-term vs short-term benefit.
- "something that's interesting you do once doesn't mean it's something interesting to do ten times."
- "It's the combination of this wonderful fantasy world that you create and the interesting decisions that the player gets to make in that world that really is the sum total of the quality of your game"

## Mapping (inference)
Content/creativity games (narrative, generative content) fail "fun" when content is an arc with no decision loop: add a check "list the decisions the player makes in minute 1-5; for each, is there a dominant choice? does the choice change later state?" This is a testable proxy for Meier's criterion.
