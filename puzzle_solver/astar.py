import heapq

class AStarSolver:
    def __init__(self, start_state):
        self.start = start_state
        self.goal = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

    def heuristic(self, state):
        # Manhattan Distance
        distance = 0
        for i in range(3):
            for j in range(3):
                val = state[i][j]
                if val != 0:
                    goal_x = (val - 1) // 3
                    goal_y = (val - 1) % 3
                    distance += abs(i - goal_x) + abs(j - goal_y)
        return distance

    def get_neighbors(self, state):
        neighbors = []
        x, y = [(ix, iy) for ix, row in enumerate(state) for iy, val in enumerate(row) if val == 0][0]
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append(new_state)
        return neighbors

    def solve(self):
        frontier = []
        heapq.heappush(frontier, (self.heuristic(self.start), self.start, []))
        visited = set()

        while frontier:
            _, current, path = heapq.heappop(frontier)
            if current == self.goal:
                return path + [current]
            visited.add(str(current))

            for neighbor in self.get_neighbors(current):
                if str(neighbor) not in visited:
                    heapq.heappush(frontier, (self.heuristic(neighbor) + len(path), neighbor, path + [current]))

        return []
