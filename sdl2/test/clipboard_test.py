import sys
import pytest
import sdl2
from sdl2 import SDL_GetError
from sdl2 import clipboard
from sdl2.stdinc import SDL_TRUE
from .conftest import SKIP_ANNOYING

@pytest.fixture
def window(with_sdl):
    flag = sdl2.SDL_WINDOW_BORDERLESS
    w = sdl2.SDL_CreateWindow(b"Test", 10, 40, 12, 13, flag)
    assert sdl2.SDL_GetError() == b""
    assert isinstance(w.contents, sdl2.SDL_Window)
    yield w
    sdl2.SDL_DestroyWindow(w)

def is_win_or_mac():
    return sys.platform in ("win32", "cygwin", "darwin")


@pytest.mark.skipif(SKIP_ANNOYING, reason="Skip unless requested")
def test_SDL_ClipboardText(window):
    # Test retrieving text from the clipboard
    ret = clipboard.SDL_GetClipboardText()
    original_contents = ret
    assert SDL_GetError() == b""
    assert ret == None or type(ret) in (str, bytes)
    # Test whether HasClipboardText is accurate
    expected = SDL_FALSE if ret == None else SDL_TRUE
    assert clipboard.SDL_HasClipboardText() == expected
    # Set some new clipboard test and test for it
    ret = clipboard.SDL_SetClipboardText(b"test")
    assert SDL_GetError() == b""
    assert ret == 0
    assert clipboard.SDL_HasClipboardText() == SDL_TRUE
    assert clipboard.SDL_GetClipboardText() == b"test"
    # Reset original contents
    clipboard.SDL_SetClipboardText(original_contents)
