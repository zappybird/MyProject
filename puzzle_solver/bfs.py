from collections import deque


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


class BFSSolver:
    def __init__(self, start_state):
        # start_state is a 3x3 list
        self.start = board_to_tuple(start_state)
        self.goal = board_to_tuple([[1,2,3],[4,5,6],[7,8,0]])

    def solve(self):
        if self.start == self.goal:
            return [tuple_to_board(self.start)]
        q = deque([self.start])
        came_from = {self.start: None}
        while q:
            cur = q.popleft()
            if cur == self.goal:
                path = []
                node = cur
                while node is not None:
                    path.append(tuple_to_board(node))
                    node = came_from[node]
                path.reverse()
                return path
            for nb in get_neighbors_tuple(cur):
                if nb not in came_from:
                    came_from[nb] = cur
                    q.append(nb)
        return []
