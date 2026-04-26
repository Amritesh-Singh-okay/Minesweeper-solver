import pyautogui
import cv2 as cv
import time 
import numpy as np

time.sleep(3)

# 578,212,748,699 for complete board
# 576,286,750,625 for pixel perfect board

board = pyautogui.screenshot('game.png',region=[578,287,748,624])
# print(board)

img = cv.imread("D:/code/Python/Minesweeper/game.png")

# there is a small error because i cant use decimal val in there it should be 31.34 smt
for x in range(24):
    for y in range(20):
        cv.rectangle(img,(x*31,y*31),((x*31)+31,(y*31)+31),(0, 0, 0),1)

lower = [72, 208, 161]
upper = [82, 216, 171]

for x in range(24):
    for y in range(20):
        cood = img[(y*31)+5][(x*31)+5]
        if(lower[0] <= cood[0] <= upper[0] and
        lower[1] <= cood[1] <= upper[1] and
        lower[2] <= cood[2] <= upper[2]):
            
            cv.rectangle(img,(x*31,y*31),((x*31)+31,(y*31)+31),(0, 255, 0),2)
        else:

            cv.rectangle(img,(x*31,y*31),((x*31)+31,(y*31)+31),(0, 0, 255),2)

# color_1 (safe wide range)
lower_1 = (185, 95, 5)
upper_1 = (235, 145, 55)

# color_2 (tightened slightly)
lower_2 = (40, 125, 40)
upper_2 = (80, 165, 75)

# color_3 (keep narrow to avoid clash with 4)
lower_3 = (35, 35, 200)
upper_3 = (65, 65, 235)

# color_4 (tightened to avoid 3)
lower_4 = (145, 20, 110)
upper_4 = (175, 50, 140)

# color_5 (safe, high contrast)
lower_5 = (0, 125, 235)
upper_5 = (20, 165, 255)

colors = [
    (lower_1, upper_1, (210,118,25)),  # color 1
    (lower_2, upper_2, (60,142,56)),   # color 2
    (lower_3, upper_3, (47,47,211)),   # color 3
    (lower_4, upper_4, (162,31,123)),  # color 4
    (lower_5, upper_5, (0,143,255))    # color 5
]

def check_patch(img, cx, cy, low, high, size=21):
    half = size // 2
    h, w = img.shape[:2]

    if cx - half < 0 or cy - half < 0 or cx + half >= w or cy + half >= h:
        return False

    patch = img[cy-half:cy+half+1, cx-half:cx+half+1]

    mask = cv.inRange(patch, np.array(low), np.array(high))

    return np.any(mask == 255)   # ANY pixel match
           

cv.imshow("Display window", img)
k = cv.waitKey(0)