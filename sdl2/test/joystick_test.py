import sys
import unittest
from sdl2 import SDL_Init, SDL_Quit, SDL_INIT_JOYSTICK
from sdl2.events import SDL_QUERY, SDL_ENABLE, SDL_IGNORE
from sdl2 import joystick


class SDLJoystickTest(unittest.TestCase):
    __tags__ = ["sdl"]

    @classmethod
    def setUpClass(cls):
        SDL_Init(SDL_INIT_JOYSTICK)
        cls.jcount = joystick.SDL_NumJoysticks()

    @classmethod
    def tearDownClass(cls):
        SDL_Quit()

    def test_SDL_NumJoysticks(self):
        retval = joystick.SDL_NumJoysticks()
        self.assertGreaterEqual(retval, 0)

    def test_SDL_JoystickNameForIndex(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            name = joystick.SDL_JoystickNameForIndex(index)
            self.assertIn(type(name), (str, bytes))

    def test_SDL_JoystickOpen(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            self.assertIsInstance(stick.contents, joystick.SDL_Joystick)
            joystick.SDL_JoystickClose(stick)

    @unittest.skip("not implemented")
    def test_SDL_JoystickName(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceGUID(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetGUID(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetGUIDString(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetGUIDFromString(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetAttached(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickInstanceID(self):
        pass

    def test_SDL_JoystickNumAxes(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            self.assertIsInstance(stick.contents, joystick.SDL_Joystick)
            axes = joystick.SDL_JoystickNumAxes(stick)
            self.assertGreaterEqual(axes, 0)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumBalls(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            self.assertIsInstance(stick.contents, joystick.SDL_Joystick)
            balls = joystick.SDL_JoystickNumBalls(stick)
            self.assertGreaterEqual(balls, 0)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumHats(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            self.assertIsInstance(stick.contents, joystick.SDL_Joystick)
            hats = joystick.SDL_JoystickNumHats(stick)
            self.assertGreaterEqual(hats, 0)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickNumButtons(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            self.assertIsInstance(stick.contents, joystick.SDL_Joystick)
            buttons = joystick.SDL_JoystickNumButtons(stick)
            self.assertGreaterEqual(buttons, 0)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickUpdate(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        joystick.SDL_JoystickUpdate()

    def test_SDL_JoystickEventState(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for state in(SDL_IGNORE, SDL_ENABLE):
            news = joystick.SDL_JoystickEventState(state)
            self.assertEqual(news, state)
            query = joystick.SDL_JoystickEventState(SDL_QUERY)
            self.assertEqual(query, state)

    def test_SDL_JoystickGetAxis(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for axis in range(joystick.SDL_JoystickNumAxes(stick)):
                val = joystick.SDL_JoystickGetAxis(stick, axis)
                self.assertTrue(-32768 <= val <= 32767)
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetBall(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for ball in range(joystick.SDL_JoystickNumBalls(stick)):
                dx, dy = joystick.SDL_JoystickGetBall(stick, ball)
                self.assertIsInstance(dx, int)
                self.assertIsInstance(dy, int)
                # TODO
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetHat(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for hat in range(joystick.SDL_JoystickNumHats(stick)):
                val = joystick.SDL_JoystickGetHat(stick, hat)
                self.assertIsInstance(val, int)
                # TODO
            joystick.SDL_JoystickClose(stick)

    def test_SDL_JoystickGetButton(self):
        if self.jcount == 0:
            self.skipTest("no joysticks detected")
        for index in range(self.jcount):
            stick = joystick.SDL_JoystickOpen(index)
            for button in range(joystick.SDL_JoystickNumButtons(stick)):
                val = joystick.SDL_JoystickGetButton(stick, button)
                # TODO: x
                # self.assertIsInstance(val, bool)
            joystick.SDL_JoystickClose(stick)

    @unittest.skip("not implemented")
    def test_SDL_JoystickClose(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickCurrentPowerLevel(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickFromInstanceID(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetVendor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetProduct(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetProductVersion(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetAxisInitialState(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetType(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceVendor(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceProduct(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceProductVersion(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceType(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_JoystickGetDeviceInstanceID(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
