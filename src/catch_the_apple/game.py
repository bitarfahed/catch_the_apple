import pygame

from catch_the_apple.audio import AudioSystem
from catch_the_apple import config
from catch_the_apple.debug import DebugSnapshot
from catch_the_apple.dynamic_environment import EnvironmentManager
from catch_the_apple.effects import VisualEffects
from catch_the_apple.input import poll_input
from catch_the_apple.rendering import Renderer
from catch_the_apple.session import GameSession
from catch_the_apple.states import MainMenuState, StateManager
from catch_the_apple.persistence import PersistenceStore
from catch_the_apple.systems.game_rules import apply_game_rules
from catch_the_apple.systems.movement import update_movement
from catch_the_apple.systems.spawning import SpawnSystem
from catch_the_apple.ui import UI
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

        self.persistence = PersistenceStore()
        self.audio = AudioSystem(self.persistence.data.settings)
        self.session = GameSession()
        self.world = World()
        self.spawn_system = SpawnSystem(config.SPAWN_CONFIG)
        self.spawn_system.update(self.world)
        self.environment_manager = EnvironmentManager()
        self.effects = VisualEffects()
        self.renderer = Renderer(self.screen)
        self.ui = UI()
        self.states = StateManager(MainMenuState())
        self.clock = pygame.time.Clock()
        self.frame_time_ms = 0.0

    def run(self) -> None:
        while self.session.running:
            delta_time = self.measure_delta_time()
            self.update(delta_time)
            self.render(delta_time)

        pygame.quit()

    def measure_delta_time(self) -> float:
        self.frame_time_ms = self.clock.tick(config.FPS)
        delta_time = self.frame_time_ms / 1000.0
        return min(delta_time, config.MAX_DELTA_TIME)

    def update(self, delta_time: float) -> None:
        input_state = poll_input()
        if input_state.quit_requested:
            self.session.running = False
        if input_state.debug_collision_toggled:
            self.session.debug_collision_enabled = not self.session.debug_collision_enabled
        if input_state.debug_overlay_toggled:
            self.session.debug_overlay_enabled = not self.session.debug_overlay_enabled
        if input_state.mute_toggled:
            self.audio.toggle_mute()
            self.persistence.save_settings(self.audio.settings)
        if input_state.volume_up_pressed:
            self.audio.set_master_volume(self.audio.settings.master_volume + 0.05)
            self.persistence.save_settings(self.audio.settings)
        if input_state.volume_down_pressed:
            self.audio.set_master_volume(self.audio.settings.master_volume - 0.05)
            self.persistence.save_settings(self.audio.settings)

        self._current_input_state = input_state
        self.states.handle_input(self, input_state)
        self.states.update(self, delta_time)

    def update_playing(self, input_state, delta_time: float) -> None:
        self.environment_manager.update(delta_time)
        update_movement(self.world, input_state, delta_time, self.environment_manager)
        events = apply_game_rules(self.world, self.session, self.spawn_system)
        self.persistence.record_events(events)
        self.spawn_system.update(self.world)
        self.effects.handle_events(events)
        self.effects.update(self.world, delta_time, self.environment_manager)
        self.ui.handle_events(events)
        self.ui.update(delta_time)

    def render(self, delta_time: float) -> None:
        self.states.render(self, delta_time)
        if self.session.debug_overlay_enabled:
            self.ui.render_debug_overlay(self.screen, self.build_debug_snapshot())
        pygame.display.flip()

    def reset_play_session(self) -> None:
        debug_collision_enabled = self.session.debug_collision_enabled
        self.session = GameSession(debug_collision_enabled=debug_collision_enabled)
        self.world = World()
        self.spawn_system = SpawnSystem(config.SPAWN_CONFIG)
        self.spawn_system.update(self.world)
        self.effects = VisualEffects()

    def finish_session(self) -> None:
        if self.session.finalized:
            return
        self.session.finalized = True
        self.persistence.finish_session(self.session)

    def build_debug_snapshot(self) -> DebugSnapshot:
        wind = self.environment_manager.state.wind
        return DebugSnapshot(
            fps=self.clock.get_fps(),
            frame_time_ms=self.frame_time_ms,
            active_objects=len(self.world.falling_objects),
            particle_count=sum(1 for _ in self.effects.particles.active_particles()),
            current_state=type(self.states.current).__name__,
            weather=self.environment_manager.state.weather.name,
            wind_strength=wind.strength,
            wind_direction=(wind.direction.x, wind.direction.y),
            collision_debug_enabled=self.session.debug_collision_enabled,
            audio_available=self.audio.available,
            muted=self.audio.settings.muted,
        )
