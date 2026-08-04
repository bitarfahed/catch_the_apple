from dataclasses import dataclass

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
MAX_DELTA_TIME = 0.1

WINDOW_TITLE = "׳×׳₪׳•׳¡ ׳׳× ׳”׳×׳₪׳•׳—׳™׳!"

WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (34, 139, 34)
BLUE = (50, 153, 213)
YELLOW = (255, 230, 80)
MAGENTA = (220, 80, 220)
CYAN = (80, 220, 220)
ORANGE = (255, 160, 70)

BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BASKET_Y_OFFSET = 10
BASKET_MAX_SPEED = 8 * FPS
BASKET_ACCELERATION = 3600.0
BASKET_DRAG = 4200.0
BASKET_DASH_SPEED = 900.0
BASKET_DASH_DURATION = 0.12
BASKET_DASH_COOLDOWN = 0.7
BASKET_CATCH_REGION_HEIGHT = 10
BASKET_RIM_WIDTH = 8
BASKET_RIM_HEIGHT = 16

APPLE_SIZE = 30
APPLE_INITIAL_SPEED = 5 * FPS
APPLE_SPEED_INCREASE = 0.45 * FPS
APPLE_MAX_SPEED = 9 * FPS

DIFFICULTY_SCORE_INTERVAL = 5

RANDOM_SEED = None


@dataclass(frozen=True)
class SpawnConfig:
    max_active_objects: int = 1
    seed: int | None = RANDOM_SEED
    enabled_object_ids: tuple[str, ...] = ("regular_apple",)
    x_min: int = 0
    x_max: int = SCREEN_WIDTH - APPLE_SIZE
    spawn_y: int = -APPLE_SIZE
    object_speed: float = APPLE_INITIAL_SPEED
    spawn_weights: tuple[tuple[str, float], ...] = (("regular_apple", 1.0),)


@dataclass(frozen=True)
class DifficultyConfig:
    score_interval: int = DIFFICULTY_SCORE_INTERVAL
    speed_increase: float = APPLE_SPEED_INCREASE
    max_object_speed: float = APPLE_MAX_SPEED


SPAWN_CONFIG = SpawnConfig()
DIFFICULTY_CONFIG = DifficultyConfig()

INITIAL_LIVES = 3
FONT_NAME = "Arial"
FONT_SIZE = 30
