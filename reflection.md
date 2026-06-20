# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The first time I ran the game, it loaded successfully, but I quickly noticed that some parts of the game were not working correctly.
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  One bug was that the hints were incorrect. No matter what number I guessed, the game would often tell me to go higher or lower incorrectly, except in cases like 1 and 100. Another bug was that sometimes the New Game button did not actually start a new game. It only reset the attempt counter, and I had to stop and rerun the program from the terminal to get a new random number.


**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input        | Expected Behavior         | Actual Behavior          | Console Output / Error |
|-------       |-------------------        |-----------------         |------------------------|
Guessed 25 when 
secret number    Hint should say "Go lower".  Hint said "Go higher"       No error
is lower

Guessed 11 when 
secret number    Hint should say "Go higher".  Hint said "Go lower"       No error
is higher

In hard level 
numbers range    Secret number shouldd be under 50.  Secret no. can go above 50.  NO error
from 1 to 50      
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?

I used Claude (Claude Code, agent mode) inside VS Code. I used it to investigate the
glitches, refactor the game logic out of app.py into logic_utils.py, fix the three bugs,
and generate the pytest suite.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

For Bug 3 (Hard mode showing a secret above 50), the AI identified the root cause: the
secret was generated only once and never refreshed when the difficulty changed, and the
New Game button hardcoded random.randint(1, 100). It centralized a full reset in a new
start_new_game(difficulty) function. I verified it with a test that samples 1000 Hard
games and asserts every secret is <= 50 (test_hard_secret_never_exceeds_50) — all passed,
and the game behaved correctly when I played it.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

The AI first created the test file at test/ (singular), but the repo already had a tests/
folder. Running pytest failed with an import-file-mismatch collision instead of running.
I caught it by actually running pytest; the AI then removed the stray test/ directory and
merged the tests into the existing tests/test_game_logic.py, after which all tests passed.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used two checks for each bug: a focused pytest test and playing the game manually.
A bug was only "fixed" once both agreed. For Bug 1 I replayed my original case (secret
88, guess 77) and confirmed the hint now says "Go HIGHER". For Bug 2 I finished a round,
pressed New Game, and confirmed I could actually play again instead of being stuck on the
game-over screen. For Bug 3 I switched to Hard and started new games repeatedly and never
saw a secret above 50.

- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.

test_hard_secret_never_exceeds_50 starts 1000 Hard games and asserts every secret is <= 50.
Running a single game can pass by luck, so sampling many games gave me confidence the range
fix was real and not a coincidence. I also have test_too_low_hint_points_higher_77_vs_88,
which pins my exact reported scenario so the backwards-hint bug can't silently come back.
Running `pytest` showed all 16 tests passing.

- Did AI help you design or understand any tests? How?

Yes. The AI wrote the pytest suite and explained the reasoning behind each test — for
example, why the range tests loop 1000 times (because the secret is random, one sample
isn't enough) and why it tests start_new_game directly (the logic was refactored out of
the UI so it can be tested without running Streamlit). It also explained that the 3
original starter tests were failing because they expected check_guess to return a string
when it actually returns an (outcome, message) tuple, which helped me update them correctly.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
