from dataclasses import dataclass, field
import random

from catch_the_apple.math2d import clamp


@dataclass(frozen=True)
class SuperPowerDefinition:
    identifier: str
    display_name: str
    duration: float
    spawn_weight: float
    cheat_code: str
    math_model: str
    visual_color: tuple[int, int, int]


@dataclass
class ActiveSuperPower:
    definition: SuperPowerDefinition
    remaining: float


@dataclass
class SuperPowerState:
    active: dict[str, ActiveSuperPower] = field(default_factory=dict)

    def activate(self, definition: SuperPowerDefinition) -> None:
        self.active[definition.identifier] = ActiveSuperPower(definition, definition.duration)

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


SUPER_POWER_DEFINITIONS = {
    "magnet": SuperPowerDefinition(
        "magnet",
        "Magnet",
        duration=15.0,
        spawn_weight=0.26,
        cheat_code="MAGNET",
        math_model="Attractive acceleration: a = clamp(k(target_x - x), -amax, amax), with clamped velocity.",
        visual_color=(255, 235, 110),
    ),
    "slow_motion": SuperPowerDefinition(
        "slow_motion",
        "Time Warp",
        duration=8.0,
        spawn_weight=0.20,
        cheat_code="TIME",
        math_model="Time scaling: dt' = s * dt where 0 < s < 1.",
        visual_color=(100, 230, 255),
    ),
    "speed_boost": SuperPowerDefinition(
        "speed_boost",
        "Dash Boost",
        duration=7.0,
        spawn_weight=0.20,
        cheat_code="DASH",
        math_model="Velocity scaling: vmax' = alpha * vmax and dash' = alpha * dash.",
        visual_color=(145, 255, 170),
    ),
    "wind_control": SuperPowerDefinition(
        "wind_control",
        "Wind Control",
        duration=10.0,
        spawn_weight=0.08,
        cheat_code="WIND",
        math_model="Vector field boost: wind' = beta * wind + control_bias.",
        visual_color=(170, 235, 255),
    ),
    "shockwave": SuperPowerDefinition(
        "shockwave",
        "Shockwave",
        duration=1.2,
        spawn_weight=0.07,
        cheat_code="WAVE",
        math_model="Radial impulse: p' = p + normalize(p-c) * I * falloff(r).",
        visual_color=(255, 245, 190),
    ),
    "black_hole": SuperPowerDefinition(
        "black_hole",
        "Black Hole",
        duration=7.0,
        spawn_weight=0.06,
        cheat_code="VOID",
        math_model="Inverse-distance attraction: a = G(center - p) / (r^2 + epsilon).",
        visual_color=(180, 120, 255),
    ),
    "gravity_control": SuperPowerDefinition(
        "gravity_control",
        "Gravity Control",
        duration=9.0,
        spawn_weight=0.06,
        cheat_code="GRAV",
        math_model="Gravity scaling: vertical velocity uses g' = gamma * g.",
        visual_color=(160, 210, 255),
    ),
    "golden_rain": SuperPowerDefinition(
        "golden_rain",
        "Golden Rain",
        duration=10.0,
        spawn_weight=0.04,
        cheat_code="GOLD",
        math_model="Weighted sampling override: P(golden) -> high while active.",
        visual_color=(255, 220, 70),
    ),
    "freeze_bombs": SuperPowerDefinition(
        "freeze_bombs",
        "Freeze Bombs",
        duration=8.0,
        spawn_weight=0.03,
        cheat_code="FREEZE",
        math_model="Selective velocity mask: v_hazard = 0 for hazardous objects.",
        visual_color=(170, 245, 255),
    ),
}


class SuperPowerSystem:
    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)
        self.definitions = tuple(SUPER_POWER_DEFINITIONS.values())

    def choose_power(self) -> SuperPowerDefinition:
        return self.random.choices(
            self.definitions,
            weights=[definition.spawn_weight for definition in self.definitions],
            k=1,
        )[0]

    def by_cheat_code(self, code: str) -> SuperPowerDefinition | None:
        normalized = code.strip().upper()
        for definition in self.definitions:
            if definition.cheat_code == normalized or definition.identifier.upper() == normalized:
                return definition
        return None


def simulation_time_scale(state: SuperPowerState) -> float:
    scale = 0.48 if state.is_active("slow_motion") else 1.0
    if state.is_active("gravity_control"):
        scale *= 0.82
    return scale


def difficulty_growth_scale(state: SuperPowerState) -> float:
    return 0.40 if state.is_active("slow_motion") else 1.0


def basket_speed_scale(state: SuperPowerState) -> float:
    return 1.35 if state.is_active("speed_boost") else 1.0


def magnet_active_object_bonus(state: SuperPowerState) -> int:
    bonus = 5 if state.is_active("magnet") else 0
    if state.is_active("golden_rain"):
        bonus += 3
    return bonus


def wind_control_scale(state: SuperPowerState) -> float:
    return 2.3 if state.is_active("wind_control") else 1.0


def object_falling_scale(identifier: str, category: str, state: SuperPowerState) -> float:
    if state.is_active("freeze_bombs") and category == "hazard":
        return 0.0
    if state.is_active("gravity_control"):
        return 0.55
    return 1.0


def golden_rain_weight_multiplier(identifier: str, state: SuperPowerState) -> float:
    if not state.is_active("golden_rain"):
        return 1.0
    if identifier == "golden_apple":
        return 8.0
    if identifier in {"rotten_apple", "bomb"}:
        return 0.15
    return 0.75


def apply_magnet_pull(world, delta_time: float, state: SuperPowerState) -> None:
    if not state.is_active("magnet"):
        for falling_object in world.falling_objects:
            falling_object.magnet_velocity.x *= max(0.0, 1.0 - 7.0 * delta_time)
        return
    basket_center_x = world.basket.rect.centerx
    for falling_object in world.falling_objects:
        if falling_object.definition.identifier not in {"regular_apple", "golden_apple"}:
            falling_object.magnet_velocity.update(0.0, 0.0)
            continue
        offset = basket_center_x - falling_object.center.x
        acceleration = clamp(offset * 18.0, -1800.0, 1800.0)
        falling_object.magnet_velocity.x += acceleration * delta_time
        falling_object.magnet_velocity.x = clamp(falling_object.magnet_velocity.x, -360.0, 360.0)
        falling_object.x += falling_object.magnet_velocity.x * delta_time


def apply_black_hole(world, delta_time: float, state: SuperPowerState) -> None:
    if not state.is_active("black_hole"):
        return
    center_x = 400.0
    for falling_object in world.falling_objects:
        offset = center_x - falling_object.center.x
        distance = max(28.0, abs(offset))
        pull = clamp(18000.0 * offset / (distance * distance), -210.0, 210.0)
        falling_object.x += pull * delta_time


def apply_shockwave(world, delta_time: float, state: SuperPowerState) -> None:
    if not state.is_active("shockwave"):
        return
    origin_x = world.basket.rect.centerx
    for falling_object in world.falling_objects:
        offset = falling_object.center.x - origin_x
        direction = 1.0 if offset >= 0.0 else -1.0
        falloff = max(0.15, 1.0 - min(1.0, abs(offset) / 420.0))
        falling_object.x += direction * 360.0 * falloff * delta_time
