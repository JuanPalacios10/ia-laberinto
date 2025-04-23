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

    def update(self) -> None:
        if not self.__running:
            return

        updated: bool = self.__environment.update()
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

    def set_search_strategy(self, strategy: ISearchStrategy) -> None:
        self.__agent.set_strategy(strategy)

    def is_running(self) -> bool:
        return self.__running

    def set_running(self,  running: bool) -> None:
        self.__running = running
