import pyautogui
import cv2 as cv
import time 
import numpy as np
import random
from enum import Enum

time.sleep(3)

class SolverState(Enum):
    FOUND_MOVES = 0    # moves found to click or flag
    STUCK = -1         # no moves found, fallback to probability guess
    DONE = 1           # game completed or no moves remaining, exit loop

# Board configuration constants
BOARD_COLS = 24
BOARD_ROWS = 20
TOTAL_MINES = 99

BOARD_REGION_LEFT = 578
BOARD_REGION_TOP = 287
BOARD_REGION_WIDTH = 749
BOARD_REGION_HEIGHT = 625

CELL_W = BOARD_REGION_WIDTH / BOARD_COLS
CELL_H = BOARD_REGION_HEIGHT / BOARD_ROWS

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

cx = int(random.randint(0, BOARD_COLS - 1) * CELL_W + CELL_W / 2)
cy = int(random.randint(0, BOARD_ROWS - 1) * CELL_H + CELL_H / 2)
screen_x = cx + BOARD_REGION_LEFT
screen_y = cy + BOARD_REGION_TOP
pyautogui.click(screen_x, screen_y)

time.sleep(1)

# loop until solver finds nothing new to click or flag
state = SolverState.FOUND_MOVES
while state != SolverState.DONE:
    state = SolverState.DONE
    arr = []
    flaged_mine_count = 0

    # screenshot
    board = pyautogui.screenshot('game.png', region=[BOARD_REGION_LEFT, BOARD_REGION_TOP, BOARD_REGION_WIDTH, BOARD_REGION_HEIGHT])

    img = cv.imread("D:/code/Python/Minesweeper/game.png")

    # draw grid lines on img for debug
    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):

            x1, y1 = int(x * CELL_W), int(y * CELL_H)
            x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 1)


    # build arr
    # -2 = flag  -1 = unrevealed  0 = empty  1-6 = number
    # check flag first then unrevealed then numbers then what left is empty
    # why this order because flag also has green of unrevealed
    for y in range(BOARD_ROWS):

        row = []

        for x in range(BOARD_COLS):

            x1, y1 = int(x * CELL_W), int(y * CELL_H)
            x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)

            cx = int(x * CELL_W + CELL_W / 2)
            cy = int(y * CELL_H + CELL_H / 2)

            if check_patch(img,cx,cy,lower_flag,upper_flag):
                row.append(-2)
                cv.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)
            
            elif check_patch(img, cx, cy, lower, upper):
                row.append(-1)
                cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
            else:

                cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

                for low, high, draw_color,cell_value in colors:

                    if check_patch(img, cx, cy, low, high):
                        row.append(cell_value)
                        cv.circle(img, (cx, cy), 8, draw_color, -1)
                        break

                else:

                    row.append(0)

        arr.append(row)


    mine_points = set()         # screen coords to right-click (flag)
    click_points = set()        # screen coords to left-click (safe)
    constraints_list = list()   # (set of unrevealed neighbors, remaining mine count)
    prob_map = dict()

    # basic solver
    for y in range(BOARD_ROWS):

        for x in range(BOARD_COLS):

            if arr[y][x]>0:
                cells = set()
                unrevealed_count = 0
                mine_count = 0

                for dy in range(-1, 2):

                    for dx in range(-1, 2):

                        if dx == 0 and dy == 0:
                            continue

                        nx = x+dx
                        ny = y+dy

                        if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:

                            if arr[ny][nx]==-1:
                                unrevealed_count+=1
                                cells.add((ny,nx))
                                prob_map.setdefault((ny,nx),[])

                            
                            if arr[ny][nx]==-2:
                                mine_count += 1

                mine = arr[y][x]-mine_count

                if cells:
                    constraints_list.append((cells,mine))

                for key in cells:
                    prob = mine/len(cells)
                    prob_map.setdefault((key),[]).append(prob)

                if mine_count + unrevealed_count==arr[y][x]:

                    for dy in range(-1, 2):

                        for dx in range(-1, 2):

                            if dx == 0 and dy == 0:
                                continue

                            nx = x+dx
                            ny = y+dy

                            if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:

                                if arr[ny][nx]==-1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    screen_x = cx + BOARD_REGION_LEFT
                                    screen_y = cy + BOARD_REGION_TOP
                                    mine_points.add((screen_x, screen_y))
                                    state = SolverState.FOUND_MOVES
                                    arr[ny][nx]=-2

                if mine_count == arr[y][x]:

                    for dy in range(-1,2):

                        for dx in range(-1,2):

                            if dx == 0 and dy == 0:
                                continue

                            nx = x+dx
                            ny = y+dy

                            if 0 <= nx < BOARD_COLS and 0 <= ny < BOARD_ROWS:

                                if arr[ny][nx]==-1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    screen_x = cx + BOARD_REGION_LEFT
                                    screen_y = cy + BOARD_REGION_TOP
                                    click_points.add((screen_x, screen_y))
                                    state = SolverState.FOUND_MOVES


