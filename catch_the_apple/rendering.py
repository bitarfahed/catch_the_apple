import pygame

from catch_the_apple import config
from catch_the_apple.collision import build_basket_collision_model
from catch_the_apple.effects import VisualEffects
from catch_the_apple.lighting import LightingSystem
from catch_the_apple.procedural_assets import ProceduralAssetRenderer
from catch_the_apple.session import GameSession
from catch_the_apple.world import World


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)
        self.assets = ProceduralAssetRenderer()
        self.lighting = LightingSystem()
        self._particle_surface_cache: dict[tuple[int, tuple[int, int, int], int], pygame.Surface] = {}

    def render(self, world: World, session: GameSession, effects: VisualEffects | None = None) -> None:
        self.screen.fill(config.BLUE)

        basket_surface = self.assets.get_basket_surface(world.basket.width, world.basket.height)
        basket_surface = self.lighting.apply_lighting(basket_surface)
        basket_scale = effects.basket_squash.scale if effects is not None else (1.0, 1.0)
        self.blit_scaled(basket_surface, world.basket.rect, basket_scale)
        for falling_object in world.falling_objects:
            object_surface = self.assets.get_falling_object_surface(
                falling_object.definition.identifier,
                falling_object.size,
                falling_object.definition.color,
            )
            height_factor = self.lighting.estimate_height_factor(falling_object.y, falling_object.size)
            self.render_ground_shadow(falling_object.rect, height_factor)
            object_surface = self.lighting.apply_lighting(object_surface, height_factor)
            object_scale = effects.object_scale(falling_object) if effects is not None else (1.0, 1.0)
            self.blit_scaled(object_surface, falling_object.rect, object_scale)

        if effects is not None:
            self.render_particles(effects)

        if session.debug_collision_enabled:
            self.render_debug_collision_overlay(world)

        score_text = self.font.render(f"Score: {session.score}", True, config.WHITE)
        lives_text = self.font.render(f"Lives: {session.lives}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (config.SCREEN_WIDTH - 120, 10))

    def blit_scaled(
        self,
        surface: pygame.Surface,
        rect: pygame.Rect,
        scale: tuple[float, float],
    ) -> None:
        if scale == (1.0, 1.0):
            self.screen.blit(surface, rect)
            return
        width = max(1, int(rect.width * scale[0]))
        height = max(1, int(rect.height * scale[1]))
        scaled_surface = pygame.transform.smoothscale(surface, (width, height))
        scaled_rect = scaled_surface.get_rect(center=rect.center)
        self.screen.blit(scaled_surface, scaled_rect)

    def render_particles(self, effects: VisualEffects) -> None:
        for particle in effects.particles.active_particles():
            if particle.alpha <= 0:
                continue
            radius = max(1, int(particle.size / 2))
            surface = self.get_particle_surface(radius, particle.color, particle.alpha)
            rect = surface.get_rect(center=(int(particle.position.x), int(particle.position.y)))
            self.screen.blit(surface, rect)

    def get_particle_surface(
        self,
        radius: int,
        color: tuple[int, int, int],
        alpha: int,
    ) -> pygame.Surface:
        key = (radius, color, alpha)
        if key not in self._particle_surface_cache:
            size = radius * 2
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            pygame.draw.circle(surface, (*color, alpha), (radius, radius), radius)
            self._particle_surface_cache[key] = surface.convert_alpha()
        return self._particle_surface_cache[key]

    def render_ground_shadow(self, object_rect: pygame.Rect, height_factor: float) -> None:
        shadow_surface = self.lighting.get_ground_shadow(object_rect.width, object_rect.height, height_factor)
        offset_x, offset_y = self.lighting.get_shadow_offset(height_factor)
        shadow_x = object_rect.centerx - shadow_surface.get_width() // 2 + offset_x
        shadow_y = self.lighting.config.ground_y - shadow_surface.get_height() // 2 + offset_y
        self.screen.blit(shadow_surface, (shadow_x, shadow_y))

    def render_debug_collision_overlay(self, world: World) -> None:
        model = build_basket_collision_model(world.basket)
        pygame.draw.rect(self.screen, config.YELLOW, model.catch_region, 2)
        pygame.draw.rect(self.screen, config.MAGENTA, model.left_rim, 2)
        pygame.draw.rect(self.screen, config.MAGENTA, model.right_rim, 2)
        pygame.draw.rect(self.screen, config.CYAN, model.body, 2)

        for falling_object in world.falling_objects:
            center = falling_object.center
            previous_center = falling_object.previous_center
            pygame.draw.circle(
                self.screen,
                config.YELLOW,
                (int(center.x), int(center.y)),
                int(falling_object.radius),
                2,
            )
            pygame.draw.line(
                self.screen,
                config.ORANGE,
                (int(previous_center.x), int(previous_center.y)),
                (int(center.x), int(center.y)),
                2,
            )
