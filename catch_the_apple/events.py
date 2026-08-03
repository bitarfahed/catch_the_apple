from dataclasses import dataclass

import pygame

from catch_the_apple.entities import FallingObject


@dataclass(frozen=True)
class ObjectCaughtEvent:
    falling_object: FallingObject
    position: pygame.Vector2
    color: tuple[int, int, int]


GameplayEvent = ObjectCaughtEvent
