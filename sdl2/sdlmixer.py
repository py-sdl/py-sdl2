import os
from ctypes import Structure, CFUNCTYPE, c_int, c_char_p, c_void_p, c_double
from ctypes import POINTER as _P
from .dll import DLL, SDLFunc
from .version import SDL_version, SDL_VERSIONNUM
from .audio import AUDIO_S16LSB, AUDIO_S16MSB, SDL_MIX_MAXVOLUME
from .stdinc import Uint8, Uint16, Uint32, Sint16, SDL_bool
from .endian import SDL_LIL_ENDIAN, SDL_BYTEORDER
from .rwops import SDL_RWops, SDL_RWFromFile
from .error import SDL_SetError, SDL_GetError, SDL_ClearError

__all__ = [
    # Structs
    "Mix_Chunk", "Mix_Music",

    # Defines
    "SDL_MIXER_MAJOR_VERSION", "SDL_MIXER_MINOR_VERSION",
    "SDL_MIXER_PATCHLEVEL", "MIX_MAJOR_VERSION", "MIX_MINOR_VERSION",
    "MIX_PATCHLEVEL", "MIX_CHANNELS", "MIX_DEFAULT_FREQUENCY",
    "MIX_DEFAULT_FORMAT", "MIX_DEFAULT_CHANNELS", "MIX_MAX_VOLUME",
    "MIX_CHANNEL_POST", "MIX_EFFECTSMAXSPEED",

    # Enums
    "MIX_InitFlags",
    "MIX_INIT_FLAC", "MIX_INIT_MOD", "MIX_INIT_MP3", "MIX_INIT_OGG",
    "MIX_INIT_MID", "MIX_INIT_OPUS",

    "Mix_Fading",
    "MIX_NO_FADING", "MIX_FADING_OUT", "MIX_FADING_IN",

    "Mix_MusicType",
    "MUS_NONE", "MUS_CMD", "MUS_WAV", "MUS_MOD", "MUS_MID", "MUS_OGG",
    "MUS_MP3", "MUS_MP3_MAD_UNUSED", "MUS_FLAC", "MUS_MODPLUG_UNUSED",
    "MUS_OPUS",
    
    # Macro Functions
    "SDL_MIXER_VERSION",  "MIX_VERSION", "SDL_MIXER_COMPILEDVERSION",
    "SDL_MIXER_VERSION_ATLEAST", "Mix_LoadWAV", "Mix_PlayChannel",
    "Mix_FadeInChannel",

    "Mix_Linked_Version",  "Mix_Init", "Mix_Quit", "Mix_OpenAudioDevice",
    "Mix_OpenAudio", "Mix_AllocateChannels", "Mix_QuerySpec",
    "Mix_LoadWAV_RW", "Mix_LoadMUS", "Mix_LoadMUS_RW",
    "Mix_LoadMUSType_RW", "Mix_QuickLoad_WAV", "Mix_QuickLoad_RAW",
    "Mix_FreeChunk", "Mix_FreeMusic", "Mix_GetNumChunkDecoders",
    "Mix_GetChunkDecoder", "Mix_GetNumMusicDecoders",
    "Mix_HasChunkDecoder", #"Mix_HasMusicDecoder",
    "Mix_GetMusicDecoder", "Mix_GetMusicType", 
    "Mix_SetPostMix", "Mix_HookMusic", 
    "Mix_HookMusicFinished", "Mix_GetMusicHookData", 
    "Mix_ChannelFinished",  "Mix_RegisterEffect", "Mix_UnregisterEffect",
    "Mix_UnregisterAllEffects",  "Mix_SetPanning",
    "Mix_SetPosition", "Mix_SetDistance", "Mix_SetReverseStereo",
    "Mix_ReserveChannels", "Mix_GroupChannel", "Mix_GroupChannels",
    "Mix_GroupAvailable", "Mix_GroupCount", "Mix_GroupOldest",
    "Mix_GroupNewer", "Mix_PlayChannelTimed",
    "Mix_PlayMusic", "Mix_FadeInMusic", "Mix_FadeInMusicPos",
    "Mix_FadeInChannelTimed", "Mix_Volume",
    "Mix_VolumeChunk", "Mix_VolumeMusic", "Mix_HaltChannel",
    "Mix_HaltGroup", "Mix_HaltMusic", "Mix_ExpireChannel",
    "Mix_FadeOutChannel", "Mix_FadeOutGroup", "Mix_FadeOutMusic",
    "Mix_FadingMusic", "Mix_FadingChannel", "Mix_Pause", "Mix_Resume",
    "Mix_Paused", "Mix_PauseMusic", "Mix_ResumeMusic", "Mix_RewindMusic",
    "Mix_PausedMusic", "Mix_SetMusicPosition", "Mix_Playing",
    "Mix_PlayingMusic", "Mix_SetMusicCMD", "Mix_SetSynchroValue",
    "Mix_GetSynchroValue", "Mix_SetSoundFonts", "Mix_GetSoundFonts",
    "Mix_EachSoundFont", "Mix_GetChunk",
    "Mix_CloseAudio", "Mix_SetError", "Mix_GetError", "Mix_ClearError",

    # Callback Functions
    "channel_finished", "music_finished", "mix_func", "soundfont_function",
    "Mix_EffectFunc_t", "Mix_EffectDone_t",

    # Python Functions
    "get_dll_file"
]

