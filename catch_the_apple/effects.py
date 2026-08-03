from dataclasses import dataclass, field

import pygame

from catch_the_apple.animation import SquashStretch
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent
from catch_the_apple.math2d import vec2
from catch_the_apple.particles import EmitterConfig, ParticleSystem
from catch_the_apple.world import World


APPLE_CATCH_BURST = EmitterConfig(
    count=18,
    speed_min=70.0,
    speed_max=190.0,
    lifetime_min=0.22,
    lifetime_max=0.48,
    start_size=4.0,
    end_size=1.0,
    start_alpha=220,
    end_alpha=0,
    start_color=(255, 120, 90),
    end_color=(255, 230, 110),
    drag=2.2,
    gravity_scale=0.25,
)

GOLDEN_SPARKLE = EmitterConfig(
    count=14,
    speed_min=40.0,
    speed_max=120.0,
    lifetime_min=0.24,
    lifetime_max=0.60,
    start_size=3.0,
    end_size=0.5,
    start_alpha=230,
    end_alpha=0,
    start_color=(255, 245, 130),
    end_color=(255, 180, 40),
    drag=1.0,
    gravity_scale=-0.05,
)

BOMB_SMOKE = EmitterConfig(
    count=16,
    speed_min=20.0,
    speed_max=90.0,
    lifetime_min=0.45,
    lifetime_max=0.90,
    start_size=7.0,
    end_size=14.0,
    start_alpha=150,
    end_alpha=0,
    start_color=(80, 80, 80),
    end_color=(30, 30, 30),
    drag=1.6,
    gravity_scale=-0.15,
)

MOTION_TRAIL = EmitterConfig(
    count=1,
    speed_min=0.0,
    speed_max=18.0,
    lifetime_min=0.12,
    lifetime_max=0.22,
    start_size=8.0,
    end_size=2.0,
    start_alpha=85,
    end_alpha=0,
    start_color=(255, 240, 210),
    end_color=(255, 240, 210),
    drag=1.0,
)

BASKET_DASH_TRAIL = EmitterConfig(
    count=2,
    speed_min=10.0,
    speed_max=55.0,
    lifetime_min=0.12,
    lifetime_max=0.24,
    start_size=10.0,
    end_size=3.0,
    start_alpha=120,
    end_alpha=0,
    start_color=(230, 180, 90),
    end_color=(120, 80, 40),
    drag=1.8,
)


@dataclass
class VisualEffects:
    particles: ParticleSystem = field(default_factory=ParticleSystem)
    basket_squash: SquashStretch = field(default_factory=lambda: SquashStretch(0.16, 0.08))
    object_squash: dict[int, SquashStretch] = field(default_factory=dict)
    _trail_timer: float = 0.0

    def handle_events(self, events: list[GameplayEvent]) -> None:
        for event in events:
            if isinstance(event, ObjectCaughtEvent):
                self.particles.emit(event.position, APPLE_CATCH_BURST)
                self.object_squash_for(event.falling_object).trigger(0.18)

    def update(self, world: World, delta_time: float) -> None:
        self._trail_timer = max(0.0, self._trail_timer - delta_time)
        self.basket_squash.update(delta_time)
        for animation in self.object_squash.values():
            animation.update(delta_time)

        if world.basket.current_speed > world.basket.max_speed * 0.45:
            self.basket_squash.trigger(0.05)

        if world.basket.movement.is_dashing:
            self.emit_basket_dash_trail(world)

        if self._trail_timer <= 0.0:
            self.emit_motion_trails(world)
            self._trail_timer = 0.045

        self.particles.update(delta_time)

    def emit_motion_trails(self, world: World) -> None:
        for falling_object in world.falling_objects:
            if falling_object.speed > 260.0:
                self.particles.emit(falling_object.center, MOTION_TRAIL)

    def emit_basket_dash_trail(self, world: World) -> None:
        basket = world.basket
        position = vec2(basket.rect.centerx, basket.rect.centery)
        self.particles.emit(position, BASKET_DASH_TRAIL)

    def object_squash_for(self, falling_object: object) -> SquashStretch:
        key = id(falling_object)
        if key not in self.object_squash:
            self.object_squash[key] = SquashStretch(0.18, 0.12)
        return self.object_squash[key]

    def object_scale(self, falling_object: object) -> tuple[float, float]:
        return self.object_squash_for(falling_object).scale
