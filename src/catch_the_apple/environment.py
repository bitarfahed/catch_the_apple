from dataclasses import dataclass
import math
import random

import pygame

from catch_the_apple import config
from catch_the_apple.dynamic_environment import EnvironmentState


@dataclass(frozen=True)
class EnvironmentLayer:
    name: str
    surface: pygame.Surface
    depth_factor: float
    scroll_speed: float


class ProceduralEnvironmentRenderer:
    def __init__(self, width: int, height: int, seed: int = 17) -> None:
        self.width = width
        self.height = height
        self.seed = seed
        self._layers: tuple[EnvironmentLayer, ...] | None = None

    def render(self, target: pygame.Surface, environment: EnvironmentState) -> None:
        for layer in self.layers:
            wind_scroll = environment.wind.velocity.x * 0.25
            offset = int(
                environment.elapsed_time * (layer.scroll_speed + wind_scroll) * layer.depth_factor
            ) % self.width
            target.blit(layer.surface, (-offset, 0))
            target.blit(layer.surface, (self.width - offset, 0))
        self._apply_environment_tint(target, environment)
        self._draw_sun_and_moon(target, environment)

    @property
    def layers(self) -> tuple[EnvironmentLayer, ...]:
        if self._layers is None:
            self._layers = self._create_layers()
        return self._layers

    def _create_layers(self) -> tuple[EnvironmentLayer, ...]:
        return (
            EnvironmentLayer("sky", self._create_sky_layer(), 0.05, 4.0),
            EnvironmentLayer("mountains", self._create_mountain_layer(), 0.16, 8.0),
            EnvironmentLayer("trees", self._create_tree_layer(), 0.35, 14.0),
            EnvironmentLayer("bushes", self._create_bush_layer(), 0.58, 22.0),
            EnvironmentLayer("grass", self._create_grass_layer(), 0.88, 32.0),
        )

    def _create_sky_layer(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height)).convert()
        top = (92, 174, 235)
        bottom = (76, 145, 204)
        for y in range(self.height):
            t = y / max(1, self.height - 1)
            color = blend_color(top, bottom, t)
            pygame.draw.line(surface, color, (0, y), (self.width, y))

        rng = random.Random(self.seed)
        for _ in range(11):
            x = rng.randint(-80, self.width)
            y = rng.randint(35, 215)
            scale = rng.uniform(0.65, 1.45)
            alpha = rng.randint(36, 70)
            self._draw_cloud(surface, x, y, scale, alpha, rng)
        return surface

    def _apply_environment_tint(self, target: pygame.Surface, environment: EnvironmentState) -> None:
        sky_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        half_height = self.height // 2
        for y in range(half_height):
            t = y / max(1, half_height - 1)
            color = blend_color(environment.day_night.sky_top, environment.day_night.sky_bottom, t)
            pygame.draw.line(sky_overlay, (*color, 135), (0, y), (self.width, y))
        tint = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tint.fill((*environment.weather.visual_tint, 28))
        target.blit(sky_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        target.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        if environment.weather.fog_alpha > 0:
            fog = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            fog.fill((220, 230, 230, environment.weather.fog_alpha))
            target.blit(fog, (0, 0))
        night_alpha = int(max(0.0, 0.55 - environment.day_night.ambient) * 210)
        if night_alpha > 0:
            night = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            night.fill((6, 10, 32, night_alpha))
            target.blit(night, (0, 0))

    def _draw_sun_and_moon(self, target: pygame.Surface, environment: EnvironmentState) -> None:
        daylight_alpha = int(environment.day_night.directional_intensity * 330)
        moon_alpha = int((1.0 - environment.day_night.ambient) * 260)
        pygame.draw.circle(target, (255, 231, 145, daylight_alpha), environment.day_night.sun_position, 30)
        pygame.draw.circle(target, (255, 245, 185, max(0, daylight_alpha // 3)), environment.day_night.sun_position, 45, 2)
        pygame.draw.circle(target, (215, 225, 245, moon_alpha), environment.day_night.moon_position, 22)
        pygame.draw.circle(target, (170, 190, 235, max(0, moon_alpha // 3)), environment.day_night.moon_position, 36, 2)

    def _create_mountain_layer(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rng = random.Random(self.seed + 1)
        base_y = int(self.height * 0.72)
        points = [(-60, base_y)]
        x = -60
        while x < self.width + 80:
            peak_y = rng.randint(int(self.height * 0.34), int(self.height * 0.55))
            points.append((x + rng.randint(60, 130), peak_y))
            x += rng.randint(120, 190)
            points.append((x, base_y))
        points.append((self.width + 80, base_y))
        points.append((self.width + 80, self.height))
        points.append((-60, self.height))
        pygame.draw.polygon(surface, (54, 93, 126, 210), points)
        pygame.draw.lines(surface, (95, 135, 160, 150), False, points[: max(2, len(points) - 2)], 2)
        return surface.convert_alpha()

    def _create_tree_layer(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rng = random.Random(self.seed + 2)
        ground_y = int(self.height * 0.84)
        for x in range(-20, self.width + 40, 42):
            trunk_height = rng.randint(32, 58)
            trunk_width = rng.randint(5, 8)
            pygame.draw.rect(
                surface,
                (83, 57, 36, 210),
                pygame.Rect(x, ground_y - trunk_height, trunk_width, trunk_height),
            )
            crown_color = rng.choice(((38, 104, 68, 220), (45, 122, 75, 220), (52, 132, 79, 220)))
            pygame.draw.circle(surface, crown_color, (x + trunk_width // 2, ground_y - trunk_height), rng.randint(18, 28))
            pygame.draw.circle(surface, crown_color, (x - 10, ground_y - trunk_height + 8), rng.randint(14, 22))
            pygame.draw.circle(surface, crown_color, (x + 14, ground_y - trunk_height + 10), rng.randint(14, 22))
        return surface.convert_alpha()

    def _create_bush_layer(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rng = random.Random(self.seed + 3)
        base_y = int(self.height * 0.91)
        for x in range(-30, self.width + 50, 30):
            radius = rng.randint(12, 24)
            color = rng.choice(((34, 125, 65, 230), (50, 145, 74, 230), (65, 158, 82, 230)))
            pygame.draw.circle(surface, color, (x, base_y + rng.randint(-8, 4)), radius)
        return surface.convert_alpha()

    def _create_grass_layer(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        rng = random.Random(self.seed + 4)
        ground_y = int(self.height * 0.94)
        pygame.draw.rect(surface, (46, 139, 73, 255), pygame.Rect(0, ground_y, self.width, self.height - ground_y))
        for x in range(0, self.width, 5):
            blade_height = rng.randint(8, 24)
            lean = rng.randint(-4, 4)
            color = rng.choice(((77, 178, 87, 255), (90, 194, 96, 255), (43, 125, 66, 255)))
            pygame.draw.line(surface, color, (x, ground_y + 4), (x + lean, ground_y - blade_height), 1)
        return surface.convert_alpha()

    def _draw_cloud(
        self,
        surface: pygame.Surface,
        x: int,
        y: int,
        scale: float,
        alpha: int,
        rng: random.Random,
    ) -> None:
        cloud = pygame.Surface((180, 70), pygame.SRCALPHA)
        for i in range(8):
            cx = int(18 + i * 20 + rng.randint(-8, 8))
            cy = int(34 + math.sin(i) * 6 + rng.randint(-4, 4))
            radius_x = int(rng.randint(22, 38) * scale)
            radius_y = int(rng.randint(10, 20) * scale)
            rect = pygame.Rect(cx - radius_x, cy - radius_y, radius_x * 2, radius_y * 2)
            pygame.draw.ellipse(cloud, (255, 255, 255, alpha), rect)
        surface.blit(cloud, (x, y))


def blend_color(
    start: tuple[int, int, int],
    end: tuple[int, int, int],
    amount: float,
) -> tuple[int, int, int]:
    return tuple(int(a + (b - a) * amount) for a, b in zip(start, end, strict=True))
