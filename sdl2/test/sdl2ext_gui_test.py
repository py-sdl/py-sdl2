import sys
import unittest
from .. import ext as sdl2ext


class SDL2ExtGUITest(unittest.TestCase):
    __tags__ = ["sdl", "sdl2ext"]

    def setUp(self):
        sdl2ext.init()

    def tearDown(self):
        sdl2ext.quit()

    @unittest.skip("not implemented")
    def test_UIFactory(self):
        pass

    @unittest.skip("not implemented")
    def test_UIFactory_create_button(self):
        pass

    @unittest.skip("not implemented")
    def test_UIFactory_create_checkbutton(self):
        pass

    @unittest.skip("not implemented")
    def test_UIFactory_create_text_entry(self):
        pass

    @unittest.skip("not implemented")
    def test_Button(self):
        pass

    @unittest.skip("not implemented")
    def test_CheckButton(self):
        pass

    @unittest.skip("not implemented")
    def test_TextEntry(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_activate(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_deactivate(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_dispatch(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_mousedown(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_mouseup(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_mousemotion(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_passevent(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_process(self):
        pass

    @unittest.skip("not implemented")
    def test_UIProcessor_textinput(self):
        pass


if __name__ == '__main__':
    sys.exit(unittest.main())
