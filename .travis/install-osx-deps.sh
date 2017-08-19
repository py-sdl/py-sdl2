#!/bin/sh
set -e

brew update

if [[ "$PYVER" == "3" ]]; then
    brew install python3
else
    brew install python
fi

brew install sdl2

brew install jpeg || brew upgrade jpeg
brew install libpng || brew upgrade libpng
brew install libtiff || brew upgrade libtiff
brew install webp || brew upgrade webp
brew install sdl2_image

brew install freetype || brew upgrade freetype
brew install sdl2_ttf

brew install flac || brew upgrade flac
brew install libmikmod || brew upgrade libmikmod
brew install libvorbis || brew upgrade libvorbis
brew install sdl2_mixer

brew install sdl2_gfx
