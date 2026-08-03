# Engineering Plan

## Current Compliance Target

Prompt 16 aligns the repository with professional Python/Pygame structure while preserving gameplay. This plan records the stable development posture after feature completion.

## Active Architecture Decisions

- Use `src/` layout for import clarity.
- Expose public integration through `catch_the_apple` and `catch_the_apple.sdk`.
- Keep `main.py` as a thin local launcher.
- Keep Pygame-specific rendering and input inside the package.
- Keep business gameplay logic in focused systems under `catch_the_apple.systems`.
- Keep documentation in `docs/`, with dedicated PRDs for major mechanisms.

## Verification Plan

- Run unit tests with `python -m unittest discover`.
- Run bytecode compilation with `python -m compileall src tests main.py`.
- Run Ruff with `uv run --group dev ruff check .` when uv/Ruff are available.
- Smoke-check `main.py` imports and SDK imports after architecture changes.

## Change Management

- Preserve gameplay behavior unless a future prompt explicitly changes it.
- Prefer small refactors with direct maintainability value.
- Avoid adding dependencies unless they support runtime, tooling, or documentation needs.
- Update `docs/PROMPTS_BOOK.md` for every prompt-driven change.
