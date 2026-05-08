import pyautogui
import cv2 as cv
import time 
import numpy as np

time.sleep(3)

# TODOO: add probability-based guessing

# 578,212,748,699 for complete board
# 576,286,750,625 for pixel perfect board

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

CELL_W = 749 / 24 #31.20
CELL_H = 625 / 20 #31.25

# loop until solver finds nothing new to click or flag
changed = True
while changed:
    changed = False
    arr = []
    flaged_mine_count = 0

    # screenshot
    board = pyautogui.screenshot('game.png',region=[578,287,749,625])

    img = cv.imread("D:/code/Python/Minesweeper/game.png")

    # draw grid lines on img for debug
    for y in range(20):
        for x in range(24):

            x1, y1 = int(x * CELL_W), int(y * CELL_H)
            x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 1)


    # build arr
    # -2 = flag  -1 = unrevealed  0 = empty  1-6 = number
    # check flag first then unrevealed then numbers then what left is empty
    # why this order because flag also has green of unrevealed
    for y in range(20):

        row = []

        for x in range(24):

            x1, y1 = int(x * CELL_W), int(y * CELL_H)
            x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)
            # cood = img[int(y * CELL_H) + 5][int(x * CELL_W) + 5]
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

    # basic solver
    for y in range(20):

        for x in range(24):

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

                        if 0 <= nx < 24 and 0 <= ny < 20:

                            if arr[ny][nx]==-1:
                                unrevealed_count+=1
                                cells.add((ny,nx))
                            
                            if arr[ny][nx]==-2:
                                mine_count += 1

                mine = arr[y][x]-mine_count

                if cells:
                    constraints_list.append((cells,mine))

                if mine_count + unrevealed_count==arr[y][x]:

                    for dy in range(-1, 2):

                        for dx in range(-1, 2):

                            if dx == 0 and dy == 0:
                                continue

                            nx = x+dx
                            ny = y+dy

                            if 0 <= nx < 24 and 0 <= ny < 20:

                                if arr[ny][nx]==-1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    mine_points.add((cx+578, cy+287))
                                    changed = True
                                    arr[ny][nx]=-2

                if mine_count == arr[y][x]:

                    for dy in range(-1,2):

                        for dx in range(-1,2):

                            if dx == 0 and dy == 0:
                                continue

                            nx = x+dx
                            ny = y+dy

                            if 0 <=nx < 24 and 0 <= ny < 20:

                                if arr[ny][nx]==-1:
                                    cx = int(nx * CELL_W + CELL_W / 2)
                                    cy = int(ny * CELL_H + CELL_H / 2)
                                    click_points.add((cx+578,cy+287))
                                    changed = True


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
                            click_points.add((cx+578,cy+287))
                            changed = True

                    # mines == cells — all mines
                    if New_count == len(New_cell):
                        for ny,nx in New_cell:
                            cx = int(nx * CELL_W + CELL_W / 2)
                            cy = int(ny * CELL_H + CELL_H / 2)
                            arr[ny][nx] = -2
                            mine_points.add((cx+578,cy+287))
                            changed = True

    for y in range(20):
        for x in range(24):
            if arr[y][x] == -2:
                flaged_mine_count += 1
    
    if flaged_mine_count == 99:
        for y in range(20):
            for x in range(24):
                if arr[y][x]==-1:
                    cx = int(x * CELL_W + CELL_W / 2)
                    cy = int(y * CELL_H + CELL_H / 2)
                    click_points.add((cx+578, cy+287))

    click_points -= mine_points

    for x, y in mine_points:

        #to get the x and y for arr 
        gx = int((x-578)/CELL_W)
        gy = int((y-287)/CELL_H)
        arr[gy][gx] = -2
        pyautogui.rightClick(x, y)

    for x, y in click_points:

        pyautogui.click(x,y)


cv.imshow("Display window", img)
k = cv.waitKey(0)