import time, threading
from functools import wraps
from multiprocessing import Process, Queue
import ctypes


def func_timeout(timeout, func, *args):
    """ Run func with the given timeout. If func didn't finish running
        within the timeout, raise TimeLimitExpired
    """

    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

            self.result = None

        def run(self):
            try:
                self.result = func(*args)
            finally:
                pass

        def get_id(self):

            # returns id of the respective thread
            if hasattr(self, '_thread_id'):
                return self._thread_id
            for id, thread in threading._active.items():
                if thread is self:
                    return id

        def terminate(self):
            thread_id = self.get_id()
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                             ctypes.py_object(SystemExit))
            if res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)

    it = FuncThread()
    it.start()
    it.join(timeout)
    if it.isAlive():
        it.terminate()
        raise TimeoutError
    else:
        return it.result
