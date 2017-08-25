import os
import sys
import unittest
import ctypes
from sdl2 import SDL_Init, SDL_Quit, rwops, version

try:
    from sdl2 import sdlmixer
    _HASSDLMIXER=True
except:
    _HASSDLMIXER=False

@unittest.skipIf(not _HASSDLMIXER, "SDL2_mixer library could not be loaded")
class SDLMixerTest(unittest.TestCase):
    __tags__ = ["sdl", "sdlmixer"]

    @classmethod
    def setUpClass(cls):
        sdlmixer.Mix_Init(0)

    @classmethod
    def tearDownClass(cls):
        sdlmixer.Mix_Quit()

    def test_Mix_Linked_Version(self):
        v = sdlmixer.Mix_Linked_Version()
        self.assertIsInstance(v.contents, version.SDL_version)
        self.assertEqual(v.contents.major, 2)
        self.assertEqual(v.contents.minor, 0)
        self.assertEqual(v.contents.patch, 1)

if __name__ == '__main__':
    sys.exit(unittest.main())
