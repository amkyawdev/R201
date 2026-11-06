"""TAB 3 — Voices.

Five Myanmar narrator cards. The selected card gets a gradient border and
a 2deg tilt; its waveform animates while a preview plays.
"""

from __future__ import annotations

import flet as ft

from core.tts_client import VOICES, Voice
from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import glass_card, waveform


def build(page: ft.Page, state: ProjectState, on_select, on_preview) -> ft.Control:
    playing_id: dict[str, str | None] = {"id": None}

    def card(voice: Voice, index: int) -> ft.Container:
        selected = voice.id == state.voice_id
        playing = playing_id["id"] == voice.id

        return glass_card(
            ft.Row(
                spacing=t.S4,
                controls=[
                    ft.Container(
                        width=52, height=52, border_radius=26,
                        gradient=ft.LinearGradient(
                            colors=t.GRAD_GOLD if selected else [t.SURFACE_2, t.SURFACE]
                        ),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.RECORD_VOICE_OVER_ROUNDED,
                            color=t.BG if selected else t.TEXT_MUTED, size=24,
                        ),
                    ),
                    ft.Column(
                        expand=True, spacing=t.S2, tight=True,
                        controls=[
                            ft.Text(voice.label, size=t.TYPE_BODY,
                                    weight=ft.FontWeight.W_600,
                                    color=t.TEXT if selected else t.TEXT_MUTED),
                            ft.Container(
                                content=waveform(seed=index, bars=20, height=22),
                                opacity=1.0 if playing else 0.45,
                                animate_opacity=ft.Animation(t.D_TAB, ft.AnimationCurve.EASE_IN_OUT),
                            ),
                        ],
                    ),
                    ft.Container(
                        width=44, height=44, border_radius=22,
                        bgcolor=t.GLASS, border=ft.Border.all(1, t.BORDER),
                        alignment=ft.Alignment.CENTER,
                        content=ft.Icon(
                            ft.Icons.PAUSE_ROUNDED if playing else ft.Icons.PLAY_ARROW_ROUNDED,
                            color=t.CYAN if playing else t.TEXT, size=22,
                        ),
                        on_click=lambda e, v=voice: _toggle(v, playing_id, on_preview),
                        ink=True,
                    ),
                ],
            ),
            radius=t.R20,
            padding=t.S4,
            border_colour=t.GOLD if selected else t.BORDER,
        )

    def select(voice: Voice) -> None:
        state.voice_id = voice.id
        state.voice_label = voice.label
        on_select()

    return ft.Column(
        expand=True, spacing=t.S4,
        controls=[
            ft.Column(
                spacing=2, tight=True,
                controls=[
                    ft.Text("အသံ ရွေးချယ်မှု", size=t.TYPE_DISPLAY,
                            weight=ft.FontWeight.W_700, color=t.TEXT),
                    ft.Text("မြန်မာ အသံ ၅ မျိုးမှ ရွေးပါ", size=t.TYPE_BODY, color=t.TEXT_MUTED),
                ],
            ),
            ft.Column(spacing=t.S3, controls=[card(v, i) for i, v in enumerate(VOICES)]),
            ft.Container(
                content=ft.Text("ရွေးချယ်မည်", color="#FFFFFF", weight=ft.FontWeight.W_600),
                height=52, alignment=ft.Alignment.CENTER,
                border_radius=t.R_PILL,
                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                on_click=lambda e: select(next(v for v in VOICES if v.id == state.voice_id)),
                ink=True,
            ),
        ],
    )


def _toggle(voice: Voice, playing_id: dict, on_preview) -> None:
    playing_id["id"] = None if playing_id["id"] == voice.id else voice.id
    on_preview(voice, playing_id["id"] is not None)
