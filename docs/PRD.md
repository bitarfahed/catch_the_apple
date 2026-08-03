# Product Requirements Document

## Product Summary

Catch the Apple is a standalone 2D Pygame arcade game. The player controls a basket, catches falling apples, preserves lives, and builds score while the game demonstrates professional Python architecture and lightweight 2D graphics programming.

## Goals

- Provide a complete, runnable arcade game.
- Demonstrate clean Python package structure and modular subsystem ownership.
- Keep gameplay readable, responsive, and fair.
- Showcase procedural rendering, lighting, collision, particles, environment systems, persistence, and testing.
- Remain understandable as a public portfolio repository.

## Non-Goals

- Do not turn the project into a general-purpose engine.
- Do not add networking, APIs, databases, or enterprise service layers.
- Do not require external image assets for the current visual presentation.
- Do not prioritize packaging as a commercial game distribution yet.

## Target User

The primary audience is a reviewer of a Python/game-development portfolio project. The game should also be playable by someone cloning the repository locally.

## Core Experience

- Launch the game from the repository or installed console script.
- Start from a main menu.
- Move left and right.
- Dash for responsive movement.
- Catch falling apples.
- Track score, lives, combo, and dash availability.
- Pause and restart.
- See polished procedural visuals and environmental atmosphere.

## Technical Requirements

- Use Python 3.11 or newer.
- Remain a 2D Pygame application.
- Expose public launch/control behavior through the SDK surface in `catch_the_apple`.
- Keep `main.py` as a thin launcher.
- Keep gameplay systems independent from rendering where practical.
- Keep procedural graphics cached rather than regenerated every frame.
- Support headless automated tests for core logic.

## Success Criteria

- The repository runs locally with documented commands.
- Core systems have automated tests.
- Documentation explains project purpose, structure, controls, architecture, and known limitations.
- Future tools can launch or inspect the game through the SDK instead of importing internal modules.
