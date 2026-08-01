# Development

## Principles

Development should be incremental, testable, and honest about the current state of the project. Each change should keep the game runnable and should improve either player experience, architecture, graphics, physics, tests, or documentation.

## Constraints

- Keep the project as a 2D Pygame game.
- Avoid turning the codebase into a generic engine.
- Prefer small modules with clear ownership.
- Keep production code, tests, and documentation aligned.
- Do not add dependencies unless they directly support the project goals.

## Workflow

1. Inspect the current code before changing it.
2. Make one focused change at a time.
3. Keep gameplay behavior stable unless the prompt explicitly changes it.
4. Verify the game or affected subsystem after each implementation step.
5. Record completed prompt work in `docs/PROMPTS_BOOK.md`.

## Verification Expectations

As the project grows, verification should include:

- Running the game when practical
- Running automated tests once they exist
- Checking formatting and linting once configured
- Manually validating visual/gameplay behavior for player-facing changes

## Documentation Expectations

Documentation should describe what exists and where the project is going. It should avoid claiming features, architecture, tests, or assets that have not been implemented yet.
