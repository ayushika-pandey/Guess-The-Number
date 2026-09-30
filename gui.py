"""
Number Guessing Game - gui.py
-----------------------------
Name:   <your name>
Class:  <your class / course>
Date:   <date>

The window (GUI) version of the game, made with tkinter.
The game rules and the best-score saving come from main.py, so the
terminal version and this window version work the same way.

How to run:
    python gui.py
    (or)  python main.py gui
"""

import tkinter as tk
from tkinter import ttk

from main import (
    LEVELS,
    Game,
    parse_guess,
    tries_text,
)

from score_manager import load_best_scores, update_best_score

# Colours for the message under the guess box
GREEN = "#1a7f37"   # won
RED = "#c62828"     # wrong guess or bad input
ORANGE = "#b26a00"  # wrong guess but very close
BLACK = "#000000"   # normal text


class GuessingGameApp:
    # The game window: level choice, guess box, messages and best scores

    def __init__(self, root):
        self.root = root
        self.root.title("Number Guessing Game")
        self.root.resizable(False, False)

        self.best_scores = load_best_scores()
        self.game = None                             # no round until Start is pressed
        self.level_choice = tk.StringVar(value="1")  # remembers which level is selected

        self.build_widgets()
        self.update_best_label()
        self.set_playing(False)

    # ----- Building the window -----
    def build_widgets(self):
        frame = ttk.Frame(self.root, padding=15)
        frame.grid()

        title = ttk.Label(frame, text="Number Guessing Game", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, pady=(0, 10))

        # One radio button for each level in LEVELS
        level_box = ttk.LabelFrame(frame, text="Choose a level", padding=8)
        level_box.grid(row=1, column=0, sticky="ew")
        for key, level in LEVELS.items():
            text = f"{level['name']} (1 to {level['max']}, {level['tries']} tries)"
            button = ttk.Radiobutton(level_box, text=text, variable=self.level_choice, value=key)
            button.pack(anchor="w")

        start_button = ttk.Button(frame, text="Start New Game", command=self.start_game)
        start_button.grid(row=2, column=0, pady=10)

        # Shows the number range and how many tries are left
        self.info_label = ttk.Label(frame, text="Pick a level and press Start New Game.")
        self.info_label.grid(row=3, column=0)

        # The guess box and the Guess button, side by side
        guess_row = ttk.Frame(frame)
        guess_row.grid(row=4, column=0, pady=10)

        guess_label = ttk.Label(guess_row, text="Your guess:")
        guess_label.pack(side="left", padx=(0, 5))

        self.guess_entry = ttk.Entry(guess_row, width=8)
        self.guess_entry.pack(side="left", padx=(0, 5))
        self.guess_entry.bind("<Return>", self.make_guess)  # pressing Enter also guesses

        self.guess_button = ttk.Button(guess_row, text="Guess", command=self.make_guess)
        self.guess_button.pack(side="left")

        # The hint after each guess (too high, too low, correct...)
        self.message_label = ttk.Label(frame, text="", font=("Arial", 12, "bold"),
                                       wraplength=340, justify="center")
        self.message_label.grid(row=5, column=0, pady=(0, 10))

        # A list of the guesses made in this round
        self.history = tk.Listbox(frame, height=7, width=40)
        self.history.grid(row=6, column=0)

        self.best_label = ttk.Label(frame, text="", wraplength=340, justify="center")
        self.best_label.grid(row=7, column=0, pady=10)

        quit_button = ttk.Button(frame, text="Quit", command=self.root.destroy)
        quit_button.grid(row=8, column=0)

    # ----- Small helper methods -----
    def set_playing(self, playing):
        # turns the guess box and button on during a round and off otherwise
        if playing:
            state = "normal"
        else:
            state = "disabled"
        self.guess_entry.config(state=state)
        self.guess_button.config(state=state)

    def show_message(self, text, colour):
        self.message_label.config(text=text, foreground=colour)

    def update_info(self):
        level = self.game.level
        text = f"Guess a number from 1 to {level['max']}.  "
        text += f"Tries left: {self.game.tries_left()}"
        self.info_label.config(text=text)

    def update_best_label(self):
        # shows the best score of every level, or a dash if there is none yet
        parts = []
        for level in LEVELS.values():
            value = self.best_scores.get(level["name"])
            if value is None:
                value = "-"
            parts.append(f"{level['name']}: {value}")
        self.best_label.config(text="Best scores (fewest tries)   " + "   ".join(parts))

    # ----- Playing -----
    def start_game(self):
        self.game = Game(LEVELS[self.level_choice.get()])
        self.history.delete(0, tk.END)
        self.set_playing(True)
        self.update_info()
        self.show_message("Good luck!", BLACK)
        self.guess_entry.focus()

    def make_guess(self, event=None):
        # event=None is only there because pressing Enter sends an event to this method
        if self.game is None or self.game.finished:
            return

        text = self.guess_entry.get()
        guess, error = parse_guess(text, self.game.level["max"])
        self.guess_entry.delete(0, tk.END)

        if error is not None:
            # a bad guess does not use up a try
            self.show_message(error, RED)
            return

        result = self.game.make_guess(guess)

        if result == "correct":
            self.history.insert(tk.END, f"Guess {self.game.attempts}: {guess} - Correct!")
            self.handle_win()
            return

        if result == "high":
            hint = "Too high!"
        else:
            hint = "Too low!"
        self.history.insert(tk.END, f"Guess {self.game.attempts}: {guess} - {hint}")

        colour = RED
        if self.game.is_close(guess):
            hint += " ...but you are very close!"
            colour = ORANGE

        if self.game.finished:
            hint += f"\nOut of tries! The number was {self.game.secret}."
            self.set_playing(False)
            self.info_label.config(text="Game over. Press Start New Game to try again.")
        else:
            self.update_info()

        self.show_message(hint, colour)

    def handle_win(self):
        text = f"Correct! You got it in {tries_text(self.game.attempts)}."

        name = self.game.level["name"]
        if update_best_score(self.best_scores, name, self.game.attempts):
            text += "\nNew best score for this level!"
            self.update_best_label()

        self.set_playing(False)
        self.info_label.config(text="You won! Press Start New Game to play again.")
        self.show_message(text, GREEN)


def run():
    root = tk.Tk()
    GuessingGameApp(root)
    root.mainloop()


# only open the window when this file is run directly
if __name__ == "__main__":
    run()
