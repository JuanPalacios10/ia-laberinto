from abc import ABC, abstractmethod
from typing import Optional
from constants.directions import DIRECTIONS, OPPOSITE_DIRECTIONS
from constants.maze_options import MAZE_OPTIONS, option_to_string


class IMaze(ABC):
    @abstractmethod
    def get_map(self) -> list[list[str]]: ...

    @abstractmethod
    def get_rows(self) -> int: ...

    @abstractmethod
    def get_columns(self) -> int: ...

    @abstractmethod
    def valid_free(self, column: int, row: int, valid_element: str) -> bool: ...

    @abstractmethod
    def can_move(self, from_column: int, from_row: int, direction: str) -> bool: ...

    @abstractmethod
    def get_element(self, column: int, row: int) -> Optional[str]: ...

    @abstractmethod
    def has_element(self, element: str, column: int, row: int) -> bool: ...

    @abstractmethod
    def add(self, element: str, column: int, row: int) -> bool: ...

    @abstractmethod
    def remove(self, element: str, column: int, row: int) -> bool: ...

    @abstractmethod
    def in_range(self, column: int, row: int) -> bool: ...

    @abstractmethod
    def get_free_positions(self, valid_element: str) -> list[tuple[int, int]]: ...

    @abstractmethod
    def get_all_positions(self) -> list[tuple[int, int]]: ...

    @abstractmethod
    def change_size(self, new_columns: int, new_rows: int) -> None: ...


class Maze(IMaze):
    OPTIONS: dict[str, str | dict[str, str]] = MAZE_OPTIONS

    def __init__(self, columns: int, rows: int, map: list[list[str]]):
        self.__rows = rows
        self.__columns = columns
        self.__map = map

    def get_map(self) -> list[list[str]]:
        return self.__map

    def get_rows(self) -> int:
        return self.__rows

    def get_columns(self) -> int:
        return self.__columns

    def __is_fix(self, value: str) -> bool:
        return not self.__is_wall(value) and value in MAZE_OPTIONS.values()

    def __is_wall(self, value: str) -> bool:
        walls = MAZE_OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("Option must be a dict")

        return value in walls.values()

    def __there_are_walls(self, element: str) -> bool:
        walls = self.OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("WALLS must be a dictionary")

        return any(c for c in element if c in walls.values())

    def in_range(self, column: int, row: int) -> bool:
        return 0 <= column < self.__columns and 0 <= row < self.__rows

    def has_element(self, element: str, column: int, row: int) -> bool:
        if not self.in_range(column, row):
            return False

        return element in self.__map[row][column]

    def valid_free(self, column: int, row: int, valid_element: str) -> bool:
        if not self.in_range(column, row):
            return False

        element: str = self.__map[row][column]

        if element == self.OPTIONS["FREE"]:
            return True

        if self.__is_fix(valid_element):
            return self.__valid_fix(element)

        if self.__is_wall(valid_element):
            return self.__valid_wall(element)

        return False

    def __valid_fix(self, element: str) -> bool:
        return not self.__is_fix(element) and self.__valid_free_wall(element)

    def __valid_free_wall(self, element: str) -> bool:
        walls = self.OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("WALLS must be a dictionary")

        are_walls = all(c in walls.values() for c in element)

        return len(element) < 4 and are_walls

    def __valid_wall(self, element: str) -> bool:
        return (
            self.__is_fix(element)
            or self.__valid_fix_wall(element)
            or self.__valid_free_wall(element)
        )

    def __valid_fix_wall(self, element: str) -> bool:
        return len(element) < 4 and self.__there_are_walls(element)

    def get_element(self, column: int, row: int) -> Optional[str]:
        if not self.in_range(column, row):
            return None

        return self.__map[row][column]

    def can_move(self, from_column: int, from_row: int, direction: str) -> bool:
        delta_row, delta_column = DIRECTIONS[direction]
        to_row, to_column = (
            from_row + delta_row,
            from_column + delta_column,
        )

        if not self.in_range(to_column, to_row) or self.has_element(
            option_to_string("OBSTACLE"), to_column, to_row
        ):
            return False

        if self.valid_free(to_column, to_row, valid_element=option_to_string("FREE")):
            return True

        element: str = self.__map[from_row][from_column]
        next_element = self.__map[to_row][to_column]

        walls = self.OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("WALLS must be a dictionary")

        wall_to_direction = walls.get(direction, "") in element
        opposite_direction = OPPOSITE_DIRECTIONS[direction]
        opposite_wall = walls.get(opposite_direction, "") in next_element

        return not wall_to_direction and not opposite_wall

    def __remove_wall(self, element: str, column: int, row: int) -> bool:
        original: str = self.__map[row][column]
        new: str = original.replace(element, "")

        if len(new) == 0:
            new = option_to_string("FREE")

        self.__map[row][column] = new
        return True

    def remove(self, element: str, column: int, row: int) -> bool:
        if not self.in_range(column, row):
            raise ValueError("Position out of range")

        if not self.has_element(element, column, row):
            return False

        if self.__is_fix(element):
            self.__map[row][column] = option_to_string("FREE")
            return True

        return self.__remove_wall(element, column, row)

    def __add_wall(self, element: str, column: int, row: int) -> bool:
        if not self.valid_free(column, row, element):
            return False

        original: str = self.__map[row][column]
        new: str = original + element

        self.__map[row][column] = new
        return True

    def add(self, element: str, column: int, row: int) -> bool:
        if self.has_element(element, column, row):
            return False

        if self.valid_free(column, row, valid_element=option_to_string("FREE")):
            self.__map[row][column] = element
            return True

        return self.__add_wall(element, column, row)

    def get_free_positions(self, valid_element: str) -> list[tuple[int, int]]:
        row_size: int = self.__rows
        column_size: int = self.__columns
        free_positions: list[tuple[int, int]] = []

        for row in range(row_size):
            for column in range(column_size):
                if self.valid_free(column, row, valid_element):
                    free_positions.append((row, column))

        return free_positions

    def __get_free_positions_agent(self, agent: bool, column: int, row: int) -> bool:
        return agent and self.has_element(option_to_string("CAT"), column, row)

    def get_all_positions(self) -> list[tuple[int, int]]:
        positions: list[tuple[int, int]] = []

        for row in range(self.__rows):
            for column in range(self.__columns):
                positions.append((row, column))

        return positions

    def change_size(self, new_columns: int, new_rows: int) -> None:
        if new_columns < 0 or new_rows < 0:
            raise ValueError("Size must be positive")

        row_size: int = self.__rows
        column_size: int = self.__columns

        if new_columns == column_size and new_rows == row_size:
            return None

        new_map: list[list[str]] = [
            ["" for _ in range(new_columns)] for _ in range(new_rows)
        ]

        for row in range(new_rows):
            for column in range(new_columns):
                if row < row_size and column < column_size:
                    new_map[row][column] = self.__map[row][column]
                else:
                    new_map[row][column] = option_to_string("FREE")

        self.__rows = new_rows
        self.__columns = new_columns
        self.__map = new_map
