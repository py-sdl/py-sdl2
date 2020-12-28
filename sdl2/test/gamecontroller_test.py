import sys
import pytest
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_GAMECONTROLLER
from sdl2 import gamecontroller, joystick


# TODO: Move tests that don't need GameController instance out of class
# TODO: Add support for actual device tests from joystick

# Make sure gamecontroller subsystem works before running tests
ret = SDL_Init(SDL_INIT_GAMECONTROLLER)
SDL_Quit()
skipmsg = 'Game controller subsystem not supported'
pytestmark = pytest.mark.skipif(ret != 0, reason=skipmsg)


class TestSDLGamecontroller(object):
    __tags__ = ["sdl"]

    def setup_method(self):
        SDL_Init(SDL_INIT_GAMECONTROLLER)

    def teardown_method(self):
        SDL_Quit()

    def test_SDL_GameControllerAddMapping(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        if sdl2.dll.version >= 2006:
            n1 = gamecontroller.SDL_GameControllerNumMappings()
            ret = gamecontroller.SDL_GameControllerAddMapping(newmap)
            assert ret != -1
            n2 = gamecontroller.SDL_GameControllerNumMappings()
            assert n2 == n1 + 1
        else:
            # NumMappings not available before 2.0.6
            ret = gamecontroller.SDL_GameControllerAddMapping(newmap)
            assert ret != -1

    def test_SDL_GameControllerMappingForGUID(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        ret = gamecontroller.SDL_GameControllerAddMapping(newmap)
        assert ret != 0
        # Get GUID for new mapping
        guid_str = newmap.split(b",")[0]
        guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
        # Get mapping for GUID
        retmap = gamecontroller.SDL_GameControllerMappingForGUID(guid)
        assert retmap == newmap

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerMapping(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_IsGameController(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerNameForIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_GameControllerTypeForIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerOpen(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerName(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_GameControllerGetType(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetAttached(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetJoystick(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerEventState(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerUpdate(self):
        pass

    def test_SDL_GameControllerGetAxisFromString(self):
        expected = {
            b'lefty': gamecontroller.SDL_CONTROLLER_AXIS_LEFTY,
            b'lefttrigger': gamecontroller.SDL_CONTROLLER_AXIS_TRIGGERLEFT,
            b'notanaxis': gamecontroller.SDL_CONTROLLER_AXIS_INVALID
        }
        for string in expected.keys():
            a = gamecontroller.SDL_GameControllerGetAxisFromString(string)
            assert a == expected[string]

    def test_SDL_GameControllerGetStringForAxis(self):
        expected = {
            gamecontroller.SDL_CONTROLLER_AXIS_LEFTY: b'lefty',
            gamecontroller.SDL_CONTROLLER_AXIS_TRIGGERLEFT: b'lefttrigger',
            gamecontroller.SDL_CONTROLLER_AXIS_INVALID: None
        }
        for axis in expected.keys():
            s = gamecontroller.SDL_GameControllerGetStringForAxis(axis)
            assert s == expected[axis]

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetBindForAxis(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerHasAxis(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetAxis(self):
        pass

    def test_SDL_GameControllerGetButtonFromString(self):
        expected = {
            b'x': gamecontroller.SDL_CONTROLLER_BUTTON_X,
            b'dpup': gamecontroller.SDL_CONTROLLER_BUTTON_DPAD_UP,
            b'notabutton': gamecontroller.SDL_CONTROLLER_BUTTON_INVALID
        }
        for string in expected.keys():
            b = gamecontroller.SDL_GameControllerGetButtonFromString(string)
            assert b == expected[string]

    def test_SDL_GameControllerGetStringForButton(self):
        expected = {
            gamecontroller.SDL_CONTROLLER_BUTTON_X: b'x',
            gamecontroller.SDL_CONTROLLER_BUTTON_DPAD_UP: b'dpup',
            gamecontroller.SDL_CONTROLLER_BUTTON_INVALID: None
        }
        for button in expected.keys():
            s = gamecontroller.SDL_GameControllerGetStringForButton(button)
            assert s == expected[button]

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetBindForButton(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerHasButton(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetButton(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerGetNumTouchpads(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerGetNumTouchpadFingers(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerGetTouchpadFinger(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerHasSensor(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerSetSensorEnabled(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerIsSensorEnabled(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerGetSensorData(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerClose(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerAddMappingsFromRW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerAddMappingsFromFile(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerFromInstanceID(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_GameControllerFromPlayerIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_GameControllerGetPlayerIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_GameControllerSetPlayerIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerGetVendor(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerGetProduct(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerGetProductVersion(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerGetSerial(self):
        pass

    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerNumMappings(self):
        num = gamecontroller.SDL_GameControllerNumMappings()
        assert num > 0

    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerMappingForIndex(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        ret = gamecontroller.SDL_GameControllerAddMapping(newmap)
        assert ret != 0
        num = gamecontroller.SDL_GameControllerNumMappings()
        retmap = gamecontroller.SDL_GameControllerMappingForIndex(num - 1)
        assert newmap == retmap

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_GameControllerMappingForDeviceIndex(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_GameControllerRumble(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerRumbleTriggers(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2014, reason="not available")
    def test_SDL_GameControllerHasSetLED(self):
        pass
