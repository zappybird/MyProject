def board_to_tuple(state):
    return tuple(n for row in state for n in row)


def tuple_to_board(tup):
    return [list(tup[i * 3:(i + 1) * 3]) for i in range(3)]


def get_neighbors_tuple(tup):
    zero = tup.index(0)
    r, c = divmod(zero, 3)
    neighbors = []
    for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            nidx = nr * 3 + nc
            lst = list(tup)
            lst[zero], lst[nidx] = lst[nidx], lst[zero]
            neighbors.append(tuple(lst))
    return neighbors


class DFSSolver:
    def __init__(self, start_state, max_depth=20):
        self.start = board_to_tuple(start_state)
        self.goal = board_to_tuple([[1,2,3],[4,5,6],[7,8,0]])
        self.max_depth = max_depth

    def solve(self):
        visited = set()
        path = []

        def dfs(node, depth):
            if depth > self.max_depth:
                return False
            visited.add(node)
            path.append(node)
            if node == self.goal:
                return True
            for nb in get_neighbors_tuple(node):
                if nb not in visited:
                    if dfs(nb, depth + 1):
                        return True
            path.pop()
            return False

        if dfs(self.start, 0):
            return [tuple_to_board(n) for n in path]
        return []
