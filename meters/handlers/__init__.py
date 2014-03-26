import threading
import time
import abc


##### Public classes #####
class ThreadedHandler(metaclass=abc.ABCMeta): # pylint: disable=R0921
    def __init__(self, period):
        self._period = period
        self._thread = None

    def start(self, dumper):
        assert self._thread is None, "Attempt to double start()"
        self._thread = _HandlerThread(lambda: self.shot(dumper()), self._period)
        self._thread.start()

    def stop(self):
        assert self._thread is not None, "Attempt to double stop()"
        self._thread.stop()
        self._thread.join()
        self._thread = None

    def is_alive(self):
        return ( self._thread is not None and self._thread.is_alive() )

    @abc.abstractmethod
    def shot(self, metrics):
        raise NotImplementedError


##### Private classes #####
class _HandlerThread(threading.Thread):
    def __init__(self, shot, period):
        threading.Thread.__init__(self)
        self._shot = shot
        self._period = period
        self._event = threading.Event()

    def stop(self):
        self._event.set()

    def run(self):
        wait_until = time.time() + self._period
        while not self._event.is_set():
            self._shot()
            self._event.wait(timeout=max(wait_until - time.time(), 0))
            wait_until = time.time() + self._period

