# Catch the Apple Prompts Book

## Project Vision

Catch the Apple will evolve from a compact Pygame prototype into a polished 2D arcade portfolio project. Development should demonstrate clean Python architecture, modular game systems, graphics programming, collision and physics concepts, procedural rendering, testing, and professional documentation.

## Development Workflow

Development is prompt-driven and incremental. Each prompt should focus on one bounded project step, preserve the game in a runnable state, and avoid mixing unrelated refactors with feature work.

Before implementation prompts, the current structure should be inspected and the intended change should be scoped. After implementation prompts, the repository should be verified with the most relevant available checks.

## Prompt Documentation Rules

Each future prompt entry should record:

- Prompt number and title
- Date
- Objective
- Files changed
- Summary of completed work
- Verification performed
- Follow-up notes, if any

Entries should describe what actually changed, not what was merely considered. Keep entries concise enough to remain useful as a long-term development history.

## Development Log

### Prompt 1: Architecture Bootstrap

**Date:** 2026-08-01

**Goal:** Refactor the single-file prototype into a modular package while preserving the existing gameplay behavior.

**Full Prompt Text:**

```text
Prompt 1 - Architecture Bootstrap

Context

The repository documentation has been initialized and the long-term vision has been documented.

Your task is now to perform the first architectural refactor.

The goal is NOT to add new gameplay features.

The game must behave exactly as before.

This prompt should only establish a clean project structure that future prompts can build upon.

---

Objectives

Refactor the project from a single-file prototype into a modular package while preserving identical behavior.

Create a clean architecture with clear separation of responsibilities.

At minimum, introduce modules for:

- application / entry point
- configuration
- game loop
- entities
- rendering
- input
- collision
- utilities (if needed)

Use names that fit the existing project naturally.

Move logic into appropriate modules without changing gameplay.

Create a proper executable entry point.

The project must no longer execute game logic at import time.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 1
- Title
- Goal
- Full prompt text
- Files created
- Files modified
- Short implementation summary
- Test results
- Completion status

---

Restrictions

Do NOT:

- Change gameplay
- Add new mechanics
- Introduce delta time
- Add particles
- Add procedural graphics
- Add menus
- Add audio
- Add tests beyond simple smoke verification
- Add unnecessary abstractions

Avoid overengineering.

---

Acceptance Criteria

- Gameplay is visually identical.
- Repository is modular.
- Entry point is clean.
- Importing modules has no side effects.
- Game still runs exactly as before.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Architectural decisions
- Manual verification performed
- Confirmation that gameplay was not intentionally changed
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/__init__.py`
- `catch_the_apple/__main__.py`
- `catch_the_apple/app.py`
- `catch_the_apple/collision.py`
- `catch_the_apple/config.py`
- `catch_the_apple/entities.py`
- `catch_the_apple/game.py`
- `catch_the_apple/input.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/utils.py`

**Files Modified:**

- `main.py`
- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

The game was split into a small `catch_the_apple` package. `main.py` now delegates to a guarded application entry point. Configuration constants, entity dataclasses, input polling, collision checks, rendering, apple utility functions, and the game loop now live in separate modules. Gameplay behavior, frame-based timing, rendering primitives, controls, scoring, lives, and apple speed progression were preserved.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Import smoke check for `main` and package modules passed without starting the game loop.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 2: Core Runtime

**Date:** 2026-08-01

**Goal:** Establish a time-based runtime foundation with separated update/render phases and reusable 2D transform utilities while preserving current gameplay.

**Full Prompt Text:**

```text
Prompt 2 - Core Runtime

Context

The project now has a modular architecture with a clean entry point.

This prompt establishes the runtime foundation that all future gameplay and rendering systems will rely on.

Do not introduce new gameplay features.

The game should feel almost identical to the player.

---

Objectives

Replace the current frame-dependent update model with a time-based runtime.

Implement:

- Delta-time based update loop.
- Separation between update() and render().
- Frame time measurement.
- Reasonable delta-time clamping to avoid large frame spikes.
- A small math module containing reusable 2D vector utilities (use pygame.Vector2 or your own lightweight abstraction where appropriate).
- A reusable Transform2D data structure supporting:
  - position
  - rotation
  - scale

The Transform2D implementation should be simple and designed for future procedural rendering, not overengineered.

Future systems should be able to reuse this runtime foundation without requiring another major refactor.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 2
- Title
- Goal
- Full prompt text
- Files created
- Files modified
- Short implementation summary
- Test results
- Completion status

---

Restrictions

Do NOT:

- Change gameplay rules.
- Add multiple apples.
- Add new entities.
- Add menus.
- Add particles.
- Add procedural rendering.
- Add lighting.
- Add physics beyond delta-time movement.
- Introduce fixed timestep yet unless it can be done with almost no additional complexity.

Avoid unnecessary abstractions.

---

Acceptance Criteria

- Gameplay remains visually almost identical.
- Movement is based on elapsed time instead of frames.
- Update and rendering are clearly separated.
- Transform2D exists and is reusable.
- Runtime is prepared for future systems.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Runtime architecture decisions
- Manual verification performed
- Confirmation that gameplay behavior was intentionally preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/math2d.py`

**Files Modified:**

- `catch_the_apple/config.py`
- `catch_the_apple/entities.py`
- `catch_the_apple/game.py`
- `catch_the_apple/utils.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

The runtime was changed from frame-dependent movement to delta-time movement. The original per-frame speeds were converted to pixels-per-second values using the existing 60 FPS target so gameplay remains nearly identical. The `Game` class now has explicit `measure_delta_time`, `update`, and `render` methods. Delta time is clamped to prevent unusually large frame spikes. A small `math2d` module now provides a `pygame.Vector2` alias, `vec2`, `clamp`, and a reusable `Transform2D` dataclass with position, rotation, and scale. Basket and apple entities now store position through `Transform2D` while preserving simple `x`, `y`, and `rect` access.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Import smoke check for `main` and package modules passed without starting the game loop.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.
