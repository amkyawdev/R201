"""Movie Recap Myanmar — Flet app entry point.

Wires the four tabs behind a floating glass bottom nav and owns the
ProjectState for the session. Run with `flet run src/main.py`.
"""

from __future__ import annotations

import flet as ft

from models.project_state import ProjectState
from ui import editor_page, export_page, recap_page, voices_page
from ui import theme as t
from ui.components.widgets import bottom_nav, thinking_dialog

NAV = [
    (ft.Icons.MOVIE_CREATION_OUTLINED, "Recap"),
    (ft.Icons.EDIT_NOTE_OUTLINED, "Editor"),
    (ft.Icons.RECORD_VOICE_OVER_OUTLINED, "Voices"),
    (ft.Icons.IOS_SHARE_OUTLINED, "Export"),
]


def main(page: ft.Page) -> None:
    page.title = "Movie Recap Myanmar"
    page.bgcolor = t.BG
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {"Padauk": "/fonts/Padauk-Regular.ttf"}

    state = ProjectState()
    current = {"tab": 0}

    body = ft.Container(
        expand=True,
        padding=ft.Padding.only(left=t.PAGE_X, right=t.PAGE_X, top=t.S7, bottom=110),
    )
    nav_holder = ft.Container(
        content=bottom_nav(NAV, 0, lambda i: select(i)),
        padding=ft.Padding.only(bottom=t.S4),
    )

    def _screen(tab: int) -> ft.Control:
        if tab == 0:
            return recap_page.build(page, state, on_import=_import)
        if tab == 1:
            return editor_page.build(page, state, on_change=refresh)
        if tab == 2:
            return voices_page.build(page, state, on_select=refresh, on_preview=_preview)
        return export_page.build(page, state, on_export=_export, on_change=refresh)

    def refresh() -> None:
        body.content = _screen(current["tab"])
        page.update()

    def select(i: int) -> None:
        current["tab"] = i
        body.content = _screen(i)
        nav_holder.content = bottom_nav(NAV, i, select)
        page.update()

    def _import() -> None:
        # A real build opens a file picker here and probes the duration;
        # a clip over 3 minutes raises this duration-guard dialog.
        dlg = thinking_dialog(page)
        page._active_dialog = dlg  # type: ignore[attr-defined]
        page.open(dlg)

    def _preview(_voice, _playing: bool) -> None:
        refresh()

    def _export() -> None:
        # Kicks off tts_client.synthesise + video_processor.render.
        page.update()

    body.content = _screen(0)
    page.add(
        ft.Stack(
            expand=True,
            controls=[
                ft.Container(expand=True, content=body),
                ft.Container(content=nav_holder, bottom=0, left=0, right=0),
            ],
        )
    )
    page.update()


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
