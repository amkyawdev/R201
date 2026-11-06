"""Reusable Flet widgets for the neo-cinematic glassmorphism system.

Each factory returns a ready-to-place control wired to the tokens in
`ui.theme`. Motion is expressed with Flet's `AnimatedSwitcher` /
`animate_*` properties; the signature curves live in theme.EASE_*.
"""

from __future__ import annotations

import math
import random

import flet as ft

from ui import theme as t


# Flet exposes only named curves; EASE_OUT_QUINT is the closest match to
# the signature cubic-bezier(0.22, 1, 0.36, 1).
EASE = ft.AnimationCurve.EASE_OUT_QUINT


def glass_card(
    content: ft.Control,
    *,
    radius: int = t.R16,
    padding: int = t.S4,
    blur: int = 18,
    border_colour: str = t.BORDER,
    gradient: list[str] | None = None,
) -> ft.Container:
    """A frosted-glass card: translucent fill, hairline border, soft shadow."""
    return ft.Container(
        content=content,
        padding=padding,
        border_radius=radius,
        bgcolor=None if gradient else t.GLASS,
        gradient=(
            ft.LinearGradient(colors=gradient) if gradient else None
        ),
        border=ft.Border.all(1, border_colour),
        blur=ft.Blur(blur, blur) if blur else None,
        shadow=ft.BoxShadow(
            blur_radius=32, spread_radius=0,
            color="#66000000", offset=ft.Offset(0, 8),
        ),
        animate=ft.Animation(t.D_TAB, EASE),
    )


def gradient_button(
    label: str,
    on_click,
    *,
    icon: str | None = None,
    width: int | None = None,
    height: int = 52,
    glow: str = t.GLOW_VIOLET,
) -> ft.Container:
    """Primary action: violet→cyan gradient pill with a soft glow."""
    inner = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=t.S2,
        controls=[
            ft.Icon(icon, color="#FFFFFF", size=18) if icon else ft.Container(),
            ft.Text(label, size=t.TYPE_BODY, weight=ft.FontWeight.W_600, color="#FFFFFF"),
        ],
    )
    return ft.Container(
        content=inner,
        width=width,
        height=height,
        alignment=ft.Alignment.CENTER,
        border_radius=t.R_PILL,
        gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
        shadow=ft.BoxShadow(blur_radius=24, color="#737C5CFF", offset=ft.Offset(0, 6)),
        on_click=on_click,
        ink=True,
        animate_scale=ft.Animation(t.D_FAST, ft.AnimationCurve.EASE_OUT),
    )


def ghost_button(label: str, on_click, *, height: int = 52) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, size=t.TYPE_BODY, weight=ft.FontWeight.W_500, color=t.TEXT),
        height=height,
        alignment=ft.Alignment.CENTER,
        border_radius=t.R_PILL,
        border=ft.Border.all(1, t.BORDER_STRONG),
        on_click=on_click,
        ink=True,
    )


def pill_chip(label: str, *, dot: bool = False, active: bool = False) -> ft.Container:
    controls: list[ft.Control] = []
    if dot:
        controls.append(
            ft.Container(
                width=6, height=6, border_radius=3, bgcolor=t.CYAN,
                animate_opacity=ft.Animation(t.D_BREATHE, ft.AnimationCurve.EASE_IN_OUT),
            )
        )
    controls.append(ft.Text(label, size=t.TYPE_CAPTION, color=t.TEXT_MUTED))
    return ft.Container(
        content=ft.Row(controls, spacing=6, tight=True),
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=t.R_PILL,
        bgcolor=t.GLASS if not active else None,
        gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY) if active else None,
        border=ft.Border.all(1, t.BORDER),
    )


