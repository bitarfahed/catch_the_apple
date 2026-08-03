from dataclasses import dataclass, field
import math
import random

import pygame

from catch_the_apple.math2d import Vector2, clamp, vec2


@dataclass
class Particle:
    position: Vector2 = field(default_factory=Vector2)
    velocity: Vector2 = field(default_factory=Vector2)
    acceleration: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    angular_velocity: float = 0.0
    lifetime: float = 0.0
    age: float = 0.0
    start_size: float = 1.0
    end_size: float = 1.0
    start_alpha: int = 255
    end_alpha: int = 0
    start_color: tuple[int, int, int] = (255, 255, 255)
    end_color: tuple[int, int, int] = (255, 255, 255)
    drag: float = 0.0
    gravity_scale: float = 0.0
    active: bool = False

    def reset(self, config: "ParticleConfig") -> None:
        self.position.update(config.position)
        self.velocity.update(config.velocity)
        self.acceleration.update(config.acceleration)
        self.rotation = config.rotation
        self.angular_velocity = config.angular_velocity
        self.lifetime = config.lifetime
        self.age = 0.0
        self.start_size = config.start_size
        self.end_size = config.end_size
        self.start_alpha = config.start_alpha
        self.end_alpha = config.end_alpha
        self.start_color = config.start_color
        self.end_color = config.end_color
        self.drag = config.drag
        self.gravity_scale = config.gravity_scale
        self.active = True

    def update(self, delta_time: float, gravity: Vector2) -> None:
        if not self.active:
            return
        self.age += delta_time
        if self.age >= self.lifetime:
            self.active = False
            return

        self.velocity += (self.acceleration + gravity * self.gravity_scale) * delta_time
        if self.drag > 0.0:
            self.velocity *= max(0.0, 1.0 - self.drag * delta_time)
        self.position += self.velocity * delta_time
        self.rotation += self.angular_velocity * delta_time

    @property
    def progress(self) -> float:
        if self.lifetime <= 0.0:
            return 1.0
        return clamp(self.age / self.lifetime, 0.0, 1.0)

    @property
    def size(self) -> float:
        return lerp(self.start_size, self.end_size, self.progress)

    @property
    def alpha(self) -> int:
        return int(lerp(self.start_alpha, self.end_alpha, self.progress))

    @property
    def color(self) -> tuple[int, int, int]:
        return tuple(
            int(lerp(start, end, self.progress))
            for start, end in zip(self.start_color, self.end_color, strict=True)
        )


@dataclass(frozen=True)
class ParticleConfig:
    position: Vector2
    velocity: Vector2
    acceleration: Vector2 = field(default_factory=Vector2)
    rotation: float = 0.0
    angular_velocity: float = 0.0
    lifetime: float = 0.4
    start_size: float = 4.0
    end_size: float = 1.0
    start_alpha: int = 220
    end_alpha: int = 0
    start_color: tuple[int, int, int] = (255, 255, 255)
    end_color: tuple[int, int, int] = (255, 255, 255)
    drag: float = 1.2
    gravity_scale: float = 0.0


@dataclass(frozen=True)
class EmitterConfig:
    count: int
    speed_min: float
    speed_max: float
    lifetime_min: float
    lifetime_max: float
    start_size: float
    end_size: float
    start_alpha: int
    end_alpha: int
    start_color: tuple[int, int, int]
    end_color: tuple[int, int, int]
    drag: float = 1.2
    gravity_scale: float = 0.0
    angular_velocity_min: float = -180.0
    angular_velocity_max: float = 180.0


class ParticleSystem:
    def __init__(self, pool_size: int = 400, seed: int | None = None) -> None:
        self.gravity = vec2(0.0, 600.0)
        self.random = random.Random(seed)
        self.particles = [Particle() for _ in range(pool_size)]
        self._next_index = 0

    def emit(self, position: Vector2, emitter: EmitterConfig) -> None:
        for _ in range(emitter.count):
            angle = self.random.uniform(0.0, math.tau)
            speed = self.random.uniform(emitter.speed_min, emitter.speed_max)
            velocity = vec2(math.cos(angle) * speed, math.sin(angle) * speed)
            particle_config = ParticleConfig(
                position=position,
                velocity=velocity,
                rotation=self.random.uniform(0.0, 360.0),
                angular_velocity=self.random.uniform(
                    emitter.angular_velocity_min,
                    emitter.angular_velocity_max,
                ),
                lifetime=self.random.uniform(emitter.lifetime_min, emitter.lifetime_max),
                start_size=emitter.start_size,
                end_size=emitter.end_size,
                start_alpha=emitter.start_alpha,
                end_alpha=emitter.end_alpha,
                start_color=emitter.start_color,
                end_color=emitter.end_color,
                drag=emitter.drag,
                gravity_scale=emitter.gravity_scale,
            )
            self._acquire_particle().reset(particle_config)

    def update(self, delta_time: float) -> None:
        for particle in self.particles:
            particle.update(delta_time, self.gravity)

    def active_particles(self):
        for particle in self.particles:
            if particle.active:
                yield particle

    def _acquire_particle(self) -> Particle:
        for _ in range(len(self.particles)):
            particle = self.particles[self._next_index]
            self._next_index = (self._next_index + 1) % len(self.particles)
            if not particle.active:
                return particle
        particle = self.particles[self._next_index]
        self._next_index = (self._next_index + 1) % len(self.particles)
        return particle


def lerp(start: float, end: float, amount: float) -> float:
    return start + (end - start) * amount
