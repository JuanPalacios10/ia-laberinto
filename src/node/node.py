class Node:
    def __init__(self, position: tuple[int, int], father=None):
        self._position: tuple[int, int] = position
        self._father = father

    def get_position(self) -> tuple[int, int]:
        return self._position

    def set_position(self, position: tuple[int, int]):
        self._position = position

    def get_father(self):
        return self._father

    def set_father(self, father):
        self._father = father


class NodeH(Node):
    def __init__(
        self, position: tuple[int, int], father=None, cost: int = 0, heuristic: int = 0
    ):
        super().__init__(position, father)
        self._cost = cost
        self._heuristic = heuristic

    def get_cost(self) -> int:
        return self._cost

    def get_heuristic(self) -> int:
        return self._heuristic

    def __lt__(self, other):
        return self._cost + self._heuristic < other.get_cost() + other.get_heuristic()
