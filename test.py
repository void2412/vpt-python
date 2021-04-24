import imgProcess
import autoUtils
from PIL import Image
from imgProcess import Point
import autoUtils

from imgProcess import Point
hwnd = autoUtils.getHandle('storage void')

needle = imgProcess.getImg('./img/dotim.png')
screen = imgProcess.captureWindow(hwnd)

x = imgProcess.findImgPoint(needle,screen)
print(x)

