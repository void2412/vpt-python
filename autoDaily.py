import time
import pyautogui
import autoit
import win32gui
import imgProcess
import startvpt
from functionTimeout import func_timeout


class gotoposTimeout(Exception):
    pass


class finishtt(Exception):
    pass


class loadMapTimeout(Exception):
    pass


class loadWindowTimeout(Exception):
    pass


class nhanQpbfinished(Exception):
    pass


def click(hwnd, x, y):
    autoit.control_click_by_handle(hwnd, hwnd, x=x, y=y)


def clearWindow(hwnd):
    autoit.control_send_by_handle(hwnd, hwnd, '{ESC}')


def sendKey(hwnd, key):
    autoit.control_send_by_handle(hwnd, hwnd, key)


def checkImg(hwnd, imgPath, tolerance=0.9):
    needle = imgProcess.getImg(imgPath)
    screen = imgProcess.CaptureWindow(hwnd)
    p = imgProcess.findImgPoint(needle, screen, tolerance)
    if p is not None:
        return p
    else:
        return False


def clickCo(hwnd):
    p = checkImg(hwnd, './img/daily/co.png')
    if p is not False:
        click(hwnd, int(p[0]), int(p[1]))


def nhanvip(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 223, 57)
    time.sleep(5)
    checkVip = checkImg(hwnd, './img/daily/vipPanel.png')
    while checkVip is False:
        time.sleep(7)
        checkVip = checkImg(hwnd, './img/daily/vipPanel.png')
    time.sleep(1.5)
    click(hwnd, 461, 284)
    time.sleep(1)
    click(hwnd, 461, 303)
    time.sleep(1)
    click(hwnd, 461, 324)
    time.sleep(1)
    for i in range(6):
        click(hwnd, 526, 356)
        time.sleep(1)
    click(hwnd, 461, 356)
    return 'hoan thanh nhan vip'
    pass


def nlswitch(i):
    switcher = {
        0: (160.5, -57),
        1: (31.5, -57),
        2: (-96.5, -57),
        3: (160.5, -104),
        4: (31.5, -104),
        5: (-96.5, -104),
        6: (160.5, -153),
        7: (31.5, -153),
        8: (-96.5, -153),
        9: (160.5, -199)
    }
    return switcher.get(i, 'invalid')


datoffset = [
    (-61, -72),
    (-113, -41),
    (-166, -7),
    (-223, 24),
    (-118, -107),
    (-171, -77),
    (-223, -45),
    (-279, -12),
    (-175, -144),
    (-229, -114),
    (-281, -80),
    (-336, -48),
    (-229, -179),
    (-283, -150),
    (-336, -116),
    (-391, -84)
]


def trongtrangvien(hwnd, nguyenlieu=0):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 860, 330)
    time.sleep(2)
    trangvien = checkImg(hwnd, './img/daily/trangvien.png')
    while trangvien is False:
        time.sleep(7)
        trangvien = checkImg(hwnd, './img/daily/trangvien.png')
    trangvien = (int(trangvien[0]), int(trangvien[1]))
    click(hwnd, int(trangvien[0] + 246), int(trangvien[1] + 265))
    time.sleep(2)
    shoptrangvien = checkImg(hwnd, './img/daily/shoptrangvien.png')
    while shoptrangvien is False:
        time.sleep(5)
        shoptrangvien = checkImg(hwnd, './img/daily/shoptrangvien.png')
    nloffset = nlswitch(nguyenlieu)
    nlpoint = (shoptrangvien[0] - nloffset[0], shoptrangvien[1] - nloffset[1])
    click(hwnd, int(nlpoint[0]), int(nlpoint[1]))
    time.sleep(2)
    for offset in datoffset:
        datpoint = (int(trangvien[0] - offset[0]), int(trangvien[1] - offset[1]))
        click(hwnd, datpoint[0], datpoint[1])
        time.sleep(3)
    click(hwnd, trangvien[0], trangvien[1])
    time.sleep(2)
    click(hwnd, trangvien[0] + 357, trangvien[1] + 269)
    time.sleep(2)
    click(hwnd, trangvien[0] + 222, trangvien[1] + 48)
    time.sleep(2)
    return 'hoan thanh trong trang vien'
    pass


