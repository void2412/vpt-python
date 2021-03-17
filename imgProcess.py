import pytesseract, cv2, numpy
import win32con
import win32gui
import win32ui
from PIL import Image
from dataclasses import dataclass
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

@dataclass
class Point:
    x:int =0
    y:int =0


def getImg(path):
    img = cv2.imread(path)
    return img
    pass

def getImgForTesseract(path):
    img = getImg(path)
    fixed_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    return fixed_img

def convert2text(img):
    text = pytesseract.image_to_string(img)
    return text
    pass


def cropImg(mainImg,left, top, right, bottom):
    cropped = mainImg.crop((left,top,right,bottom))
    return cropped


def CaptureWindow(hwnd):
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bot - top
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (0, 0), win32con.SRCCOPY)
    bmpInfo = dataBitMap.GetInfo()
    bmpStr = dataBitMap.GetBitmapBits(True)
    im = Image.frombuffer(
        'RGB',
        (bmpInfo['bmWidth'], bmpInfo['bmHeight']),
        bmpStr, 'raw', 'BGRX', 0, 1)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    return im
    pass


def findImgPoint(needle, haystack, tolerance=0.9, method=methods[1]):
    top_left = None
    middlePoint = None
    result = Point(0,0)
    toFind = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
    findIn = cv2.cvtColor(numpy.array(haystack), cv2.COLOR_RGB2GRAY)
    w, h = toFind.shape[::-1]
    matchMode = eval(method)
    res = cv2.matchTemplate(findIn, toFind, matchMode)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        if min_val < tolerance:
            top_left = min_loc
    else:
        if max_val > tolerance:
            top_left = max_loc
    if top_left is not None:
        middlePoint = (top_left[0] + w / 2, top_left[1] + h / 2)
        result.x = int(middlePoint[0])
        result.y = int(middlePoint[1])
    return result
    pass

def findImgPointandFixCoord(needle, haystack, tolerance=0.9, method=methods[1]):
    unfixPoint = findImgPoint(needle,haystack,tolerance,method)
    fixedPoint = Point(0,0)
    if(unfixPoint != Point(0,0)):
        fixedPoint = fixCoord(unfixPoint)
    return fixedPoint

def fixCoord(x, y):
    p = Point(x,y)
    p.x = p.x - 8
    p.y = p.y - 31
    return p
    pass

def fixCoord(p):
    res = Point(0,0)
    res.x = p.x - 8
    res.y = p.y - 31
    return res
    pass

def OffsetPoint(baseLoc, x, y):
    a = Point(x,y)
    a.x = baseLoc.x + x
    a.y = baseLoc.y + y
    return a