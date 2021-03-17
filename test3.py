import ctypes
import mem_edit
import win32gui,win32process
import time
from AutoUtils import thread_with_trace
from mem_edit import Process
def get_window_pid_by_title(title):
    hwnd = win32gui.FindWindow(None, title)
    threadid,pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid

pid = get_window_pid_by_title('antham3')
magicNumber = input('initial value: ')
def doWork(addr):
    with Process.open_process(pid) as p:
        while(True):
            num_cint = p.read_memory(addr,ctypes.c_long())
            num = num_cint.value
            if(num!=9999):
                p.write_memory(addr,ctypes.c_int(9999))
            time.sleep(1)

with Process.open_process(pid) as p:
    addrs = p.search_all_memory(ctypes.c_int(int(magicNumber)))
    while len(addrs) >1 :
        x = input('value changed: ')
        filtered = p.search_addresses(addrs,ctypes.c_int(int(x)))
        addrs.clear()
        addrs = filtered
        addr = addrs[0]

        th = thread_with_trace(target=doWork, args=(addr,))
        th.start()
print(addrs[0])

