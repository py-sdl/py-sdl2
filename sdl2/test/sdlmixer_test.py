import os
import sys
import pytest
import operator
from ctypes import byref, c_int, c_uint16
import sdl2
from sdl2.stdinc import SDL_TRUE, SDL_FALSE
from sdl2 import SDL_Init, SDL_Quit, rwops, version
if sys.version_info[0] >= 3:
    from functools import reduce

sdlmixer = pytest.importorskip("sdl2.sdlmixer")


# TODO: Add full list of fuctions to test
# TODO: Add actual tests for most functions (can base off of SDL_Mixer docs)

def test_Mix_Linked_Version():
    v = sdlmixer.Mix_Linked_Version()
    assert isinstance(v.contents, version.SDL_version)
    assert v.contents.major == 2
    assert v.contents.minor == 0
    assert v.contents.patch >= 0

@pytest.mark.skipif(sdlmixer.dll.version < 2004, reason="Broken in official binaries")
def test_Mix_Init():
    SDL_Init(sdl2.SDL_INIT_AUDIO)
    supported = []
    libs = {
        'FLAC': sdlmixer.MIX_INIT_FLAC,
        'MOD': sdlmixer.MIX_INIT_MOD,
        'MP3': sdlmixer.MIX_INIT_MP3,
        'OGG': sdlmixer.MIX_INIT_OGG,
        'MID': sdlmixer.MIX_INIT_MID,
        'OPUS': sdlmixer.MIX_INIT_OPUS
    }
    for lib in libs.keys():
        flags = libs[lib]
        ret = sdlmixer.Mix_Init(flags)
        err = sdlmixer.Mix_GetError()
        if ret & flags == flags:
            supported.append(lib)
        sdlmixer.Mix_Quit()
    assert len(supported) # only fail if none supported
    print("Supported formats:")
    print(supported)
    SDL_Quit()

def test_Mix_OpenAudio():
    SDL_Init(sdl2.SDL_INIT_AUDIO)
    sdlmixer.Mix_Init(0)
    ret = sdlmixer.Mix_OpenAudio(22050, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)
    assert ret == 0
    sdlmixer.Mix_CloseAudio()
    sdlmixer.Mix_Quit()
    SDL_Quit()


class TestSDLMixer(object):
    __tags__ = ["sdl", "sdlmixer"]

    @classmethod
    def setup_class(cls):
        SDL_Init(sdl2.SDL_INIT_AUDIO)
        # Determine supported audio formats for Mix_Init
        supported = []
        libs = {
            'FLAC': sdlmixer.MIX_INIT_FLAC,
            'MOD': sdlmixer.MIX_INIT_MOD,
            'MP3': sdlmixer.MIX_INIT_MP3,
            'OGG': sdlmixer.MIX_INIT_OGG,
            'MID': sdlmixer.MIX_INIT_MID,
            'OPUS': sdlmixer.MIX_INIT_OPUS
        }
        for lib in libs.keys():
            flags = libs[lib]
            ret = sdlmixer.Mix_Init(flags)
            if ret & flags == flags:
                supported.append(lib)
            sdlmixer.Mix_Quit()
        cls.supported = supported
        # Only initialize audio formats that are supported in current binary
        flaglist = [libs[lib] for lib in supported]
        flags = reduce(operator.or_, flaglist) if len(flaglist) else 0
        sdlmixer.Mix_Init(flags)
        sdlmixer.Mix_OpenAudio(22050, sdlmixer.MIX_DEFAULT_FORMAT, 2, 1024)

    @classmethod
    def teardown_class(cls):
        sdlmixer.Mix_CloseAudio()
        sdlmixer.Mix_Quit()
        SDL_Quit()

    def test_Mix_QuerySpec(self):
        freq, channels = c_int(0), c_int(0)
        fmt = c_uint16(0)
        ret = sdlmixer.Mix_QuerySpec(byref(freq), byref(fmt), byref(channels))
        assert ret != 0
        assert freq > 0 
        assert channels > 0
        assert fmt.value in sdl2.audio.AUDIO_FORMATS

    def test_Mix_AllocateChannels(self):
        # Get number currently allocated
        current = sdlmixer.Mix_AllocateChannels(-1)
        assert current > 0
        # Try allocating a single channel
        sdlmixer.Mix_AllocateChannels(1)
        assert sdlmixer.Mix_AllocateChannels(-1) == 1
        # Reset allocated channels
        sdlmixer.Mix_AllocateChannels(current)

    def test_ChunkDecoders(self):
        decoders = []
        num = sdlmixer.Mix_GetNumChunkDecoders()
        assert num > 0
        for i in range(0, num):
            name = sdlmixer.Mix_GetChunkDecoder(i)
            assert name is not None
            assert sdlmixer.Mix_HasChunkDecoder(name) == SDL_TRUE
            decoders.append(name.decode('utf-8'))
        assert sdlmixer.Mix_HasChunkDecoder(b'blah') == SDL_FALSE
        print("Available MixChunk decoders:\n{0}".format(str(decoders)))

    def test_MusicDecoders(self):
        decoders = []
        num = sdlmixer.Mix_GetNumMusicDecoders()
        assert num > 0
        for i in range(0, num):
            name = sdlmixer.Mix_GetMusicDecoder(i)
            assert name is not None
            decoders.append(name.decode('utf-8'))
        print("Available MixMusic decoders:\n{0}".format(str(decoders)))

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
