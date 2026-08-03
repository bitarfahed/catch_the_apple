# Architecture

## Overview

Catch the Apple is currently a small modular Pygame game. The root `main.py` file is a thin executable entry point, and the game logic lives in the `catch_the_apple` package.

The architecture is intentionally lightweight. It separates the first major responsibilities without introducing a broad framework or changing gameplay.

## Current Runtime Structure

The game starts when `main.py` is executed. `main.py` delegates to `catch_the_apple.app.main`, which creates and runs `catch_the_apple.game.Game`. Pygame is initialized inside the `Game` constructor, so importing the entry point no longer starts the game loop.

`Game` owns the runtime loop. `GameSession` owns session-level state such as score, lives, and whether the session is running. `World` owns active gameplay entities: currently one basket and a collection of falling objects. Falling objects are created from data-driven object definitions. The spawn system is configured to keep one regular apple active, preserving current gameplay while supporting future expansion.

The loop currently follows this order:

1. Measure clamped delta time.
2. Poll input.
3. Update basket and falling object movement.
4. Apply game rules for misses, catches, scoring, lives, and difficulty.
5. Ask the spawn system to maintain the configured active object count.
6. Render the world and session state.
7. Flip the display.

## Current Subsystems

| Subsystem | Current State |
|---|---|
| Entry point | `main.py` and `catch_the_apple.__main__` delegate to `catch_the_apple.app.main` |
| Game loop | `catch_the_apple.game.Game` owns initialization, loop, update/render calls, and shutdown |
| Game session | `catch_the_apple.session.GameSession` owns score, lives, and running flag |
| World | `catch_the_apple.world.World` owns the basket and falling object collection |
| Input | `catch_the_apple.input.poll_input` wraps Pygame event and key polling |
| Entities | `Basket` and `FallingObject` dataclasses |
| Object definitions | `catch_the_apple.object_definitions` stores registry data for apples, hazards, and power-ups |
| Collision | `catch_the_apple.collision` provides circle/object collision, composite basket regions, and swept catch checks |
| Runtime timing | Delta-time measured from `pygame.time.Clock`, clamped to avoid large spikes |
| Physics | Velocity-based basket movement with acceleration, drag, dash state, and screen constraints |
| Rendering | `catch_the_apple.rendering.Renderer` draws cached procedural surfaces and HUD text |
| Lighting | `catch_the_apple.lighting` applies reusable ambient/directional lighting and ground shadows |
| Math | `catch_the_apple.math2d` provides `Vector2`, `Transform2D`, and small helpers |
| Procedural assets | `catch_the_apple.procedural_assets` generates cached apple and basket surfaces |
| Environment | `catch_the_apple.environment` generates cached procedural parallax background layers |
| Effects | `catch_the_apple.particles`, `effects`, and `animation` provide pooled particles and squash/stretch components |
| Gameplay systems | Movement, spawning, scoring, difficulty progression, and game rules live in `catch_the_apple.systems` |
| Spawn system | `SpawnSystem` owns seeded random placement, weighted object selection, and the configured active object count |
| Assets | No external assets yet |
| Configuration | Constants, spawn parameters, and enabled object IDs in `catch_the_apple.config` |
| Tests | None yet |

## Intended Direction

Future architecture should continue separating responsibilities into small, practical modules only when the game needs them: richer state management, asset loading, deterministic systems, and testable game rules. The current runtime now has separate update and render phases, which should remain the foundation for future gameplay and rendering work.

Basket movement state exposes current velocity, movement direction, and speed for future animation and rendering systems. Visual effects are not implemented yet.

Collision debug rendering can be toggled with F1. The overlay visualizes basket regions, object circles, and swept object movement paths without changing gameplay rules.

Procedural asset rendering currently generates basket and apple surfaces from Pygame primitives and caches them by appearance. No external image assets are required.

Lighting is surface-based and cached. It applies ambient shading, directional diffuse highlights, simple specular overlays, and soft ground shadows without per-frame pixel loops.

Visual effects are simulated outside gameplay rules. Gameplay systems emit lightweight events, effects consume those events, and the renderer draws particles and animation-scaled surfaces.

The environment renderer is independent from gameplay state. It generates cached procedural layers for sky, clouds, mountains, trees, bushes, and grass, then scrolls them by per-layer depth factors for lightweight parallax.

The goal is not to create a general game engine. The architecture should serve this game first, while still being clean enough to demonstrate professional Python design.

## Keep Mostly Unchanged

The following current decisions are good foundations:

- Pygame as the rendering and input framework
- Simple arcade loop structure
- Rectangle collision for early gameplay
- Score/lives mechanic
- Gradual difficulty increase
- Fixed-size playfield while the prototype is still small
