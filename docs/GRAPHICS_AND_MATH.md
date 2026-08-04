# Graphics and Mathematics

## Purpose

This document summarizes the current graphics and mathematical systems in Catch the Apple. The project remains a 2D Pygame game, so the rendering approach favors clear, lightweight techniques over engine-style generality.

## Coordinate Model

The game uses Pygame's screen coordinate system:

- The origin is the top-left corner of the window.
- Positive X moves right.
- Positive Y moves down.
- Gameplay positions are stored as floating-point values and converted to integer rectangles for drawing and collision checks.

Reusable 2D helpers live in `catch_the_apple.math2d`:

- `Vector2` aliases `pygame.Vector2`.
- `vec2()` creates vectors consistently.
- `clamp()` constrains values such as positions, velocities, and interpolation factors.
- `Transform2D` stores position, rotation, and scale for future rendering and animation reuse.

## Timing and Motion

The runtime is delta-time based. The main loop measures elapsed time through `pygame.time.Clock`, clamps large spikes, then updates simulation and rendering as separate steps.

Basket movement is velocity-based:

- Horizontal input applies acceleration.
- Drag slows the basket when no direction is held.
- Maximum speed limits normal motion.
- Dash uses a separate timed movement state with its own speed, duration, and cooldown.
- Screen bounds clamp basket position and cancel outward velocity at the edges.

Falling objects store both previous and current positions so collision can use swept movement when needed.

## Collision Mathematics

Falling objects currently use circular collision shapes. The basket uses a composite model:

- Catch region
- Left rim
- Right rim
- Basket body

Circle-vs-rectangle checks are used for normal overlap. Continuous collision detection expands the basket catch region by the object radius and tests the segment between previous and current object centers, reducing tunneling when objects move quickly.

## Procedural Assets

The apple and basket are generated with Pygame drawing primitives rather than external PNG assets.

The apple surface includes:

- Ellipse body
- Stem
- Leaf
- Simple shading
- Highlight

The basket surface includes:

- Body
- Rim
- Woven line pattern
- Basic shading

Procedural surfaces are cached by size and appearance so they are generated only when needed.

## Lighting and Shadows

The lighting system is surface-based and intentionally inexpensive:

- Ambient lighting is applied with a multiplicative surface pass.
- Directional lighting adds diffuse color and simple specular highlights.
- Ground shadows are generated as cached translucent ellipses.
- Shadow size and alpha respond to estimated object height, light intensity, and light direction.

The system avoids expensive per-frame Python pixel loops.

## Environment Rendering

The environment renderer procedurally creates and caches parallax layers:

- Sky gradient
- Clouds
- Mountains
- Trees
- Bushes
- Foreground grass

Each layer has a depth factor and scroll speed. The dynamic environment manager supplies wind, weather tint, fog alpha, day/night colors, and lighting parameters.

## Super Powers

Every super power combines gameplay behavior, a visual identity, and a simple mathematical model.

| Power | Mathematical Idea | Gameplay Effect | Visual Representation |
|---|---|---|---|
| Magnet | Attractive force: `dx/dt = clamp(k(target_x - x), -vmax, vmax)` | Pulls regular and golden apples toward the basket and starts Apple Storm. | Gold HUD banner, apple storm density, catch particles. |
| Time Warp | Time scaling: `dt' = s * dt`, where `0 < s < 1` | Slows falling objects and difficulty growth. | Blue HUD banner and power-up burst. |
| Dash Boost | Velocity scaling: `vmax' = alpha * vmax` and `dash' = alpha * dash` | Raises basket acceleration, max speed, and dash speed. | Green HUD banner and stronger basket motion. |
| Wind Control | Vector field boost: `wind' = beta * wind + control_bias` | Amplifies sideways wind drift during normal movement. | Cyan HUD label and more visible diagonal trajectories. |
| Shockwave | Radial impulse: `p' = p + normalize(p-c) * I * falloff(r)` | Pushes falling objects away from the basket. | Bright burst particles and sudden radial separation. |
| Black Hole | Inverse-distance attraction: `a = G(center - p) / (r^2 + epsilon)` | Draws objects toward screen center. | Violet HUD label and converging object paths. |
| Gravity Control | Gravity scaling: vertical motion uses `g' = gamma * g` | Reduces falling speed independently of normal Time Warp. | Pale blue HUD label and lighter descent. |
| Golden Rain | Weighted sampling override: `P(golden)` is multiplied while active | Makes golden apples much more likely and suppresses hazards. | Gold HUD label and frequent glowing apples. |
| Freeze Bombs | Selective velocity mask: `v_hazard = 0` | Freezes hazardous objects while beneficial objects continue falling. | Ice-blue HUD label and suspended hazards. |

## Performance Notes

- Most visual assets are cached Pygame surfaces.
- Particle simulation uses a fixed pool to reduce runtime allocations.
- Lighting cache entries are invalidated only when lighting configuration changes.
- The current procedural sky and environment layers are generated once per renderer instance.
- The debug and collision overlays are optional and can be toggled during play.

## Known Technical Limits

- Collision shapes are intentionally limited to circles and rectangles.
- Lighting is stylized surface compositing, not physically based lighting.
- The environment uses lightweight procedural drawing rather than large-scale terrain generation.
- Rendering still targets a fixed-size playfield.
