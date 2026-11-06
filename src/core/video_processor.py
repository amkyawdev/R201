"""ffmpeg wrapper: probe, trim to 3 minutes, burn overlays, mux narration.

Everything shells out to ffmpeg/ffprobe via subprocess. When the ffmpeg
binary is missing the caller is expected to fall back to a cloud renderer
(see `available`).
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass

from models.project_state import Overlay, ProjectState

FFMPEG = os.environ.get("FFMPEG_BIN", "ffmpeg")
FFPROBE = os.environ.get("FFPROBE_BIN", "ffprobe")

LIMIT_S = 180


def available() -> bool:
    return shutil.which(FFMPEG) is not None and shutil.which(FFPROBE) is not None


@dataclass
class ProbeResult:
    duration_s: float
    width: int
    height: int


def probe(path: str) -> ProbeResult:
    cmd = [
        FFPROBE, "-v", "error", "-print_format", "json",
        "-show_format", "-show_streams", path,
    ]
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    duration = float(data["format"]["duration"])
    video = next(
        (s for s in data["streams"] if s.get("codec_type") == "video"), None
    )
    return ProbeResult(
        duration_s=duration,
        width=int(video["width"]) if video else 0,
        height=int(video["height"]) if video else 0,
    )


def _drawtext(overlay: Overlay, font_file: str | None, label: str) -> str:
    """Build a drawtext filter for one overlay.

    `textfile` is used rather than `text` so Myanmar glyphs survive the
    filter-graph escaping rules.
    """
    font = font_file or ""
    x = f"w*{overlay.x:.4f}-tw/2"
    y = f"h*{overlay.y:.4f}-th/2"
    return (
        f"drawtext=textfile={label}:fontfile={font}:"
        f"fontsize={overlay.size}:fontcolor={overlay.colour}:"
        f"x={x}:y={y}:box=0"
    )


def render(
    state: ProjectState,
    narration_path: str,
    out_path: str,
    work_dir: str,
    font_file: str | None = None,
) -> str:
    """Compose the final recap video.

    Steps: trim the source to <=180s, scale to the chosen orientation,
    burn the subtitle and logo overlays, then mux the narration over the
    original audio ducked to 20%.
    """
    if not available():
        raise RuntimeError("ffmpeg/ffprobe not found on PATH")

    os.makedirs(work_dir, exist_ok=True)
    sub_file = os.path.join(work_dir, "subtitle.txt")
    logo_file = os.path.join(work_dir, "logo.txt")
    with open(sub_file, "w", encoding="utf-8") as fh:
        fh.write(state.subtitle.text)
    with open(logo_file, "w", encoding="utf-8") as fh:
        fh.write(state.logo.text)

    scale = (
        "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920"
        if state.orientation == "9:16"
        else "scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080"
    )

    filters = [
        f"trim=0:{LIMIT_S}",
        "setpts=PTS-STARTPTS",
        scale,
        _drawtext(state.subtitle, font_file, sub_file),
        _drawtext(state.logo, font_file, logo_file),
    ]

    cmd = [
        FFMPEG, "-y",
        "-i", state.source_path or "",
        "-i", narration_path,
        "-filter_complex",
        f"[0:v]{','.join(filters)}[v];"
        f"[0:a]volume=0.2[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=first[a]",
        "-map", "[v]", "-map", "[a]",
        "-c:v", "libx264", "-preset", "medium", "-crf", str(_crf(state.quality)),
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        out_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, check=True)
    return out_path


def _crf(quality: int) -> int:
    """Map a 0-100 quality slider to an x264 CRF (lower is better)."""
    quality = max(0, min(100, quality))
    return int(round(30 - (quality / 100) * 12))  # 30 (worst) .. 18 (best)
