# Architecture

## Overview

Catch the Apple is currently a single-file Pygame game implemented in `main.py`. The architecture is a direct prototype structure: initialization, global state, input handling, update logic, collision checks, rendering, and shutdown all live in one module.

This is appropriate for the current size of the project, but future development should introduce clear module boundaries while preserving the simplicity of a 2D Pygame arcade game.

## Current Runtime Structure

The game starts when `main.py` is executed. Pygame is initialized, a window is created, game variables are defined, and the main loop runs until the player closes the window or loses all lives.

The loop currently follows this order:

1. Process window events.
2. Read keyboard input.
3. Update basket position.
4. Update apple position.
5. Handle missed apples.
6. Check basket/apple collision.
7. Draw background, entities, score, and lives.
8. Flip the display and cap the frame rate.

## Current Subsystems

| Subsystem | Current State |
|---|---|
| Entry point | Direct execution of `main.py` |
| Game state | Module-level variables |
| Input | Direct Pygame keyboard polling |
| Entities | Basket and apple represented by position/size variables |
| Collision | `pygame.Rect.colliderect` |
| Physics | Fixed pixel-per-frame movement |
| Rendering | Pygame primitive rectangles and font rendering |
| Assets | No external assets yet |
| Configuration | Hardcoded constants and globals |
| Tests | None yet |

## Intended Direction

Future architecture should separate responsibilities into small, practical modules: configuration, game lifecycle, entities, input, update systems, collision, rendering, assets, and state management.

The goal is not to create a general game engine. The architecture should serve this game first, while still being clean enough to demonstrate professional Python design.

## Keep Mostly Unchanged

The following current decisions are good foundations:

- Pygame as the rendering and input framework
- Simple arcade loop structure
- Rectangle collision for early gameplay
- Score/lives mechanic
- Gradual difficulty increase
- Fixed-size playfield while the prototype is still small
