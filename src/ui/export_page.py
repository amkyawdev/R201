"""TAB 4 — Export.

Resolution / format pickers, a quality slider, the pulsing export button
and the ring-progress "thinking" state with a rotating gradient border.
"""

from __future__ import annotations

import flet as ft

from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import glass_card, pill_chip, segmented

RESOLUTIONS = ["720p", "1080p", "4K"]
FORMATS = ["MP4", "MOV"]


def build(page: ft.Page, state: ProjectState, on_export, on_change) -> ft.Control:
    progress_ring = ft.ProgressRing(
        width=96, height=96, stroke_width=4,
        color=t.CYAN, bgcolor=t.SURFACE_2, value=0.0,
        visible=False,
    )

    def export_clicked(_e):
        progress_ring.visible = True
        progress_ring.value = 0.35
        page.update()
        on_export()

    return ft.Column(
        expand=True, spacing=t.S5,
        controls=[
            ft.Text("ထုတ်ယူမှု", size=t.TYPE_DISPLAY, weight=ft.FontWeight.W_700, color=t.TEXT),

            glass_card(
                ft.Column(
                    spacing=t.S4,
                    controls=[
                        ft.Text("ကြည်လင်ပြတ်သားမှု", size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                        segmented(RESOLUTIONS, RESOLUTIONS.index(state.resolution),
                                  lambda i: _set(state, "resolution", RESOLUTIONS[i], on_change)),
                        ft.Text("ဖိုင်အမျိုးအစား", size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                        segmented(FORMATS, FORMATS.index(state.fmt),
                                  lambda i: _set(state, "fmt", FORMATS[i], on_change)),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            glass_card(
                ft.Column(
                    spacing=t.S2,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("အရည်အသွေး", size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                                ft.Text(f"{state.quality}%", size=t.TYPE_CAPTION, color=t.CYAN),
                            ],
                        ),
                        ft.Slider(
                            value=state.quality, min=0, max=100, divisions=20,
                            active_color=t.VIOLET, inactive_color=t.SURFACE_2,
                            thumb_color=t.TEXT,
                            on_change=lambda e: _set(state, "quality", int(float(e.control.value)), on_change),
                        ),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            glass_card(
                ft.Row(
                    spacing=t.S4,
                    controls=[
                        progress_ring,
                        ft.Column(
                            spacing=t.S1, tight=True,
                            controls=[
                                ft.Text("ပြင်ဆင်နေသည်", size=t.TYPE_BODY,
                                        weight=ft.FontWeight.W_600, color=t.TEXT),
                                ft.Text("အသံနှင့် ဗီဒီယို ပေါင်းစပ်နေသည်…",
                                        size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                                ft.Row(spacing=6, controls=[
                                    pill_chip("ffmpeg", dot=True),
                                    pill_chip("edge-tts"),
                                ]),
                            ],
                        ),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            ft.Container(expand=True),
            ft.Container(
                content=ft.Row(
                    spacing=t.S2, alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.IOS_SHARE_ROUNDED, color="#FFFFFF", size=20),
                        ft.Text("ထုတ်ယူမည်", size=t.TYPE_BODY,
                                weight=ft.FontWeight.W_700, color="#FFFFFF"),
                    ],
                ),
                height=56, alignment=ft.Alignment.CENTER,
                border_radius=t.R_PILL,
                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                shadow=ft.BoxShadow(blur_radius=28, color="#807C5CFF", offset=ft.Offset(0, 8)),
                on_click=export_clicked, ink=True,
            ),
        ],
    )


def _set(state: ProjectState, field: str, value, cb) -> None:
    setattr(state, field, value)
    cb()
