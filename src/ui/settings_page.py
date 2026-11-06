"""Settings: API keys, default voice, ffmpeg status, about.

Keys are entered at runtime and held only in memory for the session; the
Telegram/AssemblyAI secrets are never written to disk.
"""

from __future__ import annotations

import flet as ft

from core import video_processor
from ui import theme as t
from ui.components.widgets import glass_card, pill_chip


def build(page: ft.Page, cfg: dict, on_change) -> ft.Control:
    def field(label: str, key: str, *, password: bool = False, hint: str = "") -> ft.Column:
        return ft.Column(
            spacing=t.S1, tight=True,
            controls=[
                ft.Text(label, size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                ft.TextField(
                    value=cfg.get(key, ""),
                    hint_text=hint, password=password,
                    can_reveal_password=password,
                    bgcolor=t.SURFACE_2, border_color=t.BORDER,
                    border_radius=t.R12, color=t.TEXT, text_size=t.TYPE_BODY,
                    on_change=lambda e: _set(cfg, key, e.control.value, on_change),
                ),
            ],
        )

    ffmpeg_ok = video_processor.available()

    return ft.Column(
        expand=True, spacing=t.S5,
        controls=[
            ft.Text("ဆက်တင်", size=t.TYPE_DISPLAY, weight=ft.FontWeight.W_700, color=t.TEXT),

            glass_card(
                ft.Column(
                    spacing=t.S4,
                    controls=[
                        ft.Text("API သော့များ", size=t.TYPE_TITLE,
                                weight=ft.FontWeight.W_600, color=t.TEXT),
                        field("AssemblyAI API Key", "assembly_key", password=True,
                              hint="xxxxxxxxxxxxxxxx"),
                        field("Cloud Render Endpoint", "cloud_endpoint",
                              hint="https://… (ffmpeg မရှိလျှင်)"),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            glass_card(
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=t.S1, tight=True,
                            controls=[
                                ft.Text("ffmpeg", size=t.TYPE_BODY,
                                        weight=ft.FontWeight.W_600, color=t.TEXT),
                                ft.Text("ဗီဒီယို ပေါင်းစပ်ရန် လိုအပ်သည်",
                                        size=t.TYPE_CAPTION, color=t.TEXT_MUTED),
                            ],
                        ),
                        pill_chip("ရရှိပြီး" if ffmpeg_ok else "မရှိပါ", dot=ffmpeg_ok, active=ffmpeg_ok),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            glass_card(
                ft.Column(
                    spacing=t.S3,
                    controls=[
                        ft.Text("အသံထွက် ပုံစံ", size=t.TYPE_TITLE,
                                weight=ft.FontWeight.W_600, color=t.TEXT),
                        ft.Slider(
                            value=cfg.get("speech_rate", 0), min=-30, max=30, divisions=30,
                            active_color=t.VIOLET, inactive_color=t.SURFACE_2,
                            thumb_color=t.TEXT,
                            on_change=lambda e: _set(cfg, "speech_rate", int(float(e.control.value)), on_change),
                        ),
                        ft.Text("နှုန်း %", size=t.TYPE_CAPTION, color=t.TEXT_FAINT),
                    ],
                ),
                radius=t.R20, padding=t.S4,
            ),

            ft.Container(
                content=ft.Text("အကြောင်း · Movie Recap Myanmar v1.0",
                                size=t.TYPE_CAPTION, color=t.TEXT_FAINT),
                alignment=ft.Alignment.CENTER,
            ),
        ],
    )


def _set(cfg: dict, key: str, value, cb) -> None:
    cfg[key] = value
    cb()
