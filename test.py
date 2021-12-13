import imgProcess
import autoUtils
import cv2
import numpy as np
from autoUtils import *
from wincap import *
import pynput
from pynput import keyboard
from pynput.mouse import Controller

def main():
    hwnd = autoUtils.getHandle('ga')

    img = imgProcess.getImg('./img/truma/xongQ.png')

    img2 = imgProcess.getImg('./img/truma/cuma.png')

    (h1, w1) = (img.shape[0], img.shape[1])

    (h2, w2) = (img2.shape[0], img2.shape[1])

    while True:
        screen = imgProcess.captureWindow(hwnd)

        point1 = imgProcess.findImgPoint(img, screen, 0.8)

        if point1 != (0, 0):
            print(point1)
            
            cv2.rectangle(screen, point1, point1, (0,255,0), cv2.LINE_4)

            pass

        point2 = imgProcess.findImgPoint(img2, screen, 0.8)

        if point2 != (0, 0):
            print(point2)
            
            cv2.rectangle(screen,point2,point2,(0,255,0), cv2.LINE_4)
    

        cv2.imshow('winname', screen)
        if cv2.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            break

def main2():
    # ...or, in a non-blocking fashion:
    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release)
    listener.start()
    listener.join()

def on_press(key):
    pass

def on_release(key):
    try:
        if key.char == '1':
            getCurrentMousePos()
    except AttributeError:
        
        pass
    if key == keyboard.Key.esc:
        # Stop listener
        return False

def getCurrentMousePos():
    mouse = Controller()
    print(mouse.position)

def main3():
    hwnd = getHandle('ga')
    autoUtils.ResizeWindow(hwnd)



if __name__ == '__main__':
    main3()