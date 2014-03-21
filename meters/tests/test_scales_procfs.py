import unittest

from ..scales import procfs


##### Public classes #####
class TestStat(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = procfs.Stat()()
        self.assertIsInstance(results, dict)
        self.assertGreaterEqual(len(results), 4)
        for value in results.values():
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(value, 0)

class TestSelfStat(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = procfs.SelfStat()()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 6)
        for value in results.values():
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(value, 0)

class TestLoadAverage(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = procfs.LoadAverage()()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 3)
        for value in results.values():
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0)

