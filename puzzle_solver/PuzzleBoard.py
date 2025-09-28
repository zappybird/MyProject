import random

class PuzzleBoard:
    def __init__(self, initial_state=None):
        self.goal_state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
        self.state = initial_state if initial_state else self.generate_solvable_board()

    def generate_solvable_board(self):
        flat = list(range(9))
        while True:
            random.shuffle(flat)
            matrix = [flat[i:i+3] for i in range(0, 9, 3)]
            if self.is_solvable(matrix):
                return matrix

    def is_solvable(self, matrix):
        flat = sum(matrix, [])
        inversions = 0
        for i in range(len(flat)):
            for j in range(i + 1, len(flat)):
                if flat[i] != 0 and flat[j] != 0 and flat[i] > flat[j]:
                    inversions += 1
        return inversions % 2 == 0

    def shuffle(self):
        self.state = self.generate_solvable_board()

    def display(self):
        for row in self.state:
            print(row)