# subset solver
    for A in constraints_list:
        for B in constraints_list:
            if A!=B:
                if A[0].issubset(B[0]):
                    New_cell = B[0]-A[0]
                    New_count = B[1]-A[1]

                    # 0 mines in New_cell — all safe
                    if New_count==0:
                        for ny,nx in New_cell:
                            cx = int(nx * CELL_W + CELL_W / 2)
                            cy = int(ny * CELL_H + CELL_H / 2)
                            screen_x = cx + BOARD_REGION_LEFT
                            screen_y = cy + BOARD_REGION_TOP
                            click_points.add((screen_x, screen_y))
                            state = SolverState.FOUND_MOVES

                    # mines == cells — all mines
                    if New_count == len(New_cell):
                        for ny,nx in New_cell:
                            cx = int(nx * CELL_W + CELL_W / 2)
                            cy = int(ny * CELL_H + CELL_H / 2)
                            screen_x = cx + BOARD_REGION_LEFT
                            screen_y = cy + BOARD_REGION_TOP
                            arr[ny][nx] = -2
                            mine_points.add((screen_x, screen_y))
                            state = SolverState.FOUND_MOVES

    for y in range(BOARD_ROWS):
        for x in range(BOARD_COLS):
            if arr[y][x] == -2:
                flaged_mine_count += 1
    
    if flaged_mine_count == TOTAL_MINES:
        for y in range(BOARD_ROWS):
            for x in range(BOARD_COLS):
                if arr[y][x]==-1:
                    cx = int(x * CELL_W + CELL_W / 2)
                    cy = int(y * CELL_H + CELL_H / 2)
                    screen_x = cx + BOARD_REGION_LEFT
                    screen_y = cy + BOARD_REGION_TOP
                    click_points.add((screen_x, screen_y))  

    if not click_points and not mine_points:
        state = SolverState.STUCK

    # probability based solve

    if state == SolverState.STUCK:

        print("probability ran")

        best_cell = None
        lowest = 9999

        for cell,probs in prob_map.items():

            prob = sum(probs)/len(probs)

            if prob<=lowest:
                lowest = prob
                best_cell = cell
        
        if best_cell is None:
            state = SolverState.DONE
        else:
            
            print(best_cell,lowest)

            cx = int(best_cell[1] * CELL_W + CELL_W / 2)
            cy = int(best_cell[0] * CELL_H + CELL_H / 2)
            screen_x = cx + BOARD_REGION_LEFT
            screen_y = cy + BOARD_REGION_TOP

            click_points.add((screen_x, screen_y))

            state = SolverState.FOUND_MOVES

    click_points -= mine_points

    for screen_x, screen_y in mine_points:

        #to get the x and y for arr 
        gx = int((screen_x - BOARD_REGION_LEFT) / CELL_W)
        gy = int((screen_y - BOARD_REGION_TOP) / CELL_H)
        arr[gy][gx] = -2

        pyautogui.rightClick(screen_x, screen_y)

    for screen_x, screen_y in click_points:

        pyautogui.click(screen_x, screen_y)


cv.imshow("Display window", img)
k = cv.waitKey(0)