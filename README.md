# Movie Recap Myanmar

Turn a full-length movie into a **3-minute Myanmar-language recap video** —
AssemblyAI transcription, AI voiceover in five Burmese voices, draggable
subtitle/logo overlays, and an ffmpeg render, all wrapped in a Flet app.

```
movie-recap-myanmar/
├── .github/workflows/app-build.yml   # GitHub Actions APK build
├── assets/
│   ├── logo_placeholder.png
│   ├── fonts/Padauk-Regular.ttf      # Burmese font (swappable)
│   └── voices/                       # 5 voice previews (edge-tts, cloud-rendered)
├── design/                           # interactive design board (HTML/CSS/JS)
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   └── proto.js
├── src/
│   ├── main.py                       # Flet entry + BottomNavigationBar
│   ├── ui/
│   │   ├── theme.py                  # design tokens (single source of truth)
│   │   ├── recap_page.py             # import + recents + thinking orb
│   │   ├── editor_page.py            # draggable overlays, type sheet
│   │   ├── voices_page.py            # 5 Myanmar voices
│   │   ├── export_page.py            # resolution / format / progress
│   │   ├── settings_page.py          # keys, ffmpeg status, speech rate
│   │   └── components/widgets.py     # glass card, gradient button, orb, nav
│   ├── core/
│   │   ├── assembly_client.py        # AssemblyAI wrapper
│   │   ├── tts_client.py             # edge-tts, 5 Myanmar voices
│   │   ├── video_processor.py        # ffmpeg render (subprocess)
│   │   └── duration_guard.py         # the 3-minute rule
│   └── models/project_state.py       # transcript, voice, overlay geometry
├── pyproject.toml
├── buildozer.spec                    # optional Kivy backup
└── README.md
```

## Run the app

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt        # or: pip install "flet[all]" requests edge-tts
flet run src/main.py                   # desktop
flet run --web --port 8550 src/main.py # browser
```

Set `ASSEMBLYAI_API_KEY` in the environment before transcribing. The key is
read at runtime and never written to disk.

## Design board

`design/index.html` is a standalone, dependency-free board containing the four
screens, the error dialog, the thinking/skeleton state, the motion spec, the
component library and the full token set. It has two views — **Design board**
and **Live prototype** (an interactive phone). Open it directly, or serve it:

```bash
cd design && python -m http.server 12001
```

The board's tokens are mirrored 1:1 in `src/ui/theme.py`.

## Build the APK

```bash
flet build apk --project "Movie Recap Myanmar"
```

CI does the same on every push to `main` via
`.github/workflows/app-build.yml` and uploads the artifact.

## The 3-minute rule

`core/duration_guard.py` is the gate. Anything longer than 180 s is refused
with the Myanmar dialog *"ဗီဒီယို ကြာချိန် ရှည်လွန်းနေပါသည်"*; clips within
30 s of the limit get a soft nudge. `video_processor.render` also hard-trims to
180 s as a second line of defence.

## Motion

Seven signature animations are specified in `design/index.html` §02 and
implemented in CSS (`design/styles.css`) and Flet (`src/ui/components/widgets.py`).
The signature curve is `cubic-bezier(0.22, 1, 0.36, 1)` — easeOutQuint.

## Licence

Apache-2.0. See [LICENSE](LICENSE).
