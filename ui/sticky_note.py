"""
ui/sticky_note.py
Individual sticky note window.

Features:
    - Frameless, draggable window
    - Resizable via Qt resize handle
    - Inline text editor (auto-expanding)
    - Toolbar: [color picker] [pin/unpin] [new note] [delete]
    - Always-on-top toggle
    - Auto-save on edit (via NoteManager.schedule_save)
    - Dark text on colored background
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional

from PySide6.QtCore import (
    QPoint,
    QSize,
    Qt,
    QTimer,
)
from PySide6.QtGui import (
    QColor,
    QFont,
    QIcon,
    QPainter,
    QPalette,
    QTextOption,
)
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QSizeGrip,
    QVBoxLayout,
    QWidget,
)

from config.settings import ICON_DIR, NOTE_COLORS

if TYPE_CHECKING:
    from core.note_manager import NoteManager

_log = logging.getLogger("stickynotes.sticky_note")


# ============================================================
# COLOUR CYCLE BUTTON
# ============================================================

class _ColorDot(QPushButton):
    """Small circular button that cycles through note colors."""

    def __init__(self, current_color: str, parent: QWidget) -> None:
        super().__init__(parent)
        self._color = current_color
        self.setFixedSize(18, 18)
        self.setToolTip("Change color")
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._apply_style()

    def set_color(self, color: str) -> None:
        self._color = color
        self._apply_style()

    def _apply_style(self) -> None:
        self.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {self._color};
                border: 2px solid rgba(0,0,0,0.25);
                border-radius: 9px;
            }}
            QPushButton:hover {{
                border: 2px solid rgba(0,0,0,0.55);
            }}
            """
        )


# ============================================================
# STICKY NOTE WINDOW
# ============================================================

