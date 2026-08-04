import pygame

from catch_the_apple import config
from catch_the_apple.collision import build_basket_collision_model
from catch_the_apple.dynamic_environment import EnvironmentState
from catch_the_apple.effects import VisualEffects
from catch_the_apple.environment import ProceduralEnvironmentRenderer
from catch_the_apple.lighting import LightingSystem
from catch_the_apple.math2d import clamp
from catch_the_apple.procedural_assets import ProceduralAssetRenderer
from catch_the_apple.session import GameSession
from catch_the_apple.world import World


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = make_font(config.FONT_SIZE)
        self.assets = ProceduralAssetRenderer()
        self.environment = ProceduralEnvironmentRenderer(config.SCREEN_WIDTH, config.SCREEN_HEIGHT)
        self.lighting = LightingSystem()
        self._particle_surface_cache: dict[tuple[int, tuple[int, int, int], int], pygame.Surface] = {}
        self._glow_surface_cache: dict[tuple[int, tuple[int, int, int], int], pygame.Surface] = {}
        self.world_rotation_angle = 0.0
        self.elapsed_time = 0.0

    def render(
        self,
        world: World,
        session: GameSession,
        effects: VisualEffects | None = None,
        delta_time: float = 0.0,
        environment_state: EnvironmentState | None = None,
    ) -> None:
        self.elapsed_time += delta_time
        if self.world_rotation_angle % 360.0 != 0.0:
            original_screen = self.screen
            scene = pygame.Surface(original_screen.get_size(), pygame.SRCALPHA).convert_alpha()
            self.screen = scene
            self._render_scene(world, session, effects, environment_state)
            self.screen = original_screen
            rotated = pygame.transform.rotate(scene, self.world_rotation_angle)
            rotated_rect = rotated.get_rect(center=original_screen.get_rect().center)
            original_screen.fill((3, 8, 18))
            original_screen.blit(rotated, rotated_rect)
            return
        self._render_scene(world, session, effects, environment_state)

    def _render_scene(
        self,
        world: World,
        session: GameSession,
        effects: VisualEffects | None,
        environment_state: EnvironmentState | None,
    ) -> None:
        if environment_state is not None:
            self.lighting.set_config(environment_state.lighting)
            self.environment.render(self.screen, environment_state)
        else:
            self.screen.fill(config.BLUE)

        basket_surface = self.assets.get_basket_surface(world.basket.width, world.basket.height)
        basket_surface = self.lighting.apply_lighting(basket_surface)
        if session.cheats.is_active("shield") or session.cheats.is_active("fahed"):
            self.render_basket_cheat_glow(world.basket.rect, session)
        basket_scale = effects.basket_squash.scale if effects is not None else (1.0, 1.0)
        self.blit_scaled(basket_surface, world.basket.rect, basket_scale)
        for falling_object in world.falling_objects:
            night_factor = self.night_factor(environment_state)
            object_color = self.object_color_for_environment(
                falling_object.definition.identifier,
                falling_object.definition.color,
                night_factor,
            )
            if falling_object.definition.identifier == "player_name":
                self.render_player_name_object(falling_object.rect, session.player_name)
                continue
            object_surface = self.assets.get_falling_object_surface(
                falling_object.definition.identifier,
                falling_object.size,
                object_color,
            )
            height_factor = self.lighting.estimate_height_factor(falling_object.y, falling_object.size)
            self.render_ground_shadow(falling_object.rect, height_factor)
            object_surface = self.lighting.apply_lighting(object_surface, height_factor)
            self.render_object_glow(
                falling_object.definition.identifier,
                falling_object.rect,
                object_color,
                night_factor,
                session,
            )
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

    def render_basket_cheat_glow(self, rect: pygame.Rect, session: GameSession) -> None:
        color = (245, 255, 255) if session.cheats.is_active("fahed") else (120, 245, 255)
        glow_surface = self.get_glow_surface(max(rect.width, 120), color, 132)
        glow_rect = glow_surface.get_rect(center=rect.center)
        self.screen.blit(glow_surface, glow_rect)

    def render_background(self, environment_state: EnvironmentState, delta_time: float = 0.0) -> None:
        self.elapsed_time += delta_time
        self.lighting.set_config(environment_state.lighting)
        self.environment.render(self.screen, environment_state)

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

    def render_object_glow(
        self,
        identifier: str,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        night_factor: float,
        session: GameSession,
    ) -> None:
        base_alpha = {
            "regular_apple": 118,
        }.get(identifier, 0)
        if session.powerups.is_active("magnet") and identifier in {"regular_apple", "golden_apple"}:
            base_alpha = max(base_alpha, 150)
        if session.cheats.is_active("insane") and identifier in {"regular_apple", "golden_apple"}:
            base_alpha = max(base_alpha, 135)
        alpha = int(base_alpha * night_factor)
        if session.powerups.is_active("magnet") and identifier in {"regular_apple", "golden_apple"}:
            alpha = max(alpha, 105)
        if session.cheats.is_active("insane") and identifier in {"regular_apple", "golden_apple"}:
            alpha = max(alpha, 95)
        if alpha <= 0:
            return
        glow_size = int(rect.width * 1.65)
        glow_surface = self.get_glow_surface(max(rect.width + 8, glow_size), color, alpha)
        glow_rect = glow_surface.get_rect(center=rect.center)
        self.screen.blit(glow_surface, glow_rect)

    def render_player_name_object(self, rect: pygame.Rect, player_name: str) -> None:
        label = (player_name or "LIFE")[: config.PLAYER_NAME_MAX_LENGTH]
        glow_surface = self.get_glow_surface(rect.width * 3, (245, 255, 255), 120)
        self.screen.blit(glow_surface, glow_surface.get_rect(center=rect.center))

        badge = pygame.Surface((max(82, rect.width * 3), 34), pygame.SRCALPHA)
        badge_rect = badge.get_rect()
        pygame.draw.rect(badge, (15, 28, 42, 230), badge_rect, border_radius=8)
        pygame.draw.rect(badge, (245, 255, 255), badge_rect, 2, border_radius=8)
        pygame.draw.circle(badge, (120, 245, 255, 120), (12, badge_rect.centery), 8)
        text = self.font.render(label, True, (245, 255, 255))
        badge.blit(text, text.get_rect(center=badge_rect.center))
        self.screen.blit(badge, badge.get_rect(center=rect.center))

    def get_glow_surface(
        self,
        size: int,
        color: tuple[int, int, int],
        alpha: int,
    ) -> pygame.Surface:
        key = (size, color, alpha)
        if key not in self._glow_surface_cache:
            surface = pygame.Surface((size, size), pygame.SRCALPHA)
            center = size // 2
            for index, scale in enumerate((1.0, 0.68, 0.38)):
                radius = max(1, int(center * scale))
                layer_alpha = max(0, alpha // (index + 2))
                pygame.draw.circle(surface, (*color, layer_alpha), (center, center), radius)
            self._glow_surface_cache[key] = surface.convert_alpha()
        return self._glow_surface_cache[key]

    def object_color_for_environment(
        self,
        identifier: str,
        base_color: tuple[int, int, int],
        night_factor: float,
    ) -> tuple[int, int, int]:
        night_palette = {
            "regular_apple": (245, 255, 255),
        }
        night_color = night_palette.get(identifier, base_color)
        return blend_color(base_color, night_color, clamp(night_factor, 0.0, 1.0))

    def night_factor(self, environment_state: EnvironmentState | None) -> float:
        if environment_state is None:
            return 0.0
        return clamp((0.64 - environment_state.day_night.ambient) / 0.32, 0.0, 1.0)

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


def blend_color(
    color: tuple[int, int, int],
    target: tuple[int, int, int],
    amount: float,
) -> tuple[int, int, int]:
    amount = clamp(amount, 0.0, 1.0)
    return tuple(
        max(0, min(255, int(channel + (target_channel - channel) * amount)))
        for channel, target_channel in zip(color, target, strict=True)
    )


def make_font(size: int) -> pygame.font.Font:
    font_path = pygame.font.match_font(config.FONT_NAME) or pygame.font.match_font("dejavusans")
    return pygame.font.Font(font_path, size) if font_path is not None else pygame.font.Font(None, size)
