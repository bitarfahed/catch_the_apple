from dataclasses import dataclass

import pygame

from catch_the_apple.math2d import Vector2, clamp, vec2


@dataclass(frozen=True)
class DirectionalLight:
    direction: Vector2
    intensity: float = 0.45
    color: tuple[int, int, int] = (255, 244, 210)


@dataclass(frozen=True)
class LightingConfig:
    ambient: float = 0.78
    directional: DirectionalLight = DirectionalLight(direction=vec2(-0.65, 0.45), intensity=0.42)
    specular_intensity: float = 0.22
    shadow_intensity: float = 0.34
    ground_y: int = 570


class LightingSystem:
    def __init__(self, lighting_config: LightingConfig | None = None) -> None:
        self.config = lighting_config or LightingConfig()
        self._lit_surface_cache: dict[tuple[int, tuple[int, int], float, float, float], pygame.Surface] = {}
        self._shadow_cache: dict[tuple[int, int, int], pygame.Surface] = {}

    def apply_lighting(self, surface: pygame.Surface, height_factor: float = 0.0) -> pygame.Surface:
        cache_key = (
            id(surface),
            surface.get_size(),
            self.config.ambient,
            self.config.directional.intensity,
            height_factor,
        )
        if cache_key not in self._lit_surface_cache:
            self._lit_surface_cache[cache_key] = self._create_lit_surface(surface, height_factor)
        return self._lit_surface_cache[cache_key]

    def get_ground_shadow(self, width: int, height: int, height_factor: float = 0.0) -> pygame.Surface:
        shadow_width = max(4, int(width * (1.35 - height_factor * 0.35)))
        shadow_height = max(3, int(height * (0.34 - height_factor * 0.14)))
        alpha = int(255 * self.config.shadow_intensity * (1.0 - height_factor * 0.55))
        cache_key = (shadow_width, shadow_height, alpha)
        if cache_key not in self._shadow_cache:
            self._shadow_cache[cache_key] = self._create_shadow_surface(shadow_width, shadow_height, alpha)
        return self._shadow_cache[cache_key]

    def get_shadow_offset(self, height_factor: float = 0.0) -> tuple[int, int]:
        direction = self.config.directional.direction
        length = direction.length() or 1.0
        normalized = direction / length
        distance = int(18 * self.config.directional.intensity * (0.4 + height_factor))
        return int(-normalized.x * distance), int(normalized.y * distance)

    def estimate_height_factor(self, top: float, object_height: int) -> float:
        ground_clearance = max(0.0, self.config.ground_y - (top + object_height))
        return clamp(ground_clearance / self.config.ground_y, 0.0, 1.0)

    def _create_lit_surface(self, source: pygame.Surface, height_factor: float) -> pygame.Surface:
        lit = source.copy().convert_alpha()
        ambient_value = int(255 * self.config.ambient)
        ambient_surface = pygame.Surface(lit.get_size(), pygame.SRCALPHA)
        ambient_surface.fill((ambient_value, ambient_value, ambient_value, 255))
        lit.blit(ambient_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        width, height = lit.get_size()
        diffuse_strength = self.config.directional.intensity * (0.75 + height_factor * 0.20)
        diffuse = pygame.Surface((width, height), pygame.SRCALPHA)
        diffuse.fill((*scale_color(self.config.directional.color, diffuse_strength), 0))
        pygame.draw.ellipse(
            diffuse,
            (*scale_color(self.config.directional.color, diffuse_strength), 115),
            pygame.Rect(-width * 0.10, -height * 0.20, width * 0.82, height * 0.92),
        )
        lit.blit(diffuse, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        specular = pygame.Surface((width, height), pygame.SRCALPHA)
        specular_alpha = int(180 * self.config.specular_intensity)
        pygame.draw.ellipse(
            specular,
            (255, 255, 245, specular_alpha),
            pygame.Rect(width * 0.22, height * 0.18, width * 0.22, height * 0.18),
        )
        lit.blit(specular, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return lit

    def _create_shadow_surface(self, width: int, height: int, alpha: int) -> pygame.Surface:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        for inset in range(max(1, height // 2)):
            current_alpha = max(0, int(alpha * (1.0 - inset / max(1, height // 2))))
            rect = pygame.Rect(inset * 2, inset, width - inset * 4, height - inset * 2)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.ellipse(surface, (0, 0, 0, current_alpha), rect)
        return surface.convert_alpha()


def scale_color(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(channel * factor))) for channel in color)
