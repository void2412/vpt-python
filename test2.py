import pytesseract
import imgProcess
from PIL import Image
import cv2
import autoUtils
from imgProcess import rect,Point
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

img = imgProcess.getImg('./img/trongcay/test.png')

hwnd = autoUtils.getHandle('test')
needle = imgProcess.getImg('./img/nhantraQ/roikhoi.png')
screen = imgProcess.captureWindow(hwnd)
base = imgProcess.findImgPoint(needle,screen)

cropped = imgProcess.cropImg(screen, rect(base - Point(109, 138), base + Point(85, -42)))

result = pytesseract.image_to_string(cropped,lang='vie',config='--psm 6')
result = result.strip()
lines = result.splitlines()

for line in lines:
    print(line)
