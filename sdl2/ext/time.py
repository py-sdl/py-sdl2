"""Track and control game time and framerate.

.. note::

  This is a **MODIFIED**, pure Python implementation of time-related functions
  from `PyGameSDL2's time`_, in Cython, released under zlib license.

.. code-block:: none

  PygameSDL2 Notice / zlib License:

  --------------------------------------------------------------------------
  Original work:
    Copyright 2014 Tom Rothamel <tom@rothamel.us>
    Copyright 2014 Patrick Dawson <pat@dw.is>
  Modified work:
    Copyright 2017 Lucas Siqueira <lucas.morais.siqueira@gmail.com>

  This software is provided 'as-is', without any express or implied
  warranty.  In no event will the authors be held liable for any damages
  arising from the use of this software.

  Permission is granted to anyone to use this software for any purpose,
  including commercial applications, and to alter it and redistribute it
  freely, subject to the following restrictions:

  1. The origin of this software must not be misrepresented; you must not
     claim that you wrote the original software. If you use this software
     in a product, an acknowledgment in the product documentation would be
     appreciated but is not required.
  2. Altered source versions must be plainly marked as such, and must not
     be misrepresented as being the original software.
  3. This notice may not be removed or altered from any source
     distribution.
  --------------------------------------------------------------------------

.. _`PyGameSDL2's time`: https://www.github.com/renpy/pygame_sdl2/blob/\
    master/src/pygame_sdl2/pygame_time.pyx
"""

import math
from ..timer import SDL_Delay, SDL_GetTicks


__all__ = ('Clock', 'wait', 'get_time', 'get_delta')


def get_delta(t0):
    """Get the time elapsed since the passed time."""
    return get_time - t0


def get_time():
    """Get the current time from SDL clock."""
    return SDL_GetTicks()


def wait(milliseconds):
    """Pause the program for an amount of time.

    Will pause for a given number of milliseconds. This function sleeps the
    process to share the processor with other programs. A program that waits
    for even a few milliseconds will consume very little processor time.

    Usage:
        wait(milliseconds)

    Returns:
        int (the actual number of milliseconds used)
    """
    start = SDL_GetTicks()
    SDL_Delay(int(milliseconds))
    return SDL_GetTicks() - start


class Clock:
    """Clock is used track and control the framerate of a game.

    The clock can be used to limit the framerate of a game, as well as track
    the time used per frame.

    Usage:
        clock = time.Clock()
    """

    def __init__(self):
        """Initialization."""
        self.last = SDL_GetTicks()
        self.last_frames = []
        self.frametime = 0
        self.raw_frametime = 0

    def tick(self, framerate=0):
        """Update the Clock.

        This method should be called once per frame. It will compute how many
        milliseconds have passed since the previous call.

        If you pass the optional framerate argument the function will delay
        to keep the game running slower than the given ticks per second. This
        can be used to help limit the runtime speed of a game. By calling
        clock.tick(40) once per frame, the program will never run at more
        than 40 frames per second.

        Usage:
            tick(framerate=0)

        Returns:
            float (milliseconds)
        """
        now = SDL_GetTicks()
        self.raw_frametime = now - self.last
        while len(self.last_frames) > 9:
            self.last_frames.pop(0)
        if framerate == 0:
            self.last = now
            self.last_frames.append(self.raw_frametime)
            return self.raw_frametime
        frame_duration = 1.0 / framerate * 1000
        if self.raw_frametime < frame_duration:
            wait(frame_duration - self.raw_frametime)
        now = SDL_GetTicks()
        self.frametime = now - self.last
        self.last = now
        self.last_frames.append(self.frametime)
        return self.frametime

    def get_time(self):
        """Time used in the previous tick.

        Returns the parameter passed to the last call to Clock.tick().

        Usage:
            clock.get_time()

        Returns:
            int (milliseconds)
        """
        return self.frametime

    def get_rawtime(self):
        """Actual time used in the previous tick.

        Similar to Clock.get_time(), but this does not include any time used
        while clock.tick() was delaying to limit the framerate.

        Usage:
            clock.get_rawtime()

        Returns:
            int (milliseconds)
        """
        return self.raw_frametime

    def get_fps(self):
        """Compute the clock framerate.

        Compute your game's framerate (in frames per second). It is computed
        by averaging the last ten calls to Clock.tick().

        Usage:
            get_fps()

        Returns:
            float
        """
        total_time = sum(self.last_frames)
        average_time = total_time / 1000.0 / len(self.last_frames)
        average_fps = 1.0 / average_time
        return 0 if math.isnan(average_fps) else average_fps
