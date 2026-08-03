import pygame

from catch_the_apple import config
from catch_the_apple.collision import build_basket_collision_model
from catch_the_apple.session import GameSession
from catch_the_apple.world import World


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)

    def render(self, world: World, session: GameSession) -> None:
        self.screen.fill(config.BLUE)

        pygame.draw.rect(self.screen, config.GREEN, world.basket.rect)
        for falling_object in world.falling_objects:
            pygame.draw.rect(self.screen, falling_object.definition.color, falling_object.rect)

        if session.debug_collision_enabled:
            self.render_debug_collision_overlay(world)

        score_text = self.font.render(f"Score: {session.score}", True, config.WHITE)
        lives_text = self.font.render(f"Lives: {session.lives}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (config.SCREEN_WIDTH - 120, 10))

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
