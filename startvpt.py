import time

import autoit

import imgProcess

from functionTimeout import func_timeout


class Error(Exception):
    pass


class InitTimeout(Error):
    pass


class chonKenhTimeout(Error):
    pass


class LoadNhanVatTimeout(Error):
    pass


class LoadMapTimeout(Error):
    pass


def getKenh(i):
    switcher = {
        1: (449, 188),
        2: (449, 223),
        3: (449, 258),
        4: (449, 290),
        5: (449, 325),
        6: (449, 360),
        7: (449, 395),
        8: (449, 425)
    }
    return switcher.get(i, 'invalid')


def getcharLoc(i):
    switcher = {
        1: (292, 420),
        2: (430, 420),
        3: (570, 420)
    }
    return switcher.get(i, 'invalid')


def startGame(title, link):
    autoit.run("flashplayer.exe " + link)
    time.sleep(0.5)
    hwnd = autoit.win_get_handle('Adobe Flash Player')
    autoit.win_set_title_by_handle(hwnd, title)
    time.sleep(0.5)
    return hwnd


def checkLienKet(hwnd):
    needle = imgProcess.getImg('./img/login/lienketquahan.png')
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen)
    if p is None:
        return False
    else:
        return True


def checkInit(hwnd):
    needle = imgProcess.getImg('./img/login/batbuoc.png')
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen)
    if p is None:
        return False
    else:
        return True


def checkNhanVat(hwnd):
    needle = imgProcess.getImg('./img/login/checkNhanVat.png')
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen)
    if p is None:
        return False
    else:
        return True


def finalCheck(hwnd):
    needle = imgProcess.getImg('./img/login/finalCheck.png')
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen)
    if p is None:
        return False
    else:
        return True


def clickBatBuoc(hwnd):
    autoit.control_click_by_handle(hwnd, hwnd, x=453, y=507)


def clickOkLienKet(hwnd):
    autoit.control_click_by_handle(hwnd, hwnd, x=527, y=367)


def clickVaoGame(hwnd):
    autoit.control_click_by_handle(hwnd, hwnd, x=315, y=500)


def clearWindow(hwnd):
    autoit.control_send_by_handle(hwnd, hwnd, '{ESC}')


def waitForInitLoad(hwnd):
    bb = checkInit(hwnd)
    while bb is False:
        time.sleep(5)
        bb = checkInit(hwnd)


def checkKenh(hwnd):
    needle = imgProcess.getImg('./img/login/checkKenh.png')
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen, 0.8)
    while p is None:
        time.sleep(15)
        lkcheck = checkLienKet(hwnd)
        if lkcheck is True:
            clickOkLienKet(hwnd)
            time.sleep(1)
            clickOkLienKet(hwnd)
            time.sleep(1)
            clickOkLienKet(hwnd)
            time.sleep(2)
            clickBatBuoc(hwnd)
            time.sleep(5)
        screen = imgProcess.CaptureWindow(hwnd)
        p = imgProcess.findImgPoint(needle, screen, 0.8)
        if p is None:
            clickBatBuoc(hwnd)

    pass


def waitForLoadAfterChonKenh(hwnd):
    nhanvat = checkNhanVat(hwnd)
    while nhanvat is False:
        time.sleep(3)
        nhanvat = checkNhanVat(hwnd)
    pass


def waitForLoadAfterVaoGame(hwnd):
    final = finalCheck(hwnd)
    while final is False:
        time.sleep(5)
        final = finalCheck(hwnd)


def chonKenh(hwnd, kenh, timeout=-1):
    b = getKenh(kenh)
    if b == 'invalid':
        raise IndexError
    else:
        try:
            func_timeout(timeout, checkKenh, hwnd)
        except TimeoutError:
            raise chonKenhTimeout
        else:
            autoit.control_click_by_handle(hwnd, hwnd, x=b[0], y=b[1])


def chonNV(hwnd, charLoc, timeout=-1):
    p = getcharLoc(charLoc)
    if p == 'invalid':
        raise IndexError
    else:
        try:
            func_timeout(timeout, waitForLoadAfterChonKenh, hwnd)
        except TimeoutError:
            raise LoadNhanVatTimeout
        else:
            autoit.control_click_by_handle(hwnd, hwnd, x=p[0], y=p[1])
            time.sleep(2)
            clickVaoGame(hwnd)


def InitClick(hwnd, timeout=-1):
    try:
        func_timeout(timeout, waitForInitLoad, hwnd)
    except TimeoutError:
        raise InitTimeout
    else:
        clickBatBuoc(hwnd)


def finalize(hwnd, timeout=-1):
    try:
        func_timeout(timeout, waitForLoadAfterVaoGame, hwnd)
    except TimeoutError:
        raise LoadMapTimeout
    else:
        clearWindow(hwnd)


def fullLogin(hwnd, kenh, charLoc):
    res = None
    try:
        InitClick(hwnd, 180)
    except InitTimeout:
        res = 'load game timeout'
        return res
    else:
        time.sleep(7)
        try:
            chonKenh(hwnd, kenh, 180)
        except chonKenhTimeout:
            res = 'chon kenh timeout'
            return res
        except IndexError:
            res = 'kenh out of range'
            return res
        else:
            time.sleep(7)
            try:
                chonNV(hwnd, charLoc, 180)
            except LoadMapTimeout:
                res = 'load chon nhan vat timeout'
                return res
            except IndexError:
                res = 'nhan vat out of range'
                return res
            else:
                time.sleep(15)
                try:
                    finalize(hwnd, 180)
                except LoadMapTimeout:
                    res = 'load map timeout'
                    return res
                else:
                    res = 'full login success'
                    return res


def click(hwnd, x, y):
    autoit.control_click_by_handle(hwnd, hwnd, x=x, y=y)


def checkImg(hwnd, imgPath, tolerance=0.9):
    needle = imgProcess.getImg(imgPath)
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen, tolerance)
    if p is not None:
        return p
    else:
        return False


def waitForImg(hwnd, imgPath, delay=5):
    img = checkImg(hwnd, imgPath)
    while img is False:
        time.sleep(delay)
        img = checkImg(hwnd, imgPath)
    return True


def bugonl(hwnd, charlocation):
    click(hwnd, 815, 82)
    waitForImg(hwnd, './img/daily/nhanvat.png')
    p = checkImg(hwnd, './img/daily/nhanvat.png')
    if p is not False:
        click(hwnd, int(p[0]), int(p[1]))
    charloc = getcharLoc(charlocation)
    time.sleep(2)
    click(hwnd, charloc[0], charloc[1])
    time.sleep(2)
    clickVaoGame(hwnd)
    time.sleep(0.5)
    autoit.win_close_by_handle(hwnd)
    return 'bug onl finished'
    pass
