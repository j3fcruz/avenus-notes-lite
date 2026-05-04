# 📝 Sticky Notes

A lightweight, always-available desktop sticky notes app — inspired by Windows Sticky Notes, built with Python + PySide6.

No accounts. No encryption. No complexity. Just notes.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Instant launch** | Opens directly to your notes, no login |
| **Multiple notes** | Create unlimited floating note windows |
| **Drag & move** | Move notes anywhere on your desktop |
| **Resize** | Drag the bottom-right corner to resize |
| **Color themes** | 7 colors — click the dot to cycle |
| **Pin / always-on-top** | Keep a note visible above other windows |
| **Autosave** | Saves automatically 800ms after each edit |
| **System tray** | Minimize to tray, restore with one click |
| **Plaintext storage** | Notes saved as readable JSON — no lock-in |

---

## 📦 Installation

### Requirements
- Python 3.10+
- PySide6

### Quick Start

```bash
# Clone the repo
git clone https://github.com/yourname/sticky-notes.git
cd sticky-notes

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### Windows — Build Standalone Executable

```bash
pip install nuitka zstandard ordered-set

nuitka --onefile --windows-disable-console \
       --windows-icon-from-ico=assets/icons/sticky_icon.ico \
       --include-data-dir=assets=assets \
       --output-filename=StickyNotes.exe \
       main.py
```

---

## 🗂️ Project Structure

```
sticky-notes/
├── main.py               # Entry point
├── requirements.txt
├── README.md
│
├── config/
│   └── settings.py       # All tunable constants
│
├── core/
│   ├── note_manager.py   # Note lifecycle + autosave
│   └── storage.py        # JSON read/write (atomic)
│
├── ui/
│   ├── sticky_note.py    # Individual note window
│   └── tray.py           # System tray icon + menu
│
└── assets/
    └── icons/
        ├── sticky_icon.png
        └── sticky_icon.ico
```

---

## 🎮 Usage

### Keyboard & Mouse

| Action | How |
|---|---|
| **New note** | Click `+` in any note toolbar, or tray → *New Note* |
| **Delete note** | Click `✕` in the note toolbar |
| **Move note** | Drag the toolbar bar at the top |
| **Resize note** | Drag the bottom-right grip |
| **Cycle color** | Click the colored circle in the toolbar |
| **Pin on top** | Click `⊙` in the toolbar |
| **Hide all notes** | Left-click the tray icon |
| **Show all notes** | Left-click the tray icon again |
| **Quit** | Right-click tray → *Quit* |

---

## 💾 Data Storage

Notes are stored in a plain JSON file:

| Platform | Location |
|---|---|
| Windows (installed) | `%APPDATA%\StickyNotes\.data\notes.json` |
| Development / portable | `.data/notes.json` (next to `main.py`) |

The file is human-readable and easy to back up:

```json
[
  {
    "text": "Buy milk\nCall dentist",
    "geo": [120, 150, 280, 320],
    "color": "#fef08a"
  }
]
```

---

## 🎨 Color Palette

| Name | Hex |
|---|---|
| Yellow *(default)* | `#fef08a` |
| Green | `#bbf7d0` |
| Blue | `#bfdbfe` |
| Red/Pink | `#fecaca` |
| Purple | `#e9d5ff` |
| Orange | `#fed7aa` |
| White/Grey | `#f1f5f9` |

---

## 🔧 Configuration

Edit `config/settings.py` to customize:

```python
DEFAULT_NOTE_WIDTH  = 280     # pixels
DEFAULT_NOTE_HEIGHT = 320     # pixels
AUTOSAVE_DELAY_MS   = 800     # debounce delay
NOTE_COLORS         = [...]   # color palette list
```

---

## 📸 Screenshots

*Coming soon — contributions welcome!*

---

## 🤝 Contributing

1. Fork the repo
2. Create your branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📦 Installation

### Lite Edition (Free)
1. Download the latest release from the [Releases](https://github.com/j3fcruz/avenus-notes-lite/releases/tag/avernus-notes-lite-v1.0.0) section
2. Extract the `.zip` package
3. Run `AvernusNotesLite.exe`
4. Start taking notes instantly!

### Full Edition (Commercial)
1. Purchase and download from [Gumroad](https://patronhubdevs.gumroad.com/l/lgaqim)
2. Extract the `.zip` package
3. Run `AvernusNotes.exe`
4. Set your master password on first launch
5. (Optional) Configure keyfile authentication

---

## 📄 License

MIT License — free for personal and commercial use.

---

## 🙏 Credits

Refactored from [Avernus Secure Notes](https://github.com/yourname/avernus-notes).  
UI framework: [PySide6](https://doc.qt.io/qtforpython/) (Qt for Python).
