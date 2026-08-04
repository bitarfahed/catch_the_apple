from dataclasses import dataclass

from catch_the_apple import config
from catch_the_apple.dynamic_environment import WindConfig
from catch_the_apple.math2d import vec2


@dataclass(frozen=True)
class DifficultyProfile:
    identifier: str
    display_name: str
    description: str
    spawn_config: config.SpawnConfig
    difficulty_config: config.DifficultyConfig
    wind_config: WindConfig
    gameplay_wind_scale: float


STANDARD = DifficultyProfile(
    identifier="standard",
    display_name="Standard",
    description="Balanced pace with smooth growth and visible wind.",
    spawn_config=config.SpawnConfig(
        max_active_objects=1,
        enabled_object_ids=("regular_apple", "golden_apple", "rotten_apple", "bomb", "power_up", "player_name"),
        object_speed=285.0,
        spawn_weights=(
            ("regular_apple", 0.735),
            ("golden_apple", 0.10),
            ("rotten_apple", 0.07),
            ("bomb", 0.04),
            ("power_up", 0.05),
            ("player_name", 0.005),
        ),
    ),
    difficulty_config=config.DifficultyConfig(
        score_interval=5,
        speed_increase=24.0,
        max_object_speed=540.0,
    ),
    wind_config=WindConfig(
        direction=vec2(1.0, 0.12),
        strength=16.0,
        gust_strength=6.5,
        gust_frequency=0.24,
        direction_sway=0.16,
    ),
    gameplay_wind_scale=3.8,
)

DIFFICULTY_PROFILES = (STANDARD,)
DEFAULT_DIFFICULTY_PROFILE = STANDARD
BEGINNER = STANDARD
INTERMEDIATE = STANDARD
EXPERT = STANDARD
