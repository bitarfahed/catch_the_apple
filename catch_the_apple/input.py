from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class InputState:
    quit_requested: bool
    left_pressed: bool
    right_pressed: bool


def poll_input() -> InputState:
    quit_requested = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_requested = True

    keys = pygame.key.get_pressed()
    return InputState(
        quit_requested=quit_requested,
        left_pressed=keys[pygame.K_LEFT],
        right_pressed=keys[pygame.K_RIGHT],
    )
