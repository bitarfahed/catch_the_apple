from dataclasses import dataclass, field

import pygame

from catch_the_apple import config
from catch_the_apple.math2d import Transform2D, vec2
from catch_the_apple.object_definitions import ObjectDefinition


@dataclass
class MovementState:
    velocity: pygame.Vector2 = field(default_factory=pygame.Vector2)
    acceleration: pygame.Vector2 = field(default_factory=pygame.Vector2)
    direction: pygame.Vector2 = field(default_factory=pygame.Vector2)
    dash_time_remaining: float = 0.0
    dash_cooldown_remaining: float = 0.0
    dash_direction: float = 0.0

    @property
    def speed(self) -> float:
        return self.velocity.length()

    @property
    def is_dashing(self) -> bool:
        return self.dash_time_remaining > 0.0


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
    movement: MovementState = field(default_factory=MovementState)
    max_speed: float = config.BASKET_MAX_SPEED
    acceleration_rate: float = config.BASKET_ACCELERATION
    drag: float = config.BASKET_DRAG
    dash_speed: float = config.BASKET_DASH_SPEED
    dash_duration: float = config.BASKET_DASH_DURATION
    dash_cooldown: float = config.BASKET_DASH_COOLDOWN

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

    @property
    def velocity(self) -> pygame.Vector2:
        return self.movement.velocity

    @property
    def movement_direction(self) -> pygame.Vector2:
        return self.movement.direction

    @property
    def current_speed(self) -> float:
        return self.movement.speed


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
