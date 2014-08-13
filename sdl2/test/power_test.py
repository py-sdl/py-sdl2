import sys
import os
import unittest
from ctypes import c_int, byref
from .. import power
from .util.testutils import interactive, doprint


class SDLPowerTest(unittest.TestCase):
    __tags__ = ["sdl"]

    @interactive("Do the shown numbers match your power supply status?")
    def test_get_power_info(self):
        secs, percent = c_int(), c_int()
        retval = power.SDL_GetPowerInfo(byref(secs), byref(percent))
        state = "Unknown"
        if retval == power.SDL_POWERSTATE_ON_BATTERY:
            state = "On battery"
        elif retval == power.SDL_POWERSTATE_NO_BATTERY:
            state = "No battery"
        elif retval == power.SDL_POWERSTATE_CHARGING:
            state = "Battery charging"
        elif retval == power.SDL_POWERSTATE_CHARGED:
            state = "Battery charged"
        output = "Power Status: %s" % state + os.linesep
        output += "Minutes left (-1 = undetermined): %d" % (secs.value / 60)
        output += os.linesep
        output += "Percent left (-1 = undetermined): %d" % percent.value
        output += os.linesep
        doprint(output)


if __name__ == '__main__':
    sys.exit(unittest.main())
