import sys
import pytest
import sdl2
from sdl2 import cpuinfo

_HASMP = True
try:
    import multiprocessing
except:
    _HASMP = False


class TestSDLCPUInfo(object):
    __tags__ = ["sdl"]

    def test_SDL_GetCPUCacheLineSize(self):
        ret = cpuinfo.SDL_GetCPUCacheLineSize()
        assert isinstance(ret, int)

    def test_SDL_GetCPUCount(self):
        if _HASMP:
            assert multiprocessing.cpu_count() == cpuinfo.SDL_GetCPUCount()
        else:
            assert cpuinfo.SDL_GetCPUCount() >= 1

    def test_SDL_Has3DNow(self):
        ret = cpuinfo.SDL_Has3DNow()
        assert ret in (0, 1)

    def test_SDL_HasAltiVec(self):
        ret = cpuinfo.SDL_HasAltiVec()
        assert ret in (0, 1)

    def test_SDL_HasMMX(self):
        ret = cpuinfo.SDL_HasMMX()
        assert ret in (0, 1)

    def test_SDL_HasRDTSC(self):
        ret = cpuinfo.SDL_HasRDTSC()
        assert ret in (0, 1)

    def test_SDL_HasSSE(self):
        ret = cpuinfo.SDL_HasSSE()
        assert ret in (0, 1)

    def test_SDL_HasSSE2(self):
        ret = cpuinfo.SDL_HasSSE2()
        assert ret in (0, 1)

    def test_SDL_HasSSE3(self):
        ret = cpuinfo.SDL_HasSSE3()
        assert ret in (0, 1)

    def test_SDL_HasSSE41(self):
        ret = cpuinfo.SDL_HasSSE41()
        assert ret in (0, 1)

    def test_SDL_HasSSE42(self):
        ret = cpuinfo.SDL_HasSSE42()
        assert ret in (0, 1)

    def test_SDL_HasAVX(self):
        ret = cpuinfo.SDL_HasAVX()
        assert ret in (0, 1)

    def test_SDL_HasAVX2(self):
        ret = cpuinfo.SDL_HasAVX2()
        assert ret in (0, 1)

    def test_SDL_GetSystemRAM(self):
        ret = cpuinfo.SDL_GetSystemRAM()
        assert ret > 0

    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_HasAVX512F(self):
        ret = cpuinfo.SDL_HasAVX512F()
        assert ret in (0, 1)

    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_HasARMSIMD(self):
        ret = cpuinfo.SDL_HasARMSIMD()
        assert ret in (0, 1)

    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_HasNEON(self):
        ret = cpuinfo.SDL_HasNEON()
        assert ret in (0, 1)

    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_SIMDGetAlignment(self):
        ret = cpuinfo.SDL_SIMDGetAlignment()
        assert ret % 8 == 0 # Should be multiple of 8

    @pytest.mark.skip("not implemented (no clue how)")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_SIMDAllocFree(self):
        # Should test both SDL_SIMDAlloc and SDL_SIMDFree
        pass

    @pytest.mark.skip("not implemented (no clue how)")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_SIMDRealloc(self):
        pass
