"""TAB 3 — Voices.

Five Myanmar narrator cards. The selected card gets a gold border and its
waveform lights up while a preview plays. Selection and playback update the
affected cards in place, so the list never jumps back to the top.
"""

from __future__ import annotations

import flet as ft

from core.tts_client import VOICES, Voice
from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import glass_card, waveform

CardParts = tuple[ft.Container, ft.Container, ft.Container, ft.Icon, ft.Text]


def build(page: ft.Page, state: ProjectState, on_select, on_preview) -> ft.Control:
    cards: dict[str, CardParts] = {}

    def make_card(voice: Voice, index: int) -> ft.Container:
        selected = voice.id == state.voice_id
        badge = ft.Container(
            width=52, height=52, border_radius=26,
            gradient=ft.LinearGradient(
                colors=t.GRAD_GOLD if selected else [t.SURFACE_2, t.SURFACE]
            ),
            alignment=ft.Alignment.CENTER,
            content=ft.Icon(
                ft.Icons.RECORD_VOICE_OVER_ROUNDED,
                color=t.BG if selected else t.TEXT_MUTED, size=24,
            ),
        )
        label = ft.Text(
            voice.label, size=t.TYPE_BODY, weight=ft.FontWeight.W_600,
            color=t.TEXT if selected else t.TEXT_MUTED,
        )
        wave_holder = ft.Container(
            content=waveform(seed=index, bars=20, height=22),
            opacity=0.45,
            animate_opacity=ft.Animation(t.D_TAB, ft.AnimationCurve.EASE_IN_OUT),
        )
        play_icon = ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, color=t.TEXT, size=22)
        play_btn = ft.Container(
            width=44, height=44, border_radius=22,
            bgcolor=t.GLASS, border=ft.Border.all(1, t.BORDER),
            alignment=ft.Alignment.CENTER,
            content=play_icon,
            on_click=lambda e, v=voice: toggle(v),
            ink=True,
        )
        card = glass_card(
            ft.Row(
                spacing=t.S4,
                controls=[
                    badge,
                    ft.Column(
                        expand=True, spacing=t.S2, tight=True,
                        controls=[label, wave_holder],
                    ),
                    play_btn,
                ],
            ),
            radius=t.R20,
            padding=t.S4,
            border_colour=t.GOLD if selected else t.BORDER,
        )
        card.on_click = lambda e, v=voice: select(v)
        cards[voice.id] = (card, badge, wave_holder, play_icon, label)
        return card

    def paint_selection(voice_id: str) -> None:
        for vid, (card, badge, _wave, _icon, label) in cards.items():
            active = vid == voice_id
            card.border = ft.Border.all(1, t.GOLD if active else t.BORDER)
            badge.gradient = ft.LinearGradient(
                colors=t.GRAD_GOLD if active else [t.SURFACE_2, t.SURFACE]
            )
            badge.content.color = t.BG if active else t.TEXT_MUTED
            label.color = t.TEXT if active else t.TEXT_MUTED
            card.update()

    def select(voice: Voice) -> None:
        state.voice_id = voice.id
        state.voice_label = voice.label
        paint_selection(voice.id)
        on_select()

    def toggle(voice: Voice) -> None:
        _, _, _wave, icon, _label = cards[voice.id]
        playing = icon.icon != ft.Icons.PAUSE_ROUNDED
        for vid, (_card, _b, wave, ic, _lbl) in cards.items():
            on = vid == voice.id and playing
            wave.opacity = 1.0 if on else 0.45
            ic.icon = ft.Icons.PAUSE_ROUNDED if on else ft.Icons.PLAY_ARROW_ROUNDED
            ic.color = t.CYAN if on else t.TEXT
            wave.update()
            ic.update()
        on_preview(voice, playing)

    def current() -> Voice:
        return next((v for v in VOICES if v.id == state.voice_id), VOICES[0])

    return ft.Column(
        spacing=t.S4,
        controls=[
            ft.Column(
                spacing=2, tight=True,
                controls=[
                    ft.Text("အသံ ရွေးချယ်မှု", size=t.TYPE_DISPLAY,
                            weight=ft.FontWeight.W_700, color=t.TEXT),
                    ft.Text("မြန်မာ အသံ ၅ မျိုးမှ ရွေးပါ",
                            size=t.TYPE_BODY, color=t.TEXT_MUTED),
                ],
            ),
            ft.Column(
                spacing=t.S3,
                controls=[make_card(v, i) for i, v in enumerate(VOICES)],
            ),
            ft.Container(
                content=ft.Text("ရွေးချယ်မည်", color="#FFFFFF",
                                weight=ft.FontWeight.W_600),
                height=52, alignment=ft.Alignment.CENTER,
                border_radius=t.R_PILL,
                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                on_click=lambda e: select(current()),
                ink=True,
            ),
        ],
    )