try:
    dll = DLL("SDL2_mixer", ["SDL2_mixer", "SDL2_mixer-2.0"],
              os.getenv("PYSDL2_DLL_PATH"))
except RuntimeError as exc:
    raise ImportError(exc)


def get_dll_file():
    """Gets the file name of the loaded SDL2_mixer library."""
    return dll.libfile

_bind = dll.bind_function


# Constants, enums, type definitions, and macros

SDL_MIXER_MAJOR_VERSION = 2
SDL_MIXER_MINOR_VERSION = 0
SDL_MIXER_PATCHLEVEL = 4

def SDL_MIXER_VERSION(x):
    x.major = SDL_MIXER_MAJOR_VERSION
    x.minor = SDL_MIXER_MINOR_VERSION
    x.patch = SDL_MIXER_PATCHLEVEL

MIX_MAJOR_VERSION = SDL_MIXER_MAJOR_VERSION
MIX_MINOR_VERSION = SDL_MIXER_MINOR_VERSION
MIX_PATCHLEVEL = SDL_MIXER_PATCHLEVEL
MIX_VERSION = SDL_MIXER_VERSION

SDL_MIXER_COMPILEDVERSION = SDL_VERSIONNUM(SDL_MIXER_MAJOR_VERSION, SDL_MIXER_MINOR_VERSION, SDL_MIXER_PATCHLEVEL)
SDL_MIXER_VERSION_ATLEAST = lambda x, y, z: (SDL_MIXER_COMPILEDVERSION >= SDL_VERSIONNUM(x, y, z))

MIX_InitFlags = c_int
MIX_INIT_FLAC = 0x00000001
MIX_INIT_MOD =  0x00000002
MIX_INIT_MP3 = 0x00000008
MIX_INIT_OGG = 0x000000010
MIX_INIT_MID = 0x00000020
MIX_INIT_OPUS = 0x00000040

Mix_Fading = c_int
MIX_NO_FADING = 0
MIX_FADING_OUT = 1
MIX_FADING_IN = 2
Mix_MusicType = c_int
MUS_NONE = 0
MUS_CMD = 1
MUS_WAV = 2
MUS_MOD = 3
MUS_MID = 4
MUS_OGG = 5
MUS_MP3 = 6
MUS_MP3_MAD_UNUSED = 7
MUS_FLAC = 9
MUS_MODPLUG_UNUSED = 10
MUS_OPUS = 11

MIX_CHANNELS = 8
MIX_DEFAULT_FREQUENCY = 22050
if SDL_BYTEORDER == SDL_LIL_ENDIAN:
    MIX_DEFAULT_FORMAT = AUDIO_S16LSB
else:
    MIX_DEFAULT_FORMAT = AUDIO_S16MSB
MIX_DEFAULT_CHANNELS = 2
MIX_MAX_VOLUME = SDL_MIX_MAXVOLUME

