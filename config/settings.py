"""
config/settings.py
Centralized configuration for Sticky Notes.

All tunable constants live here. Import from this module only.
Side-effect-free on import — call init_data_directory() at startup.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# ============================================================
# APPLICATION METADATA
# ============================================================
APP_NAME:    str = "Sticky Notes"
APP_VERSION: str = "1.0.0"
APP_VENDOR:  str = "Open Source"

# ============================================================
# EXECUTION ENVIRONMENT
# ============================================================

def _get_base_dir() -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    if getattr(sys, "frozen", None) == "nuitka":
        return Path(sys.argv[0]).resolve().parent
    return Path(__file__).resolve().parent.parent


BASE_DIR: Path = _get_base_dir()
IS_FROZEN: bool = (
    hasattr(sys, "_MEIPASS") or getattr(sys, "frozen", None) == "nuitka"
)

# ============================================================
# DATA DIRECTORY
# ============================================================

if IS_FROZEN:
    _appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    DATA_FOLDER: str = os.path.join(_appdata, "StickyNotes", ".data")
else:
    DATA_FOLDER: str = os.path.join(os.getcwd(), ".data")

# ============================================================
# DATA FILE PATHS
# ============================================================

DATA_FILE: str = os.path.join(DATA_FOLDER, "notes.json")

# ============================================================
# UI DEFAULTS
# ============================================================

DEFAULT_NOTE_WIDTH:  int = 280
DEFAULT_NOTE_HEIGHT: int = 320
DEFAULT_NOTE_X:      int = 100
DEFAULT_NOTE_Y:      int = 100

# Note color palette (background hex colors)
NOTE_COLORS: list[str] = [
    "#fef08a",  # yellow  (default)
    "#bbf7d0",  # green
    "#bfdbfe",  # blue
    "#fecaca",  # red/pink
    "#e9d5ff",  # purple
    "#fed7aa",  # orange
    "#f1f5f9",  # white/grey
]

DEFAULT_NOTE_COLOR: str = NOTE_COLORS[0]

# ============================================================
# ASSET DIRECTORIES
# ============================================================

ASSETS_DIR: Path = BASE_DIR / "assets"
ICON_DIR:   Path = ASSETS_DIR / "icons"
THEME_DIR:  Path = ASSETS_DIR / "themes"

# ============================================================
# AUTOSAVE
# ============================================================

AUTOSAVE_DELAY_MS: int = 800  # debounce: save 800ms after last keystroke

# ============================================================
# LAZY INITIALISER
# ============================================================

def init_data_directory() -> None:
    """
    Create the .data directory. Idempotent (exist_ok=True).
    Call once at application startup, after QApplication is created.
    """
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Hide the .data folder on Windows
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.kernel32.SetFileAttributesW(DATA_FOLDER, 0x02)
        except (AttributeError, OSError):
            pass
