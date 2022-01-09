.. module:: sdl2.ext.compat
   :synopsis: Python compatibility helpers.

sdl2.ext.compat - Python compatibility helpers
==============================================
The :mod:`sdl2.ext.compat` module is for internal purposes of the :mod:`sdl2`
package and should not be used outside of the package. Classes, methods and
interfaces might change between versions and there is no guarantee of API
compatibility on different platforms and python implementations or between
releases.

.. data:: ISPYTHON2

   ``True``, if executed in a Python 2.x compatible interpreter, ``False``
   otherwise.

.. data:: ISPYTHON3

   ``True``, if executed in a Python 3.x compatible interpreter, ``False``
   otherwise.

.. function:: long([x[, base]])

   .. note::

      Only defined for Python 3.x, for which it is the same as :func:`int()`.

.. function:: unichr(i)

   .. note::

      Only defined for Python 3.x, for which it is the same as :func:`chr()`.

.. function:: unicode(string[, encoding[, errors]])

   .. note::

      Only defined for Python 3.x, for which it is the same as :func:`str()`.

.. function:: callable(x) -> bool

   .. note::

      Only defined for Python 3.x, for which it is the same as
      ``isinstance(x, collections.Callable)``

.. function:: byteify(x : string, enc : string) -> bytes

   Converts a string to a :func:`bytes` object.

.. function:: stringify(x : bytes, enc : string) -> string

   Converts a :func:`bytes` to a string object.

.. function:: isiterable(x) -> bool

   Shortcut for ``isinstance(x, collections.Iterable)``.

.. function:: platform_is_64bit() -> bool

   Checks, if the interpreter is 64-bit capable.

.. decorator:: deprecated

   A simple decorator to mark functions and methods as deprecated. This will
   print a deprecation message each time the function or method is invoked.

.. function:: deprecation(message : string) -> None

   Prints a deprecation message using the :func:`warnings.warn()` function.

.. exception:: UnsupportedError(obj : object[, msg=None])

   Indicates that a certain class, function or behaviour is not supported in
   the specific execution environment.

.. decorator:: experimental

   A simple decorator to mark functions and methods as
   experimental. This will print a warning each time the function or
   method is invoked.

.. exception:: ExperimentalWarning(obj : object[, msg=None])

   Indicates that a certain class, function or behaviour is in an
   experimental state.
