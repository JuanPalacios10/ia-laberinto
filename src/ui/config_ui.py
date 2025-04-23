from dataclasses import dataclass
from enum import Enum

from pygame import Surface
import pygame


@dataclass
class Window:
    rows: int
    cols: int
    width: int
    height: int


@dataclass
class Colors:
    free: tuple[int, int, int] = (255, 255, 255)
    wall: tuple[int, int, int] = (0, 0, 0)
    obstacle: tuple[int, int, int] = (120, 120, 120)
    division: tuple[int, int, int] = (200, 200, 200)


class Tools(str, Enum):
    EMPTY = "Borrar"
    FREE = "Libre"
    MOUSE = "Ratón"
    CHEESE = "Queso"
    CAT = "Gato"
    OBSTACLE = "Obstaculo"
    UP = "Pared Arriba"
    RIGHT = "Pared Derecha"
    DOWN = "Pared Abajo"
    LEFT = "Pared Izquierda"


@dataclass
class Images:
    mouse: Surface = pygame.image.load("assets/mouse.png")
    cheese: Surface = pygame.image.load("assets/cheese.png")
    cat: Surface = pygame.image.load("assets/cat.png")

    @staticmethod
    def set_scale(cell_size: int) -> None:
        Images.mouse = pygame.transform.scale(Images.mouse, (cell_size, cell_size))
        Images.cheese = pygame.transform.scale(Images.cheese, (cell_size, cell_size))
        Images.cat = pygame.transform.scale(Images.cat, (cell_size, cell_size))
