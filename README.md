# Catch the Apple

Catch the Apple is a polished 2D Pygame arcade game built as a Python portfolio project. The player moves a basket along the bottom of the screen, catches falling apples, manages lives, and builds score while the game presents procedural visuals, lighting, particles, weather, and a day/night environment.

The project remains intentionally focused: it is a game, not a general-purpose engine. Its purpose is to demonstrate clean Python architecture, modular gameplay systems, 2D graphics programming, collision detection, procedural rendering, testing, and clear documentation.

## Features

- Modular `catch_the_apple` package with a thin executable entry point.
- Delta-time runtime with separate update and render phases.
- Structured session, world, entity, input, movement, spawning, scoring, difficulty, and game-rules systems.
- Data-driven object definitions with the regular apple enabled for normal play.
- Velocity-based basket movement with acceleration, drag, boundary constraints, and dash state.
- Composite basket collision with circular falling-object collision and continuous collision detection.
- Cached procedural apple and basket surfaces.
- Lightweight ambient and directional lighting with soft ground shadows.
- Generic pooled particle system, motion trails, and reusable squash/stretch animation.
- Procedural parallax environment with sky, clouds, mountains, trees, bushes, and grass.
- Dynamic wind, weather presets, and smooth day/night lighting state.
- Main menu, playing, paused, and game-over states with a modular HUD.
- Local persistence for high score, best combo, settings, and session statistics.
- Debug overlay and collision visualization toggles.
- Headless automated tests for core systems.

## Installation

Use Python 3.11 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

On macOS or Linux, activate the virtual environment with:

```bash
source .venv/bin/activate
```

## Running

Run the game from the repository root:

```bash
python main.py
```

The package entry point is also available:

```bash
python -m catch_the_apple
```

## Controls

| Control | Action |
|---|---|
| Left Arrow | Move basket left |
| Right Arrow | Move basket right |
| Space | Dash |
| Enter | Start from menu |
| Esc or P | Pause/resume |
| R | Restart from game over |
| F1 | Toggle collision overlay |
| F2 | Toggle debug overlay |
| M | Toggle mute |
| + / - | Adjust master volume |

## Testing

Run the automated test suite from the repository root:

```bash
python -m unittest discover
```

The tests configure SDL for headless execution where practical, so they can validate core logic without opening a visible game window.

## Project Structure

```text
catch_the_apple/
  app.py                  Application entry point
  game.py                 Runtime loop and subsystem composition
  states.py               Main menu, playing, paused, and game-over flow
  world.py                World-owned entities
  entities.py             Basket and falling-object data structures
  systems/                Gameplay systems
  rendering.py            Main renderer orchestration
  procedural_assets.py    Cached procedural apple and basket drawing
  lighting.py             Surface lighting and ground shadows
  environment.py          Procedural parallax background
  dynamic_environment.py  Wind, weather, and day/night state
  particles.py            Generic pooled particle simulation
  persistence.py          Local save data
  audio.py                Audio channels and settings
  debug.py                Runtime debug snapshots
docs/                     Architecture, workflow, roadmap, and prompt log
tests/                    Headless automated tests
```

## Documentation

- `docs/ARCHITECTURE.md` describes the runtime architecture and subsystem boundaries.
- `docs/DEVELOPMENT.md` defines the development workflow and verification expectations.
- `docs/GRAPHICS_AND_MATH.md` explains the current graphics and mathematical foundations.
- `docs/ROADMAP.md` captures future project directions.
- `docs/PROMPTS_BOOK.md` is the permanent prompt-driven development log.

## Save Data

Save data is stored locally in the user's home directory under `.catch_the_apple/save.json`. Missing or corrupted save files are handled by falling back to defaults.

## Known Limitations

- The game currently has one active regular apple during normal play.
- Future object definitions exist, but special behaviors are intentionally not enabled yet.
- Audio channel structure and settings exist, but no bundled audio assets are included.
- The project does not currently include packaging metadata for building a distributable executable.

## Future Work

Future development should focus on measured polish: richer enabled object behaviors, audio assets, packaging, CI automation, and additional integration tests. The project should continue to remain a focused 2D Pygame game.
