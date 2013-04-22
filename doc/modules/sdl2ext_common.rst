.. module:: sdl2.ext.common
   :synopsis: Video and graphics routines

sdl2.ext.common - Initialization routines
=========================================
The :mod:`sdl2.ext.common` module contains various classes and methods
for creating, processing and manipulating on-screen graphics.

API
---

.. exception:: SDLError(msg=None)

   An SDL2 specific :class:`Exception` class. if no *msg* is provided,
   the message will be set to the value of :func:`sdl2.error.SDL_GetError()`

.. function:: init() -> None

   Initializes the underlying SDL2 video subsystem. Raises a
   :exc:`SDLError`, if the SDL2 video subsystem could not be
   initialised.

.. function:: quit() -> None

   Quits the underlying SDL2 video subysystem. If no other SDL2 subsystems are
   active, this will also call :func:`quit()`.

.. function:: get_events() -> [SDL_Event, SDL_Event, ...]

   Gets all SDL events that are currently on the event queue.

.. class:: TestEventProcessor()

   A simple event processor for testing purposes.

   .. method:: run(window : Window) -> None

      Starts an event loop without actually processing any event. The method
      will run endlessly until a ``SDL_QUIT`` event occurs.
