import imgProcess
import autoUtils
import cv2
import numpy as np
from autoUtils import *
from wincap import *
import pynput
from pynput import keyboard
from pynput.mouse import Controller
from pynput.keyboard import Key as k
from pynput.keyboard import Controller as keycontrol
import startvpt
def main():
    hwnd = autoUtils.getHandle('test')

    img = imgProcess.getImg('./img/truma/cuma.png')

    img2 = imgProcess.getImg('./img/truma/cuthu.png')

    (h1, w1) = (img.shape[0], img.shape[1])

    (h2, w2) = (img2.shape[0], img2.shape[1])

    while True:
        screen = imgProcess.captureWindow(hwnd)

        point1 = imgProcess.findImgPoint(img, screen,0.8)

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
            cv2.destroyAllWindows()
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
    hwnd = getHandle('test')
    autoUtils.ResizeWindow(hwnd)
    keyboard = keycontrol()
    repair = imgProcess.getImg('./img/repairItem.png')
    screen = imgProcess.captureWindow(hwnd)
    p = imgProcess.findImgPoint(repair, screen)
    keyboard.press(k.ctrl)
    click(hwnd, p)
    time.sleep(0.2)
    keyboard.release(k.ctrl)

def main4():
    hwnd = getHandle('test')
    autoUtils.ResizeWindow(hwnd)
    repair = imgProcess.getImg('./img/repairItem.png')
    screen = imgProcess.captureWindow(hwnd)
    p = imgProcess.findImgPoint(repair, screen)
    autoUtils.sendKey(hwnd, win32con.VK_CONTROL)
    
    click(hwnd, p)
    autoUtils.sendKeyUp(hwnd, win32con.VK_CONTROL)
    pass
def main5():
    hwnd = getHandle('test')
    autoUtils.ResizeWindow(hwnd)
    trashcan = imgProcess.getImg('./img/trashcan.png')
    screen = imgProcess.captureWindow(hwnd)
    p = imgProcess.findImgPoint(trashcan, screen)
    useItemPoint = imgProcess.OffsetPoint(p, -357, -436)
    trungthanhPoint = imgProcess.OffsetPoint(p,154,-188)
    click(hwnd, useItemPoint)
    time.sleep(1)
    clickwithdelay(hwnd, trungthanhPoint,0.001)

def main6():
    link='http://s3.vuaphapthuat.goplay.vn/s/s40/GameLoaders.swf?user=comeback2@goid&pass=c51cfbc05d9f20661d27f083349a5e23&version=0.9.9a33.271&isExpand=true'
    title = 'test'
    startvpt.startGameAuto(title, link, 1, 6)

def main7():
    hwnd = autoUtils.getHandle('comeback2')
    screen = imgProcess.captureWindow(hwnd)
    cv2.imshow('',screen)
    cv2.waitKey()
if __name__ == '__main__':
    main6()
    print('finish')