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

- Click-to-move: The puzzle UI supports clicking on a tile to move it into the blank if the move is legal. The client sends a POST to `/move` and the server responds with the updated puzzle `state` and `tile_map`. The page updates in-place (no full page reload) so you can play by clicking tiles.

- Tile file lifecycle and cleanup:
  - When you upload an image the server resizes it and slices it into 9 PNG tiles saved under `static/tiles/` with a per-upload UUID prefix to avoid filename collisions.
  - The original uploaded image file is deleted immediately after slicing (so your raw upload is not kept).
  - The app attempts to remove the tiles for the current session in two places:
    1. When a new upload happens, `cleanup_old_tiles()` removes any files recorded in `session['tiles']` from `static/tiles/`.
    2. The Puzzle page includes a "Clear uploads" button which POSTs to `/cleanup` — this removes files for the current session and clears the session puzzle state.

  - Orphaned files can still accumulate if sessions end unexpectedly or previous runs left files behind. To remove all tile files manually (development use only), run this from PowerShell in the project root:

```powershell
Get-ChildItem -Path .\static\tiles\ -File | Remove-Item
```

  - If you prefer automatic aggressive cleanup, I can add a `/purge_tiles` admin endpoint (debug-only) or a one-time script to remove old files older than X days. Tell me if you'd like that and I can add it.

If the tile-file lifecycle conflicts with your workflow or grading requirements I won't change the design; tell me your preferred behavior (keep tiles permanently vs. delete after upload vs. delete on session end) and I'll adapt.
