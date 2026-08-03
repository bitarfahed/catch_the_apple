from dataclasses import dataclass

import pygame


@dataclass
class AudioSettings:
    master_volume: float = 0.8
    music_volume: float = 0.7
    effects_volume: float = 0.8
    muted: bool = False


class AudioSystem:
    def __init__(self, settings: AudioSettings | None = None) -> None:
        self.settings = settings or AudioSettings()
        self.available = False
        self.music: pygame.mixer.Sound | None = None
        self.sound_effects: dict[str, pygame.mixer.Sound] = {}
        self.ui_sounds: dict[str, pygame.mixer.Sound] = {}
        self.ambient_sounds: dict[str, pygame.mixer.Sound] = {}
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.available = True
        except pygame.error:
            self.available = False

    def set_settings(self, settings: AudioSettings) -> None:
        self.settings = settings
        self.apply_volumes()

    def set_master_volume(self, volume: float) -> None:
        self.settings.master_volume = clamp01(volume)
        self.apply_volumes()

    def set_music_volume(self, volume: float) -> None:
        self.settings.music_volume = clamp01(volume)
        self.apply_volumes()

    def set_effects_volume(self, volume: float) -> None:
        self.settings.effects_volume = clamp01(volume)
        self.apply_volumes()

    def toggle_mute(self) -> None:
        self.settings.muted = not self.settings.muted
        self.apply_volumes()

    def play_music(self) -> None:
        if self.available and self.music is not None:
            self.music.play(loops=-1)

    def play_effect(self, identifier: str) -> None:
        self._play(self.sound_effects.get(identifier), self.settings.effects_volume)

    def play_ui(self, identifier: str) -> None:
        self._play(self.ui_sounds.get(identifier), self.settings.effects_volume)

    def play_ambient(self, identifier: str) -> None:
        self._play(self.ambient_sounds.get(identifier), self.settings.music_volume)

    def apply_volumes(self) -> None:
        if not self.available:
            return
        music_volume = self.effective_volume(self.settings.music_volume)
        effects_volume = self.effective_volume(self.settings.effects_volume)
        for sound in [self.music, *self.ambient_sounds.values()]:
            if sound is not None:
                sound.set_volume(music_volume)
        for sound in [*self.sound_effects.values(), *self.ui_sounds.values()]:
            sound.set_volume(effects_volume)

    def effective_volume(self, channel_volume: float) -> float:
        if self.settings.muted:
            return 0.0
        return clamp01(self.settings.master_volume * channel_volume)

    def _play(self, sound: pygame.mixer.Sound | None, channel_volume: float) -> None:
        if not self.available or sound is None:
            return
        sound.set_volume(self.effective_volume(channel_volume))
        sound.play()


def clamp01(value: float) -> float:
    return max(0.0, min(1.0, value))
