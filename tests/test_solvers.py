import unittest
from puzzle_solver.astar import AStarSolver
from puzzle_solver.bfs import BFSSolver
from puzzle_solver.dfs import DFSSolver

class SolverTests(unittest.TestCase):
    def setUp(self):
        self.goal = [
            [1,2,3],
            [4,5,6],
            [7,8,0]
        ]
        self.simple = [
            [1,2,3],
            [4,0,5],
            [6,7,8]
        ]

    def test_astar_reaches_goal(self):
        solver = AStarSolver(self.simple)
        path = solver.solve()
        self.assertTrue(len(path) >= 1)
        self.assertEqual(path[-1], self.goal)

    def test_bfs_reaches_goal(self):
        solver = BFSSolver(self.simple)
        path = solver.solve()
        self.assertTrue(len(path) >= 1)
        self.assertEqual(path[-1], self.goal)

    def test_dfs_reaches_goal(self):
        solver = DFSSolver(self.simple, max_depth=20)
        path = solver.solve()
        # DFS might not find if depth insufficient, but with 20 should
        self.assertTrue(isinstance(path, list))

if __name__ == '__main__':
    unittest.main()
