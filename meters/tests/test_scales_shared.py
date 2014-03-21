import unittest

from ..scales import shared


##### Public classes #####
class TestShared(unittest.TestCase): # pylint: disable=R0904
    def test_init(self):
        for (args, number) in (
                ((),           0),
                ((int,),       0),
                ((int, 5),     5),
                ((float,),     0.0),
                ((float, 5.0), 5.0),
            ):
            result = shared.Value(*args)()
            self.assertIsInstance(result, type(number))
            self.assertEqual(result, number)

    def test_set_int(self):
        value = shared.Value()
        for number in (5, 10.0, 20):
            value.set(number)
            self.assertIsInstance(value(), int)
            self.assertEqual(value(), number)

    def test_set_float(self):
        value = shared.Value(float)
        for number in (5.0, 10, 20.0):
            value.set(number)
            self.assertIsInstance(value(), float)
            self.assertEqual(value(), number)

    def test_iadd(self):
        value = shared.Value()
        self.assertEqual(value(), 0)
        value += 1
        self.assertEqual(value(), 1)
        value += 5
        self.assertEqual(value(), 6)

    def test_isub(self):
        value = shared.Value()
        self.assertEqual(value(), 0)
        value -= 1
        self.assertEqual(value(), -1)
        value -= 5
        self.assertEqual(value(), -6)

