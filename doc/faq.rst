.. _faq:

PySDL2 FAQ
==========
This is a list of Frequently Asked Questions about PySDL2. If you think,
something is missing, please suggest it!

On importing...
---------------
... my script fails and complains that a SDL2 library could not be found!
    
   Do you have the libraries properly installed? If on macOS or Windows, 
   try running ``pip install pysdl2-dll`` and opening a fresh terminal
   to fix the problem. If on Linux or similar, did you follow the operating
   system's way of installing or registering libraries? If you placed the
   libraries in some folder, make sure that the ``PYSDL2_DLL_PATH``
   environment variable points to the correct location.
   
... my script fails complaining that the *found* SDL2 library can't be used!

   Do you use a 64-bit operating system? Please make sure, that the Python
   interpreter *and* that the SDL2 libraries are either 64-bit ones *or*
   32-bit ones. A 32-bit Python interpreter can't deal with a 64-bit library
   and vice versa.

Using...
--------

... the sdl2 API is weird. Why do you use the SDL\_ prefix all the time?

   The low-level APIs for SDL2, SDL2\_mixer, SDL2\_ttf, ... shall represent a 
   clean wrapping around the original C API calls. Thus, if you have to search
   for documentation or want to make a Python to C conversion (or C to Python),
   most of the code cleanly maps to the original API naming and layout and you
   do not have to think about whether you had to use SDL\_ or TTF\_ or whatever
   as prefix or suffix.

... the sdl2 API is does not comply to PEP-8. Please make it PEP-8 compatible.

   Most of the API is PEP-8 compatible. The low-level bindings to SDL2 and
   related libraries however use the exact naming (including capital letters)
   as the functions or structures, they map to. See the previous entry for
   the reason of that.

How do I...
-----------

... save my surfaces as image files?

   You can use :func:`sdl2.SDL_SaveBMP()` to save them as bitmap files. Other
   formats are currently unsupported, but might be added to
   the :mod:`sdl2.ext` package in the future.
   
   
Font handling...
----------------

... is too hard. Why can't it work the same way as pygame does?

   The :mod:`sdl2.sdlttf` API does not know about platform-specific font
   locations and is unable to resolve font paths based on e.g. the font name
   or typeface. It's not its job and PySDL2 likewise does not provide such
   functionality. If you need improved font detection support, you might want
   to take a look at the sysfont module of the python-utils project, which can
   be found at https://bitbucket.org/marcusva/python-utils/. That said, it's
   usually a bad idea for a projects to rely on system fonts that may not be
   available on every computer: finding a free-use font you like and bundling
   it with your code is much safer.
