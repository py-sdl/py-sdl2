import pytest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_VIDEO
from sdl2 import vulkan

class TestSDLVulkan(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        if SDL_Init(SDL_INIT_VIDEO) != 0:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_LoadLibrary(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_GetVkGetInstanceProcAddr(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_UnloadLibrary(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_GetInstanceExtensions(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_CreateSurface(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_Vulkan_GetDrawableSize(self):
        pass
