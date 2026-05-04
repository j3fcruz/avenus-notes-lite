"""
core/note_manager.py
Central coordinator for sticky note lifecycle and tray integration.

Responsibilities:
    - Load / save notes (plaintext JSON)
    - Manage open StickyNote windows
    - Drive system tray icon and menu
    - Provide new_note / delete_note / save_notes API

No cryptographic logic. No idle watcher. No authentication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, List, Optional

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from config.settings import (
    AUTOSAVE_DELAY_MS,
    DEFAULT_NOTE_COLOR,
    DEFAULT_NOTE_HEIGHT,
    DEFAULT_NOTE_WIDTH,
    DEFAULT_NOTE_X,
    DEFAULT_NOTE_Y,
)
from core.storage import load_notes, save_notes

if TYPE_CHECKING:
    from ui.sticky_note import StickyNote

_log = logging.getLogger("stickynotes.note_manager")


class NoteManager:
    """
    Manages the collection of StickyNote windows and their persistence.

    Autosave is debounced: each edit schedules a save 800 ms later,
    and rapid keystrokes collapse into a single write.
    """

    def __init__(self) -> None:
        self.notes: List["StickyNote"] = []

        # Debounced autosave timer
        self._save_timer = QTimer()
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(AUTOSAVE_DELAY_MS)
        self._save_timer.timeout.connect(self.save_notes)

        # Tray — imported late to avoid circular imports
        from ui.tray import TrayManager
        self.tray = TrayManager(self)

        self._load_notes()

    # ----------------------------------------------------------
    # NOTE LIFECYCLE
    # ----------------------------------------------------------

    def new_note(
        self,
        text: str = "",
        geo: Optional[list[int]] = None,
        color: Optional[str] = None,
    ) -> "StickyNote":
        # Qt signals (e.g. QPushButton.clicked) pass a bool `checked` arg.
        # Guard so callers can connect directly: btn.clicked.connect(manager.new_note)
        if not isinstance(text, str):
            text = ""
        """Create and show a new StickyNote window."""
        from ui.sticky_note import StickyNote

        if geo is None:
            # Cascade each new note slightly offset from previous
            offset = len(self.notes) * 24
            geo = [
                DEFAULT_NOTE_X + offset,
                DEFAULT_NOTE_Y + offset,
                DEFAULT_NOTE_WIDTH,
                DEFAULT_NOTE_HEIGHT,
            ]

        note = StickyNote(
            manager=self,
            text=text,
            geo=geo,
            color=color or DEFAULT_NOTE_COLOR,
        )
        self.notes.append(note)
        note.show()
        self.schedule_save()
        return note

    def delete_note(self, note: "StickyNote") -> None:
        """Remove note from registry and close its window."""
        if note in self.notes:
            self.notes.remove(note)
        note.close()
        self.save_notes()

        # If last note closed, keep app alive via tray
        # (QuitOnLastWindowClosed is False in main.py)

    def show_all(self) -> None:
        """Restore and bring all notes to front.

        BUG FIX: showNormal() does NOT un-hide a widget hidden via hide().
        Must call show() first to make the window visible again, then clear
        any minimized state, then raise on the next event-loop tick so the
        WM has time to map the window before we try to raise it.
        """
        from PySide6.QtCore import Qt, QTimer
        for note in self.notes:
            # Step 1: Un-hide if hidden via hide()
            if not note.isVisible():
                note.show()
            # Step 2: Clear minimized state and restore normal geometry
            note.setWindowState(
                note.windowState() & ~Qt.WindowState.WindowMinimized
            )
            note.showNormal()
            # Step 3: Bring to front on the next event-loop tick
            QTimer.singleShot(0, note.raise_)
            QTimer.singleShot(0, note.activateWindow)

    def hide_all(self) -> None:
        """Hide all notes (remain in memory, restorable via show_all)."""
        for note in self.notes:
            note.hide()

    # ----------------------------------------------------------
    # PERSISTENCE
    # ----------------------------------------------------------

    def schedule_save(self) -> None:
        """Debounce: restart the autosave timer on each edit."""
        self._save_timer.start()

    def save_notes(self) -> None:
        """Serialize all open notes and write to disk immediately."""
        data = [note.to_dict() for note in self.notes]
        success = save_notes(data)
        if not success:
            _log.error("save_notes() failed — data may not be persisted")

    def _load_notes(self) -> None:
        """Read notes.json and open a StickyNote window for each entry."""
        entries = load_notes()
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            self.new_note(
                text=entry.get("text", ""),
                geo=entry.get("geo"),
                color=entry.get("color"),
            )
