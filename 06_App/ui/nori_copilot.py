"""Backward compatibility wrapper: redirige a Kibo Copilot."""

try:
    from ui.kibo_copilot import (
        STEP_GUIDES,
        render_step_insight,
        open_copilot_modal,
        render_copilot_badge,
    )
except (ImportError, ModuleNotFoundError):
    from kibo_copilot import (
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
