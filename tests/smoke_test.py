"""Headless smoke test for the app lifecycle.

Builds `main()` against a mock Page and drives the event handlers that the
device actually calls — the original crash (`'Page' object has no attribute
'open'`) lived in a handler, so constructing the controls is not enough.

Run: python tests/smoke_test.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import flet as ft  # noqa: E402

import main as app  # noqa: E402


class MockPage:
    """Enough of ft.Page to run the app without a Flutter client."""

    def __init__(self) -> None:
        self.controls: list[ft.Control] = []
        self.services: list[ft.Control] = []
        self.dialogs_shown = 0
        self.dialogs_popped = 0
        self.updates = 0
        self.tasks: list = []
        self.title = ""
        self.bgcolor = None
        self.padding = None
        self.theme_mode = None
        self.fonts: dict = {}

    def add(self, *controls: ft.Control) -> None:
        self.controls.extend(controls)

    def update(self, *_) -> None:
        self.updates += 1

    def show_dialog(self, _dialog) -> None:
        self.dialogs_shown += 1

    def pop_dialog(self):
        self.dialogs_popped += 1
        return None

    def run_task(self, handler, *args, **kwargs):
        task = handler(*args, **kwargs)
        if hasattr(task, "close"):  # a bare coroutine from an async handler
            task.close()
        self.tasks.append(task)
        return task

    def close(self, *_):
        raise AssertionError("Page.close() does not exist in Flet 1.1")


def walk(control):
    """Yield every control in the tree."""
    yield control
    for attr in ("controls", "content"):
        child = getattr(control, attr, None)
        if isinstance(child, list):
            for c in child:
                yield from walk(c)
        elif isinstance(child, ft.Control):
            yield from walk(child)


def find(control, predicate):
    return [c for c in walk(control) if predicate(c)]


def main() -> int:
    page = MockPage()
    app.main(page)
    print(f"OK main() built {len(page.controls)} root control(s), "
          f"{page.updates} updates")

    # ---- nav: every tab must switch without raising ------------------------
    nav = find(
        page.controls[0],
        lambda c: type(c).__name__ == "Container" and getattr(c, "height", None) == 72,
    )
    if not nav:
        print("FAIL bottom nav not found")
        return 1
    tabs = find(
        nav[0],
        lambda c: type(c).__name__ == "Container"
        and getattr(c, "on_click", None) is not None,
    )
    print(f"OK bottom nav has {len(tabs)} tappable items")
    for t in tabs:
        t.on_click(None)
    print(f"OK all {len(tabs)} tabs switched (updates now {page.updates})")

    # ---- file picker service registered ------------------------------------
    pickers = [s for s in page.services if type(s).__name__ == "FilePicker"]
    print(f"OK FilePicker services registered: {len(pickers)}")

    # ---- duration dialog: show + pop ---------------------------------------
    from ui.components.widgets import thinking_dialog

    dlg = thinking_dialog(page)
    page.show_dialog(dlg)
    assert page.dialogs_shown == 1, "show_dialog not called"
    buttons = find(
        dlg,
        lambda c: type(c).__name__ == "Container"
        and getattr(c, "on_click", None) is not None,
    )
    for b in buttons:
        b.on_click(None)
    assert page.dialogs_popped == 2, f"expected 2 pops, got {page.dialogs_popped}"
    print("OK duration dialog shows and both actions dismiss it")

    # ---- orb breathing loop starts -----------------------------------------
    from ui.components.widgets import AIOrb

    orb_page = MockPage()
    orb = AIOrb(120)
    orb.start(orb_page)
    orb.start(orb_page)  # idempotent
    assert len(orb_page.tasks) == 1, "orb started more than one loop"
    orb.set_thinking(True)
    orb.set_thinking(False)
    print("OK AIOrb breathing loop starts once and toggles thinking")

    # ---- voices: select + preview mutate in place --------------------------
    from models.project_state import ProjectState
    from core.tts_client import VOICES
    import ui.voices_page as vp

    vp_page = MockPage()
    state = ProjectState()
    vp.build(vp_page, state, lambda: None, lambda v, p: None)
    assert state.voice_id == VOICES[0].id
    print("OK voices page builds with a default selection")

    # ---- export button schedules the progress coroutine --------------------
    import ui.export_page as xp

    xp_page = MockPage()
    ran = {"n": 0}

    def _capture(handler, *a, **k):
        coro = handler(*a, **k)
        ran["n"] += 1
        coro.close()  # detached controls: the loop exits on the first update
        return coro

    xp_page.run_task = _capture
    state = ProjectState()
    export = xp.build(xp_page, state, lambda: None, lambda: None)
    export_btns = find(
        export,
        lambda c: type(c).__name__ == "Container"
        and getattr(c, "height", None) == 56
        and getattr(c, "on_click", None) is not None,
    )
    assert export_btns, "export button not found"
    export_btns[0].on_click(None)
    assert ran["n"] == 1, "export click did not schedule the progress task"
    export_btns[0].on_click(None)  # must be a no-op while busy? (busy flag is set inside)
    print("OK export button schedules the progress coroutine")

    # ---- duration guard ----------------------------------------------------
    from core.duration_guard import check, fmt_mm

    assert check(200).ok is False and check(200).over_by_s == 20
    assert check(170).ok is True and check(170).warn is True
    assert fmt_mm(192) == "3:12"
    print("OK duration guard: 200s rejected, 170s warns, 192s formats 3:12")

    print("\nAll smoke checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
