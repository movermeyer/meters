import unittest
import threading

from .. import start
from .. import stop
from .. import is_running_hook
from .. import get_main_thread


##### Public classes #####
class TestMainThreadLogic(unittest.TestCase): # pylint: disable=R0904
    def test_is_running_hook(self):
        self.assertTrue(is_running_hook())

    def test_get_main_thread(self):
        thread = get_main_thread()
        self.assertEqual(thread.name, "MainThread")
        self.assertTrue(thread.is_alive())

    @unittest.skipIf(threading.current_thread().name != "MainThread", "Only for tests executed in main thread")
    def test_get_main_thread_current(self):
        self.assertEqual(get_main_thread(), threading.current_thread())

class TestStartStop(unittest.TestCase): # pylint: disable=R0904
    def test_start_stop_auto(self):
        try:
            start(True)
        finally:
            stop()

    def test_start_stop_no_auto(self):
        try:
            start(False)
        finally:
            stop()

    def test_start_stop_double(self):
        start()
        try:
            with self.assertRaisesRegex(AssertionError, "Attempt to double start()"):
                start()
        finally:
            stop()

    def test_many_stop(self):
        try:
            start()
            stop()
        finally:
            with self.assertRaisesRegex(AssertionError, "Attempt to double stop()"):
                stop()

