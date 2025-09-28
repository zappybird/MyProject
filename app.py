
# ===== Imports =====
import os
import random
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from PIL import Image, ImageOps
from werkzeug.utils import secure_filename
import uuid
import json
from pathlib import Path

# ===== Configuration =====
app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = os.path.join('static', 'tiles')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ===== Utility Functions =====
def prepare_image(image_path, target_size=(600, 600)):
    img = Image.open(image_path)
    img = ImageOps.fit(img, target_size, method=Image.BICUBIC)
    return img
def slice_image(image_path, prefix=""):
    """Resizes image, slices into 3x3 tiles, saves them with an optional
    prefix (to avoid collisions), and returns filenames (relative to
    UPLOAD_FOLDER).
    """
    # If caller passed a tuple (image_path, prefix) handle that gracefully
    if isinstance(image_path, tuple) and len(image_path) == 2:
        image_path, prefix = image_path

    img = prepare_image(image_path, target_size=(600, 600))
    w, h = img.size
    cols = rows = 3
    tw, th = w // cols, h // rows
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    tile_files = []
    idx = 0
    for r in range(rows):
        for c in range(cols):
            left, upper = c * tw, r * th
            box = (left, upper, left + tw, upper + th)
            tile = img.crop(box)
            fname = f"{prefix}tile_{idx}.png"
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            tile.save(path)
            tile_files.append(fname)
            idx += 1
    return tile_files


def cleanup_old_tiles():
    """Remove previously uploaded tiles for this session (if any).

    Uses filenames stored in session['tiles'] (list of filenames saved in
    static/tiles). This is best-effort and ignores errors.
    """
    old = session.get('tiles')
    if not old:
        return
    for fname in old:
        try:
            path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            # ignore deletion errors
            pass


# ===== Helpers =====
def flat_from_state(state):
    return [n for row in state for n in row]


def state_from_flat(flat):
    return [flat[i * 3:(i + 1) * 3] for i in range(3)]


def neighbors(pos):
    r, c = divmod(pos, 3)
    result = []
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            result.append(nr * 3 + nc)
    return result


def randomize_state_by_moves(state, moves=50):
    """Randomize state by performing valid moves from the given state.

    This guarantees the resulting configuration is solvable.
    """
    flat = flat_from_state(state)
    blank = flat.index(0)
    flat = flat[:]  # copy
    for _ in range(moves):
        nbrs = neighbors(blank)
        nxt = random.choice(nbrs)
        flat[blank], flat[nxt] = flat[nxt], flat[blank]
        blank = nxt
    return state_from_flat(flat)
# ===== Simple file-backed session store =====
DATA_DIR = Path('data')
DATA_DIR.mkdir(exist_ok=True)


def session_store_path(session_id: str) -> Path:
    return DATA_DIR / f"{session_id}.json"


def save_session_state(session_id: str, payload: dict):
    path = session_store_path(session_id)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(payload, f)


def load_session_state(session_id: str) -> dict:
    path = session_store_path(session_id)
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Use modular solvers from the `puzzle_solver` package for clarity and testability
from puzzle_solver.astar import AStarSolver
from puzzle_solver.PuzzleBoard import PuzzleBoard
from puzzle_solver.bfs import BFSSolver
from puzzle_solver.dfs import DFSSolver


# ===== Routes =====
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Use secure filename and a unique prefix so multiple users/uploads
    # don't overwrite each other's tiles. Clean up previous session tiles.
    cleanup_old_tiles()
    file = request.files.get('image')
    if not file:
        return redirect(url_for('index'))
    filename = secure_filename(file.filename)
    unique_prefix = f"{uuid.uuid4().hex}_"
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(path)
    # slice with a unique prefix
    tiles = slice_image((path, unique_prefix))

    # store state in session (serializable types only)
    puzzle_matrix = [
        [1, 2, 3],
        [4, 0, 5],
        [6, 7, 8],
    ]
    tile_map = {
        1: tiles[0],
        2: tiles[1],
        3: tiles[2],
        4: tiles[3],
        5: tiles[4],
        6: tiles[5],
        7: tiles[6],
        8: tiles[7],
        0: None
    }
    # session will JSON-serialize this dict; convert keys to strings to
    # ensure predictable lookup after serialization.
    session['puzzle_matrix'] = puzzle_matrix
    session['current_state'] = [row[:] for row in puzzle_matrix]
    session['tiles'] = tiles
    session['tile_map'] = {str(k): v for k, v in tile_map.items()}
    session['upload_prefix'] = unique_prefix
    return redirect(url_for('puzzle'))

@app.route('/puzzle')
def puzzle():
    puzzle_matrix = session.get('puzzle_matrix')
    tiles = session.get('tiles')
    raw_tile_map = session.get('tile_map') or {}
    # convert keys back to ints for template convenience
    try:
        tile_map = {int(k): v for k, v in raw_tile_map.items()}
    except Exception:
        tile_map = raw_tile_map
    if puzzle_matrix is None:
        return redirect(url_for('index'))
    return render_template('puzzle.html', puzzle_matrix=puzzle_matrix, tiles=tiles, tile_map=tile_map)


@app.route('/session_debug')
def session_debug():
    """Return the current session as JSON for debugging (safe: session only holds serializable data)."""
    return jsonify(dict(session))

@app.route('/shuffle', methods=['POST'])
def shuffle():
    current = session.get('current_state')
    tile_map = session.get('tile_map')
    if current is None:
        return redirect(url_for('puzzle'))
    # Use valid-move randomization to preserve solvability
    new_state = randomize_state_by_moves(current, moves=50)
    session['current_state'] = new_state
    return render_template('puzzle.html', puzzle_matrix=new_state, tile_map=tile_map)

@app.route('/solve', methods=['POST'])
def solve():
    current_state = session.get('current_state')
    if current_state is None:
        return redirect(url_for('puzzle'))
    algorithm = request.form.get('algorithm', 'astar').lower()
    # modular solvers expect a 3x3 list (not a PuzzleBoard instance)
    if algorithm == 'astar':
        steps = AStarSolver(current_state).solve()
    elif algorithm == 'bfs':
        steps = BFSSolver(current_state).solve()
    else:
        steps = DFSSolver(current_state).solve()
    session['solution_steps'] = steps
    session['algorithm'] = algorithm
    return redirect(url_for('solution'))

@app.route('/solution')
def solution():
    steps = session.get('solution_steps', [])
    algorithm = session.get('algorithm', 'unknown')
    raw_tile_map = session.get('tile_map') or {}
    try:
        tile_map = {int(k): v for k, v in raw_tile_map.items()}
    except Exception:
        tile_map = raw_tile_map
    return render_template('solution.html', solution_steps=steps, algorithm=algorithm, tile_map=tile_map)

# ===== Error Handlers =====
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message=str(e)), 404

# ===== Main Entry Point =====
if __name__ == '__main__':
    app.run(debug=True)

