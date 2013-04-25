import sys
import unittest
try:
    import multiprocessing
    _HASMP = True
except ImportError:
    _HASMP = False
from ..ext import events


def mp_do_nothing(sender, *args):
    # Does nothing
    pass


class SDL2ExtEventsTest(unittest.TestCase):
    __tags__ = ["sdl2ext"]

    def test_EventHandler(self):
        self.assertRaises(TypeError, events.EventHandler)
        self.assertIsInstance(events.EventHandler(None), events.EventHandler)
        self.assertIsInstance(events.EventHandler(132), events.EventHandler)
        self.assertIsInstance(events.EventHandler("Test"), events.EventHandler)

        ev = events.EventHandler(None)
        self.assertEqual(ev.sender, None)
        ev = events.EventHandler("Test")
        self.assertEqual(ev.sender, "Test")
        self.assertEqual(len(ev), 0)
        self.assertEqual(len(ev.callbacks), 0)

    def test_EventHandler_add__iadd__(self):
        ev = events.EventHandler(None)

        def doadd(ev, cb):
            ev += cb

        def callback():
            pass

        self.assertRaises(TypeError, doadd, ev, None)
        self.assertRaises(TypeError, doadd, ev, "Test")
        self.assertRaises(TypeError, doadd, ev, 1234)

        self.assertEqual(len(ev), 0)
        ev += callback
        self.assertEqual(len(ev), 1)
        for x in range(4):
            ev += callback
        self.assertEqual(len(ev), 5)

        self.assertRaises(TypeError, ev.add, None)
        self.assertRaises(TypeError, ev.add, "Test")
        self.assertRaises(TypeError, ev.add, 1234)

        self.assertEqual(len(ev), 5)
        ev.add(callback)
        self.assertEqual(len(ev), 6)
        for x in range(4):
            ev.add(callback)
        self.assertEqual(len(ev), 10)

    def test_EventHandler_remove__isub__(self):
        ev = events.EventHandler(None)

        def doremove(ev, cb):
            ev -= cb

        def callback():
            pass

        for x in range(10):
            ev += callback
        self.assertEqual(len(ev), 10)

        self.assertRaises(TypeError, ev.remove)
        for invval in ("Test", None, 1234, self.assertEqual):
            self.assertRaises(ValueError, ev.remove, invval)
            self.assertRaises(ValueError, doremove, ev, invval)
        self.assertEqual(len(ev), 10)
        ev.remove(callback)
        self.assertEqual(len(ev), 9)
        ev -= callback
        self.assertEqual(len(ev), 8)
        for x in range(3):
            ev.remove(callback)
            ev -= callback
        self.assertEqual(len(ev), 2)

    def test_EventHandler__call__(self):
        ev = events.EventHandler("Test")
        testsum = []

        def callback(sender, sumval):
            self.assertEqual(sender, "Test")
            sumval.append(1)

        for x in range(10):
            ev += callback
        self.assertEqual(len(ev), 10)
        results = ev(testsum)
        self.assertEqual(len(testsum), 10)
        for v in testsum:
            self.assertEqual(v, 1)
        self.assertEqual(len(results), 10)
        for v in results:
            self.assertIsNone(v)

    @unittest.skipIf(not _HASMP, "multiprocessing is not supported")
    def test_MPEventHandler(self):
        self.assertRaises(TypeError, events.MPEventHandler)
        self.assertIsInstance(events.MPEventHandler(None),
                              events.MPEventHandler)
        self.assertIsInstance(events.MPEventHandler(132),
                              events.MPEventHandler)
        self.assertIsInstance(events.MPEventHandler("Test"),
                              events.MPEventHandler)

        ev = events.MPEventHandler(None)
        self.assertEqual(ev.sender, None)
        ev = events.MPEventHandler("Test")
        self.assertEqual(ev.sender, "Test")
        self.assertEqual(len(ev), 0)
        self.assertEqual(len(ev.callbacks), 0)

    @unittest.skipIf(not _HASMP, "multiprocessing is not supported")
    def test_MPEventHandler_add__iadd__(self):
        ev = events.MPEventHandler(None)

        def doadd(ev, cb):
            ev += cb

        def callback():
            pass

        self.assertRaises(TypeError, doadd, ev, None)
        self.assertRaises(TypeError, doadd, ev, "Test")
        self.assertRaises(TypeError, doadd, ev, 1234)

        self.assertEqual(len(ev), 0)
        ev += callback
        self.assertEqual(len(ev), 1)
        for x in range(4):
            ev += callback
        self.assertEqual(len(ev), 5)

        self.assertRaises(TypeError, ev.add, None)
        self.assertRaises(TypeError, ev.add, "Test")
        self.assertRaises(TypeError, ev.add, 1234)

        self.assertEqual(len(ev), 5)
        ev.add(callback)
        self.assertEqual(len(ev), 6)
        for x in range(4):
            ev.add(callback)
        self.assertEqual(len(ev), 10)

    @unittest.skipIf(not _HASMP, "multiprocessing is not supported")
    def test_MPEventHandler_remove__isub__(self):
        ev = events.MPEventHandler(None)

        def doremove(ev, cb):
            ev -= cb

        def callback():
            pass

        for x in range(10):
            ev += callback
        self.assertEqual(len(ev), 10)

        self.assertRaises(TypeError, ev.remove)
        for invval in ("Test", None, 1234, self.assertEqual):
            self.assertRaises(ValueError, ev.remove, invval)
            self.assertRaises(ValueError, doremove, ev, invval)
        self.assertEqual(len(ev), 10)
        ev.remove(callback)
        self.assertEqual(len(ev), 9)
        ev -= callback
        self.assertEqual(len(ev), 8)
        for x in range(3):
            ev.remove(callback)
            ev -= callback
        self.assertEqual(len(ev), 2)

    @unittest.skipIf(not _HASMP, "multiprocessing is not supported")
    @unittest.skipIf(sys.platform == "win32",
                     "relative import will create a fork bomb")
    def test_MPEventHandler__call__(self):
        ev = events.MPEventHandler("Test")

        for x in range(10):
            ev += mp_do_nothing
        self.assertEqual(len(ev), 10)
        results = ev().get(timeout=1)
        self.assertEqual(len(results), 10)
        for v in results:
            self.assertIsNone(v)

        results = ev("Test", 1234, "MoreArgs").get(timeout=1)
        self.assertEqual(len(results), 10)
        for v in results:
            self.assertIsNone(v)


if __name__ == '__main__':
    sys.exit(unittest.main())
