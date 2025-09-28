# Minimal PyInstaller build helper for Windows PowerShell
# Usage: From the project root run: .\tools\build_pyinstaller.ps1

$exeName = "puzzle_app"
$spec = "--onefile"

# Include templates and static directories so the bundled exe can access them
$addData = "templates;templates;static;static"

$cmd = "pyinstaller $spec --add-data \"$addData\" --name $exeName app.py"
Write-Host "Running: $cmd"
Invoke-Expression $cmd

Write-Host "Build finished. Check the dist\$exeName.exe file."
