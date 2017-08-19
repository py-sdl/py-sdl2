#!/bin/sh
set -e

brew update

if [[ "$PYVER" == "3" ]]; then
    brew install python3
else
    brew install python
fi

brew install sdl2

brew install jpeg
brew install libpng
brew install libtiff
brew install webp
brew install sdl2_image

brew install freetype
brew install sdl2_ttf

brew install flac
brew install libmikmod
brew install libvorbis
brew install sdl2_mixer

brew install sdl2_gfx
