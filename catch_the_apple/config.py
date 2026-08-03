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

BASKET_WIDTH = 100
BASKET_HEIGHT = 20
BASKET_Y_OFFSET = 10
BASKET_MAX_SPEED = 8 * FPS
BASKET_ACCELERATION = 3600.0
BASKET_DRAG = 4200.0
BASKET_DASH_SPEED = 900.0
BASKET_DASH_DURATION = 0.12
BASKET_DASH_COOLDOWN = 0.7

APPLE_SIZE = 30
APPLE_INITIAL_SPEED = 5 * FPS
APPLE_SPEED_INCREASE = 1 * FPS

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


SPAWN_CONFIG = SpawnConfig()

INITIAL_LIVES = 3
FONT_NAME = "Arial"
FONT_SIZE = 30
