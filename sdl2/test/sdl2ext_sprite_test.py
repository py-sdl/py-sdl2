import sys
import pytest
from ctypes import ArgumentError, POINTER, byref
from sdl2.ext.resources import Resources
from sdl2 import ext as sdl2ext
from sdl2.surface import SDL_Surface, SDL_CreateRGBSurface, SDL_FreeSurface
from sdl2.video import SDL_Window, SDL_WINDOW_HIDDEN, SDL_DestroyWindow
from sdl2.render import SDL_Renderer, SDL_CreateWindowAndRenderer, \
    SDL_DestroyRenderer, SDL_CreateTexture, SDL_Texture, \
    SDL_TEXTUREACCESS_STATIC, SDL_TEXTUREACCESS_STREAMING, \
    SDL_TEXTUREACCESS_TARGET

_ISPYPY = hasattr(sys, "pypy_version_info")

RESOURCES = Resources(__file__, "resources")

if _ISPYPY:
    import gc
    dogc = gc.collect
else:
    dogc = lambda: None

class MSprite(sdl2ext.Sprite):
    def __init__(self, w=0, h=0):
        super(MSprite, self).__init__()
        self._size = w, h

    @property
    def size(self):
        return self._size


class TestSDL2ExtSprite(object):
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

    def check_pixels(self, view, w, h, sprite, c1, c2, cx=0, cy=0):
        msg = "color mismatch at %d,%d: %d not in %s"
        cx = cx + sprite.x
        cy = cy + sprite.y
        cw, ch = sprite.size
        cmy = cy + ch
        cmx = cx + cw
        for y in range(w):
            for x in range(h):
                if cy <= y < cmy and cx <= x < cmx:
                    assert view[y][x] == c1, msg % (x, y, view[y][x], c1)
                else:
                    assert view[y][x] in c2, msg % (x, y, view[y][x], c2)

    def check_areas(self, view, w, h, rects, c1, c2):
        def _inarea(x, y, rs):
            for r in rs:
                if (x >= r[0] and x < (r[0] + r[2]) and
                        y >= r[1] and y < (r[1] + r[3])):
                    return True
            return False
        msg = "color mismatch at %d,%d: %d not in %s"
        for y in range(w):
            for x in range(h):
                if _inarea(x, y, rects):
                    assert view[y][x] == c1, msg % (x, y, view[y][x], c1)
                else:
                    assert view[y][x] in c2, msg % (x, y, view[y][x], c2)

    def check_lines(self, view, w, h, points, c1, c2):
        def _online(x, y, pts):
            for p1, p2 in pts:
                if sdl2ext.point_on_line(p1, p2, (x, y)):
                    return True
            return False
        msg = "color mismatch at %d,%d: %d not in %s"
        for y in range(w):
            for x in range(h):
                if _online(x, y, points):
                    assert view[y][x] == c1, msg % (x, y, view[y][x], c1)
                else:
                    assert view[y][x] in c2, msg % (x, y, view[y][x], c2)

    def test_SpriteFactory(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        assert isinstance(factory, sdl2ext.SpriteFactory)
        assert factory.default_args == {}

        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE, bananas="tasty")
        assert isinstance(factory, sdl2ext.SpriteFactory)
        assert factory.default_args == {"bananas": "tasty"}

        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)

        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        assert isinstance(factory, sdl2ext.SpriteFactory)

        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        assert isinstance(factory, sdl2ext.SpriteFactory)
        assert factory.default_args == {"renderer": renderer}

        with pytest.raises(ValueError):
            sdl2ext.SpriteFactory("Test")
        with pytest.raises(ValueError):
            sdl2ext.SpriteFactory(-456)
        with pytest.raises(ValueError):
            sdl2ext.SpriteFactory(123)
        with pytest.raises(ValueError):
            sdl2ext.SpriteFactory(sdl2ext.TEXTURE)
        dogc()

    def test_SpriteFactory_create_sprite(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        for w in range(0, 100):
            for h in range(0, 100):
                for bpp in (1, 4, 8, 12, 15, 16, 24, 32):
                    sprite = sfactory.create_sprite(size=(w, h), bpp=bpp)
                    assert isinstance(sprite, sdl2ext.SoftwareSprite)

                if w == 0 or h == 0:
                    with pytest.raises(sdl2ext.SDLError):
                        tfactory.create_sprite(size=(w, h))
                    continue
                sprite = tfactory.create_sprite(size=(w, h))
                assert isinstance(sprite, sdl2ext.TextureSprite)
        dogc()

    def test_SpriteFactory_create_software_sprite(self):
        factory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        for w in range(0, 100):
            for h in range(0, 100):
                for bpp in (1, 4, 8, 12, 15, 16, 24, 32):
                    sprite = factory.create_software_sprite((w, h), bpp)
                    assert isinstance(sprite, sdl2ext.SoftwareSprite)

        #self.assertRaises(ValueError, factory.create_software_sprite, (-1,-1))
        #self.assertRaises(ValueError, factory.create_software_sprite, (-10,5))
        #self.assertRaises(ValueError, factory.create_software_sprite, (10,-5))
        with pytest.raises(TypeError):
            factory.create_software_sprite(size=None)
        with pytest.raises(sdl2ext.SDLError):
            factory.create_software_sprite(size=(10, 10), bpp=-1)
        with pytest.raises(TypeError):
            factory.create_software_sprite(masks=5)
        with pytest.raises((ArgumentError, TypeError)):
            factory.create_software_sprite(size=(10, 10),
                          masks=(None, None, None, None))
        with pytest.raises((ArgumentError, TypeError)):
            factory.create_software_sprite(size=(10, 10),
                          masks=("Test", 1, 2, 3))
        dogc()

    def test_SpriteFactory_create_texture_sprite(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        for w in range(1, 100):
            for h in range(1, 100):
                sprite = factory.create_texture_sprite(renderer, size=(w, h))
                assert isinstance(sprite, sdl2ext.TextureSprite)
                del sprite

        # Test different access flags
        for flag in (SDL_TEXTUREACCESS_STATIC, SDL_TEXTUREACCESS_STREAMING,
                     SDL_TEXTUREACCESS_TARGET):
            sprite = factory.create_texture_sprite(renderer, size=(64, 64),
                                                   access=flag)
            assert isinstance(sprite, sdl2ext.TextureSprite)
            del sprite
        dogc()

    def test_SpriteFactory_from_image(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        for suffix in ("tif", "png", "jpg"):
            imgname = RESOURCES.get_path("surfacetest.%s" % suffix)
            tsprite = tfactory.from_image(imgname)
            assert isinstance(tsprite, sdl2ext.TextureSprite)
            ssprite = sfactory.from_image(imgname)
            assert isinstance(ssprite, sdl2ext.SoftwareSprite)

        for factory in (tfactory, sfactory):
            with pytest.raises((ArgumentError, ValueError)):
                factory.from_image(None)
            #self.assertRaises((IOError, SDLError),
            #                  factory.from_image, "banana")
            if not _ISPYPY:
                with pytest.raises(ArgumentError):
                    factory.from_image(12345)
        dogc()

    @pytest.mark.skip("not implemented")
    def test_SpriteFactory_from_object(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

    def test_SpriteFactory_from_surface(self):
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)

        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        tsprite = tfactory.from_surface(sf.contents)
        assert isinstance(tsprite, sdl2ext.TextureSprite)
        ssprite = sfactory.from_surface(sf.contents)
        assert isinstance(ssprite, sdl2ext.SoftwareSprite)
        SDL_FreeSurface(sf)

        for factory in (tfactory, sfactory):
            with pytest.raises((sdl2ext.SDLError, AttributeError, ArgumentError,
                               TypeError)):
                factory.from_surface(None)
            with pytest.raises((AttributeError, ArgumentError, TypeError)):
                factory.from_surface("test")
            # TODO: crashes pypy 2.0
            #self.assertRaises((AttributeError, ArgumentError, TypeError),
            #                  factory.from_surface, 1234)
        dogc()

    def test_SpriteFactory_from_text(self):
        sfactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
        fm = sdl2ext.FontManager(RESOURCES.get_path("tuffy.ttf"))

        # No Fontmanager passed
        with pytest.raises(KeyError):
            sfactory.from_text("Test")

        # Passing various keywords arguments
        sprite = sfactory.from_text("Test", fontmanager=fm)
        assert isinstance(sprite, sdl2ext.SoftwareSprite)

        sprite = sfactory.from_text("Test", fontmanager=fm, alias="tuffy")
        assert isinstance(sprite, sdl2ext.SoftwareSprite)

        # Get text from a texture sprite factory
        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        tfactory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE,
                                         renderer=renderer,
                                         fontmanager=fm)
        sprite = tfactory.from_text("Test", alias="tuffy")
        assert isinstance(sprite, sdl2ext.TextureSprite)
        dogc()

    def test_SpriteRenderSystem(self):
        renderer = sdl2ext.SpriteRenderSystem()
        assert isinstance(renderer, sdl2ext.SpriteRenderSystem)
        assert renderer.sortfunc is not None
        assert sdl2ext.Sprite in renderer.componenttypes

    def test_SpriteRenderSystem_sortfunc(self):
        def func(p):
            pass

        renderer = sdl2ext.SpriteRenderSystem()
        assert renderer.sortfunc is not None
        renderer.sortfunc = func
        assert renderer.sortfunc == func

        def setf(x, f):
            x.sortfunc = f
        with pytest.raises(TypeError):
            setf(renderer, None)
        with pytest.raises(TypeError):
            setf(renderer, "Test")
        with pytest.raises(TypeError):
            setf(renderer, 1234)

    @pytest.mark.skip("not implemented")
    def test_SpriteRenderSystem_render(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SpriteRenderSystem_process(self):
        pass

    def test_SoftwareSpriteRenderSystem(self):
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSpriteRenderSystem()
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSpriteRenderSystem(None)
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSpriteRenderSystem("Test")
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSpriteRenderSystem(12345)

        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.SoftwareSpriteRenderSystem(window)
        assert isinstance(renderer, sdl2ext.SpriteRenderSystem)
        assert renderer.window == window.window
        assert isinstance(renderer.surface, SDL_Surface)

        renderer = sdl2ext.SoftwareSpriteRenderSystem(window.window)
        assert isinstance(renderer, sdl2ext.SpriteRenderSystem)
        assert renderer.window == window.window
        assert isinstance(renderer.surface, SDL_Surface)

        assert renderer.sortfunc is not None
        assert not (sdl2ext.Sprite in renderer.componenttypes)
        assert sdl2ext.SoftwareSprite in renderer.componenttypes
        dogc()

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_SoftwareSpriteRenderSystem_render(self):
        sf1 = SDL_CreateRGBSurface(0, 12, 7, 32, 0, 0, 0, 0)
        sp1 = sdl2ext.SoftwareSprite(sf1.contents, True)
        sdl2ext.fill(sp1, 0xFF0000)

        sf2 = SDL_CreateRGBSurface(0, 3, 9, 32, 0, 0, 0, 0)
        sp2 = sdl2ext.SoftwareSprite(sf2.contents, True)
        sdl2ext.fill(sp2, 0x00FF00)
        sprites = [sp1, sp2]

        window = sdl2ext.Window("Test", size=(20, 20))
        renderer = sdl2ext.SoftwareSpriteRenderSystem(window)
        assert isinstance(renderer, sdl2ext.SpriteRenderSystem)

        with pytest.raises(AttributeError):
            renderer.render(None, None, None)
        with pytest.raises(AttributeError):
            renderer.render([None, None],
                          None, None)

        for x, y in ((0, 0), (3, 3), (20, 20), (1, 12), (5, 6)):
            sp1.position = x, y
            renderer.render(sp1)
            view = sdl2ext.PixelView(renderer.surface)
            self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0,))
            del view
            sdl2ext.fill(renderer.surface, 0x0)
        sp1.position = 0, 0
        sp2.position = 14, 1
        renderer.render(sprites)
        view = sdl2ext.PixelView(renderer.surface)
        self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0, 0x00FF00))
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0, 0xFF0000))
        del view
        sdl2ext.fill(renderer.surface, 0x0)
        renderer.render(sprites, 1, 2)
        view = sdl2ext.PixelView(renderer.surface)
        self.check_pixels(view, 20, 20, sp1, 0xFF0000, (0x0, 0x00FF00), 1, 2)
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0, 0xFF0000), 1, 2)
        del view

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_SoftwareSpriteRenderSystem_process(self):
        sf1 = SDL_CreateRGBSurface(0, 5, 10, 32, 0, 0, 0, 0)
        sp1 = sdl2ext.SoftwareSprite(sf1.contents, True)
        sp1.depth = 0
        sdl2ext.fill(sp1, 0xFF0000)

        sf2 = SDL_CreateRGBSurface(0, 5, 10, 32, 0, 0, 0, 0)
        sp2 = sdl2ext.SoftwareSprite(sf2.contents, True)
        sp2.depth = 99
        sdl2ext.fill(sp2, 0x00FF00)
        sprites = [sp1, sp2]

        window = sdl2ext.Window("Test", size=(20, 20))
        renderer = sdl2ext.SoftwareSpriteRenderSystem(window)

        renderer.process("fakeworld", sprites)
        view = sdl2ext.PixelView(renderer.surface)
        # Only sp2 wins, since its depth is higher
        self.check_pixels(view, 20, 20, sp1, 0x00FF00, (0x0,))
        self.check_pixels(view, 20, 20, sp2, 0x00FF00, (0x0,))
        del view

        with pytest.raises(TypeError):
            renderer.process(None, None)

    @pytest.mark.skip("not implemented")
    def test_TextureSpriteRenderSystem(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_TextureSpriteRenderSystem_render(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_TextureSpriteRenderSystem_process(self):
        pass

    def test_Sprite(self):
        sprite = MSprite()
        assert isinstance(sprite, MSprite)
        assert isinstance(sprite, sdl2ext.Sprite)

    def test_Sprite_position_xy(self):
        sprite = MSprite()
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            assert sprite.position == (x, y)
            sprite.x = x + 1
            sprite.y = y + 1
            assert sprite.position == (x + 1, y + 1)

    def test_Sprite_area(self):
        for w in range(0, 200):
            for h in range(0, 200):
                sprite = MSprite(w, h)
                assert sprite.size == (w, h)
                assert sprite.area == (0, 0, w, h)
                sprite.position = w, h
                assert sprite.area == (w, h, 2 * w, 2 * h)

    def test_SoftwareSprite(self):
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSprite(None, None)
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSprite(None, True)
        with pytest.raises(TypeError):
            sdl2ext.SoftwareSprite(None, False)

        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, False)
        # TODO: the following assert fails...
        # self.assertEqual(sprite.surface, sf.contents)
        assert not sprite.free

        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        # TODO: the following assert fails...
        # self.assertEqual(sprite.surface, sf.contents)
        assert sprite.free

    def test_SoftwareSprite_repr(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        assert repr(sprite) == "SoftwareSprite(size=(10, 10), bpp=32)"

    def test_SoftwareSprite_position_xy(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        assert isinstance(sprite, sdl2ext.SoftwareSprite)
        assert sprite.position == (0, 0)
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            assert sprite.position == (x, y)
            sprite.x = x + 1
            sprite.y = y + 1
            assert sprite.position == (x + 1, y + 1)

    def test_SoftwareSprite_size(self):
        for w in range(0, 200):
            for h in range(0, 200):
                sf = SDL_CreateRGBSurface(0, w, h, 32, 0, 0, 0, 0)
                sprite = sdl2ext.SoftwareSprite(sf.contents, True)
                assert isinstance(sprite, sdl2ext.SoftwareSprite)
                assert sprite.size == (w, h)

    def test_SoftwareSprite_area(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)
        sprite = sdl2ext.SoftwareSprite(sf.contents, True)
        assert sprite.area == (0, 0, 10, 10)

        def setarea(s, v):
            s.area = v
        with pytest.raises(AttributeError):
            setarea(sprite, (1, 2, 3, 4))

        sprite.position = 7, 3
        assert sprite.area == (7, 3, 17, 13)
        sprite.position = -22, 99
        assert sprite.area == (-22, 99, -12, 109)

    def test_TextureSprite(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))

        tex = SDL_CreateTexture(renderer, 0, 0, 10, 10)
        assert isinstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        assert isinstance(sprite, sdl2ext.TextureSprite)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        dogc()

    def test_TextureSprite_position_xy(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        tex = SDL_CreateTexture(renderer, 0, 0, 10, 10)
        assert isinstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        assert isinstance(sprite, sdl2ext.TextureSprite)
        assert sprite.position == (0, 0)
        positions = [(x, y) for x in range(-50, 50) for y in range(-50, 50)]
        for x, y in positions:
            sprite.position = x, y
            assert sprite.position == (x, y)
            sprite.x = x + 1
            sprite.y = y + 1
            assert sprite.position == (x + 1, y + 1)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        dogc()

    def test_TextureSprite_size(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        for w in range(1, 200):
            for h in range(1, 200):
                tex = SDL_CreateTexture(renderer, 0, 0, w, h)
                assert isinstance(tex.contents, SDL_Texture)
                sprite = sdl2ext.TextureSprite(tex.contents)
                assert isinstance(sprite, sdl2ext.TextureSprite)
                assert sprite.size == (w, h)
                del sprite
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        dogc()

    def test_TextureSprite_area(self):
        window = POINTER(SDL_Window)()
        renderer = POINTER(SDL_Renderer)()
        SDL_CreateWindowAndRenderer(10, 10, SDL_WINDOW_HIDDEN,
                                    byref(window), byref(renderer))
        tex = SDL_CreateTexture(renderer, 0, 0, 10, 20)
        assert isinstance(tex.contents, SDL_Texture)
        sprite = sdl2ext.TextureSprite(tex.contents)
        assert isinstance(sprite, sdl2ext.TextureSprite)
        assert sprite.area == (0, 0, 10, 20)

        def setarea(s, v):
            s.area = v

        with pytest.raises(AttributeError):
            setarea(sprite, (1, 2, 3, 4))
        sprite.position = 7, 3
        assert sprite.area == (7, 3, 17, 23)
        sprite.position = -22, 99
        assert sprite.area == (-22, 99, -12, 119)
        SDL_DestroyRenderer(renderer)
        SDL_DestroyWindow(window)
        dogc()

    def test_Renderer(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0).contents

        renderer = sdl2ext.Renderer(sf)
        assert renderer.rendertarget == sf
        assert isinstance(renderer.sdlrenderer.contents, SDL_Renderer)
        del renderer

        # Deprecated
        renderer = sdl2ext.Renderer(sf)
        assert renderer.rendertarget == sf
        assert isinstance(renderer.sdlrenderer.contents, SDL_Renderer)
        del renderer


        sprite = sdl2ext.SoftwareSprite(sf, True)
        renderer = sdl2ext.Renderer(sprite)
        assert renderer.rendertarget == sprite
        assert isinstance(renderer.sdlrenderer.contents, SDL_Renderer)
        del renderer
        dogc()

        window = sdl2ext.Window("Test", size=(1, 1))
        renderer = sdl2ext.Renderer(window)
        assert renderer.rendertarget == window
        assert isinstance(renderer.sdlrenderer.contents, SDL_Renderer)
        del renderer
        dogc()

        sdlwindow = window.window
        renderer = sdl2ext.Renderer(sdlwindow)
        assert renderer.rendertarget == sdlwindow
        assert isinstance(renderer.sdlrenderer.contents, SDL_Renderer)
        del renderer
        del window

        with pytest.raises(TypeError):
            sdl2ext.Renderer(None)
        with pytest.raises(TypeError):
            sdl2ext.Renderer(1234)
        with pytest.raises(TypeError):
            sdl2ext.Renderer("test")
        dogc()

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_color(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32,
                                  0xFF000000,
                                  0x00FF0000,
                                  0x0000FF00,
                                  0x000000FF)
        renderer = sdl2ext.Renderer(sf.contents)
        assert isinstance(renderer.color, sdl2ext.Color)
        assert renderer.color == sdl2ext.Color(0, 0, 0, 0)
        renderer.color = 0x00FF0000
        assert renderer.color == sdl2ext.Color(0xFF, 0, 0, 0)
        renderer.clear()
        view = sdl2ext.PixelView(sf.contents)
        self.check_areas(view, 10, 10, [[0, 0, 10, 10]], 0xFF000000, (0x0,))
        del view
        renderer.color = 0xAABBCCDD
        assert renderer.color == sdl2ext.Color(0xBB, 0xCC, 0xDD, 0xAA)
        renderer.clear()
        view = sdl2ext.PixelView(sf.contents)
        self.check_areas(view, 10, 10, [[0, 0, 10, 10]], 0xBBCCDDAA, (0x0,))
        del view
        del renderer
        SDL_FreeSurface(sf)
        dogc()

    @pytest.mark.skip("not implemented")
    def test_Renderer_blendmode(self):
        pass

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_clear(self):
        sf = SDL_CreateRGBSurface(0, 10, 10, 32,
                                  0xFF000000,
                                  0x00FF0000,
                                  0x0000FF00,
                                  0x000000FF)
        renderer = sdl2ext.Renderer(sf.contents)
        assert isinstance(renderer.color, sdl2ext.Color)
        assert renderer.color == sdl2ext.Color(0, 0, 0, 0)
        renderer.color = 0x00FF0000
        assert renderer.color == sdl2ext.Color(0xFF, 0, 0, 0)
        renderer.clear()
        view = sdl2ext.PixelView(sf.contents)
        self.check_areas(view, 10, 10, [[0, 0, 10, 10]], 0xFF000000, (0x0,))
        del view
        renderer.clear(0xAABBCCDD)
        assert renderer.color == sdl2ext.Color(0xFF, 0, 0, 0)
        view = sdl2ext.PixelView(sf.contents)
        self.check_areas(view, 10, 10, [[0, 0, 10, 10]], 0xBBCCDDAA, (0x0,))
        del view
        del renderer
        SDL_FreeSurface(sf)
        dogc()

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_copy(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.Renderer(surface)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        w, h = 32, 32
        sp = factory.from_color(0xFF0000, (w, h))
        sp.x, sp.y = 40, 50
        renderer.copy(sp, (0, 0, w, h), (sp.x, sp.y, w, h))
        view = sdl2ext.PixelView(surface)
        self.check_pixels(view, 128, 128, sp, 0xFF0000, (0x0,))
        del view

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_draw_line(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.Renderer(surface)
        renderer.draw_line((20, 10, 20, 86), 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_lines(view, 128, 128,
                         [((20, 10), (20, 86))], 0x0000FF, (0x0,))
        del view

    @pytest.mark.skip("not implemented")
    def test_Renderer_draw_point(self):
        pass

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_draw_rect(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.Renderer(surface)
        renderer.draw_rect((40, 50, 32, 32), 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_lines(view, 128, 128, [
            ((40, 50), (71, 50)),
            ((40, 50), (40, 81)),
            ((40, 81), (71, 81)),
            ((71, 50), (71, 81))], 0x0000FF, (0x0,))
        del view
        sdl2ext.fill(surface, 0x0)
        renderer.draw_rect([(5, 5, 10, 10), (20, 15, 8, 10)], 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_lines(view, 128, 128, [
            ((5, 5), (14, 5)),
            ((5, 5), (5, 14)),
            ((5, 14), (14, 14)),
            ((14, 5), (14, 14)),
            ((20, 15), (27, 15)),
            ((20, 15), (20, 24)),
            ((20, 24), (27, 24)),
            ((27, 15), (27, 24))], 0x0000FF, (0x0,))
        del view

    @pytest.mark.skipif(_ISPYPY, 
        reason="PyPy's ctypes can't do byref(value, offset)")
    def test_Renderer_fill(self):
        surface = SDL_CreateRGBSurface(0, 128, 128, 32, 0, 0, 0, 0).contents
        sdl2ext.fill(surface, 0x0)
        renderer = sdl2ext.Renderer(surface)
        factory = sdl2ext.SpriteFactory(sdl2ext.TEXTURE, renderer=renderer)
        w, h = 32, 32
        sp = factory.from_color(0xFF0000, (w, h))
        sp.x, sp.y = 40, 50
        renderer.fill((sp.x, sp.y, w, h), 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_pixels(view, 128, 128, sp, 0x0000FF, (0x0,))
        del view
        sdl2ext.fill(surface, 0x0)
        renderer.fill([(5, 5, 10, 10), (20, 15, 8, 10)], 0x0000FF)
        view = sdl2ext.PixelView(surface)
        self.check_areas(view, 128, 128, [(5, 5, 10, 10), (20, 15, 8, 10)],
                         0x0000FF, (0x0,))
        del view
