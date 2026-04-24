import pyautogui
import cv2 as cv

img1 = pyautogui.screenshot('game.png',region=[578,212,748,699])
print(img1)

img = cv.imread("D:/code/Python/Minesweeper/game.png")
cv.imshow("Display window", img)
k = cv.waitKey(0)