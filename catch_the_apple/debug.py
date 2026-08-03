from dataclasses import dataclass


@dataclass(frozen=True)
class DebugSnapshot:
    fps: float
    frame_time_ms: float
    active_objects: int
    particle_count: int
    current_state: str
    weather: str
    wind_strength: float
    wind_direction: tuple[float, float]
    collision_debug_enabled: bool
    audio_available: bool
    muted: bool
