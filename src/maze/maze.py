from abc import ABC, abstractmethod


class IMaze(ABC):
    @abstractmethod
    def get_map(self) -> list[list[str]]: ...

    @abstractmethod
    def get_rows(self) -> int: ...

    @abstractmethod
    def get_columns(self) -> int: ...

    @abstractmethod
    def valid_free(self, column: int, row: int) -> bool: ...

    @abstractmethod
    def valid_position(self, column: int, row: int) -> bool: ...

    @abstractmethod
    def has_element(self, element: str, column: int, row: int) -> bool: ...

    @abstractmethod
    def add(self, element: str, column: int, row: int) -> None: ...

    @abstractmethod
    def remove(self, element: str, column: int, row: int) -> None: ...

    @abstractmethod
    def in_range(self, column: int, row: int) -> bool: ...

    @abstractmethod
    def get_free_positions(self) -> list[tuple[int, int]]: ...

    @abstractmethod
    def change_size(self, new_columns: int, new_rows: int) -> None: ...


class Maze(IMaze):
    OPTIONS: dict[str, dict[str, str] | str] = {
        "WALLS": {
            "UP": "U",
            "RIGHT": "R",
            "DOWN": "D",
            "LEFT": "L",
        },
        "FREE": " ",
        "OBSTACLE": "X",
        "CAT": "C",
    }

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

    def are_walls(self, element: str) -> bool:
        walls = self.OPTIONS.get("WALLS")

        if not isinstance(walls, dict):
            raise ValueError("WALLS must be a dictionary")

        return all(c in walls.values() for c in element)

    def option_to_string(self, option: str) -> str:
        value = self.OPTIONS.get(option)

        if value is None:
            raise ValueError("Invalid option")

        if isinstance(value, dict):
            raise ValueError("Option must be a string, not a dict")

        return value

    def in_range(self, column: int, row: int) -> bool:
        return 0 <= column < self.__columns and 0 <= row < self.__rows

    def has_element(self, element: str, column: int, row: int) -> bool:
        if not self.in_range(column, row):
            return False

        return element in self.__map[row][column]

    def valid_free(self, column: int, row: int) -> bool:
        element: str = self.__map[row][column]

        return element == self.OPTIONS["FREE"]

    def valid_position(self, column: int, row: int) -> bool:
        if not self.in_range(column, row):
            return False

        element: str = self.__map[row][column]

        return (len(element) < 4 and self.are_walls(element)) or self.valid_free(
            column, row
        )

    def __remove_wall(self, element: str, column: int, row: int) -> None:
        if not self.has_element(element, column, row):
            return None

        original: str = self.__map[row][column]
        new: str = original.replace(element, "")

        if len(new) == 0:
            new = self.option_to_string("FREE")

        self.__map[row][column] = new

    def remove(self, element: str, column: int, row: int) -> None:
        if not self.in_range(column, row):
            raise ValueError("Position out of range")

        if not self.are_walls(element):
            self.__map[row][column] = self.option_to_string("FREE")

        self.__remove_wall(element, column, row)

    def __add_wall(self, element: str, column: int, row: int) -> None:
        if self.has_element(element, column, row):
            return None

        original: str = self.__map[row][column]
        new: str = original + element

        if len(new) > 4:
            return None

        self.__map[row][column] = new

    def add(self, element: str, column: int, row: int) -> None:
        is_free = self.valid_position(column, row)

        if not self.are_walls(element) and is_free:
            self.__map[row][column] = element
            return None

        self.__add_wall(element, column, row)

    def get_free_positions(self) -> list[tuple[int, int]]:
        row_size: int = self.__rows
        column_size: int = self.__columns
        free_positions: list[tuple[int, int]] = []

        for row in range(row_size):
            for column in range(column_size):
                if self.valid_free(column, row):
                    free_positions.append((column, row))

        return free_positions

    def change_size(self, new_columns: int, new_rows: int) -> None:
        if new_columns < 0 or new_rows < 0:
            raise ValueError("Size must be positive")

        if new_columns == self.__columns and new_rows == self.__rows:
            return None

        new_map: list[list[str]] = [
            ["" for _ in range(new_columns)] for _ in range(new_rows)
        ]
        row_size: int = self.__rows
        column_size: int = self.__columns

        for row in range(new_rows):
            for column in range(new_columns):
                if row < row_size and column < column_size:
                    new_map[row][column] = self.__map[row][column]
                else:
                    new_map[row][column] = self.option_to_string("FREE")

        self.__rows = new_rows
        self.__columns = new_columns
        self.__map = new_map