class AIOrb(ft.Stack):
    """The breathing idle orb with optional thinking ripples.

    Idle: scale 1.0→1.04 over 3s ease-in-out, opacity 0.85→1.0.
    Thinking: three staggered concentric rings expand and fade.

    The pulse is driven by `start(page)`, an async loop that flips the core
    every half-period; Flet animates the transition between the two states.
    """

    def __init__(self, size: int = 120) -> None:
        self._size = size
        self._thinking = False
        self._task = None
        self._rings = [
            ft.Container(
                width=size, height=size, border_radius=size / 2,
                border=ft.Border.all(1.5, t.VIOLET),
                opacity=0.0,
                scale=ft.Scale(1.0),
                animate_opacity=ft.Animation(2000, ft.AnimationCurve.EASE_OUT),
                animate_scale=ft.Animation(2000, ft.AnimationCurve.EASE_OUT),
            )
            for _ in range(3)
        ]
        self._core = ft.Container(
            width=size, height=size, border_radius=size / 2,
            gradient=ft.RadialGradient(colors=[t.VIOLET, t.SURFACE]),
            shadow=ft.BoxShadow(blur_radius=40, color="#807C5CFF"),
            scale=ft.Scale(1.0),
            opacity=0.9,
            animate_scale=ft.Animation(t.D_BREATHE, ft.AnimationCurve.EASE_IN_OUT),
            animate_opacity=ft.Animation(t.D_BREATHE, ft.AnimationCurve.EASE_IN_OUT),
        )
        super().__init__(
            width=size * 2, height=size * 2,
            controls=[*self._rings, ft.Container(content=self._core, alignment=ft.Alignment.CENTER)],
            alignment=ft.Alignment.CENTER,
        )

    def start(self, page: ft.Page) -> None:
        """Kick off the breathing loop (idempotent)."""
        if self._task is None:
            self._task = page.run_task(self._breathe_loop)

    async def _breathe_loop(self) -> None:
        import asyncio

        expanded = False
        while True:
            await asyncio.sleep(t.D_BREATHE / 2000)
            if self._thinking:
                continue
            expanded = not expanded
            try:
                self._core.scale = ft.Scale(1.04 if expanded else 1.0)
                self._core.opacity = 1.0 if expanded else 0.88
                self._core.update()
            except Exception:
                return  # control detached (tab switched away)

    def set_thinking(self, on: bool) -> None:
        self._thinking = on
        if on:
            self._core.scale = ft.Scale(1.06)
            self._core.opacity = 1.0
            self._core.shadow = ft.BoxShadow(blur_radius=56, color="#B07C5CFF")
        else:
            self._core.shadow = ft.BoxShadow(blur_radius=40, color="#807C5CFF")

        for ring in self._rings:
            if on:
                ring.opacity = 0.35
                ring.scale = ft.Scale(1.7)
            else:
                ring.opacity = 0.0
                ring.scale = ft.Scale(1.0)

        # The orb may not be mounted yet; update() raises in that case.
        try:
            self._core.update()
            for ring in self._rings:
                ring.update()
        except Exception:
            pass


def waveform(seed: int = 0, bars: int = 22, height: int = 28) -> ft.Row:
    """Static bar waveform; the Voices tab animates it on tap-preview."""
    rng = random.Random(seed)
    return ft.Row(
        spacing=3,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Container(
                width=3,
                height=max(4, height * (0.25 + 0.75 * abs(math.sin(i / 2 + seed))) * (0.7 + 0.3 * rng.random())),
                border_radius=2,
                bgcolor=t.CYAN if i % 2 else t.VIOLET,
            )
            for i in range(bars)
        ],
    )


def shimmer_line(width: int, *, height: int = 14) -> ft.Container:
    """A skeleton line used while the transcript streams in."""
    return ft.Container(
        width=width, height=height, border_radius=6,
        gradient=ft.LinearGradient(
            colors=[t.SURFACE, t.SURFACE_2, t.SURFACE],
            begin=ft.Alignment.CENTER_LEFT, end=ft.Alignment.CENTER_RIGHT,
        ),
        animate_opacity=ft.Animation(t.D_SKELETON, ft.AnimationCurve.EASE_OUT),
    )


def segmented(options: list[str], selected: int, on_change) -> ft.Container:
    """Glass segmented control used for resolution / format pickers."""
    def _seg(i: int, label: str) -> ft.Container:
        active = i == selected
        return ft.Container(
            content=ft.Text(
                label, size=t.TYPE_CAPTION,
                color="#FFFFFF" if active else t.TEXT_MUTED,
                weight=ft.FontWeight.W_600 if active else ft.FontWeight.W_400,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=10),
            border_radius=t.R_PILL,
            gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY) if active else None,
            on_click=lambda e, idx=i: on_change(idx),
            ink=True,
        )

    return ft.Container(
        content=ft.Row([_seg(i, o) for i, o in enumerate(options)], spacing=4, tight=True),
        padding=4,
        border_radius=t.R_PILL,
        bgcolor=t.GLASS,
        border=ft.Border.all(1, t.BORDER),
    )


