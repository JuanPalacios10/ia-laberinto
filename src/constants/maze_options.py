MAZE_OPTIONS: dict[str, dict[str, str] | str] = {
    "WALLS": {
        "UP": "U",
        "RIGHT": "R",
        "DOWN": "D",
        "LEFT": "L",
    },
    "FREE": " ",
    "OBSTACLE": "X",
    "CAT": "C",
    "CHEESE": "G",
}


def option_to_string(option: str) -> str:
    value = MAZE_OPTIONS.get(option)

    if value is None:
        value = option_walls_to_string(option)

    if isinstance(value, dict):
        raise ValueError("Option must be a string, not a dict")

    return value


def option_walls_to_string(option: str) -> str:
    walls = MAZE_OPTIONS.get("WALLS")

    if not isinstance(walls, dict):
        raise ValueError("Option must be a dict")

    wall_value = walls.get(option)

    if wall_value is None:
        raise ValueError("Invalid option")

    return wall_value
