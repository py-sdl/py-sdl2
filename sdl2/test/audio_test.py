import os
import sys
import ctypes
from sdl2 import SDL_Init, SDL_Quit, SDL_InitSubSystem, SDL_QuitSubSystem, \
    SDL_INIT_AUDIO
from sdl2 import audio
import pytest


class TestSDLAudio(object):
    __tags__ = ["sdl"]

    @classmethod
    def setup_class(cls):
        SDL_Init(0)

        def audio_cb(userdata, audiobytes, length):
            pass

        cls.audiocallback = audio.SDL_AudioCallback(audio_cb)

    @classmethod
    def teardown_class(cls):
        SDL_Quit()

    def test_SDL_AUDIO_BITSIZE(self):
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U8) == 8
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S8) == 8
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16LSB) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16LSB) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16MSB) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16MSB) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16) == 16
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32LSB) == 32
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32MSB) == 32
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32) == 32
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32LSB) == 32
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32MSB) == 32
        assert audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32) == 32

    def test_SDL_AUDIO_ISFLOAT(self):
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U8)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S8)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16LSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16LSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16MSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16MSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32LSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32MSB)
        assert not audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32)
        assert audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32LSB)
        assert audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32MSB)
        assert audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32)

    def test_SDL_AUDIO_ISBIGENDIAN(self):
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U8)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S8)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16LSB)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16LSB)
        assert audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16MSB)
        assert audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16MSB)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32LSB)
        assert audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32MSB)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32LSB)
        assert audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32MSB)
        assert not audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32)

    def test_SDL_AUDIO_ISSIGNED(self):
        assert not audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U8)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S8)
        assert not audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16LSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16LSB)
        assert not audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16MSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16MSB)
        assert not audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32LSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32MSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32LSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32MSB)
        assert audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32)

    def test_SDL_AUDIO_ISINT(self):
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_U8)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S8)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_U16LSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S16LSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_U16MSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S16MSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_U16)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S16)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S32LSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S32MSB)
        assert audio.SDL_AUDIO_ISINT(audio.AUDIO_S32)
        assert not audio.SDL_AUDIO_ISINT(audio.AUDIO_F32LSB)
        assert not audio.SDL_AUDIO_ISINT(audio.AUDIO_F32MSB)
        assert not audio.SDL_AUDIO_ISINT(audio.AUDIO_F32)

    def test_SDL_AUDIO_ISLITTLEENDIAN(self):
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U8)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S8)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16LSB)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16LSB)
        assert not audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16MSB)
        assert not audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16MSB)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32LSB)
        assert not audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32MSB)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32LSB)
        assert not audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32MSB)
        assert audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32)

    def test_SDL_AUDIO_ISUNSIGNED(self):
        assert audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U8)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S8)
        assert audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16LSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16LSB)
        assert audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16MSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16MSB)
        assert audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32LSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32MSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32LSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32MSB)
        assert not audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32)

    @pytest.mark.skip("not implemented")
    def test_SDL_AudioSpec(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_AudioCVT(self):
        pass

    def test_SDL_GetNumAudioDrivers(self):
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        count = audio.SDL_GetNumAudioDrivers()
        assert count >= 1
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetAudioDriver(self):
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        founddummy = False
        drivercount = audio.SDL_GetNumAudioDrivers()
        for index in range(drivercount):
            drivername = audio.SDL_GetAudioDriver(index)
            assert isinstance(drivername, (str, bytes))
            if drivername == b"dummy":
                founddummy = True
        assert founddummy, "could not find dummy driver"
        # self.assertRaises(SDLError, audio.SDL_GetAudioDriver, -1)
        with pytest.raises((ctypes.ArgumentError, TypeError)):
            audio.SDL_GetAudioDriver("Test")
        with pytest.raises((ctypes.ArgumentError, TypeError)):
            audio.SDL_GetAudioDriver(None)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetCurrentAudioDriver(self):
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        SDL_QuitSubSystem(SDL_INIT_AUDIO)
        success = 0
        for index in range(audio.SDL_GetNumAudioDrivers()):
            drivername = audio.SDL_GetAudioDriver(index)
            os.environ["SDL_AUDIODRIVER"] = drivername.decode("utf-8")
            # Certain drivers fail without bringing up the correct
            # return value, such as the esd, if it is not running.
            SDL_InitSubSystem(SDL_INIT_AUDIO)
            driver = audio.SDL_GetCurrentAudioDriver()
            # Do not handle wrong return values.
            if driver is not None:
                assert drivername == driver
                success += 1
            SDL_QuitSubSystem(SDL_INIT_AUDIO)
        assert success >= 1, "Could not initialize any sound driver"

    @pytest.mark.skip("SDL_AudioCallback is not retained in SDL_AudioSpec")
    def test_SDL_OpenAudio(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        reqspec = audio.SDL_AudioSpec(44100, audio.AUDIO_U16SYS, 2, 8192,
                                      self.audiocallback, None)
        spec = audio.SDL_AudioSpec(0, 0, 0, 0)
        ret = audio.SDL_OpenAudio(reqspec, ctypes.byref(spec))
        assert ret == 0
        assert spec.format == reqspec.format
        assert spec.freq == reqspec.freq
        assert spec.channels == reqspec.channels
        audio.SDL_CloseAudio()
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetNumAudioDevices(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        outnum = audio.SDL_GetNumAudioDevices(False)
        assert outnum >= 1
        innum = audio.SDL_GetNumAudioDevices(True)
        assert innum >= 0
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetAudioDeviceName(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        outnum = audio.SDL_GetNumAudioDevices(False)
        for x in range(outnum):
            name = audio.SDL_GetAudioDeviceName(x, False)
            assert name is not None
        innum = audio.SDL_GetNumAudioDevices(True)
        for x in range(innum):
            name = audio.SDL_GetAudioDeviceName(x, True)
            assert name is not None
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    @pytest.mark.skip("SDL_AudioCallback is not retained in SDL_AudioSpec")
    def test_SDL_OpenCloseAudioDevice(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        if SDL_InitSubSystem(SDL_INIT_AUDIO) != 0:
            pytest.skip('Audio subsystem not supported')
        reqspec = audio.SDL_AudioSpec(44100, audio.AUDIO_U16SYS, 2, 8192,
                                      self.audiocallback, None)
        outnum = audio.SDL_GetNumAudioDevices(0)
        for x in range(outnum):
            spec = audio.SDL_AudioSpec()
            name = audio.SDL_GetAudioDeviceName(x, 0)
            assert name is not None
            deviceid = audio.SDL_OpenAudioDevice(None, 0, reqspec,
                                                 ctypes.byref(spec), 1)
            assert deviceid >= 2
            assert isinstance(spec, audio.SDL_AudioSpec)
            assert spec.format == reqspec.format
            assert spec.freq == reqspec.freq
            assert spec.channels == reqspec.channels
            audio.SDL_CloseAudioDevice(deviceid)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    @pytest.mark.skip("not implemented")
    def test_SDL_GetAudioStatus(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GetAudioDeviceStatus(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_PauseAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_PauseAudioDevice(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_LoadWAV_RW(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_LoadWAV(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_FreeWAV(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_BuildAudioCVT(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_ConvertAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_MixAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_MixAudioFormat(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_LockUnlockAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_LockUnlockAudioDevice(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_CloseAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_QueueAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_GetQueuedAudioSize(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_ClearQueuedAudio(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_SDL_DequeueAudio(self):
        pass
