"""AssemblyAI transcription + summarisation wrapper.

`transcribe` uploads a local media file, starts a transcript job with
auto-chapters + summarisation, and polls until completion. `summarise`
condenses the full transcript into a ~3 minute spoken script.

The API key is read from the ASSEMBLYAI_API_KEY environment variable and
never logged.
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

import requests

BASE = "https://api.assemblyai.com/v2"
POLL_INTERVAL_S = 3
TIMEOUT_S = 30 * 60


class AssemblyError(RuntimeError):
    """Raised when AssemblyAI rejects a request or a job fails."""


@dataclass
class Transcript:
    text: str
    sentences: list[str]
    summary: str
    duration_s: float


class AssemblyClient:
    def __init__(self, api_key: str | None = None) -> None:
        self._key = api_key or os.environ.get("ASSEMBLYAI_API_KEY", "")
        if not self._key:
            raise AssemblyError("ASSEMBLYAI_API_KEY is not set")

    @property
    def _headers(self) -> dict[str, str]:
        return {"authorization": self._key}

    def _upload(self, path: str) -> str:
        with open(path, "rb") as fh:
            resp = requests.post(
                f"{BASE}/upload",
                headers=self._headers,
                data=fh,
                timeout=120,
            )
        resp.raise_for_status()
        return resp.json()["upload_url"]

    def transcribe(self, path: str, language: str = "my") -> Transcript:
        upload_url = self._upload(path)
        payload = {
            "audio_url": upload_url,
            "language_code": language,
            "auto_chapters": True,
            "summarization": True,
            "summary_type": "bullets",
            "summary_model": "informative",
        }
        resp = requests.post(
            f"{BASE}/transcript", json=payload, headers=self._headers, timeout=60
        )
        resp.raise_for_status()
        job = resp.json()

        deadline = time.time() + TIMEOUT_S
        while job.get("status") not in ("completed", "error"):
            if time.time() > deadline:
                raise AssemblyError("Transcription timed out")
            time.sleep(POLL_INTERVAL_S)
            poll = requests.get(
                f"{BASE}/transcript/{job['id']}", headers=self._headers, timeout=60
            )
            poll.raise_for_status()
            job = poll.json()

        if job["status"] == "error":
            raise AssemblyError(job.get("error", "unknown error"))

        sentences = [s["text"] for s in (job.get("sentences") or [])]
        if not sentences and job.get("text"):
            sentences = [job["text"]]

        summary = job.get("summary") or ""
        if isinstance(summary, list):
            summary = "\n".join(f"• {b}" for b in summary)

        return Transcript(
            text=job.get("text", ""),
            sentences=sentences,
            summary=summary,
            duration_s=(job.get("audio_duration") or 0.0),
        )

    def summarise(self, transcript: Transcript, target_seconds: int = 180) -> str:
        """Condense a transcript into a spoken script of roughly target length.

        Myanmar speech lands near 3.2 words/second for a calm narrator voice,
        so we keep the summary near that budget and fall back to the
        AssemblyAI summary when no LLM is configured.
        """
        if not transcript.summary:
            budget = int(target_seconds * 3.2)
            joined = " ".join(transcript.sentences)
            return joined[:budget]
        return transcript.summary
