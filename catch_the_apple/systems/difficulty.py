from catch_the_apple import config
from catch_the_apple.entities import FallingObject


def apply_score_progression(score: int, falling_object: FallingObject) -> None:
    if score % 5 == 0:
        falling_object.speed += config.APPLE_SPEED_INCREASE
