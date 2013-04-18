@SETLOCAL
@IF "%PYTHON27_X86%" == "" (
    SET PYTHON27_X86=c:\Python27-x86\python.exe
)
@IF "%PYTHON27_X64%" == "" (
    SET PYTHON27_X64=c:\Python27-x64\python.exe
)
@IF "%PYTHON32_X86%" == "" (
    SET PYTHON32_X86=c:\Python32-x86\python.exe
)
@IF "%PYTHON32_X64%" == "" (
    SET PYTHON32_X64=c:\Python32-x64\python.exe
)
@IF "%PYTHON33_X86%" == "" (
    SET PYTHON33_X86=c:\Python33-x86\python.exe
)
@IF "%PYTHON33_X64%" == "" (
    SET PYTHON33_X64=c:\Python33-x64\python.exe
)
@IF "%PYTHON%" == "" (
    SET PYTHON=%PYTHON27_X64%
)
@IF "%PYPY19%" == "" (
    SET PYPY19=c:\pypy-1.9\pypy.exe
)
@IF "%IRONPYTHON27%" == "" (
    SET IRONPYTHON27=c:\IronPython-2.7.3\ipy.exe
)

@IF "%1" == "" (
    GOTO :all
)
@GOTO :%1

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
@%PYTHON27_X86% setup.py bdist --format=msi
@%PYTHON32_X86% setup.py bdist --format=msi
@%PYTHON33_X86% setup.py bdist --format=msi
@%PYTHON27_X64% setup.py bdist --format=msi
@%PYTHON32_X64% setup.py bdist --format=msi
@%PYTHON33_X64% setup.py bdist --format=msi
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
@RMDIR /S /Q build
@RMDIR /S /Q dist
@FOR /d /r . %%d in (__pycache__) do @IF EXIST "%%d" RMDIR /S /Q "%%d"
@DEL /S /Q MANIFEST
@DEL /S /Q *.pyc
@GOTO :eof

:docs
@IF "%SPHINXBUILD%" == "" (
   SET SPHINXBUILD=C:\Python27-x64\Scripts\sphinx-build.exe
)
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

:runtest
@%PYTHON% test\util\runtests.py
@GOTO :eof

@REM Do not run these in production environments. They are for testing purposes
@REM only!

:buildall
@CALL :clean
@%PYTHON27_X86% setup.py build
@CALL :clean
@%PYTHON27_X64% setup.py build
@CALL :clean
@%PYTHON32_X86% setup.py build
@CALL :clean
@%PYTHON32_X64% setup.py build
@CALL :clean
@%PYTHON33_X86% setup.py build
@CALL :clean
@%PYTHON33_X64% setup.py build
@CALL :clean
@%PYPY19% setup.py build
@CALL :clean
@%IRONPYTHON27% setup.py build
@CALL :clean
@GOTO :eof

:installall
@CALL :clean
@%PYTHON27_X86% setup.py install
@CALL :clean
@%PYTHON27_X64% setup.py install
@CALL :clean
@%PYTHON32_X86% setup.py install
@CALL :clean
@%PYTHON32_X64% setup.py install
@CALL :clean
@%PYTHON33_X86% setup.py install
@CALL :clean
@%PYTHON33_X64% setup.py install
@CALL :clean
@%PYPY19% setup.py install
@CALL :clean
@%IRONPYTHON27% setup.py install
@CALL :clean
@GOTO :eof

:testall
@FOR /F "tokens=1 delims=" %%A in ('CHDIR') do @SET PYTHONPATH=%%A && @SET IRONPYTHONPATH=%%A
@%PYTHON27_X86% test\util\runtests.py
@DEL /Q test\*.pyc
@%PYTHON27_X64% test\util\runtests.py
@DEL /Q test\*.pyc
@%PYTHON32_X86% test\util\runtests.py
@DEL /Q test\*.pyc
@RMDIR /S /Q test\__pycache__
@%PYTHON32_X64% test\util\runtests.py
@DEL /Q test\*.pyc
@RMDIR /S /Q test\__pycache__
@%PYTHON33_X86% test\util\runtests.py
@DEL /Q test\*.pyc
@RMDIR /S /Q test\__pycache__
@%PYTHON33_X64% test\util\runtests.py
@DEL /Q test\*.pyc
@RMDIR /S /Q test\__pycache__
@%PYPY19% test\util\runtests.py
@DEL /Q test\*.pyc
@%IRONPYTHON27% test\util\runtests.py
@DEL /Q test\*.pyc
@GOTO :eof

:testall2
@%PYTHON27_X86% -c "import openal.test; openal.test.run ()"
@%PYTHON27_X64% -c "import openal.test; openal.test.run ()"
@%PYTHON32_X86% -c "import openal.test; openal.test.run ()"
@%PYTHON32_X64% -c "import openal.test; openal.test.run ()"
@%PYTHON33_X86% -c "import openal.test; openal.test.run ()"
@%PYTHON33_X64% -c "import openal.test; openal.test.run ()"
@%PYPY19% -c "import openal.test; openal.test.run ()"
@%IRONPYTHON27% -c "import openal.test; openal.test.run ()"
@GOTO :eof

:purge_installs
@echo Deleting data...
@RMDIR /S /Q C:\Python27-x86\Lib\site-packages\openal
@RMDIR /S /Q C:\Python27-x64\Lib\site-packages\openal
@RMDIR /S /Q C:\Python32-x86\Lib\site-packages\openal
@RMDIR /S /Q C:\Python32-x64\Lib\site-packages\openal
@RMDIR /S /Q C:\Python33-x86\Lib\site-packages\openal
@RMDIR /S /Q C:\Python33-x64\Lib\site-packages\openal
@RMDIR /S /Q C:\pypy-1.9\site-packages\openal
@RMDIR /S /Q C:\IronPython-2.7.3\Lib\site-packages\openal
@echo done
@GOTO :eof

@ENDLOCAL
