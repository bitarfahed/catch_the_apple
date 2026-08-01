import pygame

from catch_the_apple import config
from catch_the_apple.collision import collides
from catch_the_apple.entities import Basket, GameState
from catch_the_apple.input import poll_input
from catch_the_apple.math2d import clamp
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
            delta_time = self.measure_delta_time()
            self.update(delta_time)
            self.render()

        pygame.quit()

    def measure_delta_time(self) -> float:
        delta_time = self.clock.tick(config.FPS) / 1000.0
        return min(delta_time, config.MAX_DELTA_TIME)

    def update(self, delta_time: float) -> None:
        input_state = poll_input()
        if input_state.quit_requested:
            self.state.running = False

        if input_state.left_pressed and self.basket.x > 0:
            self.basket.x -= self.basket.speed * delta_time
        if input_state.right_pressed and self.basket.x < config.SCREEN_WIDTH - self.basket.width:
            self.basket.x += self.basket.speed * delta_time

        self.basket.x = clamp(self.basket.x, 0, config.SCREEN_WIDTH - self.basket.width)

        self.apple.y += self.apple.speed * delta_time

        if self.apple.y > config.SCREEN_HEIGHT:
            self.state.lives -= 1
            reset_apple(self.apple)
            if self.state.lives <= 0:
                self.state.running = False

        if collides(self.basket, self.apple):
            self.state.score += 1
            reset_apple(self.apple)
            if self.state.score % 5 == 0:
                self.apple.speed += config.APPLE_SPEED_INCREASE

    def render(self) -> None:
        self.renderer.render(self.basket, self.apple, self.state)
        pygame.display.flip()
