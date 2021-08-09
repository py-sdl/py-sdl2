import sys
import pytest
from ctypes import ArgumentError

from sdl2 import ext as sdl2ext
from sdl2.ext.resources import Resources
from sdl2.render import (
    SDL_TEXTUREACCESS_STATIC, SDL_TEXTUREACCESS_STREAMING, SDL_TEXTUREACCESS_TARGET
)
from sdl2.surface import SDL_Surface, SDL_CreateRGBSurface, SDL_FreeSurface


_ISPYPY = hasattr(sys, "pypy_version_info")


RESOURCES = Resources(__file__, "resources")

if _ISPYPY:
    import gc
    dogc = gc.collect
else:
    dogc = lambda: None


class TestSDL2ExtSpriteSystem(object):
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
