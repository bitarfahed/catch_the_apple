from dataclasses import dataclass, field
import math

from catch_the_apple.lighting import DirectionalLight, LightingConfig
from catch_the_apple.math2d import Vector2, clamp, vec2


@dataclass(frozen=True)
class WindConfig:
    direction: Vector2 = field(default_factory=lambda: vec2(1.0, 0.0))
    strength: float = 8.0
    gust_strength: float = 6.0
    gust_frequency: float = 0.45
    direction_sway: float = 0.16


@dataclass
class WindState:
    direction: Vector2
    strength: float
    velocity: Vector2


class WindSystem:
    def __init__(self, wind_config: WindConfig | None = None) -> None:
        self.config = wind_config or WindConfig()
        self.state = WindState(
            direction=self.normalized_direction,
            strength=self.config.strength,
            velocity=self.normalized_direction * self.config.strength,
        )

    @property
    def normalized_direction(self) -> Vector2:
        direction = Vector2(self.config.direction)
        if direction.length_squared() == 0.0:
            return vec2(1.0, 0.0)
        return direction.normalize()

    def update(self, elapsed_time: float) -> WindState:
        base = self.normalized_direction * self.config.strength
        primary = vec2(
            math.sin(elapsed_time * math.tau * self.config.gust_frequency),
            math.cos(elapsed_time * 0.73),
        ) * (self.config.strength + self.config.gust_strength)
        secondary = vec2(
            math.sin(elapsed_time * 0.41 + 1.7),
            math.sin(elapsed_time * 0.29 - 0.8),
        ) * (self.config.gust_strength * 0.85)
        swirl = vec2(
            math.sin(elapsed_time * 0.19 + 2.4),
            math.cos(elapsed_time * 0.31),
        ) * (self.config.direction_sway * self.config.strength * 3.0)
        velocity = base * 0.28 + primary + secondary + swirl
        strength = velocity.length()
        direction = velocity.normalize() if strength > 0.0 else self.normalized_direction
        self.state = WindState(direction=direction, strength=strength, velocity=velocity)
        return self.state


@dataclass(frozen=True)
class WeatherPreset:
    name: str
    wind: WindConfig
    visual_tint: tuple[int, int, int]
    cloudiness: float
    fog_alpha: int
    particle_wind_scale: float
    gameplay_wind_scale: float


WEATHER_PRESETS = {
    "clear": WeatherPreset(
        name="Clear",
        wind=WindConfig(strength=4.0, gust_strength=2.0, gust_frequency=0.2),
        visual_tint=(255, 255, 255),
        cloudiness=0.25,
        fog_alpha=0,
        particle_wind_scale=0.25,
        gameplay_wind_scale=0.0,
    ),
    "light_wind": WeatherPreset(
        name="Light Wind",
        wind=WindConfig(strength=10.0, gust_strength=5.0, gust_frequency=0.35),
        visual_tint=(245, 250, 245),
        cloudiness=0.35,
        fog_alpha=0,
        particle_wind_scale=0.45,
        gameplay_wind_scale=0.04,
    ),
    "strong_wind": WeatherPreset(
        name="Strong Wind",
        wind=WindConfig(strength=22.0, gust_strength=10.0, gust_frequency=0.55),
        visual_tint=(235, 242, 238),
        cloudiness=0.50,
        fog_alpha=0,
        particle_wind_scale=0.70,
        gameplay_wind_scale=0.08,
    ),
    "rain": WeatherPreset(
        name="Rain",
        wind=WindConfig(strength=13.0, gust_strength=5.0, gust_frequency=0.4),
        visual_tint=(185, 205, 218),
        cloudiness=0.90,
        fog_alpha=20,
        particle_wind_scale=0.55,
        gameplay_wind_scale=0.03,
    ),
    "falling_leaves": WeatherPreset(
        name="Falling Leaves",
        wind=WindConfig(strength=9.0, gust_strength=7.0, gust_frequency=0.3),
        visual_tint=(255, 238, 205),
        cloudiness=0.40,
        fog_alpha=0,
        particle_wind_scale=0.65,
        gameplay_wind_scale=0.02,
    ),
    "fog": WeatherPreset(
        name="Fog",
        wind=WindConfig(strength=3.0, gust_strength=2.0, gust_frequency=0.15),
        visual_tint=(215, 225, 225),
        cloudiness=0.75,
        fog_alpha=55,
        particle_wind_scale=0.20,
        gameplay_wind_scale=0.0,
    ),
}


@dataclass
class DayNightState:
    progress: float
    sky_top: tuple[int, int, int]
    sky_bottom: tuple[int, int, int]
    ambient: float
    directional_intensity: float
    shadow_intensity: float
    sun_position: tuple[int, int]
    moon_position: tuple[int, int]


