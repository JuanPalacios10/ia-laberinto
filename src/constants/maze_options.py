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
        raise ValueError("Invalid option")

    if isinstance(value, dict):
        raise ValueError("Option must be a string, not a dict")

    return value
