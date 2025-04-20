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
    def get_children(position: tuple[int, int], maze: IMaze) -> list[tuple[int, int]]:
        children: list[tuple[int, int]] = []
        from_column, from_row = position

        for direction, movement in DIRECTIONS.items():
            if not maze.can_move(
                from_column=from_column, from_row=from_row, direction=direction
            ):
                continue

            to_column = from_column + movement[0]
            to_row = from_row + movement[1]
            children.append((to_column, to_row))

        return children

    @staticmethod
    def get_path(node: Optional[Node]) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []

        while node:
            path.append(node.get_position())
            node = node.get_parent()

        rute: list[tuple[int, int]] = path[::-1]

        return rute
