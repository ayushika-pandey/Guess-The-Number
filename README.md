# Number Guessing Game

This is a simple number guessing game I made in Python. The computer picks a secret number and you have to guess it before you run out of tries. After each guess the game gives you a hint: too high, too low, or very close. There are two versions that use the same rules: a **terminal version** and a **window (GUI) version**.

- **Author:** `<your name>`
- **Course:** `<your class / course>` (Python Essentials)
- **Date:** `<date>`

## Features

- Three levels: Easy (1 to 10, 5 tries), Medium (1 to 50, 7 tries) and Hard (1 to 100, 7 tries)
- Hints after each guess: "Too high!", "Too low!", and "very close" if you are within 2 of the number
- Input checking: letters or numbers outside the range are rejected and do not use up a try
- The best score (fewest tries) for each level is saved, so it is still there next time you play
- Terminal version and tkinter window version, both using the same rules and the same score file

## Requirements

- Python 3.8 or newer
- `tkinter` for the window version. Everything is from the standard library, so there is nothing to install with pip.
  - Windows and macOS: tkinter comes with the normal Python installer.
  - Linux (Debian/Ubuntu): if it is missing, run `sudo apt install python3-tk`.

The terminal version still works if tkinter is not installed.

## Setup

1. Install Python from https://www.python.org/downloads/ if you do not have it.
2. Download or clone this repository:

   ```
   git clone <repository-url>
   cd <repository-folder>
   ```

3. Check that Python works:

   ```
   python --version
   ```

   On some computers the command is `python3` instead of `python`. Use whichever one works for you.

## How to run

Open a terminal in the project folder and use one of these commands:

| Command | What it does |
| --- | --- |
| `python main.py` | Asks if you want the terminal or the window version |
| `python main.py cli` | Starts the terminal version |
| `python main.py gui` | Starts the window version |
| `python gui.py` | Starts the window version |

## How to play

**Terminal version**

1. Type `1`, `2` or `3` to choose a level.
2. Type a whole number and press Enter.
3. Read the hint and guess again until you find the number or run out of tries.
4. Type `y` to play again or `n` to quit.

**Window version**

1. Choose a level with the radio buttons and press **Start New Game**.
2. Type a number in the box and press **Guess** (or press the Enter key).
3. The hint shows up under the box and each guess is added to the list.
4. Press **Start New Game** to play again, or **Quit** to close the window.

## Project files

| File | What it is for |
| --- | --- |
| `main.py` | The game rules (`Game` class and guess checking), saving and loading best scores, the terminal version, and where the program starts |
| `gui.py` | The tkinter window version. It uses the rules and score saving from `main.py` |
| `README.md` | This file |
| `best_scores.txt` | Made automatically after your first win. It has one line per level, like `Easy=3` |

If `best_scores.txt` is deleted or damaged, the game just starts with no saved scores.

## Python concepts used

- Variables, data types and operators
- Conditions (`if`, `else`) and loops (`while`, `for`)
- Dictionaries (for the levels and the best scores)
- Functions with parameters and return values
- Modules (`random`, `os`, `sys`, `tkinter`) and splitting the program into more than one file
- Exception handling (`try` / `except`) for bad input and file problems
- Reading and writing a file for the best scores
- A class (`Game`) to keep the data for one round together, and a class for the window

## Example (terminal version)

```
=== Number Guessing Game ===

Choose a level:
  1. Easy (1 to 10, 5 tries)
  2. Medium (1 to 50, 7 tries)
  3. Hard (1 to 100, 7 tries)
Your choice (1/2/3): 1

I am thinking of a number from 1 to 10.
Your guess: 5
Too high!
...but you are very close!
4 left.
Your guess: 3
Correct! You got it in 2 tries.
New best score for this level!
Best on Easy: 2 tries
```
