# 8-Puzzle Image Solver

This project implements an 8-puzzle web app using Flask. Users can upload an image which is
resized and sliced into 3x3 tiles to form a playable 8-puzzle. The app supports:

- Uploading an image (any size) which is resized to 600x600 and split into 9 tiles.
- Shuffling the puzzle using valid moves (preserves solvability).
- Solving using multiple algorithms: A* (Manhattan heuristic), BFS, DFS.
- Viewing the optimal solution step-by-step.

Heuristic used for A*:
- Manhattan distance (sum of absolute row/column differences). This is admissible for the 8-puzzle.

How to run locally:

1. Create a Python environment and install dependencies:

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app:

```powershell
python app.py
```

3. Open http://127.0.0.1:5000 in your browser.

Notes:
- The app stores per-session small state in Flask session and slices images into `static/tiles/`.
- Uploaded tile files are cleaned up when a new upload occurs during the same session. A periodic cleanup
  may be desirable for production.

Files of interest:
- `app.py` - Flask app and routes
- `templates/Puzzle.html` - interactive puzzle UI (click-to-move)
- `puzzle_solver/` - solver implementations (A*, BFS, DFS)
 
Additional notes
----------------

- Click-to-move: The puzzle UI supports clicking on a tile to move it into the blank if the move is legal. The page updates in-place (no full page reload) so you can play by clicking tiles.

  - Orphaned files can still accumulate if sessions end unexpectedly or previous runs left files behind. To remove all tile files manually (development use only), run this from PowerShell in the project root:
  
    ```powershell
    Get-ChildItem -Path static\tiles -Filter "*_tile_*.png" | Remove-Item -Force
    ```

Packaging as a standalone executable (optional)
---------------------------------------------

You can bundle this Flask app into a single executable using PyInstaller for easy distribution. The project includes a minimal PowerShell helper script at `tools/build_pyinstaller.ps1` which runs PyInstaller and includes the `templates/` and `static/` folders as data files.

Steps (Windows PowerShell):

1. Install PyInstaller into your environment:

```powershell
pip install pyinstaller
```

2. Run the build helper from the project root in PowerShell:

```powershell
.\tools\build_pyinstaller.ps1
```

3. The produced executable will be in `dist\puzzle_app.exe`.

Limitations:
- The executable is self-contained; however the `static/tiles/` upload directory will be inside the bundled app and is ephemeral at runtime. For production deployment you probably want to run the Flask app under a proper WSGI server rather than packaging into one EXE.

Run locally without packaging:

```powershell
python -m venv .venv
# PowerShell
.\.venv\Scripts\Activate.ps1
# or cmd.exe
.\.venv\Scripts\activate.bat
pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

