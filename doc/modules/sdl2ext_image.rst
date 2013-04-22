.. module:: sdl2.ext.image
   :synopsis: Image loaders

sdl2.ext.image - Image loaders
==============================

.. function:: get_image_formats() -> (str, str, ...)

   Gets the formats supported by PySDL2 in the default installation.

.. function:: load_image(fname : str[, renderer=None[,assurface=False[, enforce=None]]]) -> SDL_Surface, Sprite or SoftSprite

   Creates a :class:`sdl2.surface.SDL_Surface` from an image file.

   This function makes use of the `Python Imaging Library
   <http://www.pythonware.com/products/pil/>`_, if it is available on
   the target execution environment. The function will try to load the
   file via :mod:`sdl2.sdlimage` first. If the file could not be
   loaded, it will try to load it via PIL.

   You can force the function to use only one of them, by passing the
   *enforce* as either ``"PIL"`` or ``"SDL"``.

   .. note::

      This will call :func:`sdl2.sdlimage.init()` implicitly with the
      default arguments, if the module is available.
