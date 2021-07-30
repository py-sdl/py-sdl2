"""User interface elements."""
from ctypes import byref, c_int, POINTER
from .color import Color
from .compat import isiterable, stringify, utf8
from .common import SDLError
from .ebs import System, World
from .events import EventHandler
from .sprite import Sprite
from .window import Window
from .. import (events, dll, mouse, keyboard, rect, error, SDL_PumpEvents,
    SDL_Window)
from .. import messagebox as mb

__all__ = [
    "RELEASED", "HOVERED", "PRESSED", "BUTTON", "CHECKBUTTON", "TEXTENTRY",
    "MessageBoxTheme", "MessageBox", "show_messagebox", "show_alert",
    "UIProcessor", "UIFactory"
]


RELEASED = 0x0000
HOVERED = 0x0001
PRESSED = 0x0002

BUTTON = 0x0001
CHECKABLE = 0x0002
CHECKBUTTON = (CHECKABLE | BUTTON)
TEXTENTRY = 0x0004


class MessageBoxTheme(object):
    """Initializes a color scheme for use with :obj:`MessageBox` objects.

    This is used to define the background, text, and various button colors
    to use when presenting dialog boxes to users. All colors must be defined
    as either :obj:`sdl2.ext.Color` objects or 8-bit ``(r, g, b)`` tuples.

    .. note::
       SDL2 only supports MessageBox themes on a few platforms, including
       Linux/BSD (if using X11) and Haiku. MessageBox themes will have no effect
       on Windows, macOS, or Linux if using Wayland.

    Args:
        bg (:obj:~`sdl2.ext.Color`, tuple, optional): The color to use for the
            background of the dialog box. Defaults to ``(56, 54, 53)``.
        text (:obj:~`sdl2.ext.Color`, tuple, optional): The color to use for the
            text of the dialog box. Defaults to ``(209, 207, 205)``.
        btn (:obj:~`sdl2.ext.Color`, tuple, optional): The color to use for the
            backgrounds of buttons. Defaults to ``(140, 135, 129)``.
        btn_border (:obj:~`sdl2.ext.Color`, tuple, optional): The color to use
            for the borders of buttons. Defaults to ``(105, 102, 99)``.
        btn_selected (:obj:~`sdl2.ext.Color`, tuple, optional): The color to use
            for selected buttons. Defaults to ``(205, 202, 53)``.

    """
    def __init__(
        self, bg=None, text=None, btn=None, btn_border=None, btn_selected=None
    ):
        # NOTE: Default colors taken from SDL_x11messagebox.c
        self._theme = [
            (56, 54, 53),     # Background color
            (209, 207, 205),  # Text color
            (140, 135, 129),  # Button border color
            (105, 102, 99),   # Button background color
            (205, 202, 53)    # Selected button color
        ]
        # Update default theme colors based on provided values
        elements = [bg, text, btn_border, btn, btn_selected]
        for i in range(len(elements)):
            if elements[i] is not None:
                self._theme[i] = self._validate_color(elements[i])

    def _validate_color(self, col):
        if not isinstance(col, Color):
            if not isiterable(col) or len(col) != 3:
                e = "MessageBox colors must be specified as (r, g, b) tuples."
                raise TypeError(e)
            for val in col:
                if int(val) != float(val):
                    e = "All RGB values must be integers between 0 and 255."
                    raise ValueError(e)
            col = Color(col[0], col[1], col[2])
        return (col.r, col.g, col.b)

    def _get_theme(self):
        sdl_colors = []
        for col in self._theme:
            sdl_colors.append(mb.SDL_MessageBoxColor(*col))
        col_array = (mb.SDL_MessageBoxColor * 5)(*sdl_colors)
        return mb.SDL_MessageBoxColorScheme(col_array)


