@echo off
@REM Change to the path of the current folder
cd G:\path\to\your\timer
echo %CD%

@REM Note here: pythonw.exe is not python.exe, pythonw will not open a command line window to run Python scripts
@REM Note: Change to the path of pythonw.exe
start /min "" C:\path\to\your\pythonw.exe count_down_en.py

endlocal