MIX_CHANNEL_POST = -2
MIX_EFFECTSMAXSPEED = "MIX_EFFECTSMAXSPEED"

class Mix_Chunk(Structure):
    _fields_ = [("allocated", c_int),
                ("abuf", _P(Uint8)),
                ("alen", Uint32),
                ("volume", Uint8)]

class Mix_Music(c_void_p):
    pass

mix_func = CFUNCTYPE(None, c_void_p, _P(Uint8), c_int)
music_finished = CFUNCTYPE(None)
channel_finished = CFUNCTYPE(None, c_int)
Mix_EffectFunc_t = CFUNCTYPE(None, c_int, c_void_p, c_int, c_void_p)
Mix_EffectDone_t = CFUNCTYPE(None, c_int, c_void_p)
soundfont_function = CFUNCTYPE(c_int, c_char_p, c_void_p)


# Raw ctypes function definitions

_funcdefs = [
    SDLFunc("Mix_Linked_Version", None, _P(SDL_version)),
    SDLFunc("Mix_Init", [c_int], c_int),
    SDLFunc("Mix_Quit"),
    SDLFunc("Mix_OpenAudio", [c_int, Uint16, c_int, c_int], c_int),
    SDLFunc("Mix_OpenAudioDevice", [c_int, Uint16, c_int, c_int, c_char_p, c_int], c_int, added='2.0.2'),
    SDLFunc("Mix_AllocateChannels", [c_int], c_int),
    SDLFunc("Mix_QuerySpec", [_P(c_int), _P(Uint16), _P(c_int)], c_int),
    SDLFunc("Mix_LoadWAV_RW", [_P(SDL_RWops), c_int], _P(Mix_Chunk)),
    SDLFunc("Mix_LoadMUS", [c_char_p], _P(Mix_Music)),
    SDLFunc("Mix_LoadMUS_RW", [_P(SDL_RWops)], _P(Mix_Music)),
    SDLFunc("Mix_LoadMUSType_RW", [_P(SDL_RWops), Mix_MusicType, c_int], _P(Mix_Music)),
    SDLFunc("Mix_QuickLoad_WAV", [_P(Uint8)], _P(Mix_Chunk)),
    SDLFunc("Mix_QuickLoad_RAW", [_P(Uint8), Uint32], _P(Mix_Chunk)),
    SDLFunc("Mix_FreeChunk", [_P(Mix_Chunk)]),
    SDLFunc("Mix_FreeMusic", [_P(Mix_Music)]),
    SDLFunc("Mix_GetNumChunkDecoders", None, c_int),
    SDLFunc("Mix_GetChunkDecoder", [c_int], c_char_p),
    SDLFunc("Mix_HasChunkDecoder", [c_char_p], SDL_bool, added='2.0.2'),
    SDLFunc("Mix_GetNumMusicDecoders", None, c_int),
    SDLFunc("Mix_GetMusicDecoder", [c_int], c_char_p),
    SDLFunc("Mix_GetMusicType", [_P(Mix_Music)], Mix_MusicType),
    SDLFunc("Mix_SetPostMix", [mix_func, c_void_p]),
    SDLFunc("Mix_HookMusic", [mix_func, c_void_p]),
    SDLFunc("Mix_HookMusicFinished", [music_finished]),
    SDLFunc("Mix_GetMusicHookData", None, c_void_p),
    SDLFunc("Mix_ChannelFinished", [channel_finished]),
    SDLFunc("Mix_RegisterEffect", [c_int, Mix_EffectFunc_t, Mix_EffectDone_t, c_void_p], c_int),
    SDLFunc("Mix_UnregisterEffect", [c_int, Mix_EffectFunc_t], c_int),
    SDLFunc("Mix_UnregisterAllEffects", [c_int]),
    SDLFunc("Mix_SetPanning", [c_int, Uint8, Uint8], c_int),
    SDLFunc("Mix_SetPosition", [c_int, Sint16, Uint8], c_int),
    SDLFunc("Mix_SetDistance", [c_int, Uint8]),
    SDLFunc("Mix_SetReverseStereo", [c_int, c_int], c_int),
    SDLFunc("Mix_ReserveChannels", [c_int], c_int),
    SDLFunc("Mix_GroupChannel", [c_int, c_int], c_int),
    SDLFunc("Mix_GroupChannels", [c_int, c_int, c_int], c_int),
    SDLFunc("Mix_GroupAvailable", [c_int], c_int),
    SDLFunc("Mix_GroupCount", [c_int], c_int),
    SDLFunc("Mix_GroupOldest", [c_int], c_int),
    SDLFunc("Mix_GroupNewer", [c_int], c_int),
    SDLFunc("Mix_PlayChannelTimed", [c_int, _P(Mix_Chunk), c_int, c_int], c_int),
    SDLFunc("Mix_PlayMusic", [_P(Mix_Music), c_int], c_int),
    SDLFunc("Mix_FadeInMusic", [_P(Mix_Music), c_int, c_int], c_int),
    SDLFunc("Mix_FadeInMusicPos", [_P(Mix_Music), c_int, c_int, c_double], c_int),
    SDLFunc("Mix_FadeInChannelTimed", [c_int, _P(Mix_Chunk), c_int, c_int, c_int], c_int),
    SDLFunc("Mix_Volume", [c_int, c_int], c_int),
    SDLFunc("Mix_VolumeChunk", [_P(Mix_Chunk), c_int], c_int),
    SDLFunc("Mix_VolumeMusic", [c_int], c_int),
    SDLFunc("Mix_HaltChannel", [c_int], c_int),
    SDLFunc("Mix_HaltGroup", [c_int], c_int),
    SDLFunc("Mix_HaltMusic", None, c_int),
    SDLFunc("Mix_ExpireChannel", [c_int, c_int], c_int),
    SDLFunc("Mix_FadeOutChannel", [c_int, c_int], c_int),
    SDLFunc("Mix_FadeOutGroup", [c_int, c_int], c_int),
    SDLFunc("Mix_FadeOutMusic", [c_int], c_int),
    SDLFunc("Mix_FadingMusic", None, Mix_Fading),
    SDLFunc("Mix_FadingChannel", [c_int], Mix_Fading),
    SDLFunc("Mix_Pause", [c_int]),
    SDLFunc("Mix_Resume", [c_int]),
    SDLFunc("Mix_Paused", [c_int], c_int),
    SDLFunc("Mix_PauseMusic"),
    SDLFunc("Mix_ResumeMusic"),
    SDLFunc("Mix_RewindMusic"),
    SDLFunc("Mix_PausedMusic", None, c_int),
    SDLFunc("Mix_SetMusicPosition", [c_double], c_int),
    SDLFunc("Mix_Playing", [c_int], c_int),
    SDLFunc("Mix_PlayingMusic", None, c_int),
    SDLFunc("Mix_SetMusicCMD", [c_char_p], c_int),
    SDLFunc("Mix_SetSynchroValue", [c_int], c_int),
    SDLFunc("Mix_GetSynchroValue", None, c_int),
    SDLFunc("Mix_SetSoundFonts", [c_char_p], c_int),
    SDLFunc("Mix_GetSoundFonts", None, c_char_p),
    SDLFunc("Mix_EachSoundFont", [soundfont_function, c_void_p], c_int),
    SDLFunc("Mix_GetChunk", [c_int], _P(Mix_Chunk)),
    SDLFunc("Mix_CloseAudio"),
]
_funcs = {}
for f in _funcdefs:
    _funcs[f.name] = _bind(f.name, f.args, f.returns, f.added)


