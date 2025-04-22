from typing import Optional
from maze.maze import IMaze
from node.node import Node
from .search_strategy import ISearchStrategy, Search


class DepthFirstSearch(ISearchStrategy):
    def search(
        self, start: tuple[int, int], goal: tuple[int, int], maze: IMaze
    ) -> Optional[list[tuple[int, int]]]:
        stack: list[Node] = []
        stack.append(Node(start))

        while stack:
            current_node = stack.pop()
            current_pos = current_node.get_position()

            if current_pos == goal:
                return self.get_path(current_node)

            children = self.get_children(current_pos, maze)

            for child in reversed(children):
                if not Search.without_returning(current_node, child):
                    continue

                if self.__is_in_path(current_node, child):
                    return None

                stack.append(Node(child, current_node))

        return None

    def get_children(
        self, position: tuple[int, int], maze: IMaze
    ) -> list[tuple[int, int]]:
        return Search.get_children(position, maze)

    def get_path(self, node: Optional[Node]) -> list[tuple[int, int]]:
        return Search.get_path(node)

    def __is_in_path(self, node: Optional[Node], position: tuple[int, int]) -> bool:
        while node:
            if node.get_position() == position:
                return True
            node = node.get_parent()
        return False
