from catch_the_apple import config
from catch_the_apple.collision import detect_basket_collision
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.object_definitions import ObjectDefinition
from catch_the_apple.powerups import PowerUpSystem, difficulty_growth_scale
from catch_the_apple.session import GameSession
from catch_the_apple.systems.difficulty import apply_score_progression
from catch_the_apple.systems.scoring import add_score, lose_life, subtract_score
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
        if (
            session.cheats.is_active("fahed")
            and definition.identifier in {"regular_apple", "golden_apple"}
        ):
            caught_position = falling_object.center
            score_value = score_value_for_object(session, definition)
            if score_value > 0:
                add_score(session, score_value)
            spawn_system.reset_falling_object(falling_object)
            events.append(
                ObjectCaughtEvent(
                    falling_object=falling_object,
                    position=caught_position,
                    color=definition.color,
                    object_identifier=definition.identifier,
                )
            )
            continue
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
                    object_identifier=definition.identifier,
                )
            )
            if session.lives <= 0:
                session.game_over = True

        collision = detect_basket_collision(world.basket, falling_object)
        if collision.caught:
            caught_position = falling_object.center
            definition = falling_object.definition
            if definition.identifier == "rotten_apple":
                subtract_score(session, 2)
                spawn_system.reset_falling_object(falling_object)
                events.append(
                    ObjectCaughtEvent(
                        falling_object=falling_object,
                        position=caught_position,
                        color=definition.color,
                        object_identifier=definition.identifier,
                    )
                )
                update_score_loss_condition(session)
                continue

            if definition.identifier == "bomb":
                shielded = (
                    session.cheats.is_active("shield")
                    and definition.identifier == "bomb"
                ) or session.cheats.is_active("fahed")
                damage = 0 if shielded else definition.damage
                if damage > 0:
                    lose_life(session, damage)
                if session.lives <= 0:
                    session.game_over = True
                spawn_system.reset_falling_object(falling_object)
                events.append(
                    ObjectMissedEvent(
                        falling_object=falling_object,
                        position=caught_position,
                        damage=damage,
                        object_identifier=definition.identifier,
                    )
                )
                continue

            if definition.category == "power_up" and power_up_system is not None:
                session.powerups.activate(power_up_system.choose_power_up())
            elif definition.category == "extra_life":
                session.lives = min(config.INITIAL_LIVES, session.lives + 1)
            else:
                score_value = score_value_for_object(session, definition)
                if score_value > 0:
                    add_score(session, score_value)

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
                    object_identifier=definition.identifier,
                )
            )
        update_score_loss_condition(session)
    return events


def score_value_for_object(session: GameSession, definition: ObjectDefinition) -> int:
    if session.cheats.is_active("insane") and definition.identifier == "golden_apple":
        return 3
    return definition.score_value


def update_score_loss_condition(session: GameSession) -> None:
    if session.has_earned_score and session.score <= 0:
        session.score = 0
        session.game_over = True
