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

    def test_monotonically_raises(self):
        previous = procfs.Stat()()
        for _ in range(5):
            current = procfs.Stat()()
            for name in ("cpu.user", "cpu.nice", "cpu.system", "cpu.idle"):
                self.assertGreaterEqual(current[name], previous[name])
            previous = current

class TestSelfStat(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = procfs.SelfStat()()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 6)
        for value in results.values():
            self.assertIsInstance(value, (int, float))
            self.assertGreaterEqual(value, 0)

    def test_monotonically_raises(self):
        previous = procfs.Stat()()
        for _ in range(5):
            current = procfs.Stat()()
            for name in current:
                if name.startswith("time"):
                    self.assertGreaterEqual(current[name], previous[name])
            previous = current

class TestLoadAverage(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        results = procfs.LoadAverage()()
        self.assertIsInstance(results, dict)
        self.assertEqual(len(results), 3)
        for value in results.values():
            self.assertIsInstance(value, float)
            self.assertGreaterEqual(value, 0)

