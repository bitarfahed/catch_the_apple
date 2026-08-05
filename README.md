# Catch the Apple

Catch the Apple is a polished 2D Pygame arcade game built as a Python portfolio project. The player moves a basket along the bottom of the screen, catches falling apples, manages lives, and builds score while the game presents procedural visuals, lighting, particles, weather, and a day/night environment.

The project remains intentionally focused: it is a game, not a general-purpose engine. Its purpose is to demonstrate clean Python architecture, modular gameplay systems, 2D graphics programming, collision detection, procedural rendering, testing, and clear documentation.

## Features

- Professional `src/` package layout with a thin executable launcher.
- Public SDK surface exposed through `catch_the_apple` and `catch_the_apple.sdk`.
- Delta-time runtime with separate update and render phases.
- Structured session, world, entity, input, movement, spawning, scoring, difficulty, and game-rules systems.
- Data-driven object definitions for apples, hazards, bombs, power-ups, and rare extra-life name objects.
- Velocity-based basket movement with acceleration, drag, boundary constraints, and dash state.
- Composite basket collision with circular falling-object collision and continuous collision detection.
- Cached procedural apple and basket surfaces.
- Lightweight ambient and directional lighting with soft ground shadows.
- Generic pooled particle system, motion trails, and reusable squash/stretch animation.
- Procedural parallax environment with sky, clouds, mountains, trees, bushes, and grass.
- Dynamic wind, visual rain, weather presets, and smooth day/night lighting state.
- Player-name start screen, playing, paused, and game-over states with a modular HUD.
- Lightweight generated sound effects for gameplay objects.
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

When installed as a package, the console script is also available:

```bash
catch-the-apple
```

## Controls

| Control | Action |
|---|---|
| Left Arrow | Move basket left |
| Right Arrow | Move basket right |
| Space | Dash |
| Enter | Submit player name / start from menu |
| Esc | Pause/resume |
| C while paused | Open developer cheat console |
| R | Restart from game over |
| F1 | Toggle collision overlay |
| F2 | Toggle debug overlay |
| M | Toggle mute |
| + / - | Adjust master volume |

## Core Rules

- Catching Regular Apples increases score.
- Missing Regular Apples reduces score by 2 and never removes lives.
- When multiple Regular/Golden Apples are visible together, catching one prevents miss penalties for the rest of that active group.
- Catching Rotten Apples reduces score by 2 and never removes lives.
- Missing Golden Apples, Rotten Apples, or Bombs has no penalty.
- Bomb collisions reduce lives unless a protective effect is active.
- Score is allowed to be 0 only before the player has earned points; returning to 0 later ends the game.
- Lives reaching 0 also ends the game.

## Developer Cheat Console

The cheat console is available only while paused. Press `C`, type a code, and press `Enter`. Press `Esc` to return to Pause, then press `Esc` again to resume. Temporary cheats can be entered again to disable them early. Codes are case-sensitive where shown; `WIND` activates Wind Control, while `wind` activates temporary rain.

Super Power codes also accept their internal identifier aliases such as `magnet`, `slow_motion`, and `black_hole`. The one intentional exception is wind: lowercase `wind` is the rain cheat, while uppercase `WIND` is Wind Control.

