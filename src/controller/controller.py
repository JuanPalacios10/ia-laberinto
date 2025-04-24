from agent.agent import Agent
from environment.environment import Environment
from maze.maze import IMaze
from searches.search_strategy import ISearchStrategy


class Controller:
    def __init__(self, environment: Environment, agent: Agent, maze: IMaze):
        self.__environment = environment
        self.__agent = agent
        self.__maze = maze

        self.__step_count = 0
        self.__running = True
        self.__searches = []
        self.__current_index_search = 0

    def update(self) -> None:
        if not self.__running:
            return

        self.__environment.update()
        self.set_search_strategy()
        self.__step_count += 1

        agent_position: tuple[int, int] = self.__agent.get_position()
        goal_position: tuple[int, int] = self.__environment.get_goal()

        if agent_position == goal_position:
            self.__running = False

    def reset(self) -> None:
        self.__step_count = 0
        self.__running = True

    def get_state(self) -> dict:
        return {
            "maze": self.__maze,
            "agent_position": self.__agent.get_position(),
            "goal_position": self.__environment.get_goal(),
            "step": self.__step_count,
        }

    def set_searches(self, searches: list[ISearchStrategy]) -> None:
        self.__searches = searches

    def set_search_strategy(self) -> None:
        if not self.__agent.get_no_solution():
            return None

        self.__current_index_search += 1

        if self.__current_index_search >= len(self.__searches):
            self.__current_index_search = 0

        new_strategy: ISearchStrategy = self.__searches[self.__current_index_search]
        print(new_strategy)
        self.__agent.set_strategy(new_strategy)

    def is_running(self) -> bool:
        return self.__running

    def set_running(self, running: bool) -> None:
        self.__running = running
