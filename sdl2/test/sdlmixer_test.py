import os
import sys
import pytest
import ctypes
from sdl2 import SDL_Init, SDL_Quit, rwops, version

try:
    from sdl2 import sdlmixer
    _HASSDLMIXER=True
except:
    _HASSDLMIXER=False

@pytest.mark.skipif(not _HASSDLMIXER, 
    reason="SDL2_mixer library could not be loaded")
class TestSDLMixer(object):
    __tags__ = ["sdl", "sdlmixer"]

    @classmethod
    def setup_class(cls):
        sdlmixer.Mix_Init(0)

    @classmethod
    def teardown_class(cls):
        sdlmixer.Mix_Quit()

    def test_Mix_Linked_Version(self):
        v = sdlmixer.Mix_Linked_Version()
        assert isinstance(v.contents, version.SDL_version)
        assert v.contents.major == 2
        assert v.contents.minor == 0
        assert v.contents.patch >= 2
