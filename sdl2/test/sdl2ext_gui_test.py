import sys
import pytest
from sdl2 import ext as sdl2ext


class TestSDL2ExtGUI(object):
    __tags__ = ["sdl", "sdl2ext"]

    @classmethod
    def setup_class(cls):
        try:
            sdl2ext.init()
        except sdl2ext.SDLError:
            raise pytest.skip('Video subsystem not supported')

    @classmethod
    def teardown_class(cls):
        sdl2ext.quit()

    @pytest.mark.skip("not implemented")
    def test_UIFactory(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIFactory_create_button(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIFactory_create_checkbutton(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIFactory_create_text_entry(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_Button(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_CheckButton(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_TextEntry(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_activate(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_deactivate(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_dispatch(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_mousedown(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_mouseup(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_mousemotion(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_passevent(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_process(self):
        pass

    @pytest.mark.skip("not implemented")
    def test_UIProcessor_textinput(self):
        pass
