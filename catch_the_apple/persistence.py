from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from typing import Any

from catch_the_apple.audio import AudioSettings
from catch_the_apple.events import GameplayEvent, ObjectCaughtEvent, ObjectMissedEvent
from catch_the_apple.session import GameSession


SAVE_VERSION = 1


@dataclass
class SessionStatistics:
    sessions_played: int = 0
    total_score: int = 0
    total_catches: int = 0
    total_misses: int = 0


@dataclass
class SaveData:
    version: int = SAVE_VERSION
    high_score: int = 0
    best_combo: int = 0
    settings: AudioSettings = field(default_factory=AudioSettings)
    statistics: SessionStatistics = field(default_factory=SessionStatistics)


class PersistenceStore:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path.home() / ".catch_the_apple" / "save.json"
        self.data = self.load()

    def load(self) -> SaveData:
        if not self.path.exists():
            return SaveData()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            return self._parse(raw)
        except (AttributeError, OSError, json.JSONDecodeError, TypeError, ValueError):
            return SaveData()

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.to_json(), indent=2), encoding="utf-8")

    def save_settings(self, settings: AudioSettings) -> None:
        self.data.settings = settings
        self.save()

    def record_events(self, events: list[GameplayEvent]) -> None:
        for event in events:
            if isinstance(event, ObjectCaughtEvent):
                self.data.statistics.total_catches += 1
            if isinstance(event, ObjectMissedEvent):
                self.data.statistics.total_misses += 1

    def finish_session(self, session: GameSession) -> None:
        self.data.statistics.sessions_played += 1
        self.data.statistics.total_score += session.score
        self.data.high_score = max(self.data.high_score, session.score)
        self.data.best_combo = max(self.data.best_combo, session.best_combo)
        self.save()

    def to_json(self) -> dict[str, Any]:
        return {
            "version": self.data.version,
            "high_score": self.data.high_score,
            "best_combo": self.data.best_combo,
            "settings": asdict(self.data.settings),
            "statistics": asdict(self.data.statistics),
        }

    def _parse(self, raw: dict[str, Any]) -> SaveData:
        if not isinstance(raw, dict):
            return SaveData()
        settings = raw.get("settings", {})
        if not isinstance(settings, dict):
            settings = {}
        statistics = raw.get("statistics", {})
        if not isinstance(statistics, dict):
            statistics = {}
        return SaveData(
            version=int(raw.get("version", SAVE_VERSION)),
            high_score=int(raw.get("high_score", 0)),
            best_combo=int(raw.get("best_combo", 0)),
            settings=AudioSettings(
                master_volume=float(settings.get("master_volume", 0.8)),
                music_volume=float(settings.get("music_volume", 0.7)),
                effects_volume=float(settings.get("effects_volume", 0.8)),
                muted=bool(settings.get("muted", False)),
            ),
            statistics=SessionStatistics(
                sessions_played=int(statistics.get("sessions_played", 0)),
                total_score=int(statistics.get("total_score", 0)),
                total_catches=int(statistics.get("total_catches", 0)),
                total_misses=int(statistics.get("total_misses", 0)),
            ),
        )
