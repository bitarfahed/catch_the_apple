from dataclasses import dataclass

import pygame


@dataclass(frozen=True)
class InputState:
    quit_requested: bool
    left_pressed: bool
    right_pressed: bool
    dash_pressed: bool
    debug_collision_toggled: bool
    start_pressed: bool
    pause_pressed: bool
    restart_pressed: bool


def poll_input() -> InputState:
    quit_requested = False
    dash_pressed = False
    debug_collision_toggled = False
    start_pressed = False
    pause_pressed = False
    restart_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_requested = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            dash_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            debug_collision_toggled = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            start_pressed = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_p):
            pause_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_pressed = True

    keys = pygame.key.get_pressed()
    return InputState(
        quit_requested=quit_requested,
        left_pressed=keys[pygame.K_LEFT],
        right_pressed=keys[pygame.K_RIGHT],
        dash_pressed=dash_pressed,
        debug_collision_toggled=debug_collision_toggled,
        start_pressed=start_pressed,
        pause_pressed=pause_pressed,
        restart_pressed=restart_pressed,
    )
