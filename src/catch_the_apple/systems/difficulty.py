from catch_the_apple import config
from catch_the_apple.systems.spawning import SpawnSystem


def apply_score_progression(
    score: int,
    spawn_system: SpawnSystem,
    difficulty_config: config.DifficultyConfig = config.DIFFICULTY_CONFIG,
    growth_scale: float = 1.0,
) -> bool:
    if score <= 0 or score % difficulty_config.score_interval != 0:
        return False

    spawn_system.current_object_speed = min(
        difficulty_config.max_object_speed,
        spawn_system.current_object_speed + difficulty_config.speed_increase * growth_scale,
    )
    return True
