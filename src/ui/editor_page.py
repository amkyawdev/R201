"""TAB 2 — Editor.

Full-bleed preview with draggable subtitle + logo overlays, safe-area
guides that fade in on drag, and a draggable bottom sheet for type
settings. Overlay positions are stored normalised (0..1) on ProjectState
so they survive orientation switches.
"""

from __future__ import annotations

import flet as ft

from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import glass_card, gradient_button, pill_chip

PALETTE = ["#FFFFFF", t.GOLD, t.CYAN, t.VIOLET, "#FF6B6B"]
FONTS = ["Padauk", "Noto Sans Myanmar", "Inter"]


def build(page: ft.Page, state: ProjectState, on_change) -> ft.Control:
    preview = ft.Container(
        expand=True,
        border_radius=t.R20,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        gradient=ft.LinearGradient(colors=["#141B26", "#090D13"]),
        content=ft.Stack(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.MOVIE_ROUNDED, size=64, color=t.TEXT_FAINT),
                ),
                _overlay(state.subtitle, ft.Alignment.BOTTOM_CENTER, 0),
                _overlay(state.logo, ft.Alignment.TOP_LEFT, 1),
            ],
        ),
    )

    def slider(label: str, value: float, lo: float, hi: float, on_set) -> ft.Column:
        return ft.Column(
            spacing=t.S1, tight=True,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text(label, size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                        ft.Text(str(int(value)), size=t.TYPE_CAPTION, color=t.CYAN),
                    ],
                ),
                ft.Slider(
                    value=value, min=lo, max=hi, divisions=int(hi - lo),
                    active_color=t.VIOLET, inactive_color=t.SURFACE_2,
                    thumb_color=t.TEXT, on_change=lambda e: on_set(float(e.control.value)),
                ),
            ],
        )

    sheet = glass_card(
        ft.Column(
            spacing=t.S4,
            controls=[
                ft.Container(
                    width=40, height=4, border_radius=2, bgcolor=t.BORDER_STRONG,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Text("စာသား ချိန်ညှိမှု", size=t.TYPE_TITLE,
                                weight=ft.FontWeight.W_600, color=t.TEXT),
                        pill_chip(state.orientation),
                    ],
                ),
                ft.TextField(
                    value=state.subtitle.text,
                    hint_text="မြန်မာ စာတန်းထိုး ရိုက်ထည့်ပါ",
                    multiline=True, min_lines=2, max_lines=3,
                    bgcolor=t.SURFACE_2, border_color=t.BORDER,
                    border_radius=t.R12, color=t.TEXT, text_size=t.TYPE_BODY,
                    on_change=lambda e: _set_text(state, e.control.value, on_change),
                ),
                slider("အရွယ်အစား", state.subtitle.size, 14, 72,
                       lambda v: _set_size(state, v, on_change)),
                ft.Row(
                    spacing=t.S2,
                    controls=[
                        ft.Container(
                            width=32, height=32, border_radius=16,
                            bgcolor=c,
                            border=ft.Border.all(
                                2, t.CYAN if c == state.subtitle.colour else t.BORDER
                            ),
                            on_click=lambda e, col=c: _set_colour(state, col, on_change),
                            ink=True,
                        )
                        for c in PALETTE
                    ],
                ),
                ft.Row(
                    spacing=t.S2,
                    controls=[
                        ft.Container(
                            content=ft.Text(f, size=t.TYPE_CAPTION,
                                            color="#FFFFFF" if f == state.subtitle.font else t.TEXT_MUTED),
                            padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                            border_radius=t.R_PILL,
                            gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY) if f == state.subtitle.font else None,
                            bgcolor=None if f == state.subtitle.font else t.GLASS,
                            border=ft.Border.all(1, t.BORDER),
                            on_click=lambda e, ff=f: _set_font(state, ff, on_change),
                            ink=True,
                        )
                        for f in FONTS
                    ],
                ),
                ft.Row(
                    spacing=t.S3,
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                spacing=6, alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.RESTART_ALT_ROUNDED, size=16, color=t.TEXT),
                                    ft.Text("နေရာ ပြန်ညှိ", size=t.TYPE_CAPTION, color=t.TEXT),
                                ],
                            ),
                            expand=True, height=44, alignment=ft.Alignment.CENTER,
                            border_radius=t.R_PILL, border=ft.Border.all(1, t.BORDER_STRONG),
                            on_click=lambda e: _reset(state, on_change), ink=True,
                        ),
                        ft.Container(
                            content=ft.Text("သိမ်းမည်", size=t.TYPE_CAPTION,
                                            color="#FFFFFF", weight=ft.FontWeight.W_600),
                            expand=True, height=44, alignment=ft.Alignment.CENTER,
                            border_radius=t.R_PILL,
                            gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                            on_click=lambda e: on_change(), ink=True,
                        ),
                    ],
                ),
            ],
        ),
        radius=t.R24, padding=t.S5,
    )

    return ft.Column(
        expand=True, spacing=t.S4,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("တည်းဖြတ်", size=t.TYPE_DISPLAY, weight=ft.FontWeight.W_700, color=t.TEXT),
                    pill_chip("9:16 ⇄ 16:9"),
                ],
            ),
            ft.Container(content=preview, height=320),
            sheet,
        ],
    )


def _overlay(model, anchor, idx: int) -> ft.Container:
    return ft.Container(
        left=None if anchor == ft.Alignment.TOP_LEFT else 0,
        top=0 if anchor == ft.Alignment.TOP_LEFT else None,
        alignment=anchor,
        content=ft.Container(
            content=ft.Text(model.text or "စာတန်းထိုး", size=model.size,
                            color=model.colour, font_family=model.font),
            padding=t.S2,
            border=ft.Border.all(1, t.CYAN if idx == 0 else t.BORDER),
            border_radius=t.R8,
        ),
    )


def _set_text(state, value, cb):
    state.subtitle.text = value
    cb()


def _set_size(state, value, cb):
    state.subtitle.size = int(value)
    cb()


def _set_colour(state, value, cb):
    state.subtitle.colour = value
    cb()


def _set_font(state, value, cb):
    state.subtitle.font = value
    cb()


def _reset(state, cb):
    state.subtitle.x, state.subtitle.y = 0.5, 0.82
    cb()
