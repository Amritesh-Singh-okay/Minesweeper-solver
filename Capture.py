import pyautogui
import cv2 as cv
import time 
import numpy as np

time.sleep(3)

# 578,212,748,699 for complete board
# 576,286,750,625 for pixel perfect board

board = pyautogui.screenshot('game.png',region=[578,287,749,625])
# print(board)

img = cv.imread("D:/code/Python/Minesweeper/game.png")

CELL_W = 749 / 24 #31.20
CELL_H = 625 / 20 #31.25

# there is a small error because i cant use decimal val in there it should be 31.24 smt 
# above error is fixed with cell_w and cell_h and use of int(x * CELL_W) .....
for y in range(20):
    for x in range(24):

        x1, y1 = int(x * CELL_W), int(y * CELL_H)
        x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)
        cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 1)

# bgr range for unrevealed cell color
lower = [72, 208, 161]
upper = [82, 216, 171]

# bgr ranges for each number color on revealed cells need to add 6 7
# color_1
lower_1 = (185, 95, 5)
upper_1 = (235, 145, 55)

# color_2
lower_2 = (40, 125, 40)
upper_2 = (80, 165, 75)

# color_3
lower_3 = (35, 35, 200)
upper_3 = (65, 65, 235)

# color_4
lower_4 = (145, 20, 110)
upper_4 = (175, 50, 140)

# color_5
lower_5 = (0, 125, 235)
upper_5 = (20, 165, 255)

# (low, high, draw_color, cell_value) for each no.
colors = [
    (lower_1, upper_1, (210,118,25),1),
    (lower_2, upper_2, (60,142,56),2),
    (lower_3, upper_3, (47,47,211),3),
    (lower_4, upper_4, (162,31,123),4),
    (lower_5, upper_5, (0,143,255),5)
]

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

arr = []

# only to make arr and put unrevealed  = -1 and revealed(with mine no.) = 1-5 empty = 0
for y in range(20):

    row = []

    for x in range(24):

        x1, y1 = int(x * CELL_W), int(y * CELL_H)
        x2, y2 = int((x+1) * CELL_W), int((y+1) * CELL_H)
        cood = img[int(y * CELL_H) + 5][int(x * CELL_W) + 5]

        if(lower[0] <= cood[0] <= upper[0] and lower[1] <= cood[1] <= upper[1] and lower[2] <= cood[2] <= upper[2]):

            row.append(-1)
            cv.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        else:

            cv.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cx = int(x * CELL_W + CELL_W / 2)
            cy = int(y * CELL_H + CELL_H / 2)

            for low, high, draw_color,cell_value in colors:

                if check_patch(img, cx, cy, low, high):
                    row.append(cell_value)
                    cv.circle(img, (cx, cy), 8, draw_color, -1)
                    break

            else:

                row.append(0)

    arr.append(row)


mine_points = set()
click_points = set()
constraints_list = list()
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
                                arr[ny][nx]=-2
                                # print("cx = ",cx+578,"cy = ",cy+287)

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
                                # print("cx = ",cx+578,"cy = ",cy+287)

for A in constraints_list:
    for B in constraints_list:
        if A!=B:
            if A[0].issubset(B[0]):
                New_cell = B[0]-A[0]
                New_count = B[1]-A[1]
                if New_count==0:
                    for ny,nx in New_cell:
                        cx = int(nx * CELL_W + CELL_W / 2)
                        cy = int(ny * CELL_H + CELL_H / 2)
                        click_points.add((cx+578,cy+287))
                        print("cx = ",cx+578,"cy = ",cy+287)
                if New_count == len(New_cell):
                    for ny,nx in New_cell:
                        cx = int(nx * CELL_W + CELL_W / 2)
                        cy = int(ny * CELL_H + CELL_H / 2)
                        mine_points.add((cx+578,cy+287))
                        print("cx = ",cx+578,"cy = ",cy+287)





# print(mine_points)
print(click_points)

for x, y in mine_points:

    #to get the x and y for arr 
    gx = int((x-578)/CELL_W)
    gy = int((y-287)/CELL_H)
    arr[gy][gx] = -2
    pyautogui.rightClick(x, y)
    time.sleep(0.2)

time.sleep(2)

for x, y in click_points:

    #to get the x and y for arr 
    # gx = int((x-578)/CELL_W)
    # gy = int((y-287)/CELL_H)
    # arr[gy][gx] = -2
    pyautogui.click(x,y)
    time.sleep(0.2)


cv.imshow("Display window", img)
k = cv.waitKey(0)