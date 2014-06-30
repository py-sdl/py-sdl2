import sys
import unittest
from ..ext import algorithms


class SDL2ExtAlgorithmsTest(unittest.TestCase):
    __tags__ = ["sdl2ext"]

    @unittest.skip("not implemented")
    def test_cohensutherland(self):
        pass

    @unittest.skip("not implemented")
    def test_liangbarsky(self):
        pass

    @unittest.skip("not implemented")
    def test_clipline(self):
        pass

    def test_point_on_line(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
