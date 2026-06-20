# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Describe the game's purpose.**
  A Streamlit number-guessing game. The app picks a secret number within a range
  that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50). The
  player guesses, gets a "higher/lower" hint each turn, earns a score, and tries to
  find the secret before running out of attempts.

- [x] **Detail which bugs you found.**
  - **Bug 1 — Backwards hints.** Hints pointed the wrong way (e.g. secret 88, guess
    77 said "Go LOWER"). Two causes: the "Too High"/"Too Low" messages were swapped
    in `check_guess`, and `app.py` cast the secret to a string on every even attempt,
    forcing a lexicographic comparison ("25" < "7") instead of a numeric one.
  - **Bug 2 — New Game didn't restart.** Clicking "New Game" only reset the attempt
    counter; `status`, `score`, and `history` were left stale, so after a win/loss
    the game-over guard locked you out and the round was unplayable.
  - **Bug 3 — Secret ignored difficulty.** The secret was generated once and never
    regenerated when difficulty changed, and "New Game" hardcoded `randint(1, 100)`,
    so Hard mode could produce a secret above 50.

- [x] **Explain what fixes you applied.**
  - Refactored the pure logic (`get_range_for_difficulty`, `parse_guess`,
    `check_guess`, `update_score`) out of `app.py` into `logic_utils.py` so it can be
    unit-tested without Streamlit.
  - **Bug 1:** corrected the swapped hint messages and removed the even-attempt
    stringify hack so the comparison is always numeric.
  - **Bug 2 & 3:** added a single `start_new_game(difficulty)` helper that returns a
    fully fresh state (`secret`, `attempts`, `score`, `status`, `history`) drawn from
    the active difficulty's range. Both first-load and "New Game" call it, and the
    secret is also regenerated whenever the difficulty changes.

## 📸 Demo Walkthrough

A text record of a sample game on **Normal** difficulty (range 1–100, 8 attempts).
The secret is visible as **63** via the "Developer Debug Info" expander.

1. App loads on Normal. Debug Info shows `Secret: 63`, score `0`, "Attempts left: 8".
2. User enters a guess of **40** → hint shows "📈 Go HIGHER!" (outcome: Too Low). The
   direction is now correct — before the fix this said "Go LOWER". Score becomes `-5`.
3. User enters a guess of **70** → hint shows "📉 Go LOWER!" (outcome: Too High).
   Score becomes `0`.
4. User enters a guess of **63** → "🎉 Correct!", balloons appear, status flips to
   "won", and the final score is shown as `60`. Score updated after every guess.
5. User clicks **New Game** → the round fully resets: a new secret in 1–100, attempts
   back to 8, score back to 0, status back to "playing" — the game is immediately
   playable again instead of staying stuck on the win screen.
6. User switches difficulty to **Hard** → a new secret is generated and Debug Info now
   shows a value within **1–50**, confirming the range tracks the difficulty.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ pytest tests/
============================= test session starts ==============================
platform darwin -- Python 3.13.13, pytest-9.0.3, pluggy-1.6.0
rootdir: .../ai110-module1show-gameglitchinvestigator-starter
plugins: anyio-4.13.0
collected 16 items

tests/test_game_logic.py ................                                [100%]

============================== 16 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
