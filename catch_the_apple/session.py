from dataclasses import dataclass

from catch_the_apple import config


@dataclass
class GameSession:
    score: int = 0
    lives: int = config.INITIAL_LIVES
    running: bool = True
