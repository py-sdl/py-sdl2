import sys
import unittest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_JOYSTICK
from sdl2 import gamecontroller


class SDLGamecontrollerTest(unittest.TestCase):
    __tags__ = ["sdl"]

    @classmethod
    def setUpClass(cls):
        SDL_Init(SDL_INIT_JOYSTICK)

    @classmethod
    def tearDownClass(cls):
        SDL_Quit()

    @unittest.skip("not implemented")
    def test_SDL_GameControllerAddMapping(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerMappingForGUID(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerMapping(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_IsGameController(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerNameForIndex(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerOpen(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerName(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetAttached(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetJoystick(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerEventState(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerUpdate(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetAxisFromString(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetStringForAxis(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetBindForAxis(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetAxis(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetButtonFromString(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetStringForButton(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetBindForButton(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetButton(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerClose(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerAddMappingsFromRW(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerAddMappingsFromFile(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerFromInstanceID(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetVendor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetProduct(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerGetProductVersion(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerNumMappings(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GameControllerMappingForIndex(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
