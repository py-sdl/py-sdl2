import os
import sys
import ctypes
import unittest
from .. import SDL_Init, SDL_Quit, SDL_InitSubSystem, SDL_QuitSubSystem, \
    SDL_INIT_AUDIO
from .. import audio


class SDLAudioTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(0)

        def audio_cb(userdata, audiobytes, length):
            pass

        self.audiocallback = audio.SDL_AudioCallback(audio_cb)

    def tearDown(self):
        SDL_Quit()

    def test_SDL_AUDIO_BITSIZE(self):
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U8), 8)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S8), 8)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16LSB), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16LSB), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16MSB), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16MSB), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_U16), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S16), 16)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32LSB), 32)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32MSB), 32)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_S32), 32)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32LSB), 32)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32MSB), 32)
        self.assertEqual(audio.SDL_AUDIO_BITSIZE(audio.AUDIO_F32), 32)

    def test_SDL_AUDIO_ISFLOAT(self):
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U8))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S8))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_U16))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S16))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_S32))
        self.assertTrue(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISFLOAT(audio.AUDIO_F32))

    def test_SDL_AUDIO_ISBIGENDIAN(self):
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U8))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S8))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_U16))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S16))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_S32))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISBIGENDIAN(audio.AUDIO_F32))

    def test_SDL_AUDIO_ISSIGNED(self):
        self.assertFalse(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U8))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S8))
        self.assertFalse(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_U16))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S16))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_S32))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISSIGNED(audio.AUDIO_F32))

    def test_SDL_AUDIO_ISINT(self):
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_U8))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S8))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_U16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_U16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_U16))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S16))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S32LSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISINT(audio.AUDIO_S32))
        self.assertFalse(audio.SDL_AUDIO_ISINT(audio.AUDIO_F32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISINT(audio.AUDIO_F32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISINT(audio.AUDIO_F32))

    def test_SDL_AUDIO_ISLITTLEENDIAN(self):
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U8))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S8))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_U16))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S16))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_S32))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32MSB))
        self.assertTrue(audio.SDL_AUDIO_ISLITTLEENDIAN(audio.AUDIO_F32))

    def test_SDL_AUDIO_ISUNSIGNED(self):
        self.assertTrue(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U8))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S8))
        self.assertTrue(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16LSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16LSB))
        self.assertTrue(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16MSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16MSB))
        self.assertTrue(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_U16))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S16))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_S32))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32LSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32MSB))
        self.assertFalse(audio.SDL_AUDIO_ISUNSIGNED(audio.AUDIO_F32))

    @unittest.skip("not implemented")
    def test_SDL_AudioSpec(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_AudioCVT(self):
        pass

    def test_SDL_GetNumAudioDrivers(self):
        count = audio.SDL_GetNumAudioDrivers()
        self.assertGreaterEqual(count, 1)

    def test_SDL_GetAudioDriver(self):
        founddummy = False
        drivercount = audio.SDL_GetNumAudioDrivers()
        for index in range(drivercount):
            drivername = audio.SDL_GetAudioDriver(index)
            self.assertIsInstance(drivername, (str, bytes))
            if drivername == b"dummy":
                founddummy = True
        self.assertTrue(founddummy, "could not find dummy driver")
        # self.assertRaises(SDLError, audio.SDL_GetAudioDriver, -1)
        # self.assertRaises(SDLError, audio.get_audio_driver,
        #                  drivercount + 1)
        self.assertRaises((ctypes.ArgumentError, TypeError),
                          audio.SDL_GetAudioDriver, "Test")
        self.assertRaises((ctypes.ArgumentError, TypeError),
                          audio.SDL_GetAudioDriver, None)

    def test_SDL_GetCurrentAudioDriver(self):
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
                self.assertEqual(drivername, driver)
                success += 1
            SDL_QuitSubSystem(SDL_INIT_AUDIO)
        self.assertGreaterEqual(success, 1,
                                "Could not initialize any sound driver")

    @unittest.skip("SDL_AudioCallback is not retained in SDL_AudioSpec")
    def test_SDL_OpenAudio(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        SDL_InitSubSystem(SDL_INIT_AUDIO)
        reqspec = audio.SDL_AudioSpec(44100, audio.AUDIO_U16SYS, 2, 8192,
                                      self.audiocallback, None)
        spec = audio.SDL_AudioSpec(0, 0, 0, 0)
        ret = audio.SDL_OpenAudio(reqspec, ctypes.byref(spec))
        self.assertEqual(ret, 0)
        self.assertEqual(spec.format, reqspec.format)
        self.assertEqual(spec.freq, reqspec.freq)
        self.assertEqual(spec.channels, reqspec.channels)
        audio.SDL_CloseAudio()
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetNumAudioDevices(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        SDL_InitSubSystem(SDL_INIT_AUDIO)
        outnum = audio.SDL_GetNumAudioDevices(False)
        self.assertGreaterEqual(outnum, 1)
        innum = audio.SDL_GetNumAudioDevices(True)
        self.assertGreaterEqual(innum, 0)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    def test_SDL_GetAudioDeviceName(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        SDL_InitSubSystem(SDL_INIT_AUDIO)
        outnum = audio.SDL_GetNumAudioDevices(False)
        for x in range(outnum):
            name = audio.SDL_GetAudioDeviceName(x, False)
            self.assertIsNotNone(name)
        innum = audio.SDL_GetNumAudioDevices(True)
        for x in range(innum):
            name = audio.SDL_GetAudioDeviceName(x, True)
            self.assertIsNotNone(name)
        # self.assertRaises(SDLError, audio.get_audio_device_name, -1)
        # self.assertRaises(SDLError, audio.get_audio_device_name, -1, True)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

        # self.assertRaises(SDLError, audio.get_audio_device_name, 0)
        # self.assertRaises(SDLError, audio.get_audio_device_name, 0, True)

    @unittest.skip("SDL_AudioCallback is not retained in SDL_AudioSpec")
    def test_SDL_OpenCloseAudioDevice(self):
        os.environ["SDL_AUDIODRIVER"] = "dummy"
        SDL_InitSubSystem(SDL_INIT_AUDIO)
        reqspec = audio.SDL_AudioSpec(44100, audio.AUDIO_U16SYS, 2, 8192,
                                      self.audiocallback, None)
        outnum = audio.SDL_GetNumAudioDevices(0)
        for x in range(outnum):
            spec = audio.SDL_AudioSpec()
            name = audio.SDL_GetAudioDeviceName(x, 0)
            self.assertIsNotNone(name)
            deviceid = audio.SDL_OpenAudioDevice(None, 0, reqspec,
                                                 ctypes.byref(spec), 1)
            self.assertGreaterEqual(deviceid, 2)
            self.assertIsInstance(spec, audio.SDL_AudioSpec)
            self.assertEqual(spec.format, reqspec.format)
            self.assertEqual(spec.freq, reqspec.freq)
            self.assertEqual(spec.channels, reqspec.channels)
            audio.SDL_CloseAudioDevice(deviceid)
        SDL_QuitSubSystem(SDL_INIT_AUDIO)

    @unittest.skip("not implemented")
    def test_SDL_GetAudioStatus(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetAudioDeviceStatus(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PauseAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PauseAudioDevice(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_LoadWAV_RW(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_LoadWAV(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_FreeWAV(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_BuildAudioCVT(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_ConvertAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_MixAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_MixAudioFormat(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_LockUnlockAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_LockUnlockAudioDevice(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_CloseAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_QueueAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetQueuedAudioSize(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_ClearQueuedAudio(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_DequeueAudio(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
