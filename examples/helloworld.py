"""The almighty Hello World! example"""
# We'll use sys to properly exit with an error code.
import sys
import sdl2.ext

# Create a resource container, so that we can easily access all
# resource, we bundle with our application. We are using the current
# file's location and define the "resources" subdirectory as the
# location, in which we keep all data.
RESOURCES = sdl2.ext.Resources(__file__, "resources")


def run():
    # Initialize the video system - this implicitly initializes some
    # necessary parts within the SDL2 DLL used by the video module.
    #
    # You SHOULD call this before using any video related methods or
    # classes.
    sdl2.ext.init()

    # Create a new window (like your browser window or editor window,
    # etc.) and give it a meaningful title and size. We definitely need
    # this, if we want to present something to the user.
    window = sdl2.ext.Window("Hello World!", size=(592, 460))

    # By default, every Window is hidden, not shown on the screen right
    # after creation. Thus we need to tell it to be shown now.
    window.show()

    # Create a sprite factory that allows us to create visible 2D elements
    # easily. Depending on what the user chosses, we either create a factory
    # that supports hardware-accelerated sprites or software-based ones.
    # The hardware-accelerated SpriteFactory requres a rendering context
    # (or SDL_Renderer), which will create the underlying textures for us.
    if "-hardware" in sys.argv:
        print("Using hardware acceleration")
        renderer = sdl2.ext.Renderer(window)
        factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    else:
        print("Using software rendering")
        factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)

    # Creates a simple rendering system for the Window. The
    # SpriteRenderSystem can draw Sprite objects on the window.
    spriterenderer = factory.create_sprite_render_system(window)

    # Creates a new 2D pixel-based surface to be displayed, processed or
    # manipulated. We will use the one of the shipped example images
    # from the resource package to display.
    sprite = factory.from_image(RESOURCES.get_path("hello.bmp"))

    # Display the surface on the window. This will copy the contents
    # (pixels) of the surface to the window. The surface will be
    # displayed at surface.position on the window. Play around with the
    # surface.x and surface.y values or surface.position (which is just
    # surface.x and surface.y grouped as tuple)!
    spriterenderer.render(sprite)

    # Set up an example event loop processing system. This is a necessity,
    # so the application can exit correctly, mouse movements, etc. are
    # recognised and so on. The TestEventProcessor class is just for
    # testing purposes and does not do anything meaningful.  Take a look
    # at its code to better understand how the event processing can be
    # done and customized!
    processor = sdl2.ext.TestEventProcessor()

    # Start the event processing. This will run in an endless loop, so
    # everything following after processor.run() will not be executed
    # before some quitting event is raised.
    processor.run(window)

    # We called video.init(), so we have to call video.quit() as well to
    # release the resources hold by the SDL DLL.
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
