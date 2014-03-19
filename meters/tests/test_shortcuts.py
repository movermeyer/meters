import unittest
import sys
import socket
import platform
import time

from .. import shortcuts


##### Public classes #####
class TestShortcuts(unittest.TestCase): # pylint: disable=R0904
    def test_get_app(self):
        orig = sys.argv[0]
        try:
            for name in ("foobar", "foobar.py", "foobar.pyc", "foobar.pyo", "foobar.pyw", "/srv/foobar.py"):
                sys.argv[0] = name
                self.assertEqual(shortcuts.get_app(), "foobar")
            sys.argv[0] = "foobar.py.py"
            self.assertEqual(shortcuts.get_app(), "foobar.py")
        finally:
            sys.argv[0] = orig

    def test_get_node(self):
        self.assertEqual(shortcuts.get_node(), platform.uname()[1])

    def test_get_fqdn(self):
        self.assertEqual(shortcuts.get_fqdn(), socket.getfqdn())

    def test_get_fqdn_refreshed(self):
        for _ in range(3):
            self.assertEqual(shortcuts.get_fqdn(1), socket.getfqdn())
            time.sleep(1)

