import random
from maze.maze import IMaze


class Environment:
    def __init__(self, maze: IMaze, goal_position: tuple[int, int]):
        self.__maze = maze
        self.__goal_position = goal_position

    def set_goal(self, column: int, row: int) -> None:
        if self.__maze.add("G", column, row):
            self.__goal_position = (column, row)
        else:
            return None

    def move_goal(self) -> None:
        free_positions = self.__maze.get_free_positions()

        if not free_positions:
            return None

        new_col, new_row = random.choice(free_positions)

        if self.__goal_position:
            self.__maze.remove("G", *self.__goal_position)

        self.set_goal(new_col, new_row)

    def get_goal(self) -> tuple[int, int]:
        return self.__goal_position

    def get_maze(self) -> IMaze:
        return self.__maze
