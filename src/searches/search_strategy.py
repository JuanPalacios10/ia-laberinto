from abc import ABC, abstractmethod
from typing import Optional
from constants.directions import DIRECTIONS
from maze.maze import IMaze
from node.node import Node


class ISearchStrategy(ABC):
    @abstractmethod
    def search(
        self, start: tuple[int, int], goal: tuple[int, int], maze: IMaze
    ) -> Optional[list[tuple[int, int]]]: ...

    @abstractmethod
    def get_children(
        self, position: tuple[int, int], maze: IMaze
    ) -> list[tuple[int, int]]: ...

    @abstractmethod
    def get_path(self, node: Optional[Node]) -> list[tuple[int, int]]: ...


class Search:
    @staticmethod
    def without_returning(
        current_node: Node, position: tuple[int, int]
    ) -> Optional[bool]:
        grandparent: Optional[Node] = current_node.get_parent()
        return not grandparent or position != grandparent.get_position()

    @staticmethod
    def get_children(position: tuple[int, int], maze: IMaze) -> list[tuple[int, int]]:
        children: list[tuple[int, int]] = []
        from_row, from_column = position

        for direction, movement in DIRECTIONS.items():
            if not maze.can_move(
                from_column=from_column, from_row=from_row, direction=direction
            ):
                continue

            row, column = movement
            to_row = from_row + row
            to_column = from_column + column
            children.append((to_row, to_column))

        return children

    @staticmethod
    def get_path(node: Optional[Node]) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []

        while node:
            path.append(node.get_position())
            node = node.get_parent()

        route: list[tuple[int, int]] = path[::-1]

        return route
