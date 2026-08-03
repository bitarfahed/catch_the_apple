"""Backward-compatible application entry points.

The public launch interface lives in `catch_the_apple.sdk`. This module remains
as a small compatibility layer for earlier imports.
"""

from catch_the_apple.sdk import main

__all__ = ["main"]
