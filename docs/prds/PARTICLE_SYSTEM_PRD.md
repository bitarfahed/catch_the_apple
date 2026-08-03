# Particle System PRD

## Purpose

The particle system provides reusable visual effects for catch bursts, trails, dash feedback, and future object-specific effects.

## Current Requirements

- Use a generic particle data model.
- Create effects from emitter configuration rather than custom particle classes.
- Simulate particles independently from gameplay rules.
- Use object pooling to reduce runtime allocations.
- Let rendering draw particles without owning simulation.

## Boundaries

- Particles do not determine gameplay outcomes.
- Weather and gameplay-specific emitters should share the generic engine.

## Future Considerations

- Add more emitter presets as new gameplay objects become active.
- Keep pool size configurable if effect density changes.
