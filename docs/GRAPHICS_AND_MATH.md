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

Object rendering uses an environment-aware readability palette. During daytime,
falling object colors remain unchanged. During night, regular apples interpolate
toward a light glowing white instead of being hidden by the darker environment:

- Regular apples move toward light white.
- Golden apples remain gold.
- Rotten apples remain unchanged.
- Bombs remain unchanged.
- Power-ups remain unchanged.

The interpolation is controlled by a night factor derived from ambient light:
`night = clamp((0.64 - ambient) / 0.32, 0, 1)`. This keeps transitions smooth
while preserving immediate object recognition.

The rare player-name object reuses the falling-object system and renders as a
glowing text badge. It is gameplay-visible because the rendered label is the
validated player name, and mathematically it follows the same position,
collision, wind, and delta-time update path as other falling objects.

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

Wind is modeled as a continuous vector field built from overlapping sinusoidal
components. The base weather direction is blended with primary gust,
secondary gust, and swirl vectors, allowing the horizontal component to move
smoothly through both leftward and rightward values. Wind applies to gameplay
as an eased velocity target rather than a direct position offset. Falling
objects move toward the current wind vector with:
`wind_velocity += (target_wind - wind_velocity) * response * dt`, then their
positions advance by `wind_velocity * dt`. This produces smooth diagonal paths
and visible gust changes without abrupt sideways jumps.

Rain is a visual weather event. It reuses the pooled particle system and weather
state, but it does not modify gameplay wind, object speed, collision, scoring,
or difficulty. This keeps the weather readable without making the game less fair.

## Generated Audio

Gameplay sound effects are generated in memory with short decaying sine waves.
Simple tones and two-tone chimes distinguish regular apples, golden apples,
rotten apples, bombs, power-ups, and the extra-life name object without external
audio assets. Each waveform uses a linear decay envelope so sounds remain brief
and unobtrusive. UI confirmation, error, and cheat feedback sounds use the same
generated waveform approach.

## Super Powers

Every super power combines gameplay behavior, a visual identity, and a simple mathematical model.

Canonical Super Power cheat codes are uppercase. The console also accepts each
internal identifier as an alias, such as `magnet` or `black_hole`, because the
lookup normalizes Super Power input. Lowercase `wind` is reserved for the rain
developer cheat, so use uppercase `WIND` for Wind Control.

| Command | Alias | Duration | Parameters | Mathematical Idea | Gameplay Effect | Visual Representation | Notes |
|---|---|---:|---|---|---|---|---|
| `MAGNET` | `magnet` | 15s | None | Smooth attractive acceleration: `a = clamp(k(target_x - x), -amax, amax)`, `v = clamp(v + a dt, -vmax, vmax)` | Pulls only Regular and Golden Apples toward the basket and preserves Apple Storm synergy. | Gold HUD banner/status, glow, apple-only trail particles, and denser apple action during synergy. | Rotten Apples and Bombs are explicitly excluded. |
| `TIME` | `slow_motion` | 8s | None | Time scaling: `dt' = s * dt`, where `0 < s < 1` | Slows falling objects and difficulty growth. | Blue HUD banner and power-up burst. | Stacks through the existing simulation time-scale path. |
| `DASH` | `speed_boost` | 7s | None | Velocity scaling: `vmax' = alpha * vmax` and `dash' = alpha * dash` | Raises basket acceleration, max speed, and dash speed. | Green HUD banner and stronger basket motion. | Reuses basket movement tuning. |
| `WIND` | `wind_control` | 10s | None | Vector field boost: `wind' = beta * wind + control_bias` | Amplifies sideways wind drift during normal movement. | Cyan HUD label, HUD wind vector, and stronger diagonal trajectories. | Distinct from lowercase `wind`, which activates rain. |
| `WAVE` | `shockwave` | 1.2s | None | Radial impulse: `p' = p + normalize(p-c) * I * falloff(r)` | Pushes falling objects away from the basket. | Bright burst particles and sudden radial separation. | Short-lived impulse effect. |
| `VOID` | `black_hole` | 7s | None | Inverse-distance attraction: `a = G(center - p) / (r^2 + epsilon)` | Draws objects toward screen center. | Violet HUD label and converging object paths. | Uses a minimum radius to avoid extreme acceleration. |
| `GRAV` | `gravity_control` | 9s | None | Gravity scaling: vertical motion uses `g' = gamma * g` | Reduces falling speed independently of normal Time Warp. | Pale blue HUD label and lighter descent. | Also contributes to simulation time scaling. |
| `GOLD` | `golden_rain` | 10s | None | Weighted sampling override: `P(golden)` is multiplied while active | Makes Golden Apples much more likely and suppresses hazards. | Gold HUD label and frequent glowing apples. | Does not change Golden Apple miss penalties. |
| `FREEZE` | `freeze_bombs` | 8s | None | Selective velocity mask: `v_hazard = 0` | Freezes hazardous objects while beneficial objects continue falling. | Ice-blue HUD label and suspended hazards. | Applies only to objects categorized as hazards. |

