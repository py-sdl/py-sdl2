# Test font rendering using the FontTTF class

# This example allows you to try typing out some text in a given font, and
# supports the following keys:
#   - Left/Right Arrow Keys: Cycles text alignment (left/right/center)
#   - Up/Down Arrow Keys: Increases/decreases line height
#   - Tab: Cycles font rendering style

import os
import sys
import sdl2.ext
from sdl2.sdlttf import TTF_FontLineSkip
from sdl2.ext import FontTTF, key_pressed, get_text_input

filepath = os.path.abspath(os.path.dirname(__file__))
RESOURCES = sdl2.ext.Resources(filepath, "resources")
BLACK_RGBA = (0, 0, 0, 255)
WHITE_RGBA = (255, 255, 255, 255)


def update_text(renderer, surface):
    # Create a texture for the surface and render it to the screen
    tx = sdl2.ext.Texture(renderer, surface)
    renderer.clear(BLACK_RGBA)
    renderer.copy(tx, dstrect=(10, 10))
    renderer.present()


def run():
    # Initialize SDL2 and create a Window and Renderer
    sdl2.ext.init()
    window = sdl2.ext.Window("Font Rendering", size=(800, 500))
    renderflags = sdl2.SDL_RENDERER_SOFTWARE
    if "-hardware" in sys.argv:
        renderflags = (
            sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC
        )
    renderer = sdl2.ext.Renderer(window, flags=renderflags)
    window.show()

    # Create and initialize a font to render text with
    fontpath = RESOURCES.get_path("tuffy.ttf")
    font = FontTTF(fontpath, "20px", WHITE_RGBA)

    # Add some additional font styles
    styles = ['default', 'small', 'red', 'large', 'bg_fill']
    font.add_style('small', '10px', WHITE_RGBA)
    font.add_style('red', '20px', (255, 0, 0))
    font.add_style('large', '35px', WHITE_RGBA)
    font.add_style('bg_fill', '20px', BLACK_RGBA, WHITE_RGBA)

    # Initialize font rendering options
    line_height = TTF_FontLineSkip(font.get_ttf_font())
    alignments = ["left", "center", "right"]
    align_idx = 0
    style_idx = 0

    # Set a default string with which to render text
    txt = u"Hi There!\nYou can edit this text using the keyboard and delete keys."

    # Render the text and present it on the screen
    txt_rendered = font.render_text(txt, width=780)
    update_text(renderer, txt_rendered)

    # Tell SDL2 to start reading Text Editing events. This allows for proper
    # handling of unicode characters and modifier keys.
    sdl2.ext.start_text_input()

    # Create a simple event loop and wait for keydown, text editing, and quit events.
    running = True
    while running:
        update_txt = False
        events = sdl2.ext.get_events()

        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break

        # Handle special keyboard events
        if key_pressed(events):
             # If any key pressed, re-render text
            update_txt = True
            # If backspace pressed, remove last character (if any) from txt
            if key_pressed(events, sdl2.SDLK_BACKSPACE):
                txt = txt[:-1]
            # If enter/return pressed, insert a newline
            elif key_pressed(events, sdl2.SDLK_RETURN):
                txt = txt + u"\n"
            # If left or right arrow pressed, change text alignment mode
            elif key_pressed(events, "left"):
                align_idx = (align_idx - 1) % 3
            elif key_pressed(events, "right"):
                align_idx = (align_idx + 1) % 3
            elif key_pressed(events, "up"):
                line_height += 1
            elif key_pressed(events, "down"):
                if line_height > 1:
                    line_height -= 1 
            # If tab pressed, cycle through the different font styles
            elif key_pressed(events, "tab"):
                style_idx = (style_idx + 1) % len(styles)

        # Handle text input events
        txt += get_text_input(events)

        # If txt has changed since the start of the loop, update the renderer
        if update_txt:
            align = alignments[align_idx]
            style = styles[style_idx]
            txt_rendered = font.render_text(
                txt, style, width=780, line_h=line_height, align=align
            )
            update_text(renderer, txt_rendered)

    # Now that we're done, close everything down and quit SDL2
    font.close()
    renderer.destroy()
    window.close()
    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
