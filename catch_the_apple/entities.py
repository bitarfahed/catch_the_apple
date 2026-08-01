from dataclasses import dataclass

import pygame

from catch_the_apple import config


@dataclass
class Basket:
    x: int = (config.SCREEN_WIDTH - config.BASKET_WIDTH) // 2
    y: int = config.SCREEN_HEIGHT - config.BASKET_HEIGHT - config.BASKET_Y_OFFSET
    width: int = config.BASKET_WIDTH
    height: int = config.BASKET_HEIGHT
    speed: int = config.BASKET_SPEED

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)


@dataclass
class Apple:
    x: int
    y: int = -config.APPLE_SIZE
    size: int = config.APPLE_SIZE
    speed: int = config.APPLE_INITIAL_SPEED

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.size, self.size)


@dataclass
class GameState:
    score: int = 0
    lives: int = config.INITIAL_LIVES
    running: bool = True
