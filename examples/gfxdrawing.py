"""2D drawing examples utilising the SDL2_gfx functions."""
import sys
import ctypes
from random import randint

# Try to import SDL2 and SDL2_gfx. The import might fail, if either of the
# libraries could not be loaded. In that case, just print the error and exit
# with a proper error code.
try:
    from sdl2 import SDL_QUIT, SDL_MOUSEBUTTONDOWN, Sint16
    import sdl2.sdlgfx as sdlgfx
    import sdl2.ext as sdl2ext
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)


# Draws random lines using the passed rendering context
def draw_lines(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    whalf = width // 2 - 2
    hhalf = height // 2 - 2
    lw = 5
    x0, x1 = whalf, whalf
    y0, y1 = 0, height
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    x0, x1 = 0, width
    y0, y1 = hhalf, hhalf
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first quadrant, draw normal lines
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(0, whalf), randint(0, whalf)
        y0, y1 = randint(0, hhalf), randint(0, hhalf)
        sdlgfx.lineColor(context.renderer, x0, y0, x1, y1, color)
        # In the second quadrant, draw aa lines
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(whalf + lw, width), randint(whalf + lw, width)
        y0, y1 = randint(0, hhalf), randint(0, hhalf)
        sdlgfx.aalineColor(context.renderer, x0, y0, x1, y1, color)
        # In the third quadrant, draw horizontal lines
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(0, whalf), randint(0, whalf)
        y0 = randint(hhalf + lw, height)
        sdlgfx.hlineColor(context.renderer, x0, x1, y0, color)
        # In the fourth quadrant, draw vertical lines
        color = randint(0, 0xFFFFFFFF)
        x0 = randint(whalf + lw, width)
        y0, y1 = randint(hhalf + lw, height), randint(hhalf + lw, height)
        sdlgfx.vlineColor(context.renderer, x0, y0, y1, color)


# Draws random circles using the passed rendering context
def draw_circles(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    wthird = width // 3 - 1
    lw = 3
    sdlgfx.thickLineColor(context.renderer, wthird, 0, wthird, height, lw,
                          0xFFFFFFFF)
    sdlgfx.thickLineColor(context.renderer, (2 * wthird + lw), 0,
                          (2 * wthird + lw), height, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first part, draw circles
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        r = randint(1, max(min(x, wthird - x), 2))
        sdlgfx.circleColor(context.renderer, x, y, r, color)
        # In the second part, draw aa circles
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        r = randint(1, max(min(x, wthird - x), 2))
        sdlgfx.aacircleColor(context.renderer, x + wthird + lw, y, r, color)
        # In the third part, draw filled circles
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        r = randint(1, max(min(x, wthird - x), 2))
        sdlgfx.filledCircleColor(context.renderer, x + 2 * (wthird + lw), y, r,
                                 color)


# Draws random ellipsis using the passed rendering context
def draw_ellipsis(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    wthird = width // 3 - 1
    eheight = height // 4
    lw = 3
    sdlgfx.thickLineColor(context.renderer, wthird, 0, wthird, height, lw,
                          0xFFFFFFFF)
    sdlgfx.thickLineColor(context.renderer, (2 * wthird + lw), 0,
                          (2 * wthird + lw), height, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first part, draw ellipsis
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        rx, ry = randint(1, max(min(x, wthird - x), 2)), randint(0, eheight)
        sdlgfx.ellipseColor(context.renderer, x, y, rx, ry, color)
        # In the second part, draw aa ellipsis
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        rx, ry = randint(1, max(min(x, wthird - x), 2)), randint(0, eheight)
        sdlgfx.aaellipseColor(context.renderer, x + wthird + lw, y, rx, ry,
                              color)
        # In the third part, draw filled ellipsis
        color = randint(0, 0xFFFFFFFF)
        x, y = randint(0, wthird), randint(0, height)
        rx, ry = randint(1, max(min(x, wthird - x), 2)), randint(0, eheight)
        sdlgfx.filledEllipseColor(context.renderer, x + 2 * (wthird + lw), y,
                                  rx, ry, color)


# Draws random rectangles using the passed rendering context
def draw_rects(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    whalf = width // 2 - 2
    hhalf = height // 2 - 2
    lw = 5
    x0, x1 = whalf, whalf
    y0, y1 = 0, height
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    x0, x1 = 0, width
    y0, y1 = hhalf, hhalf
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first quadrant, draw normal rectangles
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(0, whalf), randint(0, whalf)
        y0, y1 = randint(0, hhalf), randint(0, hhalf)
        sdlgfx.rectangleColor(context.renderer, x0, y0, x1, y1, color)
        # In the second quadrant, draw rounded rectangles
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(whalf + lw, width), randint(whalf + lw, width)
        y0, y1 = randint(0, hhalf), randint(0, hhalf)
        r = randint(0, max(x1 - x0, x0 - x1))
        sdlgfx.roundedRectangleColor(context.renderer, x0, y0, x1, y1, r,
                                     color)
        # In the third quadrant, draw horizontal lines
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(0, whalf), randint(0, whalf)
        y0, y1 = randint(hhalf + lw, height), randint(hhalf + lw, height)
        sdlgfx.boxColor(context.renderer, x0, y0, x1, y1, color)
        # In the fourth quadrant, draw vertical lines
        color = randint(0, 0xFFFFFFFF)
        x0, x1 = randint(whalf + lw, width), randint(whalf + lw, width)
        y0, y1 = randint(hhalf + lw, height), randint(hhalf + lw, height)
        r = randint(1, max(x1 - x0, x0 - x1))
        sdlgfx.roundedBoxColor(context.renderer, x0, y0, x1, y1, r, color)


# Draws random triangles using the passed rendering context
def draw_trigons(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    wthird = width // 3 - 1
    lw = 3
    sdlgfx.thickLineColor(context.renderer, wthird, 0, wthird, height, lw,
                          0xFFFFFFFF)
    sdlgfx.thickLineColor(context.renderer, (2 * wthird + lw), 0,
                          (2 * wthird + lw), height, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first part, draw triangles
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(0, wthird), randint(0, height)
        x1, y1 = randint(0, wthird), randint(0, height)
        x2, y2 = randint(0, wthird), randint(0, height)
        sdlgfx.trigonColor(context.renderer, x0, y0, x1, y1, x2, y2, color)
        # In the second part, draw aa triangles
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(0, wthird) + wthird + lw, randint(0, height)
        x1, y1 = randint(0, wthird) + wthird + lw, randint(0, height)
        x2, y2 = randint(0, wthird) + wthird + lw, randint(0, height)
        sdlgfx.aatrigonColor(context.renderer, x0, y0, x1, y1, x2, y2, color)
        # In the third part, draw filled triangles
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(0, wthird) + 2 * (wthird + lw), randint(0, height)
        x1, y1 = randint(0, wthird) + 2 * (wthird + lw), randint(0, height)
        x2, y2 = randint(0, wthird) + 2 * (wthird + lw), randint(0, height)
        sdlgfx.filledTrigonColor(context.renderer, x0, y0, x1, y1, x2, y2,
                                 color)


# Draws random polygons using the passed rendering context
def draw_polygons(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    wthird = width // 3 - 1
    lw = 3
    sdlgfx.thickLineColor(context.renderer, wthird, 0, wthird, height, lw,
                          0xFFFFFFFF)
    sdlgfx.thickLineColor(context.renderer, (2 * wthird + lw), 0,
                          (2 * wthird + lw), height, lw, 0xFFFFFFFF)
    for x in range(5):
        # In the first part, draw polygons
        color = randint(0, 0xFFFFFFFF)
        ptcount = randint(3, 10)
        xlist, ylist = (Sint16 * ptcount)(), (Sint16 * ptcount)()
        for k in range(ptcount):
            xlist[k] = randint(0, wthird)
            ylist[k] = randint(0, height)
        xptr = ctypes.cast(xlist, ctypes.POINTER(Sint16))
        yptr = ctypes.cast(ylist, ctypes.POINTER(Sint16))
        sdlgfx.polygonColor(context.renderer, xptr, yptr, ptcount, color)
        # In the second part, draw aa polygons
        color = randint(0, 0xFFFFFFFF)
        ptcount = randint(3, 10)
        xlist, ylist = (Sint16 * ptcount)(), (Sint16 * ptcount)()
        for k in range(ptcount):
            xlist[k] = randint(0, wthird) + wthird + lw
            ylist[k] = randint(0, height)
        xptr = ctypes.cast(xlist, ctypes.POINTER(Sint16))
        yptr = ctypes.cast(ylist, ctypes.POINTER(Sint16))
        sdlgfx.aapolygonColor(context.renderer, xptr, yptr, ptcount, color)
        # In the third part, draw filled polygons
        color = randint(0, 0xFFFFFFFF)
        ptcount = randint(3, 10)
        xlist, ylist = (Sint16 * ptcount)(), (Sint16 * ptcount)()
        for k in range(ptcount):
            xlist[k] = randint(0, wthird) + 2 * (wthird + lw)
            ylist[k] = randint(0, height)
        xptr = ctypes.cast(xlist, ctypes.POINTER(Sint16))
        yptr = ctypes.cast(ylist, ctypes.POINTER(Sint16))
        sdlgfx.filledPolygonColor(context.renderer, xptr, yptr, ptcount, color)


# Draw random elements using the passed rendering context
def draw_mixed(context, width, height):
    # Reset the visible area with a black color.
    context.clear(0)
    # Split the visible area
    whalf = width // 2 - 2
    hhalf = height // 2 - 2
    lw = 5
    x0, x1 = whalf, whalf
    y0, y1 = 0, height
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    x0, x1 = 0, width
    y0, y1 = hhalf, hhalf
    sdlgfx.thickLineColor(context.renderer, x0, y0, x1, y1, lw, 0xFFFFFFFF)
    for x in range(15):
        # In the first quadrant, draw arcs
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(0, whalf), randint(0, hhalf)
        rad = randint(0, min(whalf - x0, hhalf - y0))
        start, end = randint(0, 360), randint(0, 360)
        sdlgfx.arcColor(context.renderer, x0, y0, rad, start, end, color)
        # In the second quadrant, draw bezier curves
        color = randint(0, 0xFFFFFFFF)
        ptcount = randint(3, 10)
        xlist, ylist = (Sint16 * ptcount)(), (Sint16 * ptcount)()
        for k in range(ptcount):
            xlist[k] = randint(whalf, width)
            ylist[k] = randint(0, hhalf)
        steps = randint(2, 10)
        xptr = ctypes.cast(xlist, ctypes.POINTER(Sint16))
        yptr = ctypes.cast(ylist, ctypes.POINTER(Sint16))
        sdlgfx.bezierColor(context.renderer, xptr, yptr, ptcount, steps, color)
        # In the third quadrant, draw pies
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(0, whalf), randint(hhalf + lw, height)
        rad = randint(0, min(whalf - x0, y0 - (hhalf + lw)))
        start, end = randint(0, 360), randint(0, 360)
        sdlgfx.pieColor(context.renderer, x0, y0, rad, start, end, color)
        # In the fourth quadrant, draw filled pies
        color = randint(0, 0xFFFFFFFF)
        x0, y0 = randint(whalf + lw, width), randint(hhalf + lw, height)
        rad = randint(0, min(x0 - (whalf + lw), y0 - (hhalf + lw)))
        start, end = randint(0, 360), randint(0, 360)
        sdlgfx.filledPieColor(context.renderer, x0, y0, rad, start, end, color)


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2ext.init()
    window = sdl2ext.Window("sdlgfx drawing examples", size=(800, 600))
    window.show()

    # Create a rendering context for the window. The sdlgfx module requires it.
    context = sdl2ext.RenderContext(window)

    # We implement the functionality as it was done in colorpalettes.py and
    # utilise a mapping table to look up the function to be executed, together
    # with the arguments they should receive
    functions = ((draw_lines, (context, 800, 600)),
                 (draw_circles, (context, 800, 600)),
                 (draw_ellipsis, (context, 800, 600)),
                 (draw_rects, (context, 800, 600)),
                 (draw_trigons, (context, 800, 600)),
                 (draw_polygons, (context, 800, 600)),
                 (draw_mixed, (context, 800, 600))
                 )

    # A storage variable for the function we are currently on, so that we know
    # which function to execute next.
    curindex = 0
    draw_lines(context, 800, 600)

    # The event loop is nearly the same as we used in colorpalettes.py. If you
    # do not know, what happens here, take a look at colorpalettes.py for a
    # detailed description.
    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            if event.type == SDL_MOUSEBUTTONDOWN:
                curindex += 1
                if curindex >= len(functions):
                    curindex = 0
                # In contrast to colorpalettes.py, our mapping table consists
                # of functions and their arguments. Thus, we get the currently
                # requested function and argument tuple and execute the
                # function with the arguments.
                func, args = functions[curindex]
                func(*args)
                break
        context.present()
    sdl2ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
