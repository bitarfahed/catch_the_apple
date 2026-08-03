from dataclasses import dataclass

import pygame

from catch_the_apple import config
from catch_the_apple.dynamic_environment import EnvironmentState
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.session import GameSession
from catch_the_apple.world import World


@dataclass
class UIAnimations:
    score_pop: float = 0.0
    combo_pulse: float = 0.0
    life_flash: float = 0.0

    def handle_events(self, events: list[GameplayEvent]) -> None:
        for event in events:
            if isinstance(event, ObjectCaughtEvent):
                self.score_pop = 0.28
                self.combo_pulse = 0.25
            if isinstance(event, ObjectMissedEvent):
                self.life_flash = 0.35

    def update(self, delta_time: float) -> None:
        self.score_pop = max(0.0, self.score_pop - delta_time)
        self.combo_pulse = max(0.0, self.combo_pulse - delta_time)
        self.life_flash = max(0.0, self.life_flash - delta_time)


class UI:
    def __init__(self) -> None:
        self.title_font = pygame.font.SysFont(config.FONT_NAME, 54, bold=True)
        self.large_font = pygame.font.SysFont(config.FONT_NAME, 38, bold=True)
        self.font = pygame.font.SysFont(config.FONT_NAME, 26)
        self.small_font = pygame.font.SysFont(config.FONT_NAME, 19)
        self.animations = UIAnimations()

    def update(self, delta_time: float) -> None:
        self.animations.update(delta_time)

    def handle_events(self, events: list[GameplayEvent]) -> None:
        self.animations.handle_events(events)

    def render_hud(self, screen: pygame.Surface, session: GameSession, world: World, environment: EnvironmentState) -> None:
        panel = pygame.Surface((330, 96), pygame.SRCALPHA)
        panel.fill((15, 24, 32, 120))
        screen.blit(panel, (14, 12))

        score_scale = 1.0 + self.animations.score_pop * 0.55
        score_text = self.large_font.render(f"Score {session.score}", True, config.WHITE)
        if score_scale != 1.0:
            score_text = pygame.transform.smoothscale(
                score_text,
                (int(score_text.get_width() * score_scale), int(score_text.get_height() * score_scale)),
            )
        screen.blit(score_text, (26, 20))

        lives_color = (255, 110, 110) if self.animations.life_flash > 0.0 else config.WHITE
        lives_text = self.font.render(f"Lives {session.lives}", True, lives_color)
        screen.blit(lives_text, (26, 64))

        combo_scale = 1.0 + self.animations.combo_pulse * 0.45
        combo_text = self.font.render(f"Combo x{session.combo}", True, (255, 232, 130))
        if combo_scale != 1.0:
            combo_text = pygame.transform.smoothscale(
                combo_text,
                (int(combo_text.get_width() * combo_scale), int(combo_text.get_height() * combo_scale)),
            )
        screen.blit(combo_text, (170, 65))

        self.render_dash_status(screen, world)
        weather_text = self.small_font.render(environment.weather.name, True, (225, 235, 240))
        screen.blit(weather_text, (config.SCREEN_WIDTH - weather_text.get_width() - 18, 14))

    def render_dash_status(self, screen: pygame.Surface, world: World) -> None:
        basket = world.basket
        cooldown = basket.movement.dash_cooldown_remaining
        ready = cooldown <= 0.0
        label = "Dash Ready" if ready else "Dash Cooling"
        text = self.small_font.render(label, True, (230, 245, 255) if ready else (190, 205, 215))
        x = config.SCREEN_WIDTH - 160
        y = 44
        screen.blit(text, (x, y))
        pygame.draw.rect(screen, (35, 50, 60), pygame.Rect(x, y + 24, 132, 8), border_radius=4)
        fill_ratio = 1.0 if ready else 1.0 - min(1.0, cooldown / max(0.01, basket.dash_cooldown))
        pygame.draw.rect(
            screen,
            (90, 210, 240) if ready else (110, 150, 180),
            pygame.Rect(x, y + 24, int(132 * fill_ratio), 8),
            border_radius=4,
        )

    def render_menu(self, screen: pygame.Surface) -> None:
        self.render_center_panel(
            screen,
            "Catch the Apple",
            ("Press Enter to Start", "Arrow keys move  |  Space dashes", "F1 toggles collision debug"),
        )

    def render_pause(self, screen: pygame.Surface) -> None:
        self.render_overlay(screen, alpha=115)
        self.render_center_panel(screen, "Paused", ("Press P or Esc to Resume", "Press R to Restart"))

    def render_game_over(self, screen: pygame.Surface, session: GameSession) -> None:
        self.render_overlay(screen, alpha=135)
        self.render_center_panel(
            screen,
            "Game Over",
            (f"Final Score {session.score}", "Press R or Enter to Restart"),
        )

    def render_overlay(self, screen: pygame.Surface, alpha: int) -> None:
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, alpha))
        screen.blit(overlay, (0, 0))

    def render_center_panel(self, screen: pygame.Surface, title: str, lines: tuple[str, ...]) -> None:
        title_surface = self.title_font.render(title, True, config.WHITE)
        center_x = config.SCREEN_WIDTH // 2
        y = config.SCREEN_HEIGHT // 2 - 105
        screen.blit(title_surface, title_surface.get_rect(center=(center_x, y)))
        for index, line in enumerate(lines):
            line_surface = self.font.render(line, True, (230, 238, 244))
            screen.blit(line_surface, line_surface.get_rect(center=(center_x, y + 62 + index * 34)))
