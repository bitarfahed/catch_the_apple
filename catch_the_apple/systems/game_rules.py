from catch_the_apple import config
from catch_the_apple.collision import collides
from catch_the_apple.session import GameSession
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.scoring import add_score, lose_life
from catch_the_apple.systems.spawning import reset_falling_object
from catch_the_apple.world import World


def apply_game_rules(world: World, session: GameSession) -> None:
    apple = world.apple

    if apple.y > config.SCREEN_HEIGHT:
        lose_life(session)
        reset_falling_object(apple)
        if session.lives <= 0:
            session.running = False

    if collides(world.basket, apple):
        add_score(session)
        reset_falling_object(apple)
        apply_score_progression(session.score, apple)
