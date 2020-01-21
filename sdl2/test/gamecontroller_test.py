import sys
import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_JOYSTICK
from sdl2 import gamecontroller


class TestSDLGamecontroller(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_JOYSTICK) != 0:
            raise pytest.skip('Joystick subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerAddMapping(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerMappingForGUID(self):
        pass

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
    def test_SDL_GameControllerOpen(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerName(self):
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

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetAxisFromString(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetStringForAxis(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetBindForAxis(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetAxis(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetButtonFromString(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetStringForButton(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetBindForButton(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetButton(self):
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
    def test_SDL_GameControllerGetVendor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetProduct(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerGetProductVersion(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerNumMappings(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GameControllerMappingForIndex(self):
        pass
