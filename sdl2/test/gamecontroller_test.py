import sys
import pytest
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_FALSE, SDL_TRUE
from sdl2 import joystick
from sdl2 import gamecontroller as gamepad


# TODO: Move tests that don't need GameController instance out of class
# TODO: Add support for actual device tests from joystick

# Make sure gamecontroller subsystem works before running tests
ret = SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)
SDL_Quit()
skipmsg = 'Game controller subsystem not supported'
pytestmark = pytest.mark.skipif(ret != 0, reason=skipmsg)

# Test if SDL_GameControllerMappingForGUID is able to be tested
if sys.version_info >= (3, 8, 0) or sdl2.dll.version >= 2006:
    has_mapping_for_guid = True
else:
    has_mapping_for_guid = False


class TestSDLGamecontroller(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(sdl2.SDL_INIT_GAMECONTROLLER)
        num = joystick.SDL_NumJoysticks()
        if num < 1:
            pytest.skip("no available joystick devices")
        gamepad_ids = []
        for i in range(num):
            if gamepad.SDL_IsGameController(i) == SDL_TRUE:
                gamepad_ids.append(i)
        cls.gamepad_ids = gamepad_ids

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def setup_method(self):
        sdl2.SDL_ClearError()

    def test_SDL_GameControllerAddMapping(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        if sdl2.dll.version >= 2006:
            n1 = gamepad.SDL_GameControllerNumMappings()
            ret = gamepad.SDL_GameControllerAddMapping(newmap)
            assert ret >= 0
            n2 = gamepad.SDL_GameControllerNumMappings()
            assert n2 == n1 + 1
        else:
            # NumMappings not available before 2.0.6
            ret = gamepad.SDL_GameControllerAddMapping(newmap)
            assert ret != -1

    @pytest.mark.skipif(not has_mapping_for_guid, reason="not available")
    def test_SDL_GameControllerMappingForGUID(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        ret = gamepad.SDL_GameControllerAddMapping(newmap)
        assert ret >= 0
        # Get GUID for new mapping
        guid_str = newmap.split(b",")[0]
        guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
        # Get mapping for GUID
        retmap = gamepad.SDL_GameControllerMappingForGUID(guid)
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
            b'lefty': gamepad.SDL_CONTROLLER_AXIS_LEFTY,
            b'lefttrigger': gamepad.SDL_CONTROLLER_AXIS_TRIGGERLEFT,
            b'notanaxis': gamepad.SDL_CONTROLLER_AXIS_INVALID
        }
        for string in expected.keys():
            a = gamepad.SDL_GameControllerGetAxisFromString(string)
            assert a == expected[string]

    def test_SDL_GameControllerGetStringForAxis(self):
        expected = {
            gamepad.SDL_CONTROLLER_AXIS_LEFTY: b'lefty',
            gamepad.SDL_CONTROLLER_AXIS_TRIGGERLEFT: b'lefttrigger',
            gamepad.SDL_CONTROLLER_AXIS_INVALID: None
        }
        for axis in expected.keys():
            s = gamepad.SDL_GameControllerGetStringForAxis(axis)
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
            b'x': gamepad.SDL_CONTROLLER_BUTTON_X,
            b'dpup': gamepad.SDL_CONTROLLER_BUTTON_DPAD_UP,
            b'notabutton': gamepad.SDL_CONTROLLER_BUTTON_INVALID
        }
        for string in expected.keys():
            b = gamepad.SDL_GameControllerGetButtonFromString(string)
            assert b == expected[string]

    def test_SDL_GameControllerGetStringForButton(self):
        expected = {
            gamepad.SDL_CONTROLLER_BUTTON_X: b'x',
            gamepad.SDL_CONTROLLER_BUTTON_DPAD_UP: b'dpup',
            gamepad.SDL_CONTROLLER_BUTTON_INVALID: None
        }
        for button in expected.keys():
            s = gamepad.SDL_GameControllerGetStringForButton(button)
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
    @pytest.mark.skipif(sdl2.dll.version < 2016, reason="not available")
    def test_SDL_GameControllerGetSensorDataRate(self):
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
        num = gamepad.SDL_GameControllerNumMappings()
        assert num > 0

    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_GameControllerMappingForIndex(self):
        newmap = (
            b"030000005e0400002700000006010000,Microsoft SideWinder,"
            b"platform:Mac OS X,a:b0,b:b1,x:b2,y:b3,dpup:-a1,dpdown:+a1,"
            b"dpleft:-a0,dpright:+a0,lefttrigger:b4,righttrigger:b5"
        )
        ret = gamepad.SDL_GameControllerAddMapping(newmap)
        assert ret != 0
        num = gamepad.SDL_GameControllerNumMappings()
        retmap = gamepad.SDL_GameControllerMappingForIndex(num - 1)
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

    @pytest.mark.skipif(sdl2.dll.version < 2018, reason="not available")
    def test_SDL_GameControllerHasRumble(self):
        # If we ever add an interactive test suite, this should be moved there
        for index in self.gamepad_ids:
            pad = gamepad.SDL_GameControllerOpen(index)
            has_rumble = gamepad.SDL_GameControllerHasRumble(pad)
            assert has_rumble in [SDL_FALSE, SDL_TRUE]
            joystick.SDL_JoystickClose(pad)

    @pytest.mark.skipif(sdl2.dll.version < 2018, reason="not available")
    def test_SDL_GameControllerHasRumbleTriggers(self):
        # If we ever add an interactive test suite, this should be moved there
        for index in self.gamepad_ids:
            pad = gamepad.SDL_GameControllerOpen(index)
            has_rumble_triggers = gamepad.SDL_GameControllerHasRumbleTriggers(pad)
            assert has_rumble_triggers in [SDL_FALSE, SDL_TRUE]
            gamepad.SDL_GameControllerClose(pad)

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2016, reason="not available")
    def test_SDL_GameControllerSendEffect(self):
        # Probably impossible to test since effect data would be specific
        # to each controller type?
        pass

    @pytest.mark.skip("Only relevant on iOS, not testable by PySDL2")
    @pytest.mark.skipif(sdl2.dll.version < 2018, reason="not available")
    def test_SDL_GameControllerGetAppleSFSymbolsNameForButtonAxis(self):
        # The following two functions are deliberatly ignored:
        # - SDL_GameControllerGetAppleSFSymbolsNameForButton
        # - SDL_GameControllerGetAppleSFSymbolsNameForAxis
        pass
