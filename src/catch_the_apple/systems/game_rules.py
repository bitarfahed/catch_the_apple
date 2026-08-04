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
    update_beneficial_groups(world, session)
    mark_current_beneficial_catches(world, session)
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
            storm_bonus_object = (
                session.powerups.is_active("magnet")
                and definition.identifier in {"regular_apple", "golden_apple"}
            )
            if definition.identifier == "regular_apple" and not storm_bonus_object:
                if not beneficial_group_has_catch(session, falling_object):
                    subtract_score(session, 2)
            spawn_system.reset_falling_object(falling_object)
            events.append(
                ObjectMissedEvent(
                    falling_object=falling_object,
                    position=missed_position,
                    damage=0,
                    object_identifier=definition.identifier,
                )
            )
            update_game_over_conditions(session)
            continue

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
                update_game_over_conditions(session)
                continue

            if definition.identifier == "bomb":
                shielded = (
                    session.cheats.is_active("shield")
                    and definition.identifier == "bomb"
                ) or session.cheats.is_active("fahed")
                damage = 0 if shielded else definition.damage
                if damage > 0:
                    lose_life(session, damage)
                spawn_system.reset_falling_object(falling_object)
                events.append(
                    ObjectMissedEvent(
                        falling_object=falling_object,
                        position=caught_position,
                        damage=damage,
                        object_identifier=definition.identifier,
                    )
                )
                update_game_over_conditions(session)
                continue

            if definition.category == "power_up" and power_up_system is not None:
                session.powerups.activate(power_up_system.choose_power_up())
            elif definition.category == "extra_life":
                session.lives = min(config.INITIAL_LIVES, session.lives + 1)
            else:
                score_value = score_value_for_object(session, definition)
                if score_value > 0:
                    add_score(session, score_value)
                    mark_beneficial_group_caught(session, falling_object)

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
        update_game_over_conditions(session)
    cleanup_beneficial_groups(world, session)
    return events


def update_beneficial_groups(world: World, session: GameSession) -> None:
    visible_beneficial = [
        falling_object
        for falling_object in world.falling_objects
        if is_beneficial_object(falling_object.definition.identifier)
        and is_visible(falling_object)
    ]
    ungrouped = [
        falling_object
        for falling_object in visible_beneficial
        if falling_object.beneficial_group_id is None
    ]
    if len(visible_beneficial) >= 2 and ungrouped:
        group_id = session.next_beneficial_group_id
        session.next_beneficial_group_id += 1
        for falling_object in visible_beneficial:
            if falling_object.beneficial_group_id is None:
                falling_object.beneficial_group_id = group_id


def is_beneficial_object(identifier: str) -> bool:
    return identifier in {"regular_apple", "golden_apple"}


def is_visible(falling_object) -> bool:
    return falling_object.y <= config.SCREEN_HEIGHT and falling_object.y + falling_object.size >= 0


def mark_beneficial_group_caught(session: GameSession, falling_object) -> None:
    if falling_object.beneficial_group_id is not None:
        session.caught_beneficial_group_ids.add(falling_object.beneficial_group_id)


def mark_current_beneficial_catches(world: World, session: GameSession) -> None:
    for falling_object in world.falling_objects:
        if (
            is_beneficial_object(falling_object.definition.identifier)
            and falling_object.beneficial_group_id is not None
            and detect_basket_collision(world.basket, falling_object).caught
        ):
            mark_beneficial_group_caught(session, falling_object)


def beneficial_group_has_catch(session: GameSession, falling_object) -> bool:
    return (
        falling_object.beneficial_group_id is not None
        and falling_object.beneficial_group_id in session.caught_beneficial_group_ids
    )


def cleanup_beneficial_groups(world: World, session: GameSession) -> None:
    active_group_ids = {
        falling_object.beneficial_group_id
        for falling_object in world.falling_objects
        if falling_object.beneficial_group_id is not None
    }
    session.caught_beneficial_group_ids.intersection_update(active_group_ids)


def score_value_for_object(session: GameSession, definition: ObjectDefinition) -> int:
    if session.cheats.is_active("insane") and definition.identifier == "golden_apple":
        return 3
    return definition.score_value


def update_game_over_conditions(session: GameSession) -> None:
    if session.lives <= 0:
        session.game_over = True
    if session.has_earned_score and session.score <= 0:
        session.score = 0
        session.game_over = True
