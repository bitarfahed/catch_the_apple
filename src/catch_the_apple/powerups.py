from dataclasses import dataclass, field
import random

from catch_the_apple.math2d import clamp


@dataclass(frozen=True)
class PowerUpDefinition:
    identifier: str
    display_name: str
    duration: float
    spawn_weight: float


@dataclass
class ActivePowerUp:
    definition: PowerUpDefinition
    remaining: float


@dataclass
class PowerUpState:
    active: dict[str, ActivePowerUp] = field(default_factory=dict)

    def activate(self, definition: PowerUpDefinition) -> None:
        self.active[definition.identifier] = ActivePowerUp(definition, definition.duration)

    def update(self, delta_time: float) -> None:
        expired: list[str] = []
        for identifier, active in self.active.items():
            active.remaining = max(0.0, active.remaining - delta_time)
            if active.remaining <= 0.0:
                expired.append(identifier)
        for identifier in expired:
            del self.active[identifier]

    def is_active(self, identifier: str) -> bool:
        return identifier in self.active

    def remaining(self, identifier: str) -> float:
        active = self.active.get(identifier)
        return active.remaining if active is not None else 0.0

    def labels(self) -> tuple[str, ...]:
        return tuple(
            f"{active.definition.display_name} {active.remaining:0.0f}s"
            for active in self.active.values()
        )


POWER_UP_DEFINITIONS = {
    "magnet": PowerUpDefinition("magnet", "Magnet", duration=15.0, spawn_weight=0.35),
    "slow_motion": PowerUpDefinition("slow_motion", "Slow Motion", duration=8.0, spawn_weight=0.30),
    "speed_boost": PowerUpDefinition("speed_boost", "Speed Boost", duration=7.0, spawn_weight=0.35),
}


class PowerUpSystem:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)
        self.definitions = tuple(POWER_UP_DEFINITIONS.values())

    def choose_power_up(self) -> PowerUpDefinition:
        return self.random.choices(
            self.definitions,
            weights=[definition.spawn_weight for definition in self.definitions],
            k=1,
        )[0]


def power_up_time_scale(state: PowerUpState) -> float:
    return 0.68 if state.is_active("slow_motion") else 1.0


def difficulty_growth_scale(state: PowerUpState) -> float:
    return 0.55 if state.is_active("slow_motion") else 1.0


def basket_speed_scale(state: PowerUpState) -> float:
    return 1.35 if state.is_active("speed_boost") else 1.0


def magnet_active_object_bonus(state: PowerUpState) -> int:
    return 2 if state.is_active("magnet") else 0


def apply_magnet_pull(world, delta_time: float, state: PowerUpState) -> None:
    if not state.is_active("magnet"):
        return
    basket_center_x = world.basket.rect.centerx
    for falling_object in world.falling_objects:
        if "catchable" not in falling_object.definition.tags:
            continue
        offset = basket_center_x - falling_object.center.x
        falling_object.x += clamp(offset * 1.65 * delta_time, -150.0 * delta_time, 150.0 * delta_time)