class MessageBox(object):
    """Creates a prototype for a dialog box that can be presented to the user.

    The `MessageBox` class is for designing a dialog box in the style of the
    system's window manager, containing a title, a message to present, and
    one or more response buttons.

    Args:
        title (str): The title to use for the dialog box. All UTF-8 characters
            are supported.
        msg (str): The main body of text to display in the dialog box. All UTF-8
            characters are supported.
        buttons (list): A list of strings, containing the labels of the buttons
            to place at the bottom of the dialog box (e.g. ``["No", "Yes"]``).
            Buttons will be placed in left-to-right order.
        default (str, optional): The label of the button to highlight as the
            default option (e.g. ``"Yes"``). Must match one of the labels in
            ``buttons``. This option will be accepted if the Return/Enter key
            is pressed on the keyboard.
        msgtype (str, optional): The type of dialog box to create, if supported
            by the system. On most window managers, this changes the icon used
            in the dialog box. Must be one of 'error', 'warning', or 'info', or
            None (the default).
        theme (:obj:`MessageBoxTheme`, optional): The color scheme to use for
            the dialog box, if supported by the window manager. Defaults to the
            system default theme.

    """
    def __init__(self, title, msg, buttons, default=None, msgtype=None, theme=None):
        self._title = utf8(title).encode('utf-8')
        self._text = utf8(msg).encode('utf-8')
        self._validate_buttons(buttons)
        self._buttons = buttons
        self._sdlbuttons = self._init_buttons(buttons, default)
        self._type = self._set_msgtype(msgtype) if msgtype else 0
        self._theme = theme._get_theme() if theme else None

    def _set_msgtype(self, msgtype):
        _flagmap = {
            'error': mb.SDL_MESSAGEBOX_ERROR,
            'warning': mb.SDL_MESSAGEBOX_WARNING,
            'info': mb.SDL_MESSAGEBOX_INFORMATION,
        }
        if msgtype.lower() not in _flagmap.keys():
            raise ValueError(
                "MessageBox type must be 'error', 'warning', 'info', or None."
            )
        return _flagmap[msgtype]

    def _validate_buttons(self, buttons):
        if not isiterable(buttons):
            raise TypeError("Buttons must be provided as a list.")
        elif len(buttons) == 0:
            raise ValueError("MessageBox must have at least one button.")

    def _init_buttons(self, buttons, default):
        default_flag = mb.SDL_MESSAGEBOX_BUTTON_RETURNKEY_DEFAULT
        buttonset = []
        for i in range(len(buttons)):
            b = mb.SDL_MessageBoxButtonData(
                flags = (default_flag if buttons[i] == default else 0),
                buttonid = i,
                text = utf8(buttons[i]).encode('utf-8'),
            )
            buttonset.append(b)
        return (mb.SDL_MessageBoxButtonData * len(buttons))(*buttonset)

    def _get_window_pointer(self, win):
        if isinstance(win, Window):
            win = win.window
        if isinstance(win, SDL_Window):
            win = dll.get_pointer(win)
        if hasattr(win, "contents") and isinstance(win.contents, SDL_Window):
            return win
        else:
            e = "'window' must be a Window or SDL_Window object (got {0})"
            raise ValueError(e.format(str(type(win))))

    def _get_msgbox(self, window=None):
        if window:
            window = self._get_window_pointer(window)
        return mb.SDL_MessageBoxData(
            flags = self._type | mb.SDL_MESSAGEBOX_BUTTONS_RIGHT_TO_LEFT,
            window = window,
            title = self._title,
            message = self._text,
            numbuttons = len(self._buttons),
            buttons = self._sdlbuttons,
            colorScheme = dll.get_pointer(self._theme) if self._theme else None,
        )
        

def show_messagebox(msgbox, window=None):
    """Displays a dialog box to the user and waits for a response.

    By default message boxes are presented independently of any window, but
    they can optionally be attached explicitly to a specific SDL window. This
    prevents that window from regaining focus until a response to the dialog
    box is made.

    Args:
        msgbox (:obj:`~sdl2.ext.MessageBox`): The dialog box to display
            on-screen.
        window (:obj:`~sdl2.SDL_Window`, :obj:`~sdl2.ext.Window`, optional): The
            window to associate with the dialog box. Defaults to None.

    Returns:
        str: The label of the button selected by the user.

    """
    resp = c_int(-1)
    ret = mb.SDL_ShowMessageBox(
        msgbox._get_msgbox(window),
        byref(resp)
    )
    SDL_PumpEvents()
    if ret == 0:
        return msgbox._buttons[resp.value]
    else:
        errmsg = error.SDL_GetError().decode('utf-8')
        error.SDL_ClearError()
        e = "Error encountered displaying message box"
        if len(errmsg):
            e += ": {0}".format(errmsg)
        raise SDLError(e)


