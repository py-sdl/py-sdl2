@SETLOCAL

@REM Set the PYTHON path variable to your python command, like C:\Python33\python.exe
@IF "%PYTHON%" == "" (
    ECHO Warning: PYTHON environment path not set.
    SET PYTHON=python
)

@IF "%~1" == "" GOTO :all
@GOTO :%~1

:all
@CALL :clean
@CALL :build
@GOTO :eof

:dist
@ECHO Creating dist...
@CALL :clean
@CALL :docs
@%PYTHON% setup.py sdist --format gztar
@%PYTHON% setup.py sdist --format zip
@GOTO :eof

:bdist
@CALL :clean
@CALL :docs
@ECHO Creating bdist...
@%PYTHON% setup.py bdist --format=msi
@GOTO :eof

:build
@ECHO Running build
@%PYTHON% setup.py build
@ECHO Build finished, invoke 'make install' to install.
@GOTO :eof

:install
@ECHO Installing...
@%PYTHON% setup.py install
@GOTO :eof

:clean
@ECHO Cleaning up...
@IF EXIST build RMDIR /S /Q build
@IF EXIST dist RMDIR /S /Q dist
@FOR /d /r . %%d in (__pycache__) do @IF EXIST "%%d" RMDIR /S /Q "%%d"
@IF EXIST MANIFEST DEL /S /Q MANIFEST
@IF EXIST *.pyc DEL /S /Q *.pyc
@GOTO :eof

:test
@%PYTHON% -B -m pytest -vvl -rxXP
@GOTO :eof

:docs
@ECHO Creating docs package
@RMDIR /S /Q doc\html
@CD doc
@CALL make html
@MOVE /Y _build\html html
@RMDIR /S /Q _build
@CALL make clean
@CD ..
@GOTO :eof

:release
@CALL :dist
@GOTO :eof

@ENDLOCAL
