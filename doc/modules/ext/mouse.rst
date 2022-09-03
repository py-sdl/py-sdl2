`sdl2.ext.mouse` - Configuring and Handling Mouse Input
=======================================================

This module provides a number of functions to facilitate configuring and
retrieving input from the mouse in PySDL2.

The :func:`show_cursor`, :func:`hide_cursor`, and :func:`cursor_hidden`
functions let you easily show, hide, and check the state of the mouse cursor.
Additionally, you can check the absolute and relative location of the cursor
with the :func:`mouse_coords` and :func:`mouse_delta` functions (respectively),
and obtain the current state of the mouse buttons with
:func:`mouse_button_state`. The location of the mouse cursor can be changed
programatically using :func:`warp_mouse`.

.. automodule:: sdl2.ext.mouse
	:members:
