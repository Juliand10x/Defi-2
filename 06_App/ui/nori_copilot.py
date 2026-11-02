"""Backward compatibility wrapper: redirige a Kibo Copilot."""

from ui.kibo_copilot import (
    STEP_GUIDES,
    render_step_insight,
    open_copilot_modal,
    render_copilot_badge,
)

__all__ = [
    "STEP_GUIDES",
    "render_step_insight",
    "open_copilot_modal",
    "render_copilot_badge",
]
