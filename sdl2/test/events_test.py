import sys
import unittest
from ctypes import c_char_p, c_void_p, cast
from .. import SDL_Init, SDL_Quit, SDL_QuitSubSystem, SDL_INIT_EVERYTHING
from .. import events


class SDLEventsTest(unittest.TestCase):
    __tags__ = ["sdl"]

    def setUp(self):
        SDL_Init(SDL_INIT_EVERYTHING)

    def tearDown(self):
        SDL_QuitSubSystem(SDL_INIT_EVERYTHING)
        SDL_Quit()

    def test_SDL_AudioDeviceEvent(self):
        event = events.SDL_AudioDeviceEvent()
        self.assertIsInstance(event, events.SDL_AudioDeviceEvent)

    def test_SDL_WindowEvent(self):
        event = events.SDL_WindowEvent()
        self.assertIsInstance(event, events.SDL_WindowEvent)

    def test_SDL_KeyboardEvent(self):
        event = events.SDL_KeyboardEvent()
        self.assertIsInstance(event, events.SDL_KeyboardEvent)

    def test_SDL_TextEditingEvent(self):
        event = events.SDL_TextEditingEvent()
        self.assertIsInstance(event, events.SDL_TextEditingEvent)

    def test_SDL_TextInputEvent(self):
        event = events.SDL_TextInputEvent()
        self.assertIsInstance(event, events.SDL_TextInputEvent)

    def test_SDL_MouseMotionEvent(self):
        event = events.SDL_MouseMotionEvent()
        self.assertIsInstance(event, events.SDL_MouseMotionEvent)

    def test_SDL_MouseButtonEvent(self):
        event = events.SDL_MouseButtonEvent()
        self.assertIsInstance(event, events.SDL_MouseButtonEvent)

    def test_SDL_MouseWheelEvent(self):
        event = events.SDL_MouseWheelEvent()
        self.assertIsInstance(event, events.SDL_MouseWheelEvent)

    def test_SDL_JoyAxisEvent(self):
        event = events.SDL_JoyAxisEvent()
        self.assertIsInstance(event, events.SDL_JoyAxisEvent)

    def test_SDL_JoyBallEvent(self):
        event = events.SDL_JoyBallEvent()
        self.assertIsInstance(event, events.SDL_JoyBallEvent)

    def test_SDL_JoyHatEvent(self):
        event = events.SDL_JoyHatEvent()
        self.assertIsInstance(event, events.SDL_JoyHatEvent)

    def test_SDL_JoyButtonEvent(self):
        event = events.SDL_JoyButtonEvent()
        self.assertIsInstance(event, events.SDL_JoyButtonEvent)

    def test_SDL_TouchFingerEvent(self):
        event = events.SDL_TouchFingerEvent()
        self.assertIsInstance(event, events.SDL_TouchFingerEvent)

    def test_SDL_MultiGestureEvent(self):
        event = events.SDL_MultiGestureEvent()
        self.assertIsInstance(event, events.SDL_MultiGestureEvent)

    def test_SDL_DollarGestureEvent(self):
        event = events.SDL_DollarGestureEvent()
        self.assertIsInstance(event, events.SDL_DollarGestureEvent)

    def test_SDL_DropEvent(self):
        event = events.SDL_DropEvent()
        self.assertIsInstance(event, events.SDL_DropEvent)

    def test_SDL_QuitEvent(self):
        event = events.SDL_QuitEvent()
        self.assertIsInstance(event, events.SDL_QuitEvent)

    def test_SDL_UserEvent(self):
        event = events.SDL_UserEvent()
        self.assertIsInstance(event, events.SDL_UserEvent)

    def test_SDL_SysWMEvent(self):
        event = events.SDL_SysWMEvent()
        self.assertIsInstance(event, events.SDL_SysWMEvent)

    def test_SDL_Event(self):
        event = events.SDL_Event()
        self.assertIsInstance(event, events.SDL_Event)

    def test_SDL_AddDelEventWatch(self):
        eventwatch = []

        def watch(data, event):
            eventwatch.append((event.contents, data,))
            return 0
        efilter = events.SDL_EventFilter(watch)
        udata = c_char_p(b"Something random")
        events.SDL_AddEventWatch(efilter, cast(udata, c_void_p))
        ev = events.SDL_Event()
        ev.type = events.SDL_USEREVENT
        ev.user = events.SDL_UserEvent()
        events.SDL_PushEvent(ev)
        self.assertEqual(len(eventwatch), 1)
        # TODO: x
        # self.assertEqual(eventwatch[0][1], udata)

        events.SDL_DelEventWatch(efilter, udata)
        ev = events.SDL_Event()
        events.SDL_PushEvent(ev)
        self.assertEqual(len(eventwatch), 1)
        # TODO: x
        # self.assertEqual(eventwatch[0][1], udata)

    def test_SDL_EventState(self):
        pass
        # state = events.SDL_EventState(events.SDL_USEREVENT, events.SDL_QUERY)
        # self.assertEqual(state, events.SDL_ENABLE)
        # state = events.SDL_EventState(events.SDL_USEREVENT,events.SDL_IGNORE)
        # self.assertEqual(state, events.SDL_ENABLE)
        # state = events.SDL_EventState(events.SDL_USEREVENT, events.SDL_QUERY)
        # self.assertEqual(state, events.SDL_IGNORE)
        # state = events.SDL_EventState(events.SDL_USEREVENT,events.SDL_ENABLE)
        # self.assertEqual(state, events.SDL_IGNORE)
        # state = events.SDL_EventState(events.SDL_USEREVENT, events.SDL_QUERY)
        # self.assertEqual(state, events.SDL_ENABLE)

        # self.assertRaises(TypeError, events.SDL_EventState, None, None)

        # ev = events.SDL_Event()
        # ev.type = events.SDL_USEREVENT
        # ev.user = events.SDL_UserEvent()
        # events.SDL_PushEvent(ev)

    @unittest.skip("not implemented")
    def test_SDL_GetEventState(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_FilterEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_FlushEvent(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_FlushEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_GetSetEventFilter(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_HasEvent(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_HasEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PeepEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PollEvent(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PumpEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_PushEvent(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_RegisterEvents(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_WaitEvent(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_WaitEventTimeout(self):
        pass

    @unittest.skip("not implemented")
    def test_SDL_QuitRequested(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
