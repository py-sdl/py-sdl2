"""OpenGL rendering simulation"""
import sys
import random

try:
    import mule.video as video
    import mule.sdl.events as sdlevents
    import mule.sdl.timer as sdltimer
    import mule.sdl.render as sdlrender
    import mule.sdl.video as sdlvideo
    import mule.sdl.rect as sdlrect
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Import the resources, so we have easy access to the example images.
from sdl2.ext import Resources
RESOURCES = Resources(__file__, "resources")

def run():
    # Initialize the video subsystem, create a window and make it visible.
    video.init()
    window = video.Window("Particles", size=(800, 600),
                          flags=sdlvideo.SDL_WINDOW_OPENGL)
    window.show()

    renderer = video.RenderContext(window)

    # The almighty event loop. You already know several parts of it.
    running = True
    while running:
        for event in video.get_events():
            if event.type == sdlevents.SDL_QUIT:
                running = False
                break

    video.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
