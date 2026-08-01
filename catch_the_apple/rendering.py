import pygame

from catch_the_apple import config
from catch_the_apple.entities import Apple, Basket, GameState


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = pygame.font.SysFont(config.FONT_NAME, config.FONT_SIZE)

    def render(self, basket: Basket, apple: Apple, state: GameState) -> None:
        self.screen.fill(config.BLUE)

        pygame.draw.rect(self.screen, config.GREEN, basket.rect)
        pygame.draw.rect(self.screen, config.RED, apple.rect)

        score_text = self.font.render(f"Score: {state.score}", True, config.WHITE)
        lives_text = self.font.render(f"Lives: {state.lives}", True, config.WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (config.SCREEN_WIDTH - 120, 10))
