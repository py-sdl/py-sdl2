.. currentmodule:: sdl2.ext

Accelerated 2D Rendering
========================

.. class:: Renderer(target : obj[, logical_size=None[, index=-1[, flags=sdl2.SDL_RENDERER_ACCELERATED]])

   A rendering context for windows and sprites that can use hardware or
   software-accelerated graphics drivers.

   If target is a :class:`sdl2.ext.Window` or :class:`sdl2.SDL_Window`,
   *index* and *flags* are passed to the relevant
   :class:`sdl2.SDL_CreateRenderer()` call. If *target* is a
   :class:`SoftwareSprite` or :class:`sdl2.SDL_Surface`, the *index*
   and *flags* arguments are ignored.

   .. attribute:: sdlrenderer

      The underlying :class:`sdl2.SDL_Renderer`.

   .. attribute:: rendertarget

      The target for which the :class:`Renderer` was created.

   .. attribute:: logical_size

      The logical size of the renderer.

      Setting this allows you to draw as if your renderer had this size, even
      though the target may be larger or smaller. When drawing, the renderer will
      automatically scale your contents to the target, creating letter-boxing or
      sidebars if necessary.

      To reset your logical size back to the target's, set it to ``(0, 0)``.

      Setting this to a lower value may be useful for low-resolution effects.

      Setting this to a larger value may be useful for antialiasing.

   .. attribute:: color

      The :class:`sdl2.ext.Color` to use for draw and fill operations.

   .. attribute:: blendmode

      The blend mode used for drawing operations (fill and line). This
      can be a value of

      * ``SDL_BLENDMODE_NONE`` for no blending
      * ``SDL_BLENDMODE_BLEND`` for alpha blending
      * ``SDL_BLENDMODE_ADD`` for additive color blending
      * ``SDL_BLENDMODE_MOD`` for multiplied color blending

   .. attribute:: scale

      The horizontal and vertical drawing scale as two-value tuple.

   .. method:: clear([color=None])

      Clears the rendering context with the currently set or passed
      *color*.

   .. method:: copy(src : obj[, srcrect=None[, dstrect=None[, angle=0[, center=None[, flip=render.SDL_FLIP_NONE]]]]]) -> None

      Copies (blits) the passed *src*, which can be a :class:`TextureSprite` or
      :class:`sdl2.SDL_Texture`, to the target of the
      :class:`Renderer`. *srcrect* is the source rectangle to be used for
      clipping portions of *src*. *dstrect* is the destination rectangle.
      *angle* will cause the texture to be rotated around *center* by the given
      degrees. *flip* can be one of the SDL_FLIP_* constants and will flip the
      texture over its horizontal or vertical middle axis. If *src* is a
      :class:`TextureSprite`, *angle*, *center* and *flip* will be set from
      *src*'s attributes, if not provided.

   .. method:: draw_line(points : iterable[, color=None]) -> None

      Draws one or multiple lines on the rendering context. If *line* consists
      of four values ``(x1, y1, x2, y2)`` only, a single line is drawn. If
      *line* contains more than four values, a series of connected lines is
      drawn.

   .. method:: draw_point(points : iterable[, color=None]) -> None

      Draws one or multiple points on the rendering context. The *points*
      argument contains the x and y values of the points as simple sequence in
      the form ``(point1_x, point1_y, point2_x, point2_y, ...)``.

   .. method:: draw_rect(rects : iterable[, color=None]) -> None

      Draws one or multiple rectangles on the rendering context. *rects*
      contains sequences of four values denoting the x and y offset and width
      and height of each individual rectangle in the form ``((x1, y1, w1, h1),
      (x2, y2, w2, h2), ...)``.

   .. method:: fill(rects : iterable[, color=None]) -> None

      Fills one or multiple rectangular areas on the rendering context with
      the current set or passed *color*. *rects* contains sequences of four
      values denoting the x and y offset and width and height of each
      individual rectangle in the form ``((x1, y1, w1, h1), (x2, y2, w2, h2),
      ...)``.

   .. method:: present() -> None

      Refreshes the rendering context, causing changes to the render buffers
      to be shown.
