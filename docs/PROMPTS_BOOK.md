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

### Prompt 3: World Model & Gameplay Systems

**Date:** 2026-08-01

**Goal:** Introduce a structured world model and dedicated gameplay systems while keeping the player-facing game functionally identical.

**Full Prompt Text:**

```text
Prompt 3 - World Model & Gameplay Systems

Context

The project now has a modular architecture and a runtime based on delta time.

This prompt introduces the core gameplay architecture that future features will build upon.

Do not add new gameplay mechanics.

The player should experience the same game as before.

---

Objectives

Replace the remaining global gameplay state with a structured world model.

Introduce clear ownership and separation between:

- Game session
- World
- Basket
- Falling object(s)
- Game rules

Represent entities using appropriate data structures (prefer dataclasses where appropriate).

Create dedicated systems responsible for:

- Input
- Movement
- Spawning
- Collision
- Scoring
- Difficulty progression

Each system should have a single responsibility.

The renderer should only render.

Game rules should not directly manipulate rendering.

The current gameplay must remain functionally identical:

- One falling apple
- One basket
- Score
- Lives
- Apple speed increases every five points

The architecture should naturally support multiple falling objects in a future prompt without implementing them now.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 3
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

- Add multiple apples.
- Add procedural graphics.
- Add particles.
- Add menus.
- Add audio.
- Change collision mathematics.
- Introduce data-driven object types yet.
- Change gameplay rules.

Avoid unnecessary abstractions and overengineering.

---

Acceptance Criteria

- Global mutable state has been eliminated or significantly reduced.
- Gameplay systems have clear responsibilities.
- Gameplay remains functionally identical.
- Architecture is ready for multiple entities in the next prompt.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Architecture decisions
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/session.py`
- `catch_the_apple/world.py`
- `catch_the_apple/systems/__init__.py`
- `catch_the_apple/systems/difficulty.py`
- `catch_the_apple/systems/game_rules.py`
- `catch_the_apple/systems/movement.py`
- `catch_the_apple/systems/scoring.py`
- `catch_the_apple/systems/spawning.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/entities.py`
- `catch_the_apple/game.py`
- `catch_the_apple/rendering.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Files Removed:**

- `catch_the_apple/utils.py`

**Short Implementation Summary:**

Session state was moved into `GameSession`, and active gameplay entities were moved into `World`. The world currently contains one basket and one falling apple, represented internally as a `falling_objects` list to prepare for future multiple-object support without adding that mechanic now. Movement, spawning, scoring, difficulty progression, and game-rule coordination were split into focused system modules. The renderer now renders a world/session snapshot and does not own gameplay rules.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Import smoke check for the runtime, world, session, and gameplay systems passed without starting the game loop.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 4: Multiple Falling Objects & Spawn System

**Date:** 2026-08-03

**Goal:** Replace the single-apple spawning implementation with a configurable, collection-based falling object management system while keeping one regular apple active for current gameplay.

**Full Prompt Text:**

```text
Prompt 4 - Multiple Falling Objects & Spawn System

Context

The project now has a modular architecture, a delta-time runtime, and a structured world model.

This prompt expands the world from a single falling object to a scalable object management system.

Do not introduce new gameplay mechanics yet.

The player should still experience essentially the same game.

---

Objectives

Replace the single-apple implementation with a generic falling object management system.

Implement:

- A world-managed collection of falling objects.
- A dedicated Spawn System.
- Object lifecycle management (spawn, update, remove/reset).
- Configurable maximum active objects.
- Deterministic random generator with an optional seed.
- Spawn parameters collected into one configuration location.

For now, configure the game so that only **one regular apple** is active at a time, preserving current gameplay.

However, the architecture should naturally support multiple simultaneous objects in future prompts without another major refactor.

The Spawn System should be responsible only for deciding when and where objects appear.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 4
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

- Add golden apples.
- Add rotten apples.
- Add bombs.
- Add power-ups.
- Change scoring rules.
- Change difficulty rules.
- Add procedural rendering.
- Add particles.
- Add menus.
- Change gameplay balance.

Avoid overengineering.

---

Acceptance Criteria

- Falling objects are managed as a collection.
- Spawn logic is isolated in its own system.
- Gameplay remains functionally identical.
- The architecture is ready for multiple object types.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Spawn architecture decisions
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- None.

**Files Modified:**

- `README.md`
- `catch_the_apple/collision.py`
- `catch_the_apple/config.py`
- `catch_the_apple/entities.py`
- `catch_the_apple/game.py`
- `catch_the_apple/systems/difficulty.py`
- `catch_the_apple/systems/game_rules.py`
- `catch_the_apple/systems/spawning.py`
- `catch_the_apple/world.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

The apple entity was generalized to `FallingObject`, and `World` now owns an initially empty collection that is populated by `SpawnSystem`. Spawn parameters are centralized in `config.SpawnConfig`, including maximum active objects, spawn bounds, spawn height, object size, object speed, and an optional random seed. `SpawnSystem` owns a dedicated `random.Random` instance, creates regular apple-like falling objects, maintains the configured active object count, and resets object positions after catches or misses. The current configuration keeps `max_active_objects` at 1, preserving the current one-apple gameplay.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Import smoke check for runtime, world, session, and spawn-related systems passed without starting the game loop.
- Seeded spawn reproducibility smoke check passed.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 5: Data-Driven Gameplay Model

**Date:** 2026-08-03

**Goal:** Introduce structured object definitions and make spawning/game rules use object data while keeping only the regular apple active in normal gameplay.

**Full Prompt Text:**

```text
Prompt 5 - Data-Driven Gameplay Model

Context

The project now supports a scalable world model and a generic spawn system.

This prompt introduces a data-driven gameplay model without significantly changing the player's experience.

Only one regular apple should still appear during normal gameplay.

---

Objectives

Replace hardcoded gameplay rules with configurable object definitions.

Introduce a data-driven object type system.

Each object type should be described by structured data rather than hardcoded conditionals.

At minimum, support the concept of:

- Regular Apple
- Golden Apple
- Rotten Apple
- Bomb
- Power-Up

Only the Regular Apple should be enabled for spawning in this prompt.

Each object definition should be capable of describing attributes such as:

- Identifier
- Display name
- Category
- Score value
- Damage
- Spawn weight
- Radius or collision size
- Colors (placeholder values are acceptable)
- Gameplay tags
- Optional future behaviors

The Spawn System should obtain object information from this registry rather than embedding gameplay rules.

The architecture should allow adding future object types by creating new data definitions instead of modifying multiple systems.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 5
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

- Spawn Golden Apples.
- Spawn Rotten Apples.
- Spawn Bombs.
- Spawn Power-Ups.
- Change gameplay balance.
- Add particles.
- Add procedural rendering.
- Add menus.
- Add audio.
- Implement special object behaviors.

Avoid unnecessary abstractions.

---

Acceptance Criteria

- Gameplay remains visually and functionally identical.
- Object definitions are data-driven.
- The Spawn System uses the object registry.
- New object types can be added without modifying core gameplay systems.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Data model decisions
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/object_definitions.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/config.py`
- `catch_the_apple/entities.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/systems/game_rules.py`
- `catch_the_apple/systems/scoring.py`
- `catch_the_apple/systems/spawning.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added an `ObjectDefinition` dataclass and registry containing regular apple, golden apple, rotten apple, bomb, and power-up definitions. `SpawnConfig` now declares enabled object IDs, with only `regular_apple` enabled. `FallingObject` instances reference their object definition, and the spawn system creates objects from weighted registry definitions instead of a hardcoded regular apple constructor. Rendering now uses the object definition color, and scoring/life loss read score and damage values from object data. The regular apple data preserves the existing red color, score value, damage, and collision size.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Import smoke check for object definitions, spawning, and game rules passed without starting the game loop.
- Spawn data smoke check confirmed the default spawned object is `regular_apple` with score value 1, damage 1, red color, and size 30.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.
