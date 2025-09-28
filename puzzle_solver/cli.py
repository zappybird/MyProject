import argparse
from .astar import AStarSolver
from .bfs import BFSSolver
from .dfs import DFSSolver


def parse_state(s: str):
    # expect 9 comma-separated ints
    parts = [int(x) for x in s.split(',')]
    return [parts[i*3:(i+1)*3] for i in range(3)]


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--solver', choices=['astar','bfs','dfs'], default='astar')
    p.add_argument('--state', required=True, help='9 comma-separated ints for 3x3 state, row-major')
    args = p.parse_args()
    state = parse_state(args.state)
    if args.solver == 'astar':
        solver = AStarSolver(state)
    elif args.solver == 'bfs':
        solver = BFSSolver(state)
    else:
        solver = DFSSolver(state)
    path = solver.solve()
    for step in path:
        for row in step:
            print(row)
        print('---')


if __name__ == '__main__':
    main()