def show_alert(title, msg, msgtype=None, window=None):
    """Displays a simple alert to the user and waits for a response.

    This function is a simplified version of :func:`show_messagebox` for cases
    where only one response button ("OK") is needed and a custom color scheme
    is not necessary.

    By default message boxes are presented independently of any window, but
    they can optionally be attached explicitly to a specific SDL window. This
    prevents that window from regaining focus until a response to the dialog
    box is made.

    Args:
        msgbox (:obj:`~sdl2.ext.MessageBox`): The dialog box to display
            on-screen.
        window (:obj:`~sdl2.SDL_Window`, :obj:`~sdl2.ext.Window`, optional): The
            window to associate with the dialog box. Defaults to ``None``.

    """
    box = MessageBox(title, msg, ["OK"], msgtype=msgtype)
    if window:
        window = box._get_window_pointer(window)
    ret = mb.SDL_ShowSimpleMessageBox(
        box._type,
        box._title,
        box._text,
        window
    )
    SDL_PumpEvents()
    if ret != 0:
        errmsg = error.SDL_GetError().decode('utf-8')
        error.SDL_ClearError()
        e = "Error encountered displaying message box"
        if len(errmsg):
            e += ": {0}".format(errmsg)
        raise SDLError(e)


def _compose_button(obj):
    """Binds button attributes to the object, so it can be properly
    processed by the UIProcessor.

    Note: this is an internal helper method to avoid multiple
    inheritance and composition issues and should not be used by user
    code.
    """
    obj.uitype = BUTTON
    obj.state = RELEASED
    obj.motion = EventHandler(obj)
    obj.pressed = EventHandler(obj)
    obj.released = EventHandler(obj)
    obj.click = EventHandler(obj)
    obj.events = {
        events.SDL_MOUSEMOTION: obj.motion,
        events.SDL_MOUSEBUTTONDOWN: obj.pressed,
        events.SDL_MOUSEBUTTONUP: obj.released
        }


def _compose_checkbutton(obj):
    """Binds check button attributes to the object, so it can be properly
    processed by the UIProcessor.

    Note: this is an internal helper method to avoid multiple
    inheritance and composition issues and should not be used by user
    code.
    """
    _compose_button(obj)
    obj.uitype = CHECKBUTTON
    obj.checked = False


def _compose_textentry(obj):
    """Binds text entry attributes to the object, so it can be properly
    processed by the UIProcessor.

    Note: this is an internal helper method to avoid multiple
    inheritance and composition issues and should not be used by user
    code.
    """
    obj.uitype = TEXTENTRY
    obj.text = ""
    obj.motion = EventHandler(obj)
    obj.pressed = EventHandler(obj)
    obj.released = EventHandler(obj)
    obj.keydown = EventHandler(obj)
    obj.keyup = EventHandler(obj)
    obj.input = EventHandler(obj)
    obj.editing = EventHandler(obj)
    obj.events = {
        events.SDL_MOUSEMOTION: obj.motion,
        events.SDL_MOUSEBUTTONDOWN: obj.pressed,
        events.SDL_MOUSEBUTTONUP: obj.released,
        events.SDL_TEXTEDITING: obj.editing,
        events.SDL_TEXTINPUT: obj.input,
        events.SDL_KEYDOWN: obj.keydown,
        events.SDL_KEYUP: obj.keyup
        }


