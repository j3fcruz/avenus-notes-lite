"""
ui/tray.py
System tray icon and context menu for Sticky Notes.

Menu items:
    - New Note
    - Show All Notes
    - Hide All Notes
    - ─────────
    - Quit
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMenu, QSystemTrayIcon

from config.settings import ICON_DIR

if TYPE_CHECKING:
    from core.note_manager import NoteManager

_log = logging.getLogger("stickynotes.tray")


class TrayManager:
    """Manages the system tray icon and menu."""

    def __init__(self, manager: "NoteManager") -> None:
        self.manager = manager
        self._notes_hidden: bool = False  # explicit toggle state

        if not QSystemTrayIcon.isSystemTrayAvailable():
            _log.warning("System tray not available on this platform")
            return

        self._tray = QSystemTrayIcon()
        self._tray.setToolTip("Sticky Notes")
        self._set_icon()
        self._build_menu()

        self._tray.activated.connect(self._on_tray_activated)
        self._tray.show()

    # ----------------------------------------------------------
    # ICON
    # ----------------------------------------------------------

    def _set_icon(self) -> None:
        icon_path = ICON_DIR / "sticky_icon.png"
        if icon_path.exists():
            self._tray.setIcon(QIcon(str(icon_path)))
        else:
            from PySide6.QtWidgets import QApplication
            self._tray.setIcon(QApplication.instance().windowIcon())

    # ----------------------------------------------------------
    # MENU
    # ----------------------------------------------------------

    def _build_menu(self) -> None:
        menu = QMenu()

        act_new = menu.addAction("✚  New Note")
        act_new.triggered.connect(lambda _=False: self.manager.new_note())

        menu.addSeparator()

        act_show = menu.addAction("Show All Notes")
        act_show.triggered.connect(lambda _=False: self._do_show_all())

        act_hide = menu.addAction("Hide All Notes")
        act_hide.triggered.connect(lambda _=False: self._do_hide_all())

        menu.addSeparator()

        act_quit = menu.addAction("Quit")
        act_quit.triggered.connect(self._quit)

        self._tray.setContextMenu(menu)

    # ----------------------------------------------------------
    # SHOW / HIDE (explicit, state-tracked)
    # ----------------------------------------------------------

    def _do_show_all(self) -> None:
        self._notes_hidden = False
        self.manager.show_all()

    def _do_hide_all(self) -> None:
        self._notes_hidden = True
        self.manager.hide_all()

    # ----------------------------------------------------------
    # TRAY SINGLE-CLICK TOGGLE
    # ----------------------------------------------------------

    def _on_tray_activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason != QSystemTrayIcon.ActivationReason.Trigger:
            return
        if self._notes_hidden:
            self._do_show_all()
        else:
            self._do_hide_all()

    # ----------------------------------------------------------
    # HELPERS
    # ----------------------------------------------------------

    def show_message(self, title: str, body: str) -> None:
        if hasattr(self, "_tray"):
            self._tray.showMessage(
                title, body, QSystemTrayIcon.MessageIcon.Information, 2000
            )

    def _quit(self) -> None:
        self.manager.save_notes()
        from PySide6.QtWidgets import QApplication
        QApplication.instance().quit()

