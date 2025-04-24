from typing import Optional
from constants.maze_options import option_to_string
from maze.maze import IMaze
from node.node import Node, NodeH
from searches.search_strategy import ISearchStrategy, Search
import heapq


def manhattan(pos1: tuple[int, int], pos2: tuple[int, int]) -> int:
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Astar(ISearchStrategy):
    def search(
        self, start: tuple[int, int], goal: tuple[int, int], maze: IMaze
    ) -> Optional[list[tuple[int, int]]]:
        priority_queue: list[NodeH] = []
        limit_iterations: int = maze.get_len() * 100
        iterations: int = 0
        heapq.heappush(priority_queue, NodeH(start, None, 0, manhattan(start, goal)))

        while priority_queue and iterations <= limit_iterations:
            iterations += 1
            current_node = heapq.heappop(priority_queue)
            current_pos = current_node.get_position()

            if current_pos == goal:
                return self.get_path(current_node)

            children = self.get_children(current_pos, maze)

            for child in children:
                cost: int = 1
                row, column = child

                if maze.has_element(option_to_string("CAT"), column=column, row=row):
                    cost = 5

                if not Search.without_returning(current_node, child):
                    continue

                g = current_node.get_cost() + cost
                h = manhattan(child, goal)
                child_node = NodeH(child, current_node, g, h)
                heapq.heappush(priority_queue, child_node)

        return None

    def get_children(
        self, position: tuple[int, int], maze: IMaze
    ) -> list[tuple[int, int]]:
        return Search.get_children(position, maze)

    def get_path(self, node: Optional[Node]) -> list[tuple[int, int]]:
        return Search.get_path(node)

    def get_search_name(self) -> str:
        return "Búsqueda A*"
