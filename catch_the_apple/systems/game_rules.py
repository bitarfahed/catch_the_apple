from catch_the_apple import config
from catch_the_apple.collision import detect_basket_collision
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent
from catch_the_apple.session import GameSession
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.scoring import add_score, lose_life
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.world import World


def apply_game_rules(
    world: World,
    session: GameSession,
    spawn_system: SpawnSystem,
) -> list[GameplayEvent]:
    events: list[GameplayEvent] = []
    for falling_object in list(world.falling_objects):
        if falling_object.y > config.SCREEN_HEIGHT:
            lose_life(session, falling_object.definition.damage)
            spawn_system.reset_falling_object(falling_object)
            if session.lives <= 0:
                session.running = False

        collision = detect_basket_collision(world.basket, falling_object)
        if collision.caught:
            caught_position = falling_object.center
            add_score(session, falling_object.definition.score_value)
            spawn_system.reset_falling_object(falling_object)
            apply_score_progression(session.score, falling_object)
            events.append(
                ObjectCaughtEvent(
                    falling_object=falling_object,
                    position=caught_position,
                    color=falling_object.definition.color,
                )
            )
    return events
