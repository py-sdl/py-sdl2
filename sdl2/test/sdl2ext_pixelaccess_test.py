import sys
import unittest
from .. import ext as sdl2ext

try:
    import numpy
    _HASNUMPY = True
except:
    _HASNUMPY = False


class SDL2ExtPixelAccessTest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    @unittest.skipIf(hasattr(sys, "pypy_version_info"),
                     "PyPy's ctypes can't do byref(value, offset)")
    def test_PixelView(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(10, 10), bpp=32)
        view = sdl2ext.PixelView(sprite)
        view[1] = (0xAABBCCDD,) * 10
        rcolor = sdl2ext.prepare_color(0xAABBCCDD, sprite)
        for index, row in enumerate(view):
            if index == 1:
                for col in row:
                    self.assertEqual(col, rcolor)
            else:
                for col in row:
                    self.assertEqual(col, 0x0)

    @unittest.skip("not implemented")
    @unittest.skipIf(not _HASNUMPY, "numpy module is not supported")
    def test_pixels2d(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(5, 10), bpp=32,
                                       masks=(0xFF000000, 0x00FF0000,
                                              0x0000FF00, 0x000000FF))
        sdl2ext.fill(sprite, 0x01, (2, 2, 2, 2))
        nparray = sdl2ext.pixels2d(sprite)

    @unittest.skipIf(not _HASNUMPY, "numpy module is not supported")
    def test_pixels3d(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        sprite = factory.create_sprite(size=(5, 10), bpp=32,
                                       masks=(0xFF000000, 0x00FF0000,
                                              0x0000FF00, 0x000000FF))
        sdl2ext.fill(sprite, 0xAABBCCDD, (1, 2, 3, 4))
        nparray = sdl2ext.pixels3d(sprite)
        for x in range(1, 4):
            for y in range(2, 6):
                self.assertTrue(numpy.all([nparray[x, y],
                                           [0xAA, 0xBB, 0xCC, 0xDD]]))
        self.assertFalse(numpy.all([nparray[0, 0], [0xAA, 0xBB, 0xCC, 0xDD]]))
        self.assertFalse(numpy.all([nparray[1, 0], [0xAA, 0xBB, 0xCC, 0xDD]]))
        self.assertFalse(numpy.all([nparray[0, 1], [0xAA, 0xBB, 0xCC, 0xDD]]))
        self.assertFalse(numpy.all([nparray[3, 6], [0xAA, 0xBB, 0xCC, 0xDD]]))
        self.assertFalse(numpy.all([nparray[4, 6], [0xAA, 0xBB, 0xCC, 0xDD]]))


if __name__ == '__main__':
    sys.exit(unittest.main())
