from dataclasses import dataclass

from catch_the_apple.math2d import clamp


@dataclass
class SquashStretch:
    duration: float
    strength: float
    elapsed: float = 0.0
    active: bool = False

    def trigger(self, strength: float | None = None) -> None:
        if strength is not None:
            self.strength = strength
        self.elapsed = 0.0
        self.active = True

    def update(self, delta_time: float) -> None:
        if not self.active:
            return
        self.elapsed += delta_time
        if self.elapsed >= self.duration:
            self.active = False
            self.elapsed = self.duration

    @property
    def scale(self) -> tuple[float, float]:
        if not self.active or self.duration <= 0.0:
            return 1.0, 1.0
        progress = clamp(self.elapsed / self.duration, 0.0, 1.0)
        pulse = (1.0 - progress) * self.strength
        return 1.0 + pulse, 1.0 - pulse * 0.55
