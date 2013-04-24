"""Simple example for using sdl2 directly."""
import os
import sys
import ctypes

from sdl2 import *

def run():
    SDL_Init(SDL_INIT_VIDEO)
    window = SDL_CreateWindow(b"Hello World",
                              SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
                              592, 460, SDL_WINDOW_SHOWN)
    fname = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "resources", "hello.bmp")
    image = SDL_LoadBMP(fname.encode("utf-8"))
    windowsurface = SDL_GetWindowSurface(window)
    SDL_BlitSurface(image, None, windowsurface, None)
    SDL_UpdateWindowSurface(window)
    SDL_FreeSurface(image)

    running = True
    event = SDL_Event()
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False
                break

    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
