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


BEGINNER = DifficultyProfile(
    identifier="beginner",
    display_name="Beginner",
    description="Relaxed speed, gentle growth, light wind.",
    spawn_config=config.SpawnConfig(
        max_active_objects=1,
        object_speed=240.0,
        spawn_weights=(("regular_apple", 1.0),),
    ),
    difficulty_config=config.DifficultyConfig(
        score_interval=6,
        speed_increase=18.0,
        max_object_speed=420.0,
    ),
    wind_config=WindConfig(
        direction=vec2(1.0, 0.08),
        strength=5.0,
        gust_strength=2.0,
        gust_frequency=0.18,
        direction_sway=0.08,
    ),
    gameplay_wind_scale=0.28,
)

INTERMEDIATE = DifficultyProfile(
    identifier="intermediate",
    display_name="Intermediate",
    description="Balanced pace with steady difficulty growth.",
    spawn_config=config.SpawnConfig(
        max_active_objects=1,
        object_speed=285.0,
        spawn_weights=(("regular_apple", 1.0),),
    ),
    difficulty_config=config.DifficultyConfig(
        score_interval=5,
        speed_increase=24.0,
        max_object_speed=540.0,
    ),
    wind_config=WindConfig(
        direction=vec2(1.0, 0.12),
        strength=9.0,
        gust_strength=3.5,
        gust_frequency=0.24,
        direction_sway=0.12,
    ),
    gameplay_wind_scale=0.35,
)

EXPERT = DifficultyProfile(
    identifier="expert",
    display_name="Expert",
    description="Faster start, stronger wind, two active apples.",
    spawn_config=config.SpawnConfig(
        max_active_objects=2,
        object_speed=330.0,
        spawn_weights=(("regular_apple", 1.0),),
    ),
    difficulty_config=config.DifficultyConfig(
        score_interval=4,
        speed_increase=30.0,
        max_object_speed=660.0,
    ),
    wind_config=WindConfig(
        direction=vec2(1.0, 0.16),
        strength=14.0,
        gust_strength=5.0,
        gust_frequency=0.30,
        direction_sway=0.18,
    ),
    gameplay_wind_scale=0.42,
)

DIFFICULTY_PROFILES = (BEGINNER, INTERMEDIATE, EXPERT)
DEFAULT_DIFFICULTY_PROFILE = INTERMEDIATE
