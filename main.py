"""
main.py
Sticky Notes — application entry point.

Boot sequence:
    1. Qt application init
    2. Storage init (ensure data directory exists)
    3. Launch NoteManager (loads notes, shows tray)
    4. Show an empty note on first run
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from config.settings import ICON_DIR, init_data_directory
from core.note_manager import NoteManager

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
_log = logging.getLogger("stickynotes.main")


def _set_app_icon(app: QApplication) -> None:
    icon_path = ICON_DIR / "sticky_icon.png"
    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    init_data_directory()
    _set_app_icon(app)

    manager = NoteManager()

    # First launch — show an empty note immediately
    if not manager.notes:
        manager.new_note()

    app.aboutToQuit.connect(manager.save_notes)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
