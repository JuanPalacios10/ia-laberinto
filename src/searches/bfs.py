from collections import deque
from typing import Deque, Optional
from maze.maze import IMaze
from node.node import Node
from searches.search_strategy import ISearchStrategy, Search


class BreadthFirstSearch(ISearchStrategy):
    def search(
        self, start: tuple[int, int], goal: tuple[int, int], maze: IMaze
    ) -> Optional[list[tuple[int, int]]]:
        queue: Deque[Node] = deque()
        limit_iterations: int = maze.get_len() * 100
        iterations: int = 0
        queue.append(Node(start))

        while queue and iterations <= limit_iterations:
            iterations += 1
            current_node = queue.popleft()
            current_pos = current_node.get_position()

            if current_pos == goal:
                return self.get_path(current_node)

            children = self.get_children(current_pos, maze)

            for child in children:
                if Search.without_returning(current_node, child):
                    queue.append(Node(child, current_node))

        return None

    def get_children(
        self, position: tuple[int, int], maze: IMaze
    ) -> list[tuple[int, int]]:
        return Search.get_children(position, maze)

    def get_path(self, node: Optional[Node]) -> list[tuple[int, int]]:
        return Search.get_path(node)
