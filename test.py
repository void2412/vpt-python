import imgProcess
import AutoUtils
from PIL import Image

import AutoUtils
import autoit
from imgProcess import Point
hwnd = autoit.win_get_handle('chu quan')



im = imgProcess.CaptureWindow(hwnd)

im1 = imgProcess.getImg('./img/thai_co/thangnhomtruong.png')

p = imgProcess.findImgPoint(im1,im)
print(p)