"""
Number Guessing Game
--------------------
Name:   <your name>
Class:  <your class / course>
Date:   <date>

The computer picks a secret number. You have a limited number of tries
to guess it. After each guess you get a hint: too high, too low, or close.
Your best score (fewest tries) for each level is saved in a file.

How to run:
    python guessing_game.py
"""

import os
import random

# ---------- Settings ----------
# Each level has a name, the biggest possible number, and how many tries you get.
LEVELS = {
    "1": {"name": "Easy", "max": 10, "tries": 5},
    "2": {"name": "Medium", "max": 50, "tries": 7},
    "3": {"name": "Hard", "max": 100, "tries": 7},
}
SCORE_FILE = "best_scores.txt"


# ---------- Saving and loading best scores ----------
def load_best_scores():
    """Read best scores from the file. Returns a dictionary like {"Easy": 3}."""
    scores = {}
    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                for line in file:
                    name, value = line.strip().split("=")
                    scores[name] = int(value)
        except (OSError, ValueError):
            scores = {}  # if the file is damaged, start fresh
    return scores


def save_best_scores(scores):
    """Write the best scores to the file, one per line, like Easy=3."""
    try:
        with open(SCORE_FILE, "w") as file:
            for name, value in scores.items():
                file.write(f"{name}={value}\n")
    except OSError:
        print("(Could not save your best score.)")


# ---------- Getting input from the player ----------
def choose_level():
    """Show the levels and keep asking until the player picks a valid one."""
    print("\nChoose a level:")
    for key, level in LEVELS.items():
        print(f"  {key}. {level['name']} (1 to {level['max']}, {level['tries']} tries)")
    while True:
        choice = input("Your choice (1/2/3): ").strip()
        if choice in LEVELS:
            return LEVELS[choice]
        print("Please type 1, 2 or 3.")


def get_guess(max_number):
    """Ask for a guess. Keeps asking until it is a whole number in range."""
    while True:
        text = input("Your guess: ").strip()
        try:
            guess = int(text)
        except ValueError:
            print("That is not a number. Try again.")
            continue
        if 1 <= guess <= max_number:
            return guess
        print(f"Please pick a number from 1 to {max_number}.")


# ---------- One round of the game ----------
def play_round(level):
    """Play one round. Returns the tries used if won, or None if lost."""
    secret = random.randint(1, level["max"])

    for attempt in range(1, level["tries"] + 1):
        guess = get_guess(level["max"])

        if guess == secret:
            word = "try" if attempt == 1 else "tries"
            print(f"Correct! You got it in {attempt} {word}.")
            return attempt

        if guess > secret:
            print("Too high!")
        else:
            print("Too low!")

        if abs(guess - secret) <= 2:
            print("...but you are very close!")

        tries_left = level["tries"] - attempt
        if tries_left > 0:
            print(f"{tries_left} left.")

    print(f"Out of tries! The number was {secret}.")
    return None


# ---------- Main program ----------
def main():
    print("=== Number Guessing Game ===")
    best_scores = load_best_scores()

    while True:
        level = choose_level()
        name = level["name"]
        print(f"\nI am thinking of a number from 1 to {level['max']}.")

        result = play_round(level)

        # A lower number of tries is better, so save it if it beats the old best.
        if result is not None and (name not in best_scores or result < best_scores[name]):
            best_scores[name] = result
            save_best_scores(best_scores)
            print("New best score for this level!")

        if name in best_scores:
            print(f"Best on {name}: {best_scores[name]} tries")

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

    print("Thanks for playing!")


# This makes the game start only when you run this file directly.
if __name__ == "__main__":
    main()
