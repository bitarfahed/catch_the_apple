from dataclasses import dataclass, field


@dataclass(frozen=True)
class CheatDefinition:
    identifier: str
    display_name: str
    duration: float
    math_model: str


@dataclass
class ActiveCheat:
    definition: CheatDefinition
    remaining: float
    value: float | None = None


@dataclass
class CheatState:
    active: dict[str, ActiveCheat] = field(default_factory=dict)

    def activate(self, definition: CheatDefinition, value: float | None = None) -> None:
        self.active[definition.identifier] = ActiveCheat(definition, definition.duration, value)

    def deactivate(self, identifier: str) -> None:
        self.active.pop(identifier, None)

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

    def value(self, identifier: str, default: float = 0.0) -> float:
        active = self.active.get(identifier)
        if active is None or active.value is None:
            return default
        return active.value

    def labels(self) -> tuple[str, ...]:
        return tuple(
            f"{active.definition.display_name} {active.remaining:0.0f}s"
            for active in self.active.values()
        )


CHEAT_DEFINITIONS = {
    "easy": CheatDefinition(
        "easy",
        "Easy Mode",
        20.0,
        "Time scaling: falling-object dt is multiplied by 0.55.",
    ),
    "wind": CheatDefinition(
        "wind",
        "Rain",
        20.0,
        "Vector field and particle simulation: weather state emits rain particles.",
    ),
    "shield": CheatDefinition(
        "shield",
        "Shield",
        20.0,
        "Collision filtering: bomb damage is masked while active.",
    ),
    "cycle": CheatDefinition(
        "cycle",
        "Cycle",
        20.0,
        "Modulo arithmetic: basket x wraps with x mod screen_width.",
    ),
    "flip": CheatDefinition(
        "flip",
        "Flip",
        20.0,
        "Rotation transform: p' = R(theta)(p - c) + c.",
    ),
    "fahed": CheatDefinition(
        "fahed",
        "Fahed Mode",
        20.0,
        "Scaling and collision geometry: basket width expands and apples auto-collect.",
    ),
}
