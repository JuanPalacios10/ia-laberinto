from __future__ import annotations
from typing import Optional


class Node:
    def __init__(self, position: tuple[int, int], parent: Optional[Node] = None):
        self.__position: tuple[int, int] = position
        self.__parent = parent

    def get_position(self) -> tuple[int, int]:
        return self.__position

    def set_position(self, position: tuple[int, int]):
        self.__position = position

    def get_parent(self):
        return self.__parent


class NodeH(Node):
    def __init__(
        self,
        position: tuple[int, int],
        parent: Optional[NodeH] = None,
        cost: int = 0,
        heuristic: int = 0,
    ):
        super().__init__(position, parent)
        self.__cost = cost
        self.__heuristic = heuristic

    def get_total_cost(self) -> int:
        return self.__cost + self.__heuristic

    def __lt__(self, other: NodeH):
        return self.get_total_cost() < other.get_total_cost()
