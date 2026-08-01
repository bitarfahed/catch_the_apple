import pygame

from catch_the_apple import config
from catch_the_apple.collision import collides
from catch_the_apple.entities import Basket, GameState
from catch_the_apple.input import poll_input
from catch_the_apple.rendering import Renderer
from catch_the_apple.utils import create_apple, reset_apple


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = (
            pygame.display.set_subplots()[0]
            if hasattr(pygame, "set_subplots")
            else pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        )
        pygame.display.set_caption(config.WINDOW_TITLE)

        self.state = GameState()
        self.basket = Basket()
        self.apple = create_apple()
        self.renderer = Renderer(self.screen)
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while self.state.running:
            input_state = poll_input()
            if input_state.quit_requested:
                self.state.running = False

            if input_state.left_pressed and self.basket.x > 0:
                self.basket.x -= self.basket.speed
            if input_state.right_pressed and self.basket.x < config.SCREEN_WIDTH - self.basket.width:
                self.basket.x += self.basket.speed

            self.apple.y += self.apple.speed

            if self.apple.y > config.SCREEN_HEIGHT:
                self.state.lives -= 1
                reset_apple(self.apple)
                if self.state.lives <= 0:
                    self.state.running = False

            if collides(self.basket, self.apple):
                self.state.score += 1
                reset_apple(self.apple)
                if self.state.score % 5 == 0:
                    self.apple.speed += 1

            self.renderer.render(self.basket, self.apple, self.state)
            pygame.display.flip()
            self.clock.tick(config.FPS)

        pygame.quit()
