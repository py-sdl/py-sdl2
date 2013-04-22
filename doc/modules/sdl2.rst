.. module:: sdl2
   :synopsis: SDL2 library wrapper

sdl2 - SDL2 library wrapper
===========================
The :mod:`sdl2` module is a :mod:`ctypes`-based wrapper around
the SDL2 library. It wraps nearly all publicly accessible structures and
functions of the SDL2 library to be accessible from Python code.

A detailled documentation about the behaviour of the different functions
can found within the `SDL2 documentation
<http://wiki.libsdl.org/moin.cgi/CategoryAPI>`_.

Missing interfaces
------------------
The following functions, classes, constants and macros of SDL2 are *not*
available within :mod:`sdl2`. 

* :c:data:`SDL_REVISION` and :c:data:`SDL_REVISION_NUMBER` from ``SDL_revision.h``
* :c:data:`SDL_NAME()` from ``SDL_name.h``
* :c:func:`SDL_MostSignificantBitIndex32` from ``SDL_bits.h``
* Anything from ``SDL_main.h``
* Anything from ``SDL_system.h``
* Anything from ``SDL_assert.h``
* Anything from ``SDL_thread.h``
* Anything from ``SDL_atomic.h``
* Anything from ``SDL_opengl.h``
* Anything from ``SDL_mutex.h`` 

Additional interfaces
---------------------
The following functions, classes, constants and macros are are *not* part of
SDL2, but were introduced by :mod:`sdl2`.

.. function:: sdl2.rwops.rw_from_object(obj : object) -> SDL_RWops

   Creates a SDL_RWops from any Python object. The Python object must at least
   support the following methods:

   read(length) -> data
   
     length is the size in bytes to be read. A call to len(data) must
     return the correct amount of bytes for the data, so that
     len(data) / [size in bytes for a single element from data] returns
     the amount of elements. Must raise an error on failure.

   seek(offset, whence) -> int
   
     offset denotes the offset to move the read/write pointer of the
     object to. whence indicates the movement behaviour and can be one
     of the following values:
                
     * RW_SEEK_SET - move to offset from the start of the file
     * RW_SEEK_CUR - move by offset from the relative location
     * RW_SEEK_END - move to offset from the end of the file
     
     If it could not move read/write pointer to the desired location,
     an error must be raised.

   tell() -> int
   
     Must return the current offset. This method must only be
     provided, if seek() does not return any value.

   close() -> None
   
     Closes the object(or its internal data access methods). Must raise
     an error on failure.

   write(data) -> None
   
     Writes the passed data(which is a string of bytes) to the object.
     Must raise an error on failure.

     .. note::

        The write() method is optional and only necessary, if the passed
        object should be able to write data.

   The returned :class:`sdl2.rwops.SDL_RWops` is a pure Python object and
   **must not** be freed via :func:`sdl2.rwops.SDL_FreeRW()`.
