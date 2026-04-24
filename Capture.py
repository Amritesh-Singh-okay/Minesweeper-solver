import pyautogui
import cv2 as cv

# 578,212,748,699 for complete board

board = pyautogui.screenshot('game.png',region=[578,287,748,624])
print(board)

img = cv.imread("D:/code/Python/Minesweeper/game.png")
show = cv.rectangle(img,(0,0),(31,31),(0, 0, 0),1)
cv.imshow("Display window", img)
k = cv.waitKey(0)