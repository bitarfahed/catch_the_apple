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
