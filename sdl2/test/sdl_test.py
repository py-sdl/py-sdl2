import sys
import pytest
from sdl2 import SDL_Init, SDL_WasInit, SDL_InitSubSystem, SDL_QuitSubSystem, \
    SDL_Quit, SDL_INIT_AUDIO, SDL_INIT_EVERYTHING, SDL_INIT_GAMECONTROLLER, \
    SDL_INIT_HAPTIC, SDL_INIT_JOYSTICK, SDL_INIT_NOPARACHUTE, SDL_INIT_TIMER, \
    SDL_INIT_VIDEO, SDL_GetError


class TestSDL(object):
    __tags__ = ["sdl"]

    def setup_method(self):
        SDL_Init(0)

    def teardown_method(self):
        SDL_Quit()

    def test_SDL_INIT_TIMER(self):
        ret = SDL_Init(SDL_INIT_TIMER)
        if ret != 0:
            pytest.skip('Timer subsystem not supported')
        ret = SDL_WasInit(SDL_INIT_TIMER)
        assert ret == SDL_INIT_TIMER
        SDL_QuitSubSystem(SDL_INIT_TIMER)

    def test_SDL_INIT_AUDIO(self):
        ret = SDL_Init(SDL_INIT_AUDIO)
        if ret != 0:
            pytest.skip('Audio subsystem not supported')
        ret = SDL_WasInit(SDL_INIT_AUDIO)
        assert ret == SDL_INIT_AUDIO
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_INIT_VIDEO(self):
        ret = SDL_Init(SDL_INIT_VIDEO)
        if ret != 0:
            pytest.skip('Video subsystem not supported')
        ret = SDL_WasInit(SDL_INIT_VIDEO)
        assert ret == SDL_INIT_VIDEO
        SDL_QuitSubSystem(SDL_INIT_VIDEO)

    def test_SDL_INIT_JOYSTICK(self):
        ret = SDL_Init(SDL_INIT_JOYSTICK)
        if ret != 0:
            pytest.skip('Joystick subsystem not supported')
        ret = SDL_WasInit(SDL_INIT_JOYSTICK)
        assert ret == SDL_INIT_JOYSTICK
        SDL_QuitSubSystem(SDL_INIT_JOYSTICK)

    @pytest.mark.skipif(sys.platform.startswith("freebsd"),
        reason="FreeBSD des not support haptic input yet")
    def test_SDL_INIT_HAPTIC(self):
        ret = SDL_Init(SDL_INIT_HAPTIC)
        if ret != 0:
            pytest.skip('Haptic subsystem not supported')
        ret = SDL_WasInit(SDL_INIT_HAPTIC)
        assert ret == SDL_INIT_HAPTIC
        SDL_QuitSubSystem(SDL_INIT_HAPTIC)
