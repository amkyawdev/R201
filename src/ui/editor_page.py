"""TAB 2 — Editor.

Video preview with subtitle + logo overlays that can be dragged by hand,
safe-area guides that appear while dragging, and a bottom sheet for type
settings. Overlay positions are stored normalised (0..1) on ProjectState so
they survive an orientation switch.

Edits update the affected controls in place rather than rebuilding the
screen, so the text field keeps focus while typing.
"""

from __future__ import annotations

import flet as ft

from models.project_state import ProjectState
from ui import theme as t
from ui.components.widgets import glass_card, pill_chip

PALETTE = ["#FFFFFF", t.GOLD, t.CYAN, t.VIOLET, "#FF6B6B"]
FONTS = [("Padauk", "Padauk"), ("Noto Sans Myanmar", "Noto Sans MM"), ("Inter", "Inter")]

PREVIEW_H = 320
PREVIEW_W = 300  # nominal preview width; a phone gutter minus page margins


def build(page: ft.Page, state: ProjectState, on_change) -> ft.Control:
    guides = ft.Container(
        left=t.S4, right=t.S4, top=t.S4, bottom=t.S4,
        border=ft.Border.all(1, "#33FFFFFF"),
        border_radius=t.R12,
        opacity=0.0,
        animate_opacity=ft.Animation(t.D_SKELETON, ft.AnimationCurve.EASE_OUT),
    )

    subtitle_gesture, subtitle_box, subtitle_text = _draggable(
        state.subtitle, PREVIEW_H, "subtitle", on_change, guides
    )
    logo_gesture, logo_box, _logo_text = _draggable(
        state.logo, PREVIEW_H, "logo", on_change, guides
    )

    preview = ft.Container(
        height=PREVIEW_H,
        border_radius=t.R20,
        clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        gradient=ft.LinearGradient(colors=["#141B26", "#090D13"]),
        content=ft.Stack(
            controls=[
                ft.Container(
                    alignment=ft.Alignment.CENTER,
                    content=ft.Icon(ft.Icons.MOVIE_ROUNDED, size=64, color=t.TEXT_FAINT),
                ),
                guides,
                logo_gesture,
                subtitle_gesture,
            ],
        ),
    )

    # ---- controls that update in place -------------------------------------
    size_label = ft.Text(str(state.subtitle.size), size=t.TYPE_CAPTION, color=t.CYAN)

    def on_text(e) -> None:
        state.subtitle.text = e.control.value
        subtitle_text.value = e.control.value or "စာတန်းထိုး"
        subtitle_text.update()

    def on_size(e) -> None:
        state.subtitle.size = int(float(e.control.value))
        size_label.value = str(state.subtitle.size)
        subtitle_text.size = state.subtitle.size
        size_label.update()
        subtitle_text.update()

    text_field = ft.TextField(
        value=state.subtitle.text,
        hint_text="မြန်မာ စာတန်းထိုး ရိုက်ထည့်ပါ",
        multiline=True, min_lines=2, max_lines=3,
        bgcolor=t.SURFACE_2, border_color=t.BORDER,
        border_radius=t.R12, color=t.TEXT, text_size=t.TYPE_BODY,
        on_change=on_text,
    )

    swatches: list[ft.Control] = []

    def on_colour(colour: str) -> None:
        state.subtitle.colour = colour
        subtitle_text.color = colour
        for sw in swatches:
            sw.border = ft.Border.all(2, t.CYAN if sw.bgcolor == colour else t.BORDER)
        subtitle_text.update()
        for sw in swatches:
            sw.update()

    for c in PALETTE:
        swatches.append(
            ft.Container(
                width=32, height=32, border_radius=16, bgcolor=c,
                border=ft.Border.all(2, t.CYAN if c == state.subtitle.colour else t.BORDER),
                on_click=lambda e, col=c: on_colour(col),
                ink=True,
            )
        )

    font_buttons: list[ft.Control] = []

    def on_font(family: str) -> None:
        state.subtitle.font = family
        subtitle_text.font_family = family
        for fb in font_buttons:
            active = fb.data == family
            fb.gradient = ft.LinearGradient(colors=t.GRAD_PRIMARY) if active else None
            fb.bgcolor = None if active else t.GLASS
            fb.content.color = "#FFFFFF" if active else t.TEXT_MUTED
        subtitle_text.update()
        for fb in font_buttons:
            fb.update()

    for family, label in FONTS:
        active = family == state.subtitle.font
        font_buttons.append(
            ft.Container(
                data=family,
                content=ft.Text(label, size=t.TYPE_CAPTION,
                                color="#FFFFFF" if active else t.TEXT_MUTED),
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=t.R_PILL,
                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY) if active else None,
                bgcolor=None if active else t.GLASS,
                border=ft.Border.all(1, t.BORDER),
                on_click=lambda e, fam=family: on_font(fam),
                ink=True,
            )
        )

    def reset_positions(_e) -> None:
        state.subtitle.x, state.subtitle.y = 0.5, 0.82
        state.logo.x, state.logo.y = 0.14, 0.12
        _place(subtitle_box, state.subtitle, PREVIEW_H)
        _place(logo_box, state.logo, PREVIEW_H)
        subtitle_box.update()
        logo_box.update()

    def toggle_orientation(_e) -> None:
        state.orientation = "9:16" if state.orientation == "16:9" else "16:9"
        orient_chip.content.value = state.orientation
        orient_chip.update()

    orient_chip = pill_chip(state.orientation)

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
                        orient_chip,
                    ],
                ),
                text_field,
                ft.Column(
                    spacing=t.S1, tight=True,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Text("အရွယ်အစား", size=t.TYPE_CAPTION,
                                        color=t.TEXT_MUTED),
                                size_label,
                            ],
                        ),
                        ft.Slider(
                            value=state.subtitle.size, min=14, max=72, divisions=58,
                            active_color=t.VIOLET, inactive_color=t.SURFACE_2,
                            thumb_color=t.TEXT, on_change=on_size,
                        ),
                    ],
                ),
                ft.Row(spacing=t.S2, controls=swatches),
                ft.Row(spacing=t.S2, wrap=True, controls=font_buttons),
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
                            on_click=reset_positions, ink=True,
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
        spacing=t.S4,
        controls=[
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Text("တည်းဖြတ်", size=t.TYPE_DISPLAY,
                            weight=ft.FontWeight.W_700, color=t.TEXT),
                    ft.Container(
                        content=pill_chip("9:16 ⇄ 16:9"),
                        on_click=toggle_orientation,
                    ),
                ],
            ),
            preview,
            sheet,
        ],
    )


