"""
Number Guessing Game - main.py
------------------------------
Name:   <your name>
Class:  <your class / course>
Date:   <date>

The computer picks a secret number. You have a limited number of tries
to guess it. After each guess you get a hint: too high, too low, or close.
Your best score (fewest tries) for each level is saved in a file.

This file has the game rules, the score saving, and the terminal version.
The window (GUI) version is in gui.py and uses the code from this file.

How to run:
    python main.py          (asks you to choose terminal or window)
    python main.py cli      (terminal version)
    python main.py gui      (window version)
"""

import random
import sys

from score_manager import load_best_scores, save_best_scores, update_best_score

# ----- Settings -----
# Each level has a name, the biggest number, and how many tries you get
LEVELS = {
    "1": {"name": "Easy", "max": 10, "tries": 5},
    "2": {"name": "Medium", "max": 50, "tries": 7},
    "3": {"name": "Hard", "max": 100, "tries": 7},
}

CLOSE_RANGE = 2

# ----- Game rules (used by both the terminal and the window) -----
def parse_guess(text, max_number):
    """Checks what the player typed and returns (number, error).

    If the text is fine, error is None.
    If not, number is None and error says what went wrong.
    """
    try:
        guess = int(text.strip())
    except ValueError:
        return None, "That is not a number. Try again."

    if guess >= 1 and guess <= max_number:
        return guess, None
    return None, f"Please pick a number from 1 to {max_number}."


class Game:
    # One round of the game: keeps the secret number and the tries used so far

    def __init__(self, level):
        self.level = level
        self.secret = random.randint(1, level["max"])
        self.attempts = 0       # how many valid guesses were made
        self.finished = False   # True when the player wins or runs out of tries
        self.won = False

    def tries_left(self):
        return self.level["tries"] - self.attempts

    def is_close(self, guess):
        # True if the guess is wrong but within CLOSE_RANGE of the secret
        if guess != self.secret and abs(guess - self.secret) <= CLOSE_RANGE:
            return True
        return False

    def make_guess(self, guess):
        """Checks one guess and returns "correct", "high" or "low"."""
        self.attempts += 1

        if guess == self.secret:
            self.finished = True
            self.won = True
            return "correct"

        if self.tries_left() == 0:
            self.finished = True  # last try and it was wrong

        if guess > self.secret:
            return "high"
        else:
            return "low"


def tries_text(count):
    # gives "1 try" or "3 tries" so the sentence sounds right
    if count == 1:
        word = "try"
    else:
        word = "tries"
    return f"{count} {word}"


# ----- Terminal version -----
def choose_level():
    print("\nChoose a level:")
    for key, level in LEVELS.items():
        print(f"  {key}. {level['name']} (1 to {level['max']}, {level['tries']} tries)")

    while True:
        choice = input("Your choice (1/2/3): ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Please type 1, 2 or 3.")


def get_guess(max_number):
    # keeps asking until the player types a whole number in range
    while True:
        text = input("Your guess: ")
        guess, error = parse_guess(text, max_number)
        if error is None:
            return guess
        print(error)


def play_round(level):
    """Plays one round. Returns the tries used if the player won, otherwise None."""
    game = Game(level)

    while not game.finished:
        guess = get_guess(level["max"])
        result = game.make_guess(guess)

        if result == "correct":
            print(f"Correct! You got it in {tries_text(game.attempts)}.")
            return game.attempts

        if result == "high":
            print("Too high!")
        else:
            print("Too low!")

        if game.is_close(guess):
            print("...but you are very close!")

        if game.tries_left() > 0:
            print(f"{game.tries_left()} left.")

    print(f"Out of tries! The number was {game.secret}.")
    return None


def run_cli():
    print("=== Number Guessing Game ===")
    best_scores = load_best_scores()

    while True:
        level = choose_level()
        name = level["name"]
        print(f"\nI am thinking of a number from 1 to {level['max']}.")

        result = play_round(level)

        # result is None if the player lost, so only check the score after a win
        if result is not None:
            is_new_best = update_best_score(best_scores, name, result)
            if is_new_best:
                print("New best score for this level!")

        if name in best_scores:
            print(f"Best on {name}: {best_scores[name]} tries")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("Thanks for playing!")


# ----- Starting the program -----
def run_gui():
    try:
        import gui  # imported here so the terminal version still works without tkinter
    except ImportError:
        print("The window version needs tkinter, and it could not be loaded.")
        print("You can still play in the terminal:  python main.py cli")
        return
    gui.run()


def main():
    # use the word typed after "python main.py" if there is one
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
    else:
        mode = ""

    # otherwise ask the player
    if mode not in ("cli", "gui"):
        print("=== Number Guessing Game ===")
        print("  1. Play in the terminal")
        print("  2. Play in a window (GUI)")
        while True:
            choice = input("Your choice (1/2): ").strip()
            if choice in ("1", "2"):
                if choice == "1":
                    mode = "cli"
                else:
                    mode = "gui"
                break
            print("Please type 1 or 2.")

    if mode == "gui":
        run_gui()
    else:
        run_cli()


# only start the game when this file is run directly
if __name__ == "__main__":
    main()
