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
    debug_overlay_toggled: bool
    mute_toggled: bool
    volume_up_pressed: bool
    volume_down_pressed: bool
    mouse_left_clicked: bool
    mouse_position: tuple[int, int]
    console_requested: bool
    console_submit_pressed: bool
    text_input: str
    backspace_pressed: bool


def poll_input() -> InputState:
    quit_requested = False
    dash_pressed = False
    debug_collision_toggled = False
    start_pressed = False
    pause_pressed = False
    restart_pressed = False
    debug_overlay_toggled = False
    mute_toggled = False
    volume_up_pressed = False
    volume_down_pressed = False
    mouse_left_clicked = False
    console_requested = False
    console_submit_pressed = False
    text_input = ""
    backspace_pressed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_requested = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            dash_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
            debug_collision_toggled = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            start_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pause_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            restart_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            console_requested = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            console_submit_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            backspace_pressed = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
            debug_overlay_toggled = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            mute_toggled = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_EQUALS, pygame.K_PLUS):
            volume_up_pressed = True
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_MINUS, pygame.K_UNDERSCORE):
            volume_down_pressed = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_left_clicked = True
        if event.type == pygame.TEXTINPUT:
            text_input += event.text

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
        debug_overlay_toggled=debug_overlay_toggled,
        mute_toggled=mute_toggled,
        volume_up_pressed=volume_up_pressed,
        volume_down_pressed=volume_down_pressed,
        mouse_left_clicked=mouse_left_clicked,
        mouse_position=pygame.mouse.get_pos(),
        console_requested=console_requested,
        console_submit_pressed=console_submit_pressed,
        text_input=text_input,
        backspace_pressed=backspace_pressed,
    )
