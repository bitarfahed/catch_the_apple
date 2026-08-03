# Rendering PRD

## Purpose

The rendering system presents the playable 2D scene, procedural objects, lighting, environment layers, particles, HUD, menus, and debug overlays.

## Current Requirements

- Render through Pygame surfaces.
- Draw gameplay without changing simulation state.
- Use cached procedural apple and basket surfaces.
- Apply lightweight cached lighting and ground shadows.
- Draw procedural environment layers before gameplay entities.
- Keep debug and collision overlays optional.

## Boundaries

- Rendering does not own scoring, spawning, collision, or movement rules.
- The project should not become a general rendering engine.
- Expensive per-frame Python pixel loops should be avoided.

## Future Considerations

- Add integration smoke tests for the full renderer.
- Keep lighting parameters controllable by environment systems.
- Add visual assets only when they serve the game and are documented.
