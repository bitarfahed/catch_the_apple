"""Public SDK for launching and controlling Catch the Apple.

The SDK is the supported integration point for launchers, tests, and external
tools. Internal modules can still be imported by the game's own package, but
new consumers should prefer this small facade.
"""

from dataclasses import dataclass

from catch_the_apple._version import __version__
from catch_the_apple.game import Game


@dataclass(frozen=True)
class GameRunConfig:
    """Runtime options exposed by the public SDK."""

    auto_start: bool = False


class GameSDK:
    """Supported public interface for creating and running the game."""

    def __init__(self, run_config: GameRunConfig | None = None) -> None:
        self.run_config = run_config or GameRunConfig()

    def create_game(self) -> Game:
        """Create a configured game instance without starting the loop."""

        return Game()

    def run(self) -> int:
        """Create and run the game, returning a process-style exit code."""

        game = self.create_game()
        game.run()
        return 0


def create_game() -> Game:
    """Create a game instance through the public SDK surface."""

    return GameSDK().create_game()


def run_game() -> int:
    """Run the game through the public SDK surface."""

    return GameSDK().run()


def get_version() -> str:
    """Return the project version."""

    return __version__


def main() -> int:
    """Console-script compatible entry point."""

    return run_game()
