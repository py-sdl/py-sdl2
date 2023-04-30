import ctypes
from .. import (timer, error, dll,
    SDL_Init, SDL_InitSubSystem, SDL_Quit, SDL_QuitSubSystem, SDL_WasInit,
    SDL_INIT_VIDEO, SDL_INIT_AUDIO, SDL_INIT_TIMER, SDL_INIT_HAPTIC,
    SDL_INIT_JOYSTICK, SDL_INIT_GAMECONTROLLER, SDL_INIT_SENSOR, SDL_INIT_EVENTS,
)
from ..events import (
    SDL_Event, SDL_PumpEvents, SDL_PeepEvents,  SDL_PollEvent,
    SDL_QUIT, SDL_GETEVENT, SDL_FIRSTEVENT, SDL_LASTEVENT,
)
from .compat import isiterable
from .err import raise_sdl_err

_HASSDLTTF = True
try:
    from .. import sdlttf
except ImportError:
    _HASSDLTTF = False
_HASSDLIMAGE = True
try:
    from .. import sdlimage
except ImportError:
    _HASSDLIMAGE = False

__all__ = ["init", "quit", "get_events", "quit_requested", "TestEventProcessor"]


_sdl_subsystems = {
    'timer': SDL_INIT_TIMER,
    'audio': SDL_INIT_AUDIO,
    'video': SDL_INIT_VIDEO,
    'joystick': SDL_INIT_JOYSTICK,
    'haptic': SDL_INIT_HAPTIC,
    'gamecontroller': SDL_INIT_GAMECONTROLLER,
    'events': SDL_INIT_EVENTS,
    'sensor': SDL_INIT_SENSOR,
}


def init(
    video=True, audio=False, timer=False, joystick=False, controller=False,
    haptic=False, sensor=False, events=True
):
    """Initializes SDL and its optional subsystems.

    By default, only the video and events subsystems are initialized. Note that
    the sensor subsystem requires SDL 2.0.9 or later.

    Args:
        video (bool, optional): Whether to initialize the SDL video subsystem.
            If True, the events subsystem will also be initialized. Defaults
            to True.
        audio (bool, optional): Whether to initialize the SDL audio subsystem.
            Defaults to False.
        timer (bool, optional): Whether to initialize the SDL timer subsystem.
            Defaults to False.
        joystick (bool, optional): Whether to initialize the SDL joystick
            subsystem. If True, the events subsystem will also be initialized.
            Defaults to False.
        controller (bool, optional): Whether to initialize the SDL gamecontroller
            subsystem. If True, the joystick subsystem will also be initialized.
            Defaults to False.
        haptic (bool, optional): Whether to initialize the SDL haptic (force
            feedback) subsystem. Defaults to False.
        sensor (bool, optional): Whether to initialize the SDL sensor subsystem.
            Defaults to False.
        events (bool, optional): Whether to initialize the SDL events subsystem.
            Will automatically be initialized if the video, joystick, or
            gamecontroller subsystems are enabled. Defaults to False.

    See :ref:`pygamers_pygame` for a comparison between this function and
    ``pygame.init()``.

    Raises:
        :exc:`SDLError`: If a requested SDL subsystem cannot be initialized.

    """
    subsystems = []
    if events:
        subsystems.append("events")
    if video:
        subsystems.append("video")
    if audio:
        subsystems.append("audio")
    if timer:
        subsystems.append("timer")
    if joystick:
        subsystems.append("joystick")
    if controller:
        subsystems.append("gamecontroller")
    if haptic:
        subsystems.append("haptic")
    if sensor:
        subsystems.append("sensor")

    if SDL_Init(0) != 0:
        raise_sdl_err("initializing SDL2")

    for s in subsystems:
        if s == "sensor" and dll.version < 2009:
            e = "The sensor subsystem requires SDL 2.0.9 or later."
            raise RuntimeError(e)
        if SDL_InitSubSystem(_sdl_subsystems[s]) != 0:
            raise_sdl_err("initializing the {0} subsystem".format(s))


def quit():
    """Quits the SDL2 video subysystem.

    If no other subsystems are active, this will also call
    :func:`sdl2.SDL_Quit`, :func:`sdlttf.TTF_Quit` and
    :func:`sdlimage.IMG_Quit`.

    """
    # TODO: More subsystems? Also, is TTF_WasInit always 1?
    SDL_QuitSubSystem(SDL_INIT_VIDEO)
    if SDL_WasInit(0) != 0:
        if _HASSDLTTF and sdlttf.TTF_WasInit() > 0:
            sdlttf.TTF_Quit()
        if _HASSDLIMAGE:
            sdlimage.IMG_Quit()
        SDL_Quit()


def get_events():
    """Gets all SDL events that are currently on the event queue.

    Returns:
        :obj:`List`: A list of all :obj:`~sdl2.SDL_Event` objects currently in
        the event queue.
    
    """
    SDL_PumpEvents()

    evlist = []
    while True:
        evarray = (SDL_Event * 10)()
        ptr = ctypes.cast(evarray, ctypes.POINTER(SDL_Event))
        ret = SDL_PeepEvents(
            ptr, 10, SDL_GETEVENT, SDL_FIRSTEVENT, SDL_LASTEVENT
        )
        if ret <= 0:
            break
        evlist += list(evarray)[:ret]
        if ret < 10:
            break

    return evlist


def quit_requested(events):
    """Checks for quit requests in a given event queue.

    Quit requests occur when an SDL recieves a system-level quit signal (e.g
    clicking the 'close' button on an SDL window, pressing Command-Q on macOS).
    This function makes it easier to handle these events in your code::

        running = True
        while running:
            events = sdl2.ext.get_events()
            if quit_requested(events):
                running = False

    Args:
        events (list of :obj:`sdl2.SDL_Event`): A list of SDL events to check
            for quit requests.

    Returns:
        bool: True if a quit request has occurred, otherwise False.

    """
    # Ensure 'events' is iterable
    if not isiterable(events):
        events = [events]

    # Check for any quit events in the queue
    requested = False
    for e in events:
        if e.type == SDL_QUIT:
            requested = True
            break

    return requested


class TestEventProcessor(object):
    """A simple event processor for testing purposes."""

    def run(self, window):
        """Starts an event loop without actually processing any event.
        
        This method will run endlessly until an ``SDL_QUIT`` event occurs.

        Args:
            window (:obj:`sdl2.ext.Window`): The window within which to run
                the test event loop.
        
        """
        event = SDL_Event()
        running = True
        while running:
            ret = SDL_PollEvent(ctypes.byref(event), 1)
            if ret == 1:
                if event.type == SDL_QUIT:
                    running = False
                    break
            window.refresh()
            timer.SDL_Delay(10)
