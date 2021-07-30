.. currentmodule:: sdl2.ext

Resource management
===================
Every application usually ships with various resources, such as image and data
files, configuration files and so on. Accessing those files in the folder
hierarchy or in a bundled format for various platforms can become a complex
task. The :class:`Resources` class allows you to manage different application
data in a certain directory, providing a dictionary-style access functionality
for your in-application resources.

Let's assume, your application has the following installation layout ::

    Application Directory
        Application.exe
        Application.conf
        data/
            background.jpg
            button1.jpg
            button2.jpg
            info.dat

Within the ``Application.exe`` code, you can - completely system-agnostic -
define a new resource that keeps track of all ``data`` items. ::

    apppath = os.path.dirname(os.path.abspath(__file__))
    appresources = Resources(os.path.join(apppath, "data"))
    # Access some images
    bgimage = appresources.get("background.jpg")
    btn1image = appresources.get("button1.jpg")
    ...

To access individual files, you do not need to concat paths the whole
time and regardless of the current directory, your application operates
on, you can access your resource files at any time through the
:class:`Resources` instance, you created initially.

The :class:`Resources` class is also able to scan an index archived files,
compressed via ZIP or TAR (gzip or bzip2 compression), and subdiectories
automatically. ::

    Application Directory
        Application.exe
        Application.conf
        data/
            audio/
                example.wav
            background.jpg
            button1.jpg
            button2.jpg
            graphics.zip
                [tileset1.bmp
                 tileset2.bmp
                 tileset3.bmp
                 ]
            info.dat

    tilesimage = appresources.get("tileset1.bmp")
    audiofile = appresources.get("example.wav")

If you request an indexed file via :meth:`Resources.get`, you will receive
a :class:`io.BytesIO` stream, containing the file data, for further processing.

.. note::

   The scanned files act as keys within the :class:`Resources` class. This
   means that two files, that have the same name, but are located in different
   directories, will not be indexed. Only one of them will be accessible
   through the :class:`Resources` class.

API
---

.. class:: Resources([path=None[, subdir=None[, excludepattern=None]]])

   The Resources class manages a set of file resources and eases
   accessing them by using relative paths, scanning archives
   automatically and so on.

   .. method:: add(filename : string)

      Adds a file to the resource container. Depending on the
      file type (determined by the file suffix or name) the file will be
      automatically scanned (if it is an archive) or checked for
      availability (if it is a stream or network resource).

   .. method:: add_archive(filename : string[, typehint="zip"])

      Adds an archive file to the resource container. This will scan the
      passed archive and add its contents to the list of available and
      accessible resources.

   .. method:: add_file(filename : string)

      Adds a file to the resource container. This will only add the
      passed file and do not scan an archive or check the file for
      availability.

   .. method:: get(filename : string) -> BytesIO

      Gets a specific file from the resource container.

      Raises a :exc:`KeyError`, if the *filename* could not be found.

   .. method:: get_filelike(filename : string) -> file object

      Similar to :meth:`get()`, but tries to return the original file
      handle, if possible. If the found file is only available within an
      archive, a :class:`io.BytesIO` instance will be returned.

      Raises a :exc:`KeyError`, if the *filename* could not be found.

   .. method:: get_path(filename : string) -> string

      Gets the path of the passed *filename*. If *filename* is only
      available within an archive, a string in the form
      ``filename@archivename`` will be returned.

      Raises a :exc:`KeyError`, if the *filename* could not be found.

   .. method:: scan(path : string[, subdir=None[, excludepattern=None])

      Scans a path and adds all found files to the resource
      container. If a file within the path is a supported archive (ZIP
      or TAR), its contents will be indexed aut added automatically.

      The method will consider the directory part (``os.path.dirname``)
      of the provided *path* as path to scan, if the path is not a
      directory. If *subdir* is provided, it will be appended to the
      path and used as starting point for adding files to the resource
      container.

      *excludepattern* can be a regular expression to skip
      directories, which match the pattern.

.. function:: open_tarfile(archive : string, filename : string \
                           [, directory=None[, ftype=None]]) -> BytesIO

   Opens and reads a certain file from a TAR archive. The result is
   returned as :class:`BytesIO` stream. *filename* can be a relative
   or absolute path within the TAR archive. The optional *directory*
   argument can be used to supply a relative directory path, under which
   *filename* will be searched.

   *ftype* is used to supply additional compression information, in
   case the system cannot determine the compression type itself, and can
   be either **"gz"** for gzip compression or **"bz2"** for bzip2
   compression.

   If the filename could not be found or an error occurred on reading it,
   ``None`` will be returned.

   Raises a :exc:`TypeError`, if *archive* is not a valid TAR archive or
   if *ftype* is not a valid value of ("gz", "bz2").

   .. note::

      If *ftype* is supplied, the compression mode will be enforced for
      opening and reading.

.. function:: open_url(filename : string[, basepath=None]) -> file object

   Opens and reads a certain file from a web or remote location. This
   function utilizes the :mod:`urllib2` module for Python 2.7 and
   :mod:`urllib` for Python 3.x, which means that it is restricted to
   the types of remote locations supported by the module.

   *basepath* can be used to supply an additional location prefix.

.. function:: open_zipfile(archive : string, filename : string \
                           [, directory : string]) -> BytesIO

   Opens and reads a certain file from a ZIP archive. The result is
   returned as :class:`BytesIO` stream. *filename* can be a relative
   or absolute path within the ZIP archive. The optional *directory*
   argument can be used to supply a relative directory path, under which
   *filename* will be searched.

   If the filename could not be found, a :exc:`KeyError` will be raised.
   Raises a :exc:`TypeError`, if *archive* is not a valid ZIP archive.
