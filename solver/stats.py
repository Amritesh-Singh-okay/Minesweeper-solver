import json
from pathlib import Path

STATS_FILE = Path(__file__).parent.parent / "stats.json"

def record_game(is_win: bool, solve_time: float):
    stats = {"games": 0, "wins": 0, "losses": 0, "total_time": 0.0, "best_time": None}
    if STATS_FILE.exists():
        try:
            with open(STATS_FILE) as f:
                stats.update(json.load(f))
        except Exception:
            pass

    stats["games"] += 1
    stats["wins" if is_win else "losses"] += 1
    stats["total_time"] = round(stats["total_time"] + solve_time, 2)
    if is_win and (stats["best_time"] is None or solve_time < stats["best_time"]):
        stats["best_time"] = round(solve_time, 2)

    with open(STATS_FILE, "w") as f:
        json.dump(stats, f, indent=2)

    win_rate = round(stats["wins"] / stats["games"] * 100, 1)
    avg_time = round(stats["total_time"] / stats["games"], 2)
    print(f"\nStats: {stats['wins']}W / {stats['losses']}L ({win_rate}% Win Rate) | Avg: {avg_time}s | Best: {stats['best_time']}s\n")
