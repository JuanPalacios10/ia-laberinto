from maze.maze import Maze
from searches.dfs import DepthFirstSearch


def test_depth_first_search_basic():
    # Definir un laberinto
    maze_map = [
        ["R", "R", "R", " "],
        ["C", "X", "X", " "],
        ["D", "X", "X", " "],
        ["D", "G", "C", "R"],
    ]
    maze = Maze(4, 4, maze_map)

    dfs = DepthFirstSearch()

    # Establecer posiciones de inicio y objetivo
    start = (0, 3)
    goal = (3, 1)

    # Ejecutar la búsqueda
    path = dfs.search(start, goal, maze)

    # Verificar que se haya encontrado un camino
    assert path is not None
    assert len(path) > 0
    assert path[0] == start
    assert path[-1] == goal
    assert path == [(0, 3), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1)]


def test_depth_first_not_solution():
    maze_map = [
        ["R", "R", "D", "D"],
        ["C", "X", "X", "X"],
        ["D", "X", "X", "X"],
        ["D", "D", "G", "R"],
    ]
    maze = Maze(4, 4, maze_map)

    dfs = DepthFirstSearch()

    # Establecer posiciones de inicio y objetivo
    start = (0, 3)
    goal = (3, 2)

    # Ejecutar la búsqueda
    path = dfs.search(start, goal, maze)

    # Verificar que no se haya encontrado un camino
    assert path is None


def test_depth_first_cycle():
    maze_map = [
        [" ", " ", "X", "X"],
        ["L", "R", "U", "X"],
        ["U", "U", "U", "X"],
        ["C", "L", " ", "G"],
    ]
    maze = Maze(4, 4, maze_map)

    dfs = DepthFirstSearch()

    start = (0, 0)
    goal = (3, 3)  # Objetivo a la derecha ('G')

    path = dfs.search(start, goal, maze)

    assert path is None
