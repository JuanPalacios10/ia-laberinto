from ui.editor import ConfigMaze, create_window
from controller.controller import Controller
from environment.environment import Environment
from maze.maze import Maze
from agent.agent import Agent
from searches.search_strategy import ISearchStrategy
from searches.bfs import BreadthFirstSearch
from searches.a_star import Astar
from ui.graficar import GraphMaze

def main():
    
    window = create_window()

    #crear laberinto
    editor = ConfigMaze(window)
    editor.run()
    map, goal_position, start_position,  = editor.export_map()
    print(map, goal_position, start_position)

    row = len(map)
    col = len(map[0])
    maze = Maze(col, row, map)

    #crear agente
    agent = Agent(start_position, Astar())

    #crear entorno
    ambiente = Environment(maze, goal_position, agent)

    #crear controlador
    controller = Controller(ambiente, agent, maze)

    graficador = GraphMaze(map, start_position)
    graficador.run(controller)

if __name__ == "__main__": 
    main()