import random

from catch_the_apple import config
from catch_the_apple.entities import Apple
from catch_the_apple.math2d import Transform2D, vec2


def random_falling_object_x() -> int:
    return random.randint(0, config.SCREEN_WIDTH - config.APPLE_SIZE)


def create_apple() -> Apple:
    return Apple(transform=Transform2D(position=vec2(random_falling_object_x(), -config.APPLE_SIZE)))


def reset_falling_object(falling_object: Apple) -> None:
    falling_object.x = random_falling_object_x()
    falling_object.y = -falling_object.size
