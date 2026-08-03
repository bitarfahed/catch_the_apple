from dataclasses import dataclass, field

import pygame

from catch_the_apple import config
from catch_the_apple.math2d import Transform2D, vec2
from catch_the_apple.object_definitions import ObjectDefinition


@dataclass
class Basket:
    transform: Transform2D = field(
        default_factory=lambda: Transform2D(
            position=vec2(
                (config.SCREEN_WIDTH - config.BASKET_WIDTH) // 2,
                config.SCREEN_HEIGHT - config.BASKET_HEIGHT - config.BASKET_Y_OFFSET,
            )
        )
    )
    width: int = config.BASKET_WIDTH
    height: int = config.BASKET_HEIGHT
    speed: float = config.BASKET_SPEED

    @property
    def x(self) -> float:
        return self.transform.position.x

    @x.setter
    def x(self, value: float) -> None:
        self.transform.position.x = value

    @property
    def y(self) -> float:
        return self.transform.position.y

    @y.setter
    def y(self, value: float) -> None:
        self.transform.position.y = value

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)


@dataclass
class FallingObject:
    transform: Transform2D
    definition: ObjectDefinition
    speed: float = config.APPLE_INITIAL_SPEED

    @property
    def size(self) -> int:
        return self.definition.collision_size

    @property
    def x(self) -> float:
        return self.transform.position.x

    @x.setter
    def x(self, value: float) -> None:
        self.transform.position.x = value

    @property
    def y(self) -> float:
        return self.transform.position.y

    @y.setter
    def y(self, value: float) -> None:
        self.transform.position.y = value

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.x), int(self.y), self.size, self.size)