def bottom_nav(
    items: list[tuple[str, str, str]], selected: int, on_select
) -> ft.Container:
    """Floating frosted pill nav.

    Each item is `(outline_icon, filled_icon, label)`. The active item rises
    4px, swaps outline→filled and sits on a gradient pill; the inactive ones
    stay at 60% opacity. Matches the motion spec's 300ms easeOutQuint.
    """
    tabs: list[ft.Control] = []
    for i, (icon_out, icon_fill, label) in enumerate(items):
        active = i == selected
        tabs.append(
            ft.Container(
                content=ft.Column(
                    spacing=2,
                    tight=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(
                            icon_fill if active else icon_out,
                            size=22,
                            color=t.TEXT if active else t.TEXT_MUTED,
                        ),
                        ft.Text(
                            label,
                            size=9,
                            color=t.TEXT if active else t.TEXT_MUTED,
                            opacity=0.85,
                        ),
                    ],
                ),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                border_radius=t.R_PILL,
                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY) if active else None,
                opacity=1.0 if active else 0.6,
                on_click=lambda e, idx=i: on_select(idx),
                ink=True,
                animate=ft.Animation(t.D_TAB, EASE),
                animate_opacity=ft.Animation(t.D_TAB, EASE),
                offset=ft.Offset(0, -0.04) if active else ft.Offset(0, 0),
                shadow=(
                    ft.BoxShadow(blur_radius=24, color="#737C5CFF", offset=ft.Offset(0, 4))
                    if active
                    else None
                ),
            )
        )
    return ft.Container(
        content=ft.Row(tabs, alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        height=72,
        margin=ft.Margin.symmetric(horizontal=t.PAGE_X),
        border_radius=t.R28,
        bgcolor="#CC0B0F14",
        blur=ft.Blur(24, 24),
        border=ft.Border.all(1, t.BORDER),
        shadow=ft.BoxShadow(blur_radius=32, color="#66000000", offset=ft.Offset(0, 8)),
    )


def thinking_dialog(page: ft.Page) -> ft.AlertDialog:
    """The Myanmar duration-guard error dialog.

    Shown with `page.show_dialog(...)` and dismissed with `page.pop_dialog()`
    — Flet 1.1 removed the old `page.open`/`page.close` pair.
    """
    def dismiss(_e) -> None:
        page.pop_dialog()

    return ft.AlertDialog(
        modal=True,
        bgcolor=t.SURFACE,
        shape=ft.RoundedRectangleBorder(radius=t.R24),
        content=ft.Container(
            width=320,
            content=ft.Column(
                spacing=t.S4,
                tight=True,
                controls=[
                    ft.Container(
                        height=3, width=48, border_radius=2,
                        gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                    ),
                    ft.Row(
                        spacing=t.S3,
                        controls=[
                            ft.Icon(ft.Icons.HOURGLASS_TOP_ROUNDED, color=t.GOLD, size=22),
                            ft.Text(
                                "ဗီဒီယို ကြာချိန် ရှည်လွန်းနေပါသည်",
                                size=t.TYPE_TITLE, weight=ft.FontWeight.W_700, color=t.TEXT,
                            ),
                        ],
                    ),
                    ft.Text(
                        "တင်သွင်းထားသော ဗီဒီယိုသည် ၃ မိနစ်ထက် ကျော်လွန်နေပါသည်။ "
                        "ကျေးဇူးပြု၍ ၃ မိနစ်အတွင်း ဗီဒီယိုကို ဖြတ်တောက်ပြီးမှ ထပ်မံကြိုးစားပါ။",
                        size=t.TYPE_BODY, color=t.TEXT_MUTED,
                    ),
                    ft.Row(
                        spacing=t.S3,
                        controls=[
                            ft.Container(
                                content=ft.Text("အိုကေ", color="#FFFFFF", weight=ft.FontWeight.W_600),
                                expand=True, height=48, alignment=ft.Alignment.CENTER,
                                border_radius=t.R_PILL,
                                gradient=ft.LinearGradient(colors=t.GRAD_PRIMARY),
                                on_click=dismiss,
                                ink=True,
                            ),
                            ft.Container(
                                content=ft.Text("ပြန်လည်ရွေးချယ်", color=t.TEXT),
                                expand=True, height=48, alignment=ft.Alignment.CENTER,
                                border_radius=t.R_PILL,
                                border=ft.Border.all(1, t.BORDER_STRONG),
                                on_click=dismiss,
                                ink=True,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
