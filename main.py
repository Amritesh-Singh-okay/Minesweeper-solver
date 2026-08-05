import ctypes
import cv2 as cv
import pyautogui
import time
import random
import winsound

from solver.constants import (
    BOARD_COLS, BOARD_ROWS, TOTAL_MINES, BOARD_REGION_LEFT, BOARD_REGION_TOP,
    CELL_W, CELL_H, SolverState
)
from solver.vision import capture_board, parse_board
from solver.solver import solve_basic, solve_subset, guess_probabilistic, execute_clicks
from solver.stats import record_game

VK_ESCAPE = 0x1B  # Virtual key code for ESC key

# exit solver when esc is pressed
def is_escape_pressed():
    return (ctypes.windll.user32.GetAsyncKeyState(VK_ESCAPE) & 0x8000) != 0

def main():
    print("Starting Minesweeper solver in 5 seconds...")
    print("Please make sure the Minesweeper game window is visible on your screen!")
    print("Press ESC key at any time to stop the solver!")
    time.sleep(5)

    start_time = time.time()

    cx = int(random.randint(0, BOARD_COLS - 1) * CELL_W + CELL_W / 2)
    cy = int(random.randint(0, BOARD_ROWS - 1) * CELL_H + CELL_H / 2)
    screen_x = cx + BOARD_REGION_LEFT
    screen_y = cy + BOARD_REGION_TOP
    pyautogui.click(screen_x, screen_y)

    time.sleep(1)

    # loop until solver finds nothing new to click or flag
    state = SolverState.FOUND_MOVES
    img = None
    flaged_mine_count = 0
    arr = []

    while state != SolverState.DONE:
        if is_escape_pressed():
            print("\nESC key pressed! Exiting solver.")
            winsound.Beep(800, 250)
            break

        state = SolverState.DONE
        flaged_mine_count = 0

        # screenshot
        img = capture_board()

        # parse board matrix
        arr = parse_board(img)

        # basic solver
        mine_points, click_points, constraints_list, prob_map = solve_basic(arr)
        if mine_points or click_points:
            state = SolverState.FOUND_MOVES

        # subset solver
        sub_mine_points, sub_click_points = solve_subset(constraints_list, arr)
        mine_points.update(sub_mine_points)
        click_points.update(sub_click_points)
        if sub_mine_points or sub_click_points:
            state = SolverState.FOUND_MOVES

        for y in range(BOARD_ROWS):
            for x in range(BOARD_COLS):
                if arr[y][x] == -2:
                    flaged_mine_count += 1
        
        if flaged_mine_count == TOTAL_MINES:
            for y in range(BOARD_ROWS):
                for x in range(BOARD_COLS):
                    if arr[y][x] == -1:
                        cx = int(x * CELL_W + CELL_W / 2)
                        cy = int(y * CELL_H + CELL_H / 2)
                        screen_x = cx + BOARD_REGION_LEFT
                        screen_y = cy + BOARD_REGION_TOP
                        click_points.add((screen_x, screen_y))  

        if not click_points and not mine_points:
            state = SolverState.STUCK

        # probability based solve
        if state == SolverState.STUCK:
            prob_clicks = guess_probabilistic(prob_map, arr)
            if prob_clicks:
                click_points.update(prob_clicks)
                state = SolverState.FOUND_MOVES
            else:
                state = SolverState.DONE

        if is_escape_pressed():
            print("\nESC key pressed! Exiting solver.")
            winsound.Beep(800, 250)
            break

        execute_clicks(mine_points, click_points, arr)

    solve_time = time.time() - start_time
    is_win = (flaged_mine_count == TOTAL_MINES or (arr and not any(-1 in row for row in arr)))
    record_game(is_win, solve_time)

    if img is not None:
        cv.imshow("Display window", img)
        k = cv.waitKey(0)

if __name__ == "__main__":
    main()
