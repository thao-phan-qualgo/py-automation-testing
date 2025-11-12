"""
Web step definitions package.

This package contains all BDD step definitions for web UI testing.
"""

# Explicitly import step modules to ensure they're registered with Behave
from . import login_steps, overview_steps

__all__ = ["login_steps", "overview_steps"]
