.. currentmodule:: sdl2.ext

2D and 3D direct pixel access
=============================

.. class:: PixelView(source : object)

   2D :class:`MemoryView` for :class:`SoftwareSprite` and 
   :class:`sdl2.SDL_surface` pixel access.
  
   .. note::

      If necessary, the *source* surface will be locked for accessing its
      pixel data. The lock will be removed once the :class:`PixelView` is
      garbage-collected or deleted.

    The :class:`PixelView`  uses a y/x-layout. Accessing ``view[N]`` will
    operate on the Nth row of the underlying surface. To access a specific
    column within that row, ``view[N][C]`` has to be used.
    
    .. note:: 
    
       :class:`PixelView` is implemented on top of the :class:`MemoryView`
       class. As such it makes heavy use of recursion to access rows and
       columns and can be considered as slow in contrast to optimised
       ndim-array solutions such as :mod:`numpy`.

.. function:: pixels2d(source : object, transpose : bool)

   Creates a 2D pixel array, based on ``numpy.ndarray``, from the passed
   *source*. *source* can be a :class:`SoftwareSprite` or
   :class:`sdl2.SDL_Surface`. The ``SDL_Surface`` of the *source* will be
   locked and unlocked automatically.

   By default, the returned array is formatted so that the first dimension
   corresponds to height on the source and the second dimension corresponds
   to width, contrary to PIL and PyOpenGL convention. To obtain an array where
   the first dimension is width and second dimension is height, set the
   `transpose` argument to False.

   The *source* pixels will be accessed and manipulated directly.

   .. note::

      :func:`pixels2d` is only usable, if the numpy package is available
      within the target environment. If numpy could not be imported, a
      :exc:`sdl2.ext.compat.UnsupportedError` will be raised.

.. function:: pixels3d(source : object, transpose : bool)

   Creates a 3D pixel array, based on ``numpy.ndarray``, from the passed
   *source*. *source* can be a :class:`SoftwareSprite`
   or :class:`sdl2.SDL_Surface`. The ``SDL_Surface`` of the *source*
   will be locked and unlocked automatically.

   By default, the returned array is formatted so that the first dimension
   corresponds to height on the source and the second dimension corresponds
   to width, contrary to PIL and PyOpenGL convention. To obtain an array where
   the first dimension is width and second dimension is height, set the
   `transpose` argument to False.

   The *source* pixels will be accessed and manipulated directly.

   .. note::

      :func:`pixels3d` is only usable, if the numpy package is available
      within the target environment. If numpy could not be imported, a
      :exc:`sdl2.ext.compat.UnsupportedError` will be raised.
