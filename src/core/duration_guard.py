"""The 3-minute rule.

`check` decides whether an imported video is short enough to recap and
`shortfall` reports how much must be trimmed. The Editor and the Recap tab
both call this before transcription starts so the user is told early.
"""

from __future__ import annotations

from dataclasses import dataclass

LIMIT_S = 180
WARN_AT_S = 150  # nudge the user once they are within 30s of the limit


@dataclass(frozen=True)
class GuardResult:
    ok: bool
    duration_s: float
    over_by_s: float
    warn: bool


def check(duration_s: float, limit_s: int = LIMIT_S) -> GuardResult:
    over = max(0.0, duration_s - limit_s)
    return GuardResult(
        ok=duration_s <= limit_s,
        duration_s=duration_s,
        over_by_s=over,
        warn=limit_s - 30 < duration_s <= limit_s,
    )


def fmt_mm(seconds: float) -> str:
    """Format a duration for display, e.g. 3:12."""
    seconds = max(0, int(round(seconds)))
    return f"{seconds // 60}:{seconds % 60:02d}"
