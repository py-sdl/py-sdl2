import sys
import os
import pytest
from ctypes import c_int, byref
import sdl2


def test_SDL_GetPowerInfo():
    has_battery = [
        sdl2.SDL_POWERSTATE_ON_BATTERY,
        sdl2.SDL_POWERSTATE_CHARGING,
        sdl2.SDL_POWERSTATE_CHARGED
    ]
    remaining, pct = c_int(), c_int()
    state = sdl2.SDL_GetPowerInfo(byref(remaining), byref(pct))
    if state in has_battery:
        assert pct.value <= 100
        assert pct.value > 0
    else:
        assert remaining.value == -1
        assert pct.value == -1