def clickxuong(hwnd):
    p = checkImg(hwnd, './img/daily/xuong.png')
    if p is not False:
        click(hwnd, int(p[0]), int(p[1]))


def clickbay(hwnd):
    p = checkImg(hwnd, './img/daily/bay.png')
    if p is not False:
        click(hwnd, int(p[0]), int(p[1]))


def clicktatbangnhiemvu(hwnd):
    click(hwnd, 775, 158)


def checkLoadMap(hwnd, imgPath):
    qct = checkImg(hwnd, imgPath)
    while qct is False:
        time.sleep(5)
        qct = checkImg(hwnd, imgPath)
    return True


def waitForImg(hwnd, imgPath, delay=5):
    img = checkImg(hwnd, imgPath)
    while img is False:
        time.sleep(delay)
        img = checkImg(hwnd, imgPath)
    return True


def waitForImgDisappear(hwnd, imgPath, delay=5):
    img = checkImg(hwnd, imgPath)
    while img is not False:
        time.sleep(delay)
        img = checkImg(hwnd, imgPath)
    return True


def resetgotohanhlangpos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 434, 443)  # click QCT
    time.sleep(5)
    click(hwnd, 707, 391)  # click to move - reset ban do pos
    time.sleep(5)
    click(hwnd, 453, 180)  # click 133,55 trên bản đồ
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(12)


def gotohanhlangpos(hwnd):
    resetgotohanhlangpos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/hanhlangpos.png')
    while p is False:
        resetgotohanhlangpos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/hanhlangpos.png')
    return True


def nhanhanhlang(hwnd, timeout=-1):
    clearWindow(hwnd)
    time.sleep(2)
    clickxuong(hwnd)  # click xuống nếu đang bay
    time.sleep(5)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 434, 443)  # click QCT
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/qct.png')
    except TimeoutError:
        return 'load map timeout while doing nhan hanh lang'
    else:
        try:
            time.sleep(2)
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(timeout, gotohanhlangpos, hwnd)
        except TimeoutError:
            return 'go to hanh lang pos timeout'
        else:
            click(hwnd, 365, 195)
            try:
                func_timeout(timeout, waitForImg, hwnd, './img/daily/hanhlangwindow.png')
            except TimeoutError:
                return 'wait for hanh lang window timeout'
            else:
                time.sleep(2)
                click(hwnd, 290, 435)
                time.sleep(2)
                return 'nhan hanh lang finished'
    pass


def resetgettopb1pos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 630, 356)  # click TLT
    time.sleep(2)
    click(hwnd, 692, 363)  # click to move - reset ban do pos
    time.sleep(5)
    click(hwnd, 539, 235)  # click 295,144 trên bản đồ
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(10)
    pass


def gotopb1pos(hwnd):
    resetgettopb1pos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/pb1pos.png')
    while p is False:
        resetgettopb1pos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/pb1pos.png')
    return True
    pass


def nhanQpb1(hwnd, timeout=-1):
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 630, 356)  # click TLT
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/tlt.png')
    except TimeoutError:
        raise loadMapTimeout
    else:
        try:
            time.sleep(2)
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(timeout, gotopb1pos, hwnd)
        except TimeoutError:
            raise gotoposTimeout
        else:
            for i in range(7):
                click(hwnd, 619, 329)  # click NPC
                try:
                    func_timeout(30, waitForImg, hwnd, './img/daily/coQ.png')
                except TimeoutError:
                    raise nhanQpbfinished
                else:
                    click(hwnd, 318, 335)
                    waitForImg(hwnd, './img/daily/nhanQ.png', 3)
                    click(hwnd, 300, 422)
                    waitForImg(hwnd, './img/daily/traQ.png', 3)
                    click(hwnd, 260, 421)
                    time.sleep(2)
                    click(hwnd, 364, 534)
                    time.sleep(1)
                    a = checkImg(hwnd, './img/daily/closepb1.png')
                    while a is not False:
                        time.sleep(3)
                        a = checkImg(hwnd, './img/daily/closepb1.png')
            time.sleep(3)
            raise nhanQpbfinished

    pass


def resetgotopb2pos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 301, 508)  # click CD
    time.sleep(2)
    click(hwnd, 515, 186)  # click to move - reset ban do
    time.sleep(5)
    click(hwnd, 537, 137)  # click 195,23 tren ban do
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(12)


