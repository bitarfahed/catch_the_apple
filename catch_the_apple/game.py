import pygame

from catch_the_apple import config
from catch_the_apple.effects import VisualEffects
from catch_the_apple.input import poll_input
from catch_the_apple.rendering import Renderer
from catch_the_apple.session import GameSession
from catch_the_apple.systems.game_rules import apply_game_rules
from catch_the_apple.systems.movement import update_movement
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.world import World


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = (
            pygame.display.set_subplots()[0]
            if hasattr(pygame, "set_subplots")
            else pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        )
        pygame.display.set_caption(config.WINDOW_TITLE)

        self.session = GameSession()
        self.world = World()
        self.spawn_system = SpawnSystem(config.SPAWN_CONFIG)
        self.spawn_system.update(self.world)
        self.effects = VisualEffects()
        self.renderer = Renderer(self.screen)
        self.clock = pygame.time.Clock()

    def run(self) -> None:
        while self.session.running:
            delta_time = self.measure_delta_time()
            self.update(delta_time)
            self.render(delta_time)

        pygame.quit()

    def measure_delta_time(self) -> float:
        delta_time = self.clock.tick(config.FPS) / 1000.0
        return min(delta_time, config.MAX_DELTA_TIME)

    def update(self, delta_time: float) -> None:
        input_state = poll_input()
        if input_state.quit_requested:
            self.session.running = False
        if input_state.debug_collision_toggled:
            self.session.debug_collision_enabled = not self.session.debug_collision_enabled

        update_movement(self.world, input_state, delta_time)
        events = apply_game_rules(self.world, self.session, self.spawn_system)
        self.spawn_system.update(self.world)
        self.effects.handle_events(events)
        self.effects.update(self.world, delta_time)

    def render(self, delta_time: float) -> None:
        self.renderer.render(self.world, self.session, self.effects, delta_time)
        pygame.display.flip()
