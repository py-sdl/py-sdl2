import sys
import pytest
from sdl2 import ext as sdl2ext
from sdl2 import surface, video


class TestSDL2ExtWindow(object):
    __tags__ = ["sdl", "sdl2ext"]

    @classmethod
    def setup_class(cls):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        sdl2ext.quit()

    def test_Window(self):
        flags = video.SDL_WINDOW_BORDERLESS
        sizes = ((1, 1), (10, 10), (10, 20), (200, 17), (640, 480), (800, 600))
        for w, h in sizes:
            window = sdl2ext.Window("Window", size=(w, h), flags=flags)
            assert window.size == (w, h)
            window.close()

        with pytest.raises(TypeError):
            sdl2ext.Window("Test", None, None, None)
        with pytest.raises(TypeError):
            sdl2ext.Window("Test", None, None)
        with pytest.raises(TypeError):
            sdl2ext.Window("Test", None)


    def test_Window_title(self):
        window = sdl2ext.Window("Window", size=(10, 10))
        assert window.title == "Window"
        window.title = "Test1234"
        assert window.title == "Test1234"
        window.close()

        #window.title = None
        #self.assertEqual(window.title, "None")
        #window.title = 1234
        #self.assertEqual(window.title, "1234")

#     @interactive("Was the window shown?")
#     def test_Window_show(self):
#         window = sdl2ext.Window("Test Show Window", size=(200, 200))
#         window.show()
#         doprint("""Please check, if a window with the title
# 'Test Show Window' is shown""")

#     @interactive("Did the window vanish from your sight and pop up again?")
#     def test_Window_hide(self):
#         window = sdl2ext.Window("Test Hide Window", size=(200, 200))
#         window.show()
#         doprint("""Please check, if a window with the title
# 'Test Hide Window' is shown""")
#         window.hide()
#         doprint("Please check, that the window is not shown anymore")
#         window.show()
#         doprint("Please check, if the window is shown again")

#     @interactive("Was the window maximized?")
#     def test_Window_maximize(self):
#         window = sdl2ext.Window("Test Maximize Window", size=(200, 200),
#                                 flags=video.SDL_WINDOW_RESIZABLE)
#         window.show()
#         doprint("""Please check, that a window with the title
# 'Test Maximize Window' is shown""")
#         window.maximize()
#         doprint("Please check, if the window was maximized properly")

#     @interactive("Was the window minimized?")
#     def test_Window_minimize(self):
#         window = sdl2ext.Window("Test Minimize Window", size=(200, 200))
#         window.show()
#         doprint("""Please check, that a window with the title
# 'Test Minimize Window' is shown""")
#         window.minimize()
#         doprint("Please check, if the window was minimized properly")

    @pytest.mark.skip("not implemented")
    def test_Window_refresh(self):
        pass

    def test_Window_get_surface(self):
        window = sdl2ext.Window("Surface", size=(200, 200))
        sf = window.get_surface()
        assert isinstance(sf, surface.SDL_Surface)
        window.close()

    @pytest.mark.skip("not implemented")
    def test_Window_open(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Window_close(self):
        pass

    def test_Window_position(self):
        window = sdl2ext.Window("Position", size=(200, 200), position=(100, 100))
        assert window.position == (100, 100)
        window.position = 70, 300
        assert window.position == (70, 300)
        window.close()

    @pytest.mark.skip("not implemented")
    def test_Window_size(self):
        # This may fail for fullscreen WMs or Win10 tablet modes
        window = sdl2ext.Window("Size", size=(200, 200), flags=video.SDL_WINDOW_RESIZABLE)
        assert window.size == (200, 200)
        window.size = 150, 77
        assert window.size == (150, 77)
        window.close()
