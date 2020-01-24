import sys
import pytest
from ctypes import create_string_buffer
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_JOYSTICK
from sdl2.events import SDL_QUERY, SDL_ENABLE, SDL_IGNORE
from sdl2 import joystick


class TestSDLJoystick(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_JOYSTICK) != 0:
            raise pytest.skip('Joystick subsystem not supported')
        cls.jcount = joystick.SDL_NumJoysticks()

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def test_SDL_NumJoysticks(self):
        retval = joystick.SDL_NumJoysticks()
        assert retval >= 0

    def test_SDL_JoystickNameForIndex(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            name = joystick.SDL_JoystickNameForIndex(index)
            assert type(name) in (str, bytes)

    def test_SDL_JoystickOpen(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            joystick.SDL_JoystickClose(stick)

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickName(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceGUID(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetGUID(self):
        pass

    def test_SDL_JoystickGetGUIDFromString(self):
        guid_str = b'030000007e050000060300001c3a0000' # Wiimote on macOS
        expected = [3, 0, 0, 0, 126, 5, 0, 0, 6, 3, 0, 0, 28, 58, 0, 0]
        guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
        assert list(guid.data) == expected

    def test_SDL_JoystickGetGUIDString(self):
        guid_str = b'030000007e050000060300001c3a0000' # Wiimote on macOS
        guid = joystick.SDL_JoystickGetGUIDFromString(guid_str)
        buff = create_string_buffer(33)
        joystick.SDL_JoystickGetGUIDString(guid, buff, 33) # Get GUID string
        assert guid_str == buff.value

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetAttached(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickInstanceID(self):
        pass

    def test_SDL_JoystickNumAxes(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            axes = joystick.SDL_JoystickNumAxes(stick)
            assert axes >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumBalls(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            balls = joystick.SDL_JoystickNumBalls(stick)
            assert balls >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumHats(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            hats = joystick.SDL_JoystickNumHats(stick)
            assert hats >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumButtons(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            assert isinstance(stick.contents, joystick.SDL_Joystick)
            buttons = joystick.SDL_JoystickNumButtons(stick)
            assert buttons >= 0
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickUpdate(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        joystick.SDL_JoystickUpdate()

    def test_SDL_JoystickEventState(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for state in(SDL_IGNORE, SDL_ENABLE):
            news = joystick.SDL_JoystickEventState(state)
            assert news == state
            query = joystick.SDL_JoystickEventState(SDL_QUERY)
            assert query == state

    def test_SDL_JoystickGetAxis(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for axis in range(joystick.SDL_JoystickNumAxes(stick)):
                val = joystick.SDL_JoystickGetAxis(stick, axis)
                assert -32768 <= val <= 32767
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetBall(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for ball in range(joystick.SDL_JoystickNumBalls(stick)):
                dx, dy = joystick.SDL_JoystickGetBall(stick, ball)
                assert isinstance(dx, int)
                assert isinstance(dy, int)
                # TODO
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetHat(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for hat in range(joystick.SDL_JoystickNumHats(stick)):
                val = joystick.SDL_JoystickGetHat(stick, hat)
                assert isinstance(val, int)
                # TODO
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetButton(self):
        if self.jcount == 0:
            pytest.skip("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for button in range(joystick.SDL_JoystickNumButtons(stick)):
                val = joystick.SDL_JoystickGetButton(stick, button)
                # TODO: x
                # self.assertIsInstance(val, bool)
            joystick.SDL_JoystickClose(stick)

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickClose(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickCurrentPowerLevel(self):
        pass

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

    @pytest.mark.skip("not implemented")
    def test_SDL_JoystickGetDeviceInstanceID(self):
        pass
