import ctypes
import mem_edit
import win32gui,win32process
import time
import pytesseract
from autoUtils import *
from imgProcess import *
from mem_edit import Process
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'
hwnd = getHandle('comeback1')
needle = getImg('./img/login/batbuoc.png')
screen = captureWindow(hwnd)
x = findImgPoint(needle,screen)
print(x)
img2 = cropImg(screen,rect(Point(238,219),Point(326,239)))
img2.show()
res = pytesseract.image_to_string(img2,lang='vie',config='--psm 6')

print(res)

