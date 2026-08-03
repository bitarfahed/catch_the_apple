# Collision PRD

## Purpose

The collision system determines interactions between falling objects and the basket while keeping gameplay fair under delta-time movement.

## Current Requirements

- Represent falling objects as circles.
- Represent the basket as a composite collision model.
- Detect normal circle-vs-rectangle overlap.
- Use continuous collision detection for fast vertical sweeps through the catch region.
- Expose debug visualization data through rendering without coupling collision to UI.

## Boundaries

- Collision does not apply score, lives, particles, or audio directly.
- Collision does not implement bouncing physics or complex rigid-body response.

## Future Considerations

- Add shape types only when a concrete gameplay object requires them.
- Keep CCD coverage focused on cases where tunneling is likely.
