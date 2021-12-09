import imgProcess
import autoUtils
import cv2
import numpy as np
from imgProcess import Point
from wincap import *
hwnd = autoUtils.getHandle('ga')

img = imgProcess.getImg('./img/truma/xongQ.png')

img2 = imgProcess.getImg('./img/truma/cuma.png')

(h1, w1) = (img.shape[0], img.shape[1])

(h2, w2) = (img2.shape[0], img2.shape[1])

while True:
    screen = imgProcess.captureWindow(hwnd)
    
    point1 = imgProcess.findImgPoint(img, screen, 0.8)

    if point1 != Point(0, 0):
        print(point1)
        pointX = (point1.x, point1.y)
        cv2.rectangle(screen, pointX, pointX, (0,255,0), cv2.LINE_4)
        
        pass

    point2 = imgProcess.findImgPoint(img2, screen, 0.8)

    if point2 != Point(0, 0):
        print(point2)
        pointX = (point2.x, point2.y)
        cv2.rectangle(screen,pointX,pointX,(0,255,0), cv2.LINE_4)
  
    
    cv2.imshow('winname', screen)
    if cv2.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break