class UIFactory(object):
    """A simple UI factory for creating GUI elements for software- or
    texture-based rendering."""
    def __init__(self, spritefactory, **kwargs):
        """Creates a new UIFactory.

        The additional kwargs will be stored internally and passed to the
        UI creation methods as arguments. Hence they can act as default
        arguments to be passed to each and every UI element to be
        created.
        """
        self.spritefactory = spritefactory
        self.default_args = kwargs

    def from_image(self, uitype, fname):
        """Creates a new UI element from the passed image file."""
        sprite = self.spritefactory.from_image(fname)
        if uitype == BUTTON:
            _compose_button(sprite)
        elif uitype == CHECKBUTTON:
            _compose_checkbutton(sprite)
        elif uitype == TEXTENTRY:
            _compose_textentry(sprite)
        else:
            del sprite
            raise ValueError("uitype must be a valid UI type identifier")
        return sprite

    def from_surface(self, uitype, surface, free=False):
        """Creates a new UI element from the passed SDL surface."""
        sprite = self.spritefactory.from_surface(surface, free)
        if uitype == BUTTON:
            _compose_button(sprite)
        elif uitype == CHECKBUTTON:
            _compose_checkbutton(sprite)
        elif uitype == TEXTENTRY:
            _compose_textentry(sprite)
        else:
            del sprite
            raise ValueError("uitype must be a valid UI type identifier")
        return sprite

    def from_object(self, uitype, obj):
        """Creates a new UI element from an arbitrary object."""
        sprite = self.spritefactory.from_object(obj)
        if uitype == BUTTON:
            _compose_button(sprite)
        elif uitype == CHECKBUTTON:
            _compose_checkbutton(sprite)
        elif uitype == TEXTENTRY:
            _compose_textentry(sprite)
        else:
            del sprite
            raise ValueError("uitype must be a valid UI type identifier")
        return sprite

    def from_color(self, uitype, color, size):
        """Creates a new UI element using a certain color."""
        sprite = self.spritefactory.from_color(color, size)
        if uitype == BUTTON:
            _compose_button(sprite)
        elif uitype == CHECKBUTTON:
            _compose_checkbutton(sprite)
        elif uitype == TEXTENTRY:
            _compose_textentry(sprite)
        else:
            del sprite
            raise ValueError("uitype must be a valid UI type identifier")
        return sprite

    def create_button(self, **kwargs):
        """Creates a new Sprite that can react on mouse events."""
        args = self.default_args.copy()
        args.update(kwargs)
        sprite = self.spritefactory.create_sprite(**args)
        _compose_button(sprite)
        return sprite

    def create_checkbutton(self, **kwargs):
        """Creates a new Sprite that can react on mouse events and
        retains its state."""
        args = self.default_args.copy()
        args.update(kwargs)
        sprite = self.spritefactory.create_sprite(**args)
        _compose_checkbutton(sprite)
        return sprite

    def create_text_entry(self, **kwargs):
        """Creates a new Sprite that can react on text input."""
        args = self.default_args.copy()
        args.update(kwargs)
        sprite = self.spritefactory.create_sprite(**args)
        _compose_textentry(sprite)
        return sprite

    def __repr__(self):
        return "UIFactory(spritefactory=%s, default_args=%s)" % \
            (self.spritefactory, self.default_args)


