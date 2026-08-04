import random
import pyautogui
from solver.constants import (
    BOARD_COLS, BOARD_ROWS, BOARD_REGION_LEFT, BOARD_REGION_TOP, CELL_W, CELL_H
)

# Applies basic constraint logic (flagging obvious mines & revealing obvious safe cells)
def solve_basic(arr: list[list[int]]) -> tuple[set, set, list, dict]:
    mine_points = set()
    click_points = set()
    constraints_list = []
    prob_map = dict()

    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):
            if arr[y][x] > 0:
                cells = set()
                unrevealed_count = 0
                mine_count = 0

                for dy in range(-1, 2):
                    for dx in range(-1, 2):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:
                            if arr[ny][nx] == -1:
                                unrevealed_count += 1
                                cells.add((ny, nx))
                                prob_map.setdefault((ny, nx), [])
                            if arr[ny][nx] == -2:
                                mine_count += 1

                mine = arr[y][x] - mine_count

                if cells:
                    constraints_list.append((cells, mine))

                for key in cells:
                    prob = mine / len(cells)
                    prob_map.setdefault(key, []).append(prob)

                if mine_count + unrevealed_count == arr[y][x]:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:
                                if arr[ny][nx] == -1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    screen_x = cx + BOARD_REGION_LEFT
                                    screen_y = cy + BOARD_REGION_TOP
                                    mine_points.add((screen_x, screen_y))
                                    arr[ny][nx] = -2

                if mine_count == arr[y][x]:
                    for dy in range(-1, 2):
                        for dx in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:
                                if arr[ny][nx] == -1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    screen_x = cx + BOARD_REGION_LEFT
                                    screen_y = cy + BOARD_REGION_TOP
                                    click_points.add((screen_x, screen_y))

    return mine_points, click_points, constraints_list, prob_map

# subset solver
def solve_subset(constraints_list: list, arr: list[list[int]]) -> tuple[set, set]:
    # subset solver
    mine_points = set()
    click_points = set()

    for A in constraints_list:
        for B in constraints_list:
            if A != B:
                if A[0].issubset(B[0]):
                    New_cell = B[0] - A[0]
                    New_count = B[1] - A[1]

                    # 0 mines in New_cell — all safe
                    if New_count == 0:
                        for ny, nx in New_cell:
                            cx = int(nx * CELL_W + CELL_W / 2)
                            cy = int(ny * CELL_H + CELL_H / 2)
                            screen_x = cx + BOARD_REGION_LEFT
                            screen_y = cy + BOARD_REGION_TOP
                            click_points.add((screen_x, screen_y))

                    # mines == cells — all mines
                    if New_count == len(New_cell):
                        for ny, nx in New_cell:
                            cx = int(nx * CELL_W + CELL_W / 2)
                            cy = int(ny * CELL_H + CELL_H / 2)
                            screen_x = cx + BOARD_REGION_LEFT
                            screen_y = cy + BOARD_REGION_TOP
                            arr[ny][nx] = -2
                            mine_points.add((screen_x, screen_y))

    return mine_points, click_points

def guess_probabilistic(prob_map: dict, arr: list[list[int]] = None) -> set:
    # probability based solve
    print("probability ran")

    best_cell = None
    lowest = 9999

    for cell, probs in prob_map.items():
        prob = sum(probs) / len(probs)

        if prob <= lowest:
            lowest = prob
            best_cell = cell

    click_points = set()
    if best_cell is not None:
        print(best_cell, lowest)

        cx = int(best_cell[1] * CELL_W + CELL_W / 2)
        cy = int(best_cell[0] * CELL_H + CELL_H / 2)
        screen_x = cx + BOARD_REGION_LEFT
        screen_y = cy + BOARD_REGION_TOP

        click_points.add((screen_x, screen_y))
    elif arr is not None:
        # Fallback: pick a random unrevealed cell (-1) if no cell probabilities exist
        unrevealed = [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if arr[r][c] == -1]
        if unrevealed:
            r, c = random.choice(unrevealed)
            cx = int(c * CELL_W + CELL_W / 2)
            cy = int(r * CELL_H + CELL_H / 2)
            screen_x = cx + BOARD_REGION_LEFT
            screen_y = cy + BOARD_REGION_TOP
            click_points.add((screen_x, screen_y))

    return click_points

def execute_clicks(mine_points: set, click_points: set, arr: list[list[int]]):
    click_points -= mine_points

    for screen_x, screen_y in mine_points:
        #to get the x and y for arr 
        gx = int((screen_x - BOARD_REGION_LEFT) / CELL_W)
        gy = int((screen_y - BOARD_REGION_TOP) / CELL_H)
        arr[gy][gx] = -2

        pyautogui.rightClick(screen_x, screen_y)

    for screen_x, screen_y in click_points:
        pyautogui.click(screen_x, screen_y)
