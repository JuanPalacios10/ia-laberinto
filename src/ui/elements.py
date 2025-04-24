from abc import ABC, abstractmethod
from typing import Callable, Optional
import pygame
from ui.config_ui import Colors, Images, Tools


class Element(ABC):
    @abstractmethod
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None: ...


class Mouse(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        screen.blit(Images.mouse, rect.topleft)


class Obstacle(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        pygame.draw.rect(screen, Colors.obstacle, rect)


class Cat(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        screen.blit(Images.cat, rect.topleft)


class Cheese(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        screen.blit(Images.cheese, rect.topleft)


class WallUp(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        pygame.draw.line(
            screen,
            Colors.wall,
            rect.topleft,
            rect.topright,
            4,
        )


class WallRight(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        pygame.draw.line(
            screen,
            Colors.wall,
            rect.topright,
            rect.bottomright,
            8,
        )


class WallDown(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        pygame.draw.line(
            screen,
            Colors.wall,
            rect.bottomleft,
            rect.bottomright,
            8,
        )


class WallLeft(Element):
    def draw(
        self,
        screen: pygame.Surface,
        rect: pygame.Rect,
    ) -> None:
        pygame.draw.line(
            screen,
            Colors.wall,
            rect.topleft,
            rect.bottomleft,
            4,
        )


class ElementFactory:
    @staticmethod
    def get_element(element_type: Tools) -> Element:
        if element_type == Tools.OBSTACLE:
            return Obstacle()
        elif element_type == Tools.MOUSE:
            return Mouse()
        elif element_type == Tools.CAT:
            return Cat()
        elif element_type == Tools.CHEESE:
            return Cheese()
        elif element_type == Tools.UP:
            return WallUp()
        elif element_type == Tools.RIGHT:
            return WallRight()
        elif element_type == Tools.DOWN:
            return WallDown()
        elif element_type == Tools.LEFT:
            return WallLeft()
        else:
            raise ValueError(f"Unknown element type: {element_type}")
