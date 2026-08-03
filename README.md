# Catch the Apple

Catch the Apple is a small 2D Pygame arcade prototype. The player moves a basket along the bottom of the screen and catches falling apples while trying to preserve lives and build score.

The long-term goal is to grow this prototype into a polished portfolio project that demonstrates modern Python structure, modular 2D game architecture, graphics programming, physics, collision systems, procedural rendering, testing, and clear documentation.

## Current Status

The project is intentionally simple at this stage:

- Thin executable entry point: `main.py`
- Modular game package: `catch_the_apple/`
- Structured world/session model with focused gameplay systems
- Collection-based falling object model with a configurable spawn system
- Data-driven object definitions with only the regular apple enabled
- Velocity-based basket movement with acceleration, drag, and dash state
- Circle/composite collision system with optional debug overlay
- Cached procedural basket and apple rendering
- Lightweight ambient/directional lighting with cached shadows
- Keyboard input with left and right arrow keys
- Score, lives, collision detection, apple respawn, and basic difficulty scaling
- No asset pipeline, tests, or scene/state system yet

## Running

Run the game from the repository root:

```bash
python main.py
```

The project currently depends on Pygame being available in the active Python environment.

## Documentation

- `docs/ARCHITECTURE.md` describes the current architecture and intended direction.
- `docs/DEVELOPMENT.md` defines the development workflow.
- `docs/ROADMAP.md` captures high-level future project phases.
- `docs/PROMPTS_BOOK.md` is the permanent prompt-driven development log.

## Project Direction

This project must remain a 2D Pygame game. Future work should improve structure and polish while keeping the scope focused on a playable arcade experience rather than turning the repository into a general-purpose game engine.
