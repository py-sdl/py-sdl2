import os
import sys
import pytest
import ctypes
import sdl2
from sdl2 import SDL_Init, SDL_Quit, rwops, version

sdlmixer = pytest.importorskip("sdl2.sdlmixer")

# TODO: Add full list of fuctions to test
# TODO: Add actual tests for most functions (can base off of SDL_Mixer docs)

def test_Mix_Linked_Version():
    v = sdlmixer.Mix_Linked_Version()
    assert isinstance(v.contents, version.SDL_version)
    assert v.contents.major == 2
    assert v.contents.minor == 0
    assert v.contents.patch >= 0

def test_Mix_Init():
    SDL_Init(sdl2.SDL_INIT_AUDIO)
    libs = {
        'FLAC': sdlmixer.MIX_INIT_FLAC,
        'MOD': sdlmixer.MIX_INIT_MOD,
        'MP3': sdlmixer.MIX_INIT_MP3,
        'OGG': sdlmixer.MIX_INIT_OGG,
        'MID': sdlmixer.MIX_INIT_MID
    }
    for lib in libs.keys():
        flags = libs[lib]
        ret = sdlmixer.Mix_Init(flags)
        err = sdlmixer.Mix_GetError()
        assert ret & flags == flags
        sdlmixer.Mix_Quit()
    SDL_Quit()

@pytest.mark.xfail(reason="not sure this will work with CI")
def test_Mix_OpenAudio(self):
    SDL_Init(sdl2.SDL_INIT_AUDIO)
    sdlmixer.Mix_Init(0)
    ret = sdlmixer.Mix_OpenAudio(22050, sdlmixer.MIX_DEFAULT_FORMAT, 1, 1024)
    assert ret == 0
    sdlmixer.Mix_CloseAudio()
    sdlmixer.Mix_Quit()
    SDL_Quit()

@pytest.mark.skip("not sure this will work with CI")
class TestSDLMixer(object):
    __tags__ = ["sdl", "sdlmixer"]

    @classmethod
    def setup_class(cls):
        flags = (
            sdlmixer.MIX_INIT_FLAC | sdlmixer.MIX_INIT_MOD |
            sdlmixer.MIX_INIT_MP3  | sdlmixer.MIX_INIT_OGG |
            sdlmixer.MIX_INIT_MID
        )
        SDL_Init(sdl2.SDL_INIT_AUDIO)
        sdlmixer.Mix_Init(flags)
        sdlmixer.Mix_OpenAudio(22050, sdlmixer.MIX_DEFAULT_FORMAT, 1, 1024)

    @classmethod
    def teardown_class(cls):
        sdlmixer.Mix_CloseAudio()
        sdlmixer.Mix_Quit()
        SDL_Quit()

    @pytest.mark.skip("not implemented")
    def test_Mix_QuerySpec(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_AllocateChannels(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_ChunkDecoders(self):
        # Mix_GetNumChunkDecoders
        # Mix_GetChunkDecoder
        # Mix_HasChunkDecoder
        pass

    @pytest.mark.skip("not implemented")
    def test_MusicDecoders(self):
        # Mix_GetNumMusicDecoders
        # Mix_GetMusicDecoder
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_LoadWAV(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_LoadWAV_RW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_LoadMUS(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_LoadMUS_RW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_LoadMUSType_RW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_QuickLoad_WAV(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_QuickLoad_RAW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_GetMusicType(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_Chunk(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_Music(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_MusicType(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Mix_Fading(self):
        pass
