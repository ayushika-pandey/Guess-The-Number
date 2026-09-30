import os

SCORE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "best_scores.txt"
)


def load_best_scores():
    scores = {}

    if os.path.exists(SCORE_FILE):
        try:
            with open(SCORE_FILE, "r") as file:
                for line in file:
                    name, value = line.strip().split("=")
                    scores[name] = int(value)
        except (OSError, ValueError):
            scores = {}

    return scores


def save_best_scores(scores):
    try:
        with open(SCORE_FILE, "w") as file:
            for name, value in scores.items():
                file.write(f"{name}={value}\n")
    except OSError:
        print("(Could not save your best score.)")


def update_best_score(scores, level_name, tries):
    if level_name not in scores or tries < scores[level_name]:
        scores[level_name] = tries
        save_best_scores(scores)
        return True

    return False