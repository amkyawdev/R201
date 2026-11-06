"""TAB 1 — Recap (home).

Greeting, the breathing AI orb, the import pill, recent projects and the
floating "3 မိနစ်အတွင်း သာ" hint chip.
"""

from __future__ import annotations

import flet as ft

from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import AIOrb, glass_card, gradient_button, pill_chip


def build(page: ft.Page, state: ProjectState, on_import) -> ft.Control:
    orb = AIOrb(120)

    recents = [
        ("နွေဦးရာသီ", "02:58", "16:9"),
        ("တစ်ညအိပ်မက်", "01:42", "9:16"),
        ("မြစ်ကမ်းဘေး", "03:00", "16:9"),
    ]

    def card(title: str, dur: str, orient: str) -> ft.Container:
        thumb = ft.Container(
            height=96,
            border_radius=t.R16,
            gradient=ft.LinearGradient(
                colors=["#1B2433", "#0F1622"],
                begin=ft.Alignment.TOP_LEFT, end=ft.Alignment.BOTTOM_RIGHT,
            ),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.END,
                vertical_alignment=ft.CrossAxisAlignment.END,
                controls=[pill_chip(dur)],
            ),
            padding=t.S2,
        )
        return glass_card(
            ft.Column(
                spacing=t.S2, tight=True,
                controls=[
                    thumb,
                    ft.Text(title, size=t.TYPE_BODY, color=t.TEXT, weight=ft.FontWeight.W_600),
                    ft.Text(f"{orient} · ဒေသတွင်း", size=t.TYPE_CAPTION, color=t.TEXT_FAINT),
                ],
            ),
            radius=t.R16,
            padding=t.S3,
        )

    return ft.Column(
        expand=True,
        spacing=t.S6,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Column(
                        spacing=2, tight=True,
                        controls=[
                            ft.Text("မင်္ဂလာပါ", size=t.TYPE_DISPLAY, weight=ft.FontWeight.W_700, color=t.TEXT),
                            ft.Text("၃ မိနစ် ရုပ်ရှင် ပြန်လည်ခြုံငုံမှု ဖန်တီးပါ",
                                    size=t.TYPE_BODY, color=t.TEXT_MUTED),
                        ],
                    ),
                    ft.Container(
                        width=40, height=40, border_radius=20, bgcolor=t.GLASS,
                        border=ft.Border.all(1, t.BORDER),
                        content=ft.Icon(ft.Icons.PERSON_ROUNDED, color=t.TEXT_MUTED, size=20),
                    ),
                ],
            ),
            ft.Container(
                alignment=ft.Alignment.CENTER,
                padding=ft.Padding.symmetric(vertical=t.S5),
                content=ft.Column(
                    spacing=t.S5,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        orb,
                        gradient_button(
                            "Import Movie", lambda e: on_import(),
                            icon=ft.Icons.ADD_ROUNDED, width=210,
                        ),
                    ],
                ),
            ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("မကြာမီ ဖန်တီးခဲ့သည်", size=t.TYPE_TITLE,
                            weight=ft.FontWeight.W_600, color=t.TEXT),
                    ft.Text("အားလုံး", size=t.TYPE_CAPTION, color=t.CYAN),
                ],
            ),
            ft.Column(spacing=t.S3, controls=[card(*r) for r in recents]),
            ft.Row(controls=[pill_chip("3 မိနစ်အတွင်း သာ", dot=True)], alignment=ft.MainAxisAlignment.CENTER),
        ],
    )