class DayNightCycle:
    def __init__(self, duration: float = 120.0, start_progress: float = 0.28) -> None:
        self.duration = duration
        self.progress = start_progress

    def update(self, delta_time: float) -> DayNightState:
        self.progress = (self.progress + delta_time / self.duration) % 1.0
        return self.state

    @property
    def state(self) -> DayNightState:
        daylight = (math.sin(self.progress * math.tau - math.pi / 2) + 1.0) / 2.0
        daylight = smoothstep(daylight)
        sky_top = blend_color((2, 9, 38), (102, 198, 255), daylight)
        sky_bottom = blend_color((10, 18, 70), (112, 176, 228), daylight)
        ambient = 0.24 + daylight * 0.68
        directional = 0.08 + daylight * 0.66
        shadow = 0.20 + daylight * 0.43
        angle = self.progress * math.tau
        sun_position = (int(400 + math.cos(angle - math.pi / 2) * 330), int(350 + math.sin(angle - math.pi / 2) * 260))
        moon_position = (int(400 + math.cos(angle + math.pi / 2) * 330), int(350 + math.sin(angle + math.pi / 2) * 260))
        return DayNightState(
            progress=self.progress,
            sky_top=sky_top,
            sky_bottom=sky_bottom,
            ambient=ambient,
            directional_intensity=directional,
            shadow_intensity=shadow,
            sun_position=sun_position,
            moon_position=moon_position,
        )

    def lighting_config(self, ground_y: int) -> LightingConfig:
        state = self.state
        return LightingConfig(
            ambient=state.ambient,
            directional=DirectionalLight(direction=vec2(-0.65, 0.45), intensity=state.directional_intensity),
            specular_intensity=0.16 + state.directional_intensity * 0.20,
            shadow_intensity=state.shadow_intensity,
            ground_y=ground_y,
        )


@dataclass
class EnvironmentState:
    elapsed_time: float
    wind: WindState
    weather: WeatherPreset
    day_night: DayNightState
    lighting: LightingConfig


class EnvironmentManager:
    def __init__(
        self,
        weather_name: str = "clear",
        wind_config: WindConfig | None = None,
        gameplay_wind_scale: float | None = None,
    ) -> None:
        self.elapsed_time = 0.0
        self.weather = WEATHER_PRESETS[weather_name]
        self.wind_config_override = wind_config
        self.gameplay_wind_scale_override = gameplay_wind_scale
        self.wind = WindSystem(wind_config or self.weather.wind)
        self.day_night = DayNightCycle()
        self._weather_order = ("clear", "light_wind", "rain", "falling_leaves", "strong_wind", "fog")
        self._weather_index = self._weather_order.index(weather_name)
        self._weather_timer = 0.0
        self._weather_interval = 24.0
        self.state = self._build_state()

    def set_weather(self, weather_name: str) -> None:
        self.weather = WEATHER_PRESETS[weather_name]
        self._weather_index = self._weather_order.index(weather_name)
        self.wind = WindSystem(self.wind_config_override or self.weather.wind)
        self.state = self._build_state()

    def update(self, delta_time: float) -> EnvironmentState:
        self.elapsed_time += delta_time
        self.update_weather_cycle(delta_time)
        self.wind.update(self.elapsed_time)
        self.day_night.update(delta_time)
        self.state = self._build_state()
        return self.state

    def update_weather_cycle(self, delta_time: float) -> None:
        self._weather_timer += delta_time
        while self._weather_timer >= self._weather_interval:
            self._weather_timer -= self._weather_interval
            self._weather_index = (self._weather_index + 1) % len(self._weather_order)
            self.weather = WEATHER_PRESETS[self._weather_order[self._weather_index]]
            self.wind = WindSystem(self.wind_config_override or self.weather.wind)

    def gameplay_wind_velocity(self) -> Vector2:
        scale = (
            self.gameplay_wind_scale_override
            if self.gameplay_wind_scale_override is not None
            else self.state.weather.gameplay_wind_scale
        )
        return self.state.wind.velocity * scale

    @property
    def wind_response(self) -> float:
        return 3.7

    def particle_wind_velocity(self) -> Vector2:
        return self.state.wind.velocity * self.state.weather.particle_wind_scale

    def _build_state(self) -> EnvironmentState:
        return EnvironmentState(
            elapsed_time=self.elapsed_time,
            wind=self.wind.state,
            weather=self.weather,
            day_night=self.day_night.state,
            lighting=self.day_night.lighting_config(ground_y=570),
        )


def blend_color(
    start: tuple[int, int, int],
    end: tuple[int, int, int],
    amount: float,
) -> tuple[int, int, int]:
    amount = clamp(amount, 0.0, 1.0)
    return tuple(int(a + (b - a) * amount) for a, b in zip(start, end, strict=True))


def smoothstep(value: float) -> float:
    value = clamp(value, 0.0, 1.0)
    return value * value * (3.0 - 2.0 * value)
