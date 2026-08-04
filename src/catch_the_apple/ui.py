from dataclasses import dataclass

import pygame

from catch_the_apple import config
from catch_the_apple.debug import DebugSnapshot
from catch_the_apple.developer_console import DeveloperConsole
from catch_the_apple.difficulty_profiles import DifficultyProfile
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
            if isinstance(event, ObjectMissedEvent) and event.damage > 0:
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
        self.difficulty_buttons: list[tuple[pygame.Rect, DifficultyProfile]] = []

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
        self.render_environment_status(screen, environment)
        for index, label in enumerate(session.powerups.labels()):
            power_text = self.small_font.render(label, True, (160, 245, 255))
            screen.blit(power_text, (config.SCREEN_WIDTH - power_text.get_width() - 18, 112 + index * 21))
        if session.powerups.is_active("slow_motion"):
            self.render_status_banner(screen, "SLOW MOTION", (100, 230, 255))
        elif session.powerups.is_active("magnet"):
            self.render_status_banner(screen, "APPLE STORM", (255, 235, 110))
        elif session.powerups.is_active("speed_boost"):
            self.render_status_banner(screen, "SPEED BOOST", (145, 255, 170))
        elif session.powerups.active:
            active = next(iter(session.powerups.active.values()))
            self.render_status_banner(
                screen,
                active.definition.display_name.upper(),
                active.definition.visual_color,
            )

    def render_environment_status(self, screen: pygame.Surface, environment: EnvironmentState) -> None:
        x = config.SCREEN_WIDTH - 170
        y = 12
        panel = pygame.Surface((154, 88), pygame.SRCALPHA)
        panel.fill((8, 15, 22, 128))
        screen.blit(panel, (x - 8, y - 2))

        daylight_label = "DAY" if environment.day_night.ambient >= 0.56 else "NIGHT"
        daylight_color = (255, 226, 132) if daylight_label == "DAY" else (180, 220, 255)
        phase_text = self.small_font.render(daylight_label, True, daylight_color)
        screen.blit(phase_text, (x, y))

        weather_text = self.small_font.render(environment.weather.name, True, (225, 235, 240))
        screen.blit(weather_text, (x, y + 22))

        wind = environment.wind.velocity
        wind_strength = min(1.0, wind.length() / 34.0)
        arrow_center = (x + 27, y + 64)
        arrow_length = 22 + int(24 * wind_strength)
        direction = wind.normalize() if wind.length_squared() > 0.0 else pygame.Vector2(1.0, 0.0)
        end = (
            int(arrow_center[0] + direction.x * arrow_length),
            int(arrow_center[1] + direction.y * arrow_length),
        )
        wind_color = (130, 235, 255) if wind_strength < 0.65 else (255, 235, 125)
        pygame.draw.circle(screen, (28, 44, 54), arrow_center, 17)
        pygame.draw.line(screen, wind_color, arrow_center, end, 3)
        pygame.draw.circle(screen, wind_color, end, 4)
        label = self.small_font.render(f"Wind {int(environment.wind.strength)}", True, wind_color)
        screen.blit(label, (x + 54, y + 55))

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
            ("Press Enter or Click to Start", "Choose difficulty with the mouse", "F1 collision  |  F2 debug  |  M mute"),
        )

    def render_name_entry(self, screen: pygame.Surface, name: str, error: str) -> None:
        center_x = config.SCREEN_WIDTH // 2
        title = self.title_font.render("Catch the Apple", True, config.WHITE)
        screen.blit(title, title.get_rect(center=(center_x, 150)))

        prompt = self.font.render("Enter player name", True, (230, 238, 244))
        screen.blit(prompt, prompt.get_rect(center=(center_x, 220)))

        input_rect = pygame.Rect(center_x - 150, 255, 300, 48)
        pygame.draw.rect(screen, (8, 15, 22), input_rect, border_radius=6)
        pygame.draw.rect(screen, (120, 220, 240), input_rect, 2, border_radius=6)
        display_name = name or "NAME"
        color = config.WHITE if name else (120, 145, 155)
        name_text = self.large_font.render(display_name, True, color)
        screen.blit(name_text, name_text.get_rect(center=input_rect.center))

        hint = self.small_font.render("One word, letters or numbers only. Enter starts.", True, (210, 225, 232))
        screen.blit(hint, hint.get_rect(center=(center_x, 330)))
        if error:
            error_text = self.small_font.render(error, True, (255, 125, 125))
            screen.blit(error_text, error_text.get_rect(center=(center_x, 360)))

    def render_difficulty_selection(
        self,
        screen: pygame.Surface,
        profiles: tuple[DifficultyProfile, ...],
        mouse_position: tuple[int, int],
    ) -> None:
        title_surface = self.title_font.render("Select Difficulty", True, config.WHITE)
        center_x = config.SCREEN_WIDTH // 2
        screen.blit(title_surface, title_surface.get_rect(center=(center_x, 120)))

        self.difficulty_buttons = []
        button_width = 230
        button_height = 138
        gap = 20
        total_width = len(profiles) * button_width + (len(profiles) - 1) * gap
        start_x = center_x - total_width // 2
        y = 220
        for index, profile in enumerate(profiles):
            rect = pygame.Rect(start_x + index * (button_width + gap), y, button_width, button_height)
            self.difficulty_buttons.append((rect, profile))
            hovered = rect.collidepoint(mouse_position)
            fill = (28, 48, 58, 210) if hovered else (18, 30, 38, 185)
            border = (120, 220, 240) if hovered else (82, 122, 138)
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill(fill)
            screen.blit(panel, rect)
            pygame.draw.rect(screen, border, rect, 2, border_radius=6)

            name = self.large_font.render(profile.display_name, True, config.WHITE)
            screen.blit(name, name.get_rect(center=(rect.centerx, rect.y + 35)))

            details = (
                f"Speed {int(profile.spawn_config.object_speed)}",
                f"Growth +{int(profile.difficulty_config.speed_increase)}",
                f"Objects {profile.spawn_config.max_active_objects}",
                profile.description,
            )
            for detail_index, detail in enumerate(details):
                font = self.small_font if detail_index < 3 else self.small_font
                text = font.render(detail, True, (220, 232, 238))
                screen.blit(text, text.get_rect(center=(rect.centerx, rect.y + 68 + detail_index * 21)))

        hint = self.font.render("Click a profile to begin", True, (230, 238, 244))
        screen.blit(hint, hint.get_rect(center=(center_x, 420)))

    def profile_at_position(self, position: tuple[int, int]) -> DifficultyProfile | None:
        for rect, profile in self.difficulty_buttons:
            if rect.collidepoint(position):
                return profile
        return None

    def render_pause(self, screen: pygame.Surface) -> None:
        self.render_overlay(screen, alpha=115)
        self.render_center_panel(
            screen,
            "Paused",
            ("Press P or Esc to Resume", "Press R to Restart", "Press C for Developer Console"),
        )

    def render_developer_console(self, screen: pygame.Surface, console: DeveloperConsole) -> None:
        self.render_overlay(screen, alpha=150)
        panel = pygame.Rect(150, 190, 500, 210)
        pygame.draw.rect(screen, (8, 15, 22), panel, border_radius=6)
        pygame.draw.rect(screen, (90, 210, 240), panel, 2, border_radius=6)
        title = self.large_font.render("Developer Console", True, config.WHITE)
        screen.blit(title, title.get_rect(center=(panel.centerx, panel.y + 36)))
        prompt = self.font.render(f"> {console.text}", True, (160, 245, 255))
        screen.blit(prompt, (panel.x + 28, panel.y + 88))
        message = self.small_font.render(console.message, True, (225, 235, 240))
        screen.blit(message, (panel.x + 28, panel.y + 132))
        hint = self.small_font.render("Enter submits  |  Backspace edits  |  P/Esc resumes", True, (180, 195, 205))
        screen.blit(hint, (panel.x + 28, panel.y + 164))

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

    def render_status_banner(
        self,
        screen: pygame.Surface,
        label: str,
        color: tuple[int, int, int],
    ) -> None:
        text = self.large_font.render(label, True, color)
        glow = self.large_font.render(label, True, (255, 255, 255))
        x = config.SCREEN_WIDTH // 2
        y = 38
        glow.set_alpha(90)
        screen.blit(glow, glow.get_rect(center=(x + 2, y + 2)))
        screen.blit(text, text.get_rect(center=(x, y)))

    def render_center_panel(self, screen: pygame.Surface, title: str, lines: tuple[str, ...]) -> None:
        title_surface = self.title_font.render(title, True, config.WHITE)
        center_x = config.SCREEN_WIDTH // 2
        y = config.SCREEN_HEIGHT // 2 - 105
        screen.blit(title_surface, title_surface.get_rect(center=(center_x, y)))
        for index, line in enumerate(lines):
            line_surface = self.font.render(line, True, (230, 238, 244))
            screen.blit(line_surface, line_surface.get_rect(center=(center_x, y + 62 + index * 34)))

    def render_debug_overlay(self, screen: pygame.Surface, snapshot: DebugSnapshot) -> None:
        lines = (
            f"FPS: {snapshot.fps:5.1f}",
            f"Frame: {snapshot.frame_time_ms:5.2f} ms",
            f"State: {snapshot.current_state}",
            f"Objects: {snapshot.active_objects}",
            f"Particles: {snapshot.particle_count}",
            f"Weather: {snapshot.weather}",
            f"Wind: {snapshot.wind_strength:5.2f} ({snapshot.wind_direction[0]:.2f}, {snapshot.wind_direction[1]:.2f})",
            f"Collision debug: {'on' if snapshot.collision_debug_enabled else 'off'}",
            f"Audio: {'ok' if snapshot.audio_available else 'unavailable'} / {'muted' if snapshot.muted else 'unmuted'}",
        )
        width = 292
        height = 22 + len(lines) * 20
        panel = pygame.Surface((width, height), pygame.SRCALPHA)
        panel.fill((5, 10, 14, 190))
        screen.blit(panel, (14, config.SCREEN_HEIGHT - height - 14))
        for index, line in enumerate(lines):
            text = self.small_font.render(line, True, (210, 235, 225))
            screen.blit(text, (26, config.SCREEN_HEIGHT - height + 2 + index * 20))
