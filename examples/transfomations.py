import sys
import sdl2
import sdl2.ext

# Create a resource container, so that we can easily access all
# resource, we bundle with our application. We are using the current
# file's location and define the "resources" subdirectory as the
# location, in which we keep all data.
RESOURCES = sdl2.ext.Resources(__file__, "resources")

def run():
    # Initialize the video subsystem, create a window and make it visible.
    sdl2.ext.init()
    window = sdl2.ext.Window("Sprite Transformations", size=(800, 600))
    window.show()

    # Create a hardware-accelerated sprite factory. The sprite factory requires
    # a rendering context, which enables it to create the underlying textures
    # that serve as the visual parts for the sprites.
    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)

    # Create a simple rendering system for the window. We will use it to
    # display the sprites.
    rendersystem = factory.create_sprite_render_system(window)

    # Create the sprite to display.
    sprite = factory.from_image(RESOURCES.get_path("hello.bmp"))

    # Use the sprite.center tuple to change the center of the sprite for
    # rotation. You can reset a changed center simply by assinging None to it.
    #
    # sprite.center = 10, 30    # Changes the center
    # sprite.center = None      # Resets the center

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                # Flip the sprite over its vertical axis on pressing down or up
                if event.key.keysym.sym in (sdl2.SDLK_DOWN, sdl2.SDLK_UP):
                    sprite.flip ^= sdl2.SDL_FLIP_VERTICAL
                # Flip the sprite over its horizontal axis on pressing left or
                # right
                elif event.key.keysym.sym in (sdl2.SDLK_LEFT, sdl2.SDLK_RIGHT):
                    sprite.flip ^= sdl2.SDL_FLIP_HORIZONTAL
                # Rotate the sprite around its center on pressing plus or
                # minus. The center can be changed via sprite.center.
                elif event.key.keysym.sym == sdl2.SDLK_PLUS:
                    sprite.angle += 1.0
                    if sprite.angle >= 360.0:
                        sprite.angle = 0.0
                elif event.key.keysym.sym == sdl2.SDLK_MINUS:
                    sprite.angle -= 1.0
                    if sprite.angle <= 0.0:
                        sprite.angle = 360.0
        renderer.clear()
        rendersystem.render(sprite, 100, 75)
        sdl2.SDL_Delay(10)
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
