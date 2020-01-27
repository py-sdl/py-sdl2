import pytest
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_QuitSubSystem
from sdl2.error import SDL_GetError, SDL_ClearError
from sdl2 import touch


@pytest.fixture(scope="module", autouse=True)
def sdl_setup():
    SDL_Init(0)
    yield
    SDL_Quit()


def test_SDL_GetNumTouchDevices():
    assert touch.SDL_GetNumTouchDevices() >= 0


class TestSDLTouchDevice(object):

    # NOTE: these are currently untested due to lack of hardware
    
    @classmethod
    def setup_class(cls):
        num = touch.SDL_GetNumTouchDevices()
        if num < 1:
            pytest.skip("no available touch devices")
        cls.num_devices = num

    def setup_method(self):
        SDL_ClearError()

    def test_SDL_GetTouchDevice(self):
        for i in range(0, self.num_devices):
            dev_id = touch.SDL_GetTouchDevice(i)
            assert dev_id > 0

    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_GetTouchDeviceType(self):
        types = [
            touch.SDL_TOUCH_DEVICE_INVALID, touch.SDL_TOUCH_DEVICE_DIRECT,
            touch.SDL_TOUCH_DEVICE_INDIRECT_ABSOLUTE,
            touch.SDL_TOUCH_DEVICE_INDIRECT_RELATIVE
        ]
        for i in range(0, self.num_devices):
            dev_id = touch.SDL_GetTouchDevice(i)
            assert dev_id > 0
            dev_type = touch.SDL_GetTouchDeviceType(dev_id)
            assert dev_type in types

    def test_SDL_GetNumTouchFingers(self):
        for i in range(0, self.num_devices):
            dev_id = touch.SDL_GetTouchDevice(i)
            assert dev_id > 0
            fingers = touch.SDL_GetNumTouchFingers(dev_id)
            err = SDL_GetError()
            assert fingers > 0
            assert len(err) == 0

    def test_SDL_GetTouchFinger(self):
        for i in range(0, self.num_devices):
            dev_id = touch.SDL_GetTouchDevice(i)
            assert dev_id > 0
            fingers = touch.SDL_GetNumTouchFingers(dev_id)
            assert fingers > 0
            for f in range(0, fingers):
                finger = touch.SDL_GetTouchFinger(dev_id, f)
                assert isinstance(finger.contents, touch.SDL_Finger)
                