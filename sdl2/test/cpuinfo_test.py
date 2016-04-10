import sys
import unittest
from .. import cpuinfo

_HASMP = True
try:
    import multiprocessing
except:
    _HASMP = False


class SDLCPUInfoTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def test_SDL_GetCPUCacheLineSize(self):
        ret = cpuinfo.SDL_GetCPUCacheLineSize()
        self.assertIsInstance(ret, int)

    def test_SDL_GetCPUCount(self):
        if _HASMP:
            self.assertEqual(multiprocessing.cpu_count(),
                             cpuinfo.SDL_GetCPUCount())
        else:
            self.assertGreaterEqual(cpuinfo.SDL_GetCPUCount(), 1)

    def test_SDL_Has3DNow(self):
        ret = cpuinfo.SDL_Has3DNow()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasAltiVec(self):
        ret = cpuinfo.SDL_HasAltiVec()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasMMX(self):
        ret = cpuinfo.SDL_HasMMX()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasRDTSC(self):
        ret = cpuinfo.SDL_HasRDTSC()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasSSE(self):
        ret = cpuinfo.SDL_HasSSE()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasSSE2(self):
        ret = cpuinfo.SDL_HasSSE2()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasSSE3(self):
        ret = cpuinfo.SDL_HasSSE3()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasSSE41(self):
        ret = cpuinfo.SDL_HasSSE41()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasSSE42(self):
        ret = cpuinfo.SDL_HasSSE42()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasAVX(self):
        ret = cpuinfo.SDL_HasAVX()
        self.assertIn(ret, (0, 1))

    def test_SDL_HasAVX2(self):
        ret = cpuinfo.SDL_HasAVX2()
        # TODO: remove None as soon as 2.0.4 is released
        self.assertIn(ret, (0, 1))


if __name__ == '__main__':
    sys.exit(unittest.main())
