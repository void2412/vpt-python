import imgProcess
import autoUtils
from PIL import Image
from imgProcess import Point
import autoUtils

from imgProcess import Point
hwnd = autoUtils.getHandle('test')

needle = imgProcess.getImg('./img/trongcay/cayChin.png')
screen = imgProcess.captureWindow(hwnd)

x = imgProcess.findImgPointandFixCoord(needle,screen)

if (Point(30,10) != Point.empty):
    print('ok')
else:
    print('no')

if (Point(0,0) == Point.empty):
    print('ok')
else:
    print('no')