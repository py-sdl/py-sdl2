`sdl2.ext.input` - Handling SDL2 Input Events
=============================================

This module provides a range of Pythonic functions for handling and processing
SDL input events (e.g. key presses, mouse clicks, unicode text input) as
retrieved from :func:`~sdl2.ext.get_events`.

The :func:`key_pressed` function allows for easily checking whether a given key
has been pressed (or released). Likewise, :func:`mouse_clicked` lets you handle
mouse button press and release events. If you want to check the `locations` of
mouse clicks, :func:`get_clicks` returns the pixel coordinates for all clicks
(if any) in a given list of events.

For handling text entry in PySDL2 (including unicode characters),
:func:`get_text_input` returns all text input in a given list of events as a
unicode string. Note that text input events are disabled by default in SDL, but
can easily be enabled/disabled using :func:`start_text_input` and
:func:`stop_text_input`.

.. automodule:: sdl2.ext.input
	:members:
