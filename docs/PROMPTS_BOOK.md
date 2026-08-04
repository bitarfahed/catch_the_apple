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

## Prompt 24 - Night Palette Fix & Golden Apple Rule

**Goal:** Narrow the night palette behavior so only regular apples change at night, and ensure missed golden apples do not reduce lives.

**Full Prompt Text:**

```text
Prompt 24 - Night Palette Fix & Golden Apple Rule

Context

Recent playtesting identified two gameplay issues.

Both should be fixed by reusing the existing systems.

Do not redesign the rendering or gameplay architecture.

---

Objectives

1. Night Palette Fix

The current day/night transition darkens the environment, but the colors of the gameplay objects remain unchanged.

Update the Night Palette behavior so that:

- During daytime, object colors remain exactly as they are today.
- During nighttime only, Regular Apples change their appearance to bright white (or a very light glowing white) to improve visibility.
- Golden Apples remain gold.
- Rotten Apples remain unchanged.
- Bombs remain unchanged.

The transition between day and night should remain smooth.

The goal is to improve gameplay readability without changing daytime visuals.

---

2. Golden Apple Gameplay Rule

Missing a Golden Apple must NOT reduce lives.

The existing gameplay rules should become:

- Missing a Regular Apple -> existing behavior.
- Missing a Golden Apple -> no life lost.
- Missing a Rotten Apple -> no life lost.
- Missing a Bomb -> no life lost.

Only collision with hazardous objects should damage the player.

Reuse the existing object-type system rather than introducing special-case logic.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Modify rendering architecture.
- Modify the lighting system.
- Change collision architecture.
- Change gameplay balance except for the rules above.

---

Acceptance Criteria

- Regular Apples become white only during nighttime.
- Daytime colors remain unchanged.
- Golden Apples no longer reduce lives when missed.
- Existing architecture is reused.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files modified
- Night palette implementation
- Gameplay rule update
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Modified:**

- `docs/GRAPHICS_AND_MATH.md`
- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/rendering.py`
- `src/catch_the_apple/systems/game_rules.py`
- `tests/test_core_systems.py`

**Night Palette Implementation:**

The environment-aware object palette now changes only regular apples. Daytime regular apples keep the configured red color, and nighttime regular apples smoothly interpolate toward light glowing white using the existing night factor. Golden apples, rotten apples, bombs, and power-ups retain their configured colors.

**Gameplay Rule Update:**

Miss damage continues to come from the object definition system. Non-hazard misses use `definition.damage`, while hazard misses apply zero miss damage. Golden apples already define `damage=0`, so missing them no longer reduces lives. A regression test now covers the golden apple miss case explicitly.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 29 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.

**Completion Status:** Complete.

## Prompt 23 - Visual Readability & Environmental Polish

**Goal:** Improve gameplay readability and environmental polish by strengthening night object identity, wind visibility, and gameplay feedback while reusing existing systems.

**Full Prompt Text:**

```text
Prompt 23 - Visual Readability & Environmental Polish

Context

The project already contains lighting, procedural rendering, weather and environmental systems.

Playtesting shows that some gameplay elements are difficult to distinguish and some environmental effects remain too subtle.

This prompt focuses on visual readability and environmental polish.

Reuse existing systems.

---

Objectives

Improve gameplay readability.

1. Night Palette

Create a dedicated night color palette.

Do not simply darken the screen.

At minimum:

- Regular Apple -> glowing white or light cyan
- Golden Apple -> bright glowing gold
- Bomb -> dark red with red glow
- Rotten Apple -> dark green or purple

The objective is immediate visual recognition.

---

2. Wind

Strengthen the Wind System.

Wind should continuously influence object trajectories through the existing physics model.

Movement should feel physically natural rather than artificially displaced.

---

3. Gameplay Visibility

Ensure every important gameplay feature clearly communicates itself visually.

Examples include:

- Wind changes
- Day/Night transitions
- Magnet activation
- Time Warp
- Apple Storm
- Super Power activation

Players should immediately understand what is happening without reading instructions.

---

4. Guiding Principle

Every gameplay feature should satisfy all three:

- Gameplay value
- Clear visual feedback
- Demonstrable mathematical or algorithmic model

Avoid purely cosmetic effects that provide no engineering or gameplay value.

---

Documentation

Update GRAPHICS_AND_MATH.md where necessary to reflect new mathematical models or visual techniques.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Add new gameplay mechanics.
- Rewrite rendering architecture.
- Replace existing systems.

Focus on improving the quality of existing features.

---

Acceptance Criteria

- Night palette greatly improves readability.
- Wind influence is clearly visible.
- Gameplay events are visually obvious.
- Existing systems are reused.
- GRAPHICS_AND_MATH.md updated.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Visual design decisions
- Gameplay readability improvements
- Documentation updates
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:** None.

**Files Modified:**

- `docs/GRAPHICS_AND_MATH.md`
- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/difficulty_profiles.py`
- `src/catch_the_apple/dynamic_environment.py`
- `src/catch_the_apple/procedural_assets.py`
- `src/catch_the_apple/rendering.py`
- `src/catch_the_apple/ui.py`
- `tests/test_core_systems.py`

**Visual Design Decisions:**

Added an environment-aware object palette that interpolates objects toward dedicated night colors instead of simply darkening the entire screen. Regular apples become light cyan, golden apples become bright gold, bombs become dark red, rotten apples become deep purple, and power-ups become bright cyan. Cached glow surfaces now reinforce important object identity, especially at night and during active powers.

The day/night cycle now uses a more distinct night sky palette and stronger ambient, directional, and shadow contrast. The HUD now includes day/night status and a wind vector indicator so environmental changes are visible during play.

**Gameplay Readability Improvements:**

Wind influence was strengthened by increasing profile gameplay wind scales and the existing wind response value. Falling objects still move through the smoothed wind-velocity model, so trajectories curve continuously instead of jumping sideways.

Super Power feedback continues to use HUD banners and active-power labels, with object glows becoming stronger during Magnet and Time Warp states.

**Documentation Updates:**

`docs/GRAPHICS_AND_MATH.md` now documents the night palette interpolation formula and the eased wind-velocity update model.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 28 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.

**Completion Status:** Complete.

## Prompt 22 - Super Powers Framework

**Goal:** Activate the existing gameplay, rendering, physics, particles, weather, lighting, and UI infrastructure through a reusable Super Power framework with gameplay, visual, and mathematical dimensions.

**Full Prompt Text:**

```text
Prompt 22 - Super Powers Framework

Context

The project already contains the gameplay, rendering, physics, particles, weather, lighting and UI infrastructure.

This prompt focuses on activating these systems through a reusable Super Power framework.

Do not redesign the architecture.

Reuse existing systems whenever possible.

---

Objectives

Implement a generic Super Power framework.

Every Super Power MUST include three equally important aspects:

1. Gameplay
2. Visual Effect
3. Mathematical Model

The mathematical model should be meaningful and suitable for explanation in the project documentation.

Implement or integrate support for powers such as:

- Magnet
- Time Warp
- Dash Boost
- Wind Control
- Shockwave
- Black Hole
- Gravity Control
- Golden Rain
- Freeze Bombs

Reuse existing gameplay systems whenever possible.

---

Gameplay Synergy

Power-ups should actively cooperate with other gameplay systems.

Examples:

- Magnet -> automatically triggers an Apple Storm for approximately 15 seconds.
- Wind Control -> temporarily modifies the Wind System.
- Time Warp -> modifies the simulation time.
- Freeze Bombs -> temporarily freezes only hazardous objects.

The objective is to create memorable gameplay rather than isolated abilities.

---

Developer Cheat Console

Implement a Developer Cheat Console.

Workflow:

Pause
-> Developer Console
-> Enter Cheat Code
-> Resume Game

Do NOT allow typing during normal gameplay.

The console is intended for:

- Demonstrations
- Debugging
- Testing
- Portfolio presentation

Document every cheat code in README.md.

---

Documentation

Update GRAPHICS_AND_MATH.md.

For every Super Power explain:

- Mathematical idea
- Algorithms or formulas involved
- Gameplay effect
- Visual representation

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Rewrite architecture.
- Introduce unnecessary abstractions.
- Replace existing systems.

Build upon the current implementation.

---

Acceptance Criteria

- Generic Super Power framework implemented.
- Developer Cheat Console implemented.
- Gameplay synergy implemented.
- Mathematical documentation added.
- Cheat codes documented.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Super Power architecture
- Cheat Console implementation
- Documentation added
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `src/catch_the_apple/developer_console.py`
- `src/catch_the_apple/superpowers.py`

**Files Modified:**

- `README.md`
- `docs/GRAPHICS_AND_MATH.md`
- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/game.py`
- `src/catch_the_apple/input.py`
- `src/catch_the_apple/powerups.py`
- `src/catch_the_apple/states.py`
- `src/catch_the_apple/systems/movement.py`
- `src/catch_the_apple/systems/spawning.py`
- `src/catch_the_apple/ui.py`
- `tests/test_core_systems.py`

**Short Implementation Summary:**

Added a generic Super Power registry and active-state system covering Magnet, Time Warp, Dash Boost, Wind Control, Shockwave, Black Hole, Gravity Control, Golden Rain, and Freeze Bombs. Existing power-up imports now route through the Super Power framework for compatibility. Gameplay systems reuse the active power state to adjust simulation time, wind influence, falling-object motion, spawn weights, magnet pull, black-hole pull, and shockwave forces.

Added a pause-only Developer Cheat Console. The console accepts documented cheat codes, activates matching powers, and keeps normal gameplay typing disabled.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 27 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- Manual dummy-video smoke test confirmed Pause -> Developer Console -> enter `void` -> activate Black Hole -> resume.

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

### Prompt 6: Basket Physics & Advanced Movement

**Date:** 2026-08-03

**Goal:** Replace direct basket position changes with velocity-based movement, acceleration, drag, boundary constraints, and a configurable dash while keeping gameplay stable.

**Full Prompt Text:**

```text
Prompt 6 - Basket Physics & Advanced Movement

Context

The project now has a modular architecture, a delta-time runtime, scalable world management, a spawn system, and a data-driven gameplay model.

This prompt upgrades the player's movement system from simple position changes to a proper movement model.

The game should still feel familiar, but movement should become smoother and provide a stronger foundation for future gameplay.

---

Objectives

Replace the basket's direct position updates with a velocity-based movement system.

Implement:

- Position
- Velocity
- Acceleration
- Configurable maximum speed
- Configurable acceleration
- Configurable deceleration / drag
- Screen boundary constraints

Add a dash mechanic.

The dash should include:

- Configurable dash speed
- Dash duration
- Dash cooldown
- Clear separation between normal movement and dash movement

Prepare the movement system for future visual effects by exposing:

- Current velocity
- Current movement direction
- Current speed

These values will later be used by animation and rendering systems.

Movement tuning should prioritize responsiveness while remaining physically consistent.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 6
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

- Add visual dash effects.
- Add particles.
- Add squash/stretch.
- Add camera shake.
- Add motion trails.
- Change collision behavior.
- Change gameplay scoring.
- Change spawn behavior.
- Add new object types.

Avoid overengineering.

---

Acceptance Criteria

- Basket movement is fully velocity-based.
- Movement uses acceleration and drag.
- Dash works with configurable duration and cooldown.
- Movement remains responsive.
- Future rendering systems can access movement state.
- Gameplay remains stable.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Movement architecture decisions
- Dash implementation summary
- Manual verification performed
- Confirmation that gameplay remains stable
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- None.

**Files Modified:**

- `README.md`
- `catch_the_apple/config.py`
- `catch_the_apple/entities.py`
- `catch_the_apple/input.py`
- `catch_the_apple/systems/movement.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added `MovementState` to the basket with velocity, acceleration, movement direction, dash timers, and exposed current speed. Basket movement now applies acceleration while input is held, drag when input is released, clamps velocity to a configured maximum speed, integrates position with delta time, and enforces screen boundaries. Space triggers a dash using separate dash speed, duration, and cooldown settings. Falling object movement, collision, scoring, spawning, and object definitions were not changed.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Focused movement smoke checks confirmed acceleration, drag, dash speed/cooldown, and boundary clamping behavior.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 7: Collision System & Continuous Collision Detection

**Date:** 2026-08-03

**Goal:** Replace simple rectangle collision with a reusable collision subsystem using circular falling-object shapes, a composite basket model, continuous collision checks, and a toggleable debug overlay.

**Full Prompt Text:**

```text
Prompt 7 - Collision System & Continuous Collision Detection

Context

The project now has a modular architecture, a delta-time runtime, structured world management, data-driven object definitions, and advanced basket movement.

This prompt upgrades the collision system into a reusable gameplay subsystem.

The current gameplay should remain almost identical.

---

Objectives

Replace the current simple collision implementation with a reusable collision framework.

Implement support for:

- Circle collision shapes for falling objects.
- A composite basket collision model consisting of:
  - Catch region
  - Left rim
  - Right rim
  - Basket body

Introduce Continuous Collision Detection (CCD) to prevent fast-moving objects from tunneling through the basket.

Each falling object should keep both its previous and current position.

The collision system should determine interactions using the swept movement between frames when appropriate.

Prepare the system so additional collision shapes can be added later without another major refactor.

Create a Debug Collision Overlay that can be toggled on/off and visualizes:

- Collision boundaries
- Catch region
- Object collision circles
- Swept movement path (optional if simple to implement)

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 7
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
- Add bouncing physics.
- Add object responses.
- Add particles.
- Add camera shake.
- Add procedural rendering.
- Add lighting.
- Add new object types.

Keep the collision system focused and reusable.

---

Acceptance Criteria

- Collision logic is isolated in its own subsystem.
- Falling objects use circular collision.
- Basket uses a composite collision model.
- Continuous Collision Detection prevents tunneling.
- Debug collision overlay is available.
- Gameplay remains stable.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Collision architecture decisions
- CCD implementation summary
- Manual verification performed
- Confirmation that gameplay behavior remains stable
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
- `catch_the_apple/input.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/session.py`
- `catch_the_apple/systems/game_rules.py`
- `catch_the_apple/systems/movement.py`
- `catch_the_apple/systems/spawning.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Replaced the old rectangle-only collision helper with a collision subsystem containing circle shapes, a composite basket collision model, structured collision results, circle-vs-rectangle checks, and swept circle checks against the basket catch region. Falling objects now track previous position before movement and reset that history when respawned. The basket exposes catch, rim, and body regions for collision/debug use. F1 toggles a debug overlay that draws basket regions, falling object circles, and swept movement paths.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Focused collision smoke checks confirmed composite region construction, direct catch detection, and CCD catch detection for a tunneling movement path.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 8: Procedural Asset Rendering

**Date:** 2026-08-03

**Goal:** Replace rectangle-based basket and apple drawing with cached procedural graphics while preserving gameplay, collision, and physics behavior.

**Full Prompt Text:**

```text
Prompt 8 - Procedural Asset Rendering

Context

The project now has a solid gameplay architecture.

This prompt begins replacing placeholder graphics with procedurally generated visuals.

The objective is to improve rendering quality while keeping gameplay unchanged.

---

Objectives

Replace the rectangle-based rendering of the basket and apple with procedurally generated graphics.

Implement:

- A Procedural Apple Renderer.
- A Procedural Basket Renderer.

The procedural apple should be composed from simple geometric primitives and include:

- Apple body
- Stem
- Leaf
- Soft shading
- Highlight
- Optional subtle color variation

The procedural basket should include:

- Basket body
- Rim
- Simple woven pattern
- Basic shading

Rendering should use cached `pygame.Surface` objects.

Generate surfaces only when needed (for example, when size or appearance changes), never every frame.

The renderer should expose a clean API so future lighting and animation systems can reuse these assets.

Gameplay, collision, and physics must remain unchanged.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 8
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

- Add lighting.
- Add shadows.
- Add particles.
- Add squash/stretch.
- Add animation.
- Add image assets (PNG files).
- Change gameplay.
- Change collision.
- Add NumPy unless it provides a clear benefit.

Avoid per-frame surface generation.

---

Acceptance Criteria

- Apples are rendered procedurally.
- Basket is rendered procedurally.
- Rendering uses cached surfaces.
- No external image assets are required.
- Gameplay remains unchanged.
- Renderer is ready for future lighting.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Rendering architecture decisions
- Surface caching strategy
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/procedural_assets.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/rendering.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added `ProceduralAppleRenderer`, `ProceduralBasketRenderer`, and `ProceduralAssetRenderer`. Apples are now rendered from Pygame primitives with a body, stem, leaf, shading, and highlight. The basket is rendered from primitives with a body, rim, woven pattern, and basic shading. The main renderer now blits cached procedural surfaces at the existing entity rectangles instead of drawing placeholder rectangles. Debug collision overlay rendering remains available and is drawn over the procedural visuals when enabled.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Procedural surface smoke check confirmed apple and basket surface sizes and cache reuse.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 9: 2D Lighting & Shadow Pipeline

**Date:** 2026-08-03

**Goal:** Add a lightweight reusable 2D lighting and shadow pipeline for procedurally rendered assets while preserving gameplay behavior.

**Full Prompt Text:**

```text
Prompt 9 - 2D Lighting & Shadow Pipeline

Context

The project now renders procedural apples and baskets using cached surfaces.

This prompt introduces a lightweight 2D lighting pipeline that enhances visual quality without becoming a full rendering engine.

Gameplay must remain unchanged.

---

Objectives

Implement a reusable 2D lighting system suitable for procedurally rendered objects.

Implement:

- Ambient lighting
- One directional light source
- Diffuse shading
- Simple specular highlights
- Ground shadows beneath falling objects

The lighting system should operate on procedurally generated assets and reuse cached rendering whenever practical.

Ground shadows should respond to:

- Object height
- Light direction
- Light intensity

Shadows should appear soft and visually convincing while remaining computationally inexpensive.

The lighting implementation should expose a clean API so future systems (day/night cycle and weather) can control lighting parameters without modifying the renderer.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 9
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

- Implement a full pixel-by-pixel lighting engine.
- Use expensive per-frame Python pixel loops.
- Add particles.
- Add weather.
- Add day/night cycle.
- Add post-processing.
- Change gameplay.
- Change collision or physics.

Prefer cached surfaces, precomputed shading, or efficient rendering techniques.

---

Acceptance Criteria

- Procedural assets support lighting.
- Ambient and directional lighting are implemented.
- Objects cast convincing ground shadows.
- Lighting parameters are reusable by future systems.
- Rendering performance remains stable.
- Gameplay remains unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Lighting architecture decisions
- Shadow implementation strategy
- Performance considerations
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/lighting.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/rendering.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added `LightingConfig`, `DirectionalLight`, and `LightingSystem`. The renderer now applies cached ambient/directional lighting to procedural basket and falling-object surfaces, including simple diffuse and specular overlays. Falling objects also draw soft ground shadows whose size, offset, and opacity respond to estimated object height, directional light vector, and light intensity. Gameplay, collision, physics, spawning, and scoring were not changed.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Lighting smoke check confirmed lit surface generation, shadow generation, and cache reuse.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 10: Generic Particle System & Gameplay Effects

**Date:** 2026-08-03

**Goal:** Introduce a reusable, data-driven particle and lightweight animation system for gameplay effects while preserving gameplay rules.

**Full Prompt Text:**

```text
Prompt 10 - Generic Particle System & Gameplay Effects

Context

The project now has procedural rendering and a lightweight 2D lighting pipeline.

This prompt introduces a reusable particle system that will become the foundation for all visual gameplay effects.

The focus is architecture first, visual polish second.

Gameplay rules must remain unchanged.

---

Objectives

Implement a generic, data-driven particle system.

The particle system should support:

- Position
- Velocity
- Acceleration
- Rotation
- Angular velocity
- Lifetime
- Age
- Start and end size
- Start and end alpha
- Start and end color
- Drag
- Gravity scale

Implement configurable particle emitters.

Different visual effects should be created by emitter configuration rather than by creating separate particle classes.

Create the following gameplay effects using the generic system:

- Apple catch burst
- Golden sparkle effect (infrastructure only; no Golden Apples yet)
- Bomb smoke effect (infrastructure only; no Bombs yet)
- Motion trails for fast-moving objects
- Basket dash trail
- Simple squash & stretch animation for:
  - Basket movement
  - Apple catch

Squash & Stretch should be implemented as reusable animation components rather than special-case rendering code.

The renderer should remain responsible only for drawing particles.

Particle simulation should remain independent from gameplay logic.

Use object pooling where appropriate to reduce runtime allocations.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 10
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
- Spawn Golden Apples.
- Spawn Bombs.
- Add weather particles.
- Add environmental particles.
- Add post-processing.
- Add camera shake.
- Add audio.

Keep the particle system generic and reusable.

Avoid per-frame allocations whenever practical.

---

Acceptance Criteria

- A reusable particle engine exists.
- Particle emitters are data-driven.
- Gameplay effects reuse the generic system.
- Motion trails are implemented.
- Squash & Stretch is reusable.
- Object pooling is used where beneficial.
- Gameplay remains unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Particle architecture decisions
- Pooling strategy
- Performance considerations
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/animation.py`
- `catch_the_apple/effects.py`
- `catch_the_apple/events.py`
- `catch_the_apple/particles.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/game.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/systems/game_rules.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added a generic pooled particle engine with configurable particle data and emitter definitions. Added reusable squash/stretch animation components. Gameplay rules now return lightweight gameplay events rather than directly knowing about effects. `VisualEffects` consumes events, emits apple catch bursts, provides golden sparkle and bomb smoke emitter infrastructure, emits motion trails for fast falling objects, emits basket dash trails, and manages reusable squash/stretch state for basket movement and apple catches. The renderer draws particles and applies animation scales, while particle simulation remains outside gameplay logic.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Particle smoke check confirmed pooled emission and update behavior.
- Catch event smoke check confirmed apple catch burst emission and squash/stretch activation.
- Particle render cache smoke check confirmed cached particle drawing surfaces.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 11: Procedural Environment & Parallax

**Date:** 2026-08-03

**Goal:** Add a fully procedural, cached, multi-layer parallax environment behind gameplay without changing mechanics.

**Full Prompt Text:**

```text
Prompt 11 - Procedural Environment & Parallax

Context

The project now features a modular gameplay architecture, procedural object rendering, lighting, and a generic particle system.

This prompt upgrades the visual environment surrounding the gameplay.

The objective is to create depth and atmosphere without affecting gameplay mechanics.

---

Objectives

Implement a procedural environment renderer.

Create multiple background layers such as:

- Sky
- Distant mountains
- Trees
- Bushes
- Foreground grass

All layers should be procedurally generated.

Implement a parallax system where each layer moves according to its own depth factor.

Implement a procedural sky with:

- Vertical color gradient
- Procedural clouds
- Lightweight value noise (or a similarly simple noise technique)

Cache generated surfaces whenever practical.

The environment renderer should be completely independent from gameplay systems.

Design the renderer so future weather and day/night systems can modify the environment without requiring another major refactor.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 11
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

- Add weather.
- Add wind.
- Add day/night cycle.
- Change gameplay.
- Add camera movement.
- Add post-processing.
- Load external background images.

Keep the environment lightweight and performant.

---

Acceptance Criteria

- Environment is fully procedural.
- Multiple parallax layers are implemented.
- Sky uses a procedural gradient.
- Clouds are procedurally generated.
- Generated assets are cached.
- Gameplay remains unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Environment architecture decisions
- Caching strategy
- Performance considerations
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/environment.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/game.py`
- `catch_the_apple/rendering.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added `ProceduralEnvironmentRenderer` and `EnvironmentLayer`. The renderer procedurally generates cached layers for sky, procedural clouds, distant mountains, trees, bushes, and foreground grass. The sky uses a vertical color gradient and deterministic cloud generation. Each layer has its own depth factor and scroll speed, producing lightweight time-based parallax independent of gameplay state. The main renderer now draws the environment before gameplay objects, effects, debug overlays, and HUD.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Environment smoke check confirmed five cached layers and successful dummy-display rendering.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 12: Dynamic Environment

**Date:** 2026-08-03

**Goal:** Add modular wind, weather presets, and smooth day/night environment state coordinated by a central environment manager while preserving gameplay.

**Full Prompt Text:**

```text
Prompt 12 - Dynamic Environment

Context

The project now includes a procedural environment with layered parallax backgrounds and procedurally generated scenery.

This prompt brings the environment to life by introducing dynamic environmental systems.

The objective is to improve atmosphere and visual quality while keeping gameplay fair and readable.

---

Objectives

Implement three integrated environmental systems:

1. Wind System
- Create a reusable wind model with configurable direction, strength, and gusts.
- Wind should gently influence falling objects and compatible particle emitters.
- The current wind state should be available to future gameplay systems.

2. Weather System
Implement configurable weather presets such as:
- Clear
- Light Wind
- Strong Wind
- Rain
- Falling Leaves
- Fog

Weather should primarily affect visuals.
Gameplay influence should remain subtle and configurable.

3. Day/Night Cycle
Implement a smooth day/night cycle affecting:
- Sky colors
- Ambient light
- Directional light intensity
- Sun/moon position
- Background colors
- Shadow intensity

Transitions should be continuous and time-based.

Design these systems so they are independent, configurable, and controlled through a central Environment Manager.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 12
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

- Change scoring.
- Change collision.
- Add new gameplay mechanics.
- Add new object types.
- Add post-processing.
- Add menus.
- Add audio.

Keep all environmental systems modular and efficient.

---

Acceptance Criteria

- Wind system implemented.
- Weather presets implemented.
- Smooth day/night cycle implemented.
- Environment Manager coordinates all environmental systems.
- Gameplay remains stable and fair.
- Rendering performance remains acceptable.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Environment architecture decisions
- Performance considerations
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/dynamic_environment.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/effects.py`
- `catch_the_apple/environment.py`
- `catch_the_apple/game.py`
- `catch_the_apple/lighting.py`
- `catch_the_apple/particles.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/systems/movement.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added a central `EnvironmentManager` coordinating `WindSystem`, configurable weather presets, and a continuous `DayNightCycle`. Weather presets include clear, light wind, strong wind, rain, falling leaves, and fog. Wind exposes current direction, strength, and velocity, with configurable gusts. Falling objects receive only subtle configurable wind drift, while particles receive stronger visual wind. Day/night state updates sky colors, ambient lighting, directional light intensity, sun/moon positions, and shadow intensity. The procedural environment renderer now consumes environment state for dynamic sky tinting, fog, sun/moon drawing, and wind-influenced parallax.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Environment manager smoke check confirmed six weather presets, wind updates, lighting changes, and weather switching.
- Environment rendering smoke check confirmed fog preset rendering with cached procedural layers.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 13: Game Flow, States & User Interface

**Date:** 2026-08-03

**Goal:** Add reusable state management, main menu, pause, game-over flow, smooth transitions, and a modular animated HUD while preserving gameplay rules.

**Full Prompt Text:**

```text
Prompt 13 - Game Flow, States & User Interface

Context

The project now has a complete gameplay architecture, procedural rendering, lighting, particles, and a dynamic environment.

This prompt focuses on the player experience by introducing proper game flow and a polished user interface.

The gameplay itself should remain unchanged.

---

Objectives

Implement a reusable State Management system.

At minimum support:

- Main Menu
- Playing
- Paused
- Game Over

The state system should isolate update, input, and rendering logic for each state.

Implement smooth transitions between states (fade or similar lightweight animation).

Implement a polished HUD displaying:

- Score
- Lives
- Current combo
- Dash cooldown/availability
- Active environmental state (optional)
- Pause indicator

Improve player feedback with subtle UI animations such as:

- Score pop animation
- Combo pulse
- Life loss animation
- Dash cooldown feedback

Design the UI so future gameplay features can expose information without modifying the core HUD architecture.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 13
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
- Add new object types.
- Add audio.
- Add persistence.
- Add post-processing.
- Change physics or collision.

Keep the state system lightweight and modular.

---

Acceptance Criteria

- State management implemented.
- Main Menu, Playing, Pause and Game Over states work correctly.
- HUD is modular and polished.
- UI animations are lightweight and responsive.
- Gameplay behavior remains unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- State management architecture
- UI architecture decisions
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/states.py`
- `catch_the_apple/ui.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/events.py`
- `catch_the_apple/game.py`
- `catch_the_apple/input.py`
- `catch_the_apple/rendering.py`
- `catch_the_apple/session.py`
- `catch_the_apple/systems/game_rules.py`
- `catch_the_apple/systems/scoring.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added a lightweight `StateManager` with main menu, playing, paused, and game-over states. Each state owns its input handling, update behavior, and rendering path. The previous gameplay loop now lives in `Game.update_playing`, used only by the playing state. Added fade transitions between states. Added a reusable `UI` layer for main menu, pause overlay, game-over overlay, and HUD rendering. HUD now displays score, lives, combo, dash cooldown/availability, and active weather. UI animations respond to gameplay events with score pop, combo pulse, and life-loss flash feedback.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- State smoke check confirmed main menu, start, pause, resume, game-over restart, and session reset paths.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

### Prompt 14: Audio, Persistence & Developer Tools

**Date:** 2026-08-03

**Goal:** Add modular audio infrastructure, local persistence, settings storage, session statistics, and a runtime debug overlay without changing gameplay.

**Full Prompt Text:**

```text
Prompt 14 - Audio, Persistence & Developer Tools

Context

The project now has a complete gameplay architecture, procedural rendering, dynamic environments, game states, and a polished user interface.

This prompt focuses on usability, persistence, debugging, and developer experience.

No gameplay mechanics should change.

---

Objectives

Implement an Audio System with clear separation between:

- Music
- Sound effects
- UI sounds
- Ambient sounds

Add configurable volume controls:

- Master volume
- Music volume
- Effects volume
- Mute

Implement local persistence for:

- High score
- Settings
- Best combo
- Session statistics

Loading should be robust against missing or corrupted save files.

Implement a Debug Overlay that can be toggled during gameplay.

The overlay should display useful runtime information such as:

- FPS
- Frame time
- Active objects
- Particle count
- Current game state
- Current weather
- Wind information
- Collision visualization status
- Debug information useful for future development

Keep all developer tools isolated from gameplay logic.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 14
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
- Modify physics.
- Modify collision.
- Add new gameplay features.
- Add performance optimizations beyond obvious low-risk improvements.

Keep all systems modular.

---

Acceptance Criteria

- Audio system implemented.
- Volume settings persist.
- High scores and settings persist locally.
- Debug overlay can be toggled.
- Corrupted save files are handled gracefully.
- Gameplay behavior remains unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Audio architecture
- Persistence strategy
- Debug architecture
- Manual verification performed
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `catch_the_apple/audio.py`
- `catch_the_apple/debug.py`
- `catch_the_apple/persistence.py`

**Files Modified:**

- `README.md`
- `catch_the_apple/game.py`
- `catch_the_apple/input.py`
- `catch_the_apple/session.py`
- `catch_the_apple/states.py`
- `catch_the_apple/systems/scoring.py`
- `catch_the_apple/ui.py`
- `docs/ARCHITECTURE.md`
- `docs/PROMPTS_BOOK.md`

**Short Implementation Summary:**

Added `AudioSystem` and `AudioSettings` with separate registries for music, sound effects, UI sounds, and ambient sounds. Added master, music, effects, and mute settings with runtime controls for mute and master volume. Added `PersistenceStore` with robust JSON loading for high score, best combo, audio settings, and session statistics. Added `DebugSnapshot` and an F2-toggleable debug overlay showing FPS, frame time, active objects, particle count, state, weather, wind, collision visualization status, and audio state. Developer tools remain outside gameplay rules.

**Test Results:**

- `python -m compileall main.py catch_the_apple` passed.
- Corrupted save smoke check confirmed safe fallback to default save data.
- Settings persistence smoke check confirmed volume/mute settings save and reload.
- Session persistence smoke check confirmed high score, best combo, sessions played, and total score save correctly.
- Debug snapshot smoke check confirmed state, object count, and FPS data are available.
- Pygame launch smoke check passed using the dummy video driver with an automatic quit event.

**Completion Status:** Complete.

## Prompt 15 - Final Quality Pass, Testing & Portfolio Release

**Goal:** Polish the feature-complete project for portfolio release by adding core automated tests, cleaning release documentation, and recording final architecture, performance, and limitation notes without adding gameplay features.

**Full Prompt Text:**

```text
Prompt 15 - Final Quality Pass, Testing & Portfolio Release

Context

The project has now reached feature completion.

This final prompt is dedicated to improving quality, reliability, maintainability, and presentation.

No major gameplay features should be added.

Focus on polishing the existing project into a portfolio-quality release.

---

Objectives

Perform a complete project review.

Implement or improve:

- Automated tests for core gameplay logic and mathematical systems.
- Headless test execution where practical.
- Code cleanup and removal of dead code.
- Final architectural consistency review.
- Type hints where missing.
- Documentation improvements.
- Installation instructions.
- Controls documentation.
- Project structure documentation.
- Architecture documentation.
- Graphics and mathematics documentation.
- Performance notes.
- Known limitations.
- Future work section.

Review the entire repository for:

- Code duplication.
- Unnecessary abstractions.
- Tight coupling.
- Performance bottlenecks.
- Readability improvements.
- API consistency.
- Naming consistency.

Only optimize code where measurable or clearly beneficial.

Ensure the repository is suitable for public release.

---

PROMPTS_BOOK

Append this prompt to `docs/PROMPTS_BOOK.md`.

Include:

- Prompt Number: 15
- Title
- Goal
- Full prompt text
- Files created
- Files modified
- Final implementation summary
- Test results
- Final architecture notes
- Completion status

---

Restrictions

Do NOT:

- Add new gameplay mechanics.
- Redesign major systems.
- Introduce unnecessary optimizations.
- Expand project scope.

Prefer stability over additional features.

---

Acceptance Criteria

- Core systems are tested.
- Documentation is complete.
- Repository is clean and consistent.
- Public GitHub presentation is polished.
- PROMPTS_BOOK contains the complete development history.
- The project is ready for portfolio presentation and public release.

---

Required Response

Report:

- Files created
- Files modified
- Testing summary
- Documentation summary
- Final architecture review
- Performance review
- Remaining known limitations
- Confirmation that the repository is ready for public release
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `docs/GRAPHICS_AND_MATH.md`
- `requirements.txt`
- `tests/__init__.py`
- `tests/test_core_systems.py`

**Files Modified:**

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/PROMPTS_BOOK.md`
- `pyproject.toml`

**Final Implementation Summary:**

Added a focused headless `unittest` suite for math helpers, transforms, object definitions, deterministic spawning, basket movement and dash state, scoring and miss rules, continuous collision detection, pooled particles, persistence recovery/save behavior, environment state, procedural rendering cache behavior, lighting cache behavior, and environment layer caching. Refreshed public documentation with installation instructions, controls, testing instructions, project structure, save data notes, known limitations, future work, and a dedicated graphics and mathematics overview. Updated project metadata description from the scaffold placeholder.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 12 tests.
- `.venv\Scripts\python.exe -m compileall catch_the_apple tests` passed.
- `.venv\Scripts\python.exe -c "import main; import catch_the_apple; import catch_the_apple.app; print('import smoke ok')"` passed.

**Final Architecture Notes:**

The repository now has a coherent package layout with clear ownership across runtime, state flow, session/world data, gameplay systems, collision, procedural rendering, lighting, environment, effects, audio, persistence, UI, and debug tools. The architecture remains appropriately scoped to a 2D Pygame game and avoids a broad engine abstraction. The best-preserved foundations are the thin entry point, delta-time update/render split, data-driven object registry, composite collision model, cached procedural surfaces, pooled particle system, environment manager, and isolated developer tooling.

**Completion Status:** Complete.

## Prompt 16 - Professional Architecture Compliance

**Goal:** Align the feature-complete standalone Python/Pygame application with the project's adopted professional software engineering guidelines while preserving gameplay.

**Full Prompt Text:**

```text
Prompt 16 - Professional Architecture Compliance

Context

The project is feature complete and portfolio-ready.

This prompt aligns the repository with the professional software engineering guidelines adopted for this project.

Only adopt requirements that are relevant to a standalone Python/Pygame application.

Do not force enterprise patterns that do not fit this project.

---

Objectives

Refactor the repository to better comply with the adopted software engineering guidelines.

Implement or improve, where appropriate:

- Professional `src/` project layout.
- SDK architecture as the single public entry point for business logic.
- Thin launcher (`main.py`) that delegates to the SDK.
- Package organization using `**init**.py`.
- Project version management.
- Complete documentation structure (`README`, `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`).
- Dedicated PRDs for major mechanisms (Rendering, Collision, Particle System, Environment, etc.).
- Configuration separation.
- Type hints.
- Comprehensive docstrings.
- File-size compliance (split files exceeding ~150 LOC where practical).
- Ruff compliance.
- uv-based workflows.
- Repository consistency.

The SDK should become the primary interface for launching and controlling the game.

Future tools, tests or external applications should interact with the SDK rather than internal modules.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Add new gameplay.
- Change game balance.
- Add unnecessary enterprise infrastructure.
- Introduce APIs or networking.
- Add database support.

Adopt only architecture that clearly improves maintainability.

---

Acceptance Criteria

- SDK architecture implemented.
- Launcher delegates to SDK.
- Repository follows professional package structure.
- Documentation complies with the adopted guidelines.
- Gameplay remains unchanged.

---

Required Response

Report:

- Files created
- Files modified
- SDK architecture decisions
- Documentation improvements
- Compliance improvements
- Confirmation that gameplay behavior was preserved
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `.gitignore`
- `docs/PLAN.md`
- `docs/PRD.md`
- `docs/TODO.md`
- `docs/prds/COLLISION_PRD.md`
- `docs/prds/ENVIRONMENT_PRD.md`
- `docs/prds/PARTICLE_SYSTEM_PRD.md`
- `docs/prds/RENDERING_PRD.md`
- `src/catch_the_apple/_version.py`
- `src/catch_the_apple/sdk.py`

**Files Modified:**

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/DEVELOPMENT.md`
- `docs/PROMPTS_BOOK.md`
- `docs/ROADMAP.md`
- `main.py`
- `pyproject.toml`
- `requirements.txt`
- `tests/test_core_systems.py`

**Files Moved:**

- `catch_the_apple/` moved to `src/catch_the_apple/`

**SDK Architecture Decisions:**

Added `catch_the_apple.sdk` as the supported public integration surface. The package root now exports `GameSDK`, `GameRunConfig`, `create_game`, `run_game`, `get_version`, `main`, and `__version__`. `main.py`, `catch_the_apple.__main__`, and the compatibility `app.py` facade all delegate to the SDK. Internal modules remain available to the package, but future external tools should use the SDK boundary.

**Documentation Improvements:**

Added product, plan, TODO, and mechanism-specific PRD documents. Updated README, architecture, development, and roadmap docs for the `src/` layout, SDK launch surface, uv/Ruff workflow, package metadata, and current compliance posture.

**Compliance Improvements:**

Adopted `src/` layout, package discovery metadata, console-script metadata, version module, public SDK facade, `.gitignore`, Ruff configuration, dev dependency group, and version-sync test coverage. Large rendering/environment modules were left intact because splitting them during this prompt would be a broader redesign with little immediate gameplay or maintainability payoff.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 14 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- `.venv\Scripts\python.exe -c "import main; print('main import ok')"` passed.
- Dummy-video SDK launch smoke check passed.
- Ruff could not be executed because the local `uv.exe` launcher failed before spawning commands and Ruff is not installed in the current virtual environment. Ruff configuration and a uv dev dependency group were added for the intended workflow.

**Completion Status:** Complete.

## Prompt 17 - Final Compliance Audit

**Goal:** Perform a final engineering compliance audit against the adopted software project guidelines and identify any remaining issues without expanding scope or changing gameplay.

**Full Prompt Text:**

```text
Prompt 17 - Final Compliance Audit

Context

The project is now considered complete.

Perform one final engineering review against the adopted software project guidelines.

This is a quality and compliance audit, not a feature-development prompt.

---

Objectives

Audit the entire repository.

Evaluate compliance with the adopted software engineering guidelines.

Verify:

- Repository structure
- SDK architecture
- Documentation quality
- README completeness
- PRD / PLAN / TODO
- Dedicated mechanism documentation
- Prompt Book completeness
- Modular architecture
- Separation of responsibilities
- Type hints
- Docstrings
- File-size guideline
- Ruff compliance
- Test quality
- Coverage
- uv workflow
- Package organization
- Version management
- Public GitHub readiness

Produce a detailed compliance report.

For every guideline indicate one of:

- Fully Compliant
- Partially Compliant
- Not Applicable
- Not Implemented

For every partial or failed item explain why.

Do not implement new features unless a very small change is required to satisfy an existing guideline.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Expand project scope.
- Add new gameplay.
- Perform large refactors.
- Rewrite completed systems unless absolutely necessary.

---

Acceptance Criteria

- Complete compliance audit produced.
- Remaining issues identified.
- Repository ready for public release.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Compliance summary
- Remaining recommendations
- Known limitations
- Final architectural assessment
- Portfolio readiness assessment
- Confirmation that PROMPTS_BOOK was updated
```

**Audit Summary:**

The repository is ready for public portfolio release. The strongest compliance areas are project structure, SDK launch architecture, modular subsystem ownership, documentation structure, test coverage for core systems, package metadata, and version management. Remaining partials are limited to Ruff execution in the local environment, comprehensive internal docstrings, a few files slightly above the preferred line-count guideline, and test coverage breadth beyond core systems.

**Verification Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 14 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- SDK import/version check passed.
- `uv --version` failed because the local `uv.exe` launcher could not start.
- Ruff could not be executed because uv is unavailable in the current shell state and Ruff is not installed in the active virtual environment.

**Remaining Recommendations:**

- Install or repair uv locally, then run `uv run --group dev ruff check .`.
- Add CI for tests and Ruff.
- Add selective docstrings for public internal subsystem classes, especially rendering, collision, environment, and particles.
- Consider splitting `dynamic_environment.py`, `environment.py`, and `particles.py` only if future changes make them harder to maintain.
- Add state-flow and full-renderer smoke tests when practical.

**Known Limitations:**

- Normal gameplay still enables one regular apple.
- Future object definitions are present but inactive.
- Audio architecture exists without bundled audio assets.
- No bundled executable distribution is included.

**Final Architectural Assessment:**

The architecture is appropriate for a standalone 2D Pygame portfolio game. The SDK boundary, `src/` layout, focused gameplay systems, cached procedural rendering, environment manager, persistence, debug tooling, and headless tests provide a professional foundation without forcing enterprise patterns.

**Completion Status:** Complete.

## Prompt 18 - Gameplay Tuning & Difficulty Profiles

**Goal:** Improve gameplay feel through smoother difficulty progression, mouse-only difficulty selection, profile-driven tuning, and more natural wind influence while reusing the existing systems.

**Full Prompt Text:**

```text
Prompt 18 - Gameplay Tuning & Difficulty Profiles

Context

The current project already contains a modular gameplay architecture, a Difficulty System, Wind System, Weather System, UI, and supporting infrastructure.

Recent playtesting revealed that the existing systems work correctly but are not yet well tuned.

This prompt focuses exclusively on gameplay balancing and player experience.

Do not redesign existing architecture.

Reuse the existing systems whenever possible.

---

Objectives

Improve the gameplay feel by tuning existing systems.

Implement:

1. Difficulty Curve Tuning

The current difficulty increases too aggressively.

Rebalance the existing Difficulty System so progression is smoother and remains enjoyable throughout a session.

Use the current infrastructure instead of rewriting it.

2. Difficulty Selection Screen

Add a difficulty selection screen before gameplay.

Selection must be performed using mouse buttons only.

No keyboard shortcuts.

Provide three profiles:

- Beginner
- Intermediate
- Expert

Each profile should reuse the existing Difficulty System while supplying different configuration values.

Avoid duplicated gameplay logic.

The profiles should primarily differ in:

- Initial falling speed
- Difficulty growth rate
- Wind strength
- Maximum active objects
- Spawn probabilities

3. Wind Tuning

Improve the existing Wind System.

Wind should influence object trajectories continuously, producing smooth curved or diagonal motion rather than artificial position jumps.

Reuse the current physics system.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Add new object types.
- Add new power-ups.
- Modify rendering architecture.
- Change collision architecture.
- Introduce new gameplay mechanics.
- Perform major refactors.

Reuse existing systems.

---

Acceptance Criteria

- Difficulty progression feels significantly smoother.
- Difficulty selection works entirely with the mouse.
- Difficulty profiles reuse the existing infrastructure.
- Wind produces natural trajectories.
- Gameplay remains stable.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Difficulty tuning decisions
- Wind tuning decisions
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `src/catch_the_apple/difficulty_profiles.py`

**Files Modified:**

- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/config.py`
- `src/catch_the_apple/dynamic_environment.py`
- `src/catch_the_apple/entities.py`
- `src/catch_the_apple/game.py`
- `src/catch_the_apple/input.py`
- `src/catch_the_apple/states.py`
- `src/catch_the_apple/systems/difficulty.py`
- `src/catch_the_apple/systems/game_rules.py`
- `src/catch_the_apple/systems/movement.py`
- `src/catch_the_apple/systems/spawning.py`
- `src/catch_the_apple/ui.py`
- `tests/test_core_systems.py`

**Difficulty Tuning Decisions:**

Replaced the old global +60 px/s every five catches tuning with profile-driven `DifficultyConfig` values. Beginner starts slower, grows every six catches by a smaller amount, and caps lower. Intermediate is the balanced default. Expert starts faster, grows every four catches, allows two active regular apples, and caps higher. Spawn configuration remains data-driven and supports profile-specific weights while keeping only regular apples enabled.

**Wind Tuning Decisions:**

Wind now includes subtle direction sway and profile-specific strength. Falling objects keep a small `wind_velocity` that eases toward the current wind velocity, producing continuous diagonal/curved trajectories instead of immediately applying wind as direct positional displacement.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 17 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- Dummy-window mouse-selection smoke check passed: menu -> difficulty selection -> intermediate profile -> playing state.
- `uv --version` still fails in this shell due the local `uv.exe` launcher issue, so Ruff was not executed.

**Completion Status:** Complete.

## Prompt 19 - Gameplay Expansion & Power-up Integration

**Goal:** Activate the existing multi-object and power-up infrastructure to create richer gameplay while reusing current spawning, difficulty, effects, particle, UI, and gameplay systems.

**Full Prompt Text:**

```text
Prompt 19 - Gameplay Expansion & Power-up Integration

Context

The project already contains infrastructure for multiple object types, spawning, particles, effects, UI, and gameplay systems.

Currently the game mostly uses the regular apple.

This prompt focuses on activating and integrating existing infrastructure into richer gameplay.

Reuse existing systems whenever possible.

Avoid architectural changes.

---

Objectives

Expand gameplay using the existing architecture.

Implement:

1. Object Types

Enable and balance:

- Golden Apple
- Rotten Apple
- Bomb

Each object should reuse the existing object-definition system.

Avoid hardcoded special cases.

2. Power-Ups

Implement gameplay power-ups using the existing framework.

Examples include:

- Magnet
- Slow Motion
- Basket Speed Boost

Power-ups should have configurable duration and clean lifecycle management.

3. Gameplay Synergy

Power-ups should influence other gameplay systems rather than acting independently.

Examples:

- Magnet activates an Apple Storm for approximately 15 seconds.
- Slow Motion temporarily modifies the Difficulty System.
- Basket Speed Boost cooperates naturally with Dash.
- Future power-ups should be easy to add without changing core systems.

Use existing Spawn, Difficulty, Effects and Particle systems wherever possible.

4. Gameplay Balancing

Adjust spawn probabilities and durations so gameplay remains fair and enjoyable.

Avoid overwhelming the player.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Rewrite existing architecture.
- Replace existing systems.
- Add unnecessary abstractions.
- Change rendering architecture.
- Change physics architecture.

Build on the existing infrastructure.

---

Acceptance Criteria

- Multiple object types are fully integrated.
- Power-ups function correctly.
- Gameplay systems interact naturally.
- Existing architecture is reused.
- Gameplay remains balanced.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Gameplay integration decisions
- Balancing decisions
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:**

- `src/catch_the_apple/powerups.py`

**Files Modified:**

- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/difficulty_profiles.py`
- `src/catch_the_apple/effects.py`
- `src/catch_the_apple/game.py`
- `src/catch_the_apple/session.py`
- `src/catch_the_apple/systems/difficulty.py`
- `src/catch_the_apple/systems/game_rules.py`
- `src/catch_the_apple/systems/movement.py`
- `src/catch_the_apple/systems/spawning.py`
- `src/catch_the_apple/ui.py`
- `tests/test_core_systems.py`

**Gameplay Integration Decisions:**

Enabled golden apples, rotten apples, bombs, and the existing `power_up` object through profile-specific spawn weights. `SpawnSystem.reset_falling_object` now reselects object definitions so spawn probabilities continue to matter throughout a session. Hazards use the existing damage/life system, golden apples use existing score values, and power-up catches activate a data-driven `PowerUpState`.

Power-ups are integrated as reusable definitions rather than new falling-object types. Magnet lasts 15 seconds and cooperates with spawn and movement systems by increasing active objects and pulling catchable objects toward the basket. Slow Motion scales falling-object time and difficulty growth. Speed Boost scales basket max speed, acceleration, and dash speed.

**Balancing Decisions:**

Beginner keeps hazards and power-ups rare. Intermediate uses a balanced mix with modest hazard presence and power-up availability. Expert increases hazards and power-ups while preserving regular apples as the majority. Magnet raises active objects by two only while active, making Apple Storm temporary and bounded.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 21 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- Dummy-runtime smoke check passed: Expert + Magnet raised active objects to 4 through the real `Game.update_playing` path.

**Completion Status:** Complete.

## Prompt 20 - Gameplay Visibility, Feedback & Feature Completion

**Goal:** Make the existing gameplay systems visibly readable and functionally complete by improving wind, object identity, slow motion, Apple Storm, magnet targeting, and day/night visibility without changing architecture.

**Full Prompt Text:**

```text
Prompt 20 - Gameplay Visibility, Feedback & Feature Completion

Context

The project already contains the required gameplay systems and infrastructure.

However, recent playtesting revealed that several implemented systems are either too subtle, not correctly integrated, or difficult for the player to notice.

This prompt is **NOT** about adding new architecture.

Its purpose is to finish and polish the existing gameplay systems so they are immediately visible, enjoyable and functionally correct.

Reuse the existing architecture whenever possible.

---

Objectives

Improve the following systems.

1. Wind

The Wind System currently has little or no noticeable gameplay effect.

Increase its influence so falling objects naturally drift sideways, producing smooth diagonal trajectories.

Avoid artificial position jumps.

Wind should feel alive while remaining fair.

---

2. Object Visual Identity

Players must instantly distinguish between:

- Regular Apple
- Golden Apple
- Rotten Apple
- Bomb
- Power-ups

Improve procedural rendering using clearly different:

- silhouettes
- colors
- highlights
- glow
- particles
- animations
- visual effects

Recognition should require no conscious effort.

---

3. Slow Motion Power-up

The Slow Motion power-up currently feels absent or too weak.

Improve it so that:

- the pickup is visually obvious
- activation feedback is immediate
- HUD displays remaining duration
- the slowdown is clearly noticeable
- gameplay returns smoothly to normal afterwards

Reuse the existing timing system.

---

4. Apple Storm

Complete the Apple Storm feature.

During Apple Storm:

- many apples should spawn simultaneously
- the event should feel exciting and rewarding
- the player should not lose lives
- the player should not lose score
- missed apples during the storm should not be punished

Apple Storm should be a bonus event rather than a punishment.

---

5. Magnet Integration

When Magnet is active during Apple Storm:

ONLY

- Regular Apples
- Golden Apples

should be attracted toward the basket.

The following MUST NOT be attracted:

- Rotten Apples
- Bombs

Their trajectories should remain governed only by physics and wind.

---

6. Day / Night Visibility

The Day/Night system currently has little visual impact.

Increase the visible difference between day and night by improving:

- sky colors
- ambient lighting
- directional lighting
- shadow intensity
- sun/moon visibility
- background colors
- environmental atmosphere

Transitions should remain smooth.

---

General Goal

Prioritize gameplay readability.

Every major gameplay mechanic should communicate itself visually without requiring explanation.

Players should immediately notice when:

- wind changes
- day becomes night
- Apple Storm begins
- Slow Motion activates
- Magnet activates

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Restrictions

Do NOT:

- Rewrite architecture.
- Introduce new gameplay systems.
- Change collision architecture.
- Replace existing rendering pipeline.

Reuse existing systems and improve their integration.

---

Acceptance Criteria

- Wind is clearly noticeable.
- Object types are immediately recognizable.
- Slow Motion is visually and mechanically obvious.
- Apple Storm is exciting and non-punishing.
- Magnet only attracts beneficial apples.
- Day/Night transition is clearly visible.
- Gameplay readability is significantly improved.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files created
- Files modified
- Gameplay polish decisions
- Balancing decisions
- Manual verification
- Confirmation that PROMPTS_BOOK was updated
```

**Files Created:** None.

**Files Modified:**

- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/difficulty_profiles.py`
- `src/catch_the_apple/dynamic_environment.py`
- `src/catch_the_apple/effects.py`
- `src/catch_the_apple/environment.py`
- `src/catch_the_apple/powerups.py`
- `src/catch_the_apple/procedural_assets.py`
- `src/catch_the_apple/systems/game_rules.py`
- `src/catch_the_apple/ui.py`
- `tests/test_core_systems.py`

**Gameplay Polish Decisions:**

Increased profile wind strength and gameplay wind scale while keeping the existing eased wind velocity path, so objects drift visibly without snapping. Procedural object visuals now use distinct silhouettes: normal apples remain red fruit, golden apples glow with star highlights, rotten apples are misshapen with spots, bombs are dark circles with fuse/spark, and power-ups are glowing blue diamonds.

Slow Motion now scales falling time more strongly, slows difficulty growth more clearly, emits a power-up burst, appears in the HUD duration list, and shows a large status banner. Apple Storm now spawns many apples by increasing Magnet's active object bonus, and missed regular/golden apples during Magnet are non-punishing. Magnet attraction is restricted to regular and golden apples only.

Day/night contrast was increased with darker night sky colors, brighter daylight, stronger ambient/directional lighting differences, stronger shadow contrast, a night overlay, and larger sun/moon drawing.

**Balancing Decisions:**

Magnet now adds five temporary active objects so Apple Storm is obvious. Slow Motion uses a 0.48 falling-time scale and 0.40 difficulty-growth scale so it is immediately noticeable while still temporary. Wind was increased by profile, with Beginner remaining softer than Intermediate and Expert.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 23 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.
- Dummy gameplay render smoke passed with Expert, Magnet, and Slow Motion active: `PlayingState`, 7 active objects, HUD power-up labels rendered.

**Completion Status:** Complete.

## Prompt 21 - Fix Hazard Miss Logic

**Goal:** Correct hazard miss behavior so rotten apples and bombs only damage the player when they collide with the basket.

**Full Prompt Text:**

```text
Prompt 21 - Fix Hazard Miss Logic

Context

Playtesting revealed an incorrect gameplay rule.

Currently, when a Rotten Apple or Bomb reaches the bottom of the screen without being caught, the player still loses one life.

This is incorrect.

---

Objective

Update the gameplay rules so that lives are only lost when appropriate.

Required behavior:

- Missing a Regular Apple should continue to behave according to the existing game rules.
- Missing a Golden Apple should follow the existing intended rules.
- Missing a Rotten Apple must NOT reduce lives.
- Missing a Bomb must NOT reduce lives.

Hazards should only affect the player if they actually collide with the basket.

Reuse the existing object-type system rather than adding special-case logic.

---

PROMPTS_BOOK

Append this prompt to docs/PROMPTS_BOOK.md.

---

Acceptance Criteria

- Missing Rotten Apples does not reduce lives.
- Missing Bombs does not reduce lives.
- Hazards only cause damage on collision.
- Existing gameplay rules for beneficial objects remain unchanged.
- PROMPTS_BOOK updated.

---

Required Response

Report:

- Files modified
- Gameplay rule updated
- Manual verification performed
- Confirmation that PROMPTS_BOOK was updated
```

**Files Modified:**

- `docs/PROMPTS_BOOK.md`
- `src/catch_the_apple/systems/game_rules.py`
- `tests/test_core_systems.py`

**Gameplay Rule Updated:**

Miss damage now comes from the object definition category. Hazards use zero miss damage, while non-hazard objects keep their configured miss damage. The game rules also avoid calling `lose_life` when miss damage is zero, preventing non-damaging misses from resetting combo.

**Test Results:**

- `.venv\Scripts\python.exe -m unittest discover` passed: 24 tests.
- `.venv\Scripts\python.exe -m compileall src tests main.py` passed.

**Completion Status:** Complete.
