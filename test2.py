import pytesseract
import imgProcess
from PIL import Image
import cv2
import autoUtils
import time
import datetime,pytz
import startvpt
from autoUtils import virtualKey
import win32con
from imgProcess import rect,Point
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'



'''
screen = imgProcess.captureWindow(hwnd)

cropped = imgProcess.cropImg(screen, rect(Point(452,497),Point(613,517)))
#cropped.show()
result = pytesseract.image_to_string(cropped,lang='vie',config='--psm 6')
result = result.strip()
if result.find('Kênh') is 0:
    print('yes')
print(result)
'''
#time.sleep(3)
#autoUtils.sendKey(hwnd,virtualKey.key_Z.value)\

link = 'http://s3.vuaphapthuat.goplay.vn/s/s40/GameLoaders.swf?user=hardcore1@goid&pass=57eb28cbd0056c78044e36aafac9bad&version=0.9.9a33.271&isExpand=true'
title = 'hardcore1'

startvpt.startGame(title,link)
time.sleep(1)
hwnd = autoUtils.getHandle(title)
time.sleep(3)
a = startvpt.autoLogin()
a.hwnd = hwnd
x =a.start()
print (x)