def gotopb2pos(hwnd):
    resetgotopb2pos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/pb2pos.png')
    while p is False:
        resetgotopb2pos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/pb2pos.png')
    pass


def nhanQpb2(hwnd, timeout=-1):
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 301, 508)  # click CD
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/cd.png')
    except TimeoutError:
        raise loadMapTimeout
    else:
        try:
            time.sleep(2)
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(timeout, gotopb2pos, hwnd)
        except TimeoutError:
            raise gotoposTimeout
        else:
            click(hwnd, 600, 207)  # click NPC
            time.sleep(2)
            waitForImg(hwnd, './img/daily/nhanbando.png')
            click(hwnd, 281, 337)
            try:
                time.sleep(2)
                func_timeout(20, waitForImg, hwnd, './img/daily/nhanQtham.png')
                click(hwnd, 312, 250)
                time.sleep(1)
                waitForImg(hwnd, './img/daily/coQ2.png')
            except TimeoutError:
                raise nhanQpbfinished
            else:
                click(hwnd, 281, 327)
                waitForImg(hwnd, './img/daily/nhanQ.png', 3)
                time.sleep(2)
                click(hwnd, 300, 422)
                waitForImg(hwnd, './img/daily/traQ.png', 3)
                click(hwnd, 260, 421)
                time.sleep(2)
                click(hwnd, 364, 534)
                time.sleep(1)
                a = checkImg(hwnd, './img/daily/closepb2.png')
                while a is not False:
                    time.sleep(3)
                    a = checkImg(hwnd, './img/daily/closepb2.png')
            time.sleep(3)
            raise nhanQpbfinished


def getbarlocation(hwnd):
    up = checkImg(hwnd, './img/daily/upbar.png')
    down = checkImg(hwnd, './img/daily/downbar.png')
    if up is not False and down is not False:
        return 2
    if up is not False and down is False:
        return 3
    if up is False and down is not False:
        return 1
    if up is False and down is False:
        raise IndexError


def startautopb(hwnd):
    try:
        barloc = getbarlocation(hwnd)
    except IndexError:
        raise IndexError
    if barloc == 3:
        godown = False
    else:
        godown = True
    pbico = checkImg(hwnd, './img/daily/pbicon.png')
    while pbico is False:
        if barloc == 3:
            click(hwnd, 280, 45)
            godown = False
            barloc = 2
        if barloc == 1:
            click(hwnd, 280, 83)
            godown = True
            barloc = 2
        if barloc == 2:
            if godown is True:
                click(hwnd, 280, 83)
                godown = False
                barloc = 3
            else:
                click(hwnd, 280, 45)
                godown = True
                barloc = 1
        time.sleep(3)
        pbico = checkImg(hwnd, './img/daily/pbicon.png')

    pbicon = (int(pbico[0]), int(pbico[1]))
    time.sleep(3)
    click(hwnd, pbicon[0], pbicon[1])
    time.sleep(2)
    waitForImg(hwnd, './img/daily/autopbwindow.png')
    autopbwin = checkImg(hwnd, './img/daily/autopbwindow.png')
    p = (int(autopbwin[0]), int(autopbwin[1]))
    click(hwnd, p[0] - -261, p[1] - 68)  # sang trang 2
    time.sleep(2)
    click(hwnd, p[0] - -211, p[1] - 213)  # bat dau tham hiem
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -77, p[1] - 272)  # bat dau the gioi so
    time.sleep(2)
    click(hwnd, p[0] - -46, p[1] - 197)
    time.sleep(2)
    click(hwnd, p[0] - 19, p[1] - 211)
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -163, p[1] - 68)  # ve trang 1
    time.sleep(2)
    click(hwnd, p[0] - 15, p[1] - 210)  # bat dau mhd
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -436, p[1] - 210)  # bat dau ltc
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -75, p[1] - 167)  # bat dau ld
    time.sleep(2)
    click(hwnd, p[0] - -44, p[1] - 93)
    time.sleep(2)
    click(hwnd, p[0] - 16, p[1] - 107)
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -301, p[1] - 167)  # bat dau lang huyet
    time.sleep(2)
    click(hwnd, p[0] - -270, p[1] - 93)
    time.sleep(2)
    click(hwnd, p[0] - -209, p[1] - 107)
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -209, p[1] - 210)  # bat dau mc
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, p[0] - -529, p[1] - 167)  # bat dau quy hut mau
    time.sleep(2)
    click(hwnd, p[0] - -496, p[1] - 93)
    time.sleep(2)
    click(hwnd, p[0] - -435, p[1] - 107)
    time.sleep(2)
    clickCo(hwnd)


