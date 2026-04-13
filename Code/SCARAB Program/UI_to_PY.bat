
@echo off

setlocal enabledelayedexpansion

echo Running from: %CD%
pause
for /f "delims=" %%f in ('dir /b "GUI QtCreator\SCARAB_UI\*.ui"') do (
    set name=%%~nf
    echo Converting %%f
    pyside6-uic "GUI QtCreator\SCARAB_UI\%%f" -o "GUI_Screens\!name!.py"
)

echo Done!
pause