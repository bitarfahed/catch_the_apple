from catch_the_apple import config
from catch_the_apple.collision import collides
from catch_the_apple.session import GameSession
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.scoring import add_score, lose_life
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.world import World


def apply_game_rules(world: World, session: GameSession, spawn_system: SpawnSystem) -> None:
    for falling_object in list(world.falling_objects):
        if falling_object.y > config.SCREEN_HEIGHT:
            lose_life(session, falling_object.definition.damage)
            spawn_system.reset_falling_object(falling_object)
            if session.lives <= 0:
                session.running = False

        if collides(world.basket, falling_object):
            add_score(session, falling_object.definition.score_value)
            spawn_system.reset_falling_object(falling_object)
            apply_score_progression(session.score, falling_object)
