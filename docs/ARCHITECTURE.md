# Architecture

## Overview

Catch the Apple is currently a small modular Pygame game. The root `main.py` file is a thin executable entry point, and the game logic lives in the `catch_the_apple` package.

The architecture is intentionally lightweight. It separates the first major responsibilities without introducing a broad framework or changing gameplay.

## Current Runtime Structure

The game starts when `main.py` is executed. `main.py` delegates to `catch_the_apple.app.main`, which creates and runs `catch_the_apple.game.Game`. Pygame is initialized inside the `Game` constructor, so importing the entry point no longer starts the game loop.

`Game` owns the runtime loop. `GameSession` owns session-level state such as score, lives, and whether the session is running. `World` owns active gameplay entities: currently one basket and one falling apple stored through a list-shaped `falling_objects` model so future prompts can support multiple falling objects without changing the renderer or runtime loop again.

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
| Entry point | `main.py` and `catch_the_apple.__main__` delegate to `catch_the_apple.app.main` |
| Game loop | `catch_the_apple.game.Game` owns initialization, loop, update/render calls, and shutdown |
| Game session | `catch_the_apple.session.GameSession` owns score, lives, and running flag |
| World | `catch_the_apple.world.World` owns the basket and falling object collection |
| Input | `catch_the_apple.input.poll_input` wraps Pygame event and key polling |
| Entities | `Basket` and `Apple` dataclasses |
| Collision | `catch_the_apple.collision.collides` uses `pygame.Rect.colliderect` |
| Runtime timing | Delta-time measured from `pygame.time.Clock`, clamped to avoid large spikes |
| Physics | Simple velocity-style movement using pixels per second |
| Rendering | `catch_the_apple.rendering.Renderer` draws rectangles and HUD text |
| Math | `catch_the_apple.math2d` provides `Vector2`, `Transform2D`, and small helpers |
| Gameplay systems | Movement, spawning, scoring, difficulty progression, and game rules live in `catch_the_apple.systems` |
| Assets | No external assets yet |
| Configuration | Constants in `catch_the_apple.config` |
| Tests | None yet |

## Intended Direction

Future architecture should continue separating responsibilities into small, practical modules only when the game needs them: richer state management, asset loading, deterministic systems, and testable game rules. The current runtime now has separate update and render phases, which should remain the foundation for future gameplay and rendering work.

The goal is not to create a general game engine. The architecture should serve this game first, while still being clean enough to demonstrate professional Python design.

## Keep Mostly Unchanged

The following current decisions are good foundations:

- Pygame as the rendering and input framework
- Simple arcade loop structure
- Rectangle collision for early gameplay
- Score/lives mechanic
- Gradual difficulty increase
- Fixed-size playfield while the prototype is still small
