import sys
import pytest
from ctypes import byref, POINTER, c_int
import sdl2
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_EVERYTHING, SDL_GetError
import itertools
from sdl2.stdinc import Uint8, Uint32, SDL_TRUE, SDL_FALSE
from sdl2 import render, video, surface, pixels, blendmode, rect
from sdl2.ext.pixelaccess import PixelView

# TODO: Ensure all functions in module have corresponding tests
# TODO: Write tests for more functions
# TODO: Mostly positive tests, improve this!

_ISPYPY = hasattr(sys, "pypy_version_info")
if _ISPYPY:
    import gc
    dogc = gc.collect
else:
    dogc = lambda: None


class TestSDLRender(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        cls._RENDERFLAGS = render.SDL_RENDERER_ACCELERATED
        SDL_Init(SDL_INIT_EVERYTHING)
        driver = video.SDL_GetCurrentVideoDriver()
        if driver is None:
            raise pytest.skip('Video subsystem not supported')
        if driver == b"dummy":
            cls._RENDERFLAGS = render.SDL_RENDERER_SOFTWARE

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def test_SDL_RendererInfo(self):
        info = render.SDL_RendererInfo()
        assert isinstance(info, render.SDL_RendererInfo)

    def test_SDL_Renderer(self):
        val = render.SDL_Renderer()
        assert isinstance(val, render.SDL_Renderer)

    def test_SDL_Texture(self):
        val = render.SDL_Texture()
        assert isinstance(val, render.SDL_Texture)

    def test_SDL_GetNumRenderDrivers(self):
        val = render.SDL_GetNumRenderDrivers()
        assert val >= 1

    def test_SDL_GetRenderDriverInfo(self):
        renderers = []
        errs = []
        drivers = render.SDL_GetNumRenderDrivers()
        for x in range(drivers):
            sdl2.SDL_ClearError()
            info = render.SDL_RendererInfo()
            ret = render.SDL_GetRenderDriverInfo(x, info)
            if ret != 0:
                err = sdl2.SDL_GetError().decode("utf-8")
                errs.append("Renderer {0} error: {1}".format(x, err))
            else:
                renderers.append(info.name.decode("utf-8"))
        print("Render drivers supported by current SDL2 binary:")
        print(renderers)
        assert len(renderers)
        assert "software" in renderers

    def test_SDL_CreateWindowAndRenderer(self):
        window = POINTER(video.SDL_Window)()
        renderer = POINTER(render.SDL_Renderer)()
        ret = render.SDL_CreateWindowAndRenderer \
            (10, 10, video.SDL_WINDOW_HIDDEN, byref(window), byref(renderer))
        assert ret == 0

        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

        # TODO: the code below works, too - is that really expected from SDL?
        #window, renderer = render.SDL_CreateWindowAndRenderer \
        #   (-10, -10, video.SDL_WINDOW_HIDDEN)
        #self.assertIsInstance(window, video.SDL_Window)
        #self.assertIsInstance(renderer, render.SDL_Renderer)

    def test_SDL_CreateDestroyRenderer(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_SHOWN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)
            render.SDL_DestroyRenderer(renderer)

            # TODO: using -1 as index for the call below leads to random
            # access violations on Win32
            renderer = render.SDL_CreateRenderer(window, i,
                                                 render.SDL_RENDERER_SOFTWARE)
            assert isinstance(renderer.contents, render.SDL_Renderer)
            render.SDL_DestroyRenderer(renderer)
            video.SDL_DestroyWindow(window)
        assert not (failed == rcount), "could not create a renderer"
        dogc()

    def test_SDL_CreateSoftwareRenderer(self):
        sf = surface.SDL_CreateRGBSurface(0, 100, 100, 32,
                                          0xFF000000,
                                          0x00FF0000,
                                          0x0000FF00,
                                          0x000000FF)
        renderer = render.SDL_CreateSoftwareRenderer(sf)
        assert isinstance(renderer.contents, render.SDL_Renderer)
        render.SDL_DestroyRenderer(renderer)
        surface.SDL_FreeSurface(sf)

        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_CreateSoftwareRenderer, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_CreateSoftwareRenderer, 1234)

    def test_SDL_GetRenderer(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_GetRenderer(window)
            assert not renderer
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            ren = render.SDL_GetRenderer(window)
            assert isinstance(ren.contents, render.SDL_Renderer)
            render.SDL_DestroyRenderer(renderer)
            assert not render.SDL_GetRenderer(window)

            video.SDL_DestroyWindow(window)
            assert not render.SDL_GetRenderer(window)
        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_GetRenderer, None)
        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_GetRenderer, "Test")
        assert not (failed == rcount), "could not create a renderer"
        dogc()

    def test_SDL_GetRendererInfo(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)
            info = render.SDL_RendererInfo()
            ret = render.SDL_GetRendererInfo(renderer, byref(info))
            assert ret == 0
            render.SDL_DestroyRenderer(renderer)

            #self.assertRaises(sdl.SDLError, render.SDL_GetRendererInfo,
            #                  renderer)

            video.SDL_DestroyWindow(window)
        assert not (failed == rcount), "could not create a renderer"
        with pytest.raises((AttributeError, TypeError)):
            render.SDL_GetRendererInfo(None)
        with pytest.raises((AttributeError, TypeError)):
            render.SDL_GetRendererInfo("Test")
        dogc()

    def test_SDL_CreateDestroyTexture(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        formats = (pixels.SDL_PIXELFORMAT_ARGB8888,
                   pixels.SDL_PIXELFORMAT_RGB555,
                   pixels.SDL_PIXELFORMAT_RGBA4444,
                   pixels.SDL_PIXELFORMAT_RGBA8888,
                   pixels.SDL_PIXELFORMAT_ARGB2101010,
                   pixels.SDL_PIXELFORMAT_YUY2
                   )
        access = (render.SDL_TEXTUREACCESS_STATIC,
                  render.SDL_TEXTUREACCESS_STREAMING,
                  render.SDL_TEXTUREACCESS_TARGET)
        for fmt in formats:
            for acc in access:
                for w in range(1, 300, 5):
                    for h in range(1, 300, 5):
                        tex = render.SDL_CreateTexture(renderer, fmt, acc,
                                                       w, h)
                        assert isinstance(tex.contents, render.SDL_Texture)
                        render.SDL_DestroyTexture(tex)
                    if (w % 50) == 0:
                        dogc()

        #self.assertRaises(sdl.SDLError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, -10, 10)
        #self.assertRaises(sdl.SDLError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, 10, -10)
        #self.assertRaises(sdl.SDLError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, -10, -10)
        #self.assertRaises(ValueError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, -5, 10, 10)
        #self.assertRaises(ValueError, render.SDL_CreateTexture, renderer,
        #                  - 10, 1, 10, 10)
        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_CreateTexture, None,
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, 10, 10)
        #self.assertRaises((AttributeError, TypeError),
        #                  render.SDL_CreateTexture, "Test",
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, 10, 10)
        #self.assertRaises(ValueError, render.SDL_CreateTexture, renderer,
        #                  "Test", 1, 10, 10)
        #self.assertRaises(ValueError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, None, 10, 10)
        #self.assertRaises(ValueError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, "Test", 10, 10)

        render.SDL_DestroyRenderer(renderer)
        #self.assertRaises(sdl.SDLError, render.SDL_CreateTexture, renderer,
        #                  pixels.SDL_PIXELFORMAT_RGB555, 1, 10, 10)
        video.SDL_DestroyWindow(window)
        dogc()

    def test_SDL_CreateTextureFromSurface(self):
        sf = surface.SDL_CreateRGBSurface(0, 100, 100, 32, 0xFF000000,
                                          0x00FF0000, 0x0000FF00, 0x000000FF)
        assert isinstance(sf.contents, surface.SDL_Surface)
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)
        tex = render.SDL_CreateTextureFromSurface(renderer, sf)
        assert isinstance(tex.contents, render.SDL_Texture)
        dogc()

    def test_SDL_QueryTexture(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        formats = (pixels.SDL_PIXELFORMAT_ARGB8888,
                   pixels.SDL_PIXELFORMAT_RGB555,
                   pixels.SDL_PIXELFORMAT_RGBA4444,
                   pixels.SDL_PIXELFORMAT_ARGB2101010,
                   pixels.SDL_PIXELFORMAT_YUY2
                   )
        access = (render.SDL_TEXTUREACCESS_STATIC,
                  render.SDL_TEXTUREACCESS_STREAMING,
                  render.SDL_TEXTUREACCESS_TARGET)
        for fmt in formats:
            for acc in access:
                for w in range(1, 300, 5):
                    for h in range(1, 300, 5):
                        tex = render.SDL_CreateTexture(renderer, fmt, acc,
                                                       w, h)
                        assert isinstance(tex.contents, render.SDL_Texture)
                        qf, qa, qw, qh = Uint32(), c_int(), c_int(), c_int()
                        ret = render.SDL_QueryTexture(tex, byref(qf),
                                                      byref(qa), byref(qw),
                                                      byref(qh))
                        assert ret == 0
                        assert qf.value == fmt
                        assert qa.value == acc
                        assert qw.value == w
                        assert qh.value == h
                        render.SDL_DestroyTexture(tex)
                    if _ISPYPY and (w % 50) == 0:
                        gc.collect()

        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

    def test_SDL_GetSetTextureColorMod(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        tex = render.SDL_CreateTexture(renderer,
                                       pixels.SDL_PIXELFORMAT_ARGB8888,
                                       render.SDL_TEXTUREACCESS_STREAMING,
                                       10, 10)
        assert isinstance(tex.contents, render.SDL_Texture)
        colors = ((16, 22, 185),
                  (32, 64, 128),
                  (64, 32, 128),
                  (64, 32, 255),
                  (255, 32, 64),
                  (255, 32, 128),
                  (0, 0, 0),
                  (255, 255, 255),
                  (128, 128, 128),
                  )
        for r, g, b in colors:
            ret = render.SDL_SetTextureColorMod(tex, r, g, b)
            assert ret == 0
            tr, tg, tb = Uint8(), Uint8(), Uint8()
            ret = render.SDL_GetTextureColorMod(tex, byref(tr), byref(tg),
                                                byref(tb))
            assert ret == 0
            assert (tr.value, tg.value, tb.value) == (r, g, b)

        render.SDL_DestroyTexture(tex)
        #self.assertRaises(sdl.SDLError, render.SDL_SetTextureColorMod, tex,
        #                  10, 20, 30)
        #self.assertRaises(sdl.SDLError, render.SDL_GetTextureColorMod, tex)

        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

    def test_SDL_GetSetTextureAlphaMod(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        tex = render.SDL_CreateTexture(renderer,
                                       pixels.SDL_PIXELFORMAT_ARGB8888,
                                       render.SDL_TEXTUREACCESS_STREAMING,
                                       10, 10)
        assert isinstance(tex.contents, render.SDL_Texture)

        for alpha in range(0, 255):
            ret = render.SDL_SetTextureAlphaMod(tex, alpha)
            assert ret == 0
            talpha = Uint8()
            ret = render.SDL_GetTextureAlphaMod(tex, byref(talpha))
            assert ret == 0
            assert talpha.value == alpha

        render.SDL_DestroyTexture(tex)
        #self.assertRaises(sdl.SDLError, render.SDL_SetTextureColorMod, tex,
        #                  10, 20, 30)
        #self.assertRaises(sdl.SDLError, render.SDL_GetTextureColorMod, tex)

        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

    def test_SDL_GetSetTextureBlendMode(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        tex = render.SDL_CreateTexture(renderer,
                                       pixels.SDL_PIXELFORMAT_ARGB8888,
                                       render.SDL_TEXTUREACCESS_STREAMING,
                                       10, 10)
        assert isinstance(tex.contents, render.SDL_Texture)

        modes = (blendmode.SDL_BLENDMODE_NONE,
                 blendmode.SDL_BLENDMODE_ADD,
                 blendmode.SDL_BLENDMODE_BLEND,
                 blendmode.SDL_BLENDMODE_MOD,
                 )
        for mode in modes:
            ret = render.SDL_SetTextureBlendMode(tex, mode)
            assert ret == 0
            tmode = blendmode.SDL_BlendMode()
            ret = render.SDL_GetTextureBlendMode(tex, byref(tmode))
            assert ret == 0
            assert tmode.value == mode

        render.SDL_DestroyTexture(tex)
        #self.assertRaises(sdl.SDLError, render.SDL_SetTextureBlendMode, tex,
        #                  modes[2])
        #self.assertRaises(sdl.SDLError, render.SDL_GetTextureBlendMode, tex)

        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_GetSetTextureScaleMode(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        tex = render.SDL_CreateTexture(
            renderer, pixels.SDL_PIXELFORMAT_ARGB8888,
            render.SDL_TEXTUREACCESS_STREAMING, 10, 10
        )
        assert isinstance(tex.contents, render.SDL_Texture)

        modes = (render.SDL_ScaleModeNearest, render.SDL_ScaleModeLinear,
                 render.SDL_ScaleModeBest)
        for mode in modes:
            ret = render.SDL_SetTextureScaleMode(tex, mode)
            assert ret == 0
            tmode = render.SDL_ScaleMode()
            ret = render.SDL_GetTextureScaleMode(tex, byref(tmode))
            assert ret == 0
            assert tmode.value == mode

        render.SDL_DestroyTexture(tex)
        render.SDL_DestroyRenderer(renderer)
        video.SDL_DestroyWindow(window)
        dogc()

    @pytest.mark.skip("not implemented")
    def test_SDL_UpdateTexture(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_UpdateYUVTexture(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2012, reason="not available")
    def test_SDL_LockTextureToSurface(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_LockUnlockTexture(self):
        pass

    def test_SDL_RenderTargetSupported(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)

            val = render.SDL_RenderTargetSupported(renderer)
            assert val in (SDL_TRUE, SDL_FALSE)
            render.SDL_DestroyRenderer(renderer)
            video.SDL_DestroyWindow(window)
        assert not (failed == rcount), "could not create a renderer"
        dogc()

    def test_SDL_GetSetRenderTarget(self):
        skipcount = 0
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)

            supported = render.SDL_RenderTargetSupported(renderer)
            if not supported:
                skipcount += 1
                render.SDL_DestroyRenderer(renderer)
                continue

            ret = render.SDL_SetRenderTarget(renderer, None)
            assert ret == 0
            assert not render.SDL_GetRenderTarget(renderer)

            tex = render.SDL_CreateTexture(renderer,
                                           pixels.SDL_PIXELFORMAT_ARGB8888,
                                           render.SDL_TEXTUREACCESS_TARGET,
                                           10, 10)
            ret = render.SDL_SetRenderTarget(renderer, tex)
            assert ret == 0
            tgt = render.SDL_GetRenderTarget(renderer)
            assert isinstance(tgt.contents, render.SDL_Texture)
            render.SDL_DestroyTexture(tex)

            # TODO: Check in the SDL codebase, why the code below does
            # not fail...
            # tex2 = render.SDL_CreateTexture(renderer,
            #                              pixels.SDL_PIXELFORMAT_ARGB8888,
            #                              render.SDL_TEXTUREACCESS_STREAMING,
            #                              10, 10)
            # self.assertRaises(SDLError, render.SDL_SetRenderTarget, renderer,
            #                   tex2)
            # render.SDL_DestroyTexture(tex2)

            render.SDL_DestroyRenderer(renderer)
            video.SDL_DestroyWindow(window)

        assert not (failed == rcount), "could not create a renderer"
        if skipcount == rcount:
            pytest.skip("None of the renderers supports render targets")
        dogc()

    def test_SDL_RenderGetSetViewport(self):
        rects = (rect.SDL_Rect(0, 0, 0, 0),
                 rect.SDL_Rect(0, 0, 10, 10),
                 rect.SDL_Rect(3, 3, 5, 5),
                 rect.SDL_Rect(-5, -5, 10, 10),
                 rect.SDL_Rect(10, 10, 10, 10),
                 rect.SDL_Rect(0, 0, -10, -10),
                 rect.SDL_Rect(-10, 0, 10, 10),
                 rect.SDL_Rect(0, -10, 10, 10),
                 rect.SDL_Rect(-10, -10, 10, 10),
            )
        failcount = 0
        port = rect.SDL_Rect()
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN |
                                            video.SDL_WINDOW_BORDERLESS)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)
            ret = render.SDL_RenderSetViewport(renderer, None)
            assert ret == 0
            render.SDL_RenderGetViewport(renderer, byref(port))
            assert port == rect.SDL_Rect(0, 0, 10, 10)
            for r in rects:
                if r.w == r.h == 0:
                    # http://bugzilla.libsdl.org/show_bug.cgi?id=1622
                    # OpenGL renderers cause a exception here.
                    continue
                ret = render.SDL_RenderSetViewport(renderer, r)
                assert ret == 0
                render.SDL_RenderGetViewport(renderer, byref(port))
                if port != r:
                    failcount += 1

            render.SDL_DestroyRenderer(renderer)
            video.SDL_DestroyWindow(window)

        assert not (failed == rcount), "could not create a renderer"
        errmsg = ("For some reason, even with correct values, this seems to "
                  "fail on creating the second renderer of the window, if any")
        if failcount > 0:
            pytest.skip(errmsg)
        dogc()

    def test_SDL_GetSetRenderDrawColor(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)

            colors = ((16, 22, 185, 217),
                      (32, 64, 128, 255),
                      (64, 32, 128, 255),
                      (64, 32, 255, 128),
                      (255, 32, 64, 128),
                      (255, 32, 128, 64),
                      (0, 0, 0, 0),
                      (255, 255, 255, 255),
                      (128, 128, 128, 255),
                      )
            for r, g, b, a in colors:
                ret = render.SDL_SetRenderDrawColor(renderer, r, g, b, a)
                assert ret == 0
                dr, dg, db, da = Uint8(), Uint8(), Uint8(), Uint8()
                ret = render.SDL_GetRenderDrawColor(renderer, byref(dr),
                                                    byref(dg), byref(db),
                                                    byref(da))
                assert ret == 0
                assert (dr.value, dg.value, db.value, da.value) == (r, g, b, a)
            render.SDL_DestroyRenderer(renderer)
            #self.assertRaises(sdl.SDLError, render.SDL_SetRenderDrawColor,
            #                  renderer, 10, 20, 30, 40)
            #self.assertRaises(sdl.SDLError, render.SDL_GetRenderDrawColor,
            #                  renderer)
            video.SDL_DestroyWindow(window)
        assert not (failed == rcount), "could not create a renderer"
        dogc()

    def test_SDL_GetSetRenderDrawBlendMode(self):
        failed = 0
        rcount = render.SDL_GetNumRenderDrivers()
        for i in range(rcount):
            window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                            video.SDL_WINDOW_HIDDEN)
            assert isinstance(window.contents, video.SDL_Window)
            renderer = render.SDL_CreateRenderer(window, i, self._RENDERFLAGS)
            if not (renderer and renderer.contents):
                failed += 1
                video.SDL_DestroyWindow(window)
                continue
            assert isinstance(renderer.contents, render.SDL_Renderer)

            modes = (blendmode.SDL_BLENDMODE_NONE,
                     blendmode.SDL_BLENDMODE_ADD,
                     blendmode.SDL_BLENDMODE_BLEND,
                     blendmode.SDL_BLENDMODE_MOD,
                     )
            for mode in modes:
                ret = render.SDL_SetRenderDrawBlendMode(renderer, mode)
                bmode = blendmode.SDL_BlendMode()
                ret = render.SDL_GetRenderDrawBlendMode(renderer, byref(bmode))
                assert ret == 0
                assert bmode.value == mode
            render.SDL_DestroyRenderer(renderer)
            #self.assertRaises(sdl.SDLError, render.SDL_SetRenderDrawBlendMode,
            #                  renderer, video.SDL_BLENDMODE_ADD)
            #self.assertRaises(sdl.SDLError, render.SDL_GetRenderDrawBlendMode,
            #                  renderer)
            video.SDL_DestroyWindow(window)
        assert not (failed == rcount), "could not create a renderer"
        dogc()

    def test_SDL_RenderClear(self):
        window = video.SDL_CreateWindow(b"Test", 10, 10, 10, 10,
                                        video.SDL_WINDOW_HIDDEN)
        assert isinstance(window.contents, video.SDL_Window)
        renderer = render.SDL_CreateRenderer(window, -1, self._RENDERFLAGS)
        assert isinstance(renderer.contents, render.SDL_Renderer)

        ret = render.SDL_RenderClear(renderer)
        assert ret == 0
        render.SDL_DestroyRenderer(renderer)
        #self.assertRaises(sdl.SDLError, render.SDL_RenderClear, renderer)
#        self.assertRaises((AttributeError, TypeError),
#                          render.SDL_RenderClear, None)
#        self.assertRaises((AttributeError, TypeError),
#                          render.SDL_RenderClear, "Test")
#        self.assertRaises((AttributeError, TypeError),
#                          render.SDL_RenderClear, 123456)
        dogc()

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_SDL_RenderDrawPoint(self):
        points = ((-4, -3), (-4, 3), (4, -3),
                  (0, 0), (1, 1), (10, 10), (99, 99),
                  (4, 22), (57, 88), (45, 15),
                  (100, 100)
                  )
        r, g, b, a = 0xAA, 0xBB, 0xCC, 0xDD
        w, h = 100, 100
        sf = surface.SDL_CreateRGBSurface(0, w, h, 32, 0xFF000000, 0x00FF0000,
                                          0x0000FF00, 0x000000FF)
        color = pixels.SDL_MapRGBA(sf.contents.format, r, g, b, a)
        renderer = render.SDL_CreateSoftwareRenderer(sf)
        assert isinstance(renderer.contents, render.SDL_Renderer)
        ret = render.SDL_SetRenderDrawColor(renderer, r, g, b, a)
        assert ret == 0
        for x, y in points:
            ret = render.SDL_RenderDrawPoint(renderer, x, y)
            assert ret == 0
        render.SDL_RenderPresent(renderer)
        view = PixelView(sf.contents)
        for x, y in points:
            npx = max(x + 1, w)
            npy = max(y + 1, h)
            ppx = max(x - 1, 0)
            ppy = max(y - 1, 0)
            if x < 0 or x >= w or y < 0 or y >= h:
                continue
            assert hex(view[y][x]) == hex(color)
            if (npx, npy) not in points:
                assert hex(view[npy][npx]) != hex(color)
            if (ppx, ppy) not in points:
                assert hex(view[ppy][ppx]) != hex(color)
        render.SDL_DestroyRenderer(renderer)
        del view
        surface.SDL_FreeSurface(sf)

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderDrawPoints(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderDrawLine(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderDrawLines(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderDrawRect(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderDrawRects(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderFillRect(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderFillRects(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderCopy(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderCopyEx(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawPointF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawPointsF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawLineF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawLinesF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawRectF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderDrawRectsF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderFillRectF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderFillRectsF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderCopyF(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderCopyExF(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderReadPixels(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderPresent(self):
        pass

    @pytest.mark.skip("not implemented")
    @pytest.mark.skipif(sdl2.dll.version < 2010, reason="not available")
    def test_SDL_RenderFlush(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderGetSetScale(self):
        pass

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_SDL_RenderGetSetLogicalSize(self):
        w, h = 100, 100
        sf = surface.SDL_CreateRGBSurface(0, w, h, 32,
                                          0xFF000000,
                                          0x00FF0000,
                                          0x0000FF00,
                                          0x000000FF)

        renderer = render.SDL_CreateSoftwareRenderer(sf)
        view = PixelView(sf.contents)

        magenta = 255, 0, 255, 255
        green = 0, 255, 0, 255

        magenta_int = sum(c << (i * 8) for i, c in enumerate(reversed(magenta)))
        green_int = sum(c << (i * 8) for i, c in enumerate(reversed(green)))

        def clear_green():
            ret = render.SDL_SetRenderDrawColor(renderer, green[0], green[1],
                                                green[2], green[3])
            assert ret == 0
            ret = render.SDL_RenderClear(renderer)
            assert ret == 0

        def draw_magenta_pixel(x, y):
            ret = render.SDL_SetRenderDrawColor(renderer, magenta[0],
                                                magenta[1], magenta[2],
                                                magenta[3])
            assert ret == 0
            ret = render.SDL_RenderDrawPoint(renderer, x, y)
            assert ret == 0

        # Test 1
        # If we set the logical renderer size to 1 x 1, drawing a point
        # at 0, 0 should have the same effect as filling the entire
        # (square) window with magenta - no green should show through.
        got_width, got_height = c_int(), c_int()

        ret = render.SDL_RenderSetLogicalSize(renderer, 1, 1)
        assert ret == 0
        render.SDL_RenderGetLogicalSize(renderer, byref(got_width),
                                        byref(got_height))
        assert got_width.value == 1
        assert got_height.value == 1

        clear_green()
        draw_magenta_pixel(0, 0)

        for x, y in itertools.product(range(w), range(h)):
            assert view[y][x] == magenta_int, 'No pixel should be green'

        # Test 2
        # Reset the logical size to the original target by using 0, 0
        # only the first and last pixel should be magenta. The rest
        # should be green.
        got_width, got_height = c_int(), c_int()

        ret = render.SDL_RenderSetLogicalSize(renderer, 0, 0)
        assert ret == 0

        render.SDL_RenderGetLogicalSize(renderer, byref(got_width),
                                        byref(got_height))
        assert got_width.value == 0
        assert got_height.value == 0

        clear_green()

        draw_magenta_pixel(0, 0)
        draw_magenta_pixel(w - 1, h - 1)

        for x, y in itertools.product(range(w), range(h)):
            if (x, y) == (0, 0) or (x, y) == (w - 1, h - 1):
                assert view[y][x] == magenta_int, \
                       'First and last pixel should be magenta'
            else:
                assert view[y][x] == green_int, \
                       'All other pixels should be green'

        # Test 3
        # Set the logical size to 1/10, making a logical pixel draw be
        # 10 x 10 real pixel blocks.
        got_width, got_height = c_int(), c_int()

        ret = render.SDL_RenderSetLogicalSize(renderer, w//10, h//10)
        assert ret == 0

        render.SDL_RenderGetLogicalSize(renderer, byref(got_width),
                                        byref(got_height))
        assert got_width.value == w//10
        assert got_height.value == h//10

        clear_green()

        draw_magenta_pixel(0, 0)
        for x, y in itertools.product(range(w), range(h)):
            if x < 10 and y < 10:
                assert view[y][x] == magenta_int, \
                       'Top-left 10 x 10 pixel block should be magenta'
            else:
                assert view[y][x] == green_int, \
                       'All other pixels should be green'

        render.SDL_DestroyRenderer(renderer)
        surface.SDL_FreeSurface(sf)

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderGetSetClipRect(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GetRendererOutputSize(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_RenderIsClipEnabled(self):
        pass

    def test_SDL_RenderGetSetIntegerScale(self):
        sf = surface.SDL_CreateRGBSurface(0, 100, 100, 32,
                                          0xFF000000,
                                          0x00FF0000,
                                          0x0000FF00,
                                          0x000000FF)
        renderer = render.SDL_CreateSoftwareRenderer(sf)
        assert isinstance(renderer.contents, render.SDL_Renderer)
        assert render.SDL_RenderGetIntegerScale(renderer) == SDL_FALSE
        assert render.SDL_RenderSetIntegerScale(renderer, SDL_FALSE) == 0
        assert render.SDL_RenderGetIntegerScale(renderer) == SDL_FALSE
        assert render.SDL_RenderSetIntegerScale(renderer, SDL_TRUE) == 0
        assert render.SDL_RenderGetIntegerScale(renderer) == SDL_TRUE
        assert render.SDL_RenderSetIntegerScale(renderer, SDL_FALSE) == 0
        assert render.SDL_RenderGetIntegerScale(renderer) == SDL_FALSE
        render.SDL_DestroyRenderer(renderer)
        surface.SDL_FreeSurface(sf)