import json
from enum import Enum
from pathlib import Path

# File paths
BASE_DIR = Path(__file__).parent.parent
GAME_IMG_PATH = BASE_DIR / "game.png"
CALIBRATION_PATH = BASE_DIR / "calibration.json"

def load_calibration():
    #loads board region coordinates from calibration.json offers recalibration too.
    if not CALIBRATION_PATH.exists():
        try:
            from calibrate import calibrate
            calibrate()
        except Exception as e:
            print(f"Calibration warning: {e}")
    else:
        try:
            with open(CALIBRATION_PATH, "r") as f:
                cal = json.load(f)
            left, top, width, height = cal.get("left", 578), cal.get("top", 287), cal.get("width", 749), cal.get("height", 625)
            print(f"\nFound saved calibration: Left={left}, Top={top}, Width={width}, Height={height}")
            ans = input("   Press ENTER to use saved position, or type 'c' to recalibrate: ").strip().lower()
            if ans == 'c':
                from calibrate import calibrate
                calibrate()
        except Exception as e:
            print(f"Calibration notice: {e}")

    if CALIBRATION_PATH.exists():
        try:
            with open(CALIBRATION_PATH, "r") as f:
                cal = json.load(f)
                return (
                    cal["left"],
                    cal["top"],
                    cal["width"],
                    cal["height"]
                )
        except Exception:
            pass
    return 578, 287, 749, 625

class SolverState(Enum):
    FOUND_MOVES = 0    # moves found to click or flag
    STUCK = -1         # no moves found, fallback to probability guess
    DONE = 1           # game completed or no moves remaining, exit loop

# Board configuration constants
BOARD_COLS = 24
BOARD_ROWS = 20
TOTAL_MINES = 99

BOARD_REGION_LEFT, BOARD_REGION_TOP, BOARD_REGION_WIDTH, BOARD_REGION_HEIGHT = load_calibration()

CELL_W = BOARD_REGION_WIDTH / BOARD_COLS
CELL_H = BOARD_REGION_HEIGHT / BOARD_ROWS

# bgr range for unrevealed cell (green background)
lower = [72, 208, 161]
upper = [82, 216, 171]

# bgr ranges for each number color on revealed cells
# need to add 7
 
lower_1 = (198,106,13)
upper_1 = (222,130,37)

lower_2 = (48,130,44)
upper_2 = (72,154,68)

lower_3 = (35,35,199)
upper_3 = (59,59,223)

lower_4 = (150,19,111)
upper_4 = (174,43,135)

lower_5 = (0,131,243)
upper_5 = (12,155,255)

lower_6 = (157,141,0)
upper_6 = (177,161,10)

# flag 
lower_flag = (0,38,222)
upper_flag = (27,74,255)

# (low, high, draw_color, cell_value) for each no.
colors = [
    (lower_1, upper_1, (210,118,25),1),
    (lower_2, upper_2, (60,142,56),2),
    (lower_3, upper_3, (47,47,211),3),
    (lower_4, upper_4, (162,31,123),4),
    (lower_5, upper_5, (0,143,255),5),
    (lower_6, upper_6, (167,151,0), 6)
]
