@echo off
setlocal

rem Change directory to the location of this script
cd /d %~dp0

rem Compile the cubiomes wrapper DLLS
gcc -shared -o cubiomes_wrapper.dll -I./cubiomes cubiomes_wrapper.c ./cubiomes/biomenoise.c ./cubiomes/generator.c ./cubiomes/layers.c ./cubiomes/util.c ./cubiomes/noise.c ./cubiomes/quadbase.c ./cubiomes/biometree.c

rem Check if compilation was successful
if %errorlevel% neq 0 (
    echo Compilation failed.
    exit /b %errorlevel%
) else (
    echo Compilation successful.
)

endlocal
pause
