from dataclasses import dataclass, field

from catch_the_apple import config
from catch_the_apple.powerups import PowerUpState


@dataclass
class GameSession:
    player_name: str = ""
    score: int = 0
    lives: int = config.INITIAL_LIVES
    combo: int = 0
    best_combo: int = 0
    running: bool = True
    game_over: bool = False
    finalized: bool = False
    debug_collision_enabled: bool = False
    debug_overlay_enabled: bool = False
    powerups: PowerUpState = field(default_factory=PowerUpState)
