from maze.maze import IMaze
from searches.search_strategy import ISearchStrategy


class Agent:
    def __init__(
        self, start_position: tuple[int, int], search_strategy: ISearchStrategy
    ):
        self.__position = start_position
        self.__search_strategy = search_strategy
        self.__path: list[tuple[int, int]] = []
        self.__no_solution = False

    def set_strategy(self, strategy: ISearchStrategy) -> None:
        self.__search_strategy = strategy

    def get_strategy(self) -> ISearchStrategy:
        return self.__search_strategy

    def get_position(self) -> tuple[int, int]:
        return self.__position

    def set_no_solution(self, goal_position: tuple[int, int]) -> None:
        if self.__path[-1] != goal_position:
            self.__no_solution = True
            return None

        self.__no_solution = False

    def get_no_solution(self) -> bool:
        return self.__no_solution

    def search_path(self, goal: tuple[int, int], maze: IMaze) -> bool:
        path = self.__search_strategy.search(self.__position, goal, maze)

        if path:
            self.__path = path[1:]
            self.set_no_solution(goal)
            return True

        return False

    def move_one_step(self) -> bool:
        if not self.__path:
            return False

        self.__position = self.__path.pop(0)
        return True

    def move_towards_goal(self, goal: tuple[int, int], maze: IMaze) -> bool:
        if not self.search_path(goal, maze):
            self.reset_path()
            return False

        return self.move_one_step()

    def reset_path(self) -> None:
        self.__path = []
