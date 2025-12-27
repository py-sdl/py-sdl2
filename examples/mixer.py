"""Example for using the mixer API.

Plays music in the background and plays a coin sound when the user hits the
space bar.
"""

import sdl2
import sdl2.ext
import sdl2.sdlmixer as mix


SAMPLE_RATE = 44100
CHUNK_SIZE = 4096

def run():
    # Setup--initialize the video subsystem and start a window
    sdl2.ext.init()
    window = sdl2.ext.Window("Let's play sound", size=(800, 600))
    window.show()

    # Dynamically load libraries needed by the mixer.
    if mix.Mix_Init(0) == -1:
        print('ERR: Mix_Init')
        exit()

    # Initialize the mixer API. Use 2 channels (stereo).
    if mix.Mix_OpenAudio(SAMPLE_RATE, mix.MIX_DEFAULT_FORMAT, 2, CHUNK_SIZE) == -1:
        print('ERR: Mix_OpenAudio')
        exit()

    # This call won't fail.
    mix.Mix_AllocateChannels(1)

    # Set volume of the channel to max. We only allocated 1 channel, so use 0.
    mix.Mix_Volume(0, mix.MIX_MAX_VOLUME)

    # Load sound assets
    music = mix.Mix_LoadMUS(b'resources/title_screen.wav')
    if not music:
        print('ERR: Failed to load music')
        exit()

    coin_sound = mix.Mix_LoadWAV(b'resources/handleCoins.ogg')
    if not coin_sound:
        print('ERR: Failed to load sound effects')
        exit()

    # Start playing music and loop forever
    if mix.Mix_PlayMusic(music, -1) == -1:
        print('WARN: Mix_PlayMusic')

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_SPACE:
                    # When the user hits SPACE, play the coin sound
                    mix.Mix_PlayChannel(0, coin_sound, 0)

        sdl2.SDL_Delay(10)

    # Clean up
    mix.Mix_HaltMusic(music)
    mix.Mix_FreeMusic(music)
    if mix.Mix_Playing(0):
        mix.Mix_HaltChannel(0)
    mix.Mix_FreeChunk(coin_sound)

    mix.Mix_CloseAudio()

if __name__ == '__main__':
    run()
