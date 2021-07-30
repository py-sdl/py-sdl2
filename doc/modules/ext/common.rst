.. currentmodule:: sdl2.ext

Initialization routines
=======================

:func:`init()` simply calls :func:`SDL_Init()` to initialize only the video
subsystem. If the call fails, :exc:`SDLError` is raised. See
:ref:`pygamers_pygame` for a comparison between this function and
:func:`pygame.init()`.


API
---

.. exception:: SDLError(msg=None)

   An SDL2 specific :class:`Exception` class. if no *msg* is provided,
   the message will be set to the value of :func:`sdl2.error.SDL_GetError()`

.. function:: init() -> None

   Initialises the underlying SDL2 video subsystem. Raises a
   :exc:`SDLError`, if the SDL2 video subsystem could not be
   initialised.

.. function:: quit() -> None

   Quits the underlying SDL2 video subysystem. If no other SDL2
   subsystems are active, this will also call :func:`quit()`,
   :func:`sdl2.sdlttf.TTF_Quit()` and :func:`sdl2.sdlimage.IMG_Quit()`.

.. function:: get_events() -> [SDL_Event, SDL_Event, ...]

   Gets all SDL events that are currently on the event queue.

.. class:: TestEventProcessor()

   A simple event processor for testing purposes.

   .. method:: run(window : Window) -> None

      Starts an event loop without actually processing any event. The method
      will run endlessly until a ``SDL_QUIT`` event occurs.
