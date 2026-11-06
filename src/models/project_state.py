"""In-memory project state for an editing session.

Holds the transcript, the voiceover choice and the overlay geometry
(text + logo position/colour/size) that the Editor tab mutates.
"""

from dataclasses import dataclass, field
from typing import Literal

Orientation = Literal["9:16", "16:9"]


@dataclass
class Overlay:
    """A draggable layer drawn on top of the preview."""

    text: str
    x: float = 0.5          # normalised 0..1, centre-anchored
    y: float = 0.82
    size: int = 34
    colour: str = "#FFFFFF"
    font: str = "Padauk"


@dataclass
class ProjectState:
    name: str = "Untitled recap"
    source_path: str | None = None
    duration_s: float = 0.0
    orientation: Orientation = "16:9"

    transcript: list[str] = field(default_factory=list)
    summary: str = ""

    voice_id: str = "mm_female_1"
    voice_label: str = "မြန်မာ အမျိုးသမီး ၁"

    subtitle: Overlay = field(default_factory=lambda: Overlay(text=""))
    logo: Overlay = field(default_factory=lambda: Overlay(text="LOGO", x=0.14, y=0.12, size=22))

    resolution: str = "1080p"
    fmt: str = "MP4"
    quality: int = 80

    def reset(self) -> None:
        self.__init__()  # type: ignore[misc]
