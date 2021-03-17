import pytesseract
import imgProcess
from PIL import Image
import cv2
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

img = imgProcess.getImg('./img/trongcay/test.png')
imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

result = pytesseract.image_to_string(imgRGB,lang='vie')
result = result.strip()

lines = result.splitlines()

for line in lines:
    if line == "":
        print('empty')
    print(line)
