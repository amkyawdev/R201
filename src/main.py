"""Movie Recap Myanmar — Flet app entry point.

Owns the session ProjectState, the four tab screens and the floating glass
bottom nav. Tab switches cross-fade through an AnimatedSwitcher so the
content never pops, and every screen scrolls independently.

Run with `flet run src/main.py`.
"""

from __future__ import annotations

import asyncio

import flet as ft

from models.project_state import ProjectState
from ui import editor_page, export_page, recap_page, voices_page
from ui import theme as t
from ui.components.widgets import bottom_nav, thinking_dialog

NAV = [
    (ft.Icons.MOVIE_CREATION_OUTLINED, ft.Icons.MOVIE_CREATION, "Recap"),
    (ft.Icons.EDIT_NOTE_OUTLINED, ft.Icons.EDIT_NOTE, "Editor"),
    (ft.Icons.RECORD_VOICE_OVER_OUTLINED, ft.Icons.RECORD_VOICE_OVER, "Voices"),
    (ft.Icons.IOS_SHARE_OUTLINED, ft.Icons.IOS_SHARE, "Export"),
]


def main(page: ft.Page) -> None:
    page.title = "Movie Recap Myanmar"
    page.bgcolor = t.BG
    page.padding = 0
    page.theme_mode = ft.ThemeMode.DARK
    page.fonts = {"Padauk": "/fonts/Padauk-Regular.ttf"}

    state = ProjectState()
    current = {"tab": 0}

    picker = ft.FilePicker()
    page.services.append(picker)

    # The tab body cross-fades; each screen brings its own scroll view.
    body = ft.AnimatedSwitcher(
        content=ft.Container(),
        duration=t.D_TAB,
        switch_in_curve=ft.AnimationCurve.EASE_OUT_QUINT,
        switch_out_curve=ft.AnimationCurve.EASE_IN,
        expand=True,
    )

    def _screen(tab: int) -> ft.Control:
        if tab == 0:
            return recap_page.build(page, state, on_import=_import)
        if tab == 1:
            return editor_page.build(page, state, on_change=refresh)
        if tab == 2:
            return voices_page.build(page, state, on_select=refresh, on_preview=_preview)
        return export_page.build(page, state, on_export=_export, on_change=refresh)

    def _pane(tab: int) -> ft.Container:
        """Wrap a screen in the page gutter and a vertical scroll view."""
        return ft.Container(
            key=f"tab-{tab}",
            expand=True,
            padding=ft.Padding.only(
                left=t.PAGE_X, right=t.PAGE_X, top=t.S7, bottom=t.S8
            ),
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[_screen(tab)],
            ),
        )

    def refresh() -> None:
        body.content = _pane(current["tab"])
        page.update()

    def select(i: int) -> None:
        if i == current["tab"]:
            return
        current["tab"] = i
        body.content = _pane(i)
        nav_holder.content = bottom_nav(NAV, i, select)
        page.update()

    def _import() -> None:
        page.run_task(_pick_movie)

    async def _pick_movie() -> None:
        files = await picker.pick_files(
            dialog_title="ရုပ်ရှင် ရွေးချယ်ပါ",
            allowed_extensions=["mp4", "mkv", "mov", "avi", "webm"],
            allow_multiple=False,
        )
        if not files:
            return
        state.source_path = files[0].path
        state.name = files[0].name.rsplit(".", 1)[0]
        # Probing needs ffmpeg; a clip over 3 minutes raises the guard dialog.
        from core import duration_guard, video_processor

        duration = 0.0
        if state.source_path and video_processor.available():
            try:
                duration = video_processor.probe(state.source_path).duration_s
            except Exception:
                duration = 0.0
        state.duration_s = duration

        if duration and not duration_guard.check(duration).ok:
            page.show_dialog(thinking_dialog(page))
        else:
            refresh()

    def _preview(_voice, _playing: bool) -> None:
        refresh()

    def _export() -> None:
        page.run_task(_run_export)

    async def _run_export() -> None:
        # Kicks off tts_client.synthesise + video_processor.render.
        await asyncio.sleep(0)

    nav_holder = ft.Container(
        content=bottom_nav(NAV, 0, select),
        padding=ft.Padding.only(left=0, right=0, bottom=t.S4),
    )

    body.content = _pane(0)

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
    ft.run(main)
