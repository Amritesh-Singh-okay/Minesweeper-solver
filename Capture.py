import pyautogui
import cv2 as cv

# 578,212,748,699 for complete board

board = pyautogui.screenshot('game.png',region=[578,287,748,624])
# print(board)

img = cv.imread("D:/code/Python/Minesweeper/game.png")

# there is a small error because i cant use decimal val in there it should be 31.34 smt
for x in range(24):
    for y in range(20):
        cv.rectangle(img,(x*31,y*31),((x*31)+31,(y*31)+31),(0, 0, 0),2)

cv.imshow("Display window", img)
k = cv.waitKey(0)
