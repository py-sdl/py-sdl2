import unittest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import vulkan

class SDLVulkanTest(unittest.TestCase):
    __tags__ = ["sdl"]

    @classmethod
    def setUpClass(cls):
        SDL_Init(SDL_INIT_VIDEO)

    @classmethod
    def tearDownClass(cls):
        SDL_Quit()

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_LoadLibrary(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_GetVkGetInstanceProcAddr(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_UnloadLibrary(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_GetInstanceExtensions(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_CreateSurface(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_Vulkan_GetDrawableSize(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