class StickyNote(QWidget):
    """
    A single frameless sticky note window.

    Args:
        manager:  The NoteManager that owns this note.
        text:     Initial note content.
        geo:      [x, y, w, h] geometry list; defaults to settings values.
        color:    Background hex color string; defaults to yellow.
    """

    def __init__(
        self,
        manager: "NoteManager",
        text: str = "",
        geo: Optional[list[int]] = None,
        color: Optional[str] = None,
    ) -> None:
        super().__init__(
            None,
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool,
        )

        self.manager = manager
        self._color: str = color or NOTE_COLORS[0]
        self._pinned: bool = False
        self._drag_pos: Optional[QPoint] = None

        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)
        self.setMinimumSize(180, 140)

        # Geometry
        if geo and len(geo) == 4:
            self.setGeometry(geo[0], geo[1], geo[2], geo[3])
        else:
            self.resize(280, 320)

        self._build_ui()
        self._apply_color(self._color)

        # Set text after UI is built
        self._editor.setPlainText(text)
        self._editor.textChanged.connect(self._on_text_changed)

    # ----------------------------------------------------------
    # UI CONSTRUCTION
    # ----------------------------------------------------------

    def _build_ui(self) -> None:
        """Assemble toolbar + editor + resize grip."""
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        # ── Toolbar ──────────────────────────────────────────
        toolbar = QWidget(self)
        toolbar.setObjectName("toolbar")
        toolbar.setFixedHeight(32)
        toolbar.setCursor(Qt.CursorShape.SizeAllCursor)

        tb_layout = QHBoxLayout(toolbar)
        tb_layout.setContentsMargins(6, 4, 6, 4)
        tb_layout.setSpacing(4)

        # Color dot
        self._color_dot = _ColorDot(self._color, toolbar)
        self._color_dot.clicked.connect(self._cycle_color)
        tb_layout.addWidget(self._color_dot)

        tb_layout.addStretch()

        # Pin button
        self._btn_pin = self._make_toolbar_btn("⊙", "Pin / unpin (always on top)")
        self._btn_pin.clicked.connect(self._toggle_pin)
        tb_layout.addWidget(self._btn_pin)

        # New note button
        btn_new = self._make_toolbar_btn("+", "New note")
        btn_new.clicked.connect(lambda _checked=False: self.manager.new_note())
        tb_layout.addWidget(btn_new)

        # Delete button
        btn_del = self._make_toolbar_btn("✕", "Delete this note")
        btn_del.clicked.connect(self._confirm_delete)
        tb_layout.addWidget(btn_del)

        outer.addWidget(toolbar)

        # ── Text editor ──────────────────────────────────────
        self._editor = QPlainTextEdit(self)
        self._editor.setObjectName("editor")
        self._editor.setFrameShape(QPlainTextEdit.Shape.NoFrame)
        self._editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._editor.setLineWrapMode(QPlainTextEdit.LineWrapMode.WidgetWidth)
        self._editor.setWordWrapMode(QTextOption.WrapMode.WordWrap)

        font = QFont("Segoe UI", 10)
        font.setStyleHint(QFont.StyleHint.SansSerif)
        self._editor.setFont(font)

        outer.addWidget(self._editor, stretch=1)

        # ── Resize grip ──────────────────────────────────────
        grip_row = QHBoxLayout()
        grip_row.setContentsMargins(0, 0, 2, 2)
        grip_row.addStretch()
        grip = QSizeGrip(self)
        grip.setFixedSize(16, 16)
        grip_row.addWidget(grip)
        outer.addLayout(grip_row)

    @staticmethod
    def _make_toolbar_btn(label: str, tooltip: str) -> QPushButton:
        btn = QPushButton(label)
        btn.setFixedSize(22, 22)
        btn.setToolTip(tooltip)
        btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn.setStyleSheet(
            """
            QPushButton {
                background: transparent;
                border: none;
                font-size: 13px;
                color: rgba(0,0,0,0.55);
            }
            QPushButton:hover {
                color: rgba(0,0,0,0.85);
                background: rgba(0,0,0,0.08);
                border-radius: 4px;
            }
            """
        )
        return btn

    # ----------------------------------------------------------
    # STYLING
    # ----------------------------------------------------------

    def _apply_color(self, hex_color: str) -> None:
        """Apply background color to the whole widget and style children."""
        self._color = hex_color
        self._color_dot.set_color(hex_color)

        # Darken the color slightly for the toolbar
        base = QColor(hex_color)
        toolbar_color = base.darker(115).name()

        self.setStyleSheet(
            f"""
            StickyNote {{
                background-color: {hex_color};
                border: 1px solid rgba(0,0,0,0.18);
                border-radius: 4px;
            }}
            QWidget#toolbar {{
                background-color: {toolbar_color};
                border-bottom: 1px solid rgba(0,0,0,0.12);
            }}
            QPlainTextEdit#editor {{
                background-color: {hex_color};
                color: #1a1a1a;
                padding: 8px 10px;
                border: none;
                selection-background-color: rgba(0,0,0,0.18);
            }}
            QSizeGrip {{
                background: transparent;
            }}
            """
        )

    # ----------------------------------------------------------
    # COLOR CYCLING
    # ----------------------------------------------------------

    def _cycle_color(self) -> None:
        """Advance to the next color in the palette."""
        try:
            idx = NOTE_COLORS.index(self._color)
            next_idx = (idx + 1) % len(NOTE_COLORS)
        except ValueError:
            next_idx = 0

        self._apply_color(NOTE_COLORS[next_idx])
        self.manager.schedule_save()

    # ----------------------------------------------------------
    # PIN (always-on-top)
    # ----------------------------------------------------------

    def _toggle_pin(self) -> None:
        self._pinned = not self._pinned

        flags = Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool
        if self._pinned:
            flags |= Qt.WindowType.WindowStaysOnTopHint

        # Changing flags requires a hide/show cycle on Qt.Tool windows.
        # Track visibility BEFORE the flag change so we restore correctly
        # and don't desync TrayManager's hidden-state tracking.
        was_visible = self.isVisible()
        self.hide()
        self.setWindowFlags(flags)
        if was_visible:
            self.show()

        self._btn_pin.setToolTip("Unpin (always on top)" if self._pinned else "Pin (always on top)")
        self._btn_pin.setStyleSheet(
            self._btn_pin.styleSheet() +
            ("QPushButton { color: rgba(0,0,0,0.85); }" if self._pinned else "")
        )

    # ----------------------------------------------------------
    # DELETE
    # ----------------------------------------------------------

    def _confirm_delete(self) -> None:
        """Prompt the user before permanently deleting this note."""
        # Truncate preview so the dialog stays compact
        preview = self._editor.toPlainText().strip()
        if len(preview) > 60:
            preview = preview[:60].rstrip() + "…"
        body = f'Delete this note?\n\n"{preview}"' if preview else "Delete this note?"

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Delete Note")
        dlg.setText(body)
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
        )
        dlg.setDefaultButton(QMessageBox.StandardButton.Cancel)

        # Style the dialog to match the note's background color
        dlg.setStyleSheet(
            f"""
            QMessageBox {{
                background-color: {self._color};
                color: #1a1a1a;
            }}
            QLabel {{
                color: #1a1a1a;
                font-size: 13px;
            }}
            QPushButton {{
                background-color: rgba(0,0,0,0.10);
                border: 1px solid rgba(0,0,0,0.22);
                border-radius: 4px;
                padding: 4px 16px;
                color: #1a1a1a;
                font-size: 12px;
                min-width: 64px;
            }}
            QPushButton:hover {{
                background-color: rgba(0,0,0,0.18);
            }}
            QPushButton:default {{
                border: 1px solid rgba(0,0,0,0.45);
            }}
            """
        )

        if dlg.exec() == QMessageBox.StandardButton.Yes:
            self.manager.delete_note(self)

    # ----------------------------------------------------------
    # AUTOSAVE CALLBACK
    # ----------------------------------------------------------

    def _on_text_changed(self) -> None:
        self.manager.schedule_save()

    # ----------------------------------------------------------
    # DRAG TO MOVE (frameless window)
    # ----------------------------------------------------------

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # Only drag from toolbar area (top 32px)
            if event.position().y() <= 32:
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event) -> None:
        if self._drag_pos and (event.buttons() & Qt.MouseButton.LeftButton):
            if event.position().y() <= 40:  # small tolerance
                self.move(event.globalPosition().toPoint() - self._drag_pos)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
        self.manager.schedule_save()  # persist new position
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event) -> None:
        self.manager.schedule_save()
        super().resizeEvent(event)

    # ----------------------------------------------------------
    # SERIALIZATION
    # ----------------------------------------------------------

    def to_dict(self) -> dict:
        """Serialize note state for JSON persistence."""
        geo = self.geometry()
        return {
            "text": self._editor.toPlainText(),
            "geo": [geo.x(), geo.y(), geo.width(), geo.height()],
            "color": self._color,
        }
