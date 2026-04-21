import json
import os

FILE_PATH = "leaderboard.json"


def get_leaderboard():
    if not os.path.exists(FILE_PATH):
        return []
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except:
        return []


def add_score(nickname, score):
    scores = get_leaderboard()

    player_found = False

    for entry in scores:
        if entry["name"] == nickname:
            player_found = True

            if score > entry["score"]:
                entry["score"] = score
            break

    if not player_found:
        scores.append({"name": nickname, "score": score})

    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    with open(FILE_PATH, "w") as f:
        json.dump(scores, f)