# Python wrapper functions

def Mix_Linked_Version():
    return _funcs["Mix_Linked_Version"]()

def Mix_Init(flags):
    return _funcs["Mix_Init"](flags)

def Mix_Quit():
    return _funcs["Mix_Quit"]()


def Mix_OpenAudio(frequency, format, channels, chunksize):
    return _funcs["Mix_OpenAudio"](frequency, format, channels, chunksize)

def Mix_OpenAudioDevice(frequency, format, channels, chunksize, device, allowed_changes):
    return _funcs["Mix_OpenAudioDevice"](
        frequency, format, channels, chunksize, device, allowed_changes
    )

def Mix_AllocateChannels(numchans):
    return _funcs["Mix_AllocateChannels"](numchans)

def Mix_QuerySpec(frequency, format, channels):
    return _funcs["Mix_QuerySpec"](frequency, format, channels)


def Mix_LoadWAV_RW(src, freesrc):
    return _funcs["Mix_LoadWAV_RW"](src, freesrc)

def Mix_LoadWAV(file):
    return Mix_LoadWAV_RW(SDL_RWFromFile(file, b"rb"), 1)

def Mix_LoadMUS(file):
    return _funcs["Mix_LoadMUS"](file)

def Mix_LoadMUS_RW(src, freesrc):
    return _funcs["Mix_LoadMUS_RW"](src, freesrc)

