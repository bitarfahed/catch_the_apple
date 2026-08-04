import pygame

from catch_the_apple.audio import AudioSystem
from catch_the_apple import config
from catch_the_apple.cheats import CHEAT_DEFINITIONS
from catch_the_apple.debug import DebugSnapshot
from catch_the_apple.developer_console import DeveloperConsole
from catch_the_apple.difficulty_profiles import DEFAULT_DIFFICULTY_PROFILE, DifficultyProfile
from catch_the_apple.dynamic_environment import EnvironmentManager
from catch_the_apple.effects import VisualEffects
from catch_the_apple.events import ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.input import poll_input
from catch_the_apple.powerups import (
    PowerUpSystem,
    apply_black_hole,
    apply_magnet_pull,
    apply_shockwave,
    basket_speed_scale,
    magnet_active_object_bonus,
    power_up_time_scale,
    wind_control_scale,
)
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
        self.selected_profile = DEFAULT_DIFFICULTY_PROFILE
        self.player_name_input = ""
        self.name_error = ""
        self._cheat_rain_was_active = False
        self.session = GameSession()
        self.world = World()
        self.spawn_system = SpawnSystem(self.selected_profile.spawn_config)
        self.power_up_system = PowerUpSystem()
        self.developer_console = DeveloperConsole()
        self.spawn_system.power_state = self.session.powerups
        self.spawn_system.update(self.world)
        self.environment_manager = self.create_environment_manager()
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
        self.session.powerups.update(delta_time)
        self.session.cheats.update(delta_time)
        self.apply_cheat_environment()
        self.apply_power_up_modifiers()
        update_movement(
            self.world,
            input_state,
            delta_time,
            self.environment_manager,
            power_up_time_scale(self.session.powerups) * self.cheat_falling_time_scale(),
            self.session.powerups,
            wind_control_scale(self.session.powerups),
            self.session.cheats.is_active("cycle"),
        )
        apply_magnet_pull(self.world, delta_time, self.session.powerups)
        apply_black_hole(self.world, delta_time, self.session.powerups)
        apply_shockwave(self.world, delta_time, self.session.powerups)
        events = apply_game_rules(
            self.world,
            self.session,
            self.spawn_system,
            self.selected_profile.difficulty_config,
            self.power_up_system,
        )
        self.persistence.record_events(events)
        self.spawn_system.max_active_objects = (
            self.selected_profile.spawn_config.max_active_objects
            + magnet_active_object_bonus(self.session.powerups)
        )
        self.spawn_system.power_state = self.session.powerups
        self.spawn_system.update(self.world)
        self.effects.handle_events(events)
        self.handle_audio_events(events)
        if self.session.cheats.is_active("fahed"):
            self.effects.emit_basket_dash_trail(self.world)
        self.effects.update(self.world, delta_time, self.environment_manager)
        self.ui.handle_events(events)
        self.ui.update(delta_time)

    def append_player_name_text(self, text: str) -> None:
        if any(not character.isalnum() for character in text):
            self.name_error = "Use one word with no spaces"
            return
        if not text:
            return
        self.player_name_input = (self.player_name_input + text)[: config.PLAYER_NAME_MAX_LENGTH]
        self.name_error = ""

    def backspace_player_name(self) -> None:
        self.player_name_input = self.player_name_input[:-1]
        self.name_error = ""

    def start_named_session(self) -> bool:
        name = self.player_name_input.strip()
        if not is_valid_player_name(name):
            self.name_error = "Enter one word using letters or numbers"
            return False
        from catch_the_apple.states import PlayingState

        self.reset_play_session()
        self.session.player_name = name
        self.states.change(PlayingState())
        return True

    def render(self, delta_time: float) -> None:
        self.renderer.world_rotation_angle = self.session.cheats.value("flip", 0.0)
        self.states.render(self, delta_time)
        if self.session.debug_overlay_enabled:
            self.ui.render_debug_overlay(self.screen, self.build_debug_snapshot())
        pygame.display.flip()

    def reset_play_session(self, profile: DifficultyProfile | None = None) -> None:
        debug_collision_enabled = self.session.debug_collision_enabled
        if profile is not None:
            self.selected_profile = profile
        player_name = self.session.player_name or self.player_name_input.strip()
        self.session = GameSession(
            player_name=player_name,
            debug_collision_enabled=debug_collision_enabled,
        )
        self.world = World()
        self.spawn_system = SpawnSystem(self.selected_profile.spawn_config)
        self.spawn_system.update(self.world)
        self.environment_manager = self.create_environment_manager()
        self.effects = VisualEffects()
        self.power_up_system = PowerUpSystem()
        self.spawn_system.power_state = self.session.powerups

    def create_environment_manager(self) -> EnvironmentManager:
        return EnvironmentManager(
            wind_config=self.selected_profile.wind_config,
            gameplay_wind_scale=self.selected_profile.gameplay_wind_scale,
        )

    def apply_power_up_modifiers(self) -> None:
        speed_scale = basket_speed_scale(self.session.powerups)
        target_width = int(config.SCREEN_WIDTH * 0.92) if self.session.cheats.is_active("fahed") else config.BASKET_WIDTH
        if self.world.basket.width != target_width:
            center_x = self.world.basket.rect.centerx
            self.world.basket.width = target_width
            self.world.basket.x = center_x - target_width / 2
        self.world.basket.max_speed = config.BASKET_MAX_SPEED * speed_scale
        self.world.basket.acceleration_rate = config.BASKET_ACCELERATION * speed_scale
        self.world.basket.dash_speed = config.BASKET_DASH_SPEED * speed_scale

    def cheat_falling_time_scale(self) -> float:
        return 0.55 if self.session.cheats.is_active("easy") else 1.0

    def apply_cheat_environment(self) -> None:
        if self.session.cheats.is_active("wind"):
            self._cheat_rain_was_active = True
            self.environment_manager.set_weather("rain")
        elif self._cheat_rain_was_active:
            self.environment_manager.set_weather("clear")
            self._cheat_rain_was_active = False

    def handle_audio_events(self, events: list[ObjectCaughtEvent | ObjectMissedEvent]) -> None:
        for event in events:
            if isinstance(event, ObjectCaughtEvent):
                self.audio.play_object_effect(event.object_identifier, caught=True)
            elif isinstance(event, ObjectMissedEvent) and event.damage > 0:
                self.audio.play_object_effect(event.object_identifier, caught=False)

    def activate_cheat_code(self, code: str) -> bool:
        if self.activate_developer_cheat(code):
            return True
        definition = self.power_up_system.by_cheat_code(code)
        if definition is None:
            self.developer_console.message = f"Unknown code: {code.upper()}"
            return False
        self.session.powerups.activate(definition)
        self.spawn_system.power_state = self.session.powerups
        self.developer_console.message = f"Activated {definition.display_name}"
        self.developer_console.clear()
        return True

    def activate_developer_cheat(self, code: str) -> bool:
        parts = code.strip().lower().split()
        if not parts:
            return False
        command = parts[0]
        if command == "nosound":
            self.audio.settings.muted = True
            self.audio.apply_volumes()
            self.developer_console.message = "Muted all sound"
            self.developer_console.clear()
            return True
        if command == "sound":
            self.audio.settings.muted = False
            self.audio.apply_volumes()
            self.developer_console.message = "Sound restored"
            self.developer_console.clear()
            return True
        if command == "shield" and self.session.score < 5:
            self.developer_console.message = "Shield needs 5 score"
            return True
        if command == "shield":
            self.session.score -= 5
        if command == "flip":
            if len(parts) != 2:
                self.developer_console.message = "Usage: flip <angle>"
                return True
            try:
                angle = float(parts[1])
            except ValueError:
                self.developer_console.message = "Flip angle must be a number"
                return True
            if not 0.0 <= angle <= 360.0:
                self.developer_console.message = "Flip angle must be 0-360"
                return True
            self.session.cheats.activate(CHEAT_DEFINITIONS["flip"], angle)
            self.developer_console.message = f"Flip {angle:g} active"
            self.developer_console.clear()
            return True
        definition = CHEAT_DEFINITIONS.get(command)
        if definition is None:
            return False
        self.session.cheats.activate(definition)
        if command == "wind":
            self.environment_manager.set_weather("rain")
        self.developer_console.message = f"Activated {definition.display_name}"
        self.developer_console.clear()
        return True

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


def is_valid_player_name(name: str) -> bool:
    return 1 <= len(name) <= config.PLAYER_NAME_MAX_LENGTH and name.isalnum()
