from dataclasses import dataclass

from catch_the_apple import config


@dataclass(frozen=True)
class ObjectDefinition:
    identifier: str
    display_name: str
    category: str
    score_value: int
    damage: int
    spawn_weight: float
    collision_size: int
    color: tuple[int, int, int]
    tags: tuple[str, ...] = ()
    future_behaviors: tuple[str, ...] = ()


OBJECT_DEFINITIONS = {
    "regular_apple": ObjectDefinition(
        identifier="regular_apple",
        display_name="Regular Apple",
        category="apple",
        score_value=1,
        damage=1,
        spawn_weight=1.0,
        collision_size=config.APPLE_SIZE,
        color=config.RED,
        tags=("catchable", "fruit"),
    ),
    "golden_apple": ObjectDefinition(
        identifier="golden_apple",
        display_name="Golden Apple",
        category="apple",
        score_value=5,
        damage=0,
        spawn_weight=0.0,
        collision_size=config.APPLE_SIZE,
        color=(255, 215, 0),
        tags=("catchable", "fruit", "bonus"),
        future_behaviors=("bonus_score",),
    ),
    "rotten_apple": ObjectDefinition(
        identifier="rotten_apple",
        display_name="Rotten Apple",
        category="hazard",
        score_value=0,
        damage=1,
        spawn_weight=0.0,
        collision_size=config.APPLE_SIZE,
        color=(92, 78, 43),
        tags=("catchable", "fruit", "penalty"),
        future_behaviors=("score_penalty",),
    ),
    "bomb": ObjectDefinition(
        identifier="bomb",
        display_name="Bomb",
        category="hazard",
        score_value=0,
        damage=1,
        spawn_weight=0.0,
        collision_size=config.APPLE_SIZE,
        color=(32, 32, 32),
        tags=("hazard",),
        future_behaviors=("explosion",),
    ),
    "power_up": ObjectDefinition(
        identifier="power_up",
        display_name="Power-Up",
        category="power_up",
        score_value=0,
        damage=0,
        spawn_weight=0.0,
        collision_size=config.APPLE_SIZE,
        color=(50, 153, 213),
        tags=("catchable", "power_up"),
        future_behaviors=("temporary_effect",),
    ),
}


def get_object_definition(identifier: str) -> ObjectDefinition:
    return OBJECT_DEFINITIONS[identifier]


def get_spawnable_definitions(identifiers: tuple[str, ...]) -> tuple[ObjectDefinition, ...]:
    return tuple(get_object_definition(identifier) for identifier in identifiers)
