import random

from catch_the_apple import config
from catch_the_apple.entities import Apple


def random_apple_x() -> int:
    return random.randint(0, config.SCREEN_WIDTH - config.APPLE_SIZE)


def create_apple() -> Apple:
    return Apple(x=random_apple_x())


def reset_apple(apple: Apple) -> None:
    apple.x = random_apple_x()
    apple.y = -apple.size