## Developer Cheats

Developer cheats use the same pause-only console as Super Powers. Temporary
cheats live in `CheatState`, update by delta time, and expire back to normal
gameplay settings. Entering an active temporary cheat again toggles it off and
restores the normal state immediately.

| Syntax | Duration | Parameters | Mathematical Concept | Algorithm | Gameplay Effect | Visual Effect | Notes |
|---|---:|---|---|---|---|---|---|
| `easy` | 20s | None | Time scaling | Falling-object `dt` is multiplied by `0.55`. | Objects descend more slowly for debugging or demos. | Easy Mode countdown banner. | Entering `easy` again disables it early. |
| `wind` | 20s | None | Particle simulation and weather override | Weather is forced to Rain while rain particles are emitted from pooled emitters. | No gameplay physics changes. | Rain streaks cover the screen for about 20 seconds. | Lowercase only; uppercase `WIND` activates Wind Control. |
| `nosound` | Until `sound` | None | Boolean state gating | Audio volume resolves to zero while muted. | All generated sounds stop. | Console confirmation. | Persistent until `sound` is entered or settings change. |
| `sound` | Instant | None | Boolean state restoration | Mute is cleared and channel volumes are recomputed. | Generated sounds return. | Console confirmation. | Does not activate a timed cheat state. |
| `shield` | 20s | Costs 5 score | Collision filtering | Bomb collision damage is masked after spending 5 score. | Bombs cannot damage the player while active. | Shield countdown and basket glow. | Fails gracefully below 5 score; entering again disables it early without another cost. |
| `cycle` | 20s | None | Modulo arithmetic | Basket position wraps with `x = (x + width) mod (screen_width + width) - width`. | Exiting one side re-enters from the other. | Cycle countdown. | Entering `cycle` again disables it early. |
| `flip <angle>` | 20s | `angle` from 0 to 360 degrees | Rotation matrix | Gameplay world is rendered to a surface and rotated around the playfield center. | World orientation changes temporarily. | The world visibly rotates while HUD remains readable. | Entering any `flip <angle>` while active disables the current flip. |
| `fahed` | 20s | None | Scaling and collision geometry | Basket width scales to most of the screen; Regular and Golden Apples auto-collect; hazard damage is masked. | Powerful demo mode with safe auto-catches. | Wide glowing basket, particles, motion trail, and countdown. | Entering `fahed` again disables it early. |
| `insane` | 20s | None | Random scale sampling | Regular Apples sample `scale ~ U(3, 6)` per spawn; Golden Apples use `scale = 10`. | Regular Apples stay worth 1 point; Golden Apples are worth 3 points while active. | Insane Mode banner, giant apples, glow, and activation particles. | Rotten Apples and Bombs keep normal size. |

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
