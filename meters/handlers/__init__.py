import threading
import time
import abc


##### Public classes #####
class ThreadedHandler(threading.Thread, metaclass=abc.ABCMeta): # pylint: disable=R0921
    def __init__(self, dumper, period):
        threading.Thread.__init__(self)
        self._dumper = dumper
        self._period = period
        self._stop_loop = False

    def stop(self):
        self._stop_loop = True

    @abc.abstractmethod
    def shot(self, metrics):
        raise NotImplementedError

    def run(self):
        while not self._stop_loop:
            self.shot(self._dumper())
            time.sleep(self._period)

