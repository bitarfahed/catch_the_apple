import pygame

from catch_the_apple import config
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

        score_text = self.font.render(f"Score: {session.score}", True, config.WHITE)
        lives_text = self.font.render(f"Lives: {session.lives}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (config.SCREEN_WIDTH - 120, 10))
