import imgProcess

from PIL import Image

import AutoUtils
import autoit
hwnd = autoit.win_get_handle('chu quan')



im = imgProcess.CaptureWindow(hwnd)

im1 = imgProcess.getImg('./img/thai_co/bo.png')

p = imgProcess.findImgPoint(im1,im)
print(p)