def Mix_LoadMUSType_RW(src, type, freesrc):
    return _funcs["Mix_LoadMUSType_RW"](src, type, freesrc)

def Mix_QuickLoad_WAV(mem):
    return _funcs["Mix_QuickLoad_WAV"](mem)

def Mix_QuickLoad_RAW(mem, len):
    return _funcs["Mix_QuickLoad_RAW"](mem, len)

def Mix_FreeChunk(chunk):
    return _funcs["Mix_FreeChunk"](chunk)

def Mix_FreeMusic(music):
    return _funcs["Mix_FreeMusic"](music)


def Mix_GetNumChunkDecoders():
    return _funcs["Mix_GetNumChunkDecoders"]()

def Mix_GetChunkDecoder(index):
    return _funcs["Mix_GetChunkDecoder"](index)

def Mix_HasChunkDecoder(name):
    return _funcs["Mix_HasChunkDecoder"](name)

def Mix_GetNumMusicDecoders():
    return _funcs["Mix_GetNumMusicDecoders"]()

def Mix_GetMusicDecoder(index):
    return _funcs["Mix_GetMusicDecoder"](index)

def Mix_GetMusicType(music):
    return _funcs["Mix_GetMusicType"](music)


def Mix_SetPostMix(mix_func, arg):
    return _funcs["Mix_SetPostMix"](mix_func, arg)

def Mix_HookMusic(mix_func, arg):
    return _funcs["Mix_HookMusic"](mix_func, arg)

def Mix_HookMusicFinished(music_finished):
    return _funcs["Mix_HookMusicFinished"](music_finished)

def Mix_GetMusicHookData():
    return _funcs["Mix_GetMusicHookData"]()

def Mix_ChannelFinished(channel_finished):
    return _funcs["Mix_ChannelFinished"](channel_finished)


def Mix_RegisterEffect(chan, f, d, arg):
    return _funcs["Mix_RegisterEffect"](chan, f, d, arg)

def Mix_UnregisterEffect(channel, f):
    return _funcs["Mix_UnregisterEffect"](channel, f)

def Mix_UnregisterAllEffects(channel):
    return _funcs["Mix_UnregisterAllEffects"](channel)


def Mix_SetPanning(channel, left, right):
    return _funcs["Mix_SetPanning"](channel, left, right)

def Mix_SetPosition(channel, angle, distance):
    return _funcs["Mix_SetPosition"](channel, angle, distance)

def Mix_SetDistance(channel, distance):
    return _funcs["Mix_SetDistance"](channel, distance)

def Mix_SetReverseStereo(channel, flip):
    return _funcs["Mix_SetReverseStereo"](channel, flip)

def Mix_ReserveChannels(num):
    return _funcs["Mix_ReserveChannels"](num)


def Mix_GroupChannel(which, tag):
    return _funcs["Mix_GroupChannel"](which, tag)

def Mix_GroupChannels(from, to, tag):
    return _funcs["Mix_GroupChannels"](from, to, tag)

def Mix_GroupAvailable(tag):
    return _funcs["Mix_GroupAvailable"](tag)

def Mix_GroupCount(tag):
    return _funcs["Mix_GroupCount"](tag)

def Mix_GroupOldest(tag):
    return _funcs["Mix_GroupOldest"](tag)

def Mix_GroupNewer(tag):
    return _funcs["Mix_GroupNewer"](tag)


