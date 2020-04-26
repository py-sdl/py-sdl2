import sys
import pytest
import sdl2
from sdl2 import metal

macos = sys.platform == "darwin"

@pytest.mark.skip("not implemented")
@pytest.mark.skipif(sdl2.dll.version < 2012 or not macos, reason="not available")
def test_SDL_Metal_CreateDestroyView():
    pass
