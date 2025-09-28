#!/usr/bin/env sh
echo "This script is deprecated. On Windows use: .\\tools\\build_pyinstaller.ps1"
echo "For development we recommend running the Flask app directly: python app.py"
exit 0
#!/usr/bin/env bash
# Build script for Unix/macOS using PyInstaller
set -e
EXE_NAME="puzzle_app"
# Use one-folder by default on Unix to make static data handling easier
pyinstaller --onedir --name "$EXE_NAME" --add-data "templates:templates" --add-data "static:static" app.py

echo "Build finished. Check the dist/$EXE_NAME/ folder."