def autopb(hwnd, timeout=-1):
    clearWindow(hwnd)
    time.sleep(2)
    clickbay(hwnd)  # click bay nếu ko bay
    time.sleep(5)
    try:
        nhanQpb1(hwnd, timeout)
    except gotoposTimeout:
        return 'go to pb1 pos timeout'
    except loadMapTimeout:
        return 'load map TLT timeout'
    except nhanQpbfinished:
        try:
            nhanQpb2(hwnd, timeout)
        except loadMapTimeout:
            return 'load map CD timeout'
        except gotoposTimeout:
            return 'go to pb2 pos timeout'
        except nhanQpbfinished:
            try:
                startautopb(hwnd)
            except IndexError:
                return 'cant get bar location'
            else:
                return 'hoan thanh auto pb'

    pass


def resetnhanx2pos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 440, 238)  # click DHT
    time.sleep(2)
    click(hwnd, 505, 450)  # click to move - reset ban do
    time.sleep(5)
    click(hwnd, 520, 213)  # click 243,106 tren ban do
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(10)

    pass


def gotonhanx2pos(hwnd):
    resetnhanx2pos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/x2pos2.png')
    while p is False:
        resetnhanx2pos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/x2pos2.png')
    pass


def nhanx2(hwnd, timeout=-1):
    clickxuong(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 440, 238)  # click DHT
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/dht.png')
    except TimeoutError:
        raise loadMapTimeout
    else:
        try:
            time.sleep(2)
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(time, gotonhanx2pos, hwnd)
        except TimeoutError:
            raise gotoposTimeout
        else:
            click(hwnd, 392, 152)  # click x2 NPC
            waitForImg(hwnd, './img/daily/x2window.png')
            time.sleep(1.5)
            click(hwnd, 290, 337)
            waitForImg(hwnd, './img/daily/x2window2.png')
            time.sleep(1.5)
            click(hwnd, 290, 337)
            time.sleep(1.5)
    pass


def resetgotothantupos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 434, 443)  # click QCT
    time.sleep(3)
    click(hwnd, 707, 391)  # click to move - reset ban do pos
    time.sleep(5)
    click(hwnd, 560, 164)  # click 212,43 tren ban do
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(15)
    pass


def gotothantupos(hwnd):
    resetgotothantupos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/thantupos.png')
    while p is False:
        resetgotothantupos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/thantupos.png')
    pass


def startthantu(hwnd, timeout=-1):
    clickxuong(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 434, 443)  # click QCT
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/qct.png')
    except TimeoutError:
        raise loadMapTimeout
    else:
        try:
            time.sleep(2)
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(timeout, gotothantupos, hwnd)
        except TimeoutError:
            raise gotoposTimeout
        else:
            click(hwnd, 590, 237)  # click tt NPC
            try:
                func_timeout(timeout, waitForImg, hwnd, './img/daily/ttwindow1.png')
            except TimeoutError:
                raise loadWindowTimeout
            else:
                time.sleep(1.5)
                click(hwnd, 290, 360)  # click tu dong than tu
                waitForImg(hwnd, './img/daily/autottwindow.png')
                time.sleep(1.5)
                click(hwnd, 641, 390)  # click bat dau
                time.sleep(2)
                clickCo(hwnd)
                time.sleep(2)
                click(hwnd, 593, 357)
                try:
                    func_timeout(30, waitForImg, hwnd, './img/daily/autorunning.png')
                except TimeoutError:
                    raise finishtt

    pass


def autothantu(hwnd, timeout=-1):
    clearWindow(hwnd)
    time.sleep(2)
    try:
        nhanx2(hwnd, timeout)
    except loadMapTimeout:
        return 'load map DHT timeout'
    except gotoposTimeout:
        return 'go to x2 NPC pos timeout'
    else:
        time.sleep(2)
        try:
            startthantu(hwnd, timeout)
        except loadMapTimeout:
            return 'load map QCT timeout'
        except gotoposTimeout:
            return 'go to tt NPC pos timeout'
        except loadWindowTimeout:
            return 'wait for NPC dialog box timeout'
        except finishtt:
            return 'finished autott'
        else:
            waitForImgDisappear(hwnd, './img/daily/autorunning.png', 10)
            return 'finished autott'
    pass