class UIProcessor(System):
    """A processing system for user interface elements and events."""
    def __init__(self):
        """Creates a new UIProcessor."""
        super(UIProcessor, self).__init__()
        self.componenttypes = (Sprite,)
        self._nextactive = None
        self._activecomponent = None
        self.handlers = {
            events.SDL_MOUSEMOTION: self.mousemotion,
            events.SDL_MOUSEBUTTONDOWN: self.mousedown,
            events.SDL_MOUSEBUTTONUP: self.mouseup,
            events.SDL_TEXTINPUT: self.textinput
            }

    def activate(self, component):
        """Activates a control to receive input."""
        if self._activecomponent and self._activecomponent != component:
            self.deactivate(self._activecomponent)

        if (component.uitype & TEXTENTRY):
            area = rect.SDL_Rect(component.x, component.y,
                                 component.size[0], component.size[1])
            keyboard.SDL_SetTextInputRect(area)
            keyboard.SDL_StartTextInput()
        self._activecomponent = component

    def deactivate(self, component):
        """Deactivates the currently active control."""
        if component == self._activecomponent:
            if (self._activecomponent.uitype & TEXTENTRY):
                keyboard.SDL_StopTextInput()
            self._activecomponent = None

    def passevent(self, component, event):
        """Passes the event to a component without any additional checks
        or restrictions.
        """
        component.events[event.type](event)

    def textinput(self, component, event):
        """Checks, if an active component is available and matches the
        passed component and passes the event on to that component."""
        if self._activecomponent == component:
            if (component.uitype & TEXTENTRY):
                component.text += stringify(event.text.text, "utf-8")
            component.events[event.type](event)

    def mousemotion(self, component, event):
        """Checks, if the event's motion position is on the component
        and executes the component's event handlers on demand.

        If the motion event position is not within the area of the
        component, nothing will be done. In case the component is a
        Button, its state will be adjusted to reflect, if it is
        currently hovered or not.
        """
        x1, y1, x2, y2 = component.area
        if event.motion.x >= x1 and event.motion.x < x2 and \
                event.motion.y >= y1 and event.motion.y < y2:
            # Within the area of the component, raise the event on it.
            component.events[event.type](event)
            if (component.uitype & BUTTON):
                component.state |= HOVERED
        elif (component.uitype & BUTTON):
            # The mouse is not within the area of the button, reset the
            # state
            component.state &= ~HOVERED

    def mousedown(self, component, event):
        """Checks, if the event's button press position is on the
        component and executes the component's event handlers on demand.

        If the button press position is not within the area of the
        component, nothing will be done. In case the component is a
        Button, its state will be adjusted to reflect, if it is
        currently pressed or not. In case the component is a TextEntry and
        the pressed button is the primary mouse button, the component will
        be marked as the next control to activate for text input.
        """
        x1, y1, x2, y2 = component.area
        if event.button.x >= x1 and event.button.x < x2 and \
                event.button.y >= y1 and event.button.y < y2:
            # Within the area of the component, raise the event on it.
            component.events[event.type](event)
            if (component.uitype & BUTTON):
                component.state = PRESSED | HOVERED
                if (component.uitype & CHECKABLE):
                    if event.button.button == mouse.SDL_BUTTON_LEFT:
                        component.checked = not component.checked
            # Since we loop over all components, and might deactivate
            # some, store it temporarily for later activation.
            self._nextactive = component
        elif (component.uitype & BUTTON):
            component.state &= ~PRESSED

    def mouseup(self, component, event):
        """Checks, if the event's button release position is on the
        component and executes the component's event handlers on demand.

        If the button release position is not within the area of the
        component, nothing will be done. In case the component is a
        Button, its state will be adjusted to reflect, whether it is
        hovered or not. If the button release followed a button press on
        the same component and if the button is the primary button, the
        click() event handler is invoked, if the component is a Button.
        """
        x1, y1, x2, y2 = component.area
        if event.button.x >= x1 and event.button.x < x2 and \
                event.button.y >= y1 and event.button.y < y2:
            # Within the area of the component, raise the event on it.
            component.events[event.type](event)
            if (component.uitype & BUTTON):
                if (component.state & PRESSED) == PRESSED:
                    # Was pressed already, now it is a click
                    component.click(event)
                component.state = RELEASED | HOVERED
        elif (component.uitype & BUTTON):
            component.state &= ~HOVERED

    def dispatch(self, obj, event):
        """Passes an event to the given object.

        If obj is a World object, UI relevant components will receive
        the event, if they support the event type.

        If obj is a single object, obj.events MUST be a dictionary
        consisting of SDL event type identifiers and EventHandler
        instances bound to the object. obj also must have a 'uitype' attribute
        referring to the UI type of the object.
        If obj is an iterable, such as a list or set, every item within
        obj MUST feature an 'events' and 'uitype' attribute as described
        above.
        """
        if event is None:
            return

        handler = self.handlers.get(event.type, self.passevent)
        if isinstance(obj, World):
            for ctype in self.componenttypes:
                items = obj.get_components(ctype)
                items = [(v, e) for v in items for e in (event,)
                         if hasattr(v, "events") and hasattr(v, "uitype") \
                            and e.type in v.events]
                if len(items) > 0:
                    arg1, arg2 = zip(*items)
                    map(handler, arg1, arg2)
        elif isiterable(obj):
            items = [(v, e) for v in obj for e in (event,)
                     if e.type in v.events]
            if len(items) > 0:
                for v, e in items:
                    handler(v, e)
        elif event.type in obj.events:
            handler(obj, event)
        if self._nextactive is not None:
            self.activate(self._nextactive)
            self._nextactive = None

    def process(self, world, components):
        """The UIProcessor class does not implement the process() method
        by default. Instead it uses dispatch() to send events around to
        components.
        """
        pass

    def __repr__(self):
        return "UIProcessor()"
