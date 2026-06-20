import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


# FIX: After I described the New Game (Bug 2) and Hard-range (Bug 3) glitches,
# the AI proposed centralizing a full game reset here so both call sites in
# app.py reuse it; I approved that approach.
def start_new_game(difficulty: str):
    """
    Return a fresh game-state dict for the given difficulty.

    Used for both first load and the New Game button so that:
      - the secret is always drawn from the active difficulty's range (Bug 3)
      - the whole round resets, not just the attempt counter (Bug 2)
    """
    low, high = get_range_for_difficulty(difficulty)
    return {
        "secret": random.randint(low, high),
        "attempts": 0,
        "score": 0,
        "status": "playing",
        "history": [],
    }


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: I found the hints were reversed; the AI confirmed the messages were
    # swapped (and a stringify hack in app.py made it worse) and we corrected both.
    if guess == secret:
        return "Win", "🎉 Correct!"

    if guess > secret:
        # Guess is too high, so the player should aim LOWER.
        return "Too High", "📉 Go LOWER!"
    # Guess is too low, so the player should aim HIGHER.
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
