import unittest
import resource
import threading

from ..scales import python


##### Public classes #####
class TestResources(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        for args in [()] + [
                (getattr(resource, who),)
                for who in dir(resource)
                if who.startswith("RUSAGE_")
            ]:
            value = python.Resources(*args)()
            self.assertIsInstance(value, dict)
            self.assertNotEqual(len(value), 0)
            for (key, value) in value.items():
                self.assertTrue(key.startswith("ru_"))
                self.assertIsInstance(value, (int, float))

class TestThreads(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        value = python.Threads()()
        self.assertIsInstance(value, dict)
        self.assertIsInstance(value["alive_threads"], int)
        self.assertEqual(value["alive_threads"], threading.active_count())

class TestObjects(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        value = python.Objects()()
        self.assertIsInstance(value, dict)
        self.assertIsInstance(value["gc_objects"], int)
        self.assertGreater(value["gc_objects"], 0)