def _draggable(model, preview_h: int, kind: str, on_change, guides):
    """An overlay that follows the finger.

    Position is absolute inside the preview Stack. Each pan delta is
    converted to normalised coordinates on the model, so the layout survives
    an orientation switch. A magnetic 8px snap pulls the box onto the
    centre line and the safe-area margins.

    Returns `(gesture_detector, box, text)` so callers can mutate the label
    in place without walking the control tree.
    """
    text = ft.Text(
        model.text or ("LOGO" if kind == "logo" else "စာတန်းထိုး"),
        size=model.size,
        color=model.colour,
        font_family=model.font,
    )
    inner = ft.Container(
        content=text,
        padding=t.S2,
        border=ft.Border.all(1, t.CYAN if kind == "subtitle" else t.GOLD),
        border_radius=t.R8,
        bgcolor="#33000000",
    )
    box = ft.Container(content=inner)
    _place(box, model, preview_h)

    def on_pan_start(_e: ft.DragStartEvent) -> None:
        guides.opacity = 1.0
        guides.update()

    def on_pan_update(e: ft.DragUpdateEvent) -> None:
        # Flet 1.1 replaced the old `delta_x`/`delta_y` pair with an Offset.
        delta = e.local_delta or e.global_delta
        dx, dy = (delta.x, delta.y) if delta else (0.0, 0.0)
        left = max(0.0, (box.left or 0.0) + dx)
        top = max(0.0, min(preview_h - 40, (box.top or 0.0) + dy))
        box.left, box.top = left, top
        box.update()

    def on_pan_end(_e: ft.DragEndEvent) -> None:
        # Magnetic snap: centre line and the 8px safe-area margins.
        left = box.left or 0.0
        for target in (PREVIEW_W / 2 - 20, 8, PREVIEW_W - 80):
            if abs(left - target) < 8:
                left = target
                break
        box.left = max(0.0, left)
        model.x = box.left / PREVIEW_W
        model.y = (box.top or 0.0) / preview_h
        box.update()
        guides.opacity = 0.0
        guides.update()
        on_change()

    gesture = ft.GestureDetector(
        content=box,
        on_pan_start=on_pan_start,
        on_pan_update=on_pan_update,
        on_pan_end=on_pan_end,
        drag_interval=16,
        mouse_cursor=ft.MouseCursor.MOVE,
    )
    return gesture, box, text


def _place(box: ft.Container, model, preview_h: int) -> None:
    """Position an overlay from its normalised coordinates."""
    box.left = max(0.0, model.x * PREVIEW_W)
    box.top = max(0.0, model.y * preview_h)
