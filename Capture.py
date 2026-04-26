import pyautogui
import cv2 as cv
import time 

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


cv.imshow("Display window", img)
k = cv.waitKey(0)