import pyautogui
import cv2 as cv
import numpy as np

from solver.constants import (
    BOARD_COLS, BOARD_ROWS, BOARD_REGION_LEFT, BOARD_REGION_TOP,
    BOARD_REGION_WIDTH, BOARD_REGION_HEIGHT, CELL_W, CELL_H,
    GAME_IMG_PATH, lower, upper, lower_flag, upper_flag, colors
)

# checks a small patch around (cx,cy) for a color returns true if any pixel matches
def check_patch(img, cx, cy, low, high, size=21):
    half = size // 2
    h, w = img.shape[:2]

    # skip if patch goes out of img
    if (cx - half < 0) or (cy - half < 0) or (cx + half >= w) or (cy + half >= h):
        return False

    patch = img[cy-half:cy+half+1, cx-half:cx+half+1]

    mask = cv.inRange(patch, np.array(low), np.array(high))

    return np.any(mask == 255)   # ANY pixel match

# Takes a screenshot of the board region and returns it as a BGR OpenCV image.
def capture_board() -> np.ndarray:
    pyautogui.screenshot(
        str(GAME_IMG_PATH),
        region=[BOARD_REGION_LEFT, BOARD_REGION_TOP, BOARD_REGION_WIDTH, BOARD_REGION_HEIGHT]
    )
    return cv.imread(str(GAME_IMG_PATH))

def parse_board(img: np.ndarray) -> list[list[int]]:
    # build arr
    # -2 => flag,  -1 => unrevealed,  0 => empty,  1-6 => number
    # check flag first then unrevealed then numbers then what left is empty
    # why this order because flag also has green of unrevealed
    arr = []
    for y in range(BOARD_ROWS):
        row = []
        for x in range(BOARD_COLS):
            x1, y1 = int(x * CELL_W), int(y * CELL_H)
            x2, y2 = int((x + 1) * CELL_W), int((y + 1) * CELL_H)

            cx = int(x * CELL_W + CELL_W / 2)
            cy = int(y * CELL_H + CELL_H / 2)

            if check_patch(img, cx, cy, lower_flag, upper_flag):
                row.append(-2)
                cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            elif check_patch(img, cx, cy, lower, upper):
                row.append(-1)
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            else:
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
                for low, high, draw_color, cell_value in colors:
                    if check_patch(img, cx, cy, low, high):
                        row.append(cell_value)
                        cv.circle(img, (cx, cy), 8, draw_color, -1)
                        break
                else:
                    row.append(0)
        arr.append(row)
    return arr
