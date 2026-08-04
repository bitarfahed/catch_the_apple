import pygame


class ProceduralAppleRenderer:
    def __init__(self) -> None:
        self._cache: dict[tuple[str, int, tuple[int, int, int]], pygame.Surface] = {}

    def get_surface(
        self,
        identifier: str,
        size: int,
        base_color: tuple[int, int, int],
    ) -> pygame.Surface:
        key = (identifier, size, base_color)
        if key not in self._cache:
            self._cache[key] = self._create_surface(identifier, size, base_color)
        return self._cache[key]

    def _create_surface(
        self,
        identifier: str,
        size: int,
        base_color: tuple[int, int, int],
    ) -> pygame.Surface:
        if identifier == "bomb":
            return self._create_bomb_surface(size, base_color)
        if identifier == "power_up":
            return self._create_power_up_surface(size)

        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        body_rect = pygame.Rect(size * 0.12, size * 0.22, size * 0.76, size * 0.70)

        if identifier == "golden_apple":
            glow_rect = pygame.Rect(size * 0.02, size * 0.10, size * 0.96, size * 0.86)
            pygame.draw.ellipse(surface, (255, 218, 60, 92), glow_rect)
        if identifier == "rotten_apple":
            body_rect = pygame.Rect(size * 0.10, size * 0.26, size * 0.78, size * 0.64)

        shadow_color = scale_color(base_color, 0.58 if identifier == "rotten_apple" else 0.68)
        light_color = blend_color(base_color, (255, 255, 255), 0.36 if identifier == "golden_apple" else 0.24)
        highlight_color = (255, 245, 230, 130)

        pygame.draw.ellipse(surface, shadow_color, body_rect.move(1, 2))
        pygame.draw.ellipse(surface, base_color, body_rect)
        pygame.draw.ellipse(
            surface,
            light_color,
            pygame.Rect(size * 0.20, size * 0.24, size * 0.34, size * 0.42),
        )
        pygame.draw.ellipse(
            surface,
            highlight_color,
            pygame.Rect(size * 0.28, size * 0.32, size * 0.16, size * 0.18),
        )

        cleft_color = scale_color(base_color, 0.55)
        pygame.draw.arc(
            surface,
            cleft_color,
            pygame.Rect(size * 0.38, size * 0.16, size * 0.24, size * 0.30),
            3.4,
            5.8,
            max(1, size // 18),
        )

        stem_rect = pygame.Rect(size * 0.47, size * 0.06, max(2, size * 0.10), size * 0.22)
        pygame.draw.rect(surface, (96, 55, 28), stem_rect, border_radius=max(1, size // 18))

        leaf_points = [
            (size * 0.58, size * 0.16),
            (size * 0.86, size * 0.10),
            (size * 0.68, size * 0.30),
        ]
        pygame.draw.polygon(surface, (55, 145, 64), leaf_points)
        pygame.draw.line(
            surface,
            (86, 180, 82),
            (size * 0.61, size * 0.17),
            (size * 0.76, size * 0.15),
            1,
        )

        if identifier == "golden_apple":
            self._draw_star(surface, (int(size * 0.72), int(size * 0.36)), max(4, size // 5))
            pygame.draw.circle(surface, (255, 250, 150, 130), (int(size * 0.34), int(size * 0.42)), max(2, size // 9))
        if identifier == "rotten_apple":
            pygame.draw.circle(surface, (72, 105, 38), (int(size * 0.33), int(size * 0.55)), max(3, size // 8))
            pygame.draw.circle(surface, (44, 58, 32), (int(size * 0.64), int(size * 0.68)), max(2, size // 10))
            pygame.draw.arc(
                surface,
                (220, 210, 140),
                pygame.Rect(size * 0.18, size * 0.18, size * 0.62, size * 0.42),
                0.1,
                2.5,
                2,
            )

        return surface.convert_alpha()

    def _create_bomb_surface(self, size: int, base_color: tuple[int, int, int]) -> pygame.Surface:
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        shadow_color = scale_color(base_color, 0.42)
        highlight_color = blend_color(base_color, (255, 110, 95), 0.34)
        pygame.draw.circle(surface, shadow_color, (size // 2 + 1, int(size * 0.59) + 2), int(size * 0.35))
        pygame.draw.circle(surface, base_color, (size // 2, int(size * 0.58)), int(size * 0.34))
        pygame.draw.circle(surface, highlight_color, (int(size * 0.38), int(size * 0.46)), int(size * 0.12))
        pygame.draw.rect(surface, (58, 45, 32), pygame.Rect(size * 0.48, size * 0.13, size * 0.12, size * 0.20))
        pygame.draw.arc(
            surface,
            (210, 150, 70),
            pygame.Rect(size * 0.52, size * 0.00, size * 0.32, size * 0.28),
            1.2,
            3.5,
            2,
        )
        self._draw_star(surface, (int(size * 0.80), int(size * 0.10)), max(3, size // 7), (255, 105, 45))
        return surface.convert_alpha()

    def _create_power_up_surface(self, size: int) -> pygame.Surface:
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        points = [
            (size * 0.50, size * 0.04),
            (size * 0.92, size * 0.50),
            (size * 0.50, size * 0.96),
            (size * 0.08, size * 0.50),
        ]
        pygame.draw.circle(surface, (65, 235, 255, 70), (size // 2, size // 2), int(size * 0.48))
        pygame.draw.polygon(surface, (38, 170, 230), points)
        pygame.draw.polygon(surface, (155, 245, 255), points, 2)
        pygame.draw.circle(surface, (235, 255, 255, 190), (size // 2, size // 2), int(size * 0.16))
        pygame.draw.line(surface, (255, 255, 255, 180), (size * 0.32, size * 0.38), (size * 0.68, size * 0.62), 2)
        pygame.draw.line(surface, (255, 255, 255, 180), (size * 0.68, size * 0.38), (size * 0.32, size * 0.62), 2)
        return surface.convert_alpha()

    def _draw_star(
        self,
        surface: pygame.Surface,
        center: tuple[int, int],
        radius: int,
        color: tuple[int, int, int] = (255, 255, 190),
    ) -> None:
        x, y = center
        pygame.draw.line(surface, color, (x - radius, y), (x + radius, y), 2)
        pygame.draw.line(surface, color, (x, y - radius), (x, y + radius), 2)
        pygame.draw.line(surface, color, (x - radius // 2, y - radius // 2), (x + radius // 2, y + radius // 2), 1)
        pygame.draw.line(surface, color, (x + radius // 2, y - radius // 2), (x - radius // 2, y + radius // 2), 1)


class ProceduralBasketRenderer:
    def __init__(self) -> None:
        self._cache: dict[tuple[int, int], pygame.Surface] = {}

    def get_surface(self, width: int, height: int) -> pygame.Surface:
        key = (width, height)
        if key not in self._cache:
            self._cache[key] = self._create_surface(width, height)
        return self._cache[key]

    def _create_surface(self, width: int, height: int) -> pygame.Surface:
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        body_color = (166, 104, 43)
        dark_color = (104, 65, 31)
        light_color = (218, 153, 72)
        rim_color = (126, 77, 34)

        body_rect = pygame.Rect(0, height * 0.20, width, height * 0.80)
        pygame.draw.rect(surface, dark_color, body_rect, border_radius=max(2, height // 5))
        pygame.draw.rect(surface, body_color, body_rect.inflate(-2, -2), border_radius=max(2, height // 5))

        stripe_width = max(5, width // 12)
        for x in range(-height, width, stripe_width):
            pygame.draw.line(surface, light_color, (x, height), (x + height, height * 0.20), 2)
            pygame.draw.line(surface, dark_color, (x, height * 0.20), (x + height, height), 1)

        rim_rect = pygame.Rect(0, 0, width, max(5, height // 3))
        pygame.draw.rect(surface, rim_color, rim_rect, border_radius=max(2, height // 6))
        pygame.draw.rect(surface, light_color, rim_rect.inflate(-4, -3), border_radius=max(2, height // 7))
        pygame.draw.line(surface, (235, 183, 96), (4, 2), (width - 5, 2), 1)

        pygame.draw.rect(surface, (82, 49, 25, 150), surface.get_rect(), 1)
        return surface.convert_alpha()


class ProceduralAssetRenderer:
    def __init__(self) -> None:
        self.apples = ProceduralAppleRenderer()
        self.baskets = ProceduralBasketRenderer()

    def get_falling_object_surface(self, identifier: str, size: int, color: tuple[int, int, int]) -> pygame.Surface:
        return self.apples.get_surface(identifier, size, color)

    def get_basket_surface(self, width: int, height: int) -> pygame.Surface:
        return self.baskets.get_surface(width, height)


def scale_color(color: tuple[int, int, int], factor: float) -> tuple[int, int, int]:
    return tuple(max(0, min(255, int(channel * factor))) for channel in color)


def blend_color(
    color: tuple[int, int, int],
    target: tuple[int, int, int],
    amount: float,
) -> tuple[int, int, int]:
    return tuple(
        max(0, min(255, int(channel + (target_channel - channel) * amount)))
        for channel, target_channel in zip(color, target, strict=True)
    )
