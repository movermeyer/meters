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
            results = python.Resources(*args)()
            self.assertIsInstance(results, dict)
            self.assertNotEqual(len(results), 0)
            for (key, value) in results.items():
                self.assertTrue(key.startswith("ru_"))
                self.assertIsInstance(value, (int, float))

class TestThreads(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = python.Threads()()
        self.assertIsInstance(results, dict)
        self.assertIsInstance(results["alive_threads"], int)
        self.assertEqual(results["alive_threads"], threading.active_count())

class TestObjects(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = python.Objects()()
        self.assertIsInstance(results, dict)
        self.assertIsInstance(results["gc_objects"], int)
        self.assertGreater(results["gc_objects"], 0)