def resetgototuhanhpos(hwnd):
    clearWindow(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 289, 150)  # click TTD
    time.sleep(3)
    click(hwnd, 506, 197)  # click to move - reset ban do pos
    time.sleep(5)
    click(hwnd, 564, 174)  # click 215,51 tren ban do
    time.sleep(2)
    clearWindow(hwnd)
    time.sleep(15)
    pass


def gototuhanhpos(hwnd):
    resetgototuhanhpos(hwnd)
    time.sleep(2)
    p = checkImg(hwnd, './img/daily/tuhanhpos.png')
    while p is False:
        resetgototuhanhpos(hwnd)
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/tuhanhpos.png')
    pass


def autotuhanh(hwnd, timeout=-1):
    clearWindow(hwnd)
    time.sleep(2)
    clickbay(hwnd)
    time.sleep(2)
    click(hwnd, 770, 115)  # click bản đồ
    time.sleep(2)
    click(hwnd, 645, 89)  # click thế giới
    time.sleep(2)
    click(hwnd, 289, 150)  # click TTD
    time.sleep(2)
    clickCo(hwnd)  # bấm enter in case TDP expire
    time.sleep(3)
    try:
        func_timeout(timeout, checkLoadMap, hwnd, './img/daily/ttd.png')
    except TimeoutError:
        return 'load map TTD timeout'
    else:
        try:
            clearWindow(hwnd)
            time.sleep(2)
            func_timeout(timeout, gototuhanhpos, hwnd)
        except TimeoutError:
            return 'go to tu hanh pos timeout'
        else:
            click(hwnd, 611, 260)  # click NPC
            waitForImg(hwnd, './img/daily/tuhanhwindow.png')
            click(hwnd, 290, 363)
            waitForImg(hwnd, './img/daily/autotuhanhwindow.png')
            click(hwnd, 641, 390)
            time.sleep(2)
            clickCo(hwnd)
            click(hwnd, 593, 357)
            try:
                func_timeout(30, waitForImg, hwnd, './img/daily/autorunning.png')
            except TimeoutError:
                return 'finished auto tu hanh'
            return 'finished auto tu hanh'
    pass


def getleveltinhcung(i):
    switcher = {
        1: (813, 59),
        2: (813, 103),
        3: (813, 147),
        4: (813, 188),
        5: (813, 233),
        6: (813, 274),
        7: (813, 316),
        8: (813, 360),
        9: (813, 405),
        10: (813, 448),
        11: (813, 490),
        12: (813, 533)
    }
    return switcher.get(i, 'invalid level')


def getloaitinhcung(i):
    switcher = {
        1: (118, 114),
        2: (306, 114),
        3: (494, 114),
        4: (680, 114),
        5: (118, 288),
        6: (306, 288),
        7: (494, 288),
        8: (680, 288),
        9: (118, 464),
        10: (306, 464),
        11: (494, 464),
        12: (680, 464)
    }
    return switcher.get(i, 'invalid input')


def tinhcungsetup(hwnd, leveltinhcung, loaitinhcung):
    clearWindow(hwnd)
    time.sleep(1)
    clearWindow(hwnd)
    barloc = getbarlocation(hwnd)
    lvtc = getleveltinhcung(leveltinhcung)
    loaitc = getloaitinhcung(loaitinhcung)
    if barloc == 3:
        godown = False
    else:
        godown = True
    p = checkImg(hwnd, './img/daily/tinhcungicon.png')
    while p is False:
        if barloc == 3:
            click(hwnd, 280, 45)
            godown = False
            barloc = 2
        if barloc == 1:
            click(hwnd, 280, 83)
            godown = True
            barloc = 2
        if barloc == 2:
            if godown is True:
                click(hwnd, 280, 83)
                godown = False
                barloc = 3
            else:
                click(hwnd, 280, 45)
                godown = True
                barloc = 1
        time.sleep(2)
        p = checkImg(hwnd, './img/daily/tinhcungicon.png')
    p = (int(p[0]), int(p[1]))
    click(hwnd, p[0], p[1])
    time.sleep(2)
    click(hwnd, lvtc[0], lvtc[1])
    time.sleep(2)
    pscreen = win32gui.ClientToScreen(hwnd, loaitc)
    time.sleep(2)
    win32gui.SetForegroundWindow(hwnd)
    time.sleep(2)
    autoit.mouse_move(pscreen[0], pscreen[1], 0)
    time.sleep(2)
    click(hwnd, loaitc[0], loaitc[1])
    time.sleep(2)
    return 'tc setup finished'
    pass


