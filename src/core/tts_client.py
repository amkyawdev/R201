"""Text-to-speech for the five Myanmar narrator voices.

Uses edge-tts, which is free and needs no API key. The five voices are
presented to the user with Myanmar labels; the underlying engine voice is
mapped in VOICES. `preview` writes a short mp3 for the Voices tab and
`synthesise` renders the full recap narration.
"""

from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass

try:  # edge-tts is an optional runtime dependency
    import edge_tts
except ImportError:  # pragma: no cover - surfaced to the UI as a friendly error
    edge_tts = None  # type: ignore[assignment]


@dataclass(frozen=True)
class Voice:
    id: str
    label: str          # Myanmar label shown in the UI
    engine: str         # edge-tts voice name
    gender: str
    pitch: str = "+0Hz"


VOICES: tuple[Voice, ...] = (
    Voice("mm_female_1", "မြန်မာ အမျိုးသမီး ၁", "my-MM-NilarNeural", "female"),
    Voice("mm_female_2", "မြန်မာ အမျိုးသမီး ၂", "my-MM-NilarNeural", "female", "-2Hz"),
    Voice("mm_male_1", "မြန်မာ အမျိုးသား ၁", "my-MM-ThihaNeural", "male"),
    Voice("mm_male_2", "မြန်မာ အမျိုးသား ၂", "my-MM-ThihaNeural", "male", "+3Hz"),
    Voice("mm_male_3", "မြန်မာ အမျိုးသား ၃", "my-MM-ThihaNeural", "male", "-3Hz"),
)

PREVIEW_TEXT = "မင်္ဂလာပါ၊ ဒီဇာတ်ကားရဲ့ အနှစ်ချုပ်ကို နားထောင်ကြည့်ပါ။"


def voice_by_id(voice_id: str) -> Voice:
    for v in VOICES:
        if v.id == voice_id:
            return v
    return VOICES[0]


class TTSClient:
    def _require(self) -> None:
        if edge_tts is None:
            raise RuntimeError(
                "edge-tts is not installed. Run: pip install edge-tts"
            )

    async def _render(self, text: str, voice: Voice, out_path: str, rate: str) -> str:
        comm = edge_tts.Communicate(
            text, voice.engine, rate=rate, pitch=voice.pitch
        )
        await comm.save(out_path)
        return out_path

    def preview(self, voice: Voice, out_dir: str) -> str:
        """Render the short preview clip used by the Voices tab."""
        self._require()
        os.makedirs(out_dir, exist_ok=True)
        out = os.path.join(out_dir, f"voice_{voice.id}.mp3")
        if not os.path.exists(out):
            asyncio.run(self._render(PREVIEW_TEXT, voice, out, rate="+0%"))
        return out

    def synthesise(self, text: str, voice: Voice, out_path: str, rate: str = "+0%") -> str:
        """Render the full narration to out_path."""
        self._require()
        os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
        asyncio.run(self._render(text, voice, out_path, rate=rate))
        return out_path
