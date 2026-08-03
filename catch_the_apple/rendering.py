import pygame

from catch_the_apple import config
from catch_the_apple.collision import build_basket_collision_model
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

    def render(self, world: World, session: GameSession) -> None:
        self.screen.fill(config.BLUE)

        basket_surface = self.assets.get_basket_surface(world.basket.width, world.basket.height)
        self.screen.blit(self.lighting.apply_lighting(basket_surface), world.basket.rect)
        for falling_object in world.falling_objects:
            object_surface = self.assets.get_falling_object_surface(
                falling_object.definition.identifier,
                falling_object.size,
                falling_object.definition.color,
            )
            height_factor = self.lighting.estimate_height_factor(falling_object.y, falling_object.size)
            self.render_ground_shadow(falling_object.rect, height_factor)
            self.screen.blit(self.lighting.apply_lighting(object_surface, height_factor), falling_object.rect)

        if session.debug_collision_enabled:
            self.render_debug_collision_overlay(world)

        score_text = self.font.render(f"Score: {session.score}", True, config.WHITE)
        lives_text = self.font.render(f"Lives: {session.lives}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (config.SCREEN_WIDTH - 120, 10))

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
