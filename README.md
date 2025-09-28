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