def Mix_PlayChannelTimed(channel, chunk, loops, ticks):
    return _funcs["Mix_PlayChannelTimed"](channel, chunk, loops, ticks)

def Mix_PlayChannel(channel, chunk, loops):
    return Mix_PlayChannelTimed(channel, chunk, loops, -1)

def Mix_PlayMusic(music, loops):
    return _funcs["Mix_PlayMusic"](music, loops)


def Mix_FadeInMusic(music, loops, ms):
    return _funcs["Mix_FadeInMusic"](music, loops, ms)

def Mix_FadeInMusicPos(music, loops, ms, position):
    return _funcs["Mix_FadeInMusicPos"](music, loops, ms, position)

def Mix_FadeInChannelTimed(channel, chunk, loops, ms, ticks):
    return _funcs["Mix_FadeInChannelTimed"](channel, chunk, loops, ms, ticks)

def Mix_FadeInChannel(channel, chunk, loops, ms):
    return Mix_FadeInChannelTimed(channel, chunk, loops, ms, -1)


def Mix_Volume(channel, volume):
    return _funcs["Mix_Volume"](channel, volume)

def Mix_VolumeChunk(chunk, volume):
    return _funcs["Mix_VolumeChunk"](chunk, volume)

def Mix_VolumeMusic(volume):
    return _funcs["Mix_VolumeMusic"](volume)


def Mix_HaltChannel(channel):
    return _funcs["Mix_HaltChannel"](channel)

def Mix_HaltGroup(tag):
    return _funcs["Mix_HaltGroup"](tag)

def Mix_HaltMusic():
    return _funcs["Mix_HaltMusic"]()

def Mix_ExpireChannel(channel, ticks):
    return _funcs["Mix_ExpireChannel"](channel, ticks)


def Mix_FadeOutChannel(which, ms):
    return _funcs["Mix_FadeOutChannel"](which, ms)

def Mix_FadeOutGroup(tag, ms):
    return _funcs["Mix_FadeOutGroup"](tag, ms)

def Mix_FadeOutMusic(ms):
    return _funcs["Mix_FadeOutMusic"](ms)

def Mix_FadingMusic():
    return _funcs["Mix_FadingMusic"]()

def Mix_FadingChannel(which):
    return _funcs["Mix_FadingChannel"](which)


def Mix_Pause(channel):
    return _funcs["Mix_Pause"](channel)

def Mix_Resume(channel):
    return _funcs["Mix_Resume"](channel)

def Mix_Paused(channel):
    return _funcs["Mix_Paused"](channel)

def Mix_PauseMusic():
    return _funcs["Mix_PauseMusic"]()

def Mix_ResumeMusic():
    return _funcs["Mix_ResumeMusic"]()

def Mix_RewindMusic():
    return _funcs["Mix_RewindMusic"]()

def Mix_PausedMusic():
    return _funcs["Mix_PausedMusic"]()


def Mix_SetMusicPosition(position):
    return _funcs["Mix_SetMusicPosition"](position)

def Mix_Playing(channel):
    return _funcs["Mix_Playing"](channel)

def Mix_PlayingMusic():
    return _funcs["Mix_PlayingMusic"]()

def Mix_SetMusicCMD(command):
    return _funcs["Mix_SetMusicCMD"](command)


def Mix_SetSynchroValue(value):
    return _funcs["Mix_SetSynchroValue"](value)

def Mix_GetSynchroValue():
    return _funcs["Mix_GetSynchroValue"]()

def Mix_SetSoundFonts(paths):
    return _funcs["Mix_SetSoundFonts"](paths)

def Mix_GetSoundFonts():
    return _funcs["Mix_GetSoundFonts"]()

def Mix_EachSoundFont(function, data):
    return _funcs["Mix_EachSoundFont"](function, data)


def Mix_GetChunk(channel):
    return _funcs["Mix_GetChunk"](channel)

def Mix_CloseAudio():
    return _funcs["Mix_CloseAudio"]()


Mix_SetError = SDL_SetError
Mix_GetError = SDL_GetError
Mix_ClearError = SDL_ClearError
