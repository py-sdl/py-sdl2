import sys
from ctypes.util import find_library
from ctypes import c_int, c_float, byref, cast, POINTER, py_object
import unittest
from .util.testutils import interactive, doprint
from ..stdinc import SDL_FALSE, SDL_TRUE
from .. import video, rect, surface

if sys.version_info[0] >= 3:
    long = int

to_ctypes = lambda seq, dtype: (dtype * len(seq))(*seq)


def has_opengl_lib():
    for libname in("gl", "opengl", "opengl32"):
        path = find_library(libname)
        if path is not None:
            return True


def get_opengl_path():
    for libname in("gl", "opengl", "opengl32"):
        path = find_library(libname)
        if path is not None:
            return path


# TODO: mostly covers positive tests right now - fix this!
class SDLVideoTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        video.SDL_VideoInit(None)

    def tearDown(self):
        video.SDL_VideoQuit()

    def test_SDL_WINDOWPOS_UNDEFINED_DISPLAY(self):
        for x in range(0xFFFF):
            self.assertEqual(video.SDL_WINDOWPOS_UNDEFINED_MASK | x,
                             video.SDL_WINDOWPOS_UNDEFINED_DISPLAY(x))
            self.assertEqual((video.SDL_WINDOWPOS_UNDEFINED_DISPLAY(x) &
                              video.SDL_WINDOWPOS_UNDEFINED_MASK),
                             video.SDL_WINDOWPOS_UNDEFINED_MASK)
            self.assertTrue(video.SDL_WINDOWPOS_UNDEFINED_DISPLAY(x) !=
                            video.SDL_WINDOWPOS_CENTERED_DISPLAY(x))

    def test_SDL_WINDOWPOS_ISUNDEFINED(self):
        self.assertTrue(video.SDL_WINDOWPOS_ISUNDEFINED
                        (video.SDL_WINDOWPOS_UNDEFINED))
        self.assertFalse(video.SDL_WINDOWPOS_ISUNDEFINED
                         (video.SDL_WINDOWPOS_CENTERED))
        for x in range(0xFFFF):
            self.assertTrue(video.SDL_WINDOWPOS_ISUNDEFINED
                            (video.SDL_WINDOWPOS_UNDEFINED_DISPLAY(x)))

    def test_SDL_WINDOWPOS_CENTERED_DISPLAY(self):
        for x in range(0xFFFF):
            self.assertEqual(video.SDL_WINDOWPOS_CENTERED_MASK | x,
                             video.SDL_WINDOWPOS_CENTERED_DISPLAY(x))
            self.assertEqual((video.SDL_WINDOWPOS_CENTERED_DISPLAY(x) &
                              video.SDL_WINDOWPOS_CENTERED_MASK),
                             video.SDL_WINDOWPOS_CENTERED_MASK)
            self.assertTrue(video.SDL_WINDOWPOS_CENTERED_DISPLAY(x) !=
                            video.SDL_WINDOWPOS_UNDEFINED_DISPLAY(x))

    def test_SDL_WINDOWPOS_ISCENTERED(self):
        self.assertTrue(video.SDL_WINDOWPOS_ISCENTERED
                        (video.SDL_WINDOWPOS_CENTERED))
        self.assertFalse(video.SDL_WINDOWPOS_ISCENTERED
                         (video.SDL_WINDOWPOS_UNDEFINED))
        for x in range(0xFFFF):
            self.assertTrue(video.SDL_WINDOWPOS_ISCENTERED
                            (video.SDL_WINDOWPOS_CENTERED_DISPLAY(x)))

    def test_SDL_DisplayMode(self):
        mode = video.SDL_DisplayMode()
        self.assertIsInstance(mode, video.SDL_DisplayMode)
        for fmt in range(0, 10):
            for w in range(0, 20):
                for h in range(0, 30):
                    for r in range(0, 40):
                        mode = video.SDL_DisplayMode(fmt, w, h, r)
                        self.assertIsInstance(mode, video.SDL_DisplayMode)
                        self.assertEqual(mode.format, fmt)
                        self.assertEqual(mode.w, w)
                        self.assertEqual(mode.h, h)
                        self.assertEqual(mode.refresh_rate, r)
        self.assertRaises(TypeError, video.SDL_DisplayMode, "Test")
        self.assertRaises(TypeError, video.SDL_DisplayMode, "Test", 10, 10, 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, "Test", 10, 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, 10, "Test", 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, 10, 10, "Test")
        self.assertRaises(TypeError, video.SDL_DisplayMode, None)
        self.assertRaises(TypeError, video.SDL_DisplayMode, None, 10, 10, 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, None, 10, 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, 10, None, 10)
        self.assertRaises(TypeError, video.SDL_DisplayMode, 10, 10, 10, None)

    def test_SDL_DisplayMode__eq__(self):
        DMode = video.SDL_DisplayMode
        self.assertTrue(DMode() == DMode())
        self.assertTrue(DMode(10, 0, 0, 0) == DMode(10, 0, 0, 0))
        self.assertTrue(DMode(10, 10, 0, 0) == DMode(10, 10, 0, 0))
        self.assertTrue(DMode(10, 10, 10, 0) == DMode(10, 10, 10, 0))
        self.assertTrue(DMode(10, 10, 10, 10) == DMode(10, 10, 10, 10))
        self.assertTrue(DMode(0, 10, 0, 0) == DMode(0, 10, 0, 0))
        self.assertTrue(DMode(0, 0, 10, 0) == DMode(0, 0, 10, 0))
        self.assertTrue(DMode(0, 0, 0, 10) == DMode(0, 0, 0, 10))

        self.assertFalse(DMode() == DMode(10, 0, 0, 0))
        self.assertFalse(DMode(10, 0, 0, 0) == DMode(0, 0, 0, 0))
        self.assertFalse(DMode(10, 0, 0, 0) == DMode(0, 10, 0, 0))
        self.assertFalse(DMode(10, 0, 0, 0) == DMode(0, 0, 10, 0))
        self.assertFalse(DMode(10, 0, 0, 0) == DMode(0, 0, 0, 10))

    def test_SDL_DisplayMode__ne__(self):
        DMode = video.SDL_DisplayMode
        self.assertFalse(DMode() != DMode())
        self.assertFalse(DMode(10, 0, 0, 0) != DMode(10, 0, 0, 0))
        self.assertFalse(DMode(10, 10, 0, 0) != DMode(10, 10, 0, 0))
        self.assertFalse(DMode(10, 10, 10, 0) != DMode(10, 10, 10, 0))
        self.assertFalse(DMode(10, 10, 10, 10) != DMode(10, 10, 10, 10))
        self.assertFalse(DMode(0, 10, 0, 0) != DMode(0, 10, 0, 0))
        self.assertFalse(DMode(0, 0, 10, 0) != DMode(0, 0, 10, 0))
        self.assertFalse(DMode(0, 0, 0, 10) != DMode(0, 0, 0, 10))

        self.assertTrue(DMode() != DMode(10, 0, 0, 0))
        self.assertTrue(DMode(10, 0, 0, 0) != DMode(0, 0, 0, 0))
        self.assertTrue(DMode(10, 0, 0, 0) != DMode(0, 10, 0, 0))
        self.assertTrue(DMode(10, 0, 0, 0) != DMode(0, 0, 10, 0))
        self.assertTrue(DMode(10, 0, 0, 0) != DMode(0, 0, 0, 10))

    def test_SDL_Window(self):
        window = video.SDL_Window()
        self.assertIsInstance(window, video.SDL_Window)

    def test_SDL_GetNumVideoDrivers(self):
        numdrivers = video.SDL_GetNumVideoDrivers()
        self.assertGreaterEqual(numdrivers, 1)

    def test_SDL_GetVideoDriver(self):
        numdrivers = video.SDL_GetNumVideoDrivers()
        for i in range(numdrivers):
            name = video.SDL_GetVideoDriver(i)
            self.assertIn(type(name), (str, bytes))

    def test_SDL_GetCurrentVideoDriver(self):
        curdriver = video.SDL_GetCurrentVideoDriver()
        found = False
        numdrivers = video.SDL_GetNumVideoDrivers()
        for i in range(numdrivers):
            name = video.SDL_GetVideoDriver(i)
            if name == curdriver:
                found = True
                break
        self.assertTrue(found, "Current video driver not found")

    def test_SDL_GetNumVideoDisplays(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        self.assertGreaterEqual(numdisplays, 1)

    def test_SDL_GetNumDisplayModes(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            modes = video.SDL_GetNumDisplayModes(index)
            self.assertGreaterEqual(modes, 1)

    def test_SDL_GetDisplayMode(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            modes = video.SDL_GetNumDisplayModes(index)
            for mode in range(modes):
                dmode = video.SDL_DisplayMode()
                ret = video.SDL_GetDisplayMode(index, mode, byref(dmode))
                self.assertEqual(ret, 0)

    def test_SDL_GetCurrentDisplayMode(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            dmode = video.SDL_DisplayMode()
            ret = video.SDL_GetCurrentDisplayMode(index, byref(dmode))
            self.assertEqual(ret, 0)

    def test_SDL_GetDesktopDisplayMode(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            dmode = video.SDL_DisplayMode()
            ret = video.SDL_GetDesktopDisplayMode(index, byref(dmode))
            self.assertEqual(ret, 0)

    def test_SDL_GetClosestDisplayMode(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            modes = video.SDL_GetNumDisplayModes(index)
            dmode = video.SDL_DisplayMode()
            for mode in range(modes):
                ret = video.SDL_GetDisplayMode(index, mode, byref(dmode))
                #self.assertIsInstance(dmode.contents, video.SDL_DisplayMode)
                self.assertEqual(ret, 0)
                cmode = video.SDL_DisplayMode(dmode.format,
                                              dmode.w - 1, dmode.h - 1,
                                              dmode.refresh_rate)
                closest = video.SDL_DisplayMode()
                video.SDL_GetClosestDisplayMode(index, cmode, byref(closest))
                self.assertEqual(closest, dmode)

    def test_SDL_VideoInit(self):
        video.SDL_VideoInit(None)
        video.SDL_VideoInit(None)
        video.SDL_VideoInit(None)
        video.SDL_VideoQuit(None)
        video.SDL_VideoInit(None)

    def test_SDL_VideoQuit(self):
        video.SDL_VideoQuit()
        video.SDL_VideoQuit()
        video.SDL_VideoQuit()
        video.SDL_VideoInit(None)

    def test_SDL_GetDisplayBounds(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            bounds = rect.SDL_Rect()
            ret = video.SDL_GetDisplayBounds(index, byref(bounds))
            self.assertEqual(ret, 0)
            self.assertFalse(rect.SDL_RectEmpty(bounds))

    def test_screensaver(self):
        initial = video.SDL_IsScreenSaverEnabled()
        self.assertIn(initial, (SDL_FALSE, SDL_TRUE))

        video.SDL_EnableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_TRUE)
        video.SDL_EnableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_TRUE)
        video.SDL_DisableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_FALSE)
        video.SDL_DisableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_FALSE)
        video.SDL_EnableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_TRUE)
        video.SDL_DisableScreenSaver()
        self.assertEqual(video.SDL_IsScreenSaverEnabled(), SDL_FALSE)

        if initial == SDL_TRUE:
            video.SDL_EnableScreenSaver()
        else:
            video.SDL_DisableScreenSaver()

    def test_SDL_CreateWindow(self):
        # Borderless to ensure that the size check works
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 11, 12, 13, flag)
            self.assertIsInstance(window.contents, video.SDL_Window)
            px, py = c_int(), c_int()
            video.SDL_GetWindowPosition(window, byref(px), byref(py))
            self.assertEqual((px.value, py.value), (10, 11))
            video.SDL_GetWindowSize(window, byref(px), byref(py))
            self.assertEqual((px.value, py.value), (12, 13))
            self.assertEqual(video.SDL_GetWindowFlags(window) & flag, flag)
            self.assertEqual(video.SDL_GetWindowTitle(window), b"Test")
            video.SDL_DestroyWindow(window)
        # TODO

    def test_SDL_DestroyWindow(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            # TODO: how to check for this in a meaningful way?
            video.SDL_DestroyWindow(window)

    @unittest.skip("not implemented")
    def test_SDL_CreateWindowFrom(self):
        pass

    def test_SDL_GetWindowDisplayIndex(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 11, 12, 13, flag)
            self.assertIsInstance(window.contents, video.SDL_Window)
            px, py = c_int(), c_int()
            video.SDL_GetWindowPosition(window, byref(px), byref(py))
            self.assertEqual((px.value, py.value), (10, 11))
            video.SDL_GetWindowSize(window, byref(px), byref(py))
            self.assertEqual((px.value, py.value), (12, 13))
            self.assertEqual(video.SDL_GetWindowFlags(window) & flag, flag)
            self.assertEqual(video.SDL_GetWindowTitle(window), b"Test")

            dindex = video.SDL_GetWindowDisplayIndex(window)
            self.assertTrue(0 <= dindex <= numdisplays,
                            "Invalid display index")
            video.SDL_DestroyWindow(window)
            # self.assertRaises(sdl.SDLError, video.SDL_GetWindowDisplay,
            #                  window)

    def test_SDL_GetWindowDisplayMode(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            dmode = video.SDL_DisplayMode()
            ret = video.SDL_GetWindowDisplayMode(window, byref(dmode))
            self.assertEqual(ret, 0)
            video.SDL_DestroyWindow(window)
            # self.assertRaises(sdl.SDLError, video.SDL_GetWindowDisplayMode,
            #                  window)

    def test_SDL_SetWindowDisplayMode(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            dindex = video.SDL_GetWindowDisplayIndex(window)
            dmode = video.SDL_DisplayMode()

            ret = video.SDL_GetCurrentDisplayMode(dindex, byref(dmode))
            self.assertEqual(ret, 0)

            video.SDL_SetWindowDisplayMode(window, dmode)
            wmode = video.SDL_DisplayMode()
            ret = video.SDL_GetWindowDisplayMode(window, byref(wmode))
            self.assertEqual(ret, 0)
            # TODO: refresh rates differ
            #self.assertEqual(dmode, wmode)

            video.SDL_DestroyWindow(window)
            # self.assertRaises(sdl.SDLError, video.SDL_SetWindowDisplayMode,
            #                  window, dmode)

    def test_SDL_GetWindowPixelFormat(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            fmt = video.SDL_GetWindowPixelFormat(window)
            self.assertTrue(type(fmt) in(int, long))
            video.SDL_DestroyWindow(window)
            # self.assertRaises(sdl.SDLError, video.SDL_GetWindowPixelFormat,
            #                  window)

    def test_SDL_GetWindowID(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            self.assertGreaterEqual(video.SDL_GetWindowID(window), 0)

            video.SDL_DestroyWindow(window)
            #self.assertRaises(sdl.SDLError, video.SDL_GetWindowID, window)

    def test_SDL_GetWindowFromID(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            window2 = video.SDL_GetWindowFromID(video.SDL_GetWindowID(window))
            self.assertEqual(video.SDL_GetWindowID(window),
                             video.SDL_GetWindowID(window2))
            self.assertEqual(video.SDL_GetWindowTitle(window),
                             video.SDL_GetWindowTitle(window2))
            px1, py1, px2, py2 = c_int(), c_int(), c_int(), c_int()
            video.SDL_GetWindowPosition(window, byref(px1), byref(px2))
            video.SDL_GetWindowPosition(window2, byref(px2), byref(px2))
            self.assertEqual((px1.value, py1.value), (px2.value, py2.value))
            video.SDL_GetWindowSize(window, byref(px1), byref(px2))
            video.SDL_GetWindowSize(window2, byref(px2), byref(px2))
            self.assertEqual((px1.value, py1.value), (px2.value, py2.value))

    def test_SDL_GetWindowFlags(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flag)
            wflags = video.SDL_GetWindowFlags(window)
            self.assertEqual((wflags & flag), flag)

    def test_SDL_GetSetWindowTitle(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, 0)
        self.assertEqual(video.SDL_GetWindowTitle(window), b"Test")
        video.SDL_SetWindowTitle(window, b"Hello there")
        self.assertEqual(video.SDL_GetWindowTitle(window), b"Hello there")
        video.SDL_DestroyWindow(window)
        #self.assertRaises(sdl.SDLError, video.SDL_GetWindowTitle, window)

    def test_SDL_SetWindowIcon(self):
        sf = surface.SDL_CreateRGBSurface(0, 16, 16, 16, 0xF000, 0x0F00,
                                          0x00F0, 0x000F)
        self.assertIsInstance(sf.contents, surface.SDL_Surface)
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, 0)
        video.SDL_SetWindowIcon(window, sf)

        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_SetWindowIcon, None, None)
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_SetWindowIcon, window, None)
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_SetWindowIcon, None, sf)
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_SetWindowIcon, window, "Test")
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_SetWindowIcon, window, 123456)

    @unittest.skipIf(hasattr(sys, "pypy_version_info"),
                     "PyPy can't create proper py_object() values")
    def test_SDL_GetSetWindowData(self):
        # TODO: fix this
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, 0)
        self.assertIsInstance(window.contents, video.SDL_Window)
        values = {b"text": py_object("Teststring"),
                  b"object": py_object(self),
                  b"list": py_object([1, 2, 3, 4]),
                  b"tuple": py_object(("a", 1, self))
                 }

        for k, v in values.items():
            retval = video.SDL_GetWindowData(window, k)
            self.assertFalse(retval)
            video.SDL_SetWindowData(window, k, v)
            retval = video.SDL_GetWindowData(window, k)
            self.assertEqual(retval.contents.value, v.value)
        video.SDL_DestroyWindow(window)

    def test_SDL_GetSetWindowPosition(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, 0)
        px, py = c_int(), c_int()
        video.SDL_GetWindowPosition(window, byref(px), byref(py))
        self.assertEqual((px.value, py.value), (10, 10))
        video.SDL_SetWindowPosition(window, 0, 0)
        video.SDL_GetWindowPosition(window, byref(px), byref(py))
        self.assertEqual((px.value, py.value), (0, 0))
        video.SDL_SetWindowPosition(window, 600, 900)
        video.SDL_GetWindowPosition(window, byref(px), byref(py))
        self.assertEqual((px.value, py.value), (600, 900))
        video.SDL_SetWindowPosition(window, -200, -10)
        video.SDL_GetWindowPosition(window, byref(px), byref(py))
        self.assertEqual((px.value, py.value), (-200, -10))
        video.SDL_DestroyWindow(window)

    def test_SDL_GetSetWindowSize(self):
        flags = video.SDL_WINDOW_BORDERLESS
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10, flags)
        sx, sy = c_int(), c_int()
        video.SDL_GetWindowSize(window, byref(sx), byref(sy))
        self.assertEqual((sx.value, sy.value), (10, 10))
        video.SDL_SetWindowSize(window, 1, 1)
        video.SDL_GetWindowSize(window, byref(sx), byref(sy))
        self.assertEqual((sx.value, sy.value), (1, 1))
        video.SDL_SetWindowSize(window, 600, 900)
        video.SDL_GetWindowSize(window, byref(sx), byref(sy))
        self.assertEqual((sx.value, sy.value), (600, 900))
        video.SDL_SetWindowSize(window, -200, -10)
        video.SDL_GetWindowSize(window, byref(sx), byref(sy))
        self.assertEqual((sx.value, sy.value), (600, 900))
        video.SDL_DestroyWindow(window)

    @interactive("Was the window shown?")
    def test_SDL_ShowWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_ShowWindow",
                                        200, 200, 200, 200, 0)
        video.SDL_ShowWindow(window)
        doprint("""Please check, if a window with the title
'test_SDL_ShowWindow' is shown""")
        video.SDL_DestroyWindow(window)

    @interactive("Did the window vanish from your sight and pop up again?")
    def test_SDL_HideWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_HideWindow",
                                        200, 200, 200, 200, 0)
        video.SDL_ShowWindow(window)
        doprint("""Please check, if a window with the title
'test_SDL_HideWindow' is shown""")
        video.SDL_HideWindow(window)
        doprint("Please check, that the window is not shown anymore")
        video.SDL_ShowWindow(window)
        doprint("Please check, if the window is shown again")
        video.SDL_DestroyWindow(window)

    @interactive("Did the window raise properly?")
    def test_SDL_RaiseWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_RaiseWindow",
                                        200, 200, 200, 200, 0)
        video.SDL_ShowWindow(window)
        doprint("""Please check, that a window with the title
'test_SDL_RaiseWindow' is shown""")
        doprint("Move another window on top of the window, so it is hidden")
        video.SDL_RaiseWindow(window)
        doprint("The window should be raised to the foreground now")
        video.SDL_DestroyWindow(window)

    @interactive("Was the window maximized?")
    def test_SDL_MaximizeWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_MaximizeWindow", 200, 200,
                                        200, 200, video.SDL_WINDOW_RESIZABLE)
        video.SDL_ShowWindow(window)
        doprint("""Please check, that a window with the title
'test_SDL_MaximizeWindow' is shown""")
        video.SDL_MaximizeWindow(window)
        doprint("Please check, if the window was maximized properly")
        video.SDL_DestroyWindow(window)

    @interactive("Was the window minimized?")
    def test_SDL_MinimizeWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_MinimizeWindow", 200, 200,
                                        200, 200, 0)
        video.SDL_ShowWindow(window)
        doprint("""Please check, that a window with the title
'test_SDL_MinimizeWindow' is shown""")
        video.SDL_MinimizeWindow(window)
        doprint("Please check, if the window was minimized properly")
        video.SDL_DestroyWindow(window)

    @interactive("Was the window maximized and restored properly?")
    def test_SDL_RestoreWindow(self):
        window = video.SDL_CreateWindow(b"test_SDL_RestoreWindow", 200, 200,
                                        200, 200, video.SDL_WINDOW_RESIZABLE)
        video.SDL_ShowWindow(window)
        doprint("""Please check, that a window with the title
'test_SDL_RestoreWindow' is shown""")
        video.SDL_MaximizeWindow(window)
        doprint("Please check, if the window was maximized properly")
        video.SDL_RestoreWindow(window)
        doprint("Please check, if the window was restored properly")
        video.SDL_DestroyWindow(window)

    def test_SDL_SetWindowFullscreen(self):
        # TODO: HIDDEN avoids flickering, but is this really a sufficient test?
        flags = (video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED |
                 video.SDL_WINDOW_HIDDEN)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 0, 0, 1024, 768, flag)
            video.SDL_SetWindowFullscreen(window, True)
            flags = video.SDL_GetWindowFlags(window)
            self.assertEqual(flags & video.SDL_WINDOW_FULLSCREEN,
                             video.SDL_WINDOW_FULLSCREEN)
            video.SDL_SetWindowFullscreen(window, False)
            flags = video.SDL_GetWindowFlags(window)
            self.assertNotEqual(flags & video.SDL_WINDOW_FULLSCREEN,
                                video.SDL_WINDOW_FULLSCREEN)
            video.SDL_DestroyWindow(window)

    def test_SDL_GetWindowSurface(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 200, 200, 200, 200, flag)
            sf = video.SDL_GetWindowSurface(window)
            self.assertIsInstance(sf.contents, surface.SDL_Surface)
            video.SDL_DestroyWindow(window)
            # self.assertRaises(sdl.SDLError, video.SDL_GetWindowSurface,
            #                  window)

    def test_SDL_UpdateWindowSurface(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 200, 200, 200, 200, flag)
            video.SDL_UpdateWindowSurface(window)
            video.SDL_DestroyWindow(window)

    def test_SDL_UpdateWindowSurfaceRects(self):
        rectlist = (rect.SDL_Rect * 4)(rect.SDL_Rect(),
                                       rect.SDL_Rect(10, 10, 10, 10),
                                       rect.SDL_Rect(0, 0, 5, 4),
                                       rect.SDL_Rect(-5, -5, 6, 2))
        rptr = cast(rectlist, POINTER(rect.SDL_Rect))

        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 200, 200, 200, 200, flag)
            # self.assertRaises(sdl.SDLError,
            #                  video.SDL_UpdateWindowSurfaceRects,
            #                  window, rectlist)
            sf = surface.SDL_Surface()
            video.SDL_GetWindowSurface(window, byref(sf))
            ret = video.SDL_UpdateWindowSurfaceRects(window, rptr, 4)
            self.assertEqual(ret, 0)
            video.SDL_DestroyWindow(window)

    @unittest.skip("SDL_GetWindowGrab fails right now")
    def test_SDL_GetSetWindowGrab(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 200, 200, 200, 200, flag)
            self.assertEqual(video.SDL_GetWindowGrab(window), SDL_FALSE)
            video.SDL_SetWindowGrab(window, SDL_TRUE)
            self.assertEqual(video.SDL_GetWindowGrab(window), SDL_TRUE)
            video.SDL_SetWindowGrab(window, SDL_FALSE)
            self.assertEqual(video.SDL_GetWindowGrab(window), SDL_FALSE)

    @unittest.skip("not implemented")
    def test_SDL_GetGrabbedWindow(self):
        pass

    def test_SDL_GetSetWindowBrightness(self):
        flags = (video.SDL_WINDOW_BORDERLESS,
                 video.SDL_WINDOW_BORDERLESS | video.SDL_WINDOW_HIDDEN,
                 video.SDL_WINDOW_RESIZABLE | video.SDL_WINDOW_MINIMIZED)
        for flag in flags:
            window = video.SDL_CreateWindow(b"Test", 200, 200, 200, 200, flag)
            orig = video.SDL_GetWindowBrightness(window)
            self.assertIsInstance(orig, float)
            # Go from 0.0, 0.1 ... to 3.0
            gammas = (x * 0.1 for x in range(0, 20))
            count = 0
            for b in gammas:
                ret = video.SDL_SetWindowBrightness(window, b)
                if ret == 0:
                    val = video.SDL_GetWindowBrightness(window)
                    self.assertAlmostEqual(val, b)
                    count += 1
            # At least one gamma(1.0) must have worked.
            self.assertTrue(count > 0)

    @unittest.skip("not implemented")
    def test_SDL_SetWindowGammaRamp(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetWindowGammaRamp(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_SetWindowHitTest(self):
        pass

    def test_SDL_GL_LoadUnloadLibrary(self):
        # Try the default library
        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)
        video.SDL_GL_UnloadLibrary()

        if has_opengl_lib():
            fpath = get_opengl_path().encode("utf-8")
            self.assertEqual(video.SDL_GL_LoadLibrary(fpath), 0)
            video.SDL_GL_UnloadLibrary()

        #self.assertRaises(sdl.SDLError, video.SDL_GL_LoadLibrary, "Test")
        #self.assertRaises(sdl.SDLError, video.SDL_GL_LoadLibrary, False)
        #self.assertRaises(sdl.SDLError, video.SDL_GL_LoadLibrary, 0)

    def test_SDL_GL_GetProcAddress(self):
        procaddr = video.SDL_GL_GetProcAddress(b"glGetString")
        self.assertIsNone(procaddr)

        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)

        # Behaviour is undefined as long as there is no window and context.
        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)

        procaddr = video.SDL_GL_GetProcAddress(b"glGetString")
        self.assertTrue(procaddr is not None and int(procaddr) != 0)

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_UnloadLibrary()

        procaddr = video.SDL_GL_GetProcAddress(b"glGetString")
        self.assertIsNone(procaddr)

    def test_SDL_GL_ExtensionSupported(self):
        self.assertFalse(video.SDL_GL_ExtensionSupported(b"GL_EXT_bgra"))

        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)
        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)

        self.assertTrue(video.SDL_GL_ExtensionSupported(b"GL_EXT_bgra"))

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_UnloadLibrary()

        self.assertFalse(video.SDL_GL_ExtensionSupported(b"GL_EXT_bgra"))

    def test_SDL_GL_GetSetAttribute(self):
        # self.assertRaises(sdl.SDLError, video.SDL_GL_GetAttribute,
        #                  video.SDL_GL_DEPTH_SIZE)
        # self.assertRaises(sdl.SDLError, video.SDL_GL_SetAttribute,
        #                  1455, 24)

        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)

        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)

        depth = c_int()
        video.SDL_GL_GetAttribute(video.SDL_GL_DEPTH_SIZE, byref(depth))

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)

        newdepth = 24
        if depth == 8:
            newdepth = 16
        elif depth == 16:
            newdepth = 24
        elif depth == 24:
            newdepth = 16
        video.SDL_GL_SetAttribute(video.SDL_GL_DEPTH_SIZE, newdepth)

        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)

        val = c_int()
        video.SDL_GL_GetAttribute(video.SDL_GL_DEPTH_SIZE, byref(val))
        self.assertNotEqual(depth, val)
        self.assertEqual(val.value, newdepth)

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_UnloadLibrary()

    def test_SDL_GL_CreateDeleteContext(self):
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_GL_CreateContext, None)
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_GL_CreateContext, "Test")
        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_GL_CreateContext, 1234)

        window = video.SDL_CreateWindow(b"No OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_BORDERLESS)

        #self.assertRaises(sdl.SDLError, video.SDL_GL_CreateContext, window)
        video.SDL_DestroyWindow(window)

        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)
        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)

        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)

        ctx = video.SDL_GL_CreateContext(window)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_DeleteContext(ctx)

        video.SDL_GL_UnloadLibrary()

    def test_SDL_GL_MakeCurrent(self):
        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)

        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_GL_MakeCurrent, None, None)

        window = video.SDL_CreateWindow(b"No OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_BORDERLESS)

        #self.assertRaises(sdl.SDLError, video.SDL_GL_CreateContext, window)
        video.SDL_DestroyWindow(window)

        # self.assertRaises((AttributeError, TypeError),
        #                  video.SDL_GL_MakeCurrent, None, None)

        video.SDL_GL_UnloadLibrary()

    def test_SDL_GL_GetSetSwapInterval(self):
        #self.assertRaises(ValueError, video.SDL_GL_SetSwapInterval, None)
        #self.assertRaises(ValueError, video.SDL_GL_SetSwapInterval, "Test")
        #self.assertRaises(ValueError, video.SDL_GL_SetSwapInterval, 1234)

        # No current OpenGL context yet.
        # Might crash on certain platforms, since the internal state of
        # SDL2 does not support calling GL functions without having a
        # GL library loaded.
        # self.assertRaises(sdl.SDLError, video.SDL_GL_SetSwapInterval, 1)
        # self.assertRaises(sdl.SDLError, video.SDL_GL_SetSwapInterval, 0)

        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)
        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)
        ctx = video.SDL_GL_CreateContext(window)
        video.SDL_GL_MakeCurrent(window, ctx)

        video.SDL_GL_SetSwapInterval(0)
        self.assertEqual(video.SDL_GL_GetSwapInterval(), 0)
        video.SDL_GL_SetSwapInterval(1)
        self.assertEqual(video.SDL_GL_GetSwapInterval(), 1)

        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_UnloadLibrary()

    def test_SDL_GL_SwapWindow(self):
        self.assertEqual(video.SDL_GL_LoadLibrary(None), 0)
        window = video.SDL_CreateWindow(b"OpenGL", 10, 10, 10, 10,
                                        video.SDL_WINDOW_OPENGL)
        ctx = video.SDL_GL_CreateContext(window)
        video.SDL_GL_MakeCurrent(window, ctx)
        video.SDL_GL_SwapWindow(window)
        video.SDL_GL_SwapWindow(window)
        video.SDL_GL_SwapWindow(window)
        video.SDL_GL_SwapWindow(window)
        video.SDL_GL_DeleteContext(ctx)
        video.SDL_DestroyWindow(window)
        video.SDL_GL_UnloadLibrary()

    @unittest.skip("not implemented")
    def test_SDL_GL_ResetAttributes(self):
        pass

    def test_SDL_GetDisplayDPI(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            ddpi, hdpi, vdpi = c_float(), c_float(), c_float()
            ret = video.SDL_GetDisplayDPI(index, byref(ddpi), byref(hdpi),
                                          byref(vdpi))
            self.assertEqual(ret, 0)
            self.assertGreaterEqual(ddpi.value, 96.0)
            self.assertGreaterEqual(hdpi.value, 96.0)
            self.assertGreaterEqual(vdpi.value, 96.0)

    def test_SDL_SetWindowResizable(self):
        window = video.SDL_CreateWindow(b"Resizable", 10, 10, 10, 10,
                                        video.SDL_WINDOW_RESIZABLE)
        flags = video.SDL_GetWindowFlags(window)
        self.assertEqual(flags & video.SDL_WINDOW_RESIZABLE,
                         video.SDL_WINDOW_RESIZABLE)
        video.SDL_SetWindowResizable(window, SDL_FALSE)
        flags = video.SDL_GetWindowFlags(window)
        self.assertNotEqual(flags & video.SDL_WINDOW_RESIZABLE,
                            video.SDL_WINDOW_RESIZABLE)
        video.SDL_SetWindowResizable(window, SDL_TRUE)
        flags = video.SDL_GetWindowFlags(window)
        self.assertEqual(flags & video.SDL_WINDOW_RESIZABLE,
                         video.SDL_WINDOW_RESIZABLE)
        video.SDL_DestroyWindow(window)

    def test_SDL_GetSetWindowOpacity(self):
        window = video.SDL_CreateWindow(b"Opacity", 10, 10, 10, 10, 0)
        opacity = c_float()
        ret = video.SDL_GetWindowOpacity(window, byref(opacity))
        self.assertEqual(ret, 0)
        self.assertEqual(opacity.value, 1.0)
        ret = video.SDL_SetWindowOpacity(window, 0.0)
        self.assertEqual(ret, 0)
        ret = video.SDL_GetWindowOpacity(window, byref(opacity))
        self.assertEqual(ret, 0)
        self.assertEqual(opacity.value, 0.0)
        ret = video.SDL_SetWindowOpacity(window, 0.653)
        self.assertEqual(ret, 0)
        ret = video.SDL_GetWindowOpacity(window, byref(opacity))
        self.assertEqual(ret, 0)
        self.assertAlmostEqual(opacity.value, 0.653, 2)
        video.SDL_DestroyWindow(window)

    def test_SDL_GetDisplayUsableBounds(self):
        numdisplays = video.SDL_GetNumVideoDisplays()
        for index in range(numdisplays):
            bounds = rect.SDL_Rect()
            ret = video.SDL_GetDisplayUsableBounds(index, byref(bounds))
            self.assertEqual(ret, 0)
            self.assertFalse(rect.SDL_RectEmpty(bounds))

    def test_SDL_GetWindowsBordersSize(self):
        window = video.SDL_CreateWindow(b"Borders", 10, 10, 10, 10, 0)
        l, r, t, b = c_int(), c_int(), c_int(), c_int()
        ret = video.SDL_GetWindowBordersSize(window, byref(t), byref(l),
                                             byref(b), byref(r))
        if sys.platform in ("win32", "cygwin", "darwin"):
            self.assertEqual(ret, -1)
            self.assertEqual(t.value, 0)
            self.assertEqual(l.value, 0)
            self.assertEqual(b.value, 0)
            self.assertEqual(r.value, 0)
        else:
            self.assertEqual(ret, 0)
            self.assertNotEqual(t.value, 0)
            self.assertNotEqual(l.value, 0)
            self.assertNotEqual(b.value, 0)
            self.assertNotEqual(r.value, 0)
        video.SDL_DestroyWindow(window)
        window = video.SDL_CreateWindow(b"No Borders", 10, 10, 10, 10,
                                        video.SDL_WINDOW_BORDERLESS)
        ret = video.SDL_GetWindowBordersSize(window, byref(t), byref(l),
                                             byref(b), byref(r))
        if sys.platform not in ("win32", "cygwin", "darwin"):
            self.assertEqual(ret, 0)
            self.assertEqual(t.value, 0)
            self.assertEqual(l.value, 0)
            self.assertEqual(b.value, 0)
            self.assertEqual(r.value, 0)
        video.SDL_DestroyWindow(window)

    @unittest.skip("not implemented")
    def test_SDL_SetWindowModalFor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_SetWindowInputFocus(self):
        pass

if __name__ == '__main__':
    sys.exit(unittest.main())
