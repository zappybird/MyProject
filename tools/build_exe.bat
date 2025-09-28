@echo off
echo This script is deprecated. Use PowerShell script tools\\build_pyinstaller.ps1 instead.
echo From PowerShell run: .\tools\build_pyinstaller.ps1
exit /b 0
@echo off
REM Build script for Windows (cmd.exe) using PyInstaller
set EXE_NAME=puzzle_app
pyinstaller --onefile --name %EXE_NAME% --add-data "templates;templates" --add-data "static;static" app.py
echo Build finished. Check the dist\%EXE_NAME%.exe
