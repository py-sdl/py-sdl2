import sys
import pytest
from ctypes import create_string_buffer, byref, c_int
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_JOYSTICK
from sdl2.events import SDL_QUERY, SDL_ENABLE, SDL_IGNORE
from sdl2.stdinc import SDL_TRUE, SDL_FALSE
from sdl2.error import SDL_GetError, SDL_ClearError
from sdl2 import joystick


def test_SDL_JoystickGetGUIDFromString():
    guid_str = b'030000007e050000060300001c3a0000' # Wiimote on macOS
    expected = [3, 0, 0, 0, 126, 5, 0, 0, 6, 3, 0, 0, 28, 58, 0, 0]
    guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
    assert list(guid.data) == expected

def test_SDL_JoystickGetGUIDString():
    guid_str = b'030000007e050000060300001c3a0000' # Wiimote on macOS
    guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
    buff = create_string_buffer(33)
    joystick.SDL_JoystickGetGUIDString(guid, buff, 33) # Get GUID string
    assert guid_str == buff.value

def test_SDL_InitJoystick():
    ret = SDL_Init(SDL_INIT_JOYSTICK)
    SDL_Quit()
    assert ret == 0

def test_SDL_NumJoysticks():
    if SDL_Init(SDL_INIT_JOYSTICK) != 0:
        pytest.skip("joystick subsystem not supported")
    retval = joystick.SDL_NumJoysticks()
    SDL_Quit()
    assert retval >= 0


