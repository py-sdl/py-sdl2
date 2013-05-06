"""OpenGL rendering simulation"""
import sys
import ctypes

try:
    from OpenGL import GL, GLU
    from sdl2 import *
except ImportError:
    import traceback
    traceback.print_exc()
    sys.exit(1)


def run():
    if SDL_Init(SDL_INIT_VIDEO) != 0:
        print SDL_GetError()
        return -1

    window = SDL_CreateWindow(b"OpenGL demo", SDL_WINDOWPOS_UNDEFINED,
                              SDL_WINDOWPOS_UNDEFINED, 800, 600,
                              SDL_WINDOW_OPENGL)
    if not window:
        print(SDL_GetError())
        return -1

    context = SDL_GL_CreateContext(window)

    GL.glMatrixMode(GL.GL_PROJECTION | GL.GL_MODELVIEW)
    GL.glLoadIdentity()
    GL.glOrtho(-400, 400, 300, -300, 0, 1)

    x = 0.0
    y = 30.0

    event = SDL_Event()
    running = True
    while running:
        while SDL_PollEvent(ctypes.byref(event)) != 0:
            if event.type == SDL_QUIT:
                running = False

        GL.glClearColor(0, 0, 0, 1)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        GL.glRotatef(10.0, 0.0, 0.0, 1.0)
        GL.glBegin(GL.GL_TRIANGLES)
        GL.glColor3f(1.0, 0.0, 0.0)
        GL.glVertex2f(x, y + 90.0)
        GL.glColor3f(0.0, 1.0, 0.0)
        GL.glVertex2f(x + 90.0, y - 90.0)
        GL.glColor3f(0.0, 0.0, 1.0)
        GL.glVertex2f(x - 90.0, y - 90.0)
        GL.glEnd()

        SDL_GL_SwapWindow(window)
        SDL_Delay(10)
    SDL_GL_DeleteContext(context)
    SDL_DestroyWindow(window)
    SDL_Quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
