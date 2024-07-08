import unittest

from examplepy.module1 import Number


class TestSimple(unittest.TestCase):

    def test_add(self):
        self.assertEqual((Number(6) + Number(6)).value, 12)


if __name__ == '__main__':
    unittest.main()
