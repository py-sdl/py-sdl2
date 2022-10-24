`sdl2.ext.mouse` - Configuring and Handling Mouse Input
=======================================================

This module provides a number of functions to make it easier to configure and
retrieve mouse input in PySDL2.

The :func:`show_cursor`, :func:`hide_cursor`, and :func:`cursor_hidden`
functions allow you to easily show, hide, and check the visibility of the mouse
cursor. Additionally, you can check the cursor's absolute or relative location
with the :func:`mouse_coords` and :func:`mouse_delta` functions (respectively),
or obtain the current state of the mouse buttons with
:func:`mouse_button_state`. The location of the mouse cursor can be changed
programatically using :func:`warp_mouse`.

.. automodule:: sdl2.ext.mouse
	:members:
