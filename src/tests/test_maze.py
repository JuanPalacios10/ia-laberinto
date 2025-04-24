import pytest
from constants.maze_options import option_to_string
from maze.maze import Maze


def test_position_out_of_bounds_behavior():
    custom_map = [
        [" ", "X", "UR", " "],
        ["C", "DL", "URLX", " "],
        ["X", " ", "D", "R"],
        ["G", "L", "U", " "],
    ]
    maze = Maze(4, 4, custom_map)

    # Validaciones de rango
    assert not maze.in_range(column=-1, row=0)
    assert not maze.in_range(column=0, row=-1)
    assert not maze.in_range(column=4, row=0)
    assert not maze.in_range(column=0, row=4)

    # Remove: sí lanza ValueError
    with pytest.raises(ValueError):
        maze.remove("C", column=-1, row=0)


def test_has_element():
    custom_map = [
        [" ", "X", "UR", " "],
        ["C", "DL", "URLX", " "],
        ["X", " ", "D", "R"],
        ["G", "L", "U", " "],
    ]
    maze = Maze(4, 4, custom_map)

    assert maze.has_element("G", column=0, row=3)
    assert maze.has_element("X", column=2, row=1)
    assert maze.has_element("U", column=2, row=0)
    assert not maze.has_element(" ", column=0, row=1)
    assert not maze.has_element("D", column=2, row=3)


def test_valid_free():
    # Mapa con celdas de hasta 4 paredes, celdas libres y obstáculos
    custom_map = [
        ["URDL", "X", " ", "UD"],
        [" ", "UR", "X", "RL"],
        ["D", " ", "ULX", " "],
    ]
    maze = Maze(4, 3, custom_map)

    # Celdas libres
    assert maze.valid_free(
        column=0, row=1, valid_element=option_to_string("FREE")
    )  # libre
    assert maze.valid_free(
        column=1, row=2, valid_element=option_to_string("FREE")
    )  # libre
    assert maze.valid_free(
        column=3, row=2, valid_element=option_to_string("FREE")
    )  # libre

    # Celdas no libres
    assert not maze.valid_free(
        column=1, row=0, valid_element=option_to_string("CAT")
    )  # obstáculo "X"
    assert not maze.valid_free(
        column=0, row=0, valid_element=option_to_string("LEFT")
    )  # "URDL"
    assert not maze.valid_free(
        column=2, row=2, valid_element=option_to_string("CAT")
    )  # "UL"

    # Celdas libres con paredes
    assert maze.valid_free(
        column=3, row=0, valid_element=option_to_string("RIGHT")
    )  # "UD"
    assert maze.valid_free(column=2, row=2, valid_element=option_to_string("DOWN"))
    assert maze.valid_free(column=2, row=1, valid_element=option_to_string("UP"))

    # Celdas con paredes
    assert maze.valid_free(column=3, row=0, valid_element=option_to_string("CHEESE"))
    assert maze.valid_free(column=0, row=2, valid_element=option_to_string("CAT"))


def test_add_and_remove():
    # mapa vacío
    custom_map = [[" " for _ in range(3)] for _ in range(3)]
    maze = Maze(3, 3, custom_map)

    # Agregar obstáculo
    maze.add("X", column=1, row=1)
    assert maze.has_element("X", column=1, row=1)
    assert not maze.valid_free(column=1, row=1, valid_element=option_to_string("FREE"))
    assert maze.valid_free(column=1, row=1, valid_element=option_to_string("UP"))

    # Remover obstáculo
    maze.remove("X", column=1, row=1)
    assert not maze.has_element("X", column=1, row=1)
    assert maze.valid_free(column=1, row=1, valid_element=option_to_string("FREE"))

    # Agregar pared en fijo
    maze.add("C", column=0, row=0)
    assert maze.has_element("C", column=0, row=0)
    maze.add("U", column=0, row=0)
    assert maze.has_element("U", column=0, row=0)
    assert maze.valid_free(column=0, row=0, valid_element=option_to_string("LEFT"))
    assert not maze.valid_free(
        column=0, row=0, valid_element=option_to_string("CHEESE")
    )

    # Remover pared en fijo
    maze.remove("U", column=0, row=0)
    assert not maze.has_element("U", column=0, row=0)
    assert maze.valid_free(column=0, row=0, valid_element=option_to_string("DOWN"))
    maze.remove("C", column=0, row=0)
    assert not maze.has_element("C", column=0, row=0)

    # Agregar fijo en pared
    maze.add("U", column=2, row=2)
    assert maze.has_element("U", column=2, row=2)
    maze.add("G", column=2, row=2)
    assert maze.has_element("G", column=2, row=2)
    assert not maze.valid_free(column=2, row=2, valid_element=option_to_string("CAT"))

    # Remover fijo en pared
    maze.remove("G", column=2, row=2)
    assert not maze.has_element("G", column=2, row=2)
    assert maze.valid_free(column=2, row=2, valid_element=option_to_string("CAT"))


def test_get_free_positions():
    custom_map = [[" ", "X", " "], ["U", "UR", "C"], ["URD", "X", " "]]
    maze = Maze(3, 3, custom_map)

    expected_free = [(0, 0), (0, 2), (1, 0), (1, 1), (2, 0), (2, 2)]

    free_positions = maze.get_free_positions(valid_element=option_to_string("CHEESE"))

    # Las posiciones deben coincidir (orden no importa, comparamos como conjuntos)
    assert set(free_positions) == set(expected_free)


def test_invalid_option_to_string_and_walls():
    with pytest.raises(ValueError):
        option_to_string("DOES_NOT_EXIST")

    with pytest.raises(ValueError):
        option_to_string("WALLS")  # WALLS es un dict

    assert option_to_string("UP") == "U"
    assert option_to_string("RIGHT") == "R"
    assert option_to_string("DOWN") == "D"
    assert option_to_string("LEFT") == "L"
    assert option_to_string("FREE") == " "
    assert option_to_string("OBSTACLE") == "X"
    assert option_to_string("CAT") == "C"
    assert option_to_string("CHEESE") == "G"


def test_get_element():
    map = [[" ", "C", "X", "URL", "DG"]]
    maze = Maze(5, 1, map)

    assert maze.get_element(column=0, row=0) == " "
    assert maze.get_element(column=1, row=0) == "C"
    assert maze.get_element(column=2, row=0) == "X"
    assert maze.get_element(column=3, row=0) == "URL"
    assert maze.get_element(column=4, row=0) == "DG"


def test_can_move():
    custom_map = [
        [" ", "X", "UR", " "],
        ["C", "DL", "URLX", " "],
        ["X", " ", "D", "R"],
        ["G", "L", "U", " "],
    ]
    maze = Maze(4, 4, custom_map)

    assert maze.can_move(from_column=3, from_row=0, direction="DOWN")
    assert not maze.can_move(from_column=0, from_row=0, direction="UP")
    assert maze.can_move(from_column=0, from_row=0, direction="DOWN")
    assert not maze.can_move(from_column=1, from_row=3, direction="LEFT")
    assert not maze.can_move(from_column=1, from_row=1, direction="RIGHT")


def test_get_all_positions():
    custom_map = [
        [" ", "X", "UR", " "],
        ["C", "DL", "URLX", " "],
        ["X", " ", "D", "R"],
        ["G", "L", "U", " "],
    ]
    maze = Maze(4, 4, custom_map)

    positions = maze.get_all_positions()

    assert len(positions) == 16


def test_get_len_map():
    custom_map = [
        [" ", "X", "UR", " ", "X"],
        ["C", "DL", "URLX", " ", "C"],
        ["X", " ", "D", "R", " "],
        ["G", "L", "U", " ", "ULD"],
        [" ", "LR", "UD", "X", " "],
    ]
    maze = Maze(5, 5, custom_map)

    assert maze.get_len() == 25
