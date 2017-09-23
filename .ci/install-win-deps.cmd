@SETLOCAL

SET SDL_LIB=SDL2-devel-2.0.6-VC
SET SDLTTF_LIB=SDL2_ttf-devel-2.0.14-VC
SET SDLMIXER_LIB=SDL2_mixer-devel-2.0.1-VC
SET SDLIMAGE_LIB=SDL2_image-devel-2.0.1-VC
@REM SET SDLGFX_LIB=SDL2_gfx-1.0.3

MKDIR dlls
CHDIR dlls

IF NOT EXIST %SDL_LIB%.zip appveyor DownloadFile https://www.libsdl.org/release/%SDL_LIB%.zip
IF NOT EXIST %SDLTTF_LIB%.zip appveyor DownloadFile https://www.libsdl.org/projects/SDL_ttf/release/%SDLTTF_LIB%.zip
IF NOT EXIST %SDLMIXER_LIB%.zip appveyor DownloadFile https://www.libsdl.org/projects/SDL_mixer/release/%SDLMIXER_LIB%.zip
IF NOT EXIST %SDLIMAGE_LIB%.zip appveyor DownloadFile https://www.libsdl.org/projects/SDL_image/release/%SDLIMAGE_LIB%.zip

7z e %SDL_LIB%.zip -o64bit *x64\*.dll -r -y
7z e %SDLTTF_LIB%.zip -o64bit *x64\*.dll -r -y
7z e %SDLMIXER_LIB%.zip -o64bit *x64\*.dll -r -y
7z e %SDLIMAGE_LIB%.zip -o64bit *x64\*.dll -r -y

7z e %SDL_LIB%.zip -o32bit *x86\*.dll -r -y
7z e %SDLTTF_LIB%.zip -o32bit *x86\*.dll -r -y
7z e %SDLMIXER_LIB%.zip -o32bit *x86\*.dll -r -y
7z e %SDLIMAGE_LIB%.zip -o32bit *x86\*.dll -r -y

@ENDLOCAL