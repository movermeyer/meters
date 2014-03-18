import threading
import time
import abc


##### Public classes #####
class ThreadedHandler(threading.Thread, metaclass=abc.ABCMeta): # pylint: disable=R0921
    def __init__(self, period):
        threading.Thread.__init__(self)
        self._period = period
        self._stop_loop = False
        self._dumper = None

    def start(self):
        self._stop_loop = False
        threading.Thread.start(self)

    def stop(self):
        self._stop_loop = True

    def set_dumper(self, dumper):
        self._dumper = dumper

    @abc.abstractmethod
    def shot(self, metrics):
        raise NotImplementedError

    def run(self):
        assert self._dumper is not None
        while not self._stop_loop:
            self.shot(self._dumper())
            time.sleep(self._period)

