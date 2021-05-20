import imgProcess
import autoUtils
from PIL import Image
from imgProcess import Point,rect
import autoUtils

from imgProcess import Point
hwnd = autoUtils.getHandle('hsnam')
hwnd1 = autoUtils.getHandle('hsnu')
hwnd2 = autoUtils.getHandle('cb')
hwnd3 = autoUtils.getHandle('dy')
hwnd4 = autoUtils.getHandle('ts')

print(autoUtils.getWinPos(hwnd))
print(autoUtils.getWinPos(hwnd1))
print(autoUtils.getWinPos(hwnd2))
print(autoUtils.getWinPos(hwnd3))
print(autoUtils.getWinPos(hwnd4))





