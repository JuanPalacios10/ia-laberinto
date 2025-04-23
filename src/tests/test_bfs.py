from maze.maze import Maze
from searches.bfs import BreadthFirstSearch


def test_bfs_with_solution():
    maze_map = [
        [" ", "UR", "L", " "],
        ["X", "L", "UR", " "],
        [" ", "X", " ", "U"],
        ["U", "L", "X", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    bfs = BreadthFirstSearch()
    start = (0, 0)
    goal = (3, 3)
    path = bfs.search(start, goal, maze)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
    assert len(path) > 1
    assert path == [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 3), (3, 3)]


def test_bfs_without_solution():
    maze_map = [
        ["UR", "UR", "X", "U"],
        [" ", "DRX", "X", "X"],
        ["R", "R", "X", " "],
        ["U", "X", "L", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    bfs = BreadthFirstSearch()
    start = (0, 0)
    goal = (3, 3)
    path = bfs.search(start, goal, maze)
    assert path is None


def test_bfs_with_complex_solution():
    maze_map = [
        ["L", "U", "C", " "],
        ["LR", "DLRX", "X", " "],
        ["L", "UR", " ", "U"],
        ["U", "L", "R", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    bfs = BreadthFirstSearch()
    start = (0, 0)
    goal = (3, 3)
    path = bfs.search(start, goal, maze)
    assert path is not None
    assert path[0] == start
    assert path[-1] == goal
    assert len(path) > 1
    assert path == [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (3, 1),
        (3, 2),
        (2, 2),
        (2, 3),
        (3, 3),
    ]


def test_bfs_without_solution_complex():
    maze_map = [
        ["UR", "X", "UR", " "],
        [" ", "UR", "X", "X"],
        ["R", " ", "X", " "],
        ["U", "X", "L", "G"],
    ]
    maze = Maze(columns=4, rows=4, map=maze_map)
    bfs = BreadthFirstSearch()
    start = (0, 0)
    goal = (3, 3)
    path = bfs.search(start, goal, maze)
    assert path is None
