"""Public SDK surface for Catch the Apple.

External tools should import from this module instead of reaching into the
package's internal gameplay, rendering, or state modules.
"""

from catch_the_apple._version import __version__
from catch_the_apple.sdk import GameRunConfig, GameSDK, create_game, get_version, main, run_game

__all__ = [
    "GameRunConfig",
    "GameSDK",
    "__version__",
    "create_game",
    "get_version",
    "main",
    "run_game",
]
