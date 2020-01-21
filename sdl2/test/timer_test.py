import sys
import time
import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_TIMER
from sdl2 import timer


if sys.version_info[0] >= 3:
    long = int

calls = []


class TestSDLTimer(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_TIMER) != 0:
            raise pytest.skip('Timer subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_QuitSubSystem(SDL_INIT_TIMER)
        SDL_Quit()

    def test_SDL_GetTicks(self):
        ticks = timer.SDL_GetTicks()
        time.sleep(1)
        ticks2 = timer.SDL_GetTicks()
        time.sleep(1)
        ticks3 = timer.SDL_GetTicks()

        assert ticks3 > ticks2
        assert ticks2 > ticks
        # Add some latency, since the final numbers can heavily depend
        # on the system's context switching behaviour, load, etc., etc.,
        # etc.
        # self.assertTrue(abs(ticks2 - 1000 - ticks) <= 3,
        #     "1: %f is not <= 3 for %f and %f" % (abs(ticks2 - 1000 - ticks),
        #                                       ticks2, ticks))
        # self.assertTrue(abs(ticks3 - 1000 - ticks2) <= 3,
        #     "2: %f is not <= 3 for %f and %f" % (abs(ticks3 - 1000 - ticks2),
        #                                       ticks3, ticks2))
        # self.assertTrue(abs(ticks3 - 2000 - ticks) <= 3,
        #     "3: %f is not <= 3 for %f and %f" % (abs(ticks3 - 2000 - ticks2),
        #                                       ticks3, ticks))

    def test_SDL_GetPerformanceCounter(self):
        perf = timer.SDL_GetPerformanceCounter()
        assert type(perf) in (int, long)

    def test_SDL_GetPerformanceFrequency(self):
        freq = timer.SDL_GetPerformanceFrequency()
        assert type(freq) in (int, long)

    @pytest.mark.skip("precision problems")
    def test_SDL_Delay(self):
        for wait in range(5, 200, 5):
            start = time.time() * 1000
            timer.SDL_Delay(wait)
            end = time.time() * 1000
            sm = (end - start)
            err = "%f is not <= 3 for %f and %f" % (abs(wait - sm), wait, sm)
            assert abs(wait - sm) <= 3, err
                

    @pytest.mark.skipif(hasattr(sys, "pypy_version_info"),
        reason="PyPy can't access other vars properly from a separate thread")
    def test_SDL_AddRemoveTimer(self):
        calls = []

        def timerfunc(interval, param):
            calls.append(param)
            return interval

        callback = timer.SDL_TimerCallback(timerfunc)
        timerid = timer.SDL_AddTimer(100, callback, "Test")
        start = timer.SDL_GetTicks()
        end = long(start)
        while (end - start) < 1100:
            # One second wait
            end = timer.SDL_GetTicks()
        # check for <=11, since it can happen that a last call is still
        # executing
        assert len(calls) <= 11
        timer.SDL_RemoveTimer(timerid)
        assert len(calls) <= 11
        timer.SDL_RemoveTimer(timerid)
        # Wait a bit, so the last executing handlers can finish
        timer.SDL_Delay(10)
