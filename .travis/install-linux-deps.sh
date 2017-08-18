#!/bin/sh
set -e

SDL_LIB=SDL2-2.0.5
SDLTTF_LIB=SDL2_ttf-2.0.14
SDLMIXER_LIB=SDL2_mixer-2.0.1
SDLGFX_LIB=SDL2_gfx-1.0.3

sudo apt-get install build-essential mercurial make cmake autoconf automake \
    libtool libasound2-dev libpulse-dev libaudio-dev libx11-dev libxext-dev \
    libxrandr-dev libxcursor-dev libxi-dev libxinerama-dev libxxf86vm-dev \
    libxss-dev libgl1-mesa-dev libesd0-dev libdbus-1-dev libudev-dev \
    libgles1-mesa-dev libgles2-mesa-dev libegl1-mesa-dev libibus-1.0-dev \
    fcitx-libs-dev libsamplerate0-dev libsndio-dev \
    libfreetype6-dev \
    libflac-dev libfluidsynth-dev libmikmod2-dev libogg-dev libvorbis-dev

wget https://www.libsdl.org/release/$(SDL_LIB).tar.gz
tar xzvf $(SDL_LIB).tar.gz
cd $(SDL_LIB) \
./configure
make
sudo make install
cd ..

wget https://www.libsdl.org/projects/SDL_mixer/release/$(SDLMIXER_LIB).tar.gz
tar xzvf $(SDLMIXER_LIB).tar.gz
cd $(SDLMIXER_LIB)
./configure
make
sudo make install
cd ..

wget https://www.libsdl.org/projects/SDL_ttf/release/$(SDLTTF_LIB).tar.gz
tar xzvf $(SDLTTF_LIB).tar.gz
cd $(SDLTTF_LIB)
./configure
make
sudo make install
cd ..

wget http://www.ferzkopp.net/Software/SDL2_gfx/$(SDLGFX_LIB).tar.gz
tar xzvf $(SDLGFX_LIB).tar.gz
cd $(SDLGFX_LIB)
./configure
make
sudo make install
cd ..