def finishingautotinhcung(hwnd):
    waitForImg(hwnd, './img/daily/autotinhcungwindow.png')
    for i in range(5):
        click(hwnd, 700, 232)
        time.sleep(1)
    click(hwnd, 641, 390)  # click bat dau
    time.sleep(2)
    clickCo(hwnd)
    time.sleep(2)
    click(hwnd, 593, 357)
    try:
        func_timeout(30, waitForImg, hwnd, './img/daily/autorunning.png')
    except TimeoutError:
        return 'finished tinh cung'
    waitForImgDisappear(hwnd, './img/daily/autorunning.png', 10)
    return 'finished tinh cung'


def setupthietlap(hwnd):
    clearWindow(hwnd)
    time.sleep(1)
    click(hwnd, 807, 120)
    time.sleep(1)
    click(hwnd, 820, 83)
    waitForImg(hwnd, './img/daily/hethong.png', 1)
    annhanvat = checkImg(hwnd, './img/daily/annhanvat.png')
    anten = checkImg(hwnd, './img/daily/anten.png')
    dongmau = checkImg(hwnd, './img/daily/dongmau.png')
    if annhanvat is not False:
        click(hwnd, 395, 166)
    time.sleep(0.5)
    if anten is not False:
        click(hwnd, 388, 183)
    time.sleep(0.5)
    if dongmau is not False:
        click(hwnd, 399, 220)
    return 'finished setup thiet lap'
    pass


def clickfixdo(hwnd):
    pyautogui.keyDown('ctrl')
    time.sleep(1)
    click(hwnd, 456, 519)
    time.sleep(1)
    pyautogui.keyUp('ctrl')
    click(hwnd, 328, 143)


def fixdo(hwnd):
    clearWindow(hwnd)
    time.sleep(1)
    clearWindow(hwnd)
    time.sleep(1)
    click(hwnd, 609, 560)
    waitForImg(hwnd, 'img/daily/tuido.png')
    clickfixdo(hwnd)
    return 'sửa đồ finish'
    pass


def bugonl(hwnd, charloc):
    clearWindow(hwnd)
    time.sleep(1.5)
    clearWindow(hwnd)
    time.sleep(1.5)
    res = startvpt.bugonl(hwnd, charloc)
    return res


def doinangno(hwnd):
    pass


def daupet(hwnd):
    pass


def findandclickicon(hwnd, pathToImg, tolerance=0.9):
    clearWindow(hwnd)
    time.sleep(1)
    clearWindow(hwnd)
    barloc = getbarlocation(hwnd)
    if barloc == 3:
        godown = False
    else:
        godown = True
    p = checkImg(hwnd, pathToImg, tolerance)
    while p is False:
        if barloc == 3:
            click(hwnd, 280, 45)
            godown = False
            barloc = 2
        if barloc == 1:
            click(hwnd, 280, 83)
            godown = True
            barloc = 2
        if barloc == 2:
            if godown is True:
                click(hwnd, 280, 83)
                godown = False
                barloc = 3
            else:
                click(hwnd, 280, 45)
                godown = True
                barloc = 1
        time.sleep(2)
        p = checkImg(hwnd, pathToImg, tolerance)
    if p is not False:
        return p


def khonggiandieukhac(hwnd):
    clearWindow(hwnd)
    time.sleep(1)
    clearWindow(hwnd)
    try:
        iconPoint = func_timeout(30, findandclickicon, hwnd, './img/daily/khonggiandieukhacicon.png')
    except TimeoutError:
        raise TimeoutError
    else:
        pass
    pass


def phitac(hwnd):
    pass


def aomathap(hwnd):
    pass
