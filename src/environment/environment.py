import random
from agent.agent import Agent
from constants.maze_options import MAZE_OPTIONS, option_to_string
from maze.maze import IMaze


class Environment:
    def __init__(self, maze: IMaze, goal_position: tuple[int, int], agent: Agent):
        self.__maze = maze
        self.__goal_position = goal_position
        self.__agent = agent

    def set_goal(self, column: int, row: int) -> None:
        if self.__maze.add(option_to_string("CHEESE"), column, row):
            self.__goal_position = (row, column)
        else:
            return None

    def move_goal(self) -> None:
        free_positions = [
            pos
            for pos in self.__maze.get_free_positions(option_to_string("CHEESE"))
            if pos != self.__agent.get_position()
        ]
        if not free_positions:
            return None

        new_row, new_col = random.choice(free_positions)

        if self.__goal_position:
            row, column = self.__goal_position
            self.__maze.remove("G", column=column, row=row)

        self.set_goal(new_col, new_row)

    def get_goal(self) -> tuple[int, int]:
        return self.__goal_position

    def get_maze(self) -> IMaze:
        return self.__maze

    def update(self) -> bool:
        moved: bool = self.__agent.move_towards_goal(self.__goal_position, self.__maze)

        if moved and random.random() < 1:
            self.modify_environment()
            return True

        return False

    def modify_environment(self, max_modifications: int = 10) -> None:
        positions: list[tuple[int, int]] = self.__maze.get_all_positions()
        agent_position: tuple[int, int] = self.__agent.get_position()

        candidate_positions: list[tuple[int, int]] = [
            position for position in positions if position != agent_position
        ]

        positions_to_modify: list[tuple[int, int]] = random.sample(
            candidate_positions, min(max_modifications, len(candidate_positions))
        )

        for row, column in positions_to_modify:
            random_key: str = self.__choose_random_element()

            if random_key == "CHEESE":
                self.move_goal()
                continue

            random_element: str = option_to_string(random_key)

            if self.__maze.remove(random_element, column=column, row=row):
                continue

            self.__maze.add(random_element, column=column, row=row)

    def __choose_random_element(self) -> str:
        elements: list[str] = list(MAZE_OPTIONS.keys())
        walls = MAZE_OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("WALLS option must be a dict")

        random_key: str = random.choice(elements)

        if random_key == "WALLS":
            wall_element: list[str] = list(walls.keys())
            random_key = random.choice(wall_element)

        return random_key
