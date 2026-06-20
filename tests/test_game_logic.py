import pytest

from logic_utils import check_guess, get_range_for_difficulty, start_new_game

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    # Guess above the secret: outcome is "Too High" and hint says go LOWER (Bug 1)
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message

def test_guess_too_low():
    # Guess below the secret: outcome is "Too Low" and hint says go HIGHER (Bug 1)
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message

def test_too_low_hint_points_higher_77_vs_88():
    # Regression for the reported case: secret 88, guess 77 must say go HIGHER.
    outcome, message = check_guess(77, 88)
    assert outcome == "Too Low"
    assert "HIGHER" in message


# =========================================================================== #
# Regression tests for the two bugs fixed in start_new_game.
#
#   Bug 2 - New Game only reset the attempt counter, leaving status/score/
#           history stale, so a finished round could not be replayed.
#   Bug 3 - The secret ignored difficulty: generated once (never refreshed on
#           difficulty change) and New Game hardcoded random.randint(1, 100),
#           so Hard could hold a secret above 50.
# =========================================================================== #

DIFFICULTIES = ["Easy", "Normal", "Hard"]


# --- Bug 2: a new game must FULLY reset the round, not just attempts -------- #
@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_new_game_resets_all_round_state(difficulty):
    state = start_new_game(difficulty)
    assert state["attempts"] == 0
    assert state["score"] == 0
    assert state["status"] == "playing"
    assert state["history"] == []


@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_new_game_clears_finished_status(difficulty):
    # Simulate a finished round, then "press New Game".
    finished = {
        "secret": 42,
        "attempts": 8,
        "score": 250,
        "status": "lost",
        "history": [10, 20, 30],
    }
    finished.update(start_new_game(difficulty))
    # The status guard in app.py blocks play unless status == "playing".
    assert finished["status"] == "playing"
    assert finished["score"] == 0
    assert finished["history"] == []


def test_new_game_returns_independent_history_list():
    a = start_new_game("Normal")
    b = start_new_game("Normal")
    a["history"].append(99)
    assert b["history"] == []


# --- Bug 3: secret must fall within the active difficulty's range ---------- #
@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_secret_within_difficulty_range(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    for _ in range(1000):  # sample many times since the secret is random
        secret = start_new_game(difficulty)["secret"]
        assert low <= secret <= high, (
            f"{difficulty}: secret {secret} outside range {low}-{high}"
        )


def test_hard_secret_never_exceeds_50():
    # The headline symptom of Bug 3: Hard secrets leaking above 50.
    for _ in range(1000):
        assert start_new_game("Hard")["secret"] <= 50


def test_hard_uses_smaller_range_than_normal():
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high < normal_high
