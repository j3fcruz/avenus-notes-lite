"""
core/storage.py
Plaintext persistence layer for Sticky Notes.

Responsibilities:
    - Load notes from JSON file
    - Save notes to JSON file (atomic write for crash safety)
    - No encryption, no crypto dependencies

Atomic write strategy:
    Write to a .tmp file → fsync → rename. This prevents data loss
    if the process is killed mid-write, which is the only risk we
    guard against without an encryption layer.
"""

from __future__ import annotations

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any

from config.settings import DATA_FILE

_log = logging.getLogger("stickynotes.storage")


# ============================================================
# PUBLIC API
# ============================================================

def load_notes() -> list[dict[str, Any]]:
    """
    Load notes from DATA_FILE.

    Returns an empty list if the file does not exist or is malformed.
    Never raises — caller always gets a usable (possibly empty) list.
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as fh:
            data = json.load(fh)

        if not isinstance(data, list):
            _log.warning("notes.json root is not a list — resetting to empty")
            return []

        return [entry for entry in data if isinstance(entry, dict)]

    except json.JSONDecodeError as exc:
        _log.error("notes.json is malformed: %s", exc)
        return []
    except OSError as exc:
        _log.error("Could not read notes.json: %s", exc)
        return []


def save_notes(notes_data: list[dict[str, Any]]) -> bool:
    """
    Persist notes_data to DATA_FILE using an atomic write.

    Returns True on success, False on failure (error is logged).
    """
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    try:
        payload = json.dumps(notes_data, indent=2, ensure_ascii=False)
        _atomic_write_text(DATA_FILE, payload)
        return True

    except OSError as exc:
        _log.error("Failed to save notes: %s", exc)
        return False


# ============================================================
# INTERNAL HELPERS
# ============================================================

def _atomic_write_text(path: str, content: str) -> None:
    """
    Write *content* to *path* atomically via tmp-file + rename.

    Guarantees: if the process is killed during write, the original
    file (if any) remains intact and uncorrupted.
    """
    dir_path = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_path, suffix=".tmp")

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
            fh.flush()
            os.fsync(fh.fileno())

        os.replace(tmp_path, path)  # atomic on POSIX; near-atomic on Windows

    except Exception:
        # Clean up the temp file if rename failed
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise
