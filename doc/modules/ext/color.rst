.. currentmodule:: sdl2.ext

Color handling
==============

.. class:: Color(r=255, g=255, b=255, a=255)

   A simple RGBA-based color implementation. The Color class uses a
   byte-wise representation of the 4 channels red, green, blue and alpha
   transparency, so that the values range from 0 to 255. It allows basic
   arithmetic operations, e.g. color addition or subtraction and
   conversions to other color spaces such as HSV or CMY.

   .. attribute:: r

      The red channel value of the Color.

   .. attribute:: g

      The green channel value of the Color.

   .. attribute:: b

      The blue channel value of the Color.

   .. attribute:: a

      The alpha channel value of the Color.

   .. attribute:: cmy

      The CMY representation of the Color. The CMY components are in the
      ranges C = [0, 1], M = [0, 1], Y = [0, 1]. Note that this will not
      return the absolutely exact CMY values for the set RGB values in
      all cases. Due to the RGB mapping from 0-255 and the CMY mapping
      from 0-1 rounding errors may cause the CMY values to differ
      slightly from what you might expect.

   .. attribute:: hsla

      The HSLA representation of the Color. The HSLA components are in
      the ranges H = [0, 360], S = [0, 100], L = [0, 100], A = [0,
      100]. Note that this will not return the absolutely exact HSL
      values for the set RGB values in all cases. Due to the RGB mapping
      from 0-255 and the HSL mapping from 0-100 and 0-360 rounding
      errors may cause the HSL values to differ slightly from what you
      might expect.

   .. attribute:: hsva

      The HSVA representation of the Color. The HSVA components are in
      the ranges H = [0, 360], S = [0, 100], V = [0, 100], A = [0,
      100]. Note that this will not return the absolutely exact HSV
      values for the set RGB values in all cases. Due to the RGB mapping
      from 0-255 and the HSV mapping from 0-100 and 0-360 rounding
      errors may cause the HSV values to differ slightly from what you
      might expect.

   .. attribute:: i1i2i3

      The I1I2I3 representation of the Color. The I1I2I3 components are
      in the ranges I1 = [0, 1], I2 = [-0.5, 0.5], I3 = [-0.5,
      0.5]. Note that this will not return the absolutely exact I1I2I3
      values for the set RGB values in all cases. Due to the RGB mapping
      from 0-255 and the I1I2I3 from 0-1 rounding errors may cause the
      I1I2I3 values to differ slightly from what you might expect.

   .. method:: normalize() -> (float, float, float, float)

      Returns the normalised RGBA values of the Color as floating point
      values in the range [0, 1].

   .. method:: __add__(self, color) -> Color
               __sub__(self, color) -> Color
               __mul__(self, color) -> Color
               __div__(self, color) -> Color
               __truediv__(self, color) -> Color
               __mod__(self, color) -> Color

      Basic arithmetic functions for :class:`Color` values. The arithmetic
      operations ``+, -, *, /, %`` are supported by the :class:`Color` class
      and work on a per-channel basis. This means, that the operation ::

         color = color1 + color2

      is the same as ::

         color = Color()
         color.r = min(color1.r + color2.r, 255)
         color.g = min(color1.g + color2.g, 255)
         ...

      The operations guarantee that the channel values stay in the allowed
      range of [0, 255].

.. function:: argb_to_color(v : int) -> Color
              ARGB(v : int) -> Color

   Converts an integer value to a Color, assuming the integer represents
   a 32-bit ARGB value.

.. function:: convert_to_color(v : object) -> Color
              COLOR(v : object) -> Color

   Tries to convert the passed value to a Color object. The value can be
   an arbitrary Python object, which is passed to the different other
   conversion functions. If one of them succeeds, the Color will be
   returned to the caller. If none succeeds, a :exc:`ValueError` will be
   raised.

   If the color is an integer value, it is assumed to be in ARGB layout.

.. function:: rgba_to_color(v : int) -> Color
              RGBA(v : int) -> Color

   Converts an integer value to a Color, assuming the integer represents
   a 32-bit RGBA value.

.. function:: is_rgb_color(v : object) -> bool

   Checks, if the passed value is an item that could be converted to a
   RGB color.

.. function:: is_rgba_color(v : object) -> bool

   Checks, if the passed value is an item that could be converted to a
   RGBA color.

.. function:: string_to_color(v : string) -> Color

   Converts a hex color string or color name to a Color value. Supported
   hex values are:

   * #RGB
   * #RGBA
   * #RRGGBB
   * #RRGGBBAA
   * 0xRGB
   * 0xRGBA
   * 0xRRGGBB
   * 0xRRGGBBAA
