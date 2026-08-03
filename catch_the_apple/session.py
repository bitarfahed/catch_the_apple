from dataclasses import dataclass

from catch_the_apple import config


@dataclass
class GameSession:
    score: int = 0
    lives: int = config.INITIAL_LIVES
    combo: int = 0
    running: bool = True
    game_over: bool = False
    debug_collision_enabled: bool = False
