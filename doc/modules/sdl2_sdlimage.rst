sdl2.sdlimage - Python bindings for SDL2_image
==============================================

py-sdl2 provides bindings for SDL2_image, a library designed for use with SDL2
that adds support for loading a wide range of different common (and uncommon)
image formats for easy use with SDL2. In addition, SDL2_image includes functions
for saving :obj:`SDL_Surface` objects to PNG and/or JPEG images.

.. note::
   If using an alternative rendering system that doesn't use SDL surfaces as
   input (e.g. PyOpenGL), the Pillow imaging library may be a better fit for
   your project.


Initialization and library information functions
------------------------------------------------

.. function:: IMG_Init(flags)

   Initializes the SDL2_image library, enabling support for JPEG, PNG, TIF,
   and/or WebP images as requested. All other image formats can be loaded
   or used regardless of whether this has been called.

   The following are the supported init flags:

   ====== =================
   Format Init flag
   ====== =================
   JPEG   ``IMG_INIT_JPG``
   PNG    ``IMG_INIT_PNG``
   TIFF   ``IMG_INIT_TIF``
   WebP   ``IMG_INIT_WEBP``
   ====== =================

   Can be called multiple times to enable support for these formats
   separately, or can initialize multiple formats at once by passing a set of
   flags as a bitwise OR. You can also call this function with 0 as a flag
   to check which image libraries have already been loaded.

   .. code-block:: python

      # Initialize JPEG and PNG support separately
      for flag in [IMG_INIT_JPG, IMG_INIT_PNG]:
          IMG_Init(flag)
          err = IMG_GetError() # check for any errors loading library
          if len(err):
              print(err)

      # Initialize JPEG and PNG support at the same times
      flags = IMG_INIT_JPG | IMG_INIT_PNG
      IMG_Init(flags)
      if IMG_Init(0) != flags: # verify both libraries loaded properly
          print(IMG_GetError())

   :param flags: A bitwise OR'd set of image formats to load support for.
   :type flags: int

   :retuns: A bitmask of all the currently initialized image loaders.
   :rtype: int


.. function:: IMG_Quit()

   De-initializes the SDL2_image library, disabling JPEG, PNG, TIF, and
   WEBP support and freeing all associated memory.

   Once this has been called, you can re-initialize support for those
   image formats using :func:`IMG_Init` and the corresponding init flags.
   You only need to call this function once, no matter how many times
   :func:`IMG_Init` was called.


.. function:: IMG_GetError()

   Returns the most recently encountered SDL2 error message, if any.

   This function is a simple wrapper around :func:`SDL_GetError`.

   :retuns: A UTF-8 encoded string describing the most recent SDL2 error.
   :rtype: bytes


.. function:: IMG_SetError(fmt)

   Sets the most recent SDL2 error message to a given string.

   This function is a simple wrapper around :func:`SDL_SetError`.

   :param fmt: A UTF-8 encoded string containing the error message to set.
   :type fmt: bytes

   :retuns: Always returns ``-1``.
   :rtype: int


.. function:: IMG_Linked_Version()

   This function gets the version of the dynamically linked SDL2_image
   library.

   :returns: A pointer to an object containing the version of the SDL2_image
     library currently in use.
   :rtype: POINTER(:obj:`SDL_version`)


Image format-checking functions
-------------------------------

These functions are used to check whether an SDL file object
(:obj:`SDL_RWops`) is a valid image file of a given format. Note that
all of these functions will return 0 if SDL2_image was not built with
support for that format, even if it is a valid image of that type, so be
cautious when using these for formats like WEBP, JPEG, PNG, and TIFF, which
are optional when building SDL2_image.


