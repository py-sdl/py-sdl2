import sys
import pytest
import sdl2
from sdl2 import SDL_GetError, SDL_TRUE, SDL_FALSE
from .conftest import SKIP_ANNOYING

@pytest.fixture
def window(with_sdl):
    flag = sdl2.SDL_WINDOW_BORDERLESS
    w = sdl2.SDL_CreateWindow(b"Test", 10, 40, 12, 13, flag)
    if not isinstance(w.contents, sdl2.SDL_Window):
        assert sdl2.SDL_GetError() == b""
        assert isinstance(w.contents, sdl2.SDL_Window)
    sdl2.SDL_ClearError()
    yield w
    sdl2.SDL_DestroyWindow(w)


@pytest.mark.skipif(SKIP_ANNOYING, reason="Skip unless requested")
def test_SDL_ClipboardText(window):
    # Test retrieving text from the clipboard
    ret = sdl2.SDL_GetClipboardText()
    original_contents = ret
    assert type(ret) in (str, bytes)
    # Test whether HasClipboardText is accurate
    expected = SDL_FALSE if len(ret) == 0 else SDL_TRUE
    assert sdl2.SDL_HasClipboardText() == expected
    # Set some new clipboard test and test for it
    sdl2.SDL_ClearError()
    ret = sdl2.SDL_SetClipboardText(b"test")
    assert SDL_GetError() == b""
    assert ret == 0
    assert sdl2.SDL_HasClipboardText() == SDL_TRUE
    assert sdl2.SDL_GetClipboardText() == b"test"
    # Reset original contents
    sdl2.SDL_SetClipboardText(original_contents)
