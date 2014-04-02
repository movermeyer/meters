import unittest

from .. import start
from .. import stop
from .. import configure
from .. import clear


##### Public classes #####
class TestStartStop(unittest.TestCase): # pylint: disable=R0904
    def test_start_stop(self):
        try:
            start()
        finally:
            stop()

    def test_start_double(self):
        start()
        try:
            with self.assertRaisesRegex(AssertionError, "Attempt to double start()"):
                start()
        finally:
            stop()

    def test_stop_double(self):
        try:
            start()
            stop()
        finally:
            with self.assertRaisesRegex(AssertionError, "Attempt to double stop()"):
                stop()

    def test_auto_start(self):
        try:
            configure({ "common": { "auto-start": True } })
        finally:
            clear()