skipmsg = "joystick subsystem not supported"
@pytest.mark.skipif(SDL_Init(SDL_INIT_JOYSTICK) != 0, reason=skipmsg)
class TestSDLJoystick(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(SDL_INIT_JOYSTICK)
        num = joystick.SDL_NumJoysticks()
        if num < 1:
            pytest.skip("no available joystick devices")
        cls.jcount = num

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def setup_method(self):
        SDL_ClearError()

    def test_SDL_JoystickNameForIndex(self):
        for index in range(self.jcount):
            name = joystick.SDL_JoystickNameForIndex(index)
            assert type(name) in (str, bytes)

    def test_SDL_JoystickOpenClose(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickName(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            name = joystick.SDL_JoystickName(stick)
            assert type(name) in (str, bytes)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetDeviceGUID(self):
        for index in range(self.jcount):
            guid = joystick.SDL_JoystickGetDeviceGUID(index)
            assert isinstance(guid, joystick.SDL_JoystickGUID)
            guidlist = list(guid.data)
            assert isinstance(guidlist[0], int)

    def test_SDL_JoystickGetGUID(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            guid = joystick.SDL_JoystickGetGUID(stick)
            assert isinstance(guid, joystick.SDL_JoystickGUID)
            guidlist = list(guid.data)
            assert isinstance(guidlist[0], int)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetAttached(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            ret = joystick.SDL_JoystickGetAttached(stick)
            assert ret in [SDL_FALSE, SDL_TRUE]
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickInstanceID(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            ret = joystick.SDL_JoystickInstanceID(stick)
            assert ret > 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumAxes(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            axes = joystick.SDL_JoystickNumAxes(stick)
            assert axes >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumBalls(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            balls = joystick.SDL_JoystickNumBalls(stick)
            assert balls >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumHats(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            hats = joystick.SDL_JoystickNumHats(stick)
            assert hats >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumButtons(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            buttons = joystick.SDL_JoystickNumButtons(stick)
            assert buttons >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickUpdate(self):
        # returns void, not sure what else to test here
        joystick.SDL_JoystickUpdate()

    def test_SDL_JoystickEventState(self):
        for state in (SDL_IGNORE, SDL_ENABLE):
            news = joystick.SDL_JoystickEventState(state)
            assert news == state
            query = joystick.SDL_JoystickEventState(SDL_QUERY)
            assert query == state

    def test_SDL_JoystickGetAxis(self):
        sticks = [joystick.SDL_JoystickOpen(i) for i in range(self.jcount)]
        numaxes = [joystick.SDL_JoystickNumAxes(s) for s in sticks]
        if not any(numaxes):
            pytest.skip("no axis on any connected controller")
        for stick in sticks:
            for axis in range(joystick.SDL_JoystickNumAxes(stick)):
                val = joystick.SDL_JoystickGetAxis(stick, axis)
                assert -32768 <= val <= 32767
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetBall(self):
        sticks = [joystick.SDL_JoystickOpen(i) for i in range(self.jcount)]
        numball = [joystick.SDL_JoystickNumBalls(s) for s in sticks]
        if not any(numball):
            pytest.skip("no trackball on any connected controller")
        dx, dy = c_int(0), c_int(0)
        get_ball = joystick.SDL_JoystickGetBall
        for stick in sticks:
            for ball in range(joystick.SDL_JoystickNumBalls(stick)):
                ret = get_ball(stick, ball, byref(dx), byref(dy))
                err = SDL_GetError()
                assert ret == 0
                assert len(err) == 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetHat(self):
        hatvals = [
            joystick.SDL_HAT_UP, joystick.SDL_HAT_DOWN, joystick.SDL_HAT_LEFT,
            joystick.SDL_HAT_RIGHT, joystick.SDL_HAT_CENTERED,
            joystick.SDL_HAT_LEFTUP, joystick.SDL_HAT_LEFTDOWN,
            joystick.SDL_HAT_RIGHTUP, joystick.SDL_HAT_RIGHTDOWN
        ]
        sticks = [joystick.SDL_JoystickOpen(i) for i in range(self.jcount)]
        numhats = [joystick.SDL_JoystickNumHats(s) for s in sticks]
        if not any(numhats):
            pytest.skip("no POV hat on any connected controller")
        for stick in sticks:
            for hat in range(joystick.SDL_JoystickNumHats(stick)):
                val = joystick.SDL_JoystickGetHat(stick, hat)
                assert val in hatvals
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetButton(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for button in range(joystick.SDL_JoystickNumButtons(stick)):
                val = joystick.SDL_JoystickGetButton(stick, button)
                assert val in [0, 1]
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickCurrentPowerLevel(self):
        levels = [
            joystick.SDL_JOYSTICK_POWER_UNKNOWN,
            joystick.SDL_JOYSTICK_POWER_EMPTY,
            joystick.SDL_JOYSTICK_POWER_LOW,
            joystick.SDL_JOYSTICK_POWER_MEDIUM,
            joystick.SDL_JOYSTICK_POWER_FULL,
            joystick.SDL_JOYSTICK_POWER_WIRED,
            joystick.SDL_JOYSTICK_POWER_MAX,
        ]
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            pwr = joystick.SDL_JoystickCurrentPowerLevel(stick)
            err = SDL_GetError()
            assert pwr in levels
            assert len(err) == 0
            joystick.SDL_JoystickClose(stick)

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickFromInstanceID(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetVendor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetProduct(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetProductVersion(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetAxisInitialState(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetType(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceVendor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceProduct(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceProductVersion(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceType(self):
        pass

    @pytest.mark.skipif(sdl2.dll.version < 2006, reason="not available")
    def test_SDL_JoystickGetDeviceInstanceID(self):
        for index in range(self.jcount):
            ret = joystick.SDL_JoystickGetDeviceInstanceID(index)
            assert ret > 0

    @pytest.mark.skipif(sdl2.dll.version < 2007, reason="not available")
    def test_SDL_LockUnlockJoysticks(self):
        # NOTE: not sure how better to test these, since I don't know if
        # they'd even be useful at all in Python given the GIL
        joystick.SDL_LockJoysticks()
        joystick.SDL_UnlockJoysticks()

    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_JoystickGetPlayerIndex(self):
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            player = joystick.SDL_JoystickGetPlayerIndex(stick)
            assert player in [-1, 0, 1, 2, 3]
            joystick.SDL_JoystickClose(stick)

    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_JoystickGetDevicePlayerIndex(self):
        for index in range(self.jcount):
            player = joystick.SDL_JoystickGetDevicePlayerIndex(index)
            assert player in [-1, 0, 1, 2, 3]

    @pytest.mark.skipif(sdl2.dll.version < 2009, reason="not available")
    def test_SDL_JoystickRumble(self):
        # If we ever add an interactive test suite, this should be moved there
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            # 50% strength low-frequency, 25% high-frequency rumble for 500ms
            ret = joystick.SDL_JoystickRumble(stick, 32767, 16384, 500)
            assert ret in [-1, 0]
            joystick.SDL_JoystickClose(stick)
