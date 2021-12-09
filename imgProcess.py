import pytesseract, cv2, numpy
import win32con
import win32gui
import win32ui
import numpy as np
from PIL import Image
from dataclasses import dataclass
pytesseract.pytesseract.tesseract_cmd = r'./Tesseract-OCR/tesseract.exe'

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

@dataclass
class Point:
    #most popular, use this for simplified Point
    x:int =0
    y:int =0
    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        a = Point(x, y)
        return a
    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        a = Point(x, y)
        return a

@dataclass
class rect:
    #this usually is used with cropImg
    topLeft: Point = Point(0, 0)
    bottomRight: Point = Point(0, 0)

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


def cropImg(mainImg,region):
    #crop image
    cropped = mainImg.crop((region.topLeft.x,region.topLeft.y,region.bottomRight.x,region.bottomRight.y))
    return cropped


def captureWindow(hwnd):
    #get size and offset
    window_rect = win32gui.GetWindowRect(hwnd)
    w = window_rect[2] - window_rect[0]
    h = window_rect[3] - window_rect[1]

    border_pixels = 8
    titlebar_pixels = 30

    w = w - (border_pixels * 2)
    h = h - titlebar_pixels - border_pixels
    cropped_x = border_pixels
    cropped_y = titlebar_pixels

    offset_x = window_rect[0] + cropped_x
    offset_y = window_rect[1] + cropped_y


    #get the image of the window
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (cropped_x, cropped_y), win32con.SRCCOPY)
    # convert the raw data into a format opencv can read
    #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (h, w, 4)
    # free resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    # drop the alpha channel, or cv.matchTemplate() will throw an error like:
    #   error: (-215:Assertion failed) (depth == CV_8U || depth == CV_32F) && type == _templ.type() 
    #   && _img.dims() <= 2 in function 'cv::matchTemplate'
    img = img[...,:3]
    # make image C_CONTIGUOUS to avoid errors that look like:
    #   File ... in draw_rectangles
    #   TypeError: an integer is required (got type tuple)
    # see the discussion here:
    # https://github.com/opencv/opencv/issues/14866#issuecomment-580207109
    img = np.ascontiguousarray(img)

    return img
    pass


def findImgPoint(needle, haystack, tolerance=0.9, method=methods[1]):
    #find image and return the middle point of the image, return Point(0,0) if not found
    top_left = None
    middlePoint = None
    result = Point(0, 0)
    toFind = cv2.cvtColor(needle, cv2.COLOR_BGR2GRAY)
    findIn = cv2.cvtColor(haystack, cv2.COLOR_BGR2GRAY)
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



def OffsetPoint(baseLoc, x, y):
    a = Point(x, y)
    a.x = baseLoc.x + x
    a.y = baseLoc.y + y
    return a