"""User interface examples."""
import sys
from sdl2.events import SDL_TEXTINPUT

# Try to import SDL2. The import might fail, if the SDL2 DLL could not be
# loaded. In that case, just print the error and exit with a proper
# error code.
try:
    from sdl2 import SDL_QUIT
    import sdl2.ext as sdl2ext
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)


# Define some global color constants
WHITE = sdl2ext.Color(255, 255, 255)
GREY = sdl2ext.Color(200, 200, 200)

# Create a resource, so we have easy access to the example images.
RESOURCES = sdl2ext.Resources(__file__, "resources")


# A callback for the Button.motion event.
def onmotion(button, event):
    print("Mouse moves over the button!")


# A callback for the Button.click event.
def onclick(button, event):
    print("Button was clicked!")


# A callback for the TextEntry.input event.
def oninput(entry, event):
    print("Input received with text '%s'" % event.text.text)
    print("Text on the entry now is '%s'" % entry.text)


# A callback for the TextEntry.edit event.
def onedit(entry, event):
    print("Edit received with text '%s', start '%d', length '%d'" %
          (event.text.text, event.text.start, event.text.length))


def run():
    # You know those from the helloworld.py example.
    # Initialize the video subsystem, create a window and make it visible.
    sdl2ext.init()
    window = sdl2ext.Window("UI Elements", size=(800, 600))
    window.show()

    spritefactory = sdl2ext.SpriteFactory(sdl2ext.SOFTWARE)
    # If you want hardware-accelerated rendering, use video.TEXTURE instead
    # and pass a renderer along:
    #
    # renderer = video.RenderContext(window)
    # factory = video.SpriteFactory(video.TEXTURE, renderer=renderer)
    #

    # Create a UI factory, which will handle several defaults for
    # us. Also, the UIFactory can utilises software-based UI elements as
    # well as hardware-accelerated ones; this allows us to keep the UI
    # creation code clean.
    uifactory = sdl2ext.UIFactory(spritefactory)

    # Create a simple Button sprite, which reacts on mouse movements and
    # button presses and fill it with a white color. All UI elements
    # inherit directly from the TextureSprite (for TEXTURE) or SoftwareSprite
    # (for SOFTWARE), so everything you can do with those classes is also
    # possible for the UI elements.
    button = uifactory.from_image \
        (sdl2ext.BUTTON, RESOURCES.get_path("button.bmp"))
    button.position = 50, 50

    # Create a TextEntry sprite, which reacts on keyboard presses and
    # text input.
    entry = uifactory.from_image \
        (sdl2ext.TEXTENTRY, RESOURCES.get_path("textentry.bmp"))
    entry.position = 50, 200

    # Create a CheckButton sprite. The CheckButton is a specialised
    # Button, which can switch its state, identified by the 'checked'
    # attribute by clicking.
    checkbutton = uifactory.from_image \
        (sdl2ext.CHECKBUTTON, RESOURCES.get_path("button.bmp"))
    checkbutton.position = 200, 50

    # Bind some actions to the button's event handlers. Whenever a click
    # (combination of a mouse button press and mouse button release), the
    # onclick() function will be called.
    # Whenever the mouse moves around in the area occupied by the button, the
    # onmotion() function will be called.
    # The event handlers receive the issuer of the event as first argument
    # (the button is the issuer of that event) and the SDL event data as second
    # argument for further processing, if necessary.
    button.click += onclick
    button.motion += onmotion

    # Bind some actions to the entry's event handlers. The TextEntry
    # receives input events, once it has been activated by a mouse
    # button press on its designated area. The UIProcessor class takes
    # care of this internally through its activate() method.  If the
    # TextEntry is activated, SDL_TEXTINPUT events are enabled by the
    # relevant SDL2 functions, causing input events to occur, that are
    # handled by the TextEntry.
    entry.input += oninput
    entry.editing += onedit

    # Since all gui elements are sprites, we can use the
    # SpriteRenderer class, we learned about in helloworld.py, to
    # draw them on the Window.
    spriterenderer = spritefactory.create_sprite_renderer(window)

    # Create a new UIProcessor, which will handle the user input events
    # and pass them on to the relevant user interface elements.
    uiprocessor = sdl2ext.UIProcessor()

    running = True
    while running:
        events = sdl2ext.get_events()
        for event in events:
            if event.type == SDL_QUIT:
                running = False
                break
            # Pass the SDL2 events to the UIProcessor, which takes care of
            # the user interface logic.
            uiprocessor.dispatch([button, checkbutton, entry], event)

        # Render all user interface elements on the window.
        spriterenderer.render((button, entry, checkbutton))

    sdl2ext.quit()
    return 0


if __name__ == "__main__":
    sys.exit(run())
