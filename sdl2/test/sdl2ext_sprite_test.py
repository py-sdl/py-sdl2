import sys
import pytest
from ctypes import POINTER, byref, addressof

from sdl2 import ext as sdl2ext
from sdl2.render import (
    SDL_Renderer, SDL_CreateWindowAndRenderer, SDL_DestroyRenderer,
    SDL_Texture, SDL_CreateTexture
)
from sdl2.surface import SDL_CreateRGBSurface
from sdl2.video import SDL_Window, SDL_WINDOW_HIDDEN, SDL_DestroyWindow


_ISPYPY = hasattr(sys, "pypy_version_info")

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
        sf = SDL_CreateRGBSurface(0, 10, 10, 32, 0, 0, 0, 0)

        # Test with SDL_Surface
        sprite = sdl2ext.SoftwareSprite(sf.contents, False)
        assert addressof(sprite.surface) == addressof(sf.contents)
        assert not sprite.free

        # Test with SDL_Surface pointer
        sprite = sdl2ext.SoftwareSprite(sf, False)
        assert addressof(sprite.surface) == addressof(sf.contents)
        assert not sprite.free

        with pytest.raises(TypeError):
            sdl2ext.SoftwareSprite(None, True)

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
