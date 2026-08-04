from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import pygame

from catch_the_apple.difficulty_profiles import DIFFICULTY_PROFILES
from catch_the_apple.input import InputState

if TYPE_CHECKING:
    from catch_the_apple.game import Game


class GameStateBase:
    def enter(self, game: Game) -> None:
        pass

    def handle_input(self, game: Game, input_state: InputState) -> None:
        pass

    def update(self, game: Game, delta_time: float) -> None:
        pass

    def render(self, game: Game, delta_time: float) -> None:
        pass


class MainMenuState(GameStateBase):
    def handle_input(self, game: Game, input_state: InputState) -> None:
        if input_state.start_pressed or input_state.mouse_left_clicked:
            game.states.change(DifficultySelectionState())

    def update(self, game: Game, delta_time: float) -> None:
        game.environment_manager.update(delta_time)
        game.ui.update(delta_time)

    def render(self, game: Game, delta_time: float) -> None:
        game.renderer.render_background(game.environment_manager.state, delta_time)
        game.ui.render_menu(game.screen)


class DifficultySelectionState(GameStateBase):
    def handle_input(self, game: Game, input_state: InputState) -> None:
        if not input_state.mouse_left_clicked:
            return
        selected_profile = game.ui.profile_at_position(input_state.mouse_position)
        if selected_profile is None:
            return
        game.reset_play_session(selected_profile)
        game.states.change(PlayingState())

    def update(self, game: Game, delta_time: float) -> None:
        game.environment_manager.update(delta_time)
        game.ui.update(delta_time)

    def render(self, game: Game, delta_time: float) -> None:
        game.renderer.render_background(game.environment_manager.state, delta_time)
        game.ui.render_difficulty_selection(
            game.screen,
            DIFFICULTY_PROFILES,
            pygame.mouse.get_pos(),
        )


class PlayingState(GameStateBase):
    def handle_input(self, game: Game, input_state: InputState) -> None:
        if input_state.pause_pressed:
            game.states.change(PausedState())

    def update(self, game: Game, delta_time: float) -> None:
        input_state = getattr(game, "_current_input_state")
        game.update_playing(input_state, delta_time)
        if game.session.game_over:
            game.finish_session()
            game.states.change(GameOverState())

    def render(self, game: Game, delta_time: float) -> None:
        game.renderer.render(game.world, game.session, game.effects, delta_time, game.environment_manager.state)
        game.ui.render_hud(game.screen, game.session, game.world, game.environment_manager.state)


class PausedState(GameStateBase):
    def handle_input(self, game: Game, input_state: InputState) -> None:
        if input_state.restart_pressed:
            game.reset_play_session()
            game.states.change(PlayingState())
        elif input_state.pause_pressed:
            game.states.change(PlayingState())

    def update(self, game: Game, delta_time: float) -> None:
        game.environment_manager.update(delta_time)
        game.ui.update(delta_time)

    def render(self, game: Game, delta_time: float) -> None:
        game.renderer.render(game.world, game.session, game.effects, delta_time, game.environment_manager.state)
        game.ui.render_hud(game.screen, game.session, game.world, game.environment_manager.state)
        game.ui.render_pause(game.screen)


class GameOverState(GameStateBase):
    def handle_input(self, game: Game, input_state: InputState) -> None:
        if input_state.restart_pressed or input_state.start_pressed:
            game.reset_play_session()
            game.states.change(PlayingState())

    def update(self, game: Game, delta_time: float) -> None:
        game.environment_manager.update(delta_time)
        game.effects.update(game.world, delta_time, game.environment_manager)
        game.ui.update(delta_time)

    def render(self, game: Game, delta_time: float) -> None:
        game.renderer.render(game.world, game.session, game.effects, delta_time, game.environment_manager.state)
        game.ui.render_game_over(game.screen, game.session)


@dataclass
class StateManager:
    current: GameStateBase
    transition_alpha: float = 255.0
    transition_speed: float = 900.0

    def change(self, state: GameStateBase) -> None:
        self.current = state
        self.transition_alpha = 255.0

    def handle_input(self, game: Game, input_state: InputState) -> None:
        self.current.handle_input(game, input_state)

    def update(self, game: Game, delta_time: float) -> None:
        self.current.update(game, delta_time)
        self.transition_alpha = max(0.0, self.transition_alpha - self.transition_speed * delta_time)

    def render(self, game: Game, delta_time: float) -> None:
        self.current.render(game, delta_time)
        if self.transition_alpha > 0.0:
            overlay = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, int(self.transition_alpha)))
            game.screen.blit(overlay, (0, 0))