.. function:: IMG_isICO(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable ICO
   (Windows icon) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if BMPs are supported and file is a valid ICO, otherwise 0.
   :rtype: int


.. function:: IMG_isCUR(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable CUR
   (non-animated Windows cursor) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if BMPs are supported and file is a valid CUR, otherwise 0.
   :rtype: int


.. function:: IMG_isBMP(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable BMP
   (Windows bitmap) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if BMPs are supported and file is a valid BMP, otherwise 0.
   :rtype: int


.. function:: IMG_isGIF(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable GIF
   (Graphics Interchange Format) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if GIFs are supported and file is a valid GIF, otherwise 0.
   :rtype: int


.. function:: IMG_isJPG(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable JPEG
   image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if JPEGs are supported and file is a valid JPEG, otherwise 0.
   :rtype: int


.. function:: IMG_isLBM(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable LBM
   (Interleaved Bitmap, ``.lbm`` or ``.iff``) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if LBMs are supported and file is a valid LBM, otherwise 0.
   :rtype: int


.. function:: IMG_isPCX(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable PCX
   (IBM PC Paintbrush) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if PCXs are supported and file is a valid PCX, otherwise 0.
   :rtype: int


.. function:: IMG_isPNG(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable PNG
   (Portable Network Graphics) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if PNGs are supported and file is a valid PNG, otherwise 0.
   :rtype: int


.. function:: IMG_isPNM(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable PNM
   (Portable Anymap, ``.pbm`` or ``.pgm`` or ``.ppm``) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if PNMs are supported and file is a valid PNM, otherwise 0.
   :rtype: int


.. function:: IMG_isSVG(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable SVG
   (Scalable Vector Graphics) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if SVGs are supported and file is a valid SVG, otherwise 0.
   :rtype: int


.. function:: IMG_isTIF(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable TIFF
   (Tagged Image File Format) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if TIFFs are supported and file is a valid TIFF, otherwise 0.
   :rtype: int


.. function:: IMG_isXCF(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable XCF
   (native GIMP format) image.

   .. note:: XCF support is currently missing in official macOS binaries

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if XCFs are supported and file is a valid XCF, otherwise 0.
   :rtype: int


.. function:: IMG_isXPM(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable XPM
   (X11 Pixmap) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if XPMs are supported and file is a valid XPM, otherwise 0.
   :rtype: int


.. function:: IMG_isXV(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable XV
   thumbnail (XV Visual Schnauzer format) image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if XV thumbnails are supported and file is a valid XV
     thumbnail, otherwise 0.
   :rtype: int


.. function:: IMG_isWEBP(src)

   Tests whether a :obj:`SDL_RWops` file object contains a readable WebP
   image.

   :param src: The file object to check.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: 1 if WebPs are supported and file is a valid WebP, otherwise 0.
   :rtype: int


General image loading functions
-------------------------------

.. function:: IMG_Load(file)

   Loads an image file to a new surface. This can load all supported image
   files, including TGA as long as the filename ends with ".tga".

   It is best to call this outside of event loops and keep the loaded
   images around until you are really done with them, as disk speed and
   image conversion to a surface can be slow.

   Once you are done with a loaded image, you can call
   :func:`SDL_FreeSurface` on the returned surface pointer to free up the
   memory associated with it.

   If the image format supports a transparent pixel, SDL_image will set the
   colorkey for the surface. You can enable RLE acceleration on the surface
   afterwards by calling::

      SDL_SetColorKey(image, SDL_RLEACCEL, image.contents.format.colorkey)

   .. note:: If the image loader for the format of the given image requires
             initialization (e.g. PNG) and it is not already initialized,
             this function will attempt to load it automatically.

   :param file: A UTF8-encoded bytestring containing the path to the font
     file to load.
   :type file: bytes

   :returns: A pointer to the new surface containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_Load_RW(src, freesrc)

   Loads an image file from an SDL2 file object to a new surface. This can
   load all supported formats, *except* TGA. See :func:`IMG_Load` for more
   information.

   :param src: The file object to load an image from.
   :type src: POINTER(:obj:`SDL_RWops`)
   :param freesrc: If non-zero, the input file object will be closed and freed
     after it has been read.
   :type freesrc: int

   :returns: A pointer to the new surface containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadTyped_RW(src, freesrc, type)

   Loads an image file from an SDL2 file object to a new surface, explicitly
   specifying the format type of the image to load. Here are the different
   possible valid format type strings:

   =============  ===========================
   Format String  Format Type
   =============  ===========================
   b"TGA"         TrueVision Targa
   b"CUR"         Windows Cursor
   b"ICO"         Windows Icon
   b"BMP"         Windows Bitmap
   b"GIF"         Graphics Interchange Format
   b"JPG"         JPEG
   b"LBM"         Interleaved Bitmap
   b"PCX"         IBM PC Paintbrush
   b"PNG"         Portable Network Graphics
   b"PNM"         Portable Anymap
   b"SVG"         Scalable Vector Graphics
   b"TIF"         Tagged Image File Format
   b"XCF"         GIMP native format
   b"XPM"         X11 Pixmap
   b"XV"          XV Thumbnail
   b"WEBP"        WebP
   =============  ===========================

   See :func:`IMG_Load` for more information.

   :param src: The file object to load an image from.
   :type src: POINTER(:obj:`SDL_RWops`)
   :param freesrc: If non-zero, the input file object will be closed and freed
     after it has been read.
   :type freesrc: int
   :param type: A bytestring indicating which format to attempt to interpret
     the image as.
   :type type: bytes

   :returns: A pointer to the new surface containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadTexture(renderer, file)

   Loads an image file to a new texture using a given renderer. This can
   load all supported image files, including TGA as long as the filename
   ends with ".tga".

   It is best to call this outside of event loops and keep the loaded
   images around until you are really done with them, as disk speed and
   image conversion to a texture can be slow.

   Once you are done with a loaded image, you can call
   :func:`SDL_DestroyTexture` on the returned texture pointer to free up the
   memory associated with it.

   .. note::
      If the image loader for the format of the given image requires
      initialization (e.g. PNG) and it is not already initialized, this
      function will attempt to load it automatically.

   :param renderer: A pointer to the SDL rendering context to create the
     texture with.
   :type renderer: POINTER(:obj:`SDL_Renderer`)
   :param file: A UTF8-encoded bytestring containing the path to the font
     file to load.
   :type file: bytes)

   :returns: A pointer to the new texture containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Texture`)


.. function:: IMG_LoadTexture_RW(renderer, src, freesrc)

   Loads an image file from an SDL2 file object to a new texture using a
   given renderer. This can load all supported formats, *except* TGA. See
   :func:`IMG_LoadTexture` for more information.

   :param renderer: A pointer to the SDL rendering context to create the
     texture with.
   :type renderer: POINTER(:obj:`SDL_Renderer`)
   :param src: The file object to load an image from.
   :type src: POINTER(:obj:`SDL_RWops`)
   :param freesrc: If non-zero, the input file object will be closed and freed
     after it has been read.
   :type freesrc: int

   :returns: A pointer to the new texture containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Texture`)


.. function:: IMG_LoadTextureTyped_RW(renderer, src, freesrc, type)

   Loads an image file from an SDL2 file object to a new texture, explicitly
   specifying the format type of the image to load. The different possible
   format type strings are listed in the documentation for
   :func:`IMG_LoadTyped_RW`.

   See :func:`IMG_LoadTexture` for more information.

   :param renderer: A pointer to the SDL rendering context to create the
     texture with.
   :type renderer: POINTER(:obj:`SDL_Renderer`)
   :param src: The file object to load an image from.
   :type src: POINTER(:obj:`SDL_RWops`)
   :param freesrc: If non-zero, the input file object will be closed and freed
     after it has been read.
   :type freesrc: int
   :param type: A bytestring indicating which format to attempt to interpret
     the image as.
   :type type: bytes

   :returns: A pointer to the new texture containing the image, or a null
     pointer if there was an error.
   :rtype: POINTER(:obj:`SDL_Texture`)


Format-specific image loading functions
---------------------------------------

.. function:: IMG_LoadICO_RW(src)

   Loads an ICO (Windows icon) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the ICO from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadCUR_RW(src)

   Loads a CUR (Windows cursor) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the CUR from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadBMP_RW(src)

   Loads a BMP (Windows bitmap) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the BMP from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadGIF_RW(src)

   Loads a GIF (Graphics Interchange Format) image from an SDL :obj:`SDL_RWops`
   file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the GIF from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadJPG_RW(src)

   Loads a JPEG image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the JPEG from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadLBM_RW(src)

   Loads an LBM (Interleaved Bitmap) image from an SDL :obj:`SDL_RWops` file
   object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the LBM from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadPCX_RW(src)

   Loads a PCX (IBM PC Paintbrush) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the PCX from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadPNG_RW(src)

   Loads a PNG (Portable Network Graphics) image from an SDL :obj:`SDL_RWops`
   file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the PNG from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadPNM_RW(src)

   Loads a PNM (Portable Anymap) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the PNM from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadSVG_RW(src)

   Loads an SVG (Scalable Vector Graphics) image from an SDL :obj:`SDL_RWops`
   file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the SVG from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadTGA_RW(src)

   Loads a TGA (TrueVision Targa) image from an SDL :obj:`SDL_RWops` file
   object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the TGA from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadTIF_RW(src)

   Loads a TIFF (Tagged Image File Format) image from an SDL :obj:`SDL_RWops`
   file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the TIFF from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadXCF_RW(src)

   Loads an XCF (native GIMP format) image from an SDL :obj:`SDL_RWops` file
   object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the XCF from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadXPM_RW(src)

   Loads an XPM (X11 Pixmap) image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the XPM from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadXV_RW(src)

   Loads an XV thumbnail image (XV Visual Schnauzer format) from an SDL
   :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the XV thumbnail from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_LoadWEBP_RW(src)

   Loads a WebP image from an SDL :obj:`SDL_RWops` file object.

   Use the :func:`IMG_GetError` function to check for any errors.

   :param src: The file object to load the WebP from.
   :type src: POINTER(:obj:`SDL_RWops`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


.. function:: IMG_ReadXPMFromArray(xpm)
   
   Loads an X11 Pixmap from an array to a new surface. The XPM format consists
   of a C header with an array of strings defining the dimensions, colors, and
   pixels of a pixel art image: this is the data format that this function
   expects to be passed.

   .. note::
      Due to the unique input format for this function, it is not obvious how
      to pass data to it using Python. If you figure out a working example,
      please let us know and we'll include it here!

   :param xpm:
   :type xpm: POINTER(:obj:`ctypes.c_char_p`)

   :returns: A pointer to a new surface containing the image, or ``None``
     if there was an error.
   :rtype: POINTER(:obj:`SDL_Surface`)


Image writing functions
-----------------------

.. function:: IMG_SavePNG(surface, file)

   Saves an :obj:`SDL_Surface` object to a PNG file.

   .. note:: This should work regardless of whether PNG support was
             successfully initialized with :func:`IMG_Init`, but the full set
             of PNG features may not be available.

   :param surface: A pointer to the surface containing the image to be saved.
   :type surface: POINTER(:obj:`SDL_Surface`)
   :param file: A UTF-8 encoded bytestring containing the path to save the
     PNG to.
   :type file: bytes

   :returns: 0 on success or a negative error code on failure, can call
     :func:`IMG_GetError` for more information.
   :rtype: int


.. function:: IMG_SavePNG_RW(surface, dst, freedst)

   Saves an :obj:`SDL_Surface` object to an SDL :obj:`SDL_RWops` file object
   containing a PNG file.

   See :func:`IMG_SavePNG` for more information.

   :param surface: A pointer to the surface containing the image to be saved.
   :type surface: POINTER(:obj:`SDL_Surface`)
   :param dst: A pointer to the file object to save the PNG to.
   :type dst: POINTER(:obj:`SDL_RWops`)
   :param freedst: If non-zero, the destination file object will be closed once
     the PNG has been written.
   :type freedst: int

   :returns: 0 on success or a negative error code on failure, can call
     :func:`IMG_GetError` for more information.
   :rtype: int


.. function:: IMG_SaveJPG(surface, file, quality)

   Saves an :obj:`SDL_Surface` object to a JPEG file at a given quality.

   JPEG support must be already initialized using :func:`IMG_Init` before this
   function can be used, otherwise this function will fail without an explicit
   error that can be retrieved with :func:`IMG_GetError`.

   :param surface: A pointer to the surface containing the image to be saved.
   :type surface: POINTER(:obj:`SDL_Surface`)
   :param file: A UTF-8 encoded bytestring containing the path to save the
     JPEG to.
   :type: bytes
   :param quality: The quality at which to compress the JPEG, from 0 to 100
     inclusive.
   :type quality: int

   :returns: 0 on success or a negative error code on failure, can call
     :func:`IMG_GetError` for more information.
   :rtype: int


.. function:: IMG_SaveJPG_RW(surface, dst, freedst, quality)

   Saves an :obj:`SDL_Surface` object to an SDL :obj:`SDL_RWops` file object
   containing a JPEG file at a given quality.

   See :func:`IMG_SaveJPG` for more information.

   :param surface: A pointer to the surface containing the image to be saved.
   :type surface: POINTER(:obj:`SDL_Surface`)
   :param dst: A pointer to the file object to save the JPEG to.
   :type dst: POINTER(:obj:`SDL_RWops`)
   :param freedst: If non-zero, the destination file object will be closed once
     the JPEG has been written.
   :type: int
   :param quality: The quality at which to compress the JPEG, from 0 to 100
     inclusive.
   :type quality: int

   :returns: 0 on success or a negative error code on failure, can call
     :func:`IMG_GetError` for more information.
   :rtype: int


Module constants
----------------

.. data:: IMG_MAJOR_VERSION

    Latest SDL2_image library major number supported by PySDL2.

.. data:: IMG_MINOR_VERSION

    Latest SDL2_image library minor number supported by PySDL2.

.. data:: IMG_PATCHLEVEL

    Latest SDL2_image library patch level number supported by PySDL2.

.. data:: IMG_INIT_JPG

    :func:`IMG_Init` flag to enable support for the JPEG image format.

.. data:: IMG_INIT_PNG

    :func:`IMG_Init` flag to enable support for the PNG image format.

.. data:: IMG_INIT_TIF

    :func:`IMG_Init` flag to enable support for the TIFF image format.

.. data:: IMG_INIT_WEBP

    :func:`IMG_Init` flag to enable support for the WEBP image format.
