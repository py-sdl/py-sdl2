.. currentmodule:: sdl2.ext

Software Surface manipulation
=============================

.. function:: subsurface(surface : SDL_Surface, area : (int, int, int, int)) -> SDL_Surface

   Creates a surface from a part of another surface. The two surfaces share
   pixel data.
   
   .. note::
      
      The newly created surface *must not* be used after its parent has been
      freed!