| Syntax | Duration | Gameplay effect | Visual effect | Math / algorithm |
|---|---:|---|---|---|
| `MAGNET` | 15s | Attracts only Regular and Golden Apples and supports Apple Storm synergy. | Gold HUD/status, glow, trails, and attraction particles. | Clamped attractive acceleration and velocity integration. |
| `TIME` | 8s | Slows simulation time and difficulty growth. | Blue Time Warp feedback. | Delta-time scaling. |
| `DASH` | 7s | Increases basket movement and dash speed. | Green Dash Boost feedback. | Velocity scaling. |
| `WIND` | 10s | Amplifies gameplay wind drift. | Cyan wind feedback and stronger diagonal trajectories. | Vector-field scaling. |
| `WAVE` | 1.2s | Pushes falling objects away from the basket. | Bright radial burst. | Radial impulse with distance falloff. |
| `VOID` | 7s | Pulls objects toward the screen center. | Violet Black Hole feedback. | Inverse-distance attraction. |
| `GRAV` | 9s | Reduces falling speed through gravity/simulation scaling. | Pale-blue Gravity Control feedback. | Gravity and time scaling. |
| `GOLD` | 10s | Increases Golden Apple probability and suppresses hazards. | Frequent glowing Golden Apples. | Weighted spawn sampling. |
| `FREEZE` | 8s | Freezes hazardous objects only. | Ice-blue Freeze Bombs feedback. | Selective velocity mask. |
| `easy` | 20s | Reduces falling-object time scale to 0.55. | Easy Mode countdown. | Delta-time scaling. |
| `wind` | 20s | Forces visual rain only; gameplay physics are unchanged. | Screen-covering rain particles. | Weather override and particle simulation. |
| `nosound` | Until `sound` | Mutes all generated sounds. | Console confirmation. | Boolean audio gate. |
| `sound` | Instant | Restores generated sound playback. | Console confirmation. | Volume recomputation. |
| `shield` | 20s | Costs 5 score, then blocks bomb damage; fails gracefully below 5 score. | Shield countdown and basket glow. | Collision filtering. |
| `cycle` | 20s | Wraps basket movement across screen edges. | Cycle countdown. | Modulo arithmetic. |
| `flip <angle>` | 20s | Rotates the gameplay world by `angle` degrees, where `angle` is 0-360. | Rotated world with readable HUD. | Rotation transform around the playfield center. |
| `fahed` | 20s | Expands the basket, auto-collects Regular/Golden Apples, and blocks hazards. | Strong glow, particles, motion trail, and countdown. | Scaling and expanded collision geometry. |
| `insane` | 20s | Regular Apples spawn at random 3x-6x scale for 1 point; Golden Apples spawn at 10x scale for 3 points. | Giant apples, banner, glow, and activation particles. | Random scale sampling. |

## Testing

Run the automated test suite from the repository root:

```bash
python -m unittest discover
```

The tests configure SDL for headless execution where practical, so they can validate core logic without opening a visible game window.

Ruff is configured in `pyproject.toml`. When uv and the dev tool group are available, run:

```bash
uv run --group dev ruff check .
```

## Project Structure

```text
main.py                     Thin local launcher
src/catch_the_apple/
  __init__.py               Public SDK exports
  sdk.py                    Supported launch/control interface
  app.py                    Backward-compatible launch facade
  game.py                   Runtime loop and subsystem composition
  states.py                 Main menu, playing, paused, and game-over flow
  world.py                  World-owned entities
  entities.py               Basket and falling-object data structures
  systems/                  Gameplay systems
  rendering.py              Main renderer orchestration
  procedural_assets.py      Cached procedural apple and basket drawing
  lighting.py               Surface lighting and ground shadows
  environment.py            Procedural parallax background
  dynamic_environment.py    Wind, weather, and day/night state
  particles.py              Generic pooled particle simulation
  persistence.py            Local save data
  audio.py                  Audio channels and settings
  debug.py                  Runtime debug snapshots
docs/                       Architecture, PRDs, workflow, roadmap, and prompt log
tests/                      Headless automated tests
```

## Documentation

- `docs/ARCHITECTURE.md` describes the runtime architecture and subsystem boundaries.
- `docs/DEVELOPMENT.md` defines the development workflow and verification expectations.
- `docs/GRAPHICS_AND_MATH.md` explains the current graphics and mathematical foundations.
- `docs/PRD.md` defines the product requirements.
- `docs/PLAN.md` records the current engineering plan.
- `docs/TODO.md` tracks deferred quality and release work.
- `docs/prds/` contains mechanism-specific PRDs.
- `docs/ROADMAP.md` captures future project directions.
- `docs/PROMPTS_BOOK.md` is the permanent prompt-driven development log.

## Save Data

Save data is stored locally in the user's home directory under `.catch_the_apple/save.json`. Missing or corrupted save files are handled by falling back to defaults.

## Known Limitations

- Audio channel structure and settings exist, but no bundled audio assets are included.
- The project does not currently include a bundled distributable executable.

## Future Work

Future development should focus on measured polish: richer enabled object behaviors, audio assets, packaging, CI automation, and additional integration tests. The project should continue to remain a focused 2D Pygame game.
