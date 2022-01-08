
import threading
import sys
import win32gui
import win32process
import win32con
import win32api
import enum
import time

# SendMessage is synchronous, PostMessage is async


class virtualKey(enum.Enum):
    key_0=0x30
    key_1=0x31
    key_2=0x32
    key_3=0x33
    key_4=0x34
    key_5=0x35
    key_6=0x36
    key_7=0x37
    key_8=0x38
    key_9=0x39
    key_A=0x41
    key_B=0x42
    key_C=0x43
    key_D=0x44
    key_E=0x45
    key_F=0x46
    key_G=0x47
    key_H=0x48
    key_I=0x49
    key_J=0x4A
    key_K=0x4B
    key_L=0x4C
    key_M=0x4D
    key_N=0x4E
    key_O=0x4F
    key_P=0x50
    key_Q=0x51
    key_R=0x52
    key_S=0x53
    key_T=0x54
    key_U=0x55
    key_V=0x56
    key_W=0x57
    key_X=0x58
    key_Y=0x59
    key_Z=0x5A
    key_ESC = 0x1B #c #class #


def changeWinTitle(hwnd,title):
    win32gui.SetWindowText(hwnd,title)

def closeWindow(hwnd):
    win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)


def getHandle(title): #return 0 if not found
    return win32gui.FindWindow(None, title)

def getWinPos(hwnd):
    return win32gui.GetWindowRect(hwnd)

def findAndClose(title):
    hwnd=getHandle(title)
    if hwnd != 0:
        closeWindow(hwnd)

def click(hwnd, point): #most popular method, using PostMessage to get advantage of async
    lParam = win32api.MAKELONG(point[0],point[1])
    win32gui.PostMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,lParam)
    win32gui.PostMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,lParam)
    pass

def clickusingSend(hwnd, point): #same with click but use SendMessage instead of PostMessage
    lParam = win32api.MAKELONG(point[0], point[1])
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

def get_window_pid_by_title(title): #get pid to use with memory access
    hwnd = getHandle(title)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

def sendKey(hwnd,key): #send key to a window, use virtual key class to choose key
    win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN,key,0)
    pass

def clickwithdelay(hwnd,point, delay = 0): #click with delay
    lParam = win32api.MAKELONG(point[0],point[1])
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,lParam)
    if delay != 0:
        time.sleep(delay)
    win32gui.SendMessage(hwnd,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,lParam)

def sendKeyUp(hwnd,key): 
    win32gui.PostMessage(hwnd,win32con.WM_KEYDOWN, key, 0)

def ResizeWindow(hwnd): #this can be used to make sure the window size stay the same (1 minor change can mess up find image Function)
    (x, y, x1, y1) = win32gui.GetWindowRect(hwnd)
    w = 1066
    h = 724
    win32gui.MoveWindow(hwnd,x,y,w,h,True)

class thread_with_trace(threading.Thread):
    #Stoppable thread, since most of program must run in a loop
    #This thread can use kill method to stop and destroy the thread
    #However, daemon thread should be use as well so when close program, all relevant threads close as well
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False

    def start(self):
        self.__run_backup = self.run
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, event, arg):
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True