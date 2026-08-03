from dataclasses import dataclass, field

import pygame

Vector2 = pygame.Vector2


def vec2(x: float = 0.0, y: float = 0.0) -> Vector2:
    return Vector2(x, y)


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(value, maximum))


@dataclass
class Transform2D:
    position: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    scale: Vector2 = field(default_factory=lambda: Vector2(1.0, 1.0))
