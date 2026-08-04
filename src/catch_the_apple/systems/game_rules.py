from catch_the_apple import config
from catch_the_apple.collision import detect_basket_collision
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.powerups import PowerUpSystem, difficulty_growth_scale
from catch_the_apple.session import GameSession
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.scoring import add_score, lose_life
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.world import World


def apply_game_rules(
    world: World,
    session: GameSession,
    spawn_system: SpawnSystem,
    difficulty_config: config.DifficultyConfig = config.DIFFICULTY_CONFIG,
    power_up_system: PowerUpSystem | None = None,
) -> list[GameplayEvent]:
    events: list[GameplayEvent] = []
    for falling_object in list(world.falling_objects):
        definition = falling_object.definition
        if falling_object.y > config.SCREEN_HEIGHT:
            missed_position = falling_object.center
            miss_damage = definition.damage if definition.category != "hazard" else 0
            storm_bonus_object = (
                session.powerups.is_active("magnet")
                and definition.identifier in {"regular_apple", "golden_apple"}
            )
            if not storm_bonus_object and miss_damage > 0:
                lose_life(session, miss_damage)
            spawn_system.reset_falling_object(falling_object)
            events.append(
                ObjectMissedEvent(
                    falling_object=falling_object,
                    position=missed_position,
                    damage=0 if storm_bonus_object else miss_damage,
                )
            )
            if session.lives <= 0:
                session.game_over = True

        collision = detect_basket_collision(world.basket, falling_object)
        if collision.caught:
            caught_position = falling_object.center
            definition = falling_object.definition
            if definition.category == "hazard":
                lose_life(session, definition.damage)
                if session.lives <= 0:
                    session.game_over = True
                spawn_system.reset_falling_object(falling_object)
                events.append(
                    ObjectMissedEvent(
                        falling_object=falling_object,
                        position=caught_position,
                        damage=definition.damage,
                    )
                )
                continue

            if definition.category == "power_up" and power_up_system is not None:
                session.powerups.activate(power_up_system.choose_power_up())
            elif definition.score_value > 0:
                add_score(session, definition.score_value)

            spawn_system.reset_falling_object(falling_object)
            if apply_score_progression(
                session.score,
                spawn_system,
                difficulty_config,
                difficulty_growth_scale(session.powerups),
            ):
                falling_object.speed = spawn_system.current_object_speed
            events.append(
                ObjectCaughtEvent(
                    falling_object=falling_object,
                    position=caught_position,
                    color=definition.color,
                )
            )
    return events
