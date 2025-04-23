from maze.maze import Maze
from searches.a_star import Astar


def test_astar_with_solution():
    maze_map = [
        [" ", "UR", "X", " "],
        [" ", "L", "U", " "],
        [" ", "L", " ", "U"],
        ["U", "L", "D", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    astar = Astar()
    start = (0, 3)
    goal = (3, 3)
    path = astar.search(start, goal, maze)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
    assert path == [(0, 3), (1, 3), (1, 2), (2, 2), (2, 3), (3, 3)]


def test_astar_without_solution():
    maze_map = [
        ["U", "URX", "X", "UG"],
        [" ", " ", "X", "X"],
        ["R", "LD", " ", " "],
        ["U", "X", "L", "URLG"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    astar = Astar()
    start = (0, 0)
    goal = (0, 3)
    path = astar.search(start, goal, maze)
    assert path is None


def test_astar_with_cat_cost():
    maze_map = [
        [" ", "UR", "L", " "],
        ["C", "L", "U", " "],
        [" ", "X", " ", "LR"],
        ["U", "L", "C", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    astar = Astar()
    start = (0, 0)
    goal = (3, 3)
    path = astar.search(start, goal, maze)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
    assert path == [(0, 0), (0, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]


# def test_astar_blocked_by_obstacles():
#     maze_map = [
#         ["UR", "X", "UR", " "],
#         [" ", "URC", "X", "X"],
#         ["L", " ", "C", "D"],
#         ["U", "X", "LU", "G"],
#     ]
#     maze = Maze(columns=4, rows=4, map=maze_map)
#     astar = Astar()
#     start = (0, 0)
#     goal = (3, 3)
#     path = astar.search(start, goal, maze)
#     assert